"""Gamification models — ported from modules/gamification/models.py."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class AchievementBadge(Base):
    __tablename__ = "ACHIEVEMENT_BADGE"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    badge_image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    required_visits: Mapped[int] = mapped_column(Integer, default=1)
    target_locations: Mapped[list] = mapped_column(JSON, nullable=False)
    reward_promo: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    unlocks = relationship("UserPassport", back_populates="badge")


class UserPassport(Base):
    __tablename__ = "USER_PASSPORT"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("USER.id", ondelete="CASCADE"), nullable=False, index=True
    )
    badge_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ACHIEVEMENT_BADGE.id", ondelete="CASCADE"), nullable=False, index=True
    )
    unlocked_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    user = relationship("User", back_populates="passports")
    badge = relationship("AchievementBadge", back_populates="unlocks")

    __table_args__ = (
        UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),
    )


class TouristCheckIn(Base):
    __tablename__ = "TOURIST_CHECK_IN"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("USER.id", ondelete="CASCADE"), nullable=False, index=True
    )
    attraction_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ATTRACTION.id", ondelete="SET NULL"), nullable=True, index=True
    )
    establishment_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ESTABLISHMENT.id", ondelete="SET NULL"), nullable=True, index=True
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    distance_meters: Mapped[float | None] = mapped_column(Float, nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    user = relationship("User", back_populates="check_ins")

    __table_args__ = (
        UniqueConstraint("user_id", "attraction_id", name="uq_user_attraction"),
        UniqueConstraint("user_id", "establishment_id", name="uq_user_establishment"),
    )
