# Context7 Status Bridge instructions

## What this repo is
- Small internal integration service that normalizes external status-feed incidents.

## Commands you should prefer
- Install deps: `uv sync --extra dev`
- Import fixture: `uv run python -m status_bridge.cli import-fixture`
- Run API: `uv run uvicorn status_bridge.app:app --reload`
- Run tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Show summary: `uv run python -m status_bridge.cli summary`

## Working rules
- Read `README.md`, `docs/architecture.md`, and `docs/mcp-playbook.md` before making multi-file changes.
- When a task depends on current library behavior or examples, use Context7 instead of guessing.
- Prefer focused changes over broad framework rewrites.
- If you change feed parsing or API behavior, update or add tests.
- Explain why Context7 was necessary when you use it.

## Code style
- Keep provider parsing explicit and easy to trace.
- Favor standard library and small utilities over heavy abstractions.
- Use UTC ISO timestamps in stored incident records.

## Validation expectations
- Run targeted tests first.
- Run `uv run pytest` after non-trivial changes.
- Run `uv run ruff check .` if multiple Python modules changed.
