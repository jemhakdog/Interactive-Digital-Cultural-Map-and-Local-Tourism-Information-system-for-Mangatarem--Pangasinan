"""Attractions models — ported from modules/attractions/models.py."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
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


class Attraction(Base):
    __tablename__ = "ATTRACTION"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    directions: Mapped[str | None] = mapped_column(Text, nullable=True)
    osm_alternatives: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    barangay_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("BARANGAY_INFO.id"), nullable=True, index=True
    )
    heritage_profile_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("HERITAGE_PROFILE.id"), nullable=True
    )

    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    physical_status: Mapped[str | None] = mapped_column(String(50), default="Open Public", nullable=True)
    is_verified: Mapped[bool | None] = mapped_column(Boolean, default=True, nullable=True)

    # Practical details
    opening_hours: Mapped[str | None] = mapped_column(String(100), nullable=True)
    entrance_fee: Mapped[str | None] = mapped_column(String(100), nullable=True)
    contact_info: Mapped[str | None] = mapped_column(String(100), nullable=True)
    facilities: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Safety advisories
    advisory_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    advisory_status: Mapped[str | None] = mapped_column(String(20), nullable=True, default="Normal")

    # Steward
    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=True, index=True
    )
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    # Relationships
    barangay = relationship("BarangayInfo", back_populates="attractions")
    heritage_profile = relationship("HeritageProfile", back_populates="attractions")
    user = relationship("User", foreign_keys=[user_id], back_populates="attractions")
    reviews = relationship("Review", back_populates="attraction", lazy="dynamic")
    map_feedbacks = relationship("MapFeedback", back_populates="attraction")
    bookable_asset = relationship("BookableAsset", back_populates="attraction", uselist=False, cascade="all, delete-orphan")

    @property
    def rating(self) -> float | None:
        # This property is sync and can't use async session.
        # The rating should be computed in the API endpoint using an async query.
        return None


class Review(Base):
    __tablename__ = "REVIEW"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("USER.id"), nullable=False, index=True)
    attraction_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ATTRACTION.id", ondelete="CASCADE"), nullable=True, index=True
    )
    establishment_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ESTABLISHMENT.id", ondelete="CASCADE"), nullable=True, index=True
    )
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("REVIEW.id", ondelete="CASCADE"), nullable=True, index=True
    )
    photo_urls: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user = relationship("User", back_populates="reviews")
    attraction = relationship("Attraction", back_populates="reviews")
    establishment = relationship("Establishment", back_populates="reviews")
    parent = relationship("Review", remote_side="Review.id", backref="replies", foreign_keys="[Review.parent_id]")

    __table_args__ = (
        CheckConstraint(
            "(attraction_id IS NOT NULL AND establishment_id IS NULL) OR "
            "(attraction_id IS NULL AND establishment_id IS NOT NULL)",
            name="ck_review_target",
        ),
    )


class UserFavorite(Base):
    __tablename__ = "USER_FAVORITE"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("USER.id"), nullable=False, index=True)
    attraction_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ATTRACTION.id", ondelete="CASCADE"), nullable=True, index=True
    )
    establishment_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ESTABLISHMENT.id", ondelete="CASCADE"), nullable=True, index=True
    )
    event_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("EVENT.id", ondelete="CASCADE"), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(String(20), default="favorite", index=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")

    __table_args__ = (
        CheckConstraint(
            "(attraction_id IS NOT NULL AND establishment_id IS NULL AND event_id IS NULL) OR "
            "(attraction_id IS NULL AND establishment_id IS NOT NULL AND event_id IS NULL) OR "
            "(attraction_id IS NULL AND establishment_id IS NULL AND event_id IS NOT NULL)",
            name="ck_favorite_target",
        ),
    )


class MapFeedback(Base):
    __tablename__ = "MAP_FEEDBACK"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attraction_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ATTRACTION.id"), nullable=True
    )
    feedback_type: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    attraction = relationship("Attraction", back_populates="map_feedbacks")
