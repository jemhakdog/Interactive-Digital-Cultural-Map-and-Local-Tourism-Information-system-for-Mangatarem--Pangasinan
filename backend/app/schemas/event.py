"""Pydantic request/response schemas for Event endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

# ---------- Request schemas ----------

class EventCreate(BaseModel):
    """Create a new event (admin only)."""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    date: datetime
    location: str = Field(..., min_length=1, max_length=255)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    barangay_id: int | None = None
    image_url: str | None = None
    category: str = Field("Civic", max_length=50)


class EventUpdate(BaseModel):
    """Partial update for an event (admin only)."""
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    date: datetime | None = None
    location: str | None = Field(None, min_length=1, max_length=255)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    barangay_id: int | None = None
    image_url: str | None = None
    category: str | None = Field(None, max_length=50)
    status: str | None = None


# ---------- Response schemas ----------

class EventResponse(BaseModel):
    """Public event detail."""
    id: int
    name: str
    description: str
    date: datetime | None = None
    location: str
    latitude: float | None = None
    longitude: float | None = None
    barangay_id: int | None = None
    barangay_name: str | None = None
    image_url: str | None = None
    category: str
    status: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class EventListResponse(BaseModel):
    """Paginated list of events."""
    events: list[EventResponse]
    pagination: PaginationMeta


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool


# Fix forward ref
EventListResponse.model_rebuild()
