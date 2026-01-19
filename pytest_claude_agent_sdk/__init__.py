"""pytest-claude-agent-sdk: Pytest plugin for testing with Claude Agent SDK.

This package provides pytest fixtures for testing applications that use
the Claude Agent SDK.

Fixtures (available automatically when plugin is installed):
    claude_query: Raw query function for stateless LLM calls
    claude_client: SpyClaudeSDKClient that records calls for assertions
    claude_judge_client: Separate query function for LLM-as-judge pattern

Types (importable from this package):
    CallRecord: Dataclass capturing a single query call (prompt, kwargs, response)
    SpyClaudeSDKClient: Spy wrapper with call recording and assertion helpers

Example:
    from pytest_claude_agent_sdk import SpyClaudeSDKClient

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_my_app(claude_client: SpyClaudeSDKClient):
        await my_app(claude_client)
        claude_client.assert_called_once()
"""

from pytest_claude_agent_sdk.spy import CallRecord, SpyClaudeSDKClient

__version__ = "0.1.1"

__all__ = [
    "CallRecord",
    "SpyClaudeSDKClient",
    "__version__",
]
