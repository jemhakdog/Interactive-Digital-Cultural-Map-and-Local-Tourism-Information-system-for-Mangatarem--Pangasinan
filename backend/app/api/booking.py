"""Booking API router — availability, reservations, admin.

Migrated from modules/booking/routes.py (Flask) to FastAPI.
"""
from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.core.database import get_db
from backend.app.core.dependencies import (
    get_current_active_user,
    get_current_user,
    require_roles,
)
from backend.app.models.analytics import VisitorLog
from backend.app.models.attractions import Attraction
from backend.app.models.booking import BookableAsset, BookingSlot, Reservation
from backend.app.models.business import Establishment
from backend.app.models.user import User
from backend.app.schemas.booking import (
    AvailabilityResponse,
    ReserveRequest,
    ReserveResponse,
    UpdateStatusRequest,
    VerifyArrivalRequest,
    VerifyArrivalResponse,
)

router = APIRouter()


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ───────────────────────────────────────────────────────────────
# PUBLIC — Availability
# ───────────────────────────────────────────────────────────────

@router.get("/availability/{asset_id}", summary="Check availability for a bookable asset")
async def get_availability(
    asset_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    date: str = Query(..., description="YYYY-MM-DD"),
):
    result = await db.execute(select(BookableAsset).where(BookableAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset or asset.status != "active":
        raise HTTPException(status_code=400, detail="Asset is not available for booking")

    try:
        query_date = datetime.strptime(f"{date}T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (YYYY-MM-DD)")

    slot_result = await db.execute(
        select(BookingSlot).where(
            BookingSlot.bookable_asset_id == asset.id,
            BookingSlot.date == query_date,
        )
    )
    slot = slot_result.scalar_one_or_none()
    available = asset.daily_capacity if not slot else slot.available_capacity

    return {
        "asset_id": asset.id,
        "date": date,
        "available_capacity": available,
        "daily_capacity": asset.daily_capacity,
    }


# ───────────────────────────────────────────────────────────────
# AUTH — Reserve
# ───────────────────────────────────────────────────────────────

@router.post("/reserve", summary="Create a reservation")
async def reserve_slot(
    body: ReserveRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        reserve_date = datetime.strptime(f"{body.date}T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    result = await db.execute(select(BookableAsset).where(BookableAsset.id == body.asset_id))
    asset = result.scalar_one_or_none()
    if not asset or asset.status != "active":
        raise HTTPException(status_code=400, detail="Asset not available")

    # Get or create slot
    slot_result = await db.execute(
        select(BookingSlot).where(
            BookingSlot.bookable_asset_id == asset.id,
            BookingSlot.date == reserve_date,
        )
    )
    slot = slot_result.scalar_one_or_none()
    if not slot:
        slot = BookingSlot(
            bookable_asset_id=asset.id,
            date=reserve_date,
            total_capacity=asset.daily_capacity,
            booked_count=0,
        )
        db.add(slot)
        await db.flush()

    # Idempotency check
    existing_result = await db.execute(
        select(Reservation).where(
            Reservation.user_id == user.id,
            Reservation.booking_slot_id == slot.id,
            Reservation.status != "cancelled",
        )
    )
    existing = existing_result.scalar_one_or_none()
    if existing:
        return {
            "success": True,
            "reservation_id": existing.id,
            "status": existing.status,
            "qr_token": existing.qr_code_token,
            "idempotent": True,
        }

    # Check capacity
    if (slot.total_capacity - slot.booked_count) < body.party_size:
        raise HTTPException(status_code=400, detail="Not enough capacity available")

    slot.booked_count += body.party_size
    reservation = Reservation(
        user_id=user.id,
        booking_slot_id=slot.id,
        party_size=body.party_size,
        primary_contact=body.contact,
        status="pending" if asset.requires_approval else "confirmed",
    )
    db.add(reservation)
    await db.flush()

    return {
        "success": True,
        "reservation_id": reservation.id,
        "status": reservation.status,
        "qr_token": reservation.qr_code_token,
    }


# ───────────────────────────────────────────────────────────────
# ADMIN — Update reservation status
# ───────────────────────────────────────────────────────────────

ALLOWED_TRANSITIONS = {
    "pending": ["confirmed", "cancelled"],
    "confirmed": ["cancelled", "attended", "no-show"],
    "cancelled": [],
    "attended": [],
    "no-show": [],
}


@router.post("/admin/update-status", summary="Update reservation status")
async def update_status(
    body: UpdateStatusRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    if user.role not in ("admin", "contributor", "business_owner"):
        raise HTTPException(status_code=403, detail="Unauthorized")

    result = await db.execute(select(Reservation).where(Reservation.id == body.reservation_id))
    reservation = result.scalar_one_or_none()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if body.status not in ALLOWED_TRANSITIONS.get(reservation.status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from {reservation.status} to {body.status}",
        )

    # Roll back capacity on cancel
    if body.status == "cancelled":
        slot_result = await db.execute(
            select(BookingSlot).where(BookingSlot.id == reservation.booking_slot_id)
        )
        slot = slot_result.scalar_one()
        slot.booked_count = max(0, slot.booked_count - reservation.party_size)

    reservation.status = body.status
    return {"success": True, "new_status": reservation.status}


# ───────────────────────────────────────────────────────────────
# AUTH — GPS arrival verification
# ───────────────────────────────────────────────────────────────

THRESHOLD_METERS = 100.0


@router.post("/verify-arrival", summary="GPS arrival verification")
async def verify_arrival(
    body: VerifyArrivalRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    today = datetime.now(UTC).date()  # matches VisitorLog.visit_date default (date.today, local timezone)
    booking_attended = False
    navigated_arrived = False
    place_name = ""
    arrived_target_id = None
    arrived_target_type = None

    # Step 1: check today's confirmed reservations
    slot_q = (
        select(BookingSlot)
        .join(Reservation, Reservation.booking_slot_id == BookingSlot.id)
        .where(
            Reservation.user_id == user.id,
            Reservation.status == "confirmed",
            BookingSlot.date == today,
        )
    )
    slots = (await db.execute(slot_q)).scalars().all()

    for slot in slots:
        asset_result = await db.execute(
            select(BookableAsset).where(BookableAsset.id == slot.bookable_asset_id)
        )
        asset = asset_result.scalar_one_or_none()
        if not asset or not asset.attraction_id:
            continue
        att_result = await db.execute(select(Attraction).where(Attraction.id == asset.attraction_id))
        att = att_result.scalar_one_or_none()
        if not att:
            continue
        dist = _haversine_m(body.latitude, body.longitude, att.latitude, att.longitude)
        if dist <= THRESHOLD_METERS:
            res_result = await db.execute(
                select(Reservation).where(
                    Reservation.user_id == user.id,
                    Reservation.booking_slot_id == slot.id,
                )
            )
            res = res_result.scalar_one()
            res.status = "attended"
            booking_attended = True
            place_name = att.name
            # Idempotent visit log: one row per (user, target, day)
            existing_log = (
                await db.execute(
                    select(VisitorLog).where(
                        VisitorLog.visitor_user_id == user.id,
                        VisitorLog.target_type == "attraction",
                        VisitorLog.target_id == att.id,
                        VisitorLog.visit_date == today,
                    )
                )
            ).scalar_one_or_none()
            if existing_log is None:
                db.add(
                    VisitorLog(
                        target_type="attraction",
                        target_id=att.id,
                        visitor_count=res.party_size,
                        visitor_name=user.username,
                        is_system_user=True,
                        logged_by=user.id,
                        visitor_user_id=user.id,
                        notes="verified via GPS arrival",
                    )
                )
            break

    # Step 2: check navigation target
    if body.navigated_target_id and body.navigated_target_type:
        if body.navigated_target_type == "attraction":
            obj_result = await db.execute(
                select(Attraction).where(Attraction.id == body.navigated_target_id)
            )
        else:
            obj_result = await db.execute(
                select(Establishment).where(Establishment.id == body.navigated_target_id)
            )
        obj = obj_result.scalar_one_or_none()
        if obj:
            dist = _haversine_m(body.latitude, body.longitude, obj.latitude, obj.longitude)
            if dist <= THRESHOLD_METERS:
                navigated_arrived = True
                place_name = obj.name
                arrived_target_id = body.navigated_target_id
                arrived_target_type = body.navigated_target_type
                # Idempotent visit log: one row per (user, target, day)
                existing_log = (
                    await db.execute(
                        select(VisitorLog).where(
                            VisitorLog.visitor_user_id == user.id,
                            VisitorLog.target_type == body.navigated_target_type,
                            VisitorLog.target_id == body.navigated_target_id,
                            VisitorLog.visit_date == today,
                        )
                    )
                ).scalar_one_or_none()
                if existing_log is None:
                    db.add(
                        VisitorLog(
                            target_type=body.navigated_target_type,
                            target_id=body.navigated_target_id,
                            visitor_count=1,
                            visitor_name=user.username,
                            is_system_user=True,
                            logged_by=user.id,
                            visitor_user_id=user.id,
                            notes="verified via GPS arrival at navigated destination",
                        )
                    )

    return {
        "success": True,
        "booking_attended": booking_attended,
        "navigated_arrived": navigated_arrived,
        "place_name": place_name,
        "target_id": arrived_target_id,
        "target_type": arrived_target_type,
    }


# ───────────────────────────────────────────────────────────────
# ADMIN — List reservations (admin / contributor / business_owner)
# ───────────────────────────────────────────────────────────────

class AdminBookingItem(BaseModel):
    """Local response model — matches frontend admin/bookings page shape."""

    id: int
    date: str
    asset: str
    tourist: str
    party_size: int
    status: str


def _asset_name(asset: BookableAsset) -> str:
    if asset is None:
        return "Unknown asset"
    if asset.attraction is not None:
        return asset.attraction.name
    if asset.heritage_profile is not None:
        return asset.heritage_profile.common_name or asset.heritage_profile.name_of_asset or f"Asset #{asset.id}"
    return f"Asset #{asset.id}"


@router.get(
    "/admin/list",
    response_model=list[AdminBookingItem],
    summary="List all reservations for admin review",
)
async def list_reservations_admin(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(require_roles("admin", "contributor", "business_owner"))],
):
    stmt = (
        select(Reservation)
        .options(
            selectinload(Reservation.slot)
            .selectinload(BookingSlot.bookable_asset)
            .selectinload(BookableAsset.attraction),
            selectinload(Reservation.slot)
            .selectinload(BookingSlot.bookable_asset)
            .selectinload(BookableAsset.heritage_profile),
            selectinload(Reservation.user),
        )
        .join(Reservation.slot)
        .order_by(BookingSlot.date.desc(), Reservation.id.desc())
    )
    reservations = (await db.execute(stmt)).scalars().all()

    items: list[AdminBookingItem] = []
    for r in reservations:
        asset = r.slot.bookable_asset if r.slot else None
        tourist = r.user
        items.append(
            AdminBookingItem(
                id=r.id,
                date=r.slot.date.isoformat() if r.slot and r.slot.date else "",
                asset=_asset_name(asset),
                tourist=f"{tourist.username} ({tourist.email})" if tourist else "Unknown",
                party_size=r.party_size,
                status=r.status,
            )
        )
    return items
