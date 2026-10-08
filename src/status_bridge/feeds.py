from __future__ import annotations

import json
from pathlib import Path

import httpx

from status_bridge.models import Incident


def load_statuspage_fixture(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fetch_statuspage_payload(url: str, timeout: float = 5.0) -> dict:
    response = httpx.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def statuspage_to_incidents(payload: dict, source: str = "statuspage") -> list[Incident]:
    incidents: list[Incident] = []
    for row in payload.get("incidents", []):
        incidents.append(
            Incident(
                id=str(row["id"]),
                source=source,
                title=row["name"],
                impact=row.get("impact", "unknown"),
                status=row.get("status", "unknown"),
                component_names=[component.get("name", "unknown") for component in row.get("components", [])],
                started_at=row["created_at"],
                resolved_at=row.get("resolved_at"),
            )
        )
    return incidents
