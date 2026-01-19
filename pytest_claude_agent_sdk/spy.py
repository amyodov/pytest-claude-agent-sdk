"""Spy wrapper for claude_agent_sdk.query()."""

from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Optional

from claude_agent_sdk import Message, ResultMessage
from claude_agent_sdk import query as sdk_query


@dataclass
class CallRecord:
    """Record of a single call to query().

    Captures the prompt, any additional keyword arguments, and the final response.

    Attributes:
        prompt: The prompt string sent to the LLM.
        kwargs: Additional keyword arguments passed to query() (e.g., options).
        response: The final ResultMessage from the LLM, or None if not yet received.

    Properties:
        result: Shortcut to get response.result (the text output), or None.

    Example:
        record = client.last_call
        print(record.prompt)      # "What is 2+2?"
        print(record.result)      # "4"
        print(record.kwargs)      # {"options": ClaudeAgentOptions(...)}
    """

    prompt: str
    kwargs: dict[str, Any] = field(default_factory=dict)
    response: Optional[ResultMessage] = None

    @property
    def result(self) -> Optional[str]:
        """Shortcut to get the result text from the response."""
        return self.response.result if self.response else None


class SpyClaudeSDKClient:
    """A spy wrapper around claude_agent_sdk.query() that records all calls.

    Provides a client-like interface that can be injected into code under test.
    All calls go through to the real LLM, but are also recorded for inspection
    and assertions in tests.

    The query() method accepts the same arguments as claude_agent_sdk.query(),
    including ClaudeAgentOptions for configuring model, tools, permissions, etc.

    Attributes:
        calls: List of all CallRecord objects for queries made.
        call_count: Number of queries made.
        last_call: Most recent CallRecord (or None if no calls).

    Example:
        @pytest.mark.asyncio
        async def test_my_app(claude_client: SpyClaudeSDKClient):
            # Use in your app - real LLM calls happen
            await my_app(claude_client)

            # Inspect what happened
            assert claude_client.call_count == 1
            assert "chess" in claude_client.calls[0].prompt

            # Use assertion helpers
            claude_client.assert_called_once()
            claude_client.assert_any_call_contains("chess")
    """

    def __init__(self) -> None:
        self.calls: list[CallRecord] = []

    @property
    def call_count(self) -> int:
        """Number of queries made."""
        return len(self.calls)

    @property
    def last_call(self) -> Optional[CallRecord]:
        """Most recent call, or None if no calls made."""
        return self.calls[-1] if self.calls else None

    async def query(self, prompt: str, **kwargs: Any) -> AsyncIterator[Message]:
        """Query the LLM and record the call.

        All arguments are passed through to claude_agent_sdk.query().

        Args:
            prompt: The prompt to send to the LLM.
            **kwargs: Additional arguments, typically including:
                - options: ClaudeAgentOptions for model, tools, permissions, etc.

        Yields:
            Message objects from the LLM. Common types:
                - AssistantMessage: Claude's response with content blocks
                - ResultMessage: Final message with result text and cost info

        Example:
            from claude_agent_sdk import ClaudeAgentOptions, ResultMessage

            options = ClaudeAgentOptions(max_turns=1)
            async for msg in client.query("Hello", options=options):
                if isinstance(msg, ResultMessage):
                    print(msg.result)
        """
        record = CallRecord(prompt=prompt, kwargs=kwargs)
        self.calls.append(record)

        # Use the standalone query function which handles connection internally
        async for msg in sdk_query(prompt=prompt, **kwargs):
            if isinstance(msg, ResultMessage):
                record.response = msg
            yield msg

    # ==================== Assertion helpers ====================

    def assert_called(self) -> None:
        """Assert that at least one call was made.

        Raises:
            AssertionError: If no calls were made.
        """
        assert self.call_count > 0, "Expected at least one call, but none were made"

    def assert_not_called(self) -> None:
        """Assert that no calls were made.

        Raises:
            AssertionError: If any calls were made.
        """
        assert self.call_count == 0, f"Expected no calls, but {self.call_count} were made"

    def assert_called_once(self) -> None:
        """Assert that exactly one call was made.

        Raises:
            AssertionError: If call count is not exactly 1.
        """
        assert self.call_count == 1, f"Expected exactly one call, but {self.call_count} were made"

    def assert_call_count(self, expected: int) -> None:
        """Assert that exactly `expected` calls were made.

        Args:
            expected: The expected number of calls.

        Raises:
            AssertionError: If call count doesn't match expected.
        """
        assert self.call_count == expected, (
            f"Expected {expected} calls, but {self.call_count} were made"
        )

    def assert_any_call_contains(self, substring: str) -> None:
        """Assert that at least one call's prompt contains the substring.

        Args:
            substring: The substring to search for in prompts.

        Raises:
            AssertionError: If no call's prompt contains the substring.
        """
        for call in self.calls:
            if substring in call.prompt:
                return
        prompts = [call.prompt for call in self.calls]
        raise AssertionError(f"No call contained '{substring}'. Prompts were: {prompts}")

    def assert_last_call_contains(self, substring: str) -> None:
        """Assert that the last call's prompt contains the substring.

        Args:
            substring: The substring to search for.

        Raises:
            AssertionError: If no calls were made or substring not in last prompt.
        """
        assert self.last_call is not None, "No calls were made"
        assert substring in self.last_call.prompt, (
            f"Last call prompt did not contain '{substring}'. Prompt was: {self.last_call.prompt}"
        )

    def reset_calls(self) -> None:
        """Clear the call history.

        Use between test cases or when you need to reset state.
        """
        self.calls.clear()
