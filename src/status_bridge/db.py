from __future__ import annotations

import sqlite3
from pathlib import Path

from status_bridge.config import DATABASE_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS incidents (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    impact TEXT NOT NULL,
    status TEXT NOT NULL,
    component_names TEXT NOT NULL,
    started_at TEXT NOT NULL,
    resolved_at TEXT
);
"""


def get_connection() -> sqlite3.Connection:
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA)
    connection.commit()
