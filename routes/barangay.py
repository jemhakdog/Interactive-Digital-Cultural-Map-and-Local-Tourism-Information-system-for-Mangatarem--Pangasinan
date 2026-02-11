"""
Barangay contributor routes.

Handles contributor dashboard, CRUD for attractions, events, gallery items,
and barangay profile management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Attraction, Event, GalleryItem, BarangayInfo
from extensions import limiter
from utils.file_helpers import save_uploaded_file, detect_media_type
from datetime import datetime
import logging

barangay_bp = Blueprint("barangay", __name__, url_prefix="/barangay")
logger = logging.getLogger(__name__)


# === DASHBOARD ===


@barangay_bp.route("/dashboard")
@login_required
def barangay_dashboard():
    """Display the barangay contributor dashboard with content statistics."""
    logger.info("Barangay dashboard accessed by %s (%s)", current_user.username, current_user.barangay)

    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    stats = {
        "attractions": Attraction.query.filter_by(user_id=current_user.id).count(),
        "events": Event.query.filter_by(user_id=current_user.id).count(),
        "gallery": GalleryItem.query.filter_by(user_id=current_user.id).count(),
    }

    logger.info("Dashboard stats for %s: %s", current_user.username, stats)
    return render_template("barangay/dashboard.html", stats=stats)


# === ATTRACTIONS ===


@barangay_bp.route("/attractions")
@login_required
def barangay_attractions():
    """Display all attractions created by the current contributor."""
    logger.info("Barangay attractions page accessed by %s", current_user.username)

    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    attractions = (
        Attraction.query.filter_by(user_id=current_user.id)
        .order_by(Attraction.created_at.desc())
        .all()
    )

    logger.info("Loaded %d attractions for %s", len(attractions), current_user.username)
    return render_template("barangay/attractions.html", attractions=attractions)


@barangay_bp.route("/attractions/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_add_attraction():
    """Add a new attraction (submitted as 'pending' for admin approval)."""
    logger.info("Add attraction page accessed by %s", current_user.username)

    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    if request.method == "POST":
        image_url = request.form.get("image_url")

        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                image_url = uploaded_url

        attraction = Attraction(
            name=request.form["name"],
            category=request.form["category"],
            description=request.form["description"],
            lat=float(request.form["lat"]),
            lng=float(request.form["lng"]),
            image_url=image_url,
            barangay=current_user.barangay,
            user_id=current_user.id,
            status="pending",
        )
        db.session.add(attraction)
        db.session.commit()

        logger.info("New attraction '%s' submitted by %s", attraction.name, current_user.username)
        flash("Attraction submitted for approval!")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/add_attraction.html")


@barangay_bp.route("/attractions/edit/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_edit_attraction(id):
    """Edit an attraction owned by the current contributor (resets to 'pending')."""
    logger.info("Edit attraction ID %d requested by %s", id, current_user.username)

    attraction = Attraction.query.get_or_404(id)

    if attraction.user_id != current_user.id:
        flash("Access denied.")
        return redirect(url_for("barangay.barangay_dashboard"))

    if request.method == "POST":
        attraction.name = request.form["name"]
        attraction.category = request.form["category"]
        attraction.description = request.form["description"]
        attraction.lat = float(request.form["lat"])
        attraction.lng = float(request.form["lng"])

        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                attraction.image_url = uploaded_url

        # Fallback to URL if no file uploaded
        if request.form.get("image_url") and not (
            "image" in request.files and request.files["image"].filename
        ):
            attraction.image_url = request.form.get("image_url")

        attraction.status = "pending"
        db.session.commit()

        logger.info("Attraction '%s' (ID: %d) updated by %s", attraction.name, id, current_user.username)
        flash("Attraction updated and submitted for approval.")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/edit_attraction.html", attraction=attraction)


@barangay_bp.route("/attractions/delete/<int:id>")
@login_required
@limiter.limit("10 per minute")
def barangay_delete_attraction(id):
    """Delete an attraction owned by the current contributor."""
    logger.info("Delete attraction ID %d requested by %s", id, current_user.username)

    attraction = Attraction.query.get_or_404(id)

    if attraction.user_id != current_user.id:
        flash("Access denied.")
        return redirect(url_for("barangay.barangay_dashboard"))

    attraction_name = attraction.name
    db.session.delete(attraction)
    db.session.commit()

    logger.info("Attraction '%s' (ID: %d) deleted by %s", attraction_name, id, current_user.username)
    flash("Attraction deleted.")
    return redirect(url_for("barangay.barangay_dashboard"))


# === EVENTS ===


@barangay_bp.route("/events")
@login_required
def barangay_events():
    """Display all events created by the current contributor."""
    logger.info("Barangay events page accessed by %s", current_user.username)

    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    events = (
        Event.query.filter_by(user_id=current_user.id)
        .order_by(Event.date.asc())
        .all()
    )

    logger.info("Loaded %d events for %s", len(events), current_user.username)
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
            barangay=current_user.barangay,
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
    logger.info("Edit event ID %d requested by %s", id, current_user.username)

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

        # Fallback to URL if no file uploaded
        if request.form.get("image_url") and not (
            "image" in request.files and request.files["image"].filename
        ):
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
    logger.info("Delete event ID %d requested by %s", id, current_user.username)

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


# === PROFILE ===


@barangay_bp.route("/profile", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_profile_manage():
    """Manage the barangay's cultural and tourism profile information."""
    logger.info("Barangay profile management by %s", current_user.username)

    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    info = BarangayInfo.query.filter_by(barangay_name=current_user.barangay).first()

    if request.method == "POST":
        if not info:
            info = BarangayInfo(
                barangay_name=current_user.barangay, user_id=current_user.id
            )
            db.session.add(info)

        info.history = request.form.get("history")
        info.cultural_assets = request.form.get("cultural_assets")
        info.traditions = request.form.get("traditions")
        info.local_practices = request.form.get("local_practices")
        info.unique_features = request.form.get("unique_features")

        db.session.commit()

        logger.info("Barangay profile for %s updated by %s", current_user.barangay, current_user.username)
        flash("Barangay profile updated successfully!")
        return redirect(url_for("barangay.barangay_profile_manage"))

    return render_template("barangay/profile.html", info=info)


