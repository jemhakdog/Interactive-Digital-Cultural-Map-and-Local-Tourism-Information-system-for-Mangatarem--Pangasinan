"""Pydantic schemas for the Business module."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

# ── Establishment ──────────────────────────────────────────────

class EstablishmentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    type: str = Field(..., description="inn, restaurant, cafe, fastfood")
    description: str = Field("", max_length=2000)
    address: str = Field(..., min_length=1, max_length=300)
    latitude: float
    longitude: float
    barangay_name: str | None = None
    contact_number: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=100)
    website: str | None = Field(None, max_length=200)
    price_range: str | None = Field(None, max_length=10)
    amenities: list[str] | None = None
    operating_hours: dict[str, str] | None = None


class EstablishmentUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    type: str | None = None
    description: str | None = Field(None, max_length=2000)
    address: str | None = Field(None, min_length=1, max_length=300)
    latitude: float | None = None
    longitude: float | None = None
    barangay_name: str | None = None
    contact_number: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=100)
    website: str | None = Field(None, max_length=200)
    price_range: str | None = Field(None, max_length=10)
    amenities: list[str] | None = None
    operating_hours: dict[str, str] | None = None


class EstablishmentResponse(BaseModel):
    id: int
    name: str
    type: str | None = None
    description: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    contact_number: str | None = None
    email: str | None = None
    website: str | None = None
    price_range: str | None = None
    rating_avg: float | None = None
    review_count: int | None = None
    cover_image_url: str | None = None
    logo_url: str | None = None
    amenities: list[str] | None = None
    operating_hours: dict[str, str] | None = None
    barangay: str | None = None
    owner_id: int | None = None
    status: str | None = None
    is_featured: bool | None = None
    created_at: datetime | None = None
    distance: float | None = None

    model_config = {"from_attributes": True}


class EstablishmentListResponse(BaseModel):
    establishments: list[EstablishmentResponse]
    pagination: dict[str, Any]


# ── Room ───────────────────────────────────────────────────────

class RoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=1000)
    price_per_night: float | None = Field(None, ge=0)
    capacity: int = Field(2, ge=1, le=100)
    is_available: bool = True
    amenities: list[str] | None = None
    image_urls: list[str] | None = None


class RoomUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    price_per_night: float | None = Field(None, ge=0)
    capacity: int | None = Field(None, ge=1, le=100)
    is_available: bool | None = None
    amenities: list[str] | None = None
    image_urls: list[str] | None = None


class RoomResponse(BaseModel):
    id: int
    establishment_id: int
    name: str
    description: str | None = None
    price_per_night: float | None = None
    capacity: int | None = None
    is_available: bool | None = None
    amenities: list[str] | None = None
    image_urls: list[str] | None = None

    model_config = {"from_attributes": True}


# ── Menu Item ──────────────────────────────────────────────────

class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=1000)
    price: float | None = Field(None, ge=0)
    category: str = Field(..., min_length=1, max_length=100)
    is_available: bool = True
    is_bestseller: bool = False
    image_url: str | None = None


class MenuItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    price: float | None = Field(None, ge=0)
    category: str | None = Field(None, min_length=1, max_length=100)
    is_available: bool | None = None
    is_bestseller: bool | None = None
    image_url: str | None = None


class MenuItemResponse(BaseModel):
    id: int
    establishment_id: int
    name: str
    description: str | None = None
    price: float | None = None
    category: str | None = None
    image_url: str | None = None
    is_available: bool | None = None
    is_bestseller: bool | None = None

    model_config = {"from_attributes": True}


# ── Review ─────────────────────────────────────────────────────

class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., max_length=2000)


class ReviewReply(BaseModel):
    comment: str = Field(..., min_length=1, max_length=2000)


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    establishment_id: int
    rating: int | None = None
    comment: str | None = None
    parent_id: int | None = None
    status: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
