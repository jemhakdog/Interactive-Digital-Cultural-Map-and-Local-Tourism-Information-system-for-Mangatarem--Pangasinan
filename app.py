"""
Application Factory implementation.

Modularizes application creation and configuration to improve testability
and clarify dependency management.
"""

import os
import sys
import logging
from flask import Flask, render_template, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db, login_manager, limiter
from config import config_by_name
from routes import register_blueprints
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

# Configure root logger so all info/debug messages print to console
logging.basicConfig(
    level=logging.DEBUG if os.environ.get("FLASK_ENV") != "production" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """
    Application factory to create and configure the Flask app.
    
    Args:
        config_name: Configuration key ('development', 'production', 'testing')
        
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    
    # Determine absolute paths for template/static folders
    is_vercel = "VERCEL" in os.environ
    if is_vercel:
        base_dir = "/var/task"
    elif getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
    )
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Apply ProxyFix for Production/Vercel
    if is_vercel:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    if not is_vercel:
        from flask_migrate import Migrate
        Migrate(app, db)

    # Register Blueprints
    register_blueprints(app)
    
    # Initialize Lazy-loaded Supabase support
    _init_supabase_support(app)
    
    # Register core application hooks and handlers
    _register_error_handlers(app)
    _register_context_processors(app)
    _register_request_hooks(app)
    _register_utility_routes(app)
    
    # Database initialization/seeding (Local only)
    with app.app_context():
        if not is_vercel:
            db.create_all()
            _seed_database(app)

    return app


def _init_supabase_support(app: Flask) -> None:
    """Adds lazy-loaded Supabase client to the app instance."""
    from utils.db_manager import get_supabase_client
    
    _supabase_client = None

    def get_lazy_supabase():
        nonlocal _supabase_client
        if _supabase_client is None:
            _supabase_client = get_supabase_client()
        return _supabase_client

    class LazySupabase:
        def __get__(self, obj, objtype=None):
            return get_lazy_supabase()

    app.__class__.supabase = LazySupabase()


def _register_error_handlers(app: Flask) -> None:
    """Register custom error page handlers."""
    error_codes = [400, 401, 403, 404, 408, 429, 451, 500]
    
    def handle_error(e):
        code = getattr(e, 'code', 500)
        return render_template(f"errors/{code}.html"), code

    for code in error_codes:
        app.errorhandler(code)(handle_error)


def _register_context_processors(app: Flask) -> None:
    """Register variables available in all templates."""
    @app.context_processor
    def inject_config():
        return dict(
            config=app.config,
            mapbox_token=os.environ.get("mapbox_token", "")
        )


def _register_request_hooks(app: Flask) -> None:
    """Register before/after request processing hooks."""
    request_logger = logging.getLogger("request")

    @app.before_request
    def make_session_permanent():
        from flask import session
        session.permanent = True

    @app.after_request
    def log_and_add_headers(response):
        # Log every user action (skip static files to reduce noise)
        if not request.path.startswith("/static"):
            from flask_login import current_user
            user_info = (
                f"user={current_user.username}(id={current_user.id})"
                if hasattr(current_user, "username") and current_user.is_authenticated
                else "user=anonymous"
            )
            request_logger.info(
                "%s %s %s -> %s",
                request.method,
                request.path,
                user_info,
                response.status_code,
            )

        response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
        
        # Smart Cache-Control logic
        is_vercel = "VERCEL" in os.environ
        if is_vercel and request.method == "GET" and response.status_code == 200:
            _apply_cache_headers(response, request.path)
            
        return response


def _apply_cache_headers(response, path: str) -> None:
    """Applies Vercel Edge Cache headers based on path and type."""
    no_cache_prefixes = ("/admin", "/auth", "/user", "/barangay-admin")
    if any(path.startswith(p) for p in no_cache_prefixes):
        response.headers["Cache-Control"] = "private, no-store"
    elif "text/html" in response.content_type:
        response.headers["Cache-Control"] = "public, max-age=60, s-maxage=300, stale-while-revalidate=600"
    elif any(path.endswith(ext) for ext in (".js", ".css", ".png", ".jpg", ".webp", ".woff2")):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    else:
        response.headers["Cache-Control"] = "public, max-age=30, s-maxage=120, stale-while-revalidate=300"


def _register_utility_routes(app: Flask) -> None:
    """Register static utility routes (service worker, manifest)."""
    @app.route('/sw.js')
    def serve_sw():
        return send_from_directory(app.static_folder, 'sw.js', mimetype='application/javascript')

    @app.route('/manifest.json')
    def serve_manifest():
        return send_from_directory(app.static_folder, 'manifest.json', mimetype='application/json')


def _seed_database(app):
    """Seed initial data if needed."""
    from models import Attraction, User, BarangayInfo
    import json
    
    if Attraction.query.first() is not None:
        return

    data_path = os.path.join(app.root_path, "data", "attractions.json")
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            data = json.load(f)
            for item in data:
                # Handle barangay relationship
                barangay_name = item.get("barangay")
                brgy = None
                if barangay_name:
                    brgy = BarangayInfo.query.filter_by(name=barangay_name).first()
                    if not brgy:
                        brgy = BarangayInfo(name=barangay_name)
                        db.session.add(brgy)
                        db.session.flush()

                db.session.add(Attraction(
                    name=item["name"], category=item["category"],
                    barangay=brgy, description=item["description"],
                    latitude=item["lat"], longitude=item["lng"], 
                    image_url=item["image"],
                    status="approved"
                ))
        db.session.commit()
        logger.info("Database seeded with sample attractions.")

    # Create default admin
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", email="admin@example.com", role="admin", is_approved=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        logger.info("Default admin user created.")

    # Seed establishments
    from models import Establishment, EstablishmentRoom, EstablishmentMenuItem
    if Establishment.query.first() is None:
        # Create a demo business owner
        biz_user = User.query.filter_by(username="business_demo").first()
        if not biz_user:
            biz_user = User(
                username="business_demo",
                email="business@example.com",
                role="business_owner",
                is_approved=True,
            )
            biz_user.set_password("business123")
            db.session.add(biz_user)
            db.session.flush()

        est_path = os.path.join(app.root_path, "data", "establishments.json")
        if os.path.exists(est_path):
            with open(est_path, "r", encoding="utf-8") as f:
                est_data = json.load(f)
            for item in est_data:
                est = Establishment(
                    owner_id=biz_user.id,
                    name=item["name"],
                    type=item["type"],
                    description=item.get("description", ""),
                    address=item.get("address", ""),
                    latitude=item.get("latitude", 0),
                    longitude=item.get("longitude", 0),
                    contact_number=item.get("contact_number"),
                    price_range=item.get("price_range"),
                    amenities=item.get("amenities", []),
                    operating_hours=item.get("operating_hours", {}),
                    status="approved",
                )
                db.session.add(est)
                db.session.flush()

                for room in item.get("rooms", []):
                    db.session.add(EstablishmentRoom(
                        establishment_id=est.id,
                        name=room["name"],
                        description=room.get("description", ""),
                        price_per_night=room.get("price_per_night"),
                        capacity=room.get("capacity", 2),
                        amenities=room.get("amenities", []),
                    ))

                for mi in item.get("menu_items", []):
                    db.session.add(EstablishmentMenuItem(
                        establishment_id=est.id,
                        name=mi["name"],
                        description=mi.get("description", ""),
                        price=mi.get("price"),
                        category=mi.get("category", "main"),
                        is_bestseller=mi.get("is_bestseller", False),
                    ))

            db.session.commit()
            logger.info("Database seeded with sample establishments.")


# Entry point for Vercel and local running
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
