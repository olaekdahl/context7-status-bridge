from status_bridge.feeds import statuspage_to_incidents


def test_statuspage_payload_maps_to_internal_incidents() -> None:
    payload = {
        "incidents": [
            {
                "id": "inc_1",
                "name": "API issue",
                "status": "investigating",
                "impact": "major",
                "created_at": "2026-03-27T11:30:00Z",
                "resolved_at": None,
                "components": [{"name": "API"}],
            }
        ]
    }
    incidents = statuspage_to_incidents(payload)
    assert len(incidents) == 1
    assert incidents[0].title == "API issue"
    assert incidents[0].component_names == ["API"]
