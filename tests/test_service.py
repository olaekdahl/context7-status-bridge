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
