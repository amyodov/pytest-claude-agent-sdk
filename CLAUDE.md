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
```

## Code Standards

- Python 3.10+ type hints
- Ruff linting (E, F, I, W rules)
- Use `@pytest.mark.llm` for tests making actual LLM calls
