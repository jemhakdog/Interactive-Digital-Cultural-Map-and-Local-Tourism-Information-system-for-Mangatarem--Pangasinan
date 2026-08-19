"""Gallery API router — photo/video gallery items.

Migrated from modules/gallery/routes.py (Flask) to FastAPI.
"""
from __future__ import annotations

import math
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.models.gallery import GalleryItem
from backend.app.models.user import User

router = APIRouter()


class GalleryItemCreate(BaseModel):
    type: str = Field(default="photo", description="photo or video")
    url: str = Field(..., description="Direct media URL")
    caption: str | None = Field(default=None, description="Media caption or title")
    user_id: int | None = None


@router.get("/", summary="List approved gallery items")
async def list_gallery(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    per_page: int = Query(24, ge=1, le=100),
    type: str | None = Query(None, description="Filter by media type: photo or video"),
    barangay: str | None = Query(None, description="Filter by barangay ID or name"),
):
    """Return paginated approved gallery items with unique barangay list."""
    stmt = select(GalleryItem).where(GalleryItem.status == "approved")

    if type and type != "all":
        stmt = stmt.where(GalleryItem.type == type)

    if barangay and barangay != "all":
        stmt = stmt.join(User, User.id == GalleryItem.user_id).where(
            User.barangay_id == barangay
        )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    offset = (page - 1) * per_page
    stmt = stmt.order_by(GalleryItem.created_at.desc()).offset(offset).limit(per_page)
    items = (await db.execute(stmt)).scalars().all()

    # Unique barangays
    bq = (
        select(User.barangay_id)
        .join(GalleryItem, User.id == GalleryItem.user_id)
        .where(GalleryItem.status == "approved", User.barangay_id.is_not(None))
        .distinct()
        .order_by(User.barangay_id)
    )
    barangays = [str(b) for b in (await db.execute(bq)).scalars().all()]

    pages = math.ceil(total / per_page) if total else 0
    return {
        "items": [
            {
                "id": item.id,
                "title": item.caption or f"Media #{item.id}",
                "caption": item.caption,
                "description": item.caption,
                "url": item.url,
                "image_url": item.url,
                "media_url": item.url,
                "type": item.type or "photo",
                "media_type": item.type or "photo",
                "status": item.status,
                "user_id": item.user_id,
                "created_at": item.created_at.isoformat() if item.created_at else None,
            }
            for item in items
        ],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1,
        },
        "barangays": barangays,
    }


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Submit a gallery item")
async def create_gallery_item(
    payload: GalleryItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Submit a new media item for moderation."""
    new_item = GalleryItem(
        type=payload.type,
        url=payload.url,
        caption=payload.caption,
        user_id=payload.user_id,
        status="pending",
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return {
        "success": True,
        "message": "Media item submitted for review",
        "item": {
            "id": new_item.id,
            "type": new_item.type,
            "url": new_item.url,
            "caption": new_item.caption,
            "status": new_item.status,
            "created_at": new_item.created_at.isoformat() if new_item.created_at else None,
        },
    }

