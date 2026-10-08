# Lab review: affected_components

## 1. Feature implemented

Summary output (CLI and `GET /incidents/summary`) now includes `affected_components`: a sorted list of unique component names from open incidents only (`status != "resolved"`). Empty list when nothing is open.

## 2. Files changed

- `src/status_bridge/models.py`
- `src/status_bridge/service.py`
- `src/status_bridge/cli.py`
- `tests/test_service.py`
- `tests/test_api_incidents.py`
- `docs/lab-plan.md`

`src/status_bridge/api/incidents.py` unchanged — it already returns `summarize_incidents(...).model_dump()`.

## 3. Tests run

- `uv run pytest tests/test_service.py` — passed
- `uv run pytest tests/test_api_incidents.py` — passed
- `uv run pytest` — 7 passed

## 4. Command output verified

After `import-fixture`, `uv run python -m status_bridge.cli summary` returned existing fields plus:

```json
"affected_components": [
  "Background Jobs",
  "Public API"
]
```

## 5. Risk / edge case worth watching

Blank or placeholder component names (e.g. feed fallback `"unknown"`) are included as-is; there is no normalization or filtering of empty strings.

## 6. Intentionally out of scope

Feed parsing, DB/repository changes, and including components from resolved incidents.
