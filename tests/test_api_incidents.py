import sqlite3

from status_bridge.db import initialize_db
from status_bridge.models import Incident
from status_bridge.repository import IncidentRepository
from status_bridge.service import summarize_incidents


def test_repository_round_trip_and_summary() -> None:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    initialize_db(connection)
    repo = IncidentRepository(connection)
    repo.replace_all(
        [
            Incident(
                id="inc_1001",
                source="statuspage",
                title="API latency",
                impact="major",
                status="investigating",
                component_names=["Public API"],
                started_at="2026-03-27T11:30:00Z",
                resolved_at=None,
            )
        ]
    )
    incidents = repo.list_incidents()
    assert len(incidents) == 1
    assert incidents[0].title == "API latency"
    assert summarize_incidents(incidents).major_open == 1
