import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Event
from datetime import datetime
from utils.file_helpers import save_uploaded_file
from utils.security import validate_string_input, sanitize_html_input
from . import barangay_bp

logger = logging.getLogger(__name__)

@barangay_bp.route("/events")
@login_required
def barangay_events():
    """Display all events created by the current contributor."""
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    events = (
        Event.query.filter_by(user_id=current_user.id)
        .order_by(Event.date.asc())
        .all()
    )
    return render_template("barangay/events.html", events=events)


@barangay_bp.route("/events/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_add_event():
    """Add a new event (submitted as 'pending' for admin approval)."""
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        location = request.form.get("location", "")
        category = request.form.get("category", "")
        date_str = request.form.get("date", "")

        # Validate name
        is_valid, error_msg = validate_string_input(title, max_length=200, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid event name: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_event"))

        # Validate description
        is_valid, error_msg = validate_string_input(description, max_length=2000, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid description: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_event"))

        # Validate location
        is_valid, error_msg = validate_string_input(location, max_length=300, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid location: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_event"))

        # Validate category
        is_valid, error_msg = validate_string_input(category, max_length=100, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid category: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_event"))

        # Validate date
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            flash("Invalid date: date must be in YYYY-MM-DD format.", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_event"))

        image_url = request.form.get("image_url")
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                image_url = uploaded_url

        event = Event(
            name=title,
            date=event_date,
            location=location,
            category=category,
            description=sanitize_html_input(description),
            image_url=image_url,
            barangay_id=current_user.barangay_id,
            user_id=current_user.id,
            status="pending",
        )
        db.session.add(event)
        db.session.commit()

        logger.info("New event '%s' submitted by %s", event.name, current_user.username)
        flash("Event submitted for approval!")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/add_event.html")


@barangay_bp.route("/events/edit/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_edit_event(id):
    """Edit an event owned by the current contributor (resets to 'pending')."""
    event = Event.query.get_or_404(id)

    if event.user_id != current_user.id:
        flash("Access denied.")
        return redirect(url_for("barangay.barangay_dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        location = request.form.get("location", "")
        category = request.form.get("category", "")
        date_str = request.form.get("date", "")

        # Validate name
        is_valid, error_msg = validate_string_input(title, max_length=200, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid event name: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_event", id=event.id))

        # Validate description
        is_valid, error_msg = validate_string_input(description, max_length=2000, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid description: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_event", id=event.id))

        # Validate location
        is_valid, error_msg = validate_string_input(location, max_length=300, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid location: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_event", id=event.id))

        # Validate category
        is_valid, error_msg = validate_string_input(category, max_length=100, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid category: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_event", id=event.id))

        # Validate date
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            flash("Invalid date: date must be in YYYY-MM-DD format.", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_event", id=event.id))

        event.name = title
        event.date = event_date
        event.location = location
        event.category = category
        event.description = sanitize_html_input(description)

        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                event.image_url = uploaded_url

        if request.form.get("image_url") and not ("image" in request.files and request.files["image"].filename):
            event.image_url = request.form.get("image_url")

        event.status = "pending"
        db.session.commit()

        logger.info("Event '%s' (ID: %d) updated by %s", event.name, id, current_user.username)
        flash("Event updated and submitted for approval.")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/edit_event.html", event=event)


@barangay_bp.route("/events/delete/<int:id>")
@login_required
@limiter.limit("10 per minute")
def barangay_delete_event(id):
    """Delete an event owned by the current contributor."""
    event = Event.query.get_or_404(id)

    if event.user_id != current_user.id:
        flash("Access denied.")
        return redirect(url_for("barangay.barangay_dashboard"))

    event_title = event.name
    db.session.delete(event)
    db.session.commit()

    logger.info("Event '%s' (ID: %d) deleted by %s", event_title, id, current_user.username)
    flash("Event deleted.")
    return redirect(url_for("barangay.barangay_dashboard"))
