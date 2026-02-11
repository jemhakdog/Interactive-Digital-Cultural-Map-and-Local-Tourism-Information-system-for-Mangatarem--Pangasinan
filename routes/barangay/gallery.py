import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import GalleryItem
from utils.file_helpers import save_uploaded_file, detect_media_type
from . import barangay_bp

logger = logging.getLogger(__name__)

@barangay_bp.route("/gallery")
@login_required
def barangay_gallery():
    """Display all gallery items created by the current contributor."""
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    gallery_items = (
        GalleryItem.query.filter_by(user_id=current_user.id)
        .order_by(GalleryItem.uploaded_at.desc())
        .all()
    )
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

        if request.form.get("url") and not ("media_file" in request.files and request.files["media_file"].filename):
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
    gallery_item = GalleryItem.query.get_or_404(id)

    if gallery_item.user_id != current_user.id:
        flash("Access denied.")
        return redirect(url_for("barangay.barangay_dashboard"))

    db.session.delete(gallery_item)
    db.session.commit()

    logger.info("Gallery item ID %d deleted by %s", id, current_user.username)
    flash("Gallery item deleted.")
    return redirect(url_for("barangay.barangay_dashboard"))
