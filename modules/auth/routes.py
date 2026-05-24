"""
Authentication routes for the Auth module.
Refactored into a Centralized Router pattern. All views are imported and attached to the Blueprint here.
"""

from flask import Blueprint
from .login import login_view, logout_view
from .register import register_view, register_business_view, pending_approval_view
from .oauth import google_login_view, select_role_view
from .password import forgot_password_view, reset_password_view
from .api import api_user_search_view

auth_bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")

# Login and Logout
auth_bp.add_url_rule("/login", view_func=login_view, methods=["GET", "POST"], endpoint="login")
auth_bp.add_url_rule("/logout", view_func=logout_view, methods=["GET", "POST"], endpoint="logout")

# Registration
auth_bp.add_url_rule("/register", view_func=register_view, methods=["GET", "POST"], endpoint="register")
auth_bp.add_url_rule("/register/business", view_func=register_business_view, methods=["GET", "POST"], endpoint="register_business")
auth_bp.add_url_rule("/pending-approval", view_func=pending_approval_view, methods=["GET"], endpoint="pending_approval")

# OAuth / Google
auth_bp.add_url_rule("/google-login", view_func=google_login_view, methods=["POST"], endpoint="google_login")
auth_bp.add_url_rule("/select-role", view_func=select_role_view, methods=["GET", "POST"], endpoint="select_role")

# Password Management
auth_bp.add_url_rule("/forgot-password", view_func=forgot_password_view, methods=["GET", "POST"], endpoint="forgot_password")
auth_bp.add_url_rule("/reset-password/<token>", view_func=reset_password_view, methods=["GET", "POST"], endpoint="reset_password")

# APIs
auth_bp.add_url_rule("/api/users/search", view_func=api_user_search_view, methods=["GET"], endpoint="api_user_search")
