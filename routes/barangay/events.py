import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Event
from datetime import datetime
from utils.file_helpers import save_uploaded_file
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
        image_url = request.form.get("image_url")
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                image_url = uploaded_url

        event = Event(
            title=request.form["title"],
            date=datetime.strptime(request.form["date"], "%Y-%m-%d").date(),
            location=request.form["location"],
            category=request.form["category"],
            description=request.form["description"],
            image_url=image_url,
            barangay_id=current_user.barangay_id,
            user_id=current_user.id,
            status="pending",
        )
        db.session.add(event)
        db.session.commit()

        logger.info("New event '%s' submitted by %s", event.title, current_user.username)
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
        event.title = request.form["title"]
        event.date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        event.location = request.form["location"]
        event.category = request.form["category"]
        event.description = request.form["description"]

        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                event.image_url = uploaded_url

        if request.form.get("image_url") and not ("image" in request.files and request.files["image"].filename):
            event.image_url = request.form.get("image_url")

        event.status = "pending"
        db.session.commit()

        logger.info("Event '%s' (ID: %d) updated by %s", event.title, id, current_user.username)
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

    event_title = event.title
    db.session.delete(event)
    db.session.commit()

    logger.info("Event '%s' (ID: %d) deleted by %s", event_title, id, current_user.username)
    flash("Event deleted.")
    return redirect(url_for("barangay.barangay_dashboard"))
