import logging
from flask import Blueprint, request, jsonify, flash, redirect, url_for
from extensions import db
from modules.notifications.models import NewsletterSubscriber
from utils.validators import validate_form_data

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")
logger = logging.getLogger(__name__)

@notifications_bp.route("/subscribe", methods=["POST"])
@validate_form_data({
    'email': {'type': 'email', 'required': True}
})
def subscribe():
    """
    Handle newsletter subscription requests.
    """
    email = request.validated_data['email']
    from modules.auth.models import User
    
    # Check if user exists to link to subscription
    user = User.query.filter_by(email=email).first()
    user_id = user.id if user else None
    
    # Check if already subscribed
    existing = NewsletterSubscriber.query.filter_by(email=email).first()
    if existing:
        if not existing.is_active or existing.user_id != user_id:
            existing.is_active = True
            existing.user_id = user_id
            db.session.commit()
            
            try:
                from utils.email_sender import send_newsletter_thankyou_email
                send_newsletter_thankyou_email(email)
            except Exception as mail_err:
                logger.error(f"Failed to send resubscribe email to {email}: {mail_err}")

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"status": "success", "message": "Welcome back! You've been resubscribed."})
            flash("Welcome back! You've been resubscribed.", "success")
            return redirect(url_for("public.index"))
        
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"status": "info", "message": "You are already subscribed!"})
        flash("You are already subscribed!", "info")
        return redirect(url_for("public.index"))

    # Create new subscriber
    try:
        new_subscriber = NewsletterSubscriber(email=email, user_id=user_id)
        db.session.add(new_subscriber)
        db.session.commit()
        
        try:
            from utils.email_sender import send_newsletter_thankyou_email
            send_newsletter_thankyou_email(email)
        except Exception as mail_err:
            logger.error(f"Failed to send welcome email to {email}: {mail_err}")
        
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"status": "success", "message": "Thank you for subscribing to our newsletter!"})
        flash("Thank you for subscribing to our newsletter!", "success")
        return redirect(url_for("public.index"))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Subscription error: {e}")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"status": "error", "message": "An error occurred. Please try again later."}), 500
        flash("An error occurred. Please try again later.", "error")
        return redirect(url_for("public.index"))


from flask_login import login_required, current_user
from modules.notifications.models import UserNotification

@notifications_bp.route("/mark-read", methods=["POST"])
@login_required
def mark_all_read():
    """Mark all unread notifications of current user as read."""
    try:
        unread = UserNotification.query.filter_by(user_id=current_user.id, is_read=False).all()
        for notification in unread:
            notification.is_read = True
        db.session.commit()
        return jsonify({"status": "success", "message": "All notifications marked as read."})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking notifications as read: {e}")
        return jsonify({"status": "error", "message": "An error occurred."}), 500


@notifications_bp.route("/mark-read/<int:id>", methods=["POST"])
@login_required
def mark_single_read(id):
    """Mark a single notification of current user as read."""
    try:
        notification = UserNotification.query.filter_by(id=id, user_id=current_user.id).first_or_404()
        notification.is_read = True
        db.session.commit()
        return jsonify({"status": "success", "message": "Notification marked as read."})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking notification as read: {e}")
        return jsonify({"status": "error", "message": "An error occurred."}), 500

