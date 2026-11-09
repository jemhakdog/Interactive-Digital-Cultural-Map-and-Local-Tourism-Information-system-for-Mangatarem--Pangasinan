# Core Module Contract (`backend/app/core`)

## Overview
The `backend.app.core` package provides foundational runtime services for the Mangatarem Tourism System API, including configuration management via Pydantic Settings, asynchronous database engine and session pooling via SQLAlchemy, and dependency injection guards for authentication, authorization (RBAC), and transactional database sessions.

## Interface
- `Settings`, `get_settings`: Pydantic `BaseSettings` reading environment variables (`.env`) with computed `async_database_url`.
- `engine: AsyncEngine`: SQLAlchemy async engine with `pool_pre_ping=True` and disabled statement cache on Postgres.
- `async_session_factory: async_sessionmaker[AsyncSession]`: Factory for non-expiring async sessions.
- `get_db() -> AsyncGenerator[AsyncSession, None]`: FastAPI dependency yielding an async session wrapped in atomic commit/rollback.
- `init_db() -> None`: Asynchronously creates all ORM tables declared in `Base.metadata`.
- `oauth2_scheme`: `OAuth2PasswordBearer(tokenUrl="/api/auth/login")`.
- `get_current_user`, `get_current_active_user`, `require_admin`, `require_roles`, `require_business_owner`: RBAC dependencies.

## Invariants
- Missing `SECRET_KEY` causes early startup termination.
- Database sessions yielded by `get_db` automatically commit on success and rollback on unhandled exceptions.
- `statement_cache_size` must be 0 for PostgreSQL to prevent asyncpg `DuplicatePreparedStatementError` on PgBouncer pooler.

## Side Effects
- Reads `.env` file from working directory.
- Connects to SQLite local database file or remote Supabase PostgreSQL pooler.

## Verification
- Run: `.venv/bin/pytest tests/test_auth.py`
