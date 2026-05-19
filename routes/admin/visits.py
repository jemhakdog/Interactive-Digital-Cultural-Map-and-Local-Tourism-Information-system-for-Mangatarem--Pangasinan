import logging
import csv
import io
from datetime import date, datetime, timedelta
from sqlalchemy import func
from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_required, current_user
from models import db, VisitorLog, Attraction, Establishment, EstablishmentReview, AttractionReview, AnalyticsPageView
from . import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route("/visits")
@login_required
def visits_index():
    """Display all visitor logs with statistics."""
    if current_user.role not in ["admin", "contributor", "business_owner"]:
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    # Filtering parameters
    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Base query
    query = VisitorLog.query
    if current_user.role != "admin":
        from sqlalchemy import or_
        if current_user.role == "business_owner":
            owned_est_ids = [e.id for e in Establishment.query.filter_by(owner_id=current_user.id).all()]
            query = query.filter(
                or_(
                    VisitorLog.logged_by == current_user.id,
                    db.and_(VisitorLog.target_type == "establishment", VisitorLog.target_id.in_(owned_est_ids))
                )
            )
        elif current_user.role == "contributor":
            stewarded_attr_ids = [a.id for a in Attraction.query.filter_by(user_id=current_user.id).all()]
            query = query.filter(
                or_(
                    VisitorLog.logged_by == current_user.id,
                    db.and_(VisitorLog.target_type == "attraction", VisitorLog.target_id.in_(stewarded_attr_ids))
                )
            )
        else:
            query = query.filter_by(logged_by=current_user.id)
    
    if target_type:
        query = query.filter_by(target_type=target_type)
    if target_id:
        query = query.filter_by(target_id=target_id)
        
    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(VisitorLog.visit_date >= parsed_start)
        except ValueError:
            pass
    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(VisitorLog.visit_date <= parsed_end)
        except ValueError:
            pass
        
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
        from sqlalchemy import or_
        if current_user.role == "business_owner":
            owned_est_ids = [e.id for e in Establishment.query.filter_by(owner_id=current_user.id).all()]
            filter_cond = or_(
                VisitorLog.logged_by == current_user.id,
                db.and_(VisitorLog.target_type == "establishment", VisitorLog.target_id.in_(owned_est_ids))
            )
        elif current_user.role == "contributor":
            stewarded_attr_ids = [a.id for a in Attraction.query.filter_by(user_id=current_user.id).all()]
            filter_cond = or_(
                VisitorLog.logged_by == current_user.id,
                db.and_(VisitorLog.target_type == "attraction", VisitorLog.target_id.in_(stewarded_attr_ids))
            )
        else:
            filter_cond = (VisitorLog.logged_by == current_user.id)
            
        stats_query = stats_query.filter(filter_cond)
        month_stats_query = month_stats_query.filter(filter_cond)
        top_loc_query = top_loc_query.filter(filter_cond)

    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, '%Y-%m-%d').date()
            stats_query = stats_query.filter(VisitorLog.visit_date >= parsed_start)
            month_stats_query = month_stats_query.filter(VisitorLog.visit_date >= parsed_start)
            top_loc_query = top_loc_query.filter(VisitorLog.visit_date >= parsed_start)
        except ValueError:
            pass
    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, '%Y-%m-%d').date()
            stats_query = stats_query.filter(VisitorLog.visit_date <= parsed_end)
            month_stats_query = month_stats_query.filter(VisitorLog.visit_date <= parsed_end)
            top_loc_query = top_loc_query.filter(VisitorLog.visit_date <= parsed_end)
        except ValueError:
            pass

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
    location_counts_query = db.session.query(
        VisitorLog.target_type,
        VisitorLog.target_id,
        func.sum(VisitorLog.visitor_count).label('count')
    )
    if current_user.role != "admin":
        location_counts_query = location_counts_query.filter(filter_cond)
    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, '%Y-%m-%d').date()
            location_counts_query = location_counts_query.filter(VisitorLog.visit_date >= parsed_start)
        except ValueError:
            pass
    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, '%Y-%m-%d').date()
            location_counts_query = location_counts_query.filter(VisitorLog.visit_date <= parsed_end)
        except ValueError:
            pass
            
    location_counts = location_counts_query.group_by(VisitorLog.target_type, VisitorLog.target_id).all()

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

    # Calculate top locations for the comparison chart (top 5 by total physical visits)
    top_5_query = db.session.query(
        VisitorLog.target_type,
        VisitorLog.target_id,
        func.sum(VisitorLog.visitor_count).label('total_visits')
    )
    if current_user.role != "admin":
        top_5_query = top_5_query.filter(filter_cond)
    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, '%Y-%m-%d').date()
            top_5_query = top_5_query.filter(VisitorLog.visit_date >= parsed_start)
        except ValueError:
            pass
    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, '%Y-%m-%d').date()
            top_5_query = top_5_query.filter(VisitorLog.visit_date <= parsed_end)
        except ValueError:
            pass
            
    top_5_result = top_5_query.group_by(VisitorLog.target_type, VisitorLog.target_id)\
     .order_by(func.sum(VisitorLog.visitor_count).desc())\
     .limit(5).all()

    comparison_chart = []
    for target_type, target_id, total_visits in top_5_result:
        temp = VisitorLog(target_type=target_type, target_id=target_id)
        name = temp.target_name
        
        # Get page views for this specific item ( sampled 50% rate )
        web_views = db.session.query(func.count(AnalyticsPageView.id))\
            .filter(
                AnalyticsPageView.view_type == target_type,
                AnalyticsPageView.item_id == target_id
            ).scalar() or 0
        
        comparison_chart.append({
            "name": name,
            "type": target_type.capitalize(),
            "visits": int(total_visits),
            "views": int(web_views)
        })

    # Fetch options for logging form (Role-based)
    form_attractions = []
    form_establishments = []
    if current_user.role == "contributor":
        form_attractions = Attraction.query.filter_by(steward_id=current_user.id).all()
        form_establishments = Establishment.query.filter_by(owner_id=current_user.id).all()
    elif current_user.role == "business_owner":
        form_attractions = []
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
        current_id=target_id,
        start_date=start_date,
        end_date=end_date,
        comparison_chart_data=comparison_chart
    )

