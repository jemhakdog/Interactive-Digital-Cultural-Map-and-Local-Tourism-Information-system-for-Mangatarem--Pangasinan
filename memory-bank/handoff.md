# Handoff

- Last touched: 2026-09-02
- Last model: Pi Coding Agent (Claude)
- Branch: main
- Status: **Vercel deployment complete and verified** — backend + frontend live, Google OAuth login working.

## Current state

The repo is fully migrated from Flask to **FastAPI (backend/) + Next.js (frontend/)**. That migration was completed 2026-09-01 (see MEMORY.md). Today (2026-09-02) we deployed both to Vercel.

## Live deployments

| App | URL | Status |
|---|---|---|
| Backend (FastAPI) | https://mangatarem-tourism-api.vercel.app | ✅ live, `/health` → 200 `{"status":"ok"}`, CORS verified |
| Frontend (Next.js) | https://mangatarem-tourism-frontend.vercel.app | ✅ live & public |

**Critical URL nuance:** the frontend has TWO aliases:
- `https://mangatarem-tourism-frontend.vercel.app` → **public** (this is the one to use/test)
- `https://mangatarem-tourism-frontend-jemhakdogs-projects.vercel.app` → **SSO-protected** (redirects to Vercel login) — because team SSO protection `all_except_custom_domains` applies to non-custom domains. Do NOT use this for testing.

## What was done today (deploy)

1. **Branch fix:** Vercel was auto-deploying from `main` which still had old Flask code. Fast-forwarded `main` to `feat/react-migration` (FastAPI+Next). Both projects deploy `main`.
2. **`api/index.py`** (new): Vercel Python-runtime ASGI entrypoint re-exporting `backend.app.main:app`.
3. **`backend/app/core/config.py`**: `async_database_url` now rewrites `postgresql://` → `postgresql+asyncpg://` (was SQLite-only `aiosqlite`).
4. **`pyproject.toml` + `uv.lock`**: added `asyncpg` dependency.
5. **frontend/src/components/image-upload.tsx**: replaced hardcoded `http://localhost:8000` with `API_BASE` (`@/lib/api`).
6. **Env vars set on Vercel backend project (`mangatarem-tourism-api`):**
   - `DATABASE_URL=postgresql://postgres.yeptvckixavcltatwhnw:<pw>@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres` — **port 6543 (transaction pooler), NOT 5432** (5432 gave `EMAXCONNSESSION max clients reached`).
   - `SECRET_KEY=<random hex>` (rotate later if needed)
   - `CORS_ORIGINS=["https://mangatarem-tourism-frontend.vercel.app","http://localhost:3000"]` (JSON array format — pydantic list)
   - Other legacy env already present (SMTP_*, SUPABASE_*, DB_PROVIDER=sqlite, mapbox, GEMINI — harmless, unused by FastAPI).
7. **Frontend project:** user created `mangatarem-tourism-frontend` (Next.js preset, root `frontend`). Deployed with `NEXT_PUBLIC_API_URL=https://mangatarem-tourism-api.vercel.app` via CLI (`vercel deploy --prod --build-env NEXT_PUBLIC_API_URL=...`). Note: that env was passed at build time, not stored as a project env — a future redeploy without `--build-env` will fall back to `http://localhost:8000`. Consider adding `NEXT_PUBLIC_API_URL` as a persistent project env.
8. **Old broken frontend project** (`interactive-digital-cultural-map-and-local-tourism-information-system-for-mangatarem-pangasinan`) still exists, configured `framework: "flask"`, builds Error. It can be deleted or ignored.
9. **Gitignore**: added `.vercel`; restored user's `supabase` npm devDependency (was stashed during branch switch).

## Resolved after initial deploy

- ✅ **Google OAuth `origin_mismatch`** — URL nuance: the deployed app popup uses the **short public URL** `https://mangatarem-tourism-frontend.vercel.app`. User added it to the Google OAuth client's Authorized JavaScript origins → **login works now** (user confirmed).
- ✅ **Intermittent backend 500** — Supabase pooler (pgbouncer transaction mode) rejects asyncpg prepared statements: `DuplicatePreparedStatementError` on fresh connections (`select pg_catalog.version()`). Fixed by `connect_args={"statement_cache_size": 0}` for Postgres URLs in `backend/app/core/database.py` (commit `bf6374e`). Verified live: `/health` 5/5 → 200.

## Known limitations (documented in `docs/VERCEL_DEPLOYMENT.md` + `docs/VERCEL_ARCH_DECISION.md`)

- **Uploads are ephemeral** on Vercel (server FS reset between invocations) — acceptable for capstone demo; future work = object storage.
- **`init_db()` dev-only**; no Alembic migration infra yet.
- Root `package.json` `npm run dev` runs both servers locally (unchanged).

## Deploy docs added this session

- `docs/VERCEL_DEPLOYMENT.md` — click-by-click dashboard guide
- `docs/VERCEL_ARCH_DECISION.md` — why two projects, choices, upload limitation
- `docs/VERCEL_CLI.md` — CLI alternative

## git state

- Branch: `main`. Last commit: `bf6374e` ("fix: disable asyncpg statement cache for Supabase pooler").
- Commits today: `69c77c5` (deploy support), `3a6b097` (asyncpg + config rewrite), `8f56e99` (chore: .vercel gitignore + supabase CLI dev dep), `87e6051` (memory bank update), `bf6374e` (statement cache fix).
- Note: local uncommitted change may exist — the `feat/react-migration` branch has prior work committed; main was fast-forwarded. Verify with `git status` before continuing.

## Previous session (2026-08-23, pre-migration era — historical only)

Business dashboard profile seeded + 422 bug fixed (details in old handoff below; superseded by migration).