"""Pydantic schemas for the Gallery module."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class GalleryItemResponse(BaseModel):
    id: int
    title: str | None = None
    description: str | None = None
    media_url: str | None = None
    media_type: str | None = None
    status: str | None = None
    user_id: int | None = None
    barangay: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class GalleryListResponse(BaseModel):
    items: list[GalleryItemResponse]
    pagination: dict[str, Any]
    barangays: list[str]