@admin_bp.route("/visits/export")
@login_required
def export_visits():
    """Export visitor logs to CSV with dynamic filtering."""
    if current_user.role not in ["admin", "contributor", "business_owner"]:
        flash("Access denied.")
        return redirect(url_for("public.index"))

    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id')
    search = request.args.get('search')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = VisitorLog.query
    if current_user.role != "admin":
        from sqlalchemy import or_
        if current_user.role == "business_owner":
            owned_est_ids = [e.id for e in Establishment.query.filter_by(owner_id=current_user.id).all()]
            query = query.filter(
                or_(
                    VisitorLog.logged_by == current_user.id,
                    db.and_(VisitorLog.target_type == "establishment", VisitorLog.target_id.in_(owned_est_ids))
                )
            )
        elif current_user.role == "contributor":
            stewarded_attr_ids = [a.id for a in Attraction.query.filter_by(user_id=current_user.id).all()]
            query = query.filter(
                or_(
                    VisitorLog.logged_by == current_user.id,
                    db.and_(VisitorLog.target_type == "attraction", VisitorLog.target_id.in_(stewarded_attr_ids))
                )
            )
        else:
            query = query.filter_by(logged_by=current_user.id)

    if target_type:
        query = query.filter_by(target_type=target_type)
    if target_id:
        query = query.filter_by(target_id=target_id)
    if search:
        query = query.filter(VisitorLog.visitor_name.ilike(f"%{search}%"))

    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(VisitorLog.visit_date >= parsed_start)
        except ValueError:
            pass
    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(VisitorLog.visit_date <= parsed_end)
        except ValueError:
            pass

    logs = query.order_by(VisitorLog.visit_date.desc()).all()
    
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

