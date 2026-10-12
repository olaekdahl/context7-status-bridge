from status_bridge.models import Incident
from status_bridge.service import summarize_incidents


def _incidents() -> list[Incident]:
    return [
        Incident(
            id="inc_1001",
            source="statuspage",
            title="API latency",
            impact="major",
            status="investigating",
            component_names=["Public API"],
            started_at="2026-03-27T11:30:00Z",
            resolved_at=None,
        ),
        Incident(
            id="inc_1002",
            source="statuspage",
            title="Webhook delay",
            impact="minor",
            status="resolved",
            component_names=["Webhooks"],
            started_at="2026-03-26T08:15:00Z",
            resolved_at="2026-03-26T09:05:00Z",
        ),
    ]


def test_summary_counts_open_and_major_incidents() -> None:
    summary = summarize_incidents(_incidents())
    assert summary.total == 2
    assert summary.open_count == 1
    assert summary.major_open == 1
    assert summary.sources == ["statuspage"]
    assert summary.affected_components == ["Public API"]
    assert summary.open_titles == ["API latency"]


def test_summary_affected_components_open_only_unique_and_sorted() -> None:
    incidents = [
        Incident(
            id="inc_2001",
            source="statuspage",
            title="API and dashboard issues",
            impact="major",
            status="investigating",
            component_names=["Webhooks", "Dashboard"],
            started_at="2026-03-27T11:30:00Z",
            resolved_at=None,
        ),
        Incident(
            id="inc_2002",
            source="statuspage",
            title="API partial outage",
            impact="critical",
            status="identified",
            component_names=["Public API", "Webhooks"],
            started_at="2026-03-27T12:00:00Z",
            resolved_at=None,
        ),
        Incident(
            id="inc_2003",
            source="statuspage",
            title="Resolved cache blip",
            impact="minor",
            status="resolved",
            component_names=["Cache"],
            started_at="2026-03-26T08:15:00Z",
            resolved_at="2026-03-26T09:05:00Z",
        ),
    ]
    summary = summarize_incidents(incidents)
    assert summary.affected_components == ["Dashboard", "Public API", "Webhooks"]


def test_summary_open_titles_open_only_unique_and_sorted() -> None:
    incidents = [
        Incident(
            id="inc_3001",
            source="statuspage",
            title="Webhook delay",
            impact="major",
            status="investigating",
            component_names=["Webhooks"],
            started_at="2026-03-27T11:30:00Z",
            resolved_at=None,
        ),
        Incident(
            id="inc_3002",
            source="statuspage",
            title="API latency",
            impact="critical",
            status="identified",
            component_names=["Public API"],
            started_at="2026-03-27T12:00:00Z",
            resolved_at=None,
        ),
        Incident(
            id="inc_3003",
            source="statuspage",
            title="API latency",
            impact="minor",
            status="monitoring",
            component_names=["Public API"],
            started_at="2026-03-27T12:30:00Z",
            resolved_at=None,
        ),
        Incident(
            id="inc_3004",
            source="statuspage",
            title="Resolved cache blip",
            impact="minor",
            status="resolved",
            component_names=["Cache"],
            started_at="2026-03-26T08:15:00Z",
            resolved_at="2026-03-26T09:05:00Z",
        ),
    ]
    summary = summarize_incidents(incidents)
    assert summary.open_titles == ["API latency", "Webhook delay"]
    assert summary.affected_components == ["Public API", "Webhooks"]
