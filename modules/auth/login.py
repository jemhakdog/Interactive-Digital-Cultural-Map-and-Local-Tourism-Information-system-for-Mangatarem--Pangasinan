from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import limiter
from .models import User
import logging
from utils.logger_helper import (
    log_entry,
    log_query,
    log_logic,
    log_success,
    log_error,
    log_render,
    log_redirect
)
from typing import Optional

logger = logging.getLogger(__name__)

def _authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate user by username and password."""
    log_query("auth", "login", f"Fetching user '{username}'")
    user = User.query.filter_by(username=username).first()
    
    if user:
        log_logic("auth", "login", f"Found user '{username}' with role '{user.role}'")
        if user.check_password(password):
            log_logic("auth", "login", f"Password check successful for '{username}'")
            return user
    
    return None

def _check_approval_status(user: User) -> bool:
    """Check if user is approved. Business owners allowed if unapproved to upload docs."""
    if user.role == "contributor" and not user.is_approved:
        log_logic("auth", "login", f"User '{user.username}' with role '{user.role}' pending approval")
        return False
    return True

@limiter.limit("5 per minute")
def login_view():
    log_entry("auth", "login", method=request.method)
    logger.info("Login page accessed")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = _authenticate_user(username, password)
        
        if user:
            if not _check_approval_status(user):
                log_logic("auth", "login", f"Redirecting unapproved contributor '{username}' to pending page")
                return redirect(url_for("auth.pending_approval"))
            
            log_success("auth", "login", f"User '{username}' logged in")
            logger.info(f"User '{username}' with role '{user.role}' logged in successfully")
            login_user(user, remember=True)
            
            if user.role == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            elif user.role == "contributor":
                return redirect(url_for("barangay.barangay_dashboard"))
            elif user.role == "business_owner":
                return redirect(url_for("business.dashboard"))
            elif user.role == "user":
                return redirect(url_for("user.dashboard"))
            
            return redirect(url_for("public.index"))
        
        log_error("auth", "login", f"Invalid credentials for '{username}'")
        flash("Invalid username or password", "error")
    
    from .oauth import _generate_oauth_nonce
    nonce = _generate_oauth_nonce()
    session["oauth_nonce"] = nonce
    log_render("auth", "login", "login.html")
    return render_template("auth/login.html", oauth_nonce=nonce)

@login_required
def logout_view():
    log_entry("auth", "logout", user=current_user.username)
    logger.info("User logged out successfully")
    logout_user()
    log_redirect("auth", "logout", "home")
    return redirect(url_for("public.index"))
