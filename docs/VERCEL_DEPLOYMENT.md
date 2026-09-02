# Vercel Deployment Guide (Frontend + Backend)

Also read: [`docs/VERCEL_ARCH_DECISION.md`](VERCEL_ARCH_DECISION.md) — the architecture notes
and reasons behind each choice here.

You DO **not** need the Vercel CLI for anything on this page. Everything is done in the
browser at https://vercel.com — click, paste, done.

You will create **two** Vercel projects (frontend + backend). They are separate apps living
in this same GitHub repo.

---

## 0. Before you start

| Needed | Where |
|---|---|
| A GitHub account with this repo pushed | https://github.com/jemhakdog/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan |
| A Vercel account (free) — sign in **with GitHub** | https://vercel.com |
| A Supabase project (free tier) — for the production database | https://supabase.com (create → *New Project* → your region + password) |

> **Why a real Postgres database is required.** Vercel's serverless functions are
> **ephemeral**: their filesystem (including your SQLite `.db` file) disappears between
> requests, and you cannot write to the server during a request anyway. The app already
> supports Postgres via `DATABASE_URL` (`backend/app/core/config.py`), so we simply point
> it at Supabase. Free Supabase Postgres is fine for a capstone.
>
> **Why two projects (not one).** A single Vercel project serves **one** framework (Next.js
> *or* Python functions) on **one** domain. Putting a Next.js frontend and a FastAPI backend
> in one project is not supported.

---

## 1. Production database (Supabase) — ~5 min

1. In Supabase click **Connect** → **Database Session** (or **Connection string** pane).
2. Copy the **PostgreSQL connection string** — it looks like:
   `postgresql://postgres.XXXX:YOUR_PASSWORD@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres`
3. Keep it in a scratch note — you'll paste it into Vercel as `DATABASE_URL` in step 3.

> You may later swap in Postgres from Neon/Railway/any host — the app only reads `DATABASE_URL`.

---

## 2. Project A — frontend (`frontend/`)

1. Go to https://vercel.com/new/import → **import your GitHub repo**.
2. **Root Directory:** `frontend` *(critical — everything below the dashboard config assumes this)*.
3. Framework Preset: **Next.js** (auto-detected). Build Command: `next build`. Output: override `next start`.
4. **Environment Variables** → paste the row:
   | Key | Value |
   |---|---|
   | `NEXT_PUBLIC_API_URL` | `https://your-backend.vercel.app` — *the backend URL from step 3; you can change this later, but the frontend must be rebuilt to pick up the change* |
   | `NEXT_PUBLIC_GOOGLE_CLIENT_ID` | (optional) your Google OAuth client ID. If blank, the Google button hides. |
   | `NEXT_PUBLIC_MAPBOX_TOKEN` | (optional) your Mapbox token, if the map feature uses it. |
   | `NEXT_PUBLIC_GEMINI_API_KEY` | (optional) if the app talks to Gemini. |
5. Click **Deploy**. Wait for the build — Next.js will compile. A green `✓` = done.

---

## 3. Project B — backend (`/` root) 

1. Go to https://vercel.com/new/import → click **Continue with GitHub**, same repo.
   - Name the project differently, e.g. `mangatarem-tourism-api`.
2. **Root Directory:** keep `.` (the repo root).
3. You'll see **Deploy** — but before that, set the three environment variables:
   | Key | Value |
   |---|---|
   | `DATABASE_URL` | the Supabase URL from step 1 |
   | `SECRET_KEY` | a long random string (`openssl rand -hex 32` or a password manager value) |
   | `CORS_ORIGINS` | `https://your-frontend.vercel.app` — *the URL of project A* |
4. Click **Deploy**. The build installs from `pyproject.toml`, builds assets, and starts the
   ASGI app.
5. In the project's **Settings → Functions & Deployment Config** confirm:
   - **Function Runtime:** `Python 3.12`
   - **Max Duration:** `60` (free tier)
   - **Output Preset:** blank
6. Test the API: visit `https://your-backend.vercel.app/health` → returns `{"status":"ok"}`.

---

## 4. Link them up

1. Copy the backend's URL, e.g. `https://mangatarem-tourism-api.vercel.app`.
2. In Project A (frontend) **Env vars → `NEXT_PUBLIC_API_URL`** = that URL.
3. **Redeploy frontend** (Dashboard → Deployments → `Redeploy`). Now `example.com`
   talks to your live API.

---

## 5. Before you call it done

- [ ] `https://<backend>.vercel.app/health` → `{"status":"ok"}`
- [ ] Frontend loads from `https://<frontend>.vercel.app`
- [ ] Log in / register a user on the live site (proves DB seed + auth against Supabase)
- [ ] Upload an image — then **confirm a known caveat**: uploads go to the _server-side_
      filesystem, which is **ephemeral** on Vercel. Files appear for a while, then vanish after
      the serverless instance recycles. **This is a known limitation** (see the decision doc).
      If you need permanent uploads, you must add a storage bucket service
      (see `docs/VERCEL_ARCH_DECISION.md → future Backend work`).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Backend `Runtime.ImportModuleError: No module named 'aiohttp'` | This is the known Python 3.12 ASGI flakiness on Vercel. Try pinning runtime `python3.9` + `mangum` (docs) or check the open issue in the decision doc. |
| Frontend API calls hit `localhost:8000` | You forgot `NEXT_PUBLIC_API_URL` — the code falls back to localhost for local dev only; on Vercel set it and Redeploy. |
| `CORS error` in browser | `CORS_ORIGINS` doesn't match the front project URL exactly. It must be the exact origin, no trailing slash, e.g. `https://abc.vercel.app`. |
| Database tables empty | `init_db()` only runs when `ENVIRONMENT=development`. Applications should create tables once: run `scripts/seed_or_migrate.py` once against production, or set production DB up through a migration. |
| Env var not applied | Env changes need a **redeploy** — edits only affect the *next* build. |

---

## Optional extras (not required)

- **Custom domain**: project settings → Domains → add `api.mangatarem.ph` or `www.mangatarem.ph`.
- **Password protection**: before launch, Settings → Protection → require auth to view.
- **Cost**: all of the above is on the free plans of Vercel + Supabase. Bumps to prod scale
  only when you hit limits (see decision doc, "Scale" section).