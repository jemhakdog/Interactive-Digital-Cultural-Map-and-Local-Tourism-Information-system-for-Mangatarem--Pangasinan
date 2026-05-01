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
    
    # Check if already subscribed
    existing = NewsletterSubscriber.query.filter_by(email=email).first()
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.session.commit()
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
        new_subscriber = NewsletterSubscriber(email=email)
        db.session.add(new_subscriber)
        db.session.commit()
        
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
