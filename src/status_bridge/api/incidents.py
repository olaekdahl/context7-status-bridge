from __future__ import annotations

from fastapi import APIRouter

from status_bridge.db import get_connection
from status_bridge.models import Incident
from status_bridge.repository import IncidentRepository
from status_bridge.service import summarize_incidents

router = APIRouter(prefix="/incidents", tags=["incidents"])


def _repo() -> IncidentRepository:
    return IncidentRepository(get_connection())


@router.get("", response_model=list[Incident])
def list_incidents() -> list[Incident]:
    return _repo().list_incidents()


@router.get("/summary")
def incident_summary() -> dict:
    incidents = _repo().list_incidents()
    return summarize_incidents(incidents).model_dump()
