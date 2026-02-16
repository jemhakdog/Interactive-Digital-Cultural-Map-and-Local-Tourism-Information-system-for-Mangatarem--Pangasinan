import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Attraction
from utils.file_helpers import save_uploaded_file
from . import barangay_bp

logger = logging.getLogger(__name__)

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
    return render_template("barangay/attractions.html", attractions=attractions)


@barangay_bp.route("/attractions/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_add_attraction():
    """Add a new attraction (submitted as 'pending' for admin approval)."""
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

        if request.form.get("image_url") and not ("image" in request.files and request.files["image"].filename):
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
