def register_blueprints(app):
    """Register all application blueprints"""
    from .public import public_bp
    from .api import api_bp
    from modules.auth.routes import auth_bp
    from .admin import admin_bp
    from modules.barangay.routes import barangay_bp
    from .user import user_bp
    from .update import update_bp
    from .map_routes import map_bp

    from .admin.newsletter import newsletter_admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(barangay_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(newsletter_admin_bp)
    from modules.attractions.routes import attractions_bp
    from modules.events.routes import events_bp
    from modules.business.routes import business_bp
    from modules.heritage.routes import heritage_bp
    from modules.gallery.routes import gallery_bp
    from modules.notifications.routes import notifications_bp
    from modules.analytics.routes import analytics_bp

    from .v1.documents import v1_docs_bp
    from .v1.public import public_v1_bp
    app.register_blueprint(v1_docs_bp)
    app.register_blueprint(public_v1_bp)
    app.register_blueprint(attractions_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(business_bp)
    app.register_blueprint(heritage_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(analytics_bp)

    from modules.chat.routes import chat_bp
    import modules.chat.sockets  # Register socket handlers
    app.register_blueprint(chat_bp)

