"""
Admin heritage routes — CRUD for all 5 heritage types.

Admin-only, auto-approved on creation. Uses unified type-based routing
via the heritage registry to avoid code duplication.
"""
import json
import logging
from datetime import date, datetime

from flask import render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from extensions import db, limiter
from models import HeritageProfile
from utils.heritage_registry import (
    HERITAGE_TYPES,
    get_heritage_config,
    get_all_types,
    get_display_name,
)
from utils.logger_helper import log_entry, log_success, log_error
from . import admin_bp

logger = logging.getLogger(__name__)


def _require_admin():
    """Abort with 403 if current user is not admin."""
    if current_user.role != "admin":
        log_error("admin", "heritage", "Access denied — not admin")
        abort(403)


def _parse_form_value(value, field_type):
    """Parse a form value based on field type."""
    if not value or value.strip() == "":
        return None

    if field_type == "number":
        try:
            return float(value) if "." in value else int(value)
        except (ValueError, TypeError):
            return None
    elif field_type == "date":
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None
    elif field_type == "json":
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    else:
        return value.strip()


def _populate_item_from_form(profile, detail, config, form_data):
    """Populate both profile and detail models from form data."""
    for field_name, label, field_type, required in config["fields"]:
        raw_value = form_data.get(field_name, "")
        parsed = _parse_form_value(raw_value, field_type)
        
        # Determine whether the field belongs to HeritageProfile or the detail model
        if hasattr(HeritageProfile, field_name) and field_name not in ["id"]:
            setattr(profile, field_name, parsed)
        else:
            setattr(detail, field_name, parsed)


def _item_to_dict(profile, detail, config):
    """Convert a heritage item (profile + detail) to a serializable dictionary."""
    result = {
        "id": profile.id,
        "status": profile.status,
        "created_at": profile.created_at.isoformat() if profile.created_at else None,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
        "user_id": profile.user_id,
        "asset_type": profile.asset_type
    }

    for field_name, label, field_type, required in config["fields"]:
        if hasattr(HeritageProfile, field_name) and field_name not in ["id"]:
            value = getattr(profile, field_name, None)
        else:
            value = getattr(detail, field_name, None)
            
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        result[field_name] = value

    return result


class ProxyItem:
    """A proxy object to allow templates to access fields seamlessly whether they are on profile or detail."""
    def __init__(self, profile, detail):
        self.profile = profile
        self.detail = detail
        
    def __getattr__(self, name):
        if hasattr(self.detail, name):
            return getattr(self.detail, name)
        elif hasattr(self.profile, name):
            return getattr(self.profile, name)
        raise AttributeError(f"ProxyItem has no attribute '{name}'")


# === Dashboard ===

@admin_bp.route("/heritage")
@login_required
def admin_heritage_dashboard():
    """Overview of all heritage types with submission counts."""
    log_entry("admin", "heritage_dashboard")
    _require_admin()

    type_stats = []
    for slug, config in get_all_types():
        total = HeritageProfile.query.filter_by(asset_type=slug).count()
        approved = HeritageProfile.query.filter_by(asset_type=slug, status="approved").count()
        pending = HeritageProfile.query.filter_by(asset_type=slug, status="pending").count()
        type_stats.append({
            "slug": slug,
            "label": config["label"],
            "label_plural": config["label_plural"],
            "form": config["form"],
            "total": total,
            "approved": approved,
            "pending": pending,
        })

    log_success("admin", "heritage_dashboard", f"Loaded stats for {len(type_stats)} types")
    return render_template(
        "admin/heritage_dashboard.html",
        type_stats=type_stats,
        heritage_types=HERITAGE_TYPES,
    )


# === List ===

@admin_bp.route("/heritage/<heritage_type>")
@login_required
def admin_heritage_list(heritage_type):
    """List all entries for a specific heritage type."""
    log_entry("admin", "heritage_list", heritage_type=heritage_type)
    _require_admin()

    config = get_heritage_config(heritage_type)
    if not config:
        abort(404)

    model = config["model"]
    # Get all profiles of this type, join with detail, order by profile's created_at
    profiles = HeritageProfile.query.filter_by(asset_type=heritage_type).order_by(HeritageProfile.created_at.desc()).all()
    
    # We load details sequentially or use a joinedload. Since this is admin, a simple lookup is fine.
    # To keep template compatible, we yield proxy objects.
    items = []
    for p in profiles:
        # The relationship is usually dynamically named or we can query it
        # The PK of the detail model is usually profile_id
        detail = model.query.get(p.id)
        if detail:
            items.append(ProxyItem(p, detail))

    log_success("admin", "heritage_list", f"Loaded {len(items)} {config['label']} entries")
    return render_template(
        "admin/heritage_list.html",
        items=items,
        heritage_type=heritage_type,
        config=config,
    )


