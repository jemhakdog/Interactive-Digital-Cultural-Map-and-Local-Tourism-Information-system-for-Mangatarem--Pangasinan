"""
Main application entry with clean function design.

Separates seeding concerns: attractions, admin, contributor.
Each function does one thing and returns meaningful values.
"""

import os
import logging

from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from extensions import limiter
from models import db
from routes import register_blueprints
from utils.db_manager import get_database_uri, get_db_config, get_supabase_client
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Named constants for session / cookie lifetimes (in seconds)
SESSION_LIFETIME_SECONDS = 86400 * 7   # 7 days
REMEMBER_COOKIE_SECONDS = 86400 * 30   # 30 days

# Load environment variables
load_dotenv()

# Determine if running on Vercel
IS_VERCEL = "VERCEL" in os.environ

# Determine absolute paths
if IS_VERCEL:
    BASE_DIR = "/var/task"
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

template_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Apply ProxyFix for Vercel/Production
if IS_VERCEL:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your-secret-key-here")
app.config["UPLOAD_FOLDER"] = os.path.join(static_dir, "uploads")
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4"}

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
get_db_config(app)

# Server & Session configuration
app.config["SERVER_NAME"] = None
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = SESSION_LIFETIME_SECONDS
app.config["REMEMBER_COOKIE_DURATION"] = REMEMBER_COOKIE_SECONDS

if IS_VERCEL:
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
else:
    app.config["SESSION_COOKIE_SECURE"] = False
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_DOMAIN"] = None

app.config["PREFERRED_URL_SCHEME"] = os.environ.get(
    "PREFERRED_URL_SCHEME", "https" if IS_VERCEL else "http"
)

# Initialize database
db.init_app(app)

# Flask-Migrate: only needed for local development
if not IS_VERCEL:
    from flask_migrate import Migrate
    migrate = Migrate(app, db)

# Rate limiter
limiter.init_app(app)

# Login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "error"
login_manager.init_app(app)

# Supabase client: lazy-loaded on first access to avoid cold start penalty
_supabase_client = None


