from flask import render_template, request, redirect, url_for, flash
from extensions import db, limiter
from .models import User
import logging
from utils.security import (
    validate_email_format,
    validate_username,
    validate_password_strength,
    validate_and_escape,
)
from utils.logger_helper import (
    log_entry,
    log_query,
    log_logic,
    log_success,
    log_error,
    log_render,
)
from typing import Optional

logger = logging.getLogger(__name__)

def _validate_username_available(username: str) -> bool:
    """Check if username is available for registration."""
    if User.query.filter_by(username=username).first():
        log_error("auth", "register", f"Username '{username}' already exists")
        return False
    return True

def _validate_email_available(email: str) -> bool:
    """Check if email is available for registration."""
    if User.query.filter_by(email=email).first():
        log_error("auth", "register", f"Email '{email}' already exists")
        return False
    return True

def _validate_barangay_representative(barangay_id: Optional[int], role: str) -> bool:
    """Check if barangay already has an approved representative."""
    if role != "contributor":
        return True
    
    log_query("auth", "register", f"Checking existing representative for ID '{barangay_id}'")
    existing_rep = User.query.filter_by(
        barangay_id=barangay_id, role="contributor", is_approved=True
    ).first()
    
    if existing_rep:
        log_error("auth", "register", f"Representative already exists for ID '{barangay_id}'")
        return False
    
    return True

def _create_user_from_form(username: str, email: str, password: str, role: str, barangay_id: Optional[int]) -> User:
    """Create new user from registration form data."""
    log_logic("auth", "register", f"Creating new user '{username}' with role '{role}'")
    
    user = User(
        username=username,
        email=email,
        role=role,
        barangay_id=barangay_id if role == "contributor" else None,
        is_approved=(role == "user"),
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    log_success("auth", "register", f"New user '{username}' registered with role '{role}'")
    logger.info(f"New user '{username}' registered with role '{role}', awaiting approval={not user.is_approved}")
    
    return user

@limiter.limit("5 per minute")
def register_view():
    log_entry("auth", "register", method=request.method)
    logger.info("Registration page accessed")
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "user")
        barangay_name = request.form.get("barangay")
        
        barangay_id = None
        if role == "contributor" and barangay_name:
            from modules.barangay.models import BarangayInfo
            barangay_record = BarangayInfo.query.filter_by(name=barangay_name).first()
            if not barangay_record:
                # Create the barangay if it doesn't exist
                barangay_record = BarangayInfo(name=barangay_name)
                db.session.add(barangay_record)
                db.session.commit()
            barangay_id = barangay_record.id

        log_query("auth", "register", f"Checking existence for username='{username}', email='{email}'")

        # Input format validation
        if not validate_username(username):
            flash("Username must be 3-30 characters and contain only letters, numbers, and underscores.", "error")
            return redirect(url_for("auth.register"))

        if not validate_email_format(email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("auth.register"))

        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            flash(error_msg, "error")
            return redirect(url_for("auth.register"))

        # Validation chain
        if not _validate_username_available(username):
            flash("Username already exists.", "error")
            return redirect(url_for("auth.register"))

        if not _validate_email_available(email):
            flash("Email already exists.", "error")
            return redirect(url_for("auth.register"))

        if not _validate_barangay_representative(barangay_id, role):
            flash("This Barangay already has a registered representative.", "error")
            return redirect(url_for("auth.register"))

        # Sanitize inputs before saving
        username = validate_and_escape(username)
        email = validate_and_escape(email)

        # Create user
        _create_user_from_form(username, email, password, role, barangay_id)

        if role in ["contributor", "business_owner"]:
            return redirect(url_for("auth.pending_approval"))
        else:
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("auth.login"))
    
    log_render("auth", "register", "register.html")
    return render_template("auth/register.html")

@limiter.limit("5 per minute")
def register_business_view():
    log_entry("auth", "register_business", method=request.method)
    logger.info("Business registration page accessed")
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        
        # Input format validation
        if not validate_username(username):
            flash("Username must be 3-30 characters and contain only letters, numbers, and underscores.", "error")
            return redirect(url_for("auth.register_business"))

        if not validate_email_format(email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("auth.register_business"))

        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            flash(error_msg, "error")
            return redirect(url_for("auth.register_business"))

        # Validation
        if not _validate_username_available(username):
            flash("Username already exists.", "error")
            return redirect(url_for("auth.register_business"))

        if not _validate_email_available(email):
            flash("Email already exists.", "error")
            return redirect(url_for("auth.register_business"))

        # Sanitize inputs before saving
        username = validate_and_escape(username)
        email = validate_and_escape(email)

        # Create business owner user
        user = User(
            username=username,
            email=email,
            role="business_owner",
            is_approved=False,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        log_success("auth", "register_business", f"Business owner '{username}' registered")
        logger.info(f"New business owner '{username}' registered, awaiting approval")

        return redirect(url_for("auth.pending_approval"))
    
    return render_template("auth/register_business.html")

def pending_approval_view():
    log_entry("auth", "pending_approval")
    return render_template("auth/pending_approval.html")