# === GALLERY ===


@barangay_bp.route("/gallery")
@login_required
def barangay_gallery():
    """Display all gallery items created by the current contributor."""
    logger.info("Barangay gallery page accessed by %s", current_user.username)

    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    gallery_items = (
        GalleryItem.query.filter_by(user_id=current_user.id)
        .order_by(GalleryItem.uploaded_at.desc())
        .all()
    )

    logger.info("Loaded %d gallery items for %s", len(gallery_items), current_user.username)
    return render_template("barangay/gallery.html", gallery_items=gallery_items)


@barangay_bp.route("/gallery/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_add_gallery():
    """Add a new gallery item (photo or video), submitted as 'pending'."""
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    if request.method == "POST":
        url = request.form.get("url")
        item_type = request.form.get("type", "photo")

        if "media_file" in request.files:
            uploaded_url = save_uploaded_file(request.files["media_file"])
            if uploaded_url:
                url = uploaded_url
                item_type = detect_media_type(request.files["media_file"].filename)

        if not url:
            flash("Please provide a media file or URL.")
            return redirect(url_for("barangay.barangay_add_gallery"))

        gallery_item = GalleryItem(
            type=item_type,
            url=url,
            caption=request.form.get("caption"),
            user_id=current_user.id,
            status="pending",
        )
        db.session.add(gallery_item)
        db.session.commit()

        logger.info("New gallery item (%s) submitted by %s", item_type, current_user.username)
        flash("Gallery item submitted for approval!")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/add_gallery.html")


@barangay_bp.route("/gallery/edit/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_edit_gallery(id):
    """Edit a gallery item owned by the current contributor (resets to 'pending')."""
    logger.info("Edit gallery item ID %d requested by %s", id, current_user.username)

    gallery_item = GalleryItem.query.get_or_404(id)

    if gallery_item.user_id != current_user.id:
        flash("Access denied.")
        return redirect(url_for("barangay.barangay_dashboard"))

    if request.method == "POST":
        gallery_item.caption = request.form.get("caption")

        if "media_file" in request.files:
            uploaded_url = save_uploaded_file(request.files["media_file"])
            if uploaded_url:
                gallery_item.url = uploaded_url
                gallery_item.type = detect_media_type(request.files["media_file"].filename)

        # Fallback to URL if no file uploaded
        if request.form.get("url") and not (
            "media_file" in request.files and request.files["media_file"].filename
        ):
            gallery_item.url = request.form.get("url")

        gallery_item.status = "pending"
        db.session.commit()

        logger.info("Gallery item ID %d updated by %s", id, current_user.username)
        flash("Gallery item updated and submitted for approval.")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/edit_gallery.html", gallery_item=gallery_item)


@barangay_bp.route("/gallery/delete/<int:id>")
@login_required
@limiter.limit("10 per minute")
def barangay_delete_gallery(id):
    """Delete a gallery item owned by the current contributor."""
    logger.info("Delete gallery item ID %d requested by %s", id, current_user.username)

    gallery_item = GalleryItem.query.get_or_404(id)

    if gallery_item.user_id != current_user.id:
        flash("Access denied.")
        return redirect(url_for("barangay.barangay_dashboard"))

    db.session.delete(gallery_item)
    db.session.commit()

    logger.info("Gallery item ID %d deleted by %s", id, current_user.username)
    flash("Gallery item deleted.")
    return redirect(url_for("barangay.barangay_dashboard"))
