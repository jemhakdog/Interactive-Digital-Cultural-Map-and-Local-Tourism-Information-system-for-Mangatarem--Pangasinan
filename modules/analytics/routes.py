from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from .models import VisitorLog
from modules.business.models import Establishment
from modules.attractions.models import Attraction
import logging

analytics_bp = Blueprint('analytics_module', __name__, url_prefix='/analytics')
logger = logging.getLogger(__name__)

@analytics_bp.route('/log-visitor/<target_type>/<int:target_id>', methods=['GET', 'POST'])
@login_required
def log_visitor(target_type, target_id):
    """Page to record a new visitor for an establishment or attraction."""
    
    # Permission Check
    target_name = "Unknown"
    if target_type == "establishment":
        target = Establishment.query.get_or_404(target_id)
        if int(target.owner_id) != int(current_user.id) and current_user.role != "admin":
            flash("Unauthorized access", "error")
            return redirect(url_for("business.dashboard"))
        target_name = target.name
    elif target_type == "attraction":
        target = Attraction.query.get_or_404(target_id)
        if int(target.user_id) != int(current_user.id) and current_user.role != "admin":
            flash("Unauthorized access", "error")
            return redirect(url_for("barangay.barangay_dashboard"))
        
        is_steward = target.user_id == current_user.id
        is_barangay_rep = (current_user.role == 'contributor' and target.barangay_id == current_user.barangay_id)
        
        if not is_steward and not is_barangay_rep and current_user.role != 'admin':
            flash("Access denied. You do not manage this attraction.", "error")
            return redirect(url_for('barangay.barangay_dashboard'))
        target_name = target.name
    else:
        flash("Invalid target type.", "error")
        return redirect(url_for('public.index'))

    if request.method == 'POST':
        visitor_name = request.form.get('visitor_name')
        visitor_age = request.form.get('visitor_age')
        visitor_address = request.form.get('visitor_address')
        is_system_user = request.form.get('is_system_user') == 'true'
        visitor_count = request.form.get('visitor_count', 1, type=int)
        notes = request.form.get('notes')

        new_log = VisitorLog(
            target_type=target_type,
            target_id=target_id,
            visitor_name=visitor_name,
            visitor_age=int(visitor_age) if visitor_age else None,
            visitor_address=visitor_address,
            is_system_user=is_system_user is True,
            visitor_count=max(1, visitor_count),
            logged_by=current_user.id,
            notes=notes
        )

        try:
            db.session.add(new_log)
            db.session.commit()
            flash(f"Visitor log for '{target_name}' recorded successfully!", "success")
            
            # Redirect back to appropriate dashboard
            if target_type == 'establishment':
                return redirect(url_for('business.dashboard'))
            else:
                return redirect(url_for('barangay.barangay_dashboard'))
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error logging visitor: {e}")
            flash("An error occurred while saving the log.", "error")

    return render_template(
        'analytics/visitor_log.html',
        target_type=target_type,
        target_id=target_id,
        target_name=target_name
    )
