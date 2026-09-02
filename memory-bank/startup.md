# Startup Context

Project: mangatarem-cultural-map (Mangatarem Interactive Digital Cultural Map & Tourism Information System).

Goal: Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan.

Last updated: 2026-09-02

Current focus: **Deployment done** — FastAPI backend + Next.js frontend both live on Vercel with Supabase Postgres. Google OAuth origin fix is the only outstanding item (user adding short Vercel frontend domain to Google Cloud Console allowlist).

If resuming work or switching models, read `memory-bank/handoff.md` next.

Next:
- Confirm Google OAuth `origin_mismatch` clears after user registers `https://mangatarem-tourism-frontend.vercel.app` in Google Cloud Console.
- If first login hits "relation does not exist", run one-time table seed against Supabase (`init_db()` only runs in development env).
- Keep unknown project-specific requirements as `TBD` until user provides them.