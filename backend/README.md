# Backend Blueprint

## Overview
The `backend/` directory houses the complete server-side application for the Mangatarem Interactive Digital Cultural Map and Local Tourism Information System. Built on Python 3.12 and FastAPI, it delivers asynchronous REST endpoints, database persistence (SQLite locally, Supabase PostgreSQL in production), Google OAuth authentication, and media storage.

## Subdirectories & Boundaries
- [`app/`](./app/README.md): Application entrypoint, routers, models, schemas, and core infrastructure.
- [`app/core/`](./app/core/README.md): Settings, async engine/session factories, and RBAC security dependencies.
- [`app/models/`](./app/models/README.md): SQLAlchemy 2.0 ORM persistence models.
- [`app/schemas/`](./app/schemas/README.md): Pydantic request and response schemas.
- [`app/api/`](./app/api/README.md): FastAPI presentation controllers and domain endpoints.

## Invariants
- The backend service must be importable and runnable via standard ASGI servers (`uvicorn backend.app.main:app`).
- All database interactions must be async-compatible.
- `statement_cache_size` is 0 for PostgreSQL to prevent asyncpg errors under transaction pooling.

## Verification
- Run: `.venv/bin/pytest tests/`
