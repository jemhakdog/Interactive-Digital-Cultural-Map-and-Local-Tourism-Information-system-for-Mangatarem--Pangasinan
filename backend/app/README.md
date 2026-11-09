# Backend Application Blueprint (`backend/app`)

## Overview
The `backend.app` package is the core application assembly layer. It instantiates the `FastAPI` application object, configures CORS middleware, binds startup/shutdown lifespan events, registers all 19 functional API routers, and mounts static file serving for uploads.

## Subdirectories & Boundaries
- [`core/`](./core/README.md): Settings, async database pooling, and auth dependencies.
- [`models/`](./models/README.md): SQLAlchemy 2.0 ORM persistence models.
- [`schemas/`](./schemas/README.md): Pydantic data validation and serialization models.
- [`api/`](./api/README.md): REST API route controllers and endpoints.

## Invariants
- Table initialization runs during startup lifespan only when `ENVIRONMENT` is `development`.
- CORS middleware allows origins configured in `Settings.cors_origins`.
- Mounted router routes conform to prefixes defined in `main.py`.

## Verification
- Run: `.venv/bin/pytest tests/`
