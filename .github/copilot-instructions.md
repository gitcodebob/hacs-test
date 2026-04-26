# Copilot Workspace Instructions

## Python package management

Always use **uv** instead of pip or python -m venv for all Python package and environment operations.

| Task | Command |
|------|---------|
| Install / sync dependencies | `uv sync --group dev` |
| Add a package | `uv add --group dev <package>` |
| Run a tool in the venv | `uv run <command>` |
| Run tests | `uv run pytest tests/ -v` |

Never suggest `pip install`, `python -m venv`, or bare `pytest` invocations.
