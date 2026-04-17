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

    # Direct relationship lookup - contributors must have an assigned barangay
    info = current_user.barangay
    
    if not info:
        flash("No barangay assigned to your account. Please contact the administrator.", "error")
        logger.error("Contributor %s has no barangay assigned", current_user.username)
        return redirect(url_for("barangay.barangay_dashboard"))

    if request.method == "POST":
        mission = request.form.get("mission", "")
        vision = request.form.get("vision", "")
        history = request.form.get("history", "")
        cultural_assets = request.form.get("cultural_assets", "")
        traditions = request.form.get("traditions", "")
        local_practices = request.form.get("local_practices", "")
        unique_features = request.form.get("unique_features", "")

        # Validation logic
        fields_to_validate = {
            "mission": mission,
            "vision": vision,
            "history": history,
            "cultural_assets": cultural_assets,
            "traditions": traditions,
            "local_practices": local_practices,
            "unique_features": unique_features
        }

        for label, value in fields_to_validate.items():
            is_valid, error_msg = validate_string_input(value, max_length=5000, block_sql_injection=True)
            if not is_valid:
                flash(f"Invalid {label.replace('_', ' ')}: {error_msg}", "error")
                return redirect(url_for("barangay.barangay_profile_manage"))

        # Update properties
        info.mission = sanitize_html_input(mission)
        info.vision = sanitize_html_input(vision)
        info.history = sanitize_html_input(history)
        info.cultural_assets = sanitize_html_input(cultural_assets)
        info.traditions = sanitize_html_input(traditions)
        info.local_practices = sanitize_html_input(local_practices)
        info.unique_features = sanitize_html_input(unique_features)
        
        # Ensure user_id link is maintained if not already set
        if not info.user_id:
            info.user_id = current_user.id

        db.session.commit()

        logger.info("Barangay profile for %s updated by %s", info.name, current_user.username)
        flash("Barangay profile updated successfully!")
        return redirect(url_for("barangay.barangay_profile_manage"))

    return render_template("barangay/profile.html", info=info)


    return render_template("barangay/profile.html", info=info)
