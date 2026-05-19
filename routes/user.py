from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from utils.validators import validate_form_data
from models import (
    db,
    User,
    Attraction,
    Establishment,
    Event,
    UserFavoriteAttraction,
    UserFavoriteEstablishment,
    UserEventInterest,
    AttractionReview,
    GalleryItem,
    VisitorLog,
)
from functools import wraps

user_bp = Blueprint("user", __name__, url_prefix="/user")


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "user":
            flash("Access denied. This section is for regular users only.", "error")
            return redirect(url_for("public.index"))
        return f(*args, **kwargs)

    return decorated_function


@user_bp.route("/dashboard")
@login_required
@user_required
def dashboard():
    favorite_count = UserFavoriteAttraction.query.filter_by(user_id=current_user.id).count() + \
                     UserFavoriteEstablishment.query.filter_by(user_id=current_user.id).count()
    event_interest_count = UserEventInterest.query.filter_by(
        user_id=current_user.id
    ).count()
    contribution_count = (
        AttractionReview.query.filter_by(user_id=current_user.id).count()
        + GalleryItem.query.filter_by(user_id=current_user.id).count()
    )
    visit_count = VisitorLog.query.filter_by(visitor_user_id=current_user.id).count()

    recent_favorites = (
        db.session.query(Attraction)
        .join(UserFavoriteAttraction)
        .filter(UserFavoriteAttraction.user_id == current_user.id)
        .order_by(UserFavoriteAttraction.created_at.desc())
        .limit(3)
        .all()
    )
    
    recent_fav_establishments = (
        db.session.query(Establishment)
        .join(UserFavoriteEstablishment)
        .filter(UserFavoriteEstablishment.user_id == current_user.id)
        .order_by(UserFavoriteEstablishment.created_at.desc())
        .limit(3)
        .all()
    )

    recent_visits = (
        VisitorLog.query.filter_by(visitor_user_id=current_user.id)
        .order_by(VisitorLog.visit_date.desc())
        .limit(5)
        .all()
    )

    stats = {
        "favorites": favorite_count,
        "events": event_interest_count,
        "contributions": contribution_count,
        "visits": visit_count,
    }

    return render_template(
        "user/dashboard.html", 
        stats=stats, 
        recent_favorites=recent_favorites,
        recent_fav_establishments=recent_fav_establishments,
        recent_visits=recent_visits
    )


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
@user_required
@validate_form_data({
    'username': {'type': 'string', 'min_length': 3, 'max_length': 30, 'required': True},
    'email': {'type': 'email', 'required': True}
})
def profile():
    if request.method == "POST":
        username = request.validated_data["username"]
        email = request.validated_data["email"].lower()

        # Check if username is taken by another user
        existing_user = User.query.filter(User.username == username, User.id != current_user.id).first()
        if existing_user:
            flash("Username already taken.", "error")
            return redirect(url_for("user.profile"))

        # Check if email is taken by another user
        existing_email = User.query.filter(User.email == email, User.id != current_user.id).first()
        if existing_email:
            flash("Email already registered.", "error")
            return redirect(url_for("user.profile"))

        # Save
        current_user.username = username
        current_user.email = email
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("user.profile"))

    return render_template("user/profile.html")


@user_bp.route("/favorites")
@login_required
@user_required
def favorites():
    fav_attractions = (
        db.session.query(Attraction)
        .join(UserFavoriteAttraction)
        .filter(UserFavoriteAttraction.user_id == current_user.id)
        .all()
    )
    fav_establishments = (
        db.session.query(Establishment)
        .join(UserFavoriteEstablishment)
        .filter(UserFavoriteEstablishment.user_id == current_user.id)
        .all()
    )
    return render_template(
        "user/favorites.html", 
        attractions=fav_attractions, 
        establishments=fav_establishments
    )


