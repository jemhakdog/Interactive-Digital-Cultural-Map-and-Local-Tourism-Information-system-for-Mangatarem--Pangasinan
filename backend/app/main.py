"""FastAPI application entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.app.core.config import get_settings
from backend.app.core.database import init_db
from backend.app.core.rate_limiter import limiter

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    # Create tables on first run (replace with Alembic for prod)
    if settings.environment == "development":
        await init_db()
    yield


app = FastAPI(
    title="Mangatarem Tourism System API",
    description="FastAPI backend for the Mangatarem tourism platform",
    version="1.0.0",
    lifespan=lifespan,
)

# --- Rate Limiter ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Health check ---
@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "name": "Mangatarem Tourism System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# --- Register routers ---
from backend.app.api.auth import router as auth_router  # noqa: E402
from backend.app.api.public import router as public_router  # noqa: E402
from backend.app.api.attractions import router as attractions_router  # noqa: E402
from backend.app.api.events import router as events_router  # noqa: E402
from backend.app.api.business import router as business_router  # noqa: E402
from backend.app.api.booking import router as booking_router  # noqa: E402
from backend.app.api.chat import router as chat_router  # noqa: E402
from backend.app.api.gallery import router as gallery_router  # noqa: E402
from backend.app.api.heritage import router as heritage_router  # noqa: E402
from backend.app.api.gamification import router as gamification_router  # noqa: E402
from backend.app.api.notifications import router as notifications_router  # noqa: E402
from backend.app.api.analytics import router as analytics_router  # noqa: E402
from backend.app.api.uploads import router as uploads_router  # noqa: E402
from backend.app.api.admin import router as admin_router  # noqa: E402

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(public_router, prefix="/api", tags=["public"])
app.include_router(attractions_router, prefix="/api/attractions", tags=["attractions"])
app.include_router(events_router, prefix="/api/events", tags=["events"])
app.include_router(business_router, prefix="/api/business", tags=["business"])
app.include_router(booking_router, prefix="/api/booking", tags=["booking"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(gallery_router, prefix="/api/gallery", tags=["gallery"])
app.include_router(heritage_router, prefix="/api/heritage", tags=["heritage"])
app.include_router(gamification_router, prefix="/api/gamification", tags=["gamification"])
app.include_router(notifications_router, prefix="/api/notifications", tags=["notifications"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["analytics"])
app.include_router(uploads_router, prefix="/api/uploads", tags=["uploads"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

# Serve uploaded files in development
from fastapi.staticfiles import StaticFiles
from pathlib import Path

_uploads_dir = Path(__file__).resolve().parent.parent / "uploads"
_uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_uploads_dir)), name="uploads")
