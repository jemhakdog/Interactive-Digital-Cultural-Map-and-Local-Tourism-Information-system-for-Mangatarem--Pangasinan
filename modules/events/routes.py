"""
Routes for the Events module.
Extracted from routes/public.py.
"""

from flask import Blueprint, render_template, request
from .models import Event
from core.logger import log_entry, log_query, log_render
import logging

events_bp = Blueprint("events", __name__, url_prefix="/events")
logger = logging.getLogger(__name__)

@events_bp.route("/")
def index():
    """
    Display all approved events in chronological order.
    """
    log_entry("events", "index")
    logger.info("Events page accessed")

    page = request.args.get('page', 1, type=int)
    per_page = 12

    log_query("events", "index", "Fetching approved events with pagination")
    paginated = Event.query.filter_by(status="approved").order_by(Event.date.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    log_render("events", "index", "events.html")
    return render_template(
        "pagez/events.html", events=paginated.items, pagination=paginated
    )