@admin_bp.route("/visits/export/page-views")
@login_required
def export_page_views():
    """Export web page traffic analytics to CSV."""
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for("admin.visits_index"))

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    view_type = request.args.get('view_type')

    query = AnalyticsPageView.query

    if view_type:
        query = query.filter_by(view_type=view_type)

    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(AnalyticsPageView.timestamp >= parsed_start)
        except ValueError:
            pass
    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(AnalyticsPageView.timestamp < parsed_end)
        except ValueError:
            pass

    views = query.order_by(AnalyticsPageView.timestamp.desc()).all()

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Timestamp', 'View Type', 'Page Name', 'Item ID', 'Target Name', 'User ID', 'IP Address', 'Device Info'])

    for view in views:
        target_name = "N/A"
        if view.view_type in ['attraction', 'establishment'] and view.item_id:
            temp = VisitorLog(target_type=view.view_type, target_id=view.item_id)
            target_name = temp.target_name

        cw.writerow([
            view.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            view.view_type.capitalize() if view.view_type else "Page",
            view.page_name or "N/A",
            view.item_id or "N/A",
            target_name,
            view.user_id or "Anonymous",
            view.ip_address or "N/A",
            view.device_info or "N/A"
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=web_traffic_report_{date.today()}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@admin_bp.route("/visits/export/destination-insights")
@login_required
def export_destination_insights():
    """Export consolidated destination insights (performance summary) to CSV."""
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for("admin.visits_index"))

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow([
        'Destination Name', 
        'Type', 
        'Category / Subtype', 
        'Barangay', 
        'Physical Visitor Check-ins', 
        'Web Page Views', 
        'Avg Rating (1-5)', 
        'Total Reviews'
    ])

    # Fetch all Attractions
    attractions = Attraction.query.all()
    for attr in attractions:
        physical_visits = db.session.query(func.sum(VisitorLog.visitor_count))\
            .filter_by(target_type='attraction', target_id=attr.id).scalar() or 0
        
        web_views = db.session.query(func.count(AnalyticsPageView.id))\
            .filter_by(view_type='attraction', item_id=attr.id).scalar() or 0

        avg_rating = db.session.query(func.avg(AttractionReview.rating))\
            .filter_by(attraction_id=attr.id, status='approved').scalar() or 0.0
        reviews_count = db.session.query(func.count(AttractionReview.id))\
            .filter_by(attraction_id=attr.id, status='approved').scalar() or 0

        cw.writerow([
            attr.name,
            'Attraction',
            attr.category or 'N/A',
            attr.barangay.name if attr.barangay else 'General',
            int(physical_visits),
            int(web_views),
            round(float(avg_rating), 1),
            int(reviews_count)
        ])

    # Fetch all Establishments
    establishments = Establishment.query.all()
    for est in establishments:
        physical_visits = db.session.query(func.sum(VisitorLog.visitor_count))\
            .filter_by(target_type='establishment', target_id=est.id).scalar() or 0
        
        web_views = db.session.query(func.count(AnalyticsPageView.id))\
            .filter_by(view_type='establishment', item_id=est.id).scalar() or 0

        avg_rating = db.session.query(func.avg(EstablishmentReview.rating))\
            .filter_by(establishment_id=est.id, status='approved').scalar() or 0.0
        reviews_count = db.session.query(func.count(EstablishmentReview.id))\
            .filter_by(establishment_id=est.id, status='approved').scalar() or 0

        cw.writerow([
            est.name,
            'Establishment',
            est.type.capitalize() if est.type else 'N/A',
            est.barangay.name if est.barangay else 'General',
            int(physical_visits),
            int(web_views),
            round(float(avg_rating), 1),
            int(reviews_count)
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=destination_insights_report_{date.today()}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@admin_bp.route("/visits/registry")
@login_required
def visitor_registry():
    """Master table view for all detailed visitor records."""
    if current_user.role not in ["admin", "contributor", "business_owner"]:
        flash("Access denied.")
        return redirect(url_for("public.index"))

    # Filtering parameters
    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id')
    search = request.args.get('search')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = VisitorLog.query.filter(VisitorLog.visitor_name.isnot(None))

    if current_user.role != "admin":
        from sqlalchemy import or_
        if current_user.role == "business_owner":
            owned_est_ids = [e.id for e in Establishment.query.filter_by(owner_id=current_user.id).all()]
            query = query.filter(
                or_(
                    VisitorLog.logged_by == current_user.id,
                    db.and_(VisitorLog.target_type == "establishment", VisitorLog.target_id.in_(owned_est_ids))
                )
            )
        elif current_user.role == "contributor":
            stewarded_attr_ids = [a.id for a in Attraction.query.filter_by(user_id=current_user.id).all()]
            query = query.filter(
                or_(
                    VisitorLog.logged_by == current_user.id,
                    db.and_(VisitorLog.target_type == "attraction", VisitorLog.target_id.in_(stewarded_attr_ids))
                )
            )
        else:
            query = query.filter_by(logged_by=current_user.id)

    target_location = None
    if target_type and target_id:
        query = query.filter_by(target_type=target_type, target_id=target_id)
        # Fetch location name for context
        if target_type == 'attraction':
            target_location = Attraction.query.get(target_id)
        else:
            target_location = Establishment.query.get(target_id)
    
    if search:
        query = query.filter(VisitorLog.visitor_name.ilike(f"%{search}%"))

    if start_date:
        try:
            parsed_start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(VisitorLog.visit_date >= parsed_start)
        except ValueError:
            pass
    if end_date:
        try:
            parsed_end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(VisitorLog.visit_date <= parsed_end)
        except ValueError:
            pass

    logs = query.order_by(VisitorLog.visit_date.desc()).all()

    # Fetch all locations for the registry filter
    attractions = Attraction.query.all()
    establishments = Establishment.query.all()

    return render_template(
        "admin/visitor_registry.html",
        logs=logs,
        search=search,
        target_type=target_type,
        target_id=target_id,
        target_location=target_location,
        start_date=start_date,
        end_date=end_date,
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
        is_system_user = str(data.get("is_system_user")).lower() == "true"
        
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
