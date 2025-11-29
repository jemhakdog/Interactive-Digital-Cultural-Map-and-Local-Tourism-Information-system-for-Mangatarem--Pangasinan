from .public import public_bp
from .api import api_bp
from .auth import auth_bp
from .admin import admin_bp
from .barangay import barangay_bp
from .update import update_bp

def register_blueprints(app):
    """Register all application blueprints"""
    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(barangay_bp)
    app.register_blueprint(update_bp)