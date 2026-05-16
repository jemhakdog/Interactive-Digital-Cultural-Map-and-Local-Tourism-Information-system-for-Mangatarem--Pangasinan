import logging
import csv
import io
from datetime import date
from sqlalchemy import func
from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_required, current_user
from models import db, VisitorLog, Attraction, Establishment
from . import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route("/visits")
@login_required
def visits_index():
    """Display all visitor logs with statistics."""
    if current_user.role not in ["admin", "contributor"]:
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    # Filtering parameters
    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id')
    
    # Base query
    query = VisitorLog.query
    if current_user.role != "admin":
        query = query.filter_by(logged_by=current_user.id)
    
    if target_type:
        query = query.filter_by(target_type=target_type)
    if target_id:
        query = query.filter_by(target_id=target_id)
        
    logs = query.order_by(VisitorLog.visit_date.desc()).all()
    
    # Get all potential targets for filtering
    attractions = Attraction.query.all()
    establishments = Establishment.query.all()
    
    # Calculate Statistics (Admin sees global, Contributor sees theirs)
    stats_query = db.session.query(func.sum(VisitorLog.visitor_count))
    month_stats_query = db.session.query(func.sum(VisitorLog.visitor_count))
    top_loc_query = db.session.query(
        VisitorLog.target_type, 
        VisitorLog.target_id, 
        func.sum(VisitorLog.visitor_count).label('total')
    )

    if current_user.role != "admin":
        stats_query = stats_query.filter(VisitorLog.logged_by == current_user.id)
        month_stats_query = month_stats_query.filter(VisitorLog.logged_by == current_user.id)
        top_loc_query = top_loc_query.filter(VisitorLog.logged_by == current_user.id)

    total_visitors = stats_query.scalar() or 0
    
    # This month's total
    first_of_month = date.today().replace(day=1)
    month_total = month_stats_query.filter(VisitorLog.visit_date >= first_of_month).scalar() or 0
        
    # Top Location
    top_loc_result = top_loc_query.group_by(VisitorLog.target_type, VisitorLog.target_id)\
     .order_by(func.sum(VisitorLog.visitor_count).desc()).first()
    
    top_location = "N/A"
    if top_loc_result:
        temp_log = VisitorLog(target_type=top_loc_result[0], target_id=top_loc_result[1])
        top_location = temp_log.target_name

    stats = {
        "total": total_visitors,
        "month_total": month_total,
        "top_location": top_location
    }

    # Location Statistics for the "Audits" section
    # Group by target_type and target_id to get counts for all locations
    location_counts = db.session.query(
        VisitorLog.target_type,
        VisitorLog.target_id,
        func.sum(VisitorLog.visitor_count).label('count')
    ).group_by(VisitorLog.target_type, VisitorLog.target_id).all()

    # Build a list of locations with their metadata and counts
    location_stats = []
    for type_, id_, count in location_counts:
        # Create a dummy log to get the target_name easily using our property
        temp = VisitorLog(target_type=type_, target_id=id_)
        location_stats.append({
            'name': temp.target_name,
            'type': type_,
            'id': id_,
            'count': count
        })
    
    # Sort by count descending
    location_stats.sort(key=lambda x: x['count'], reverse=True)

    # Fetch options for logging form (Role-based)
    form_attractions = []
    form_establishments = []
    if current_user.role == "contributor":
        form_attractions = Attraction.query.filter_by(steward_id=current_user.id).all()
        form_establishments = Establishment.query.filter_by(owner_id=current_user.id).all()
    else:
        form_attractions = attractions
        form_establishments = establishments
        
    return render_template(
        "admin/visits.html", 
        logs=logs,
        stats=stats,
        location_stats=location_stats,
        attractions=form_attractions,
        establishments=form_establishments,
        all_attractions=attractions,
        all_establishments=establishments,
        current_type=target_type,
        current_id=target_id
    )

@admin_bp.route("/visits/export")
@login_required
def export_visits():
    """Export visitor logs to CSV."""
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for("admin.visits_index"))

    logs = VisitorLog.query.order_by(VisitorLog.visit_date.desc()).all()
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Location', 'Type', 'Visitors', 'Visitor Name', 'Age', 'Address', 'App User?', 'Notes', 'Logged By'])
    
    for log in logs:
        cw.writerow([
            log.visit_date,
            log.target_name,
            log.target_type.capitalize(),
            log.visitor_count,
            log.visitor_name or "N/A",
            log.visitor_age or "N/A",
            log.visitor_address or "N/A",
            "Yes" if log.is_system_user else "No",
            log.notes or "",
            log.steward.username
        ])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=visitor_report_{date.today()}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@admin_bp.route("/visits/registry")
@login_required
def visitor_registry():
    """Master table view for all detailed visitor records."""
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for("admin.visits_index"))

    # Filtering parameters
    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id')
    search = request.args.get('search')

    query = VisitorLog.query.filter(VisitorLog.visitor_name != None)

    target_location = None
    if target_type and target_id:
        query = query.filter_by(target_type=target_type, target_id=target_id)
        # Fetch location name for context
        if target_type == 'attraction':
            from modules.attractions.models import Attraction
            target_location = Attraction.query.get(target_id)
        else:
            from modules.business.models import Establishment
            target_location = Establishment.query.get(target_id)
    
    if search:
        query = query.filter(VisitorLog.visitor_name.ilike(f"%{search}%"))

    logs = query.order_by(VisitorLog.visit_date.desc()).all()

    # Fetch all locations for the registry filter
    from modules.attractions.models import Attraction
    from modules.business.models import Establishment
    attractions = Attraction.query.all()
    establishments = Establishment.query.all()

    return render_template(
        "admin/visitor_registry.html",
        logs=logs,
        search=search,
        target_type=target_type,
        target_id=target_id,
        target_location=target_location,
        all_attractions=attractions,
        all_establishments=establishments
    )

@admin_bp.route("/visits/log", methods=["POST"])
@login_required
def log_visit():
    """API endpoint to log a visitor check-in."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        target_type = data.get("target_type")
        target_id = data.get("target_id")
        visitor_count = int(data.get("visitor_count", 1))
        visit_date = data.get("visit_date")
        notes = data.get("notes")
        
        # Detailed Visitor Data
        visitor_name = data.get("visitor_name")
        visitor_age = data.get("visitor_age")
        visitor_address = data.get("visitor_address")
        is_system_user = data.get("is_system_user") == "true" or data.get("is_system_user") == True
        
        if not target_type or not target_id:
            return jsonify({"success": False, "error": "Missing target information"}), 400
            
        new_log = VisitorLog(
            target_type=target_type,
            target_id=target_id,
            visitor_count=visitor_count,
            visitor_name=visitor_name,
            visitor_age=int(visitor_age) if visitor_age and str(visitor_age).isdigit() else None,
            visitor_address=visitor_address,
            is_system_user=is_system_user,
            logged_by=current_user.id,
            notes=notes
        )
        
        if visit_date:
            from datetime import datetime
            new_log.visit_date = datetime.strptime(visit_date, '%Y-%m-%d').date()
            
        db.session.add(new_log)
        db.session.commit()
        
        if request.is_json:
            return jsonify({"success": True, "message": "Visit logged successfully"})
        
        flash("Visit logged successfully.")
        return redirect(url_for("admin.visits_index"))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error logging visit: {e}")
        if request.is_json:
            return jsonify({"success": False, "error": str(e)}), 500
        flash(f"Error: {e}")
        return redirect(url_for("admin.visits_index"))
