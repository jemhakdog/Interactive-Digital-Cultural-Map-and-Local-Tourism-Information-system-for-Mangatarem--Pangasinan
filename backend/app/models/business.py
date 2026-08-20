"""Business models — ported from modules/business/models.py."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
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


class Establishment(Base):
    __tablename__ = "ESTABLISHMENT"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    barangay_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("BARANGAY_INFO.id"), nullable=True
    )
    contact_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(120), nullable=True)
    website: Mapped[str | None] = mapped_column(String(300), nullable=True)
    operating_hours: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    price_range: Mapped[str | None] = mapped_column(String(20), nullable=True)
    amenities: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    # ponytail: new column — requires migration or DB recreate (init_db uses create_all, won't alter existing tables)
    rating_avg: Mapped[float] = mapped_column(Float, default=0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    # Relationships
    barangay = relationship("BarangayInfo", back_populates="establishments")
    owner = relationship("User", back_populates="establishments")
    rooms = relationship("EstablishmentRoom", back_populates="establishment", lazy=True, cascade="all, delete-orphan")
    menu_items = relationship("EstablishmentMenuItem", back_populates="establishment", lazy=True, cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="establishment", lazy=True, cascade="all, delete-orphan")


class EstablishmentRoom(Base):
    __tablename__ = "ESTABLISHMENT_ROOM"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    establishment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ESTABLISHMENT.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price_per_night: Mapped[float | None] = mapped_column(Float, nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, default=2)
    amenities: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    image_urls: Mapped[list | None] = mapped_column(JSON, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    establishment = relationship("Establishment", back_populates="rooms")


class EstablishmentMenuItem(Base):
    __tablename__ = "ESTABLISHMENT_MENU_ITEM"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    establishment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ESTABLISHMENT.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_bestseller: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    establishment = relationship("Establishment", back_populates="menu_items")


class BusinessVerification(Base):
    __tablename__ = "BUSINESS_VERIFICATION"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=False, index=True
    )
    permit_document_url: Mapped[str] = mapped_column(String(500), nullable=False)
    other_document_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="business_verification")
