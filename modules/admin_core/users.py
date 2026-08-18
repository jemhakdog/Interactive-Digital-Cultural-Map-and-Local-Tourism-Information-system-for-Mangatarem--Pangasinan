import logging
from flask import redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import User
from utils.logger_helper import log_entry, log_success, log_error
from . import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route("/users/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_user(id):
    """Approve pending contributor user."""
    log_entry("admin", "approve_user", id=id)
    
    if current_user.role != "admin":
        log_error("admin", "approve_user", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    user = User.query.get_or_404(id)
    user.is_approved = True
    db.session.commit()
    
    log_success("admin", "approve_user", f"User '{user.username}' approved")
    flash(f"User {user.username} approved!")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/users/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_user(id):
    """Reject and delete pending contributor user."""
    log_entry("admin", "reject_user", id=id)
    
    if current_user.role != "admin":
        log_error("admin", "reject_user", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    user = User.query.get_or_404(id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    log_success("admin", "reject_user", f"User '{username}' rejected")
    flash(f"User {username} rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))
