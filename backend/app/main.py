"""HTTP API for the internship board.

Run from the backend folder:  uvicorn app.main:app --reload
Interactive docs:             http://localhost:8000/docs
"""

import os
from collections.abc import Iterator
from typing import Annotated

import psycopg
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app import queries
from app.db import get_connection
from app.models import JobsPage

app = FastAPI(title="Internship Board API")

# Browsers block a website from calling an API on another address unless the API allows it.
# The deployed site's address is added through the ALLOWED_ORIGINS setting (comma-separated).
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware, allow_origins=allowed_origins, allow_methods=["GET"], allow_headers=["*"]
)


def get_db() -> Iterator[psycopg.Connection]:
    """Give each request its own connection, closed automatically when the request ends."""
    with get_connection() as conn:
        yield conn


Db = Annotated[psycopg.Connection, Depends(get_db)]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/jobs", response_model=JobsPage)
def get_jobs(
    db: Db,
    search: str | None = None,
    category: str | None = None,
    location: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    total, items = queries.list_jobs(db, search, category, location, limit, offset)
    return {"total": total, "items": items}


@app.get("/api/categories")
def get_categories(db: Db) -> list[str]:
    return queries.list_categories(db)
