"""Pydantic settings loaded from environment variables / .env file."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Security ---
    secret_key: str
    google_client_id: str = "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com"

    # --- Database ---
    database_url: str | None = None  # Full URL override (default: sqlite in ./instance)

    # --- JWT ---
    algorithm: str = "HS256"

    # --- CORS ---
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:3000"]

    # --- Misc ---
    environment: str = "development"

    # --- Computed database URL ---
    @property
    def async_database_url(self) -> str:
        """Async-compatible database URL (aiosqlite for sqlite)."""
        url = self.database_url or self._build_sqlite_url()
        return url.replace("sqlite:///", "sqlite+aiosqlite:///")

    @property
    def sync_database_url(self) -> str:
        """Synchronous database URL."""
        return self.database_url or self._build_sqlite_url()

    def _build_sqlite_url(self) -> str:
        base = Path(__file__).resolve().parent.parent.parent.parent  # project root
        instance = base / "instance"
        instance.mkdir(exist_ok=True)
        return f"sqlite:///{instance / 'mangatarem.db'}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
