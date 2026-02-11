from flask import Blueprint

# Create the barangay blueprint
barangay_bp = Blueprint("barangay", __name__, url_prefix="/barangay")

# Import sub-modules to register their routes
# These imports are at the bottom to avoid circular dependencies
from . import dashboard, attractions, events, gallery, profile  # noqa: F401
