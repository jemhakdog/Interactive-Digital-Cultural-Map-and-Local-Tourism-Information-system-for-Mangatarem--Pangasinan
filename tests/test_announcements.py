"""
Tests for public announcements API (FastAPI port of test_announcements.py).

The Flask-era test asserted on the HTML feed (/announcements). FastAPI is
API-first; the equivalent is GET /api/announcements which returns
{"announcements": [...]} with only approved announcements.
"""
import asyncio

from sqlalchemy import select

from backend.app.models.user import User
from backend.app.models.barangay import BarangayInfo
from backend.app.models.announcements import Announcement
from backend.app.core.database import async_session_factory


def _run(coro):
    return asyncio.run(coro)


def _seed(client, auth_headers):
    async def _seed_async():
        async with async_session_factory() as db:
            # Barangay
            brgy = BarangayInfo(name="Poblacion")
            db.add(brgy)
            await db.flush()
            # Contributor
            user = User(
                username="contrib_user",
                email="contrib@example.com",
                role="contributor",
                barangay_id=brgy.id,
            )
            user.set_password("password123")
            db.add(user)
            await db.flush()

            approved = Announcement(
                title="Approved Notice",
                content="This notice should be visible.",
                user_id=user.id,
                barangay_id=brgy.id,
                status="approved",
            )
            pending = Announcement(
                title="Pending Notice",
                content="This should be hidden from public.",
                user_id=user.id,
                status="pending",
            )
            db.add_all([approved, pending])
            await db.commit()

    _run(_seed_async())


def test_public_announcements_feed(client, auth_headers):
    """Only approved announcements appear in the public feed."""
    _seed(client, auth_headers)

    resp = client.get("/api/announcements")
    assert resp.status_code == 200
    data = resp.json()
    announcements = data["announcements"]
    titles = [a["title"] for a in announcements]
    assert "Approved Notice" in titles
    assert "Pending Notice" not in titles
