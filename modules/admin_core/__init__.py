from flask import Blueprint

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

from . import dashboard, users, visits, content, documents

# Import admin routes from domain modules to register them with admin_bp
from modules.attractions import admin_routes as _attractions_admin
from modules.business import admin_routes as _business_admin
from modules.events import admin_routes as _events_admin
from modules.heritage import admin_routes as _heritage_admin
