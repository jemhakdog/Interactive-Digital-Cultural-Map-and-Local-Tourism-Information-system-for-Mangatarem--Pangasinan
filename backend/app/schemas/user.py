"""Pydantic schemas for the /api/user (tourist profile) endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """Full read-only user profile (extends auth.UserResponse)."""
    id: int
    username: str
    email: str
    name: str
    role: str
    is_approved: bool
    barangay_id: int | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class UserStatsResponse(BaseModel):
    """Aggregate dashboard stats for the current user."""
    favorites_count: int = 0
    reviews_count: int = 0
    visits_count: int = 0
    check_ins_count: int = 0
    total_stamps: int = 0


class FavoriteResponse(BaseModel):
    """A user's saved favorite (attraction / establishment / event)."""
    id: int
    user_id: int
    attraction_id: int | None = None
    establishment_id: int | None = None
    event_id: int | None = None
    status: str | None = None
    created_at: datetime | None = None
    # Optional denormalized display fields
    name: str | None = None
    type: str | None = None

    model_config = {"from_attributes": True}


class VisitResponse(BaseModel):
    """A visit logged by/for the current user."""
    id: int
    target_type: str
    target_id: int
    target_name: str | None = None
    visit_date: datetime | None = None
    visitor_count: int = 1
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
