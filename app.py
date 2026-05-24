"""
Application Factory implementation.

Modularizes application creation and configuration to improve testability
and clarify dependency management.
"""

import os
import sys
import logging
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
import models
from extensions import db, login_manager, limiter, csrf, socketio
from config import config_by_name
from modules.registry import register_blueprints
from utils.template_filters import register_filters
from dotenv import load_dotenv

# Load environment variables early
from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configure root logger so all info/debug messages print to console
logging.basicConfig(
    level=logging.DEBUG if os.environ.get("FLASK_ENV") != "production" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

from core.app_setup import (
    init_supabase_support,
    init_redis_support,
    register_error_handlers,
    register_context_processors,
    register_request_hooks,
    register_utility_routes,
    seed_database
)

def create_app(config_name=None):
    """
    Application factory to create and configure the Flask app.
    
    Args:
        config_name: Configuration key ('development', 'production', 'testing')
        
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    
    # Determine absolute paths for template/static folders
    is_vercel = "VERCEL" in os.environ
    if is_vercel:
        base_dir = "/var/task"
    elif getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
    )
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Apply ProxyFix for Production/Vercel
    if is_vercel:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import jsonify, flash, redirect, url_for
        # Handle AJAX/fetch requests by returning 401 JSON instead of 302 Redirect
        if request.is_json or request.path.startswith('/api/') or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.accept_mimetypes.values() or request.path.startswith('/user/') or request.path.startswith('/booking/'):
            return jsonify({
                "success": False,
                "status": "error",
                "message": "Please log in to access this resource.",
                "redirect_url": url_for("auth.login")
            }), 401
            
        flash(login_manager.login_message, login_manager.login_message_category)
        return redirect(url_for(login_manager.login_view, next=request.url))
    
    if not is_vercel:
        from flask_migrate import Migrate
        Migrate(app, db)

    # Register Blueprints
    register_blueprints(app)

    # Register template filters for secure output encoding
    register_filters(app)

    # Initialize Lazy-loaded Supabase support
    init_supabase_support(app)
    
    # Initialize Redis support for caching
    init_redis_support(app)
    
    # Register core application hooks and handlers
    register_error_handlers(app)
    register_context_processors(app)
    register_request_hooks(app)
    register_utility_routes(app)
    
    # Database initialization/seeding (Local only)
    with app.app_context():
        if not is_vercel:
            db.create_all()
            seed_database(app)

    return app

# Entry point for Vercel and local running
app = create_app()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5002, debug=True)
