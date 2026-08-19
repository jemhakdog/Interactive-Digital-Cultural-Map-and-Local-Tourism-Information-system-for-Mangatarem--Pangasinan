"""Async SQLAlchemy engine and session factory."""
from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.core.config import get_settings
from backend.app.models.base import Base

settings = get_settings()

engine = create_async_engine(
    settings.async_database_url,
    echo=(settings.environment == "development"),
    pool_pre_ping=True,
    # aiosqlite doesn't support pool_size; only set for real databases
    **(
        {"pool_size": 15, "max_overflow": 25, "pool_recycle": 1800}
        if "sqlite" not in settings.async_database_url
        else {}
    ),
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields an async DB session, auto-closes."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Create all tables (dev convenience — use Alembic in production)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
