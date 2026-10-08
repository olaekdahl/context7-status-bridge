#!/usr/bin/env bash
set -euo pipefail
uv run uvicorn status_bridge.app:app --reload
