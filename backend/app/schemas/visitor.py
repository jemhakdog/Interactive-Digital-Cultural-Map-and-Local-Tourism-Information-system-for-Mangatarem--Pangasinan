"""Pydantic schemas for admin Visitor registry / visits endpoints."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel


class VisitResponse(BaseModel):
    """A single visitor-log entry (admin registry view)."""
    id: int
    visitor_name: str | None = None
    visitor_age: int | None = None
    visitor_address: str | None = None
    target_type: str
    target_id: int
    target_name: str | None = None
    visit_date: date | None = None
    steward: str | None = None
    visitor_count: int = 1
    is_system_user: bool = False
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class VisitorRegistryResponse(BaseModel):
    """Paginated visitor registry list."""
    visitors: list[VisitResponse]
    total: int = 0
