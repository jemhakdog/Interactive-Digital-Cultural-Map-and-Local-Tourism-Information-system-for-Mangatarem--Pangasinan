import os
import hashlib
import hmac
import secrets
from flask import request, redirect, url_for, flash, render_template, session, current_app
from flask_login import login_user
from extensions import db, csrf
from .models import User
import logging
from utils.logger_helper import (
    log_entry,
    log_logic,
    log_success,
    log_error,
    log_render
)
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from typing import Optional, Tuple
from .login import _check_approval_status

logger = logging.getLogger(__name__)

GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com",
)

def _verify_google_token(token: str) -> Optional[Tuple[str, str]]:
    """Verify Google OAuth token and extract user info."""
    try:
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        email = idinfo.get("email")
        name = idinfo.get("name")
        log_success("auth", "google_login", f"Verified token for {email} ({name})")
        return (email, name)
    except Exception as e:
        log_error("auth", "google_login", f"Token verification failed ({type(e).__name__}): {str(e)}")
        return None

def _generate_unique_username(base_username: str) -> str:
    """Generate unique username by appending counter if needed."""
    username = base_username
    counter = 1
    while User.query.filter_by(username=username).first():
        username = f"{base_username}_{counter}"
        counter += 1
    return username

def _create_google_user(email: str, name: Optional[str], role: str) -> Optional[User]:
    """Create new user from Google OAuth data with a chosen role."""
    log_logic("auth", "google_login", f"User not found, creating new account for {email} with role {role}")
    
    if name:
        base_username = name.lower().replace(" ", "")
    else:
        base_username = email.split("@")[0]
    
    username = _generate_unique_username(base_username)
    
    try:
        user = User(
            username=username,
            email=email,
            role=role,
            is_approved=(role == "user"),
        )
        user.set_password(os.urandom(24).hex()) # Dummy password for Google users
        db.session.add(user)
        db.session.commit()
        log_success("auth", "google_login", f"Created new user '{username}' for '{email}' with role '{role}'")
        return user
    except Exception as e:
        db.session.rollback()
        log_error("auth", "google_login", f"DB Commit failed: {str(e)}")
        return None

def _check_role_restrictions(user: User) -> bool:
    """Check if user role is allowed for Google Sign-In."""
    log_logic("auth", "google_login", f"Allowing role '{user.role}' for Google Sign-In")
    return True

def _generate_oauth_nonce() -> str:
    """Generate a cryptographic nonce for Google Identity Services."""
    return secrets.token_urlsafe(32)


@csrf.exempt
def google_login_view():
    log_entry("auth", "google_login")
    try:
        return _handle_google_login()
    except Exception as e:
        logger.exception("Unhandled error in google_login_view")
        log_error("auth", "google_login", f"Unhandled error: {type(e).__name__}: {str(e)}")
        flash("Google sign-in encountered an error. Please try again.", "error")
        return redirect(url_for("auth.login"))


def _handle_google_login():
    token = request.form.get("credential")
    nonce = request.form.get("nonce")
    
    if not token:
        log_error("auth", "google_login", "No credential provided")
        flash("No Google credential received.", "error")
        return redirect(url_for("auth.login"))
    
    # Validate OAuth nonce to prevent credential replay attacks
    expected_nonce = session.pop("oauth_nonce", None)
    if not expected_nonce or not nonce or not hmac.compare_digest(expected_nonce, nonce):
        log_error("auth", "google_login", "OAuth nonce validation failed — possible replay attack")
        flash("OAuth session validation failed. Please try again.", "error")
        return redirect(url_for("auth.login"))
    
    credentials = _verify_google_token(token)
    if not credentials:
        flash("Invalid Google token. Please try again.", "error")
        return redirect(url_for("auth.login"))
    
    email, name = credentials
    user = User.query.filter_by(email=email).first()
    
    if not user:
        log_logic("auth", "google_login", f"New user '{email}' detected. Storing details and redirecting to role selection.")
        secret = current_app.config['SECRET_KEY'].encode()
        email_hmac = hmac.new(secret, email.encode(), hashlib.sha256).hexdigest()
        session['oauth_signup'] = {
            'email': email,
            'name': name,
            '_hmac': email_hmac
        }
        return redirect(url_for("auth.select_role"))
    
    if not _check_role_restrictions(user):
        flash("Google Sign-In is not allowed for this account.", "error")
        return redirect(url_for("auth.login"))
    
    if not _check_approval_status(user):
        log_logic("auth", "google_login", f"Redirecting unapproved user '{user.username}' to pending page")
        return redirect(url_for("auth.pending_approval"))
    
    log_success("auth", "google_login", f"Logging in existing user {email} (ID: {user.id})")
    login_user(user, remember=True)
    
    flash(f"Welcome back, {user.username}!", "success")
    
    if user.role == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    elif user.role == "contributor":
        return redirect(url_for("barangay.barangay_dashboard"))
    elif user.role == "business_owner":
        return redirect(url_for("business.dashboard"))
    elif user.role == "user":
        return redirect(url_for("user.dashboard"))
    
    return redirect(url_for("public.index"))

def select_role_view():
    log_entry("auth", "select_role", method=request.method)
    
    oauth_signup = session.get('oauth_signup')
    if not oauth_signup:
        log_error("auth", "select_role", "No Google session registration data found")
        flash("Google sign-in session expired. Please try again.", "error")
        return redirect(url_for("auth.login"))
    
    email = oauth_signup.get('email')
    name = oauth_signup.get('name')
    stored_hmac = oauth_signup.get('_hmac')
    
    if not email or not stored_hmac:
        log_error("auth", "select_role", "Missing email or HMAC in OAuth session")
        flash("Invalid OAuth session data. Please try again.", "error")
        return redirect(url_for("auth.login"))
    
    secret = current_app.config['SECRET_KEY'].encode()
    expected_hmac = hmac.new(secret, email.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(stored_hmac, expected_hmac):
        log_error("auth", "select_role", f"HMAC mismatch for email in session — possible session tampering")
        flash("OAuth session verification failed. Please try again.", "error")
        session.pop('oauth_signup', None)
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        # Validate CSRF token explicitly (defense-in-depth over Flask-WTF global check)
        from flask_wtf.csrf import validate_csrf
        form_csrf = request.form.get("csrf_token")
        if not form_csrf:
            log_error("auth", "select_role", "Missing CSRF token in role selection form")
            flash("Security token missing. Please try again.", "error")
            return redirect(url_for("auth.login"))
        try:
            validate_csrf(form_csrf)
        except Exception:
            log_error("auth", "select_role", "CSRF token validation failed — possible CSRF attack")
            flash("Security token invalid. Please try again.", "error")
            return redirect(url_for("auth.login"))
        
        role = request.form.get("role")
        if role not in ["user", "business_owner", "contributor"]:
            flash("Invalid role selected.", "error")
            return redirect(url_for("auth.select_role"))
        
        user = _create_google_user(email, name, role)
        if not user:
            flash("An error occurred while creating your account. Please try again.", "error")
            return redirect(url_for("auth.login"))
        
        session.pop('oauth_signup', None)
        login_user(user, remember=True)
        
        if role == "user":
            flash(f"Welcome to GoMangatarem, {name or user.username}!", "success")
            return redirect(url_for("user.dashboard"))
        
        flash("Account created! Awaiting administrator approval.", "success")
        return redirect(url_for("auth.pending_approval"))
        
    log_render("auth", "select_role", "select_role.html")
    return render_template("auth/select_role.html", email=email, name=name)
