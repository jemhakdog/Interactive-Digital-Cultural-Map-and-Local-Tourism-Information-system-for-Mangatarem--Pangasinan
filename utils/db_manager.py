import os
import logging

# Configure logging
logger = logging.getLogger(__name__)


def get_database_uri():
    """
    Returns the appropriate SQLAlchemy database URI based on the
    DB_PROVIDER environment variable.

    Supported Providers:
    - 'supabase' (or 'postgres')
    - 'mysql'
    - 'sqlite' (default)
    """
    provider = os.getenv("DB_PROVIDER", "sqlite").lower()

    # Check if we are on Vercel and DATABASE_URL is set - default to supabase if so
    if os.getenv("VERCEL") and os.getenv("DATABASE_URL") and provider == "sqlite":
        provider = "supabase"

    logger.info(f"Configuring database for provider: {provider}")

    if provider in ["supabase", "postgres", "postgresql"]:
        # Supabase/Postgres connection
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL env var is required for Supabase/Postgres")

        # SQLAlchemy requires 'postgresql://', but some providers give 'postgres://'
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        return db_url

    elif provider == "mysql":
        # MySQL connection (requires pymysql driver)
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME")

        if not all([user, host, db_name]):
            raise ValueError("DB_USER, DB_HOST, and DB_NAME are required for MySQL")

        return f"mysql+pymysql://{user}:{password if password else ''}@{host}:{port}/{db_name}"

    elif provider in ["xampp", "laragon"]:
        # XAMPP/Laragon standard local MySQL settings
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASS", "")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "mangatarem")

        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

    else:
        # Default to SQLite (Local Development)
        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        instance_path = os.path.join(base_dir, "instance")
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)

        db_path = os.path.join(instance_path, "mangatarem.db")
        return f"sqlite:///{db_path}"


def get_db_config(app):
    """
    Applies database-specific configuration settings to the Flask app.
    """
    provider = os.getenv("DB_PROVIDER", "sqlite").lower()

    # Check if we are on Vercel and DATABASE_URL is set
    if os.getenv("VERCEL") and os.getenv("DATABASE_URL") and provider == "sqlite":
        provider = "supabase"

    # Common Config
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if provider in ["supabase", "postgres", "mysql", "xampp", "laragon"]:
        # Production-grade settings
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_pre_ping": True,  # Handles disconnected connections gracefully
            "pool_recycle": 300,  # Recycle connections every 5 minutes
            "pool_size": 10,  # Connection pool size
            "max_overflow": 20,
        }
    else:
        # SQLite settings (Low overhead for local)
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}

    return app
