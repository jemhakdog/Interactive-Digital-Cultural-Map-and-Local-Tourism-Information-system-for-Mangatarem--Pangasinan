"""Runtime smoke test for the newly-added FastAPI endpoints.

Uses a FRESH temp sqlite DB (DATABASE_URL override) so it never touches the
real dev database. Seeds one user per role + a barangay + an establishment,
mints JWTs, then hits every new endpoint and flags any HTTP 500 (server error)
or unhandled exception. 422/404/401/403 are expected for missing resources and
are NOT treated as failures.

Run:  SECRET_KEY=smoke .venv/bin/python backend/scripts/smoke_test_endpoints.py
"""
from __future__ import annotations

import os
import asyncio

os.environ["SECRET_KEY"] = "smoke-test-secret-key"
os.environ["DATABASE_URL"] = "sqlite:///./smoke_test.db"  # config converts to +aiosqlite

from jose import jwt  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from backend.app.core.database import init_db, async_session_factory  # noqa: E402
from backend.app.main import app  # noqa: E402
from backend.app.core.config import get_settings  # noqa: E402
from backend.app.models.user import User  # noqa: E402
from backend.app.models.barangay import BarangayInfo  # noqa: E402
from backend.app.models.business import Establishment  # noqa: E402
from backend.app.core.database import engine  # noqa: E402
from passlib.context import CryptContext  # noqa: E402

pwd = CryptContext(schemes=["bcrypt"])
SECRET = get_settings().secret_key


async def seed() -> dict:
    await init_db()
    async with async_session_factory() as s:
        bar = BarangayInfo(
            name="Smoke Barangay", mission="Mission", vision="Vision", history="History",
        )
        s.add(bar)
        await s.flush()
        ids = {}
        for role in ["admin", "contributor", "business_owner", "user"]:
            u = User(email=f"{role}@smoke.test", username=role, role=role, is_approved=True)
            u.password = pwd.hash("password123")
            s.add(u)
            await s.flush()
            ids[role] = u.id
        est = Establishment(
            name="Smoke Biz", type="restaurant", owner_id=ids["business_owner"],
            status="pending", barangay_id=bar.id, latitude=15.0, longitude=120.0,
        )
        s.add(est)
        await s.flush()
        ids["establishment"] = est.id
        await s.commit()
        return ids


def make_token(uid: int) -> str:
    return jwt.encode({"sub": str(uid)}, SECRET, algorithm="HS256")


# (method, path_template, role, json_body)  role=None -> no auth
TESTS = [
    ("GET", "/api/barangays", None, None),
    ("GET", "/api/announcements", None, None),
    ("GET", "/api/documents", None, None),
    ("GET", "/api/newsletter/subscribers", None, None),
    ("GET", "/api/visitor-registry", None, None),
    ("GET", "/api/visits", None, None),

    ("GET", "/api/admin/reviews", "admin", None),
    ("GET", "/api/admin/merchants/pending", "admin", None),
    ("GET", "/api/admin/establishments", "admin", None),
    ("GET", "/api/admin/users/pending", "admin", None),
    ("POST", "/api/admin/users/1/approve", "admin", None),
    ("POST", "/api/admin/users/1/reject", "admin", None),
    ("POST", "/api/admin/merchants/1/verify", "admin", None),
    ("POST", "/api/admin/establishments/1/moderate", "admin", {"action": "approve"}),
    ("POST", "/api/admin/reviews/1/moderate", "admin", {"action": "approve"}),

    ("GET", "/api/contributor/stats", "contributor", None),
    ("GET", "/api/contributor/activity", "contributor", None),
    ("GET", "/api/contributor/attractions", "contributor", None),
    ("POST", "/api/contributor/attractions", "contributor", {"name": "X", "description": "y", "barangay_id": 1}),
    ("GET", "/api/contributor/events", "contributor", None),
    ("POST", "/api/contributor/events", "contributor", {"name": "X", "barangay_id": 1}),
    ("GET", "/api/contributor/gallery", "contributor", None),
    ("POST", "/api/contributor/gallery", "contributor", {"url": "http://x/y.jpg", "barangay_id": 1}),
    ("GET", "/api/contributor/announcements", "contributor", None),
    ("POST", "/api/contributor/announcements", "contributor", {"title": "T", "content": "c"}),
    ("GET", "/api/contributor/profile", "contributor", None),
    ("PUT", "/api/contributor/profile", "contributor", {"captain": "Cap2"}),
    ("GET", "/api/contributor/reviews", "contributor", None),
    ("POST", "/api/contributor/reviews/1/reply", "contributor", {"content": "r"}),

    ("GET", "/api/user/profile", "user", None),
    ("PUT", "/api/user/profile", "user", {"name": "NewName"}),
    ("GET", "/api/user/stats", "user", None),
    ("GET", "/api/user/favorites", "user", None),
    ("POST", "/api/user/favorites/1", "user", None),
    ("DELETE", "/api/user/favorites/1", "user", None),
    ("GET", "/api/user/visits", "user", None),

    ("POST", "/api/business/verification", "business_owner", {"establishment_id": "{establishment}"}),
    ("GET", "/api/business/{establishment}/reviews", "business_owner", None),
    ("GET", "/api/booking/admin/list", "admin", None),
]


def main() -> int:
    ids = asyncio.run(seed())
    tokens = {r: make_token(ids[r]) for r in ["admin", "contributor", "business_owner", "user"]}
    client = TestClient(app)

    failures = []
    print(f"{'METHOD':6} {'PATH':42} {'ROLE':14} STATUS")
    print("-" * 80)
    for method, path, role, body in TESTS:
        path = path.format(establishment=ids["establishment"])
        if isinstance(body, dict) and body.get("establishment_id") == "{establishment}":
            body = {**body, "establishment_id": ids["establishment"]}
        headers = {"Authorization": f"Bearer {tokens[role]}"} if role else {}
        try:
            resp = client.request(method, path, headers=headers, json=body)
        except Exception as e:  # pragma: no cover
            print(f"{method:6} {path:42} {str(role):14} EXC {e!r}")
            failures.append((method, path, role, f"EXC {e!r}"))
            continue
        status = resp.status_code
        mark = "  <-- 500" if status >= 500 else ""
        print(f"{method:6} {path:42} {str(role):14} {status}{mark}")
        if status >= 500:
            failures.append((method, path, role, status))
            try:
                print("    BODY:", resp.text[:400])
            except Exception:
                pass

    print("-" * 80)
    if failures:
        print(f"FAILURES ({len(failures)}): server errors / exceptions")
        for f in failures:
            print("  ", f)
        _dispose()
        return 1
    print("OK: no HTTP 500 / unhandled exceptions across all tested endpoints.")
    _dispose()
    return 0


def _dispose() -> None:
    try:
        asyncio.run(engine.dispose())
    except Exception:
        pass


if __name__ == "__main__":
    raise SystemExit(main())
