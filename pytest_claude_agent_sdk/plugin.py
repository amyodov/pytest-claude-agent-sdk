"""pytest-claude-agent-sdk: Pytest plugin entry point.

This module is registered as a pytest plugin via the entry point in pyproject.toml:

    [project.entry-points.pytest11]
    claude_agent_sdk = "pytest_claude_agent_sdk.plugin"

It automatically registers:
- Fixtures: claude_query, claude_client, claude_judge_client
- Marker: @pytest.mark.llm for tests that make LLM calls
"""

import pytest

# Import fixtures so they're registered with pytest
from pytest_claude_agent_sdk.fixtures import (  # noqa: F401
    claude_client,
    claude_judge_client,
    claude_query,
)

# Re-export types for user convenience
from pytest_claude_agent_sdk.spy import CallRecord, SpyClaudeSDKClient  # noqa: F401

__all__ = [
    # Fixtures
    "claude_client",
    "claude_judge_client",
    "claude_query",
    # Types
    "CallRecord",
    "SpyClaudeSDKClient",
]


def pytest_configure(config: pytest.Config) -> None:
    """Register the 'llm' marker for tests that make LLM calls.

    This allows running or skipping LLM tests selectively:
        pytest -m llm        # Run only LLM tests
        pytest -m "not llm"  # Skip LLM tests (fast CI)
    """
    config.addinivalue_line(
        "markers",
        "llm: mark test as requiring LLM calls (may be slow/costly)",
    )
