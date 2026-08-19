"""Event CRUD routes.

Migrated from modules/events/routes.py (Flask) to FastAPI.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_active_user, require_admin
from backend.app.models.events import Event
from backend.app.models.barangay import BarangayInfo
from backend.app.models.user import User
from backend.app.schemas.event import (
    EventCreate,
    EventListResponse,
    EventResponse,
    EventUpdate,
    PaginationMeta,
)

router = APIRouter()


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
async def _get_event_or_404(event_id: int, db: AsyncSession) -> Event:
    event = await db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


async def _event_to_dict(e: Event, db: AsyncSession) -> dict:
    barangay_name = None
    if e.barangay_id:
        b = await db.get(BarangayInfo, e.barangay_id)
        barangay_name = b.name if b else None

    return {
        "id": e.id,
        "name": e.name,
        "description": e.description,
        "date": e.date.isoformat() if e.date else None,
        "location": e.location,
        "latitude": e.latitude,
        "longitude": e.longitude,
        "barangay_id": e.barangay_id,
        "barangay_name": barangay_name,
        "image_url": e.image_url,
        "category": e.category,
        "status": e.status,
        "created_at": e.created_at.isoformat() if e.created_at else None,
    }


# ─────────────────────────────────────────────
# GET /api/events — list all
# ─────────────────────────────────────────────
@router.get("/", response_model=EventListResponse, summary="List events")
async def list_events(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 20,
    category: str | None = None,
    status_filter: str | None = Query(None, alias="status"),
):
    stmt = select(Event).order_by(Event.date.desc())

    if status_filter and status_filter != "all":
        stmt = stmt.where(Event.status == status_filter)
    else:
        # Default: only show approved
        stmt = stmt.where(Event.status == "approved")

    if category and category != "all":
        stmt = stmt.where(Event.category == category)

    # Count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    offset = (page - 1) * per_page
    stmt = stmt.offset(offset).limit(per_page)
    result = await db.execute(stmt)
    events = result.scalars().all()

    items = [await _event_to_dict(e, db) for e in events]
    pages = max(1, -(-total // per_page))

    return EventListResponse(
        events=[EventResponse(**e) for e in items],
        pagination=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        ),
    )


# ─────────────────────────────────────────────
# GET /api/events/{id} — detail
# ─────────────────────────────────────────────
@router.get("/{event_id}", response_model=EventResponse, summary="Event detail")
async def get_event(
    event_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    event = await _get_event_or_404(event_id, db)
    return EventResponse(**await _event_to_dict(event, db))


# ─────────────────────────────────────────────
# POST /api/events — create (admin)
# ─────────────────────────────────────────────
@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create event",
)
async def create_event(
    body: EventCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    event = Event(
        **body.model_dump(),
        status="approved",
        user_id=admin.id,
    )
    db.add(event)
    await db.flush()
    await db.refresh(event)
    return EventResponse(**await _event_to_dict(event, db))


# ─────────────────────────────────────────────
# PUT /api/events/{id} — update (admin)
# ─────────────────────────────────────────────
@router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update event",
)
async def update_event(
    event_id: int,
    body: EventUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    event = await _get_event_or_404(event_id, db)
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    await db.flush()
    await db.refresh(event)
    return EventResponse(**await _event_to_dict(event, db))


# ─────────────────────────────────────────────
# DELETE /api/events/{id} — delete (admin)
# ─────────────────────────────────────────────
@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete event",
)
async def delete_event(
    event_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    event = await _get_event_or_404(event_id, db)
    await db.delete(event)
