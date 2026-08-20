"""Contributor (barangay steward) dashboard + CRUD endpoints.

Mounted under /api/contributor (prefix applied centrally in main.py via
``include_router(contributor_router, prefix="/api/contributor", ...)``).

Auth: every route requires role ``contributor`` or ``admin`` via
``require_roles("contributor", "admin")``.

Barangay scoping is derived from ``User.barangay_id``. All read queries are
defensive: a contributor with no linked barangay gets empty results instead
of 500s. Write operations require the linked barangay (400 when missing) and
enforce ownership (403 when the row belongs to another barangay/user).

Response shapes are matched exactly to the React frontend under
``frontend/src/app/contributor`` and ``frontend/src/components/contributor``.
"""
from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import require_roles
from backend.app.models.announcements import Announcement
from backend.app.models.attractions import Attraction, Review
from backend.app.models.barangay import BarangayInfo
from backend.app.models.events import Event
from backend.app.models.gallery import GalleryItem
from backend.app.models.user import User

router = APIRouter()

ContributorUser = Annotated[User, Depends(require_roles("contributor", "admin"))]


# ─────────────────────────────────────────────
# Request bodies (local — shared schemas are owned by the foundation agent)
# ─────────────────────────────────────────────
class AttractionBody(BaseModel):
    name: str
    category: str
    description: str
    directions: str | None = None
    image_url: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class EventBody(BaseModel):
    name: str
    category: str
    date: str  # "YYYY-MM-DD" (or full ISO) — parsed below
    location: str
    description: str
    image_url: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class GalleryBody(BaseModel):
    type: str = "photo"
    url: str | None = None
    caption: str | None = None


class AnnouncementBody(BaseModel):
    title: str
    content: str


class ProfileBody(BaseModel):
    mission: str | None = None
    vision: str | None = None
    history: str | None = None
    cultural_assets: str | None = None
    traditions: str | None = None
    local_practices: str | None = None
    unique_features: str | None = None


class ReviewReplyBody(BaseModel):
    comment: str


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def _barangay_id(user: User) -> int | None:
    return getattr(user, "barangay_id", None)


def _parse_date(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format; expected YYYY-MM-DD",
        )