# === Add (auto-approved) ===

@admin_bp.route("/heritage/<heritage_type>/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def admin_heritage_add(heritage_type):
    """Create a new heritage entry. Auto-approved since admin creates it."""
    log_entry("admin", "heritage_add", heritage_type=heritage_type, method=request.method)
    _require_admin()

    config = get_heritage_config(heritage_type)
    if not config:
        abort(404)

    if request.method == "POST":
        model = config["model"]
        
        # Create base profile
        profile = HeritageProfile(
            asset_type=heritage_type,
            status="approved",
            user_id=current_user.id
        )
        db.session.add(profile)
        db.session.flush() # To get the profile.id
        
        # Create detail model
        detail = model(heritage_profile_id=profile.id)
        _populate_item_from_form(profile, detail, config, request.form)
        
        db.session.add(detail)
        db.session.commit()

        display_name = get_display_name(detail, heritage_type)
        log_success("admin", "heritage_add", f"Created {config['label']}: '{display_name}'")
        flash(f'{config["label"]} "{display_name}" created successfully!')
        return redirect(url_for("admin.admin_heritage_list", heritage_type=heritage_type))

    return render_template(
        "admin/heritage_form.html",
        heritage_type=heritage_type,
        config=config,
        item=None,
        is_edit=False,
    )


# === Edit ===

@admin_bp.route("/heritage/<heritage_type>/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def admin_heritage_edit(heritage_type, item_id):
    """Edit an existing heritage entry."""
    log_entry("admin", "heritage_edit", heritage_type=heritage_type, id=item_id, method=request.method)
    _require_admin()

    config = get_heritage_config(heritage_type)
    if not config:
        abort(404)

    model = config["model"]
    profile = HeritageProfile.query.get_or_404(item_id)
    if profile.asset_type != heritage_type:
        abort(404)
        
    detail = model.query.get_or_404(item_id)
    proxy_item = ProxyItem(profile, detail)

    if request.method == "POST":
        _populate_item_from_form(profile, detail, config, request.form)
        db.session.commit()

        display_name = get_display_name(detail, heritage_type)
        log_success("admin", "heritage_edit", f"Updated {config['label']}: '{display_name}'")
        flash(f'{config["label"]} "{display_name}" updated successfully!')
        return redirect(url_for("admin.admin_heritage_list", heritage_type=heritage_type))

    return render_template(
        "admin/heritage_form.html",
        heritage_type=heritage_type,
        config=config,
        item=proxy_item,
        is_edit=True,
    )


# === Delete ===

@admin_bp.route("/heritage/<heritage_type>/delete/<int:item_id>", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def admin_heritage_delete(heritage_type, item_id):
    """Delete a heritage entry."""
    log_entry("admin", "heritage_delete", heritage_type=heritage_type, id=item_id)
    _require_admin()

    config = get_heritage_config(heritage_type)
    if not config:
        abort(404)

    model = config["model"]
    profile = HeritageProfile.query.get_or_404(item_id)
    detail = model.query.get(item_id)
    
    display_name = get_display_name(detail, heritage_type) if detail else f"Profile {item_id}"

    if detail:
        db.session.delete(detail)
    db.session.delete(profile)
    db.session.commit()

    log_success("admin", "heritage_delete", f"Deleted {config['label']}: '{display_name}'")
    flash(f'{config["label"]} "{display_name}" deleted.')
    return redirect(url_for("admin.admin_heritage_list", heritage_type=heritage_type))


# === API-style JSON endpoints (for AJAX / future frontend) ===

@admin_bp.route("/heritage/<heritage_type>/json")
@login_required
def admin_heritage_json(heritage_type):
    """Return heritage items as JSON (for AJAX tables, datatables, etc.)."""
    _require_admin()

    config = get_heritage_config(heritage_type)
    if not config:
        return jsonify({"error": "Invalid heritage type"}), 404

    model = config["model"]
    profiles = HeritageProfile.query.filter_by(asset_type=heritage_type).order_by(HeritageProfile.created_at.desc()).all()
    
    json_items = []
    for p in profiles:
        detail = model.query.get(p.id)
        if detail:
            json_items.append(_item_to_dict(p, detail, config))

    return jsonify({
        "heritage_type": heritage_type,
        "label": config["label"],
        "count": len(json_items),
        "items": json_items,
    })
