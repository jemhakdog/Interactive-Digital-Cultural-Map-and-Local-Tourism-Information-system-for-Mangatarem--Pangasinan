def register_blueprints(app):
    """Register all application blueprints from the Modular Monolith structure"""
    
    # Core Global Routes
    from modules.core.public_routes import public_bp
    from modules.core.api_routes import api_bp
    from modules.core.map_routes import map_bp
    from modules.core.user_routes import user_bp
    from modules.core.update_routes import update_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(update_bp)

    # API v1
    from modules.api_v1.documents import v1_docs_bp
    from modules.api_v1.public import public_v1_bp
    app.register_blueprint(v1_docs_bp)
    app.register_blueprint(public_v1_bp)

    # Admin Core
    from modules.admin_core import admin_bp
    app.register_blueprint(admin_bp)

    # Domain Modules
    from modules.auth.routes import auth_bp
    from modules.barangay.routes import barangay_bp
    from modules.attractions.routes import attractions_bp
    from modules.events.routes import events_bp
    from modules.business.routes import business_bp
    from modules.heritage.routes import heritage_bp
    from modules.gallery.routes import gallery_bp
    from modules.notifications.routes import notifications_bp
    from modules.analytics.routes import analytics_bp
    from modules.booking.routes import booking_bp
    
    # Notifications Admin (newsletter)
    from modules.notifications.admin_routes import newsletter_admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(barangay_bp)
    app.register_blueprint(attractions_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(business_bp)
    app.register_blueprint(heritage_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(newsletter_admin_bp)

    # Route Optimization
    from modules.routing.routes import routing_bp
    app.register_blueprint(routing_bp)

    # Chat Module
    from modules.chat.routes import chat_bp
    import modules.chat.sockets  # Register socket handlers
    app.register_blueprint(chat_bp)

    # Gamification Module
    from modules.gamification import gamification_bp
    app.register_blueprint(gamification_bp)

