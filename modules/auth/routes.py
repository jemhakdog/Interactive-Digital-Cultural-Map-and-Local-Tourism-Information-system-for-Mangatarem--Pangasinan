"""
Authentication routes for the Auth module.
Refactored from routes/auth.py into Modular Monolith structure.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, limiter
from .models import User, PasswordResetToken
from core.email_sender import send_password_reset_email
from core.security import (
    validate_email_format,
    validate_username,
    validate_password_strength,
    validate_and_escape,
)
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from core.logger import (
    log_entry,
    log_query,
    log_logic,
    log_success,
    log_error,
    log_render,
    log_redirect
)
import logging
import os
from typing import Optional, Tuple

auth_bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")
logger = logging.getLogger(__name__)

# Google OAuth Client ID – loaded from environment variable
GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com",
)


def _authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Authenticate user by username and password.
    """
    log_query("auth", "login", f"Fetching user '{username}'")
    user = User.query.filter_by(username=username).first()
    
    if user:
        log_logic("auth", "login", f"Found user '{username}' with role '{user.role}'")
        if user.check_password(password):
            log_logic("auth", "login", f"Password check successful for '{username}'")
            return user
    
    return None


def _check_approval_status(user: User) -> bool:
    """
    Check if user is approved.
    """
    if user.role in ["contributor", "business_owner"] and not user.is_approved:
        log_logic("auth", "login", f"User '{user.username}' with role '{user.role}' pending approval")
        return False
    return True


def _validate_username_available(username: str) -> bool:
    """
    Check if username is available for registration.
    """
    if User.query.filter_by(username=username).first():
        log_error("auth", "register", f"Username '{username}' already exists")
        return False
    return True


def _validate_email_available(email: str) -> bool:
    """
    Check if email is available for registration.
    """
    if User.query.filter_by(email=email).first():
        log_error("auth", "register", f"Email '{email}' already exists")
        return False
    return True


def _validate_barangay_representative(barangay_id: str, role: str) -> bool:
    """
    Check if barangay already has an approved representative.
    """
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


def _create_user_from_form(username: str, email: str, password: str, role: str, barangay_id: Optional[str]) -> User:
    """
    Create new user from registration form data.
    """
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


def _verify_google_token(token: str) -> Optional[Tuple[str, str]]:
    """
    Verify Google OAuth token and extract user info.
    """
    try:
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        email = idinfo.get("email")
        name = idinfo.get("name")
        log_success("auth", "google_login", f"Verified token for {email} ({name})")
        return (email, name)
    except ValueError as e:
        log_error("auth", "google_login", f"Invalid token: {str(e)}")
        return None


def _generate_unique_username(base_username: str) -> str:
    """
    Generate unique username by appending counter if needed.
    """
    username = base_username
    counter = 1
    while User.query.filter_by(username=username).first():
        username = f"{base_username}_{counter}"
        counter += 1
    return username


def _create_google_user(email: str, name: Optional[str]) -> Optional[User]:
    """
    Create new user from Google OAuth data.
    """
    log_logic("auth", "google_login", f"User not found, creating new account for {email}")
    
    # Generate base username from name or email
    if name:
        base_username = name.lower().replace(" ", "")
    else:
        base_username = email.split("@")[0]
    
    username = _generate_unique_username(base_username)
    
    try:
        user = User(
            username=username,
            email=email,
            role="user",
            is_approved=True,
        )
        user.set_password(os.urandom(24).hex()) # Dummy password for Google users
        db.session.add(user)
        db.session.commit()
        log_success("auth", "google_login", f"Created new user '{username}' for '{email}'")
        return user
    except Exception as e:
        db.session.rollback()
        log_error("auth", "google_login", f"DB Commit failed: {str(e)}")
        return None


def _check_role_restrictions(user: User) -> bool:
    """
    Check if user role is allowed for Google Sign-In.
    """
    if user.role in ["admin", "contributor"]:
        log_error("auth", "google_login", f"Role '{user.role}' restricted from Google Sign-In")
        return False
    return True


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
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
    
    log_render("auth", "login", "login.html")
    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():
    log_entry("auth", "register", method=request.method)
    logger.info("Registration page accessed")
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "user")
        barangay_id = request.form.get("barangay")

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


