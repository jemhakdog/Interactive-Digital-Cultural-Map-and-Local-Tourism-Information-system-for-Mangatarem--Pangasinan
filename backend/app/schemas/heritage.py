"""Pydantic request/response schemas for Heritage endpoints."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field

# ---------- Request schemas ----------

class HeritageProfileCreate(BaseModel):
    """Create a new heritage profile."""
    asset_type: str = Field(..., min_length=1, max_length=50)
    form_control_number: str | None = Field(None, max_length=100)
    form_data: dict[str, Any] | None = None
    name_of_asset: str | None = Field(None, max_length=200)
    common_name: str | None = Field(None, max_length=200)
    barangay_id: int | None = None
    location_details: str | None = None
    contact_person: str | None = Field(None, max_length=200)
    contact_number: str | None = Field(None, max_length=50)
    ownership_type: str | None = Field(None, max_length=50)
    owner_administrator: str | None = Field(None, max_length=200)
    usage_status: str | None = Field(None, max_length=50)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    significance: str | None = None
    conservation_status: str | None = None
    template_slug: str | None = Field(None, max_length=100)
    mapper_name: str | None = Field(None, max_length=200)
    date_profiled: date | None = None
    status: str = Field(default="pending", max_length=20)


class HeritageProfileUpdate(BaseModel):
    """Partial update for a heritage profile."""
    asset_type: str | None = Field(None, min_length=1, max_length=50)
    form_control_number: str | None = Field(None, max_length=100)
    form_data: dict[str, Any] | None = None
    name_of_asset: str | None = Field(None, max_length=200)
    common_name: str | None = Field(None, max_length=200)
    barangay_id: int | None = None
    location_details: str | None = None
    contact_person: str | None = Field(None, max_length=200)
    contact_number: str | None = Field(None, max_length=50)
    ownership_type: str | None = Field(None, max_length=50)
    owner_administrator: str | None = Field(None, max_length=200)
    usage_status: str | None = Field(None, max_length=50)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    significance: str | None = None
    conservation_status: str | None = None
    template_slug: str | None = Field(None, max_length=100)
    mapper_name: str | None = Field(None, max_length=200)
    date_profiled: date | None = None
    status: str | None = Field(None, max_length=20)


# ---------- Response schemas ----------

class HeritageProfileResponse(BaseModel):
    """Single heritage profile response."""
    id: int
    asset_type: str
    form_control_number: str | None = None
    form_data: dict[str, Any] | None = None
    name_of_asset: str | None = None
    common_name: str | None = None
    barangay_id: int | None = None
    barangay_name: str | None = None
    location_details: str | None = None
    contact_person: str | None = None
    contact_number: str | None = None
    ownership_type: str | None = None
    owner_administrator: str | None = None
    usage_status: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    significance: str | None = None
    conservation_status: str | None = None
    template_slug: str | None = None
    mapper_name: str | None = None
    date_profiled: date | None = None
    status: str = "pending"
    user_id: int | None = None
    image_url: str | None = None
    category: str | None = None
    stories: str | None = None
    protection_status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool


class HeritageTypeItem(BaseModel):
    slug: str
    label: str
    label_plural: str
    count: int = 0


class HeritageTypeListResponse(BaseModel):
    types: list[HeritageTypeItem]


class HeritageListResponse(BaseModel):
    heritage_type: str
    label: str
    items: list[HeritageProfileResponse]
    pagination: PaginationMeta
