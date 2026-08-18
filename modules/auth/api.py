from flask import request, jsonify
from flask_login import login_required, current_user
from .models import User

@login_required
def api_user_search_view():
    """API for searching users to auto-fill visitor logs."""
    query = request.args.get("q", "").strip()
    if not query or len(query) < 2:
        return jsonify([])

    # Only search for approved 'user' role accounts
    users = User.query.filter(
        User.role == "user",
        User.is_approved
    ).filter(
        (User.username.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
    ).limit(5).all()

    is_privileged = current_user.role in ("admin", "contributor")

    results = []
    for user in users:
        entry = {
            "id": user.id,
            "username": user.username,
            "barangay": user.barangay.name if user.barangay else "Unknown"
        }
        if is_privileged:
            entry["email"] = user.email
        results.append(entry)

    return jsonify(results)
