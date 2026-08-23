"""Smoke test for new admin announcement/gallery/barangay endpoints (runnable standalone)."""
import asyncio
import os

os.environ.setdefault("SECRET_KEY", "x")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite://")

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa: E402

from backend.app.core.database import Base  # noqa: E402
from backend.app.models import Announcement, BarangayInfo, GalleryItem, User  # noqa: E402
from backend.app.api.admin import (  # noqa: E402
    moderate_gallery_item,
    update_announcement,
    update_barangay,
    ModerateBody,
    AnnouncementBody,
    BarangayUpdateBody,
)


async def main():
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = async_sessionmaker(engine, expire_on_commit=False)()

    admin = User(username="admin", email="a@x.com", role="admin", is_approved=True)
    session.add(admin)
    brgy = BarangayInfo(name="Poblacion")
    session.add(brgy)
    await session.commit()

    ann = Announcement(title="T", content="C", user_id=admin.id, status="pending")
    session.add(ann)
    g = GalleryItem(type="image", url="https://x/y.jpg", status="pending")
    session.add(g)
    await session.commit()

    # barangay narrative update
    res = await update_barangay(brgy.id, BarangayUpdateBody(mission="Serve"), None, session)
    assert res["success"] and res["id"] == brgy.id
    await session.refresh(brgy)
    assert brgy.mission == "Serve"

    # pending announcement gets published on edit
    res = await update_announcement(ann.id, AnnouncementBody(title="T2", content="C2"), admin, session)
    assert res["status"] == "published"
    await session.refresh(ann)
    assert ann.title == "T2"

    # gallery moderation
    res = await moderate_gallery_item(g.id, ModerateBody(action="approve"), None, session)
    assert res["status"] == "approved"
    try:
        await moderate_gallery_item(g.id, ModerateBody(action="nope"), None, session)
        raise SystemExit("expected 400 for bad action")
    except Exception as e:
        assert "400" in str(e), e

    print("ALL SMOKE CHECKS PASSED")


asyncio.run(main())
