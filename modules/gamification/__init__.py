from flask import Blueprint

gamification_bp = Blueprint("gamification", __name__, url_prefix="/passport")

from . import routes
