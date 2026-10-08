from __future__ import annotations

import os
from pathlib import Path

APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "data/dev.db"))
STATUSPAGE_FIXTURE_PATH = Path(
    os.getenv("STATUSPAGE_FIXTURE_PATH", "data/fixtures/statuspage_sample.json")
)
