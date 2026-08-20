"""Pydantic schemas for admin moderation endpoints."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ReviewModerationResponse(BaseModel):
    """A review pending/under moderation."""
    id: int
    user_name: str | None = None
    rating: int | None = None
    comment: str | None = None
    status: str
    location: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class EstablishmentModerationResponse(BaseModel):
    """Establishment row in the admin business directory."""
    id: int
    name: str
    type: str | None = None
    status: str | None = None
    barangay: str | None = None
    owner_name: str | None = None
    cover_image_url: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class MerchantPendingResponse(BaseModel):
    """Pending business-verification applicant (verify-merchants view)."""
    id: int
    name: str
    type: str | None = None
    status: str | None = None
    barangay: str | None = None
    owner_name: str | None = None
    cover_image_url: str | None = None

    model_config = {"from_attributes": True}


class UserPendingResponse(BaseModel):
    """A user pending approval / shown in the admin user table."""
    id: int
    username: str
    name: str
    email: str
    role: str
    is_approved: bool
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