@user_bp.route("/favorites/toggle", methods=["POST"])
@login_required
@user_required
def toggle_favorite():
    """API endpoint to toggle favorite status for an attraction or establishment."""
    data = request.get_json()
    target_type = data.get("target_type")
    target_id = data.get("target_id")
    
    if not target_type or not target_id:
        return jsonify({"success": False, "error": "Missing parameters"}), 400
        
    if target_type == "attraction":
        fav = UserFavoriteAttraction.query.filter_by(
            user_id=current_user.id, attraction_id=target_id
        ).first()
        if fav:
            db.session.delete(fav)
            action = "removed"
        else:
            new_fav = UserFavoriteAttraction(user_id=current_user.id, attraction_id=target_id)
            db.session.add(new_fav)
            action = "added"
    elif target_type == "establishment":
        fav = UserFavoriteEstablishment.query.filter_by(
            user_id=current_user.id, establishment_id=target_id
        ).first()
        if fav:
            db.session.delete(fav)
            action = "removed"
        else:
            new_fav = UserFavoriteEstablishment(user_id=current_user.id, establishment_id=target_id)
            db.session.add(new_fav)
            action = "added"
    else:
        return jsonify({"success": False, "error": "Invalid target type"}), 400
        
    db.session.commit()
    return jsonify({"success": True, "action": action})


@user_bp.route("/favorites/ids")
@login_required
def get_favorite_ids():
    """API endpoint to get list of favorite attraction and establishment IDs for the current user."""
    fav_attractions = [f.attraction_id for f in UserFavoriteAttraction.query.filter_by(user_id=current_user.id).all()]
    fav_establishments = [f.establishment_id for f in UserFavoriteEstablishment.query.filter_by(user_id=current_user.id).all()]
    return jsonify({
        "success": True,
        "attractions": fav_attractions,
        "establishments": fav_establishments
    })


@user_bp.route("/visits/ids")
@login_required
def get_visited_ids():
    """API endpoint to get list of visited attraction and establishment IDs for the current user."""
    logs = VisitorLog.query.filter_by(visitor_user_id=current_user.id).all()
    visited_attractions = list(set([log.target_id for log in logs if log.target_type == 'attraction']))
    visited_establishments = list(set([log.target_id for log in logs if log.target_type == 'establishment']))
    return jsonify({
        "success": True,
        "attractions": visited_attractions,
        "establishments": visited_establishments
    })


@user_bp.route("/visits")
@login_required
@user_required
def visits():
    personal_visits = (
        VisitorLog.query.filter_by(visitor_user_id=current_user.id)
        .order_by(VisitorLog.visit_date.desc())
        .all()
    )
    return render_template("user/visits.html", visits=personal_visits)


@user_bp.route("/visits/log", methods=["POST"])
@login_required
@user_required
def log_personal_visit():
    """API endpoint for users to self-report a visit."""
    data = request.get_json()
    target_type = data.get("target_type") # 'attraction' or 'establishment'
    target_id = data.get("target_id")
    visit_date_str = data.get("visit_date") # YYYY-MM-DD
    notes = data.get("notes", "")
    
    if not target_type or not target_id:
        return jsonify({"success": False, "error": "Missing parameters"}), 400
        
    from datetime import datetime
    try:
        visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date() if visit_date_str else datetime.utcnow().date()
    except ValueError:
        return jsonify({"success": False, "error": "Invalid date format"}), 400

    # Create a visitor log
    # In this case, the user is logging it themselves, so logged_by = current_user.id
    # And visitor_user_id = current_user.id
    new_log = VisitorLog(
        target_type=target_type,
        target_id=target_id,
        visitor_count=1,
        visitor_name=current_user.username,
        is_system_user=True,
        visitor_user_id=current_user.id,
        logged_by=current_user.id,
        visit_date=visit_date,
        notes=notes
    )
    
    db.session.add(new_log)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Visit logged successfully!"})


@user_bp.route("/my-events")
@login_required
@user_required
def my_events():
    events = (
        db.session.query(Event)
        .join(UserEventInterest)
        .filter(UserEventInterest.user_id == current_user.id)
        .all()
    )
    return render_template("user/my_events.html", events=events)


@user_bp.route("/contributions")
@login_required
@user_required
def contributions():
    reviews = AttractionReview.query.filter_by(user_id=current_user.id).all()
    gallery_items = GalleryItem.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "user/contributions.html", reviews=reviews, gallery_items=gallery_items
    )