@auth_bp.route("/register/business", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register_business():
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


@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    log_entry("auth", "google_login")
    token = request.form.get("credential")
    
    if not token:
        log_error("auth", "google_login", "No credential provided")
        flash("No Google credential received.", "error")
        return redirect(url_for("auth.login"))
    
    # Verify token
    credentials = _verify_google_token(token)
    if not credentials:
        flash("Invalid Google token. Please try again.", "error")
        return redirect(url_for("auth.login"))
    
    email, name = credentials
    user = User.query.filter_by(email=email).first()
    
    # Create new user if doesn't exist
    if not user:
        user = _create_google_user(email, name)
        if not user:
            flash("An error occurred while creating your account. Please try again.", "error")
            return redirect(url_for("auth.login"))
        
        log_success("auth", "google_login", f"Logged in NEW user '{user.username}' (ID: {user.id})")
        login_user(user, remember=True)
        flash(f"Welcome to GoMangatarem, {name or user.username}!", "success")
        return redirect(url_for("user.dashboard"))
    
    # Check role restrictions for existing users
    if not _check_role_restrictions(user):
        flash(
            "Google Sign-In is only available for regular visitor accounts. Please use your credentials to log in.",
            "error",
        )
        return redirect(url_for("auth.login"))
    
    log_success("auth", "google_login", f"Logging in existing user {email} (ID: {user.id})")
    login_user(user, remember=True)
    
    if user.role == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    elif user.role == "contributor":
        return redirect(url_for("barangay.barangay_dashboard"))
    
    return redirect(url_for("user.dashboard"))


@auth_bp.route("/logout")
@login_required
def logout():
    log_entry("auth", "logout", user=current_user.username)
    logger.info("User logged out successfully")
    logout_user()
    log_redirect("auth", "logout", "home")
    return redirect(url_for("public.index"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def forgot_password():
    log_entry("auth", "forgot_password", method=request.method)

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        log_logic("auth", "forgot_password", f"Received password reset request for email: '{email}'")
        user = User.query.filter_by(email=email).first()

        if user:
            log_logic("auth", "forgot_password", f"User found matching email: '{email}'")
            expiry = current_app.config.get("PASSWORD_RESET_EXPIRY_MINUTES", 30)
            reset_token = PasswordResetToken.create_for_user(user, expiry_minutes=expiry)
            relative_url = url_for(
                "auth.reset_password",
                token=reset_token.token
            )
            reset_url = f"{request.url_root.rstrip('/')}{relative_url}"
            sent = send_password_reset_email(user.email, reset_url)
            if sent:
                log_success("auth", "forgot_password", f"Reset email sent to '{email}'")
                flash("A password reset link has been sent. Check your inbox.", "success")
            else:
                log_error("auth", "forgot_password", f"Failed to send reset email to '{email}'")
                flash("Failed to send reset email. Please try again later.", "error")
        else:
            log_error("auth", "forgot_password", f"No user found matching email: '{email}'")
            flash("No user found with that email address. Please check your spelling.", "error")

        return redirect(url_for("auth.forgot_password"))

    return render_template("auth/forgot_password.html")


def _validate_reset_token(token_str: str) -> "PasswordResetToken | None":
    record = PasswordResetToken.query.filter_by(token=token_str).first()
    if record and record.is_valid:
        return record
    return None


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token: str):
    log_entry("auth", "reset_password", method=request.method)

    reset_record = _validate_reset_token(token)
    if not reset_record:
        log_error("auth", "reset_password", "Invalid or expired token")
        flash("Reset link is invalid or has expired. Please request a new one.", "error")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        new_password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if len(new_password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return render_template("auth/reset_password.html", token=token)

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("auth/reset_password.html", token=token)

        reset_record.user.set_password(new_password)
        reset_record.used = True
        db.session.commit()

        log_success("auth", "reset_password", f"Password reset for user id={reset_record.user_id}")
        flash("Your password has been reset. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", token=token)


@auth_bp.route("/pending-approval")
def pending_approval():
    log_entry("auth", "pending_approval")
    return render_template("auth/pending_approval.html")


@auth_bp.route("/api/users/search")
@login_required
def api_user_search():
    """API for searching users to auto-fill visitor logs."""
    query = request.args.get("q", "").strip()
    if not query or len(query) < 2:
        return jsonify([])

    # Only search for approved 'user' role accounts
    users = User.query.filter(
        User.role == "user",
        User.is_approved
    ).filter(
        (User.username.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
    ).limit(5).all()

    results = []
    for user in users:
        results.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "barangay": user.barangay.name if user.barangay else "Unknown"
        })

    return jsonify(results)

