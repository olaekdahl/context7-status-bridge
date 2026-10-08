    #!/usr/bin/env bash
    set -euo pipefail
    uv sync --extra dev
    uv run python -m status_bridge.cli import-fixture
    printf '
Bootstrap complete.
'
    printf 'Run the API with: uv run uvicorn status_bridge.app:app --reload
'
