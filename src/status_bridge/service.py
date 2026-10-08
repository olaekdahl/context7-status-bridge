from __future__ import annotations

from status_bridge.models import Incident, IncidentSummary


def summarize_incidents(incidents: list[Incident]) -> IncidentSummary:
    open_incidents = [incident for incident in incidents if incident.status != "resolved"]
    major_open = [
        incident
        for incident in open_incidents
        if incident.impact in {"major", "critical"}
    ]
    sources = sorted({incident.source for incident in incidents})
    return IncidentSummary(
        total=len(incidents),
        open_count=len(open_incidents),
        major_open=len(major_open),
        sources=sources,
    )
