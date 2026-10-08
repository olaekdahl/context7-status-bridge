# Architecture

Context7 Status Bridge uses a small integration-service shape:

- **FastAPI app** exposes health and incident summary endpoints.
- **SQLite** stores normalized incidents locally for labs.
- **Feed parser** translates a provider payload into internal records.
- **Repository layer** isolates storage concerns.
- **CLI** supports fixture import and summary output.

The code is deliberately small, but the work is the kind of work where current docs help:

- FastAPI patterns change over time
- `httpx` usage details matter for fetching and testing
- students can compare repo-only reasoning with repo + Context7 grounding
- `feeds.py` is a good target for provider-specific parsing work.
- `app.py` is a good place to evaluate startup guidance against current FastAPI docs.
- `repository.py` and `service.py` are good for small feature additions without large rewrites.
