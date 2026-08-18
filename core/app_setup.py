import os
import logging
from flask import Flask, render_template, request, send_from_directory
from extensions import db, csrf

logger = logging.getLogger(__name__)

def init_supabase_support(app: Flask) -> None:
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


def init_redis_support(app: Flask) -> None:
    """Adds global Redis client to the app instance."""
    redis_url = os.environ.get("UPSTASH_REDIS_REST_URL")
    redis_token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")

    if not redis_url or not redis_token:
        logger.warning("Redis credentials not found, caching disabled")
        app.redis_client = None
        return

    try:
        from upstash_redis import Client
        app.redis_client = Client(url=redis_url, token=redis_token)
        logger.info("Global Redis client initialized")
    except ImportError:
        logger.warning("upstash-redis not installed, caching disabled")
        app.redis_client = None
    except Exception as e:
        logger.error(f"Failed to initialize global Redis client: {e}")
        app.redis_client = None


def register_error_handlers(app: Flask) -> None:
    """Register custom error page handlers with sanitized error messages."""
    error_codes = [400, 401, 403, 404, 408, 429, 451, 500]

    def handle_error(e):
        code = getattr(e, 'code', 500)
        
        # Log detailed error server-side for debugging
        if code >= 500:
            logger.error(f"Server error {code}: {str(e)}", exc_info=True)
        
        # Sanitize error message - never expose internal details to users
        # In production, return generic messages
        is_prod = app.config.get("FLASK_ENV") == "production"
        
        return render_template(
            f"errors/{code}.html",
            error_message="An unexpected error occurred" if code >= 500 and is_prod else str(e)
        ), code

    for code in error_codes:
        app.errorhandler(code)(handle_error)
    
    # Catch-all handler for unhandled exceptions
    @app.errorhandler(Exception)
    def handle_uncaught_exception(e):
        # Log the full exception server-side
        logger.critical(f"Uncaught exception: {str(e)}", exc_info=True)
        
        # Return generic 500 error to user
        if app.config.get("FLASK_ENV") == "production":
            return render_template("errors/500.html", error_message="An unexpected error occurred"), 500
        else:
            # In development, show the actual error for debugging
            raise e


def register_context_processors(app: Flask) -> None:
    """Register variables available in all templates."""
    @app.context_processor
    def inject_utilities():
        from datetime import datetime
        from flask_login import current_user
        
        unread_notifications_count = 0
        latest_notifications = []
        
        if current_user and current_user.is_authenticated:
            try:
                from modules.notifications.models import UserNotification
                unread_notifications_count = UserNotification.query.filter_by(
                    user_id=current_user.id, is_read=False
                ).count()
                latest_notifications = UserNotification.query.filter_by(
                    user_id=current_user.id
                ).order_by(UserNotification.created_at.desc()).limit(5).all()
            except Exception:
                pass
                
        return dict(
            config=app.config,
            mapbox_token=os.environ.get("mapbox_token") or os.environ.get("MAPBOX_TOKEN", ""),
            now=datetime.utcnow,
            unread_notifications_count=unread_notifications_count,
            latest_notifications=latest_notifications
        )


def _apply_cache_headers(response, path: str) -> None:
    """Applies Vercel Edge Cache headers based on path and type."""
    no_cache_prefixes = ("/admin", "/auth", "/user", "/barangay-admin")
    if path in ("/sw.js", "/manifest.json", "/offline") or any(path.startswith(p) for p in no_cache_prefixes):
        response.headers["Cache-Control"] = "private, no-store, no-cache, must-revalidate, max-age=0"
    elif "text/html" in response.content_type:
        # Disable cache for HTML temporarily to force CSP update
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0"
    elif any(path.endswith(ext) for ext in (".js", ".css", ".png", ".jpg", ".webp", ".woff2")):
        # Immutable assets (1 year)
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    else:
        # Default API/Other responses
        response.headers["Cache-Control"] = "public, max-age=30, s-maxage=300, stale-while-revalidate=600"


