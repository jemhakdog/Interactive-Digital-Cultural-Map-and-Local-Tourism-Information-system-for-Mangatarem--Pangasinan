"""Booking models — ported from modules/booking/models.py."""
from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


def _generate_qr_token() -> str:
    return uuid.uuid4().hex[:12].upper()


class BookableAsset(Base):
    __tablename__ = "BOOKABLE_ASSET"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attraction_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ATTRACTION.id", ondelete="CASCADE"), nullable=True, index=True
    )
    heritage_profile_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("HERITAGE_PROFILE.id", ondelete="CASCADE"), nullable=True, index=True
    )
    daily_capacity: Mapped[int] = mapped_column(Integer, default=50)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True)
    booking_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    attraction = relationship("Attraction", back_populates="bookable_asset")
    heritage_profile = relationship("HeritageProfile", back_populates="bookable_asset")
    slots = relationship("BookingSlot", back_populates="bookable_asset", lazy="dynamic", cascade="all, delete-orphan")


class BookingSlot(Base):
    __tablename__ = "BOOKING_SLOT"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bookable_asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("BOOKABLE_ASSET.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    total_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    booked_count: Mapped[int] = mapped_column(Integer, default=0)

    bookable_asset = relationship("BookableAsset", back_populates="slots")
    reservations = relationship("Reservation", back_populates="slot", lazy="dynamic")

    __table_args__ = (
        UniqueConstraint("bookable_asset_id", "date", name="uq_asset_date"),
    )

    @property
    def available_capacity(self) -> int:
        return max(0, self.total_capacity - self.booked_count)


class Reservation(Base):
    __tablename__ = "RESERVATION"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=False, index=True
    )
    booking_slot_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("BOOKING_SLOT.id", ondelete="CASCADE"), nullable=False, index=True
    )
    party_size: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    primary_contact: Mapped[str | None] = mapped_column(String(100), nullable=True)
    special_requests: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    qr_code_token: Mapped[str] = mapped_column(
        String(20), unique=True, default=_generate_qr_token, index=True
    )
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = relationship("User", back_populates="reservations")
    slot = relationship("BookingSlot", back_populates="reservations")

    __table_args__ = (
        UniqueConstraint("user_id", "booking_slot_id", name="uq_user_slot"),
    )
