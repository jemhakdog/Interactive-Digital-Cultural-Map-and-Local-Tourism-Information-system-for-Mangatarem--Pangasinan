"""Admin API router — admin-only management endpoints."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import require_admin
from backend.app.models.announcements import Announcement
from backend.app.models.attractions import Attraction, Review
from backend.app.models.barangay import BarangayInfo
from backend.app.models.business import BusinessVerification, Establishment
from backend.app.models.gallery import GalleryItem
from backend.app.models.user import User
from backend.app.schemas.auth import UserResponse

router = APIRouter()


class ModerateBody(BaseModel):
    """Generic moderation action body (admin-owned local schema)."""

    action: str


def _user_to_response(user: User) -> UserResponse:
    """Map User model → UserResponse."""
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.username,
        role=user.role or "user",
        is_approved=user.is_approved,
        created_at=user.created_at,
    )


@router.get("/users")
async def list_users(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
) -> dict:
    """Return a paginated list of all users (admin only)."""
    # Total count
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar_one()

    # Paginated users
    offset = (page - 1) * per_page
    result = await db.execute(
        select(User).order_by(User.id).offset(offset).limit(per_page)
    )
    users = result.scalars().all()

    return {
        "users": [_user_to_response(u) for u in users],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }


# ─────────────────────────────────────────────
# Review moderation
# ─────────────────────────────────────────────
async def _review_to_dict(r: Review, db: AsyncSession) -> dict:
    """Map a Review row to the fields the admin reviews UI reads."""
    user = await db.get(User, r.user_id)
    location = None
    if r.attraction_id:
        att = await db.get(Attraction, r.attraction_id)
        location = att.name if att else None
    elif r.establishment_id:
        est = await db.get(Establishment, r.establishment_id)
        location = est.name if est else None
    return {
        "id": r.id,
        "user_id": r.user_id,
        "user_name": user.username if user else "Visitor",
        "rating": r.rating,
        "comment": r.comment,
        "status": r.status,
        "target_type": (
            "attraction" if r.attraction_id else "establishment" if r.establishment_id else None
        ),
        "attraction_id": r.attraction_id,
        "establishment_id": r.establishment_id,
        "location": location,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }


@router.get("/reviews")
async def list_reviews(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Return all reviews with their moderation status (admin only)."""
    result = await db.execute(select(Review).order_by(Review.created_at.desc()))
    reviews = result.scalars().all()
    return {"reviews": [await _review_to_dict(r, db) for r in reviews]}