def register_request_hooks(app: Flask) -> None:
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

        # === Security Headers ===
        csp_policies = {
            "default-src": "'self'",
            "script-src": "'self' https://fonts.googleapis.com https://maps.mapbox.com https://api.mapbox.com https://accounts.google.com https://unpkg.com https://cdn.jsdelivr.net https://*.jsdelivr.net https://vercel.live https://*.vercel.live 'unsafe-inline' 'unsafe-eval'",
            "style-src": "'self' https://fonts.googleapis.com https://api.mapbox.com https://unpkg.com https://cdn.jsdelivr.net https://*.jsdelivr.net https://vercel.live https://accounts.google.com 'unsafe-inline'",
            "img-src": "'self' data: https: blob: https://vercel.com https://*.vercel.com https://*.basemaps.cartocdn.com https://*.arcgisonline.com",
            "font-src": "'self' https://fonts.gstatic.com data:",
            "connect-src": "'self' https://router.project-osrm.org https://*.basemaps.cartocdn.com https://unpkg.com https://cdn.jsdelivr.net https://*.jsdelivr.net https://fonts.googleapis.com https://fonts.gstatic.com https://placehold.co https://*.mapbox.com https://api.mapbox.com https://events.mapbox.com https://*.supabase.co https://*.upstash.io https://accounts.google.com https://vercel.live https://*.vercel.live wss://*.vercel.live https://*.arcgisonline.com ws://127.0.0.1:5002 ws://localhost:5002 wss://*",
            "worker-src": "'self' blob:",
            "frame-src": "https://accounts.google.com https://*.google.com https://*.googleusercontent.com",
            "frame-ancestors": "'none'",
            "base-uri": "'self'",
            "form-action": "'self'",
            "object-src": "'none'",
            "upgrade-insecure-requests": ""
        }
        csp_string = "; ".join([f"{k} {v}".strip() for k, v in csp_policies.items()])
        response.headers["Content-Security-Policy"] = csp_string

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy (restrict browser features)
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(self), geolocation=(self), payment=()"
        )

        # Cross-Origin protection (only meaningful with HTTPS)
        # Skip COOP/CORP on auth pages — Google GSI needs cross-origin postMessage with accounts.google.com
        is_auth_page = request.path.startswith("/auth/")
        if app.config.get("SESSION_COOKIE_SECURE") and not is_auth_page:
            response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
            response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        # HSTS for production (only if SESSION_COOKIE_SECURE is enabled)
        if app.config.get("SESSION_COOKIE_SECURE"):
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        # Smart Cache-Control logic
        is_vercel = "VERCEL" in os.environ
        if is_vercel and request.method == "GET" and response.status_code == 200:
            _apply_cache_headers(response, request.path)
            
            # PERFORMANCE: Drop session cookie for anonymous home page visits.
            # This ensures Vercel Edge Cache covers the home page for all guests.
            from flask_login import current_user
            if request.path == "/" and current_user.is_anonymous:
                if 'Set-Cookie' in response.headers:
                    del response.headers['Set-Cookie']

        return response


def register_utility_routes(app: Flask) -> None:
    """Register static utility routes (service worker, manifest)."""
    @app.route('/sw.js')
    def serve_sw():
        return send_from_directory(app.static_folder, 'sw.js', mimetype='application/javascript')

    @csrf.exempt
    @app.route('/manifest.json')
    def serve_manifest():
        return send_from_directory(app.static_folder, 'manifest.json', mimetype='application/json')

    @app.route('/offline')
    def serve_offline():
        return render_template('offline.html')


def seed_database(app):
    try:
        _execute_seeding(app)
    except Exception as e:
        logger.warning(f"Database seeding bypassed: {e}")

def _execute_seeding(app):
    """Seed initial data if needed."""
    from models import Attraction, User, BarangayInfo
    import json
    
    if Attraction.query.first() is None:
        data_path = os.path.join(app.root_path, "data", "attractions.json")
        if os.path.exists(data_path):
            with open(data_path, "r") as f:
                data = json.load(f)
                i = 0
                for item in data:
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
                        status="approved",
                        is_featured=(i < 3)
                    ))
                i += 1
            db.session.commit()
            logger.info("Database seeded with sample attractions.")

    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", email="admin@example.com", role="admin", is_approved=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        logger.info("Default admin user created.")

    if not User.query.filter_by(username="test_owner").first():
        test_owner = User(username="test_owner", email="test_owner@example.com", role="business_owner", is_approved=True)
        test_owner.set_password("owner123")
        db.session.add(test_owner)
        db.session.commit()
        logger.info("Default test_owner user created.")

    if not User.query.filter_by(username="tourist").first():
        tourist = User(username="tourist", email="tourist@example.com", role="user", is_approved=True)
        tourist.set_password("tourist123")
        db.session.add(tourist)
        db.session.commit()
        logger.info("Default tourist user created.")

    from models import Establishment, EstablishmentRoom, EstablishmentMenuItem
    if Establishment.query.first() is None:
        dining_owner = User.query.filter_by(username="dining_owner").first()
        if not dining_owner:
            dining_owner = User(
                username="dining_owner",
                email="dining@example.com",
                role="business_owner",
                is_approved=True,
            )
            dining_owner.set_password("dining123")
            db.session.add(dining_owner)

        hospitality_owner = User.query.filter_by(username="hospitality_owner").first()
        if not hospitality_owner:
            hospitality_owner = User(
                username="hospitality_owner",
                email="hospitality@example.com",
                role="business_owner",
                is_approved=True,
            )
            hospitality_owner.set_password("hospitality123")
            db.session.add(hospitality_owner)
        
        db.session.flush()

        est_path = os.path.join(app.root_path, "data", "establishments.json")
        if os.path.exists(est_path):
            with open(est_path, "r", encoding="utf-8") as f:
                est_data = json.load(f)
            i = 0
            for item in est_data:
                current_owner_id = hospitality_owner.id if item["type"] == "inn" else dining_owner.id
                
                est = Establishment(
                    owner_id=current_owner_id,
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
                    is_featured=(i < 2)
                )
                db.session.add(est)
                i += 1
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
            logger.info("Database seeded with specialized owner establishments.")
