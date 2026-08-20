"""Pydantic schemas for BarangayInfo endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class BarangayInfoResponse(BaseModel):
    """Barangay profile + list item.

    `attraction_count`, `image_url`, `tags`, and `category` are computed/derived
    fields populated by the router (not stored on the model).
    """
    id: int
    name: str
    mission: str | None = None
    vision: str | None = None
    history: str | None = None
    cultural_assets: str | None = None
    traditions: str | None = None
    local_practices: str | None = None
    unique_features: str | None = None
    user_id: int | None = None
    created_at: datetime | None = None
    map_geo_json: Any = None
    location_data: Any = None
    # Derived list fields
    attraction_count: int | None = None
    image_url: str | None = None
    tags: list[str] | None = None
    category: str | None = None

    model_config = {"from_attributes": True}


class BarangayInfoUpdate(BaseModel):
    """Barangay profile edit (contributor manager / admin)."""
    name: str | None = Field(None, min_length=1, max_length=100)
    mission: str | None = None
    vision: str | None = None
    history: str | None = None
    cultural_assets: str | None = None
    traditions: str | None = None
    local_practices: str | None = None
    unique_features: str | None = None
    map_geo_json: Any = None
    location_data: Any = None
