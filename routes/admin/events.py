import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Event
from datetime import datetime
from utils.logger_helper import log_entry, log_success, log_error
from utils.file_helpers import save_uploaded_file
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
    
    log_success("admin", "approve_event", f"Event '{event.title}' approved")
    flash(f'Event "{event.title}" approved!')
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
    title = event.title
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
        image_url = request.form.get("image_url")
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                image_url = uploaded_url
        
        event = Event(
            title=request.form["title"],
            date=datetime.strptime(request.form["date"], "%Y-%m-%d"),
            location=request.form["location"],
            category=request.form["category"],
            description=request.form["description"],
            image_url=image_url,
            barangay=request.form.get("barangay", "Mangatarem"),
            user_id=current_user.id,
            status="approved",
        )
        db.session.add(event)
        db.session.commit()
        
        log_success("admin", "add_event", f"New event '{event.title}' added")
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
        event.title = request.form["title"]
        event.date = datetime.strptime(request.form["date"], "%Y-%m-%d")
        event.location = request.form["location"]
        event.category = request.form["category"]
        event.description = request.form["description"]
        event.barangay = request.form.get("barangay", event.barangay)
        
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                event.image_url = uploaded_url
        
        if request.form.get("image_url") and not ("image" in request.files and request.files["image"].filename):
            event.image_url = request.form.get("image_url")
        
        db.session.commit()
        log_success("admin", "edit_event", f"Event '{event.title}' updated")
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
    title = event.title
    db.session.delete(event)
    db.session.commit()
    
    log_success("admin", "delete_event", f"Event '{title}' deleted")
    flash("Event deleted successfully!")
    return redirect(url_for("admin.admin_events"))
