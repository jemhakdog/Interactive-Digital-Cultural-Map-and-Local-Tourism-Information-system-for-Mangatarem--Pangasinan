"""
Pytest configuration and fixtures for the FastAPI test suite.

Uses an isolated SQLite database (env overrides) + the FastAPI TestClient.
The Flask app (`app.py` / `extensions` / `modules`) is NOT imported here.
"""
import os
import sys

# Isolate the DB before anything imports backend.app (settings are cached at import).
_TEST_DB = os.path.join(os.path.dirname(__file__), "test_fastapi.db")
os.environ["DB_PROVIDER"] = "sqlite"
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB}"  # config.py adds the aiosqlite driver
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["REDIS_ENABLED"] = "false"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from backend.app.core.database import engine
from backend.app.main import app
from backend.app.models.base import Base


@pytest.fixture(scope="session", autouse=True)
def _create_tables():
    """Create schema once for the whole session against the isolated SQLite file."""
    import asyncio

    async def _create_all():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_create_all())
    yield
    # Drop after session so re-runs start clean
    async def _drop_all():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

    asyncio.run(_drop_all())


@pytest.fixture(autouse=True)
def _clean_tables():
    """Truncate all tables before each test for isolation."""
    import asyncio

    from sqlalchemy import inspect as sa_inspect

    async def _clean():
        async with engine.begin() as conn:

            def _do(conn):
                from sqlalchemy import inspect as sa_inspect

                inspector = sa_inspect(conn)
                tables = list(reversed(inspector.get_table_names()))  # FK-safe order
                for t in tables:
                    conn.execute(text(f'DELETE FROM "{t}"'))

            await conn.run_sync(_do)

    asyncio.run(_clean())
    yield


@pytest.fixture
def client():
    """A synchronous test client for the FastAPI app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_headers(client):
    """Register + login a user, return Bearer headers."""

    def _make(role="user", username="test_user"):
        resp = client.post(
            "/api/auth/register",
            json={
                "name": username,
                "email": f"{username}@example.com",
                "password": "password123",
                "role": role,
            },
        )
        assert resp.status_code == 200, resp.text
        tokens = resp.json()
        return {"Authorization": f"Bearer {tokens['access_token']}"}

    return _make
