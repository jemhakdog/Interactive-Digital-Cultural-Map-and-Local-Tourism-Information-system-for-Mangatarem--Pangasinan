"""Pydantic schemas for the Analytics module."""
from __future__ import annotations

from pydantic import BaseModel, Field


class VisitorLogRequest(BaseModel):
    visitor_name: str | None = None
    visitor_age: int | None = None
    visitor_address: str | None = None
    is_system_user: bool = False
    visitor_count: int = Field(1, ge=1)
    notes: str | None = None
