import json
import os
import shutil

from dotenv import load_dotenv
from flask import Flask, url_for, render_template, request
from flask_login import LoginManager
from extensions import limiter

from models import Attraction, User, db
from routes import register_blueprints

# Load environment variables from .ENV file
load_dotenv()

# Determine absolute paths for templates and static folders
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your-secret-key-here")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(static_dir, "uploads")
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4"}

# Handle SQLite database path for Vercel
IS_VERCEL = "VERCEL" in os.environ
if IS_VERCEL:
    # On Vercel, the filesystem is read-only except for /tmp/
    db_path = "/tmp/mangatarem.db"
    source_db = os.path.join(BASE_DIR, "instance", "mangatarem.db")

    # Copy the database to /tmp if it doesn't exist there yet
    if os.path.exists(source_db) and not os.path.exists(db_path):
        try:
            shutil.copy2(source_db, db_path)
            print(f"Database copied to {db_path}")
        except Exception as e:
            print(f"Error copying database: {e}")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
else:
    # Local development
    instance_path = os.path.join(BASE_DIR, "instance")
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(instance_path, 'mangatarem.db')}"
    )

# Server URL configuration for external URL generation
app.config["SERVER_NAME"] = os.environ.get("SERVER_NAME")
app.config["PREFERRED_URL_SCHEME"] = os.environ.get("PREFERRED_URL_SCHEME", "http")

# Initialize database
db.init_app(app)

# Rate limiter initialization
limiter.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def seed_database():
    """Seed the database with initial data"""
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
        # On Vercel, we only create tables if they don't exist in /tmp
        db.create_all()


# Make config available in all templates
@app.context_processor
def inject_config():
    return dict(config=app.config)


# Register all blueprints
register_blueprints(app)


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

    # Set default SERVER_NAME for local development if not already set
    if not app.config.get("SERVER_NAME"):
        app.config["SERVER_NAME"] = f"127.0.0.1:{port}"

    with app.app_context():
        # Using a request context simulation if needed for url_for
        # but here we just want to print the base URL
        try:
            base_url = url_for("public.index", _external=True)
            print(f"The host URL is: {base_url}")
        except RuntimeError:
            print("Could not build URL outside of request context")

    # Clear SERVER_NAME before running to avoid routing issues in development
    if os.environ.get("SERVER_NAME") is None:
        app.config["SERVER_NAME"] = None

    app.run(host=host, port=port, debug=True)
