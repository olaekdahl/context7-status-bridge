from __future__ import annotations

import json
import sqlite3

from status_bridge.models import Incident


class IncidentRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def replace_all(self, incidents: list[Incident]) -> None:
        self.connection.execute("DELETE FROM incidents")
        for incident in incidents:
            self.connection.execute(
                """
                INSERT INTO incidents (id, source, title, impact, status, component_names, started_at, resolved_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    incident.id,
                    incident.source,
                    incident.title,
                    incident.impact,
                    incident.status,
                    json.dumps(incident.component_names),
                    incident.started_at,
                    incident.resolved_at,
                ),
            )
        self.connection.commit()

    def list_incidents(self) -> list[Incident]:
        rows = self.connection.execute(
            """
            SELECT id, source, title, impact, status, component_names, started_at, resolved_at
            FROM incidents
            ORDER BY started_at DESC, id DESC
            """
        ).fetchall()
        incidents: list[Incident] = []
        for row in rows:
            incidents.append(
                Incident(
                    id=row["id"],
                    source=row["source"],
                    title=row["title"],
                    impact=row["impact"],
                    status=row["status"],
                    component_names=json.loads(row["component_names"]),
                    started_at=row["started_at"],
                    resolved_at=row["resolved_at"],
                )
            )
        return incidents
