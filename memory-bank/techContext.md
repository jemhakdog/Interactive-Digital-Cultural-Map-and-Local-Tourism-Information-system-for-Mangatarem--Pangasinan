# Tech Context

## Stack (current, post-migration)

- **Backend**: Python 3.12, **FastAPI**, SQLAlchemy (async), uvicorn
- **Frontend**: **Next.js 16** (App Router), React 19, Tailwind v4, maplibre-gl, SWR, shadcn/ui, zod
- **Database**: SQLite (`aiosqlite`) locally; **Supabase Postgres** (`asyncpg`) in production via `DATABASE_URL`
- **Auth**: JWT (`python-jose`), bcrypt via `passlib`, Google Sign-In (GSI, client-side `accounts.id`)
- **Package manager**: uv (Python), npm (Node)
- **Monorepo**: `backend/` (FastAPI), `frontend/` (Next.js), `tests/` (pytest, 13 tests), root `package.json` runs both via `concurrently`

## Commands

### Install
```bash
uv sync          # Python deps (backend + tests)
cd frontend && npm install
```

### Run locally
```bash
npm run dev      # runs backend (uvicorn :8000) + frontend (Next :3000) with concurrently
```

### Test
```bash
.venv/bin/python -m pytest -q   # 13 tests, tests/
cd frontend && npx playwright test   # E2E (optional)
```

### Lint
```bash
.venv/bin/uv run ruff check .   # or: ruff check backend tests
```

## Config (backend/app/core/config.py)

- Reads env vars / `.env`. Required: `SECRET_KEY`. Optional: `DATABASE_URL`, `CORS_ORIGINS` (JSON array), `GOOGLE_CLIENT_ID`, `ENVIRONMENT`, `SMTP_*`.
- `async_database_url`: `sqlite:///` → `sqlite+aiosqlite:///`, `postgresql://` → `postgresql+asyncpg://`.
- `init_db()` (create_all) runs only when `environment == "development"`; production relies on external DB setup (no Alembic yet — flagged).

## Vercel deployment specifics

- Backend: root `/`, Python runtime, entry `api/index.py` re-exports `backend.app.main:app`.
- Frontend: root `frontend/`, Next.js preset, `NEXT_PUBLIC_API_URL` build-time env.
- Supabase pooler: use **port 6543** (transaction) not 5432 (session) to avoid connection-pool exhaustion on serverless.
- Env vars on backend project: `DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGINS` (JSON array).
- Frontend project currently has **no persistent env vars** (API URL passed via `--build-env` at deploy) — pending addition.

## Tooling notes

- Vercel CLI authenticated as `jemhakdog` (`~/.vercel`). Team: `jemhakdogs-projects`.
- `vercel redeploy <url> --target production` rebuilds with new envs (add env → redeploy).

## Historical (pre-migration)

- Old stack: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, WTForms, Supabase, Upstash Redis, Tailwind. Superseded 2026-09-01.