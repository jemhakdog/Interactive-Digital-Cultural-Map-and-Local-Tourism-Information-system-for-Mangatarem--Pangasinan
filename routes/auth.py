from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from extensions import limiter  # Import from shared extensions
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from datetime import datetime
import logging

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    """
    Handle user login.

    GET: Display login form.
    POST: Authenticate user credentials and create session.

    Contributor users must be approved by admin before they can log in.

    Returns:
        GET: Rendered login template.
        POST: Redirect to home page on success, or login page with error.
    """
    print(f"[PROGRESSIVE LOG] [auth] > login > ENTRY: method={request.method}")
    logger.info("Login page accessed")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"[PROGRESSIVE LOG] [auth] > login > QUERY: Fetching user '{username}'")
        user = User.query.filter_by(username=username).first()
        if user:
            print(
                f"[PROGRESSIVE LOG] [auth] > login > LOGIC: Found user '{username}' with role '{user.role}'"
            )

        if user and user.check_password(password):
            print(
                f"[PROGRESSIVE LOG] [auth] > login > LOGIC: Password check successful for '{username}'"
            )
            if user.role == "contributor" and not user.is_approved:
                print(
                    f"[PROGRESSIVE LOG] [auth] > login > LOGIC: Contributor '{username}' pending approval"
                )
                flash("Your account is pending approval by the admin.", "warning")
                return redirect(url_for("auth.login"))

            print(
                f"[PROGRESSIVE LOG] [auth] > login > SUCCESS: User '{username}' logged in"
            )
            logger.info(
                f"User '{username}' with role '{user.role}' logged in successfully"
            )
            login_user(user)
            return redirect(url_for("public.index"))
        print(
            f"[PROGRESSIVE LOG] [auth] > login > ERROR: Invalid credentials for '{username}'"
        )
        flash("Invalid username or password", "error")
    print("[PROGRESSIVE LOG] [auth] > login > RENDER: Rendering login.html")
    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():
    """
    Handle new user registration for barangay contributors.

    Creates a new contributor account that requires admin approval.
    Validates that username and email are unique.

    Returns:
        GET: Rendered registration template.
        POST: Redirect to login page with confirmation message.
    """
    print(f"[PROGRESSIVE LOG] [auth] > register > ENTRY: method={request.method}")
    logger.info("Registration page accessed")

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "user")
        barangay = request.form.get("barangay")

        print(
            f"[PROGRESSIVE LOG] [auth] > register > QUERY: Checking existence for username='{username}', email='{email}'"
        )
        if User.query.filter_by(username=username).first():
            print(
                f"[PROGRESSIVE LOG] [auth] > register > ERROR: Username '{username}' already exists"
            )
            flash("Username already exists.", "error")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            print(
                f"[PROGRESSIVE LOG] [auth] > register > ERROR: Email '{email}' already exists"
            )
            flash("Email already exists.", "error")
            return redirect(url_for("auth.register"))

        # Enforce one contributor per barangay ONLY if selected role is contributor
        if role == "contributor":
            print(
                f"[PROGRESSIVE LOG] [auth] > register > QUERY: Checking existing representative for '{barangay}'"
            )
            existing_rep = User.query.filter_by(
                barangay=barangay, role="contributor", is_approved=True
            ).first()
            if existing_rep:
                print(
                    f"[PROGRESSIVE LOG] [auth] > register > ERROR: Representative already exists for '{barangay}'"
                )
                flash("This Barangay already has a registered representative.", "error")
                return redirect(url_for("auth.register"))

        print(
            f"[PROGRESSIVE LOG] [auth] > register > LOGIC: Creating new user '{username}' with role '{role}'"
        )
        user = User(
            username=username,
            email=email,
            role=role,
            barangay=barangay if role == "contributor" else None,
            is_approved=(role == "user"),  # Auto-approve regular users
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        print(
            f"[PROGRESSIVE LOG] [auth] > register > SUCCESS: New user '{username}' registered for barangay '{barangay}'"
        )
        logger.info(
            f"New contributor user '{username}' registered for barangay '{barangay}', awaiting approval"
        )

        if role == "contributor":
            flash("Registration successful! Please wait for admin approval.", "success")
        else:
            flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    print("[PROGRESSIVE LOG] [auth] > register > RENDER: Rendering register.html")
    return render_template("auth/register.html")


@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    """
    Handle Google Sign-In response.
    Verifies the JWT and either logs in the existing user or creates a new one.
    """
    print("[PROGRESSIVE LOG] [auth] > google_login > ENTRY")
    token = request.form.get("credential")
    print(f"[PROGRESSIVE LOG] [auth] > google_login > QUERY: Received token: {token}")
    print(
        f"[PROGRESSIVE LOG] [auth] > google_login > QUERY: Received method: {request.method}"
    )
    print(
        f"[PROGRESSIVE LOG] [auth] > google_login > QUERY: Received form: {request.form}"
    )

    if not token:
        print("[PROGRESSIVE LOG] [auth] > google_login > ERROR: No credential provided")
        flash("No Google credential received.", "error")
        return redirect(url_for("auth.login"))

    try:
        # Client ID from the provided secret file
        CLIENT_ID = (
            "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com"
        )
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), CLIENT_ID
        )

        email = idinfo.get("email")
        # name = idinfo.get("name") # Currently unused
        print(
            f"[PROGRESSIVE LOG] [auth] > google_login > SUCCESS: Verified token for {email}"
        )

        user = User.query.filter_by(email=email).first()

        if not user:
            print(
                f"[PROGRESSIVE LOG] [auth] > google_login > LOGIC: Creating new user for {email}"
            )
            # Generate a username if not already exists
            username = email.split("@")[0]
            if User.query.filter_by(username=username).first():
                username = f"{username}_{int(datetime.utcnow().timestamp())}"

            user = User(
                username=username,
                email=email,
                role="user",
                is_approved=True,  # Regular users don't need approval
            )
            db.session.add(user)
            db.session.commit()
            print(
                f"[PROGRESSIVE LOG] [auth] > google_login > SUCCESS: Created and logging in {email}"
            )
            login_user(user)
            return redirect(url_for("public.index"))

        # Explicitly restrict Google Sign-In to the 'user' role
        if user.role in ["admin", "contributor"]:
            print(
                f"[PROGRESSIVE LOG] [auth] > google_login > ERROR: Role '{user.role}' restricted from Google Sign-In"
            )
            flash(
                "Google Sign-In is only available for regular users. Please log in with your credentials.",
                "error",
            )
            return redirect(url_for("auth.login"))

        print(f"[PROGRESSIVE LOG] [auth] > google_login > SUCCESS: Logging in {email}")
        login_user(user)
        return redirect(url_for("public.index"))

    except ValueError as e:
        print(f"[PROGRESSIVE LOG] [auth] > google_login > ERROR: {str(e)}")
        flash("Invalid Google token.", "error")
        return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Log out the current user and end their session.

    Returns:
        Redirect to home page.
    """
    print(f"[PROGRESSIVE LOG] [auth] > logout > ENTRY: user='{current_user.username}'")
    logger.info("User logged out successfully")
    logout_user()
    print("[PROGRESSIVE LOG] [auth] > logout > REDIRECT: Redirecting to home")
    return redirect(url_for("public.index"))
