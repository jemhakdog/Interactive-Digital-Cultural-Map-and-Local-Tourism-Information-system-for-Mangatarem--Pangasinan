import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import BarangayInfo
from utils.security import validate_string_input, sanitize_html_input
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

        history = request.form.get("history", "")
        cultural_assets = request.form.get("cultural_assets", "")
        traditions = request.form.get("traditions", "")
        local_practices = request.form.get("local_practices", "")
        unique_features = request.form.get("unique_features", "")

        # Validate history
        is_valid, error_msg = validate_string_input(history, max_length=5000, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid history: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_profile_manage"))

        # Validate cultural_assets
        is_valid, error_msg = validate_string_input(cultural_assets, max_length=5000, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid cultural assets: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_profile_manage"))

        # Validate traditions
        is_valid, error_msg = validate_string_input(traditions, max_length=5000, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid traditions: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_profile_manage"))

        # Validate local_practices
        is_valid, error_msg = validate_string_input(local_practices, max_length=5000, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid local practices: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_profile_manage"))

        # Validate unique_features
        is_valid, error_msg = validate_string_input(unique_features, max_length=5000, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid unique features: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_profile_manage"))

        info.history = sanitize_html_input(history)
        info.cultural_assets = sanitize_html_input(cultural_assets)
        info.traditions = sanitize_html_input(traditions)
        info.local_practices = sanitize_html_input(local_practices)
        info.unique_features = sanitize_html_input(unique_features)

        db.session.commit()

        logger.info("Barangay profile for %s updated by %s", current_user.barangay, current_user.username)
        flash("Barangay profile updated successfully!")
        return redirect(url_for("barangay.barangay_profile_manage"))

    return render_template("barangay/profile.html", info=info)
