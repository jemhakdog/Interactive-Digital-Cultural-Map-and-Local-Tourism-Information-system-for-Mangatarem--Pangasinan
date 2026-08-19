"""Business API router — establishments, rooms, menu items, reviews.

Migrated from modules/business/routes.py (Flask) to FastAPI.
Covers the JSON/API endpoints only; template-rendering routes stay in Flask.
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_active_user, get_current_user
from backend.app.models.business import (
    Establishment,
    EstablishmentMenuItem,
    EstablishmentRoom,
)
from backend.app.models.attractions import Review
from backend.app.models.barangay import BarangayInfo
from backend.app.models.gamification import TouristCheckIn
from backend.app.models.user import User
from backend.app.schemas.business import (
    EstablishmentCreate,
    EstablishmentListResponse,
    EstablishmentResponse,
    EstablishmentUpdate,
    MenuItemCreate,
    MenuItemResponse,
    MenuItemUpdate,
    ReviewCreate,
    ReviewReply,
    ReviewResponse,
    RoomCreate,
    RoomResponse,
    RoomUpdate,
)

router = APIRouter()


# ── Helpers ────────────────────────────────────────────────────

def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlng / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ───────────────────────────────────────────────────────────────
# PUBLIC — List establishments
# ───────────────────────────────────────────────────────────────

@router.get("/", summary="List approved establishments")
async def list_establishments(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    type: str | None = Query(None),
    price_range: str | None = Query(None),
    barangay: str | None = Query(None),
    q: str | None = Query(None, max_length=200),
    is_featured: bool | None = Query(None),
    lat: float | None = Query(None),
    lng: float | None = Query(None),
    radius: float = Query(10, ge=0.1, le=500),
):
    """Return paginated, filtered list of approved establishments."""
    stmt = (
        select(Establishment, BarangayInfo.name.label("barangay_name"))
        .outerjoin(BarangayInfo, BarangayInfo.id == Establishment.barangay_id)
        .where(Establishment.status == "approved")
    )

    if type and type != "all":
        stmt = stmt.where(Establishment.type == type)
    if price_range:
        stmt = stmt.where(Establishment.price_range == price_range)
    if is_featured is not None:
        stmt = stmt.where(Establishment.is_featured == is_featured)
    if barangay and barangay != "all":
        stmt = stmt.where(BarangayInfo.name == barangay)
    if q:
        stmt = stmt.where(
            or_(
                Establishment.name.ilike(f"%{q}%"),
                Establishment.description.ilike(f"%{q}%"),
                Establishment.address.ilike(f"%{q}%"),
            )
        )

    # Count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    # Paginate
    offset = (page - 1) * per_page
    stmt = stmt.order_by(Establishment.is_featured.desc(), Establishment.rating_avg.desc()).offset(offset).limit(per_page)
    result = await db.execute(stmt)
    rows = result.all()

    establishments = []
    for est, b_name in rows:
        est_dict = {
            "id": est.id,
            "name": est.name,
            "type": est.type,
            "description": est.description,
            "address": est.address,
            "latitude": est.latitude,
            "longitude": est.longitude,
            "contact_number": est.contact_number,
            "email": est.email,
            "website": est.website,
            "price_range": est.price_range,
            "rating_avg": est.rating_avg or 0,
            "review_count": est.review_count or 0,
            "cover_image_url": est.cover_image_url,
            "logo_url": est.logo_url,
            "amenities": est.amenities or [],
            "operating_hours": est.operating_hours,
            "barangay": b_name,
            "barangay_name": b_name,
            "owner_id": est.owner_id,
            "is_featured": est.is_featured,
            "created_at": est.created_at.isoformat() if est.created_at else None,
        }
        if lat and lng and est.latitude and est.longitude:
            est_dict["distance"] = round(_haversine_km(lat, lng, est.latitude, est.longitude), 2)
        establishments.append(est_dict)

    # Sort by distance if provided
    if lat and lng:
        establishments.sort(key=lambda x: x.get("distance", float("inf")))
        establishments = [e for e in establishments if e.get("distance", float("inf")) <= radius]

    pages = math.ceil(total / per_page) if total else 0
    return {
        "establishments": establishments,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1,
        },
    }


# ───────────────────────────────────────────────────────────────
# PUBLIC — Establishment detail
# ───────────────────────────────────────────────────────────────

@router.get("/{establishment_id}", summary="Establishment detail")
async def get_establishment(
    establishment_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(Establishment, BarangayInfo.name.label("barangay_name"))
        .outerjoin(BarangayInfo, BarangayInfo.id == Establishment.barangay_id)
        .where(Establishment.id == establishment_id)
    )
    row = result.first()
    if not row or row[0].status != "approved":
        raise HTTPException(status_code=404, detail="Establishment not found")
    est, b_name = row

    # Load rooms or menu items
    rooms: list = []
    menu_items: list = []
    if est.type == "inn":
        r = await db.execute(
            select(EstablishmentRoom).where(
                EstablishmentRoom.establishment_id == est.id,
                EstablishmentRoom.is_available == True,  # noqa: E712
            )
        )
        rooms = r.scalars().all()
    else:
        m = await db.execute(
            select(EstablishmentMenuItem).where(
                EstablishmentMenuItem.establishment_id == est.id,
                EstablishmentMenuItem.is_available == True,  # noqa: E712
            ).order_by(EstablishmentMenuItem.category, EstablishmentMenuItem.name)
        )
        menu_items = m.scalars().all()

    # Reviews with reviewer usernames
    rev = await db.execute(
        select(Review, User.username.label("username"))
        .outerjoin(User, User.id == Review.user_id)
        .where(
            Review.establishment_id == est.id,
            Review.status == "approved",
            Review.parent_id.is_(None),
        ).order_by(Review.created_at.desc())
    )
    rev_rows = rev.all()
    review_list = []
    for r, uname in rev_rows:
        rep = await db.execute(
            select(Review, User.username.label("username"))
            .outerjoin(User, User.id == Review.user_id)
            .where(
                Review.parent_id == r.id,
                Review.status == "approved",
            ).order_by(Review.created_at.asc())
        )
        reply_list = [
            {
                "id": rp.id,
                "user_id": rp.user_id,
                "username": rp_uname or "Owner",
                "comment": rp.comment,
                "created_at": rp.created_at.isoformat() if rp.created_at else None,
            }
            for rp, rp_uname in rep.all()
        ]
        review_list.append({
            "id": r.id,
            "user_id": r.user_id,
            "username": uname or "Visitor",
            "rating": r.rating,
            "comment": r.comment,
            "parent_id": r.parent_id,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "replies": reply_list,
        })

    return {
        "establishment": {
            "id": est.id,
            "name": est.name,
            "type": est.type,
            "description": est.description,
            "address": est.address,
            "latitude": est.latitude,
            "longitude": est.longitude,
            "contact_number": est.contact_number,
            "email": est.email,
            "website": est.website,
            "price_range": est.price_range,
            "rating_avg": est.rating_avg,
            "review_count": est.review_count,
            "cover_image_url": est.cover_image_url,
            "logo_url": est.logo_url,
            "amenities": est.amenities,
            "operating_hours": est.operating_hours,
            "barangay": b_name,
            "barangay_name": b_name,
            "owner_id": est.owner_id,
            "status": est.status,
            "is_featured": est.is_featured,
            "created_at": est.created_at.isoformat() if est.created_at else None,
        },
        "rooms": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "price_per_night": r.price_per_night,
                "capacity": r.capacity,
                "amenities": r.amenities,
                "image_urls": r.image_urls,
            }
            for r in rooms
        ],
        "menu_items": [
            {
                "id": m.id,
                "name": m.name,
                "description": m.description,
                "price": m.price,
                "category": m.category,
                "image_url": m.image_url,
                "is_bestseller": m.is_bestseller,
            }
            for m in menu_items
        ],
        "reviews": review_list,
    }


# ───────────────────────────────────────────────────────────────
# OWNER — Create / Edit establishment
# ───────────────────────────────────────────────────────────────

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create establishment")
async def create_establishment(
    body: EstablishmentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    if user.role != "business_owner":
        raise HTTPException(status_code=403, detail="Business owner role required")

    # Check if owner already has one
    existing = await db.execute(
        select(Establishment).where(Establishment.owner_id == user.id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="You already have an establishment")

    # Resolve barangay
    barangay_id = None
    if body.barangay_name:
        b = await db.execute(
            select(BarangayInfo).where(BarangayInfo.name == body.barangay_name)
        )
        barangay = b.scalar_one_or_none()
        if not barangay:
            barangay = BarangayInfo(name=body.barangay_name)
            db.add(barangay)
            await db.flush()
        barangay_id = barangay.id

    est = Establishment(
        name=body.name,
        type=body.type,
        description=body.description,
        address=body.address,
        latitude=body.latitude,
        longitude=body.longitude,
        barangay_id=barangay_id,
        contact_number=body.contact_number,
        email=body.email,
        website=body.website,
        price_range=body.price_range,
        amenities=body.amenities,
        operating_hours=body.operating_hours,
        owner_id=user.id,
        status="pending",
    )
    db.add(est)
    await db.flush()
    return {"id": est.id, "status": est.status, "message": "Establishment submitted for approval"}


@router.put("/{establishment_id}", summary="Update establishment")
async def update_establishment(
    establishment_id: int,
    body: EstablishmentUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    result = await db.execute(
        select(Establishment).where(Establishment.id == establishment_id)
    )
    est = result.scalar_one_or_none()
    if not est:
        raise HTTPException(status_code=404, detail="Establishment not found")
    if est.owner_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = body.model_dump(exclude_unset=True)

    # Resolve barangay if name changed
    if "barangay_name" in update_data:
        barangay_name = update_data.pop("barangay_name")
        if barangay_name:
            b = await db.execute(select(BarangayInfo).where(BarangayInfo.name == barangay_name))
            barangay = b.scalar_one_or_none()
            if not barangay:
                barangay = BarangayInfo(name=barangay_name)
                db.add(barangay)
                await db.flush()
            est.barangay_id = barangay.id

    for field, value in update_data.items():
        setattr(est, field, value)

    return {"id": est.id, "message": "Establishment updated"}


# ───────────────────────────────────────────────────────────────
# OWNER — Rooms CRUD
# ───────────────────────────────────────────────────────────────

async def _get_owner_establishment(db: AsyncSession, user_id: int) -> Establishment:
    result = await db.execute(
        select(Establishment).where(Establishment.owner_id == user_id)
    )
    est = result.scalar_one_or_none()
    if not est:
        raise HTTPException(status_code=404, detail="No establishment found for this owner")
    return est


@router.get("/rooms/list", summary="List rooms for owner's establishment")
async def list_rooms(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    est = await _get_owner_establishment(db, user.id)
    result = await db.execute(
        select(EstablishmentRoom).where(EstablishmentRoom.establishment_id == est.id)
    )
    return {"rooms": [{"id": r.id, "name": r.name, "price_per_night": r.price_per_night, "capacity": r.capacity, "is_available": r.is_available} for r in result.scalars().all()]}


@router.post("/rooms", status_code=status.HTTP_201_CREATED, summary="Add room")
async def add_room(
    body: RoomCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    est = await _get_owner_establishment(db, user.id)
    room = EstablishmentRoom(
        establishment_id=est.id,
        name=body.name,
        description=body.description,
        price_per_night=body.price_per_night,
        capacity=body.capacity,
        is_available=body.is_available,
        amenities=body.amenities,
        image_urls=body.image_urls,
    )
    db.add(room)
    await db.flush()
    return {"id": room.id, "message": f"Room '{room.name}' added"}


@router.put("/rooms/{room_id}", summary="Edit room")
async def edit_room(
    room_id: int,
    body: RoomUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    est = await _get_owner_establishment(db, user.id)
    result = await db.execute(select(EstablishmentRoom).where(EstablishmentRoom.id == room_id))
    room = result.scalar_one_or_none()
    if not room or room.establishment_id != est.id:
        raise HTTPException(status_code=404, detail="Room not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(room, field, value)
    return {"message": f"Room '{room.name}' updated"}


@router.delete("/rooms/{room_id}", summary="Delete room")
async def delete_room(
    room_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    est = await _get_owner_establishment(db, user.id)
    result = await db.execute(select(EstablishmentRoom).where(EstablishmentRoom.id == room_id))
    room = result.scalar_one_or_none()
    if not room or room.establishment_id != est.id:
        raise HTTPException(status_code=404, detail="Room not found")
    await db.delete(room)
    return {"message": "Room deleted"}


# ───────────────────────────────────────────────────────────────
# OWNER — Menu items CRUD
# ───────────────────────────────────────────────────────────────

@router.get("/menu/list", summary="List menu items for owner's establishment")
async def list_menu(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    est = await _get_owner_establishment(db, user.id)
    result = await db.execute(
        select(EstablishmentMenuItem)
        .where(EstablishmentMenuItem.establishment_id == est.id)
        .order_by(EstablishmentMenuItem.category, EstablishmentMenuItem.name)
    )
    return {"menu_items": [{"id": m.id, "name": m.name, "price": m.price, "category": m.category, "is_available": m.is_available, "is_bestseller": m.is_bestseller} for m in result.scalars().all()]}


@router.post("/menu", status_code=status.HTTP_201_CREATED, summary="Add menu item")
async def add_menu_item(
    body: MenuItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    est = await _get_owner_establishment(db, user.id)
    item = EstablishmentMenuItem(
        establishment_id=est.id,
        name=body.name,
        description=body.description,
        price=body.price,
        category=body.category,
        is_available=body.is_available,
        is_bestseller=body.is_bestseller,
        image_url=body.image_url,
    )
    db.add(item)
    await db.flush()
    return {"id": item.id, "message": f"Menu item '{item.name}' added"}


@router.put("/menu/{item_id}", summary="Edit menu item")
async def edit_menu_item(
    item_id: int,
    body: MenuItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    est = await _get_owner_establishment(db, user.id)
    result = await db.execute(select(EstablishmentMenuItem).where(EstablishmentMenuItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item or item.establishment_id != est.id:
        raise HTTPException(status_code=404, detail="Menu item not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    return {"message": f"Menu item '{item.name}' updated"}


@router.delete("/menu/{item_id}", summary="Delete menu item")
async def delete_menu_item(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    est = await _get_owner_establishment(db, user.id)
    result = await db.execute(select(EstablishmentMenuItem).where(EstablishmentMenuItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item or item.establishment_id != est.id:
        raise HTTPException(status_code=404, detail="Menu item not found")
    await db.delete(item)
    return {"message": "Menu item deleted"}


# ───────────────────────────────────────────────────────────────
# REVIEWS
# ───────────────────────────────────────────────────────────────

@router.post("/{establishment_id}/reviews", status_code=status.HTTP_201_CREATED, summary="Submit review")
async def submit_review(
    establishment_id: int,
    body: ReviewCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    result = await db.execute(
        select(Establishment).where(Establishment.id == establishment_id)
    )
    est = result.scalar_one_or_none()
    if not est:
        raise HTTPException(status_code=404, detail="Establishment not found")

    review = Review(
        user_id=user.id,
        establishment_id=est.id,
        rating=body.rating,
        comment=body.comment,
        status="approved",
    )
    db.add(review)
    await db.flush()

    # Recalculate rating
    rev_result = await db.execute(
        select(func.count(), func.avg(Review.rating)).where(
            Review.establishment_id == est.id,
            Review.status == "approved",
            Review.parent_id.is_(None),
        )
    )
    cnt, avg = rev_result.one()
    est.rating_avg = round(float(avg), 2) if avg else 0
    est.review_count = cnt

    return {"id": review.id, "message": "Review posted"}


@router.post("/reviews/{review_id}/reply", summary="Reply to review")
async def reply_to_review(
    review_id: int,
    body: ReviewReply,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    est = await _get_owner_establishment(db, user.id)
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    if not review or review.establishment_id != est.id:
        raise HTTPException(status_code=404, detail="Review not found")

    reply = Review(
        user_id=user.id,
        establishment_id=est.id,
        parent_id=review.id,
        comment=body.comment,
        rating=None,
        status="approved",
    )
    db.add(reply)
    return {"message": "Reply posted"}
