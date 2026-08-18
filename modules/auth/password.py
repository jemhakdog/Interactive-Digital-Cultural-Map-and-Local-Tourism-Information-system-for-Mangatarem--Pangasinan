from flask import request, redirect, url_for, flash, render_template, current_app
from sqlalchemy import update
from extensions import db, limiter
from .models import User, PasswordResetToken
from utils.email_sender import send_password_reset_email
import logging
from utils.logger_helper import (
    log_entry,
    log_logic,
    log_success,
    log_error
)

logger = logging.getLogger(__name__)

@limiter.limit("5 per minute")
def forgot_password_view():
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
    user = User.query.filter_by(reset_token=token_str).first()
    if user:
        record = PasswordResetToken(
            user=user,
            token=user.reset_token,
            expires_at=user.reset_token_expires_at,
            used=user.reset_token_used
        )
        if record.is_valid:
            return record
    return None

def reset_password_view(token: str):
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

        # TOCTOU fix: atomically claim the token with a single UPDATE
        # that only succeeds if the token is still unused.
        stmt = (
            update(User)
            .where(User.reset_token == token, User.reset_token_used == False)
            .values(reset_token_used=True)
        )
        result = db.session.execute(stmt)
        if result.rowcount == 0:
            db.session.rollback()
            log_error("auth", "reset_password", "Token already used — possible concurrent reset")
            flash("Reset link is invalid or has expired. Please request a new one.", "error")
            return redirect(url_for("auth.forgot_password"))
        db.session.commit()

        reset_record.user.set_password(new_password)
        db.session.commit()

        log_success("auth", "reset_password", f"Password reset for user id={reset_record.user_id}")
        flash("Your password has been reset. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", token=token)
