"""BarangayInfo model — ported from modules/barangay/models.py."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class BarangayInfo(Base):
    __tablename__ = "BARANGAY_INFO"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Narrative fields
    mission: Mapped[str | None] = mapped_column(Text, nullable=True)
    vision: Mapped[str | None] = mapped_column(Text, nullable=True)
    history: Mapped[str | None] = mapped_column(Text, nullable=True)
    cultural_assets: Mapped[str | None] = mapped_column(Text, nullable=True)
    traditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    local_practices: Mapped[str | None] = mapped_column(Text, nullable=True)
    unique_features: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Metadata
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("USER.id"), nullable=True)

    # JSON fields (use JSON type for SQLite compat; switch to postgresql.JSON in prod)
    map_geo_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    location_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    manager = relationship("User", foreign_keys=[user_id], back_populates="managed_barangay_info")
    residents = relationship("User", foreign_keys="[User.barangay_id]", back_populates="barangay")
    attractions = relationship("Attraction", back_populates="barangay")
    events = relationship("Event", back_populates="barangay")
    establishments = relationship("Establishment", back_populates="barangay")
    profiles = relationship("HeritageProfile", back_populates="barangay")
    announcements = relationship("Announcement", back_populates="barangay")