@router.post("/reviews/{review_id}/moderate")
async def moderate_review(
    review_id: int,
    body: ModerateBody,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Approve or reject a review."""
    if body.action not in ("approve", "reject"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="action must be 'approve' or 'reject'",
        )
    review = await db.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    review.status = "approved" if body.action == "approve" else "rejected"
    await db.flush()
    return {"success": True, "id": review.id, "status": review.status}


# ─────────────────────────────────────────────
# Merchant verification
# ─────────────────────────────────────────────
async def _verification_to_dict(v: BusinessVerification, db: AsyncSession) -> dict:
    """Enrich a BusinessVerification row with owner + establishment display fields."""
    owner = await db.get(User, v.user_id)
    est_result = await db.execute(
        select(Establishment).where(Establishment.owner_id == v.user_id).order_by(Establishment.id)
    )
    establishment = est_result.scalars().first()
    barangay_name = None
    if establishment and establishment.barangay_id:
        b = await db.get(BarangayInfo, establishment.barangay_id)
        barangay_name = b.name if b else None
    return {
        "verification_id": v.id,
        "user_id": v.user_id,
        "owner_name": owner.username if owner else None,
        "owner_email": owner.email if owner else None,
        "establishment_id": establishment.id if establishment else None,
        "name": establishment.name if establishment else None,
        "type": establishment.type if establishment else None,
        "barangay": barangay_name,
        "status": v.status,
        "permit_document_url": v.permit_document_url,
        "other_document_url": v.other_document_url,
        "submitted_at": v.submitted_at.isoformat() if v.submitted_at else None,
    }


@router.get("/merchants/pending")
async def list_pending_merchants(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Return pending BusinessVerification rows (admin only)."""
    result = await db.execute(
        select(BusinessVerification)
        .where(BusinessVerification.status == "pending")
        .order_by(BusinessVerification.submitted_at.desc())
    )
    rows = result.scalars().all()
    return {"merchants": [await _verification_to_dict(v, db) for v in rows]}


@router.post("/merchants/{merchant_id}/verify")
async def verify_merchant(
    merchant_id: int,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Verify a merchant: mark the BusinessVerification verified and approve its Establishment."""
    verification = await db.get(BusinessVerification, merchant_id)
    if verification is None:
        raise HTTPException(status_code=404, detail="Verification not found")
    verification.status = "verified"

    establishment_id = None
    est_result = await db.execute(
        select(Establishment).where(Establishment.owner_id == verification.user_id).order_by(Establishment.id)
    )
    establishment = est_result.scalars().first()
    if establishment:
        establishment.verified = True
        establishment.status = "approved"
        establishment_id = establishment.id

    await db.flush()
    return {
        "success": True,
        "verification_id": verification.id,
        "establishment_id": establishment_id,
        "status": verification.status,
    }


@router.post("/merchants/{merchant_id}/reject")
async def reject_merchant(
    merchant_id: int,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Reject a merchant: mark the BusinessVerification rejected and unapprove its Establishment."""
    verification = await db.get(BusinessVerification, merchant_id)
    if verification is None:
        raise HTTPException(status_code=404, detail="Verification not found")
    verification.status = "rejected"

    establishment_id = None
    est_result = await db.execute(
        select(Establishment).where(Establishment.owner_id == verification.user_id).order_by(Establishment.id)
    )
    establishment = est_result.scalars().first()
    if establishment:
        establishment.verified = False
        establishment.status = "rejected"
        establishment_id = establishment.id

    await db.flush()
    return {
        "success": True,
        "verification_id": verification.id,
        "establishment_id": establishment_id,
        "status": verification.status,
    }


# ─────────────────────────────────────────────
# Establishment moderation
# ─────────────────────────────────────────────
async def _establishment_to_dict(est: Establishment, db: AsyncSession) -> dict:
    """Map an Establishment row to the fields the admin establishments UI reads."""
    owner = await db.get(User, est.owner_id)
    barangay_name = None
    if est.barangay_id:
        b = await db.get(BarangayInfo, est.barangay_id)
        barangay_name = b.name if b else None
    return {
        "id": est.id,
        "name": est.name,
        "type": est.type,
        "status": est.status,
        "barangay": barangay_name,
        "owner_name": owner.username if owner else None,
        "owner_id": est.owner_id,
        "verified": est.verified,
        "cover_image_url": est.cover_image_url,
        "rating_avg": est.rating_avg,
        "created_at": est.created_at.isoformat() if est.created_at else None,
    }


@router.get("/establishments")
async def list_establishments_admin(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    status_filter: str | None = Query(None),
) -> dict:
    """Return all establishments with status (admin only)."""
    stmt = select(Establishment)
    if status_filter:
        stmt = stmt.where(Establishment.status == status_filter)
    stmt = stmt.order_by(Establishment.created_at.desc())
    result = await db.execute(stmt)
    establishments = result.scalars().all()
    return {
        "establishments": [await _establishment_to_dict(e, db) for e in establishments]
    }


@router.post("/establishments/{establishment_id}/moderate")
async def moderate_establishment(
    establishment_id: int,
    body: ModerateBody,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Approve, reject, or delete an establishment."""
    if body.action not in ("approve", "reject", "delete"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="action must be 'approve', 'reject', or 'delete'",
        )
    est = await db.get(Establishment, establishment_id)
    if est is None:
        raise HTTPException(status_code=404, detail="Establishment not found")
    if body.action == "delete":
        await db.delete(est)
        await db.flush()
        return {"success": True, "id": establishment_id, "action": "delete"}
    est.status = "approved" if body.action == "approve" else "rejected"
    await db.flush()
    return {"success": True, "id": est.id, "status": est.status}


# ─────────────────────────────────────────────
# User approval
# ─────────────────────────────────────────────
@router.get("/users/pending")
async def list_pending_users(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Return users awaiting approval (is_approved=False)."""
    result = await db.execute(
        select(User)
        .where(User.is_approved == False)
        .order_by(User.created_at.desc())
    )
    users = result.scalars().all()
    return {"users": [_user_to_response(u) for u in users], "total": len(users)}


@router.post("/users/{user_id}/approve")
async def approve_user(
    user_id: int,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Approve a user account."""
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_approved = True
    await db.flush()
    return {"success": True, **_user_to_response(user).model_dump()}


@router.post("/users/{user_id}/reject")
async def reject_user(
    user_id: int,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Reject / disable a user account."""
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_approved = False
    await db.flush()
    return {"success": True, **_user_to_response(user).model_dump()}



# ─────────────────────────────────────────────
# Announcements
# ─────────────────────────────────────────────
class AnnouncementBody(BaseModel):
    """Create/update payload for admin-owned announcements."""

    title: str
    content: str
    barangay_id: int | None = None


async def _announcement_to_dict(a: Announcement, db: AsyncSession) -> dict:
    author = await db.get(User, a.user_id) if a.user_id else None
    barangay = await db.get(BarangayInfo, a.barangay_id) if a.barangay_id else None
    return {
        "id": a.id,
        "title": a.title,
        "content": a.content,
        "status": a.status,
        "barangay_id": a.barangay_id,
        "barangay_name": barangay.name if barangay else None,
        "author_name": author.username if author else "LGU Mangatarem",
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


@router.get("/announcements")
async def list_announcements(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Return all announcements regardless of status (admin only)."""
    result = await db.execute(
        select(Announcement).order_by(Announcement.created_at.desc())
    )
    items = result.scalars().all()
    return {"announcements": [await _announcement_to_dict(a, db) for a in items]}


@router.post("/announcements", status_code=status.HTTP_201_CREATED)
async def create_announcement(
    body: AnnouncementBody,
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Create an announcement, published immediately (admin only)."""
    if body.barangay_id is not None and await db.get(BarangayInfo, body.barangay_id) is None:
        raise HTTPException(status_code=404, detail="Barangay not found")
    a = Announcement(
        title=body.title,
        content=body.content,
        user_id=admin.id,
        barangay_id=body.barangay_id,
        status="published",
    )
    db.add(a)
    await db.flush()
    await db.refresh(a)
    return _announcement_to_dict_sync(a)


def _announcement_to_dict_sync(a: Announcement) -> dict:
    # ponytail: no author/barangay enrichment on create response — list refetch covers it
    return {
        "id": a.id,
        "title": a.title,
        "content": a.content,
        "status": a.status,
        "barangay_id": a.barangay_id,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


@router.put("/announcements/{item_id}")
async def update_announcement(
    item_id: int,
    body: AnnouncementBody,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Update an announcement's text and/or publish state (admin only)."""
    a = await db.get(Announcement, item_id)
    if a is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    a.title = body.title
    a.content = body.content
    if body.barangay_id is not None:
        a.barangay_id = body.barangay_id
    if a.status not in ("published", "approved", "active"):
        a.status = "published"  # admin edits publish pending submissions
    await db.flush()
    return {"success": True, **_announcement_to_dict_sync(a)}


@router.delete("/announcements/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    item_id: int,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Delete an announcement (admin only)."""
    a = await db.get(Announcement, item_id)
    if a is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    await db.delete(a)


# ─────────────────────────────────────────────
# Gallery moderation
# ─────────────────────────────────────────────
@router.get("/gallery")
async def list_gallery_items(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Return all gallery items regardless of status (admin only)."""
    result = await db.execute(select(GalleryItem).order_by(GalleryItem.created_at.desc()))
    items = result.scalars().all()
    return {
        "items": [
            {
                "id": g.id,
                "type": g.type,
                "url": g.url,
                "caption": g.caption,
                "status": g.status,
                "created_at": g.created_at.isoformat() if g.created_at else None,
            }
            for g in items
        ]
    }


@router.post("/gallery/{item_id}/moderate")
async def moderate_gallery_item(
    item_id: int,
    body: ModerateBody,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Approve or reject a gallery item."""
    if body.action not in ("approve", "reject"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="action must be 'approve' or 'reject'",
        )
    g = await db.get(GalleryItem, item_id)
    if g is None:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    g.status = "approved" if body.action == "approve" else "rejected"
    await db.flush()
    return {"success": True, "id": g.id, "status": g.status}


@router.delete("/gallery/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gallery_item(
    item_id: int,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Delete a gallery item (admin only)."""
    g = await db.get(GalleryItem, item_id)
    if g is None:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    await db.delete(g)


# ─────────────────────────────────────────────
# Barangays
# ─────────────────────────────────────────────
class BarangayUpdateBody(BaseModel):
    """Optional narrative-field updates for a barangay."""

    mission: str | None = None
    vision: str | None = None
    history: str | None = None
    cultural_assets: str | None = None
    traditions: str | None = None
    local_practices: str | None = None
    unique_features: str | None = None


@router.get("/barangays")
async def list_barangays(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Return all barangays with content counts (admin only)."""
    rows = (await db.execute(select(BarangayInfo).order_by(BarangayInfo.name))).scalars().all()
    att_counts = dict(
        (await db.execute(select(Attraction.barangay_id, func.count()).group_by(Attraction.barangay_id))).all()
    )
    return {
        "barangays": [
            {
                "id": b.id,
                "name": b.name,
                "mission": b.mission,
                "vision": b.vision,
                "history": b.history,
                "attractions_count": att_counts.get(b.id, 0),
                "has_geo": b.map_geo_json is not None,
            }
            for b in rows
        ]
    }


@router.put("/barangays/{barangay_id}")
async def update_barangay(
    barangay_id: int,
    body: BarangayUpdateBody,
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """Update a barangay's narrative fields (admin only)."""
    b = await db.get(BarangayInfo, barangay_id)
    if b is None:
        raise HTTPException(status_code=404, detail="Barangay not found")
    for field in BarangayUpdateBody.model_fields:
        value = getattr(body, field)
        if value is not None:
            setattr(b, field, value)
    await db.flush()
    return {"success": True, "id": b.id, "name": b.name}
