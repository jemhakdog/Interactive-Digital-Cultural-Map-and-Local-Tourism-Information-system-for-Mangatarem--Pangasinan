"""Pydantic schemas for the Analytics module."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class VisitorLogRequest(BaseModel):
    visitor_name: str | None = None
    visitor_age: int | None = None
    visitor_address: str | None = None
    is_system_user: bool = False
    visitor_count: int = Field(1, ge=1)
    notes: str | None = None


class VisitorLogResponse(BaseModel):
    success: bool
    message: str


class TopPageItem(BaseModel):
    page_name: str | None = None
    views: int


class AnalyticsSummaryResponse(BaseModel):
    total_visitors: int
    total_page_views: int
    top_pages: list[TopPageItem]


class VisitorItem(BaseModel):
    id: int
    target_type: str
    target_id: int
    visitor_name: str | None = None
    visitor_age: int | None = None
    visitor_count: int
    visit_date: date | None = None
    is_system_user: bool
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class VisitorListResponse(BaseModel):
    visitors: list[VisitorItem]
