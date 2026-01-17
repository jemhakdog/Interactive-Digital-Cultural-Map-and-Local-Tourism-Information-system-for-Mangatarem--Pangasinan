from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import (
    db,
    Attraction,
    Event,
    Favorite,
    EventInterest,
    Review,
    GalleryItem,
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
    favorite_count = Favorite.query.filter_by(user_id=current_user.id).count()
    event_interest_count = EventInterest.query.filter_by(
        user_id=current_user.id
    ).count()
    contribution_count = (
        Review.query.filter_by(user_id=current_user.id).count()
        + GalleryItem.query.filter_by(user_id=current_user.id).count()
    )

    recent_favorites = (
        db.session.query(Attraction)
        .join(Favorite)
        .filter(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
        .limit(5)
        .all()
    )

    stats = {
        "favorites": favorite_count,
        "events": event_interest_count,
        "contributions": contribution_count,
    }

    return render_template(
        "user/dashboard.html", stats=stats, recent_favorites=recent_favorites
    )


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
@user_required
def profile():
    if request.method == "POST":
        current_user.username = request.form.get("username")
        current_user.email = request.form.get("email")
        # In a real app, handle profile picture and password updates here
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("user.profile"))

    return render_template("user/profile.html")


@user_bp.route("/favorites")
@login_required
@user_required
def favorites():
    favorites = (
        db.session.query(Attraction)
        .join(Favorite)
        .filter(Favorite.user_id == current_user.id)
        .all()
    )
    return render_template("user/favorites.html", favorites=favorites)


@user_bp.route("/my-events")
@login_required
@user_required
def my_events():
    events = (
        db.session.query(Event)
        .join(EventInterest)
        .filter(EventInterest.user_id == current_user.id)
        .all()
    )
    return render_template("user/my_events.html", events=events)


@user_bp.route("/contributions")
@login_required
@user_required
def contributions():
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    gallery_items = GalleryItem.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "user/contributions.html", reviews=reviews, gallery_items=gallery_items
    )
