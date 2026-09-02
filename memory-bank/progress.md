# Progress

## 2026-09-02 — Vercel deployment of FastAPI + Next.js (DONE)

Both apps deploy and run on Vercel:
- Backend `mangatarem-tourism-api` — FastAPI live, `/health` 200, CORS verified, Supabase Postgres connected (pooler :6543, asyncpg).
- Frontend `mangatarem-tourism-frontend` — Next.js public live.

Fixed during deploy:
1. Deploy from wrong branch (main had old Flask) → fast-forwarded main to FastAPI+Next.
2. Missing Postgres driver → added `asyncpg`; rewrote `postgresql://` → `postgresql+asyncpg://` in config.
3. Wrong DB password in Vercel env → corrected to real Supabase password.
4. `Max clients reached / pool_size 15` on Supabase session pooler → switched to transaction pooler port **6543**.
5. CORS missing → `CORS_ORIGINS` JSON array on backend.
6. Frontend Google OAuth origin → short public URL must be allowlisted in Google Console (user doing).

Deploy docs added: `docs/VERCEL_DEPLOYMENT.md`, `docs/VERCEL_ARCH_DECISION.md`, `docs/VERCEL_CLI.md`.

## Outstanding / known

- `init_db()` only runs in development — production tables need one-time seed (no Alembic yet). Login worked, so tables were created somehow (likely via an earlier /health cold-start run or user seed) — verify on first real write.
- Uploads ephemeral on Vercel — documented.
- Frontend `NEXT_PUBLIC_API_URL` currently passed only at build time via CLI; consider persisting.

## 2026-09-02 — Post-deploy fixes (DONE)

- ✅ Google OAuth `origin_mismatch` resolved — user added `https://mangatarem-tourism-frontend.vercel.app` to Google Console origins; login confirmed working.
- ✅ Intermittent `DuplicatePreparedStatementError` — asyncpg statement cache disabled for Postgres (`connect_args={"statement_cache_size": 0}`) in `backend/app/core/database.py`; `/health` 5/5 stable.

---

## Historical (pre-migration era — superseded)

94% of this file described Flask-era audit, ERD/DFD diagram work, manuscript (Chapters 1–3), PWA, seed work (2026-07). The app has since been fully migrated from Flask to FastAPI + Next.js (2026-09-01) — see git history and `MEMORY.md`. Those diagram/manuscript notes are no longer the active system state.