"""Pydantic schemas for the /api/contributor (barangay steward) endpoints."""
from __future__ import annotations

from pydantic import BaseModel


class ContributorStatsResponse(BaseModel):
    """Aggregate counts for the contributor dashboard."""
    total: int = 0
    approved: int = 0
    pending: int = 0
    rejected: int = 0
    reviews: int = 0


class ContributorActivityItem(BaseModel):
    """A single row in the contributor activity feed."""
    id: int
    name: str
    type: str
    status: str
    date: str | None = None
    href: str | None = None


class ContributorActivityResponse(BaseModel):
    """Activity feed list wrapper."""
    items: list[ContributorActivityItem]
