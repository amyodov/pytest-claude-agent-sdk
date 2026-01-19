---
name: complete-checkpoint
description: Run after completing significant work — implementing a feature, fixing a bug, refactoring, or any substantial code changes. Proactively ensure code quality before reporting work as done.
---

# Complete Checkpoint

After finishing a significant piece of work, run these checks:

## 1. Lint and Format

```bash
uv run ruff check --fix && uv run ruff format
```

## 2. Run Tests

```bash
uv run pytest -m "not llm" -v
```

## One-Liner

```bash
uv run ruff check --fix && uv run ruff format && uv run pytest -m "not llm" -v
```

## Behavior

1. Run the checks without asking permission
2. If everything passes: briefly report success, continue with summary
3. If anything fails: fix the issues, then re-run checks
4. Don't report work as "done" until checks pass
