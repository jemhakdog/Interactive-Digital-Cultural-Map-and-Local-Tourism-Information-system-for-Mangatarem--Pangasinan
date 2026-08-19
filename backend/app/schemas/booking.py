"""Pydantic schemas for the Booking module."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class AvailabilityResponse(BaseModel):
    asset_id: int
    date: str
    available_capacity: int
    daily_capacity: int


class ReserveRequest(BaseModel):
    asset_id: int
    date: str = Field(..., description="YYYY-MM-DD")
    party_size: int = Field(1, ge=1)
    contact: str = ""


class ReserveResponse(BaseModel):
    success: bool
    reservation_id: int
    status: str
    qr_token: str | None = None
    idempotent: bool | None = None


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    booking_slot_id: int
    party_size: int
    primary_contact: str | None = None
    status: str
    qr_code_token: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class UpdateStatusRequest(BaseModel):
    reservation_id: int
    status: str = Field(..., description="pending, confirmed, cancelled, attended, no-show")


class VerifyArrivalRequest(BaseModel):
    latitude: float
    longitude: float
    navigated_target_id: int | None = None
    navigated_target_type: str | None = None


class VerifyArrivalResponse(BaseModel):
    success: bool
    booking_attended: bool = False
    navigated_arrived: bool = False
    place_name: str = ""
    target_id: int | None = None
    target_type: str | None = None
