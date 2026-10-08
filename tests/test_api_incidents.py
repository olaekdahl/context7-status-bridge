import sqlite3
from pathlib import Path

from fastapi.testclient import TestClient

from status_bridge.app import app
from status_bridge.db import get_connection, initialize_db
from status_bridge.models import Incident
from status_bridge.repository import IncidentRepository
from status_bridge.service import summarize_incidents

SAMPLE_INCIDENT = Incident(
    id="inc_1001",
    source="statuspage",
    title="API latency",
    impact="major",
    status="investigating",
    component_names=["Public API"],
    started_at="2026-03-27T11:30:00Z",
    resolved_at=None,
)


def test_repository_round_trip_and_summary() -> None:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    initialize_db(connection)
    repo = IncidentRepository(connection)
    repo.replace_all([SAMPLE_INCIDENT])
    incidents = repo.list_incidents()
    assert len(incidents) == 1
    assert incidents[0].title == "API latency"
    assert summarize_incidents(incidents).major_open == 1


def test_list_incidents_endpoint(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("status_bridge.db.DATABASE_PATH", tmp_path / "test.db")
    with TestClient(app) as client:
        IncidentRepository(get_connection()).replace_all([SAMPLE_INCIDENT])
        response = client.get("/incidents")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 1
        assert payload[0]["id"] == "inc_1001"
        assert payload[0]["title"] == "API latency"
        assert payload[0]["impact"] == "major"
        assert payload[0]["status"] == "investigating"


def test_incidents_summary_endpoint(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("status_bridge.db.DATABASE_PATH", tmp_path / "test.db")
    with TestClient(app) as client:
        IncidentRepository(get_connection()).replace_all([SAMPLE_INCIDENT])
        response = client.get("/incidents/summary")
        assert response.status_code == 200
        assert response.json() == {
            "total": 1,
            "open_count": 1,
            "major_open": 1,
            "sources": ["statuspage"],
            "affected_components": ["Public API"],
        }
