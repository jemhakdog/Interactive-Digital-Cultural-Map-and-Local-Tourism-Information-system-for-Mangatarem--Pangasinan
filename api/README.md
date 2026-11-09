# `api` (Vercel Serverless Entrypoint)

## Overview
Vercel serverless execution entrypoint. Exposes the ASGI application object `app` to Vercel's Python runtime.

## Interface
- `app`: `fastapi.FastAPI` application instance re-exported from `backend.app.main:app`.
  - CORS middleware (`CORSMiddleware`) parameterized by `settings.cors_origins`
  - Lifespan context manager (`backend.app.main:lifespan`) initializing SQLite tables during development
  - 19 modular domain API routers mounted under `/api/*`
  - System health probes: `/health` (HTTP 200 `{"status": "ok"}`) and `/` (API metadata)

## Invariants
- Zero-Side-Effect Import: Importing `api/index.py` must not execute destructive or blocking side-effects outside of FastAPI/uvicorn lifecycle hooks.
- ASGI Compliance: The exported `app` object must strictly conform to ASGI 3.0 specification for compatibility with Vercel's ASGI bridge and local uvicorn runners.
- Router Delegation: All business logic and routing is delegated to `backend.app.main:app` and its respective domain controllers in `backend/app/api/`.

## Side Effects
- Runs `init_db()` during application startup when `settings.environment == 'development'`.
- Mounts static file directory for local development uploads (`/uploads`).
- Uploads in Vercel environment are ephemeral and reset across cold starts.

## Verification
- Run: `pytest`
