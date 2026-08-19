"""HeritageProfile model — ported from modules/heritage/models.py."""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class HeritageProfile(Base):
    __tablename__ = "HERITAGE_PROFILE"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    form_control_number: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    form_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    name_of_asset: Mapped[str | None] = mapped_column(String(200), nullable=True)
    common_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    barangay_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("BARANGAY_INFO.id"), nullable=True, index=True
    )
    location_details: Mapped[str | None] = mapped_column(Text, nullable=True)
    contact_person: Mapped[str | None] = mapped_column(String(200), nullable=True)
    contact_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ownership_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    owner_administrator: Mapped[str | None] = mapped_column(String(200), nullable=True)
    usage_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    significance: Mapped[str | None] = mapped_column(Text, nullable=True)
    conservation_status: Mapped[str | None] = mapped_column(Text, nullable=True)

    template_slug: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    mapper_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    date_profiled: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=True, index=True
    )
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    barangay = relationship("BarangayInfo", back_populates="profiles")
    user = relationship("User", foreign_keys=[user_id], back_populates="profiles")
    attractions = relationship("Attraction", back_populates="heritage_profile")
    bookable_asset = relationship("BookableAsset", back_populates="heritage_profile", uselist=False, cascade="all, delete-orphan")
