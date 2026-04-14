import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Event
from datetime import datetime
from utils.logger_helper import log_entry, log_success, log_error
from utils.file_helpers import save_uploaded_file
from utils.security import validate_string_input, sanitize_html_input, validate_integer
from . import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route("/events")
@login_required
def admin_events():
    """Display events management page."""
    log_entry("admin", "admin_events")
    
    if current_user.role != "admin":
        log_error("admin", "admin_events", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    all_events = Event.query.order_by(Event.date.asc()).all()
    pending_events = [e for e in all_events if e.status == "pending"]
    
    log_success("admin", "admin_events", f"Loaded {len(all_events)} events")
    return render_template(
        "admin/events.html", pending_events=pending_events, all_events=all_events
    )


@admin_bp.route("/events/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_event(id):
    """Approve pending event."""
    log_entry("admin", "approve_event", id=id)
    
    if current_user.role != "admin":
        log_error("admin", "approve_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    event = Event.query.get_or_404(id)
    event.status = "approved"
    db.session.commit()
    
    log_success("admin", "approve_event", f"Event '{event.name}' approved")
    flash(f'Event "{event.name}" approved!')
    return redirect(url_for("admin.admin_events"))


@admin_bp.route("/events/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_event(id):
    """Reject and delete pending event."""
    log_entry("admin", "reject_event", id=id)
    
    if current_user.role != "admin":
        log_error("admin", "reject_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    event = Event.query.get_or_404(id)
    title = event.name
    db.session.delete(event)
    db.session.commit()
    
    log_success("admin", "reject_event", f"Event '{title}' rejected")
    flash(f'Event "{title}" rejected and removed.')
    return redirect(url_for("admin.admin_events"))


@admin_bp.route("/events/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def add_event():
    """Add new event (admin only)."""
    log_entry("admin", "add_event", method=request.method)
    
    if current_user.role != "admin":
        log_error("admin", "add_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        category = request.form.get("category")
        description = request.form.get("description")
        date_str = request.form.get("date")
        barangay_id_str = request.form.get("barangay_id", "1")

        # Validate name
        valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
        if not valid:
            flash(f"Name: {err}", "error")
            return redirect(url_for("admin.add_event"))

        # Validate and sanitize description
        valid, err = validate_string_input(description, max_length=2000, block_sql_injection=True)
        if not valid:
            flash(f"Description: {err}", "error")
            return redirect(url_for("admin.add_event"))
        description = sanitize_html_input(description)

        # Validate location
        valid, err = validate_string_input(location, max_length=300, block_sql_injection=True)
        if not valid:
            flash(f"Location: {err}", "error")
            return redirect(url_for("admin.add_event"))

        # Validate category
        valid, err = validate_string_input(category, max_length=100, block_sql_injection=True)
        if not valid:
            flash(f"Category: {err}", "error")
            return redirect(url_for("admin.add_event"))

        # Validate date (existing strptime validation)
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            flash("Invalid date format. Use YYYY-MM-DD.", "error")
            return redirect(url_for("admin.add_event"))

        # Validate barangay_id
        valid_bar, barangay_id, err_bar = validate_integer(barangay_id_str, min_value=1)
        if not valid_bar:
            flash("Invalid barangay ID.", "error")
            return redirect(url_for("admin.add_event"))

        image_url = request.form.get("image_url")
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                image_url = uploaded_url

        event = Event(
            name=name,
            date=event_date,
            location=location,
            category=category,
            description=description,
            image_url=image_url,
            barangay_id=barangay_id,
            user_id=current_user.id,
            status="approved",
        )
        db.session.add(event)
        db.session.commit()

        log_success("admin", "add_event", f"New event '{event.name}' added")
        flash("Event added successfully!")
        return redirect(url_for("admin.admin_events"))
    
    return render_template("admin/add_event.html")


@admin_bp.route("/events/edit/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def edit_event(id):
    """Edit existing event (admin only)."""
    log_entry("admin", "edit_event", id=id, method=request.method)
    event = Event.query.get_or_404(id)
    
    if current_user.role != "admin":
        log_error("admin", "edit_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        category = request.form.get("category")
        description = request.form.get("description")
        date_str = request.form.get("date")
        barangay_id_str = request.form.get("barangay_id")

        # Validate name
        valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
        if not valid:
            flash(f"Name: {err}", "error")
            return redirect(url_for("admin.edit_event", id=id))

        # Validate and sanitize description
        valid, err = validate_string_input(description, max_length=2000, block_sql_injection=True)
        if not valid:
            flash(f"Description: {err}", "error")
            return redirect(url_for("admin.edit_event", id=id))
        description = sanitize_html_input(description)

        # Validate location
        valid, err = validate_string_input(location, max_length=300, block_sql_injection=True)
        if not valid:
            flash(f"Location: {err}", "error")
            return redirect(url_for("admin.edit_event", id=id))

        # Validate category
        valid, err = validate_string_input(category, max_length=100, block_sql_injection=True)
        if not valid:
            flash(f"Category: {err}", "error")
            return redirect(url_for("admin.edit_event", id=id))

        # Validate date
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            flash("Invalid date format. Use YYYY-MM-DD.", "error")
            return redirect(url_for("admin.edit_event", id=id))

        # Validate barangay_id if provided
        if barangay_id_str:
            valid_bar, barangay_id, err_bar = validate_integer(barangay_id_str, min_value=1)
            if not valid_bar:
                flash("Invalid barangay ID.", "error")
                return redirect(url_for("admin.edit_event", id=id))
            event.barangay_id = barangay_id

        event.name = name
        event.date = event_date
        event.location = location
        event.category = category
        event.description = description

        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                event.image_url = uploaded_url

        if request.form.get("image_url") and not ("image" in request.files and request.files["image"].filename):
            event.image_url = request.form.get("image_url")

        db.session.commit()
        log_success("admin", "edit_event", f"Event '{event.name}' updated")
        flash("Event updated successfully!")
        return redirect(url_for("admin.admin_events"))
    
    return render_template("admin/edit_event.html", event=event)


@admin_bp.route("/events/delete/<int:id>")
@login_required
@limiter.limit("10 per minute")
def delete_event(id):
    """Delete event (admin only)."""
    log_entry("admin", "delete_event", id=id)
    
    if current_user.role != "admin":
        log_error("admin", "delete_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    event = Event.query.get_or_404(id)
    title = event.name
    db.session.delete(event)
    db.session.commit()
    
    log_success("admin", "delete_event", f"Event '{title}' deleted")
    flash("Event deleted successfully!")
    return redirect(url_for("admin.admin_events"))
