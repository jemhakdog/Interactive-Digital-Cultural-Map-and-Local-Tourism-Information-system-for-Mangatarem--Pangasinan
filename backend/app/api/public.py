"""Public API routes — no authentication required.

Migrated from modules/core/public_routes.py (Flask) to FastAPI.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.models.attractions import Attraction, Review
from backend.app.models.barangay import BarangayInfo
from backend.app.models.events import Event

router = APIRouter()


# ─────────────────────────────────────────────
# GET /api/ — homepage data
# ─────────────────────────────────────────────
@router.get("/", summary="Homepage data")
async def homepage(db: Annotated[AsyncSession, Depends(get_db)]):
    """Return featured attractions and events for the home page."""
    # Featured attractions (up to 6, approved only)
    att_stmt = (
        select(Attraction)
        .where(Attraction.status == "approved")
        .order_by(Attraction.is_featured.desc(), func.random())
        .limit(6)
    )
    att_result = await db.execute(att_stmt)
    attractions = att_result.scalars().all()

    # Featured events (up to 6, approved only)
    evt_stmt = (
        select(Event)
        .where(Event.status == "approved")
        .order_by(Event.date.desc())
        .limit(6)
    )
    evt_result = await db.execute(evt_stmt)
    events = evt_result.scalars().all()

    async def _att_dict(a: Attraction) -> dict:
        barangay_name = None
        if a.barangay_id:
            b = await db.get(BarangayInfo, a.barangay_id)
            barangay_name = b.name if b else None
        return {
            "id": a.id,
            "name": a.name,
            "category": a.category,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "image_url": a.image_url,
            "is_featured": a.is_featured,
            "barangay_name": barangay_name,
        }

    async def _evt_dict(e: Event) -> dict:
        barangay_name = None
        if e.barangay_id:
            b = await db.get(BarangayInfo, e.barangay_id)
            barangay_name = b.name if b else None
        return {
            "id": e.id,
            "name": e.name,
            "category": e.category,
            "date": e.date.isoformat() if e.date else None,
            "location": e.location,
            "image_url": e.image_url,
            "barangay_name": barangay_name,
        }

    return {
        "featured_attractions": [await _att_dict(a) for a in attractions],
        "featured_events": [await _evt_dict(e) for e in events],
    }


# ─────────────────────────────────────────────
# GET /api/search — unified search
# ─────────────────────────────────────────────
@router.get("/search", summary="Search attractions and events")
async def search(
    db: Annotated[AsyncSession, Depends(get_db)],
    q: Annotated[str, Query(max_length=200)] = "",
    category: Annotated[str, Query(max_length=50)] = "all",
    barangay: Annotated[str, Query(max_length=50)] = "all",
):
    """Unified search for attractions, events, and barangays."""
    query_text = q.strip().lower()

    # ── Attractions ──
    att_stmt = select(Attraction).where(Attraction.status == "approved")
    if query_text:
        like = f"%{query_text}%"
        att_stmt = att_stmt.where(
            or_(
                Attraction.name.ilike(like),
                Attraction.description.ilike(like),
                Attraction.category.ilike(like),
            )
        )
    if category != "all":
        att_stmt = att_stmt.where(Attraction.category == category)
    if barangay != "all":
        att_stmt = (
            att_stmt.join(BarangayInfo, Attraction.barangay_id == BarangayInfo.id)
            .where(BarangayInfo.name == barangay)
        )
    att_result = await db.execute(att_stmt)
    attractions = att_result.scalars().all()

    # ── Events ──
    evt_stmt = select(Event).where(Event.status == "approved")
    if query_text:
        like = f"%{query_text}%"
        evt_stmt = evt_stmt.where(
            or_(
                Event.name.ilike(like),
                Event.description.ilike(like),
                Event.category.ilike(like),
            )
        )
    if category != "all":
        evt_stmt = evt_stmt.where(Event.category == category)
    if barangay != "all":
        evt_stmt = (
            evt_stmt.join(BarangayInfo, Event.barangay_id == BarangayInfo.id)
            .where(BarangayInfo.name == barangay)
        )
    evt_result = await db.execute(evt_stmt)
    events = evt_result.scalars().all()

    # ── Barangays (info) ──
    barangays_info: list = []
    if query_text or barangay != "all":
        b_stmt = select(BarangayInfo)
        if query_text:
            b_stmt = b_stmt.where(BarangayInfo.name.ilike(f"%{query_text}%"))
        if barangay != "all":
            b_stmt = b_stmt.where(BarangayInfo.name == barangay)
        b_result = await db.execute(b_stmt)
        barangays_info = b_result.scalars().all()

    # ── Filter options for UI dropdowns ──
    cat_stmt = (
        select(Attraction.category)
        .where(Attraction.status == "approved")
        .distinct()
    )
    evt_cat_stmt = (
        select(Event.category)
        .where(Event.status == "approved")
        .distinct()
    )
    cats_a = (await db.execute(cat_stmt)).scalars().all()
    cats_e = (await db.execute(evt_cat_stmt)).scalars().all()
    all_categories = sorted(set(cats_a + cats_e))

    b_stmt = (
        select(BarangayInfo.name)
        .join(Attraction, Attraction.barangay_id == BarangayInfo.id)
        .where(Attraction.status == "approved")
        .distinct()
    )
    all_barangays = sorted(
        [b for b in (await db.execute(b_stmt)).scalars().all() if b]
    )

    return {
        "attractions": [
            {
                "id": a.id,
                "name": a.name,
                "category": a.category,
                "latitude": a.latitude,
                "longitude": a.longitude,
                "image_url": a.image_url,
            }
            for a in attractions
        ],
        "events": [
            {
                "id": e.id,
                "name": e.name,
                "category": e.category,
                "date": e.date.isoformat() if e.date else None,
                "location": e.location,
                "image_url": e.image_url,
            }
            for e in events
        ],
        "barangays_info": [
            {"id": b.id, "name": b.name} for b in barangays_info
        ],
        "categories": all_categories,
        "barangays": all_barangays,
    }


# ─────────────────────────────────────────────
# GET /api/map — map data (attractions with lat/lng)
# ─────────────────────────────────────────────
@router.get("/map", summary="Map data")
async def map_data(
    db: Annotated[AsyncSession, Depends(get_db)],
    category: Annotated[str, Query(max_length=50)] = "all",
):
    """Return approved attractions with coordinates for map rendering."""
    stmt = select(Attraction).where(Attraction.status == "approved")
    if category != "all":
        stmt = stmt.where(Attraction.category == category)
    result = await db.execute(stmt)
    attractions = result.scalars().all()

    markers = []
    for a in attractions:
        barangay_name = None
        if a.barangay_id:
            b = await db.get(BarangayInfo, a.barangay_id)
            barangay_name = b.name if b else None
        markers.append({
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "category": a.category,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "image_url": a.image_url,
            "barangay_name": barangay_name,
            "is_featured": a.is_featured,
            "physical_status": a.physical_status,
            "advisory_status": a.advisory_status,
            "advisory_message": a.advisory_message,
            "opening_hours": a.opening_hours,
            "entrance_fee": a.entrance_fee,
            "contact_info": a.contact_info,
            "facilities": a.facilities,
            "directions": a.directions,
        })

    return {"markers": markers}
