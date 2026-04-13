import os
import sys
from datetime import timedelta
from utils.db_manager import get_database_uri

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")

    # Static and upload folders
    # Handle PyInstaller paths
    if getattr(sys, 'frozen', False):
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    STATIC_FOLDER = os.path.join(BASE_DIR, "static")
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4"}

    # Database
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Session and Cookie Security
    # HttpOnly prevents JavaScript access to cookies (XSS mitigation)
    SESSION_COOKIE_HTTPONLY = True
    # SameSite prevents cross-site request forgery
    SESSION_COOKIE_SAMESITE = "Lax"
    # Session lifetime
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    # Remember me cookie settings
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    # SESSION_COOKIE_SECURE is set per-environment (False in dev, True in prod)

    # Misc
    PASSWORD_RESET_EXPIRY_MINUTES = 30
    # Use request host by default, don't force SERVER_NAME in base config
    # unless explicitly needed for background tasks.
    PREFERRED_URL_SCHEME = "https"
    WTF_CSRF_TIME_LIMIT = None  # Token valid for session duration

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    PREFERRED_URL_SCHEME = "http"
    WTF_CSRF_SSL_STRICT = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True  # Add secure flag for remember cookie
    WTF_CSRF_SSL_STRICT = True
    
    # Vercel specific adjustments usually go here
    # but many are handled by ProxyFix in app.py

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
