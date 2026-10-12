# On-call handoff checklist

Use this when you are on call for Context7 Status Bridge and need to read or change a status summary field.

## What this service does

Context7 Status Bridge is a small integration service that normalizes external status-feed incidents into local records.

- The FastAPI app exposes health and incident summary endpoints.
- SQLite stores normalized incidents locally for labs.
- The feed parser translates a provider payload into internal records.
- The repository layer isolates storage concerns.
- The CLI supports fixture import and summary output.

## Commands that produce the summary

Print the stored summary from the CLI:

```bash
uv run python -m status_bridge.cli summary
```

The same summary is also served by the API. Start the app, then request the incident summary endpoint:

```bash
uv run uvicorn status_bridge.app:app --reload
```

`GET /incidents/summary` at `http://127.0.0.1:8000/incidents/summary`.

## Files a summary-field change may touch

Read `AGENTS.md` and `docs/architecture.md` before editing a summary field. Keep the field derived from open incidents unless the task says otherwise. Update the summary model, the service, the CLI output, and a focused test together.

A summary-field change may touch only these files:

- `src/status_bridge/models.py`
- `src/status_bridge/service.py`
- `src/status_bridge/cli.py`
- `tests/test_service.py`
- `tests/test_api_incidents.py`

Leave every other file unchanged unless a real defect forces another edit.

## Tests to run before review

Run the focused service tests first, then the full suite:

```bash
uv run pytest tests/test_service.py
uv run pytest
```
