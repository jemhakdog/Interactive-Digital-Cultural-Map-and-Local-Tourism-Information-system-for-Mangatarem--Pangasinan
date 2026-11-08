import io
import pytest
from httpx import AsyncClient, ASGITransport

from backend.app.main import app
from backend.app.core.dependencies import get_current_user
from backend.app.models.user import User


@pytest.fixture
def override_user():
    user = User(
        id=1,
        username="admin_tester",
        email="test@mangatarem.gov.ph",
        password="hashedpassword",
        role="admin",
        is_approved=True,
    )
    app.dependency_overrides[get_current_user] = lambda: user
    yield user
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_upload_image_valid_png(override_user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        files = {"file": ("test.png", io.BytesIO(png_bytes), "image/png")}
        resp = await ac.post("/api/uploads/image", files=files)
        assert resp.status_code == 200
        data = resp.json()
        assert "url" in data
        assert data["url"].startswith("/uploads/") or "supabase" in data["url"]


@pytest.mark.asyncio
async def test_upload_image_spoofed_extension(override_user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        fake_bytes = b"This is just plain text, not a PNG file!"
        files = {"file": ("malicious.png", io.BytesIO(fake_bytes), "image/png")}
        resp = await ac.post("/api/uploads/image", files=files)
        assert resp.status_code == 400
        assert "File signature does not match" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_upload_image_disallowed_extension(override_user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        files = {"file": ("test.exe", io.BytesIO(b"MZ..."), "application/octet-stream")}
        resp = await ac.post("/api/uploads/image", files=files)
        assert resp.status_code == 400
        assert "File extension '.exe' not allowed" in resp.json()["detail"]
