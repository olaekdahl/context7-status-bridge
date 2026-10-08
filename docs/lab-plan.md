# Add affected_components to summary

## Goal

Extend summary output (CLI `summary` and `GET /incidents/summary`) with `affected_components`: a sorted list of unique component names taken only from open incidents (`status != "resolved"`), matching how `open_count` is already computed.

## Likely edit targets

- [`src/status_bridge/models.py`](../src/status_bridge/models.py) — add `affected_components: list[str]` to `IncidentSummary`
- [`src/status_bridge/service.py`](../src/status_bridge/service.py) — in `summarize_incidents`, collect names from `open_incidents` via set comprehension, then `sorted(...)`
- [`src/status_bridge/cli.py`](../src/status_bridge/cli.py) — add the same field to `SummaryOutput` so CLI JSON stays aligned with the model
- [`tests/test_service.py`](../tests/test_service.py) — assert open-only uniqueness/sorting
- [`tests/test_api_incidents.py`](../tests/test_api_incidents.py) — include `affected_components` in the expected `/incidents/summary` payload

[`src/status_bridge/api/incidents.py`](../src/status_bridge/api/incidents.py) stays as-is: it already returns `summarize_incidents(...).model_dump()`.

Core aggregation (reuse existing `open_incidents`):

```python
affected_components = sorted({
    name
    for incident in open_incidents
    for name in incident.component_names
})
```

## Tests to add or update first

Update tests before (or with) the production change so the contract is locked:

1. **`tests/test_service.py`** — extend `test_summary_counts_open_and_major_incidents` (or add a focused sibling) so that:
   - open incident’s `"Public API"` appears
   - resolved incident’s `"Webhooks"` does not
   - expected value is `affected_components == ["Public API"]`
2. **`tests/test_api_incidents.py`** — update `test_incidents_summary_endpoint` expected JSON to include `"affected_components": ["Public API"]`

No new test files; no feed/repository test changes.

## Validation order

1. `uv run pytest tests/test_service.py tests/test_api_incidents.py`
2. `uv run pytest`
3. `uv run ruff check .` (multiple Python modules touched)
4. Manual smoke (optional): `uv run python -m status_bridge.cli summary` after fixture import — expect `affected_components` for the single open fixture incident

## Out-of-scope items

- Feed parsing (`feeds.py`), DB schema, or repository changes (`component_names` already stored)
- Changing the definition of “open”
- Including components from resolved incidents
- New endpoints, query params, or severity-filtered component lists
- Docs rewrites beyond what is required for the code change
