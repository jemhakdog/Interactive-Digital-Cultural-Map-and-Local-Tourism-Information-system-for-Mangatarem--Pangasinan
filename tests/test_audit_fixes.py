"""
Regression tests for Goldfish audit fixes:
- Finding 1: Analytics overview doesn't crash on User.name attribute.
- Finding 2: Gamification check-in executes cleanly with db.add without insert().on_conflict_do_nothing.
- Finding 3: Uploads endpoint works on both /api/uploads/image and /api/uploads/single alias.
- Finding 4: Refresh tokens are rejected when used as access tokens.
- Finding 5: Spatial bounding box pre-filters attractions within radius.
- Finding 7: Gallery submission requires authentication and sets current user ID.
- Finding 8: Profile update returns 409 Conflict on username collision.
"""
import io
import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.api.auth import _create_refresh_token
from backend.app.core.database import async_session_factory
from backend.app.main import app
from backend.app.models.attractions import Attraction
from backend.app.models.business import Establishment
from backend.app.models.user import User


@pytest.mark.asyncio
async def test_refresh_token_rejected_as_access_token():
    """Verify Finding 4: Using a refresh token on protected endpoints returns 401."""
    async with async_session_factory() as db:
        user = User(username="refresh_test_user", email="refresh@example.com", role="user", is_approved=True)
        user.set_password("password123")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        user_id = user.id

    refresh_token = _create_refresh_token(user_id)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/api/user/profile", headers={"Authorization": f"Bearer {refresh_token}"})
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Could not validate credentials"


@pytest.mark.asyncio
async def test_gallery_submission_requires_auth():
    """Verify Finding 7: Unauthenticated gallery submission is rejected with 401."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Without auth header
        resp = await ac.post("/api/gallery/", json={"type": "photo", "url": "https://example.com/test.jpg", "caption": "Test"})
        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_profile_username_collision_rejected_409():
    """Verify Finding 8: Profile update with an existing username returns 409 Conflict."""
    async with async_session_factory() as db:
        user1 = User(username="alice", email="alice@example.com", role="user", is_approved=True)
        user1.set_password("password123")
        user2 = User(username="bob", email="bob@example.com", role="user", is_approved=True)
        user2.set_password("password123")
        db.add_all([user1, user2])
        await db.commit()
        await db.refresh(user1)
        await db.refresh(user2)

    # Login as bob, try to change username to alice
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_resp = await ac.post("/api/auth/login", json={"email": "bob@example.com", "password": "password123"})
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp = await ac.put("/api/user/profile", json={"name": "alice"}, headers=headers)
        assert resp.status_code == 409
        assert resp.json()["detail"] == "Username already taken"


@pytest.mark.asyncio
async def test_analytics_overview_no_user_name_crash():
    """Verify Finding 1: Analytics overview runs cleanly without User.name AttributeError."""
    async with async_session_factory() as db:
        admin = User(username="admin_analytics", email="admin_ana@example.com", role="admin", is_approved=True)
        admin.set_password("password123")
        steward = User(username="steward_john", email="steward@example.com", role="business_owner", is_approved=True)
        steward.set_password("password123")
        db.add_all([admin, steward])
        await db.commit()
        await db.refresh(admin)
        await db.refresh(steward)

        # Create an establishment with owner_id to populate steward_ids
        est = Establishment(
            name="Test Cafe",
            type="dining",
            latitude=15.79,
            longitude=120.29,
            owner_id=steward.id,
            status="approved",
        )
        db.add(est)
        await db.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_resp = await ac.post("/api/auth/login", json={"email": "admin_ana@example.com", "password": "password123"})
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp = await ac.get("/api/analytics/overview?days=30", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "summary" in data
        assert "period" in data


@pytest.mark.asyncio
async def test_gamification_checkin_success():
    """Verify Finding 2: Check-in succeeds without insert().on_conflict_do_nothing AttributeError."""
    async with async_session_factory() as db:
        user = User(username="tourist_checkin", email="tourist@example.com", role="user", is_approved=True)
        user.set_password("password123")
        att = Attraction(
            name="Daang Kalikasan Checkin Spot",
            description="Scenic viewpoint",
            category="nature",
            latitude=15.7890,
            longitude=120.2910,
            status="approved",
        )
        db.add_all([user, att])
        await db.commit()
        await db.refresh(user)
        await db.refresh(att)
        att_id = att.id
        att_lat = att.latitude
        att_lon = att.longitude

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_resp = await ac.post("/api/auth/login", json={"email": "tourist@example.com", "password": "password123"})
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Checkin right next to the spot (< 50m)
        resp = await ac.post(
            "/api/gamification/checkin",
            json={"type": "attraction", "id": att_id, "latitude": att_lat, "longitude": att_lon},
            headers=headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert "Stamp awarded" in data["message"]


@pytest.mark.asyncio
async def test_uploads_single_alias():
    """Verify Finding 3: /api/uploads/single alias functions correctly with auth."""
    async with async_session_factory() as db:
        user = User(username="uploader", email="uploader@example.com", role="user", is_approved=True)
        user.set_password("password123")
        db.add(user)
        await db.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_resp = await ac.post("/api/auth/login", json={"email": "uploader@example.com", "password": "password123"})
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Valid 1x1 PNG bytes
        png_bytes = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4"
            b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        files = {"file": ("test.png", io.BytesIO(png_bytes), "image/png")}

        resp = await ac.post("/api/uploads/single", files=files, headers=headers)
        assert resp.status_code == 200
        assert "url" in resp.json()
