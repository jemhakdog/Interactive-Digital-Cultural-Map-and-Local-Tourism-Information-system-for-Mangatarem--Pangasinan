import os
import logging
from supabase import create_client, Client

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

    # Visible print for terminal output
    print("\n🚀 DATABASE CONFIGURATION:")
    print(f"   Provider: {provider.upper()}")
    print(f"   Status: {'READY' if provider != 'sqlite' else 'LOCAL (SQLite)'}")
    print("-" * 30 + "\n")
    if provider in ["supabase", "postgres", "postgresql"]:
        # Supabase/Postgres connection
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError(
                "DATABASE_URL env var is required for Supabase/Postgres. "
                "Format: postgresql://postgres:[PASSWORD]@[HOST]:[PORT]/postgres"
            )

        # SQLAlchemy requires 'postgresql://', but some providers give 'postgres://'
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        # Ensure we're using the synchronous internal driver if not specified
        if "postgresql://" in db_url and "+psycopg2" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

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
        is_vercel = os.getenv("VERCEL") or os.getenv("IS_VERCEL")

        if is_vercel:
            # Vercel has read-only filesystem - require external database
            raise ValueError(
                "SQLite is not supported on Vercel (read-only filesystem). "
                "Please set DATABASE_URL environment variable with a PostgreSQL/Supabase connection string, "
                "and optionally set DB_PROVIDER=supabase"
            )

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


def get_supabase_client() -> Client:
    """
    Initializes and returns a Supabase Python SDK client.
    Requires SUPABASE_URL and SUPABASE_KEY to be set in environment.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        logger.warning("SUPABASE_URL or SUPABASE_KEY not found in environment.")
        return None

    try:
        return create_client(url, key)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        return None
