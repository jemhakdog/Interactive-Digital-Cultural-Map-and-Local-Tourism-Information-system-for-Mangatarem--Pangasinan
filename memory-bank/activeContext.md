# Active Context

## Current focus (2026-09-02, pm)

**Deployment is fully live and working.** Google OAuth login confirmed working by user. Backend `/health` 5/5 stable after fixing asyncpg prepared-statement error.

Resolved this session:
- ✅ Google OAuth `origin_mismatch` — user added short public frontend URL to Google Console allowlist; login works.
- ✅ Intermittent `DuplicatePreparedStatementError` on Supabase pooler — fixed with `connect_args={"statement_cache_size": 0}` in `backend/app/core/database.py` (commit `bf6374e`). Verified 5/5 `/health` 200.


## Live state

- **Backend** `https://mangatarem-tourism-api.vercel.app` — FastAPI, healthy (`/health` 200), CORS allows frontend.
- **Frontend** `https://mangatarem-tourism-frontend.vercel.app` — Next.js, public.
- Database: **Supabase Postgres** via pooler port **6543** (transaction mode). Env `DATABASE_URL` on backend project.
- Old `interactive-digital-cultural-map-...` Vercel project: broken `framework:flask`, unused. Keep or delete.

## Key decisions this session

1. **Two Vercel projects** (frontend root `frontend`, backend root `/`) — required by Vercel (one framework per project). Documented in `docs/VERCEL_ARCH_DECISION.md`.
2. **Postgres via `DATABASE_URL`**, not SQLite — Vercel serverless FS is ephemeral.
3. **Port 6543** (transaction pooler), not 5432 — avoids `max clients reached` pool exhaustion.
4. **`asyncpg`** added; `postgresql://` → `postgresql+asyncpg://` in `config.async_database_url`.
5. Frontend behind **SSO protection** on `-jemhakdogs-projects` alias; short alias is public. Use short URL for all testing.

## Files changed this session

- `api/index.py` (new — Vercel ASGI entrypoint)
- `backend/app/core/config.py` (asyncpg rewrite)
- `pyproject.toml`, `uv.lock` (asyncpg)
- `frontend/src/components/image-upload.tsx` (API_BASE)
- `.gitignore` (`.vercel`)
- `package.json`, `package-lock.json` (supabase CLI dev dep)
- Deploy docs (3 new)

## Next steps

1. If tables missing on first login: one-time seed script against Supabase (login already works, so tables look fine).
2. Consider adding `NEXT_PUBLIC_API_URL` as persistent project env (currently only passed via `--build-env` at deploy time) so future bare pushes don't fall back to `http://localhost:8000`.
3. Optionally deprecate/delete old broken `flask`-framed frontend project.
4. Rotate the Supabase DB password shared in chat (optional hygiene).

## Historical (pre-migration, 2026-07/08)

Flask-era audit/cleanup, Map V2 fixes, business dashboard seed — superseded by the FastAPI+Next migration (2026-09-01). See `progress.md` / old handoff history in git if needed.