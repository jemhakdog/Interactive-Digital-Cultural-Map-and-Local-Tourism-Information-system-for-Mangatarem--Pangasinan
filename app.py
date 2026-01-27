import os
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from extensions import limiter
from flask_migrate import Migrate

from models import db
from routes import register_blueprints
from utils.db_manager import get_database_uri, get_db_config, get_supabase_client
from dotenv import load_dotenv
# Load environment variables from .ENV file
load_dotenv()

# Determine if we are running on Vercel
IS_VERCEL = "VERCEL" in os.environ
print("IS_VERCEL: ", IS_VERCEL)

# Determine absolute paths for templates and static folders
# On Vercel, the code is deployed to /var/task/
if IS_VERCEL:
    BASE_DIR = "/var/task"
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

template_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")
print("template_dir: ", template_dir)
print("static_dir: ", static_dir)
print("BASE_DIR: ", BASE_DIR)
# Debug: Print paths for troubleshooting
print(f"BASE_DIR: {BASE_DIR}")
print(f"template_dir: {template_dir}")
print(f"template_dir exists: {os.path.exists(template_dir)}")
if os.path.exists(template_dir):
    print(f"template_dir contents: {os.listdir(template_dir)}")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Apply ProxyFix for Vercel/Production environments
if IS_VERCEL:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your-secret-key-here")
app.config["UPLOAD_FOLDER"] = os.path.join(static_dir, "uploads")
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4"}

# Database Configuration via db_manager (supports SQLite, MySQL, Supabase/PostgreSQL)
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
get_db_config(app)  # Applies engine options & TRACK_MODIFICATIONS

# Server & Session Configuration
# We avoid setting SERVER_NAME globally as it can interfere with cookie domains.
# Flask will dynamically determine the host from incoming request headers.
app.config["SERVER_NAME"] = None

# Session Cookie Configuration
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent JavaScript access
app.config["PERMANENT_SESSION_LIFETIME"] = 86400 * 7  # 7 days in seconds
app.config["REMEMBER_COOKIE_DURATION"] = 86400 * 30  # 30 days for remember me

if IS_VERCEL:
    # Production (HTTPS)
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
else:
    # Local Development (HTTP)
    app.config["SESSION_COOKIE_SECURE"] = False
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_DOMAIN"] = None

app.config["PREFERRED_URL_SCHEME"] = os.environ.get(
    "PREFERRED_URL_SCHEME", "https" if IS_VERCEL else "http"
)

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Rate limiter initialization
limiter.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "error"
login_manager.init_app(app)
# Initialize Supabase client
supabase = get_supabase_client()
app.supabase = supabase

@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(int(user_id))


def seed_database():
    """Seed the database with initial data"""
    from models import Attraction, User
    import json

    # Check if attractions exist
    if Attraction.query.first() is None:
        data_path = os.path.join(BASE_DIR, "data", "attractions.json")
        if os.path.exists(data_path):
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
            print("Database seeded with attractions.")

    # Create default admin if not exists
    if User.query.filter_by(username="admin").first() is None:
        admin = User(
            username="admin", email="admin@example.com", role="admin", is_approved=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Default admin created.")

    # Create default contributor (Barangay Rep) if not exists
    if User.query.filter_by(username="barangay").first() is None:
        contributor = User(
            username="barangay",
            email="barangay@example.com",
            role="contributor",
            barangay="Poblacion",
            is_approved=True,
        )
        contributor.set_password("barangay123")
        db.session.add(contributor)
        db.session.commit()
        print("Default contributor created.")


# Database initialization and seeding (safely)
with app.app_context():
    if not IS_VERCEL:
        db.create_all()
        seed_database()
    else:
        # On Vercel, we NEVER run create_all() or seed_database() in the main flow.
        # These should be handled by migrations or a manual trigger.
        # Running them on every cold start adds several seconds of latency.
        pass


# Make config available in all templates
@app.context_processor
def inject_config():
    return dict(
        config=app.config,
        mapbox_token=os.environ.get("mapbox_token", "")
    )


# Session Persistence Handler
@app.before_request
def make_session_permanent():
    """Make all sessions permanent to persist across browser restarts"""
    from flask import session

    session.permanent = True


# Register all blueprints
register_blueprints(app)

@app.route('/sw.js')
def serve_sw():
    from flask import send_from_directory
    return send_from_directory(static_dir, 'sw.js', mimetype='application/javascript')

@app.route('/manifest.json')
def serve_manifest():
    from flask import send_from_directory
    return send_from_directory(static_dir, 'manifest.json', mimetype='application/json')



@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    # Allow Google Sign-In popup to communicate with the main window
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    return response


# Error Handlers
@app.errorhandler(400)
def bad_request(e):
    return render_template("errors/400.html"), 400


@app.errorhandler(401)
def unauthorized(e):
    return render_template("errors/401.html"), 401


@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(408)
def request_timeout(e):
    return render_template("errors/408.html"), 408


@app.errorhandler(429)
def too_many_requests(e):
    return render_template("errors/429.html"), 429


@app.errorhandler(451)
def legal_reasons(e):
    return render_template("errors/451.html"), 451


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000

    # NOTE: Do NOT set SERVER_NAME here - it causes session cookie domain binding issues.
    # Flask automatically determines the host from incoming request headers.
    # Setting SERVER_NAME to "127.0.0.1:5000" causes cookies to fail when accessing via "localhost".

    # Local development Detected message
    if not IS_VERCEL:
        print(f"Starting in local development mode on http://{host}:{port}")

    app.run(host=host, port=port, debug=True)
