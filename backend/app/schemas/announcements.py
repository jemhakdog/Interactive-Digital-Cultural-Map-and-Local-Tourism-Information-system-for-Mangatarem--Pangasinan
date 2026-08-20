"""Pydantic schemas for Announcement endpoints."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class AnnouncementCreate(BaseModel):
    """Create/update an announcement (contributor or admin)."""
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10, max_length=5000)
    barangay_id: int | None = None


class AnnouncementResponse(BaseModel):
    """Announcement as returned to clients."""
    id: int
    title: str
    content: str | None = None
    status: str
    barangay_id: int | None = None
    barangay_name: str | None = None
    author_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
