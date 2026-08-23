"""Pydantic settings — mirrors existing Flask config.py values."""
from __future__ import annotations

import os
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
    secret_key: str  # Required, same as Flask SECRET_KEY
    google_client_id: str = "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com"

    # --- Database ---
    db_provider: str = "sqlite"
    database_url: str | None = None  # Override full URL
    # Supabase / Postgres individual vars
    user: str = ""
    password: str = ""
    host: str = ""
    port: str = "5432"
    dbname: str = ""
    supabase_url: str = ""
    # MySQL
    db_user: str = ""
    db_pass: str = ""
    db_host: str = "localhost"
    db_port: str = "3306"
    db_name: str = ""

    # --- JWT ---
    access_token_expire_minutes: int = 30 * 24  # 7 days (matches Flask REMEMBER_COOKIE_DURATION)
    algorithm: str = "HS256"

    # --- CORS ---
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:3000"]

    # --- Redis ---
    redis_url: str = "redis://localhost:6379/0"
    redis_enabled: bool = True

    # --- Misc ---
    environment: str = "development"

    # --- Computed database URL ---
    @property
    def async_database_url(self) -> str:
        """Return an async-compatible database URL."""
        if self.database_url:
            url = self.database_url
        else:
            url = self._build_url()

        # Convert sync drivers to async equivalents
        url = url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
        url = url.replace("postgresql://", "postgresql+asyncpg://")
        url = url.replace("mysql+pymysql://", "mysql+aiomysql://")
        url = url.replace("sqlite:///", "sqlite+aiosqlite:///")
        return url

    @property
    def sync_database_url(self) -> str:
        """Return a synchronous database URL (for Alembic migrations, etc.)."""
        if self.database_url:
            return self.database_url
        return self._build_url()

    def _build_url(self) -> str:
        provider = self.db_provider.lower()

        if provider in ("supabase", "postgres", "postgresql"):
            return self._build_postgres_url()
        elif provider == "mysql":
            return self._build_mysql_url()
        else:
            return self._build_sqlite_url()

    def _build_postgres_url(self) -> str:
        from urllib.parse import quote_plus

        user = self.user
        password = quote_plus(self.password) if self.password else ""
        host = self.host
        port = self.port
        dbname = self.dbname

        if not all([user, host, dbname]):
            raise ValueError("DB credentials (user, host, dbname) are required for PostgreSQL.")

        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}?sslmode=require"

    def _build_mysql_url(self) -> str:
        if not all([self.db_user, self.db_host, self.db_name]):
            raise ValueError("DB_USER, DB_HOST, and DB_NAME are required for MySQL.")
        return f"mysql+pymysql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    def _build_sqlite_url(self) -> str:
        base = Path(__file__).resolve().parent.parent.parent.parent  # project root
        instance = base / "instance"
        instance.mkdir(exist_ok=True)
        db_path = instance / "mangatarem.db"
        return f"sqlite:///{db_path}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
