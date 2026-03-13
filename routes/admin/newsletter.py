from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, NewsletterSubscriber
from utils.email_sender import send_email
import csv
import io
from datetime import datetime
from functools import wraps

newsletter_admin_bp = Blueprint('newsletter_admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for('public.index'))
        return f(*args, **kwargs)
    return decorated_function

@newsletter_admin_bp.route("/admin/newsletter")
@login_required
@admin_required
def index():
    """List all subscribers and show stats."""
    subscribers = NewsletterSubscriber.query.order_by(NewsletterSubscriber.created_at.desc()).all()
    active_count = NewsletterSubscriber.query.filter_by(is_active=True).count()
    return render_template("admin/newsletter/index.html", 
                           subscribers=subscribers, 
                           active_count=active_count)

@newsletter_admin_bp.route("/admin/newsletter/compose", methods=["GET", "POST"])
@login_required
@admin_required
def compose():
    """Compose and send newsletter."""
    if request.method == "POST":
        subject = request.form.get("subject")
        content = request.form.get("content")
        
        if not subject or not content:
            flash("Subject and content are required.", "error")
            return render_template("admin/newsletter/compose.html")

        subscribers = NewsletterSubscriber.query.filter_by(is_active=True).all()
        if not subscribers:
            flash("No active subscribers found.", "warning")
            return redirect(url_for("newsletter_admin.index"))

        # Send emails
        success_count = 0
        for sub in subscribers:
            # In a real app, this should be a background task (e.g., Celery)
            # For this MVP, we'll send them synchronously but with logging
            if send_email(subject, sub.email, content):
                success_count += 1
        
        flash(f"Newsletter sent successfully to {success_count} subscribers.", "success")
        return redirect(url_for("newsletter_admin.index"))

    return render_template("admin/newsletter/compose.html")

@newsletter_admin_bp.route("/admin/newsletter/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_subscriber(id):
    """Delete or deactivate a subscriber."""
    subscriber = NewsletterSubscriber.query.get_or_404(id)
    db.session.delete(subscriber)
    db.session.commit()
    flash("Subscriber removed successfully.", "success")
    return redirect(url_for("newsletter_admin.index"))

@newsletter_admin_bp.route("/admin/newsletter/export")
@login_required
@admin_required
def export_subscribers():
    """Export subscribers list as CSV."""
    from flask import Response
    
    subscribers = NewsletterSubscriber.query.all()
    
    def generate():
        data = io.StringIO()
        writer = csv.writer(data)
        writer.writerow(['Email', 'Status', 'Created At'])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        
        for sub in subscribers:
            writer.writerow([sub.email, 'Active' if sub.is_active else 'Inactive', sub.created_at])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename=f"subscribers_{datetime.now().strftime('%Y%m%d')}.csv")
    return response
