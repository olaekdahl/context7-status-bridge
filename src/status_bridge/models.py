from __future__ import annotations

from pydantic import BaseModel, Field


class Incident(BaseModel):
    id: str = Field(min_length=2)
    source: str = Field(min_length=2)
    title: str = Field(min_length=3)
    impact: str
    status: str
    component_names: list[str]
    started_at: str
    resolved_at: str | None = None


class IncidentSummary(BaseModel):
    total: int
    open_count: int
    major_open: int
    sources: list[str]
