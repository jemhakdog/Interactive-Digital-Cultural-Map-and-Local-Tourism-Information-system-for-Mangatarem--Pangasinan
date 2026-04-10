def register_blueprints(app):
    """Register all application blueprints"""
    from .public import public_bp
    from .api import api_bp
    from .auth import auth_bp
    from .admin import admin_bp
    from .barangay import barangay_bp
    from .user import user_bp
    from .update import update_bp
    from .map_routes import map_bp

    from .admin.newsletter import newsletter_admin_bp
    from .business import business_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(barangay_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(newsletter_admin_bp)
    app.register_blueprint(business_bp)

