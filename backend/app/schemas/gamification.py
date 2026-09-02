"""Pydantic schemas for the Gamification module."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class StartNavigationRequest(BaseModel):
    id: int
    type: str = "attraction"


class CheckinRequest(BaseModel):
    type: str = Field(..., description="attraction or establishment")
    id: int
    latitude: float
    longitude: float


class CheckinBadgeResponse(BaseModel):
    title: str
    description: str
    badge_image_url: str | None = None
    reward_promo: str | None = None


class CheckinResponse(BaseModel):
    success: bool
    message: str
    distance: int | None = None
    already_checked_in: bool = False
    unlocked_badges: list[CheckinBadgeResponse] = []
