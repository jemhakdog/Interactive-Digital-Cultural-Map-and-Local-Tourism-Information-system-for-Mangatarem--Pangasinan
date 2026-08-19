"""Heritage CRUD API — ported from Flask modules/heritage.

All five heritage types (built, natural, intangible, movable, mixed)
live in a single HERITAGE_PROFILE table, differentiated by asset_type.
"""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_active_user, require_admin
from backend.app.models.barangay import BarangayInfo
from backend.app.models.heritage import HeritageProfile
from backend.app.models.user import User
from backend.app.schemas.heritage import (
    HeritageListResponse,
    HeritageProfileCreate,
    HeritageProfileResponse,
    HeritageProfileUpdate,
    HeritageTypeItem,
    HeritageTypeListResponse,
    PaginationMeta,
)

router = APIRouter()

# ── Valid heritage type slugs ──
_VALID_TYPES: dict[str, str] = {
    "built": "Built Heritage",
    "natural": "Natural Heritage",
    "intangible": "Intangible Heritage",
    "movable": "Movable Heritage",
    "mixed": "Mixed Heritage",
}


def _validate_type(heritage_type: str) -> str:
    """Return the label for a valid type slug, else raise 404."""
    if heritage_type == "all":
        return "All Heritage"
    label = _VALID_TYPES.get(heritage_type)
    if label is None:
        raise HTTPException(status_code=404, detail=f"Invalid heritage type: {heritage_type}")
    return label


async def _profile_to_response(profile: HeritageProfile, db: AsyncSession) -> HeritageProfileResponse:
    barangay_name = None
    if profile.barangay_id:
        b = await db.get(BarangayInfo, profile.barangay_id)
        if b:
            barangay_name = b.name

    fd = profile.form_data or {}
    image_url = (
        fd.get("image_url")
        or fd.get("photo_url")
        or fd.get("facade_photo_url")
        or fd.get("cover_image_url")
    )
    category = fd.get("category") or fd.get("subcategory") or fd.get("type_of_object")
    stories = fd.get("stories") or fd.get("stories_associated") or fd.get("peoples_stories")
    protection_status = fd.get("protection_status") or fd.get("status_condition") or fd.get("practice_status")

    return HeritageProfileResponse(
        id=profile.id,
        asset_type=profile.asset_type,
        form_control_number=profile.form_control_number,
        form_data=profile.form_data,
        name_of_asset=profile.name_of_asset,
        common_name=profile.common_name,
        barangay_id=profile.barangay_id,
        barangay_name=barangay_name,
        location_details=profile.location_details,
        contact_person=profile.contact_person,
        contact_number=profile.contact_number,
        ownership_type=profile.ownership_type,
        owner_administrator=profile.owner_administrator,
        usage_status=profile.usage_status,
        latitude=profile.latitude,
        longitude=profile.longitude,
        significance=profile.significance,
        conservation_status=profile.conservation_status,
        template_slug=profile.template_slug,
        mapper_name=profile.mapper_name,
        date_profiled=profile.date_profiled,
        status=profile.status,
        user_id=profile.user_id,
        image_url=image_url,
        category=category,
        stories=stories,
        protection_status=protection_status,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


# ───────────────────────────────────────────────────────────────
# GET /api/heritage/ — list all heritage items across categories
# ───────────────────────────────────────────────────────────────

@router.get("/", response_model=HeritageListResponse, summary="List all heritage items")
async def list_all_heritage(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    type: str | None = Query(None, description="Filter by asset_type (built, natural, intangible, movable, mixed)"),
    search: str = Query("", max_length=200),
    barangay_id: int | None = Query(None),
):
    """Return paginated approved heritage items across all or filtered types."""
    stmt = select(HeritageProfile).where(HeritageProfile.status == "approved")

    if type and type != "all":
        stmt = stmt.where(HeritageProfile.asset_type == type)

    if barangay_id:
        stmt = stmt.where(HeritageProfile.barangay_id == barangay_id)

    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                HeritageProfile.name_of_asset.ilike(pattern),
                HeritageProfile.common_name.ilike(pattern),
                HeritageProfile.location_details.ilike(pattern),
                HeritageProfile.significance.ilike(pattern),
            )
        )

    # Total count (for pagination)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    # Paginated results
    stmt = stmt.order_by(HeritageProfile.created_at.desc(), HeritageProfile.id.desc())
    stmt = stmt.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    items = result.scalars().all()

    pages = (total + per_page - 1) // per_page if total else 0

    response_items = [await _profile_to_response(i, db) for i in items]

    return HeritageListResponse(
        heritage_type=type or "all",
        label=_VALID_TYPES.get(type or "", "All Heritage"),
        items=response_items,
        pagination=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        ),
    )


# ───────────────────────────────────────────────────────────────
# GET /api/heritage/types — list types with real counts
# ───────────────────────────────────────────────────────────────

@router.get("/types", response_model=HeritageTypeListResponse, summary="List heritage types with counts")
async def list_types(db: Annotated[AsyncSession, Depends(get_db)]):
    """Return all heritage types with approved-item counts from the DB."""
    # Count approved items per asset_type
    count_stmt = (
        select(
            HeritageProfile.asset_type,
            func.count(HeritageProfile.id).label("count"),
        )
        .where(HeritageProfile.status == "approved")
        .group_by(HeritageProfile.asset_type)
    )
    result = await db.execute(count_stmt)
    counts: dict[str, int] = {row.asset_type: row.count for row in result.all()}

    types = []
    for slug, label in _VALID_TYPES.items():
        types.append(
            HeritageTypeItem(
                slug=slug,
                label=label,
                label_plural=label + "s",
                count=counts.get(slug, 0),
            )
        )
    return HeritageTypeListResponse(types=types)


