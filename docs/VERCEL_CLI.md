# Vercel CLI (optional alternative to the dashboard)

The main walkthrough in [`VERCEL_DEPLOYMENT.md`](VERCEL_DEPLOYMENT.md) uses the dashboard.
This is the equivalent **terminal-only** path if you ever want it. Not required for the
primary flow.

Prereqs: `node` ≥ 18, a Vercel token (Dashboard → Account Settings → Tokens → Create),
and the code pushed to GitHub.

## A — frontend project

```bash
cd frontend
npx vercel login          # or: npx vercel --prod --token $VERCEL_TOKEN
npx vercel --prod --token $VERCEL_TOKEN \
  --build-env NEXT_PUBLIC_API_URL=https://tourism-api.vercel.app \
  --build-env NEXT_PUBLIC_GOOGLE_CLIENT_ID=... # optional
```

## B — backend project

```bash
cd /path/to/repo
npx vercel --prod --token $VERCEL_TOKEN \
  --build-env DATABASE_URL=postgresql://... \
  --build-env SECRET_KEY=... \
  --build-env CORS_ORIGINS=https://tourism.vercel.app
```

Notes:
- Use build-time envs (`NEXT_PUBLIC_*` are baked in) — Vercel auto-detects the Python
  runtime for the root.
- File-based envs: `npx vercel env add KEY production` sets runtime-only vars.
- The one-file ASGI wrapper (`api/index.py`) described in the decision doc is only needed
  if the framework preset doesn't find `app` in `backend.app.main`.