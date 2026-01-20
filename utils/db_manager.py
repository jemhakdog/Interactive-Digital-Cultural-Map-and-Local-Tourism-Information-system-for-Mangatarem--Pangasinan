import os
import logging
import re
from urllib.parse import quote_plus
from sqlalchemy.pool import NullPool
from supabase import create_client, Client

# Configure logging
logger = logging.getLogger(__name__)


def _encode_password_in_url(db_url: str) -> str:
    """
    Properly URL-encodes the password in a database connection URL.
    Handles special characters like @, #, !, etc.
    """
    # Pattern to match: scheme://user:password@host:port/database
    # We need to extract and encode only the password portion
    pattern = r"^(postgresql(?:\+psycopg2)?|postgres|mysql(?:\+pymysql)?):\/\/([^:]+):(.+)@(.+)$"
    match = re.match(pattern, db_url)

    if match:
        scheme = match.group(1)
        user = match.group(2)
        password = match.group(3)
        host_and_db = match.group(4)

        # URL-encode the password
        encoded_password = quote_plus(password)

        return f"{scheme}://{user}:{encoded_password}@{host_and_db}"

    # If pattern doesn't match, return original URL
    return db_url


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
        # Try individual environment variables first
        user = os.getenv("user")
        password = os.getenv("password")
        host = os.getenv("host")
        port = os.getenv("port", "5432")
        dbname = os.getenv("dbname")

        # Automatic Transaction Pooler switch for Vercel + Supabase
        if os.getenv("VERCEL") and host and "supabase.com" in host and port == "5432":
            logger.info(
                "Auto-switching to Supabase Transaction Pooler (Port 6543) for Vercel"
            )
            port = "6543"

        if all([user, host, dbname]):
            if password:
                password = quote_plus(password)

            db_url = f"postgresql+psycopg2://{user}:{password if password else ''}@{host}:{port}/{dbname}?sslmode=require"

            # Add pgbouncer flag if using the pooler port
            if port == "6543":
                db_url += "&pgbouncer=true"

            logger.info(f"Constructed URI from components (Port: {port})")
            return db_url

        # Fallback to DATABASE_URL env var
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError(
                "DATABASE_URL or individual DB vars (user, host, dbname) are required."
            )

        # SQLAlchemy standardizations
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        if "postgresql://" in db_url and "+psycopg2" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

        # Ensure Vercel uses the transaction pooler if possible
        if os.getenv("VERCEL") and ":5432" in db_url and "supabase.co" in db_url:
            logger.info(
                "Updating DATABASE_URL to use Supabase Transaction Pooler (Port 6543)"
            )
            db_url = db_url.replace(":5432", ":6543")
            if "pgbouncer=true" not in db_url:
                separator = "&" if "?" in db_url else "?"
                db_url += f"{separator}pgbouncer=true"

        db_url = _encode_password_in_url(db_url)
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
        is_serverless = os.getenv("VERCEL") or os.getenv("IS_VERCEL")

        if is_serverless:
            # Serverless environments (Vercel) shouldn't use traditional pooling
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
                "poolclass": NullPool,
                # Connect timeout is crucial for cold starts
                "connect_args": {
                    "connect_timeout": 10,
                },
            }
        else:
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
                "pool_pre_ping": True,
                "pool_recycle": 1800,  # Increased recycle time for non-serverless
                "pool_size": 15,
                "max_overflow": 25,
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
