"""Gamification API router — QR check-in, navigation, passport.

Migrated from modules/gamification/routes.py (Flask) to FastAPI.
"""
from __future__ import annotations

import math
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.models.attractions import Attraction
from backend.app.models.business import Establishment
from backend.app.models.gamification import AchievementBadge, TouristCheckIn, UserPassport
from backend.app.models.user import User
from backend.app.schemas.gamification import (
    CheckinBadgeResponse,
    CheckinRequest,
    CheckinResponse,
    StartNavigationRequest,
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
# Navigation lock (Redis-backed session store)
# ───────────────────────────────────────────────────────────────
from datetime import timezone
from backend.app.core.redis import redis_client

NAV_SESSION_TTL = 86400  # 24 hours


@router.post("/start-navigation", summary="Lock active navigation route")
async def start_navigation(
    body: StartNavigationRequest,
    user: Annotated[User, Depends(get_current_user)],
):
    """Store active navigation target in Redis with 24h TTL."""
    import json
    session_data = {
        "route_id": body.id,
        "route_type": body.type,
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    await redis_client.set_json(f"nav:{user.id}", session_data, ttl=NAV_SESSION_TTL)
    return {"success": True, "message": "Active navigation route locked"}


@router.post("/stop-navigation", summary="Clear active navigation")
async def stop_navigation(
    user: Annotated[User, Depends(get_current_user)],
):
    await redis_client.delete(f"nav:{user.id}")
    return {"success": True, "message": "Active navigation route cleared"}


@router.get("/active-navigation", summary="Get active navigation session")
async def get_active_navigation(
    user: Annotated[User, Depends(get_current_user)],
):
    """Return the user's current active navigation, or null if none."""
    session = await redis_client.get_json(f"nav:{user.id}")
    if session is None:
        return {"active": False, "session": None}
    return {"active": True, "session": session}


# ───────────────────────────────────────────────────────────────
# GPS-validated QR check-in
# ───────────────────────────────────────────────────────────────

MAX_THRESHOLD = 50.0  # meters


@router.post("/checkin", summary="GPS-validated check-in", response_model=CheckinResponse)
async def verify_checkin(
    body: CheckinRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    # Get official coordinates
    target_lat = None
    target_lon = None
    spot_name = "Unknown"

    if body.type == "attraction":
        spot_result = await db.execute(select(Attraction).where(Attraction.id == body.id))
        spot = spot_result.scalar_one_or_none()
        if spot:
            target_lat, target_lon = spot.latitude, spot.longitude
            spot_name = spot.name
    elif body.type == "establishment":
        spot_result = await db.execute(select(Establishment).where(Establishment.id == body.id))
        spot = spot_result.scalar_one_or_none()
        if spot:
            target_lat, target_lon = spot.latitude, spot.longitude
            spot_name = spot.name

    if target_lat is None or target_lon is None:
        raise HTTPException(status_code=400, detail="Target has no registered coordinates")

    distance = _haversine_m(body.latitude, body.longitude, target_lat, target_lon)
    if distance > MAX_THRESHOLD:
        raise HTTPException(
            status_code=400,
            detail=f"Too far: {int(distance)}m from '{spot_name}'. Must be within {int(MAX_THRESHOLD)}m.",
        )

    # Check existing
    existing_q = select(TouristCheckIn).where(
        TouristCheckIn.user_id == user.id,
        TouristCheckIn.attraction_id == (body.id if body.type == "attraction" else None),
        TouristCheckIn.establishment_id == (body.id if body.type == "establishment" else None),
    )
    existing = (await db.execute(existing_q)).scalar_one_or_none()
    if existing:
        return CheckinResponse(
            success=True,
            message=f"Already checked in at '{spot_name}'",
            distance=int(distance),
            already_checked_in=True,
        )

    # Insert check-in (ON CONFLICT DO NOTHING)
    conflict_cols = ["user_id", "attraction_id"] if body.type == "attraction" else ["user_id", "establishment_id"]
    await db.execute(
        insert(TouristCheckIn)
        .values(
            user_id=user.id,
            attraction_id=body.id if body.type == "attraction" else None,
            establishment_id=body.id if body.type == "establishment" else None,
            latitude=body.latitude,
            longitude=body.longitude,
            distance_meters=distance,
        )
        .on_conflict_do_nothing(index_elements=conflict_cols)
    )
    await db.flush()

    # Badge unlock logic
    unlocked_badges: list[dict] = []
    passport_q = select(UserPassport.badge_id).where(UserPassport.user_id == user.id)
    unlocked_ids = set((await db.execute(passport_q)).scalars().all())

    badges_q = select(AchievementBadge)
    if unlocked_ids:
        badges_q = badges_q.where(~AchievementBadge.id.in_(unlocked_ids))
    badges = (await db.execute(badges_q)).scalars().all()

    checkin_q = select(TouristCheckIn.attraction_id).where(
        TouristCheckIn.user_id == user.id,
        TouristCheckIn.attraction_id.is_not(None),
    )
    visited_ids = set((await db.execute(checkin_q)).scalars().all())

    for badge in badges:
        req_ids = badge.target_locations or []
        if req_ids and all(rid in visited_ids for rid in req_ids):
            await db.execute(
                insert(UserPassport)
                .values(user_id=user.id, badge_id=badge.id)
                .on_conflict_do_nothing(index_elements=["user_id", "badge_id"])
            )
            unlocked_badges.append({
                "title": badge.title,
                "description": badge.description,
                "badge_image_url": badge.badge_image_url,
                "reward_promo": badge.reward_promo,
            })

    return CheckinResponse(
        success=True,
        message=f"Stamp awarded! Checked in at '{spot_name}'!",
        distance=int(distance),
        unlocked_badges=[CheckinBadgeResponse(**b) for b in unlocked_badges],
    )


# ───────────────────────────────────────────────────────────────
# Passport view
# ───────────────────────────────────────────────────────────────

@router.get("/passport", summary="View tourist passport")
async def view_passport(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    badges_result = await db.execute(select(AchievementBadge))
    badges = badges_result.scalars().all()

    unlocked_ids_q = select(UserPassport.badge_id).where(UserPassport.user_id == user.id)
    unlocked_ids = set((await db.execute(unlocked_ids_q)).scalars().all())

    visited_q = select(TouristCheckIn.attraction_id).where(
        TouristCheckIn.user_id == user.id,
        TouristCheckIn.attraction_id.is_not(None),
    )
    visited_ids = set((await db.execute(visited_q)).scalars().all())

    badges_data = []
    unlocked_coupons = []
    for badge in badges:
        is_unlocked = badge.id in unlocked_ids
        req_ids = badge.target_locations or []
        completed = sum(1 for rid in req_ids if rid in visited_ids)
        total = len(req_ids)
        pct = int((completed / total) * 100) if total else 0

        badges_data.append({
            "badge_id": badge.id,
            "title": badge.title,
            "description": badge.description,
            "badge_image_url": badge.badge_image_url,
            "is_unlocked": is_unlocked,
            "progress_pct": pct,
            "completed_reqs": completed,
            "total_reqs": total,
        })
        if is_unlocked and badge.reward_promo:
            unlocked_coupons.append({"badge_title": badge.title, "promo": badge.reward_promo})

    checkins_q = (
        select(TouristCheckIn)
        .where(TouristCheckIn.user_id == user.id)
        .order_by(TouristCheckIn.verified_at.desc())
        .limit(5)
    )
    recent = (await db.execute(checkins_q)).scalars().all()

    return {
        "badges": badges_data,
        "unlocked_coupons": unlocked_coupons,
        "recent_checkins": [
            {
                "id": c.id,
                "attraction_id": c.attraction_id,
                "establishment_id": c.establishment_id,
                "distance_meters": c.distance_meters,
                "verified_at": c.verified_at.isoformat() if c.verified_at else None,
            }
            for c in recent
        ],
    }
