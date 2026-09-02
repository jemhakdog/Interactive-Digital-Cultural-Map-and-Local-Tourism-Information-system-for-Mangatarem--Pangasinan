# Startup Context

Project: mangatarem-cultural-map (Mangatarem Interactive Digital Cultural Map & Tourism Information System).

Goal: Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan.

Last updated: 2026-09-02 (pm)

Current focus: **Deployment done and verified** — FastAPI backend + Next.js frontend live on Vercel with Supabase Postgres. Google OAuth login confirmed working; backend `/health` stable (5/5) after asyncpg statement-cache fix.

If resuming work or switching models, read `memory-bank/handoff.md` next.

Next:
- Consider persisting `NEXT_PUBLIC_API_URL` as a Vercel project env (currently build-time only).
- If first real DB write errors, seed tables against Supabase (init_db is dev-only).
- Optionally clean up old broken `flask`-framed Vercel project / rotate Supabase password.