from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO

# Initialize extensions without app
# They will be initialized with the app instance in the application factory (app.py)

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

import os

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.environ.get("LIMITER_STORAGE_URI", "memory://"),
    default_limits=["100 per minute"],
)

csrf = CSRFProtect()

socketio = SocketIO()
