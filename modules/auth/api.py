from flask import request, jsonify
from flask_login import login_required
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

    results = []
    for user in users:
        results.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "barangay": user.barangay.name if user.barangay else "Unknown"
        })

    return jsonify(results)