def _get_lazy_supabase():
    """Return Supabase client, initializing on first call."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = get_supabase_client()
    return _supabase_client


class _LazySupabase:
    """Descriptor that lazy-loads the Supabase client on first access."""
    def __get__(self, obj, objtype=None):
        return _get_lazy_supabase()


app.__class__.supabase = _LazySupabase()


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    from models import User
    return User.query.get(int(user_id))


def _seed_attractions_from_json(data_path: str) -> int:
    """
    Seed attractions from JSON file if database is empty.
    
    Args:
        data_path: Path to attractions.json
        
    Returns:
        Number of attractions seeded
    """
    from models import Attraction
    import json
    
    if Attraction.query.first() is not None:
        return 0
    
    if not os.path.exists(data_path):
        return 0
    
    with open(data_path, "r") as f:
        data = json.load(f)
        for item in data:
            attraction = Attraction(
                name=item["name"],
                category=item["category"],
                barangay=item.get("barangay"),
                description=item["description"],
                lat=item["lat"],
                lng=item["lng"],
                image_url=item["image"],
                status="approved",
            )
            db.session.add(attraction)
    
    db.session.commit()
    return len(data)


def _create_default_admin() -> bool:
    """
    Create default admin account if not exists.
    
    Returns:
        True if created, False if already exists
    """
    from models import User
    
    if User.query.filter_by(username="admin").first() is not None:
        return False
    
    admin = User(
        username="admin",
        email="admin@example.com",
        role="admin",
        is_approved=True
    )
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    return True


def _create_default_contributor(barangay: str = "Poblacion") -> bool:
    """
    Create default contributor account if not exists.
    
    Args:
        barangay: Barangay name for contributor
        
    Returns:
        True if created, False if already exists
    """
    from models import User
    
    if User.query.filter_by(username="barangay").first() is not None:
        return False
    
    contributor = User(
        username="barangay",
        email="barangay@example.com",
        role="contributor",
        barangay=barangay,
        is_approved=True,
    )
    contributor.set_password("barangay123")
    db.session.add(contributor)
    db.session.commit()
    return True


def seed_database() -> None:
    """
    Orchestrate database seeding (attractions, admin, contributor).
    
    Delegates to focused helper functions for each seeding task.
    """
    data_path = os.path.join(BASE_DIR, "data", "attractions.json")
    
    attractions_count = _seed_attractions_from_json(data_path)
    if attractions_count > 0:
        logger.info("Database seeded with %d attractions.", attractions_count)

    if _create_default_admin():
        logger.info("Default admin created.")

    if _create_default_contributor():
        logger.info("Default contributor created.")


def _run_auto_migrations():
    """
    Add missing columns to Supabase tables automatically.
    Uses IF NOT EXISTS-style checks so it's safe to run repeatedly.
    """
    from sqlalchemy import text, inspect

    inspector = inspect(db.engine)
    migrations = {
        "attraction": [
            ("reviewed_by", 'ALTER TABLE attraction ADD COLUMN reviewed_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL'),
            ("reviewed_at", "ALTER TABLE attraction ADD COLUMN reviewed_at TIMESTAMP"),
        ],
        "event": [
            ("reviewed_by", 'ALTER TABLE event ADD COLUMN reviewed_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL'),
            ("reviewed_at", "ALTER TABLE event ADD COLUMN reviewed_at TIMESTAMP"),
        ],
        "gallery_item": [
            ("reviewed_by", 'ALTER TABLE gallery_item ADD COLUMN reviewed_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL'),
            ("reviewed_at", "ALTER TABLE gallery_item ADD COLUMN reviewed_at TIMESTAMP"),
        ],
        "review": [
            ("reviewed_by", 'ALTER TABLE review ADD COLUMN reviewed_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL'),
            ("reviewed_at", "ALTER TABLE review ADD COLUMN reviewed_at TIMESTAMP"),
        ],
    }

    for table_name, columns in migrations.items():
        existing = [col["name"] for col in inspector.get_columns(table_name)]
        for col_name, alter_sql in columns:
            if col_name not in existing:
                try:
                    db.session.execute(text(alter_sql))
                    db.session.commit()
                    logger.info("[migrate] Added column %s.%s", table_name, col_name)
                except Exception as e:
                    db.session.rollback()
                    logger.warning("[migrate] Skipped %s.%s: %s", table_name, col_name, e)


# Database initialization and seeding
with app.app_context():
    if not IS_VERCEL:
        db.create_all()
        seed_database()
    # Auto-migrations removed from cold start for performance.
    # Use /admin/run-migrations to run manually when needed.


@app.context_processor
def inject_config():
    """Make config available in all templates."""
    return dict(
        config=app.config,
        mapbox_token=os.environ.get("mapbox_token", "")
    )


@app.before_request
def make_session_permanent():
    """Make all sessions permanent to persist across browser restarts."""
    from flask import session
    session.permanent = True


# Register blueprints
register_blueprints(app)


@app.route('/sw.js')
def serve_sw():
    """Serve service worker."""
    from flask import send_from_directory
    return send_from_directory(static_dir, 'sw.js', mimetype='application/javascript')


@app.route('/manifest.json')
def serve_manifest():
    """Serve PWA manifest."""
    from flask import send_from_directory
    return send_from_directory(static_dir, 'manifest.json', mimetype='application/json')


@app.after_request
def add_headers(response):
    """Add security and caching headers to all responses."""
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"

    # Smart Cache-Control for Vercel Edge Network
    if IS_VERCEL and request.method == "GET" and response.status_code == 200:
        # Skip caching for authenticated/admin/auth routes
        path = request.path
        no_cache_prefixes = ("/admin", "/auth", "/user", "/barangay-admin")
        if any(path.startswith(p) for p in no_cache_prefixes):
            response.headers["Cache-Control"] = "private, no-store"
        elif "text/html" in response.content_type:
            # HTML pages: short browser cache, longer edge cache
            response.headers["Cache-Control"] = (
                "public, max-age=60, s-maxage=300, stale-while-revalidate=600"
            )
        elif any(path.endswith(ext) for ext in (".js", ".css", ".png", ".jpg", ".webp", ".woff2")):
            # Static assets: long cache with immutable
            response.headers["Cache-Control"] = (
                "public, max-age=31536000, immutable"
            )
        else:
            # API/JSON responses: moderate edge cache
            response.headers["Cache-Control"] = (
                "public, max-age=30, s-maxage=120, stale-while-revalidate=300"
            )

    return response


# Error handlers
@app.errorhandler(400)
def bad_request(e):
    """Handle 400 Bad Request errors."""
    return render_template("errors/400.html"), 400


@app.errorhandler(401)
def unauthorized(e):
    """Handle 401 Unauthorized errors."""
    return render_template("errors/401.html"), 401


@app.errorhandler(403)
def forbidden(e):
    """Handle 403 Forbidden errors."""
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 Not Found errors."""
    return render_template("errors/404.html"), 404


@app.errorhandler(408)
def request_timeout(e):
    """Handle 408 Request Timeout errors."""
    return render_template("errors/408.html"), 408


@app.errorhandler(429)
def too_many_requests(e):
    """Handle 429 Too Many Requests errors."""
    return render_template("errors/429.html"), 429


@app.errorhandler(451)
def legal_reasons(e):
    """Handle 451 Unavailable For Legal Reasons errors."""
    return render_template("errors/451.html"), 451


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000

    if not IS_VERCEL:
        logger.info("Starting in local development mode on http://%s:%d", host, port)

    app.run(host=host, port=port, debug=True)
