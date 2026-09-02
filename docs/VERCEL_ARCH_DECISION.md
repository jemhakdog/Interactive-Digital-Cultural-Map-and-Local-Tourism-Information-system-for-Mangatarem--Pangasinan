# Vercel Architecture Decision

Companion to [`VERCEL_DEPLOYMENT.md`](VERCEL_DEPLOYMENT.md) — the "why" behind the how.

## Why two Vercel projects, not one

Vercel serves one framework per project:
- A Next.js project runs `next build` + a Node/Vercel frontend runtime.
- A Python function project runs one file (e.g. `api/index.py`) as a serverless function.

FastAPI is an ASGI app — it needs a Python function entry, not Next.js. Therefore the
frontend and backend necessarily become two projects pointed at the same repo with
`Root Directory: frontend` and `Root Directory: /` respectively. This matches Vercel's own
monorepo guidance (developers import the same repo twice with a different root).

## Choices

| Concern | Decision | Why |
|---|---|---|
| Production DB | Supabase Postgres via `DATABASE_URL` | Vercel functions are ephemeral read-only filesystems — SQLite cannot persist. The app already reads `DATABASE_URL` in `config.py`. |
| Backend runtime | Vercel Python (3.12 default, `3.9` fallback) | ASGI is first-party; `mangum` optional only if the preset's ASGI adapter flakiness bites (track: Vercel issue #11545 "Python 3.12 does not honor Node ASGI" — pin to 3.9 + mangum as a fallback). |
| Backend root | repo root `.` | `backend.app.main:app` imports work unmodified; a one-file `api/index.py` wrapper (`from backend.app.main import app`) lets Vercel find the ASGI app. |
| Frontend env | `NEXT_PUBLIC_API_URL` (build-time) | Client-side `fetch` to the API needs the build-time public URL; the code already falls back to localhost for local-only dev. |
| `image-upload.tsx` | fixed hardcoded `http://localhost:8000` → `API_BASE` | Was pointing at the visitor's own machine; now consistent with `API_BASE`. |

## Known limitation — uploads are ephemeral

`backend/app/api/uploads.py` + `main.py` mount `/uploads` from the server filesystem.
**Vercel functions have no persistent filesystem** — an upload survives briefly and the file
vanishes once the instance recycles / the dir resets.

- It is acceptable for a **capstone demo** (single server, short-lived images).
- For production: move files to an object store (Supabase **Storage**, Cloudflare R2, S3) and
  serve them from that bucket; swap the upload handler to return e.g. `https://bucket.supabase.co/...` URLs.
- Same for `instance/` SQLite — replaced by Postgres via `DATABASE_URL`, so no data loss.

## What would *eventually* change (future Backend work)

- Real migrations: the app uses `create_all()` (`database.py`) which is dev-only;
  production needs Alembic or a one-time seed + `ALTER TABLE` on schema changes
  (there's already a `ponytail:` note on `backend/app/models/business.py:48`).
- Auth: Google OAuth (`google-client-id`) should use a prod client + redirect to the prod URL.
- SMTP secret: `SMTP_PASSWORD`/`SMTP_EMAIL` for mailer features (templates/emails).
- Secrets: rotate `SECRET_KEY`, never commit `.env`.

## Scale notes (free → paid)

- Free: ephemeral filesystem, 100GB bandwidth, 30d logs — fine for capstone/small traffic.
- Pay only if you exceed ~small UTA traffic or want dedicated instance. Each bump-up is
  a Vercel project setting change, not a code change.