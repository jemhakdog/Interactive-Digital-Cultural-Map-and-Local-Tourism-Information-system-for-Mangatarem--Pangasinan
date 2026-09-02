"""Pydantic request/response schemas for Attraction endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

# ---------- Request schemas ----------

class AttractionCreate(BaseModel):
    """Create a new attraction (admin only)."""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=50)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    barangay_id: int | None = None
    image_url: str | None = None
    directions: str | None = None
    opening_hours: str | None = None
    entrance_fee: str | None = None
    contact_info: str | None = None
    facilities: str | None = None
    physical_status: str | None = "Open Public"
    is_featured: bool = False


class AttractionUpdate(BaseModel):
    """Partial update for an attraction (admin only)."""
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    category: str | None = Field(None, min_length=1, max_length=50)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    barangay_id: int | None = None
    image_url: str | None = None
    directions: str | None = None
    opening_hours: str | None = None
    entrance_fee: str | None = None
    contact_info: str | None = None
    facilities: str | None = None
    physical_status: str | None = None
    is_featured: bool | None = None
    advisory_message: str | None = None
    advisory_status: str | None = None
    status: str | None = None


class ReviewCreate(BaseModel):
    """Submit a review or reply for an attraction."""
    rating: int | None = Field(None, ge=1, le=5)
    comment: str | None = None
    parent_id: int | None = None


# ---------- Response schemas ----------

class AttractionResponse(BaseModel):
    """Public attraction detail."""
    id: int
    name: str
    description: str
    category: str
    latitude: float
    longitude: float
    image_url: str | None = None
    barangay_id: int | None = None
    barangay_name: str | None = None
    status: str
    is_featured: bool = False
    physical_status: str | None = None
    is_verified: bool | None = None
    opening_hours: str | None = None
    entrance_fee: str | None = None
    contact_info: str | None = None
    facilities: str | None = None
    advisory_message: str | None = None
    advisory_status: str | None = None
    directions: str | None = None
    osm_alternatives: Any = None
    heritage_profile_id: int | None = None
    heritage_asset_type: str | None = None
    rating: float | None = None
    created_at: datetime | None = None
    distance: float | None = None

    model_config = {"from_attributes": True}


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool


class AttractionListResponse(BaseModel):
    """Paginated list of attractions."""
    attractions: list[AttractionResponse]
    pagination: PaginationMeta


class ReviewResponse(BaseModel):
    """A single review."""
    id: int
    user_id: int
    username: str = "Visitor"
    attraction_id: int | None = None
    establishment_id: int | None = None
    rating: int | None = None
    comment: str | None = None
    status: str
    parent_id: int | None = None
    created_at: datetime | None = None
    photos: list[dict] = []
    replies: list[ReviewResponse] = []

    model_config = {"from_attributes": True}


ReviewResponse.model_rebuild()


class ReviewSummary(BaseModel):
    average: float
    total: int
    distribution: dict[str, int]


class ReviewListResponse(BaseModel):
    """Paginated reviews with summary."""
    reviews: list[ReviewResponse]
    pending_reviews: list[ReviewResponse] = []
    summary: ReviewSummary
    pagination: PaginationMeta


class ReviewCreateResponse(BaseModel):
    success: bool
    review_id: int
    photos_saved: int
    message: str
