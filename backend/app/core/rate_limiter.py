"""Rate limiter configuration using slowapi."""
from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# In-memory storage for dev; use Redis in production
# limiter = Limiter(key_func=get_remote_address, storage_uri="redis://localhost:6379/0")
limiter = Limiter(key_func=get_remote_address)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Custom handler for rate limit exceeded."""
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded",
            "message": str(exc.detail),
            "retry_after": getattr(exc, "retry_after", None),
        },
    )


# Rate limit tiers (for documentation)
RATE_LIMITS = {
    "default": "100/minute",
    "auth": "10/minute",
    "search": "30/minute",
    "uploads": "20/minute",
    "admin": "200/minute",
    "public": "100/minute",
}
