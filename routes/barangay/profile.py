import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import BarangayInfo
from . import barangay_bp

logger = logging.getLogger(__name__)

@barangay_bp.route("/profile", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_profile_manage():
    """Manage the barangay's cultural and tourism profile information."""
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