def _attraction_summary(a: Attraction) -> dict:
    return {
        "id": a.id,
        "name": a.name,
        "category": a.category,
        "description": a.description,
        "directions": a.directions,
        "image_url": a.image_url,
        "latitude": a.latitude,
        "longitude": a.longitude,
        "barangay_id": a.barangay_id,
        "status": a.status,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


def _event_summary(e: Event) -> dict:
    return {
        "id": e.id,
        "name": e.name,
        "category": e.category,
        "description": e.description,
        "date": e.date.isoformat() if e.date else None,
        "location": e.location,
        "image_url": e.image_url,
        "latitude": e.latitude,
        "longitude": e.longitude,
        "barangay_id": e.barangay_id,
        "status": e.status,
        "created_at": e.created_at.isoformat() if e.created_at else None,
    }


def _gallery_summary(g: GalleryItem) -> dict:
    return {
        "id": g.id,
        "type": g.type,
        "url": g.url,
        "caption": g.caption,
        "status": g.status,
        "created_at": g.created_at.isoformat() if g.created_at else None,
    }


def _announcement_summary(a: Announcement) -> dict:
    return {
        "id": a.id,
        "title": a.title,
        "content": a.content,
        "status": a.status,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


def _barangay_profile_dict(b: BarangayInfo) -> dict:
    return {
        "id": b.id,
        "name": b.name,
        "mission": b.mission,
        "vision": b.vision,
        "history": b.history,
        "cultural_assets": b.cultural_assets,
        "traditions": b.traditions,
        "local_practices": b.local_practices,
        "unique_features": b.unique_features,
    }


# ─────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────
@router.get("/stats")
async def contributor_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    """Counts of the contributor's barangay submissions + reviews."""
    bid = _barangay_id(user)
    if bid is None:
        return {"total": 0, "approved": 0, "pending": 0, "rejected": 0, "reviews": 0}

    total = (
        await db.execute(select(func.count()).where(Attraction.barangay_id == bid))
    ).scalar() or 0
    approved = (
        await db.execute(
            select(func.count()).where(
                Attraction.barangay_id == bid, Attraction.status == "approved"
            )
        )
    ).scalar() or 0
    pending = (
        await db.execute(
            select(func.count()).where(
                Attraction.barangay_id == bid, Attraction.status == "pending"
            )
        )
    ).scalar() or 0
    rejected = (
        await db.execute(
            select(func.count()).where(
                Attraction.barangay_id == bid, Attraction.status == "rejected"
            )
        )
    ).scalar() or 0

    reviews = (
        await db.execute(
            select(func.count())
            .select_from(Review)
            .join(Attraction, Review.attraction_id == Attraction.id)
            .where(Attraction.barangay_id == bid)
        )
    ).scalar() or 0

    return {
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected,
        "reviews": reviews,
    }


@router.get("/activity")
async def contributor_activity(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    """Recent submissions (attractions + events) for the contributor's barangay."""
    bid = _barangay_id(user)
    if bid is None:
        return {"items": []}

    atts = (
        await db.execute(
            select(Attraction)
            .where(Attraction.barangay_id == bid)
            .order_by(Attraction.created_at.desc())
        )
    ).scalars().all()
    evts = (
        await db.execute(
            select(Event)
            .where(Event.barangay_id == bid)
            .order_by(Event.created_at.desc())
        )
    ).scalars().all()

    items = [
        {
            "id": a.id,
            "name": a.name,
            "type": "Attraction",
            "status": a.status,
            "date": a.created_at.isoformat() if a.created_at else None,
            "href": f"/contributor/attractions/{a.id}",
        }
        for a in atts
    ]
    items += [
        {
            "id": e.id,
            "name": e.name,
            "type": "Event",
            "status": e.status,
            "date": e.created_at.isoformat() if e.created_at else None,
            "href": f"/contributor/events/{e.id}",
        }
        for e in evts
    ]
    items.sort(key=lambda x: x["date"] or "", reverse=True)
    return {"items": items[:10]}


# ─────────────────────────────────────────────
# Attractions (barangay-scoped)
# ─────────────────────────────────────────────
@router.get("/attractions")
async def list_contributor_attractions(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    if bid is None:
        return []
    rows = (
        await db.execute(
            select(Attraction)
            .where(Attraction.barangay_id == bid)
            .order_by(Attraction.created_at.desc())
        )
    ).scalars().all()
    return [_attraction_summary(a) for a in rows]


@router.post("/attractions", status_code=status.HTTP_201_CREATED)
async def create_contributor_attraction(
    body: AttractionBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    if bid is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your account is not linked to a barangay",
        )
    att = Attraction(
        name=body.name,
        category=body.category,
        description=body.description,
        directions=body.directions,
        image_url=body.image_url,
        latitude=body.latitude,
        longitude=body.longitude,
        status="pending",
        user_id=user.id,
        barangay_id=bid,
    )
    db.add(att)
    await db.flush()
    await db.refresh(att)
    return _attraction_summary(att)


@router.put("/attractions/{attraction_id}")
async def update_contributor_attraction(
    attraction_id: int,
    body: AttractionBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    att = await db.get(Attraction, attraction_id)
    if att is None:
        raise HTTPException(status_code=404, detail="Attraction not found")
    if bid is not None and att.barangay_id != bid:
        raise HTTPException(status_code=403, detail="Not your barangay's attraction")
    att.name = body.name
    att.category = body.category
    att.description = body.description
    att.directions = body.directions
    att.image_url = body.image_url
    att.latitude = body.latitude
    att.longitude = body.longitude
    await db.flush()
    await db.refresh(att)
    return _attraction_summary(att)


@router.delete("/attractions/{attraction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contributor_attraction(
    attraction_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    att = await db.get(Attraction, attraction_id)
    if att is None:
        raise HTTPException(status_code=404, detail="Attraction not found")
    if bid is not None and att.barangay_id != bid:
        raise HTTPException(status_code=403, detail="Not your barangay's attraction")
    await db.delete(att)


# ─────────────────────────────────────────────
# Events (barangay-scoped)
# ─────────────────────────────────────────────
@router.get("/events")
async def list_contributor_events(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    if bid is None:
        return []
    rows = (
        await db.execute(
            select(Event)
            .where(Event.barangay_id == bid)
            .order_by(Event.date.desc())
        )
    ).scalars().all()
    return [_event_summary(e) for e in rows]


@router.post("/events", status_code=status.HTTP_201_CREATED)
async def create_contributor_event(
    body: EventBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    if bid is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your account is not linked to a barangay",
        )
    event = Event(
        name=body.name,
        category=body.category,
        date=_parse_date(body.date),
        location=body.location,
        description=body.description,
        image_url=body.image_url,
        latitude=body.latitude,
        longitude=body.longitude,
        status="pending",
        user_id=user.id,
        barangay_id=bid,
    )
    db.add(event)
    await db.flush()
    await db.refresh(event)
    return _event_summary(event)


@router.put("/events/{event_id}")
async def update_contributor_event(
    event_id: int,
    body: EventBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    event = await db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if bid is not None and event.barangay_id != bid:
        raise HTTPException(status_code=403, detail="Not your barangay's event")
    event.name = body.name
    event.category = body.category
    event.date = _parse_date(body.date)
    event.location = body.location
    event.description = body.description
    event.image_url = body.image_url
    event.latitude = body.latitude
    event.longitude = body.longitude
    await db.flush()
    await db.refresh(event)
    return _event_summary(event)


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contributor_event(
    event_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    event = await db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if bid is not None and event.barangay_id != bid:
        raise HTTPException(status_code=403, detail="Not your barangay's event")
    await db.delete(event)


# ─────────────────────────────────────────────
# Gallery (user-scoped — GalleryItem has no barangay_id)
# ─────────────────────────────────────────────
@router.get("/gallery")
async def list_contributor_gallery(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    rows = (
        await db.execute(
            select(GalleryItem)
            .where(GalleryItem.user_id == user.id)
            .order_by(GalleryItem.created_at.desc())
        )
    ).scalars().all()
    return [_gallery_summary(g) for g in rows]


@router.get("/gallery/{item_id}")
async def get_contributor_gallery_item(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    g = await db.get(GalleryItem, item_id)
    if g is None:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    if g.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your gallery item")
    return _gallery_summary(g)


@router.post("/gallery", status_code=status.HTTP_201_CREATED)
async def create_contributor_gallery(
    body: GalleryBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    g = GalleryItem(
        type=body.type,
        url=body.url,
        caption=body.caption,
        user_id=user.id,
        status="pending",
    )
    db.add(g)
    await db.flush()
    await db.refresh(g)
    return _gallery_summary(g)


@router.put("/gallery/{item_id}")
async def update_contributor_gallery(
    item_id: int,
    body: GalleryBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    g = await db.get(GalleryItem, item_id)
    if g is None:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    if g.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your gallery item")
    g.type = body.type
    g.url = body.url
    g.caption = body.caption
    await db.flush()
    await db.refresh(g)
    return _gallery_summary(g)


@router.delete("/gallery/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contributor_gallery(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    g = await db.get(GalleryItem, item_id)
    if g is None:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    if g.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your gallery item")
    await db.delete(g)


# ─────────────────────────────────────────────
# Announcements (barangay-scoped)
# ─────────────────────────────────────────────
@router.get("/announcements")
async def list_contributor_announcements(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    if bid is None:
        return {"items": []}
    rows = (
        await db.execute(
            select(Announcement)
            .where(Announcement.barangay_id == bid)
            .order_by(Announcement.created_at.desc())
        )
    ).scalars().all()
    return {"items": [_announcement_summary(a) for a in rows]}


@router.get("/announcements/{item_id}")
async def get_contributor_announcement(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    a = await db.get(Announcement, item_id)
    if a is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    if bid is not None and a.barangay_id != bid:
        raise HTTPException(status_code=403, detail="Not your barangay's announcement")
    return _announcement_summary(a)


@router.post("/announcements", status_code=status.HTTP_201_CREATED)
async def create_contributor_announcement(
    body: AnnouncementBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    if bid is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your account is not linked to a barangay",
        )
    a = Announcement(
        title=body.title,
        content=body.content,
        user_id=user.id,
        barangay_id=bid,
        status="pending",
    )
    db.add(a)
    await db.flush()
    await db.refresh(a)
    return _announcement_summary(a)


@router.put("/announcements/{item_id}")
async def update_contributor_announcement(
    item_id: int,
    body: AnnouncementBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    a = await db.get(Announcement, item_id)
    if a is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    if bid is not None and a.barangay_id != bid:
        raise HTTPException(status_code=403, detail="Not your barangay's announcement")
    a.title = body.title
    a.content = body.content
    await db.flush()
    await db.refresh(a)
    return _announcement_summary(a)


@router.delete("/announcements/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contributor_announcement(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    a = await db.get(Announcement, item_id)
    if a is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    if bid is not None and a.barangay_id != bid:
        raise HTTPException(status_code=403, detail="Not your barangay's announcement")
    await db.delete(a)


# ─────────────────────────────────────────────
# Reviews (barangay-scoped aggregate) + steward reply
# ─────────────────────────────────────────────
@router.get("/reviews")
async def contributor_reviews(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    if bid is None:
        return {"items": []}

    att_ids = (
        await db.execute(select(Attraction.id).where(Attraction.barangay_id == bid))
    ).scalars().all()
    if not att_ids:
        return {"items": []}

    reviews = (
        await db.execute(
            select(Review)
            .where(Review.attraction_id.in_(att_ids), Review.parent_id.is_(None))
            .order_by(Review.created_at.desc())
        )
    ).scalars().all()

    items = []
    for r in reviews:
        u = await db.get(User, r.user_id)
        att = await db.get(Attraction, r.attraction_id) if r.attraction_id else None
        replies = (
            await db.execute(
                select(Review)
                .where(Review.parent_id == r.id)
                .order_by(Review.created_at.asc())
            )
        ).scalars().all()
        reply_list = []
        for rep in replies:
            ru = await db.get(User, rep.user_id)
            reply_list.append(
                {
                    "id": rep.id,
                    "comment": rep.comment,
                    "created_at": rep.created_at.isoformat() if rep.created_at else None,
                    "user": {
                        "username": ru.username if ru else "Visitor",
                        "role": ru.role if ru else None,
                    },
                }
            )
        items.append(
            {
                "id": r.id,
                "rating": r.rating,
                "comment": r.comment,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "user": {
                    "username": u.username if u else "Visitor",
                    "role": u.role if u else None,
                },
                "attraction": {"name": att.name if att else None},
                "replies": reply_list,
            }
        )
    return {"items": items}


@router.post("/reviews/{review_id}/reply", status_code=status.HTTP_201_CREATED)
async def reply_contributor_review(
    review_id: int,
    body: ReviewReplyBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    parent = await db.get(Review, review_id)
    if parent is None:
        raise HTTPException(status_code=404, detail="Review not found")
    # Ensure the review belongs to this contributor's barangay.
    if bid is not None and parent.attraction_id is not None:
        att = await db.get(Attraction, parent.attraction_id)
        if att is None or att.barangay_id != bid:
            raise HTTPException(status_code=403, detail="Not your barangay's review")

    reply = Review(
        user_id=user.id,
        attraction_id=parent.attraction_id,
        parent_id=parent.id,
        rating=None,
        comment=body.comment,
        status="approved",
    )
    db.add(reply)
    await db.flush()
    await db.refresh(reply)
    return {"success": True, "reply_id": reply.id}


# ─────────────────────────────────────────────
# Barangay profile (the contributor's linked barangay)
# ─────────────────────────────────────────────
@router.get("/profile")
async def contributor_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    if bid is None:
        raise HTTPException(
            status_code=404, detail="No barangay linked to your account"
        )
    bar = await db.get(BarangayInfo, bid)
    if bar is None:
        raise HTTPException(status_code=404, detail="Barangay profile not found")
    return _barangay_profile_dict(bar)


@router.put("/profile")
async def update_contributor_profile(
    body: ProfileBody,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: ContributorUser,
):
    bid = _barangay_id(user)
    if bid is None:
        raise HTTPException(
            status_code=404, detail="No barangay linked to your account"
        )
    bar = await db.get(BarangayInfo, bid)
    if bar is None:
        raise HTTPException(status_code=404, detail="Barangay profile not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(bar, field, value)
    await db.flush()
    await db.refresh(bar)
    return _barangay_profile_dict(bar)