# ───────────────────────────────────────────────────────────────
# GET /api/heritage/{type} — list items by type (paginated)
# ───────────────────────────────────────────────────────────────

@router.get("/{heritage_type}", response_model=HeritageListResponse, summary="List heritage items by type")
async def list_by_type(
    heritage_type: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str = Query("", max_length=200),
    barangay_id: int | None = Query(None),
):
    """Return paginated approved heritage items of a given type."""
    label = _validate_type(heritage_type)

    stmt = select(HeritageProfile).where(HeritageProfile.status == "approved")
    if heritage_type != "all":
        stmt = stmt.where(HeritageProfile.asset_type == heritage_type)

    if barangay_id:
        stmt = stmt.where(HeritageProfile.barangay_id == barangay_id)

    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                HeritageProfile.name_of_asset.ilike(pattern),
                HeritageProfile.common_name.ilike(pattern),
                HeritageProfile.location_details.ilike(pattern),
                HeritageProfile.significance.ilike(pattern),
            )
        )

    # Total count (for pagination)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    # Paginated results
    stmt = stmt.order_by(HeritageProfile.created_at.desc(), HeritageProfile.id.desc())
    stmt = stmt.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    items = result.scalars().all()

    pages = (total + per_page - 1) // per_page if total else 0

    response_items = [await _profile_to_response(i, db) for i in items]

    return HeritageListResponse(
        heritage_type=heritage_type,
        label=label,
        items=response_items,
        pagination=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        ),
    )


# ───────────────────────────────────────────────────────────────
# GET /api/heritage/{type}/{id} — single item detail
# ───────────────────────────────────────────────────────────────

@router.get("/{heritage_type}/{item_id}", response_model=HeritageProfileResponse, summary="Heritage item detail")
async def detail(
    heritage_type: str,
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Return a single approved heritage item."""
    _validate_type(heritage_type)

    profile = await db.get(HeritageProfile, item_id)
    if profile is None or (heritage_type != "all" and profile.asset_type != heritage_type):
        raise HTTPException(status_code=404, detail="Heritage item not found")
    if profile.status != "approved":
        raise HTTPException(status_code=404, detail="Heritage item not found")

    return await _profile_to_response(profile, db)


# ───────────────────────────────────────────────────────────────
# POST /api/heritage/{type} — create (auth required)
# ───────────────────────────────────────────────────────────────

@router.post(
    "/{heritage_type}",
    response_model=HeritageProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a heritage profile",
)
async def create_profile(
    heritage_type: str,
    body: HeritageProfileCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Create a new heritage profile. Auth required; status defaults to 'pending'."""
    _validate_type(heritage_type)

    profile = HeritageProfile(
        asset_type=heritage_type,
        form_control_number=body.form_control_number,
        form_data=body.form_data,
        name_of_asset=body.name_of_asset,
        common_name=body.common_name,
        barangay_id=body.barangay_id,
        location_details=body.location_details,
        contact_person=body.contact_person,
        contact_number=body.contact_number,
        ownership_type=body.ownership_type,
        owner_administrator=body.owner_administrator,
        usage_status=body.usage_status,
        latitude=body.latitude,
        longitude=body.longitude,
        significance=body.significance,
        conservation_status=body.conservation_status,
        template_slug=body.template_slug,
        mapper_name=body.mapper_name,
        date_profiled=body.date_profiled,
        status=body.status,
        user_id=current_user.id,
    )
    db.add(profile)
    await db.flush()
    await db.refresh(profile)

    return await _profile_to_response(profile, db)


# ───────────────────────────────────────────────────────────────
# PUT /api/heritage/{type}/{id} — update (auth required)
# ───────────────────────────────────────────────────────────────

@router.put(
    "/{heritage_type}/{item_id}",
    response_model=HeritageProfileResponse,
    summary="Update a heritage profile",
)
async def update_profile(
    heritage_type: str,
    item_id: int,
    body: HeritageProfileUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Update an existing heritage profile. Auth required."""
    _validate_type(heritage_type)

    profile = await db.get(HeritageProfile, item_id)
    if profile is None or (heritage_type != "all" and profile.asset_type != heritage_type):
        raise HTTPException(status_code=404, detail="Heritage item not found")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    await db.flush()
    await db.refresh(profile)

    return await _profile_to_response(profile, db)


# ───────────────────────────────────────────────────────────────
# DELETE /api/heritage/{type}/{id} — delete (admin only)
# ───────────────────────────────────────────────────────────────

@router.delete(
    "/{heritage_type}/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a heritage profile",
)
async def delete_profile(
    heritage_type: str,
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _admin: Annotated[User, Depends(require_admin)],
):
    """Delete a heritage profile. Admin only."""
    _validate_type(heritage_type)

    profile = await db.get(HeritageProfile, item_id)
    if profile is None or (heritage_type != "all" and profile.asset_type != heritage_type):
        raise HTTPException(status_code=404, detail="Heritage item not found")

    await db.delete(profile)
    await db.flush()

