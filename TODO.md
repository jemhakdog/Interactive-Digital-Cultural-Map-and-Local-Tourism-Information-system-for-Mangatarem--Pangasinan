# Remaining Tasks — post-migration cleanup

Migration (Flask → FastAPI + Next.js) is DONE. **Cleanup complete — committed as `dd14780` (2026-09-02).**

## Status: all items closed ✅

### 1. Order-dependent duplicate-arrival test failure — STALE, does not reproduce
- `tests/test_booking_arrival.py::test_duplicate_arrival_prevention`
- Timezone root cause fixed in `backend/app/api/booking.py` verify-arrival:
  `today = datetime.now(UTC).date()` (idempotent per (user, navigated_target, day)).
- Verified 2026-09-02: full suite passes **86/86 twice**; both file orders of
  `visitor_analytics` ↔ `booking_arrival` pass (9/9); duplicate-arrival test alone ×3 passes.
  Persistent-DB + `_clean_tables` truncation confirmed working between tests.

### 2. Ruff lint errors — FIXED (0 errors)
- `uv run ruff check .` → **All checks passed!** 119 auto-fixed + 33 manual (36 findings).
- Manual judgments: narrowed 3 over-broad `except Exception` sites (google_auth.py,
  docs/diagrams/*.py); DTZ replacements keep naive-UTC semantics (`.replace(tzinfo=None)`)
  so writes still match UTC-naive `DateTime` columns; `--preview --fix` experiment reverted.
- **Regression caught & repaired:** the ruff lane's `git checkout -- .` also reverted the
  uncommitted migration edits to `pyproject.toml`/`uv.lock`. Rebuilt `pyproject.toml`
  (FastAPI + uvicorn + sqlalchemy[asyncio] + aiosqlite + alembic + pydantic-settings +
  python-multipart + passlib[bcrypt] + python-jose + slowapi + aiosmtplib + jinja2 + flask
  [legacy] etc., plus `[dependency-groups] dev` = pytest/pytest-asyncio/httpx/ruff) and
  regenerated `uv.lock`. Full CI green after rebuild.

### 3. CI green + commit — DONE
- Local CI sequence passes: `uv sync --all-extras --dev && uv run ruff check . && uv run pytest` (86 passed).
- Committed `dd14780` — 45 files: ruff fixes (backend/, build/, docs/, utils/), rebuilt
  pyproject.toml + uv.lock, booking.py timezone fix. TODO.md left untracked on purpose.

## Notes
- `uv` at `~/.local/bin/uv` (CI installs via `astral-sh/setup-uv`).
- `frontend/` builds clean; runtime = uvicorn + Next (`npm run dev`).
- No active Vercel/Cloudflare deploy — `vercel.json`/`wrangler.toml` deleted as stale.
- `utils/file_helpers.py` still imports flask (`current_app`/`url_for`) — kept intentionally,
  so `flask` stays in deps.
- Workflow-tool subagents were broken in this session (empty output / timeouts) — the cleanup
  was completed via direct `Agent` lanes + manual verification instead.
