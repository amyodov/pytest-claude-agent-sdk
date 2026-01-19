# pytest-claude-agent-sdk

Pytest plugin for testing applications built with Claude Agent SDK.

See README.md for installation, fixtures API, and usage examples.

## Technology Foundation

- **claude-agent-sdk** — The agent framework being tested (docs via Context7)
- **pytest** — Test framework, plugin registration via entry points

## Architecture

- `spy.py` — SpyClaudeSDKClient wraps `query()` to record calls while passing through to LLM
- `fixtures.py` — Three fixtures: `claude_query`, `claude_client` (spy), `claude_judge_client`
- `plugin.py` — Pytest entry point, registers fixtures and `llm` marker

## Development Commands

```bash
uv sync                    # Install dependencies
uv run pytest              # Run all tests
uv run pytest -m "not llm" # Skip LLM tests (fast)
uv run ruff check .        # Lint
uv run ruff format .       # Format
```

## Pre-Commit Checklist

Before committing, run:

```bash
uv run ruff check --fix && uv run ruff format
uv run pytest -m "not llm" -v
```

For release commits, also run LLM tests:

```bash
uv run pytest -v
```

## Code Standards

- Python 3.10+ type hints
- Ruff linting (E, F, I, W rules)
- Use `@pytest.mark.llm` for tests making actual LLM calls

## Documentation Strategy

**Docstrings are the source of truth.** The `llms.txt` file links to source files, and tools like Context7 read the docstrings directly.

When modifying code:
1. Update docstrings in the same commit as code changes
2. Include: description, Args, Returns/Yields, Raises, Example where appropriate
3. Update `llms.txt` if adding/removing/renaming public APIs
4. Keep README.md examples in sync with actual API

Files with public API docstrings:
- `pytest_claude_agent_sdk/__init__.py` — Package overview
- `pytest_claude_agent_sdk/spy.py` — CallRecord, SpyClaudeSDKClient
- `pytest_claude_agent_sdk/fixtures.py` — Fixture definitions
- `pytest_claude_agent_sdk/plugin.py` — Plugin entry point
