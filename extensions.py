from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize extensions without app
# They will be initialized with the app instance in the application factory (app.py)

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "error"

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=["100 per minute"],
)
