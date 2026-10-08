from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from status_bridge.api.health import router as health_router
from status_bridge.api.incidents import router as incidents_router
from status_bridge.db import get_connection, initialize_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db(get_connection())
    yield

app = FastAPI(
    title="Context7 Status Bridge", 
    version="0.1.0", 
    lifespan=lifespan,
)
app.include_router(health_router)
app.include_router(incidents_router)
