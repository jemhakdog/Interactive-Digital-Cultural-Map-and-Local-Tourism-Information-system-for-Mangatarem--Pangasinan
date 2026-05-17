from flask import Blueprint, redirect, url_for, request
import logging

events_bp = Blueprint("events", __name__, url_prefix="/events")
logger = logging.getLogger(__name__)

@events_bp.route("/")
def index():
    logger.info("Redirecting legacy /events/ to /v1/events")
    return redirect(url_for("public_v1.events_v2_view", **request.args), code=302)
