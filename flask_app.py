import json
import os

from dotenv import load_dotenv
from flask import Flask, url_for, render_template
from flask_login import LoginManager
from extensions import limiter

from models import Attraction, User, db
from routes import register_blueprints

# Load environment variables from .ENV file
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"  # Change this in production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mangatarem.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4"}

# Server URL configuration for external URL generation
# Set SERVER_NAME env var in production (e.g., "yourdomain.com" or "yourdomain.com:8080")
app.config["SERVER_NAME"] = os.environ.get("SERVER_NAME")
app.config["PREFERRED_URL_SCHEME"] = os.environ.get("PREFERRED_URL_SCHEME", "http")
print(os.environ.get("SERVER_NAME"))
# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize rate limiter
# Default limits are defined in extensions.py
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
        data_path = os.path.join(app.root_path, "data", "attractions.json")
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
    print(app.url_map)
    host = "0.0.0.0"
    port = 5000

    # Set default SERVER_NAME for local development if not already set
    if not app.config.get("SERVER_NAME"):
        app.config["SERVER_NAME"] = f"127.0.0.1:{port}"

    with app.app_context():
        base_url = url_for("public.index", _external=True)
        print(f"The host URL is: {base_url}")
        db.create_all()
        seed_database()

    # Clear SERVER_NAME before running to avoid routing issues in development
    if os.environ.get("SERVER_NAME") is None:
        app.config["SERVER_NAME"] = None

    app.run(host=host, port=port, debug=True)
