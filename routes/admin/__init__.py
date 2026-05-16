from flask import Blueprint

# Create the admin blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Import sub-modules to register their routes
# These imports are at the bottom to avoid circular dependencies
from . import dashboard, users, attractions, events, content, heritage, documents, establishments, visits  # noqa: F401
