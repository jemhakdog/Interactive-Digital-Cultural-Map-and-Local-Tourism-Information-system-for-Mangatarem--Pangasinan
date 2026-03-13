"""
Authentication routes with clean function design.

Each helper function has a single responsibility.
Print statements replaced with logging helpers.
Complex route handlers decomposed into focused functions.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from extensions import limiter
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from utils.logger_helper import (
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

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)

# Google OAuth Client ID – loaded from environment variable
GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com",
)


def _authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Authenticate user by username and password.
    
    Args:
        username: Username to authenticate
        password: Password to check
        
    Returns:
        User object if authenticated, None otherwise
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
    Check if contributor user is approved.
    
    Args:
        user: User object to check
        
    Returns:
        True if approved or not a contributor, False if pending
    """
    if user.role == "contributor" and not user.is_approved:
        log_logic("auth", "login", f"Contributor '{user.username}' pending approval")
        return False
    return True


def _validate_username_available(username: str) -> bool:
    """
    Check if username is available for registration.
    
    Args:
        username: Username to validate
        
    Returns:
        True if available, False if taken
    """
    if User.query.filter_by(username=username).first():
        log_error("auth", "register", f"Username '{username}' already exists")
        return False
    return True


def _validate_email_available(email: str) -> bool:
    """
    Check if email is available for registration.
    
    Args:
        email: Email to validate
        
    Returns:
        True if available, False if taken
    """
    if User.query.filter_by(email=email).first():
        log_error("auth", "register", f"Email '{email}' already exists")
        return False
    return True


def _validate_barangay_representative(barangay: str, role: str) -> bool:
    """
    Check if barangay already has an approved representative.
    
    Args:
        barangay: Barangay name
        role: User role (check only if 'contributor')
        
    Returns:
        True if validation passes, False if representative exists
    """
    if role != "contributor":
        return True
    
    log_query("auth", "register", f"Checking existing representative for '{barangay}'")
    existing_rep = User.query.filter_by(
        barangay=barangay, role="contributor", is_approved=True
    ).first()
    
    if existing_rep:
        log_error("auth", "register", f"Representative already exists for '{barangay}'")
        return False
    
    return True


def _create_user_from_form(username: str, email: str, password: str, role: str, barangay: Optional[str]) -> User:
    """
    Create new user from registration form data.
    
    Args:
        username: Username
        email: Email address
        password: Plain text password
        role: User role
        barangay: Barangay name (for contributors)
        
    Returns:
        Created and committed User object
    """
    log_logic("auth", "register", f"Creating new user '{username}' with role '{role}'")
    
    user = User(
        username=username,
        email=email,
        role=role,
        barangay=barangay if role == "contributor" else None,
        is_approved=(role == "user"),
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    log_success("auth", "register", f"New user '{username}' registered for barangay '{barangay}'")
    logger.info(f"New contributor user '{username}' registered for barangay '{barangay}', awaiting approval")
    
    return user


def _verify_google_token(token: str) -> Optional[Tuple[str, str]]:
    """
    Verify Google OAuth token and extract user info.
    
    Args:
        token: JWT token from Google
        
    Returns:
        Tuple of (email, name) if valid, None otherwise
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
    
    Args:
        base_username: Base username to start from
        
    Returns:
        Unique username
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
    
    Args:
        email: Google email
        name: Google display name
        
    Returns:
        Created User object or None on error
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
    
    Args:
        user: User to check
        
    Returns:
        True if allowed, False if restricted
    """
    if user.role in ["admin", "contributor"]:
        log_error("auth", "google_login", f"Role '{user.role}' restricted from Google Sign-In")
        return False
    return True


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    """
    Handle user login (clean refactored version).
    
    GET: Display login form.
    POST: Authenticate credentials and create session.
    
    Returns:
        Rendered login template or redirect after successful login
    """
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
    """
    Handle user registration (clean refactored version).
    
    Creates contributor accounts requiring admin approval.
    Validates username, email, and barangay representative uniqueness.
    
    Returns:
        Rendered registration template or redirect after successful registration
    """
    log_entry("auth", "register", method=request.method)
    logger.info("Registration page accessed")
    
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "user")
        barangay = request.form.get("barangay")
        
        log_query("auth", "register", f"Checking existence for username='{username}', email='{email}'")
        
        # Validation chain
        if not _validate_username_available(username):
            flash("Username already exists.", "error")
            return redirect(url_for("auth.register"))
        
        if not _validate_email_available(email):
            flash("Email already exists.", "error")
            return redirect(url_for("auth.register"))
        
        if not _validate_barangay_representative(barangay, role):
            flash("This Barangay already has a registered representative.", "error")
            return redirect(url_for("auth.register"))
        
        # Create user
        _create_user_from_form(username, email, password, role, barangay)
        
        if role == "contributor":
            return redirect(url_for("auth.pending_approval"))
        else:
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("auth.login"))
    
    log_render("auth", "register", "register.html")
    return render_template("auth/register.html")


@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    """
    Handle Google Sign-In (clean refactored version).
    
    Verifies JWT, creates new users or logs in existing ones.
    Restricts admin/contributor roles from Google OAuth.
    
    Returns:
        Redirect to dashboard or login page
    """
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
    """
    Log out current user and end session.
    
    Returns:
        Redirect to home page
    """
    log_entry("auth", "logout", user=current_user.username)
    logger.info("User logged out successfully")
    logout_user()
    log_redirect("auth", "logout", "home")
    return redirect(url_for("public.index"))


@auth_bp.route("/pending-approval")
def pending_approval():
    """
    Display the pending approval page for newly registered contributors.
    """
    log_entry("auth", "pending_approval")
    return render_template("auth/pending_approval.html")
