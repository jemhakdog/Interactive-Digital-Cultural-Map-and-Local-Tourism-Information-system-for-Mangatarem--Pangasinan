import logging
from flask import redirect, url_for, request
from flask_login import login_required
from . import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route("/documents/create/<slug>", methods=["GET", "POST"])
@login_required
def admin_document_create(slug):
    """Redirect legacy document create route to modern v1 version."""
    logger.info(f"Redirecting legacy document create for slug '{slug}' to v1.")
    return redirect(url_for("v1_docs.v1_document_create", slug=slug), code=302)

@admin_bp.route("/documents/record/<int:record_id>/edit", methods=["GET", "POST"])
@login_required
def admin_document_record_edit(record_id):
    """Redirect legacy document record edit route to modern v1 version."""
    logger.info(f"Redirecting legacy document record edit for ID {record_id} to v1.")
    return redirect(url_for("v1_docs.v1_document_record_edit", record_id=record_id), code=302)

@admin_bp.route("/documents")
@login_required
def admin_documents():
    """Redirect legacy admin documents dashboard to modern v1 version."""
    logger.info("Redirecting legacy admin documents dashboard to v1.")
    return redirect(url_for("v1_docs.v1_documents_view"), code=302)

@admin_bp.route("/documents/category/<path:category_name>")
@login_required
def admin_document_category_files(category_name):
    """Redirect legacy category files route to modern v1 version."""
    logger.info(f"Redirecting legacy category files for '{category_name}' to v1.")
    return redirect(url_for("v1_docs.v1_document_category_files", category_name=category_name), code=302)

@admin_bp.route("/documents/<slug>/files")
@login_required
def admin_document_files(slug):
    """Redirect legacy document files route to modern v1 version."""
    logger.info(f"Redirecting legacy document files for slug '{slug}' to v1.")
    return redirect(url_for("v1_docs.v1_document_files", slug=slug), code=302)

@admin_bp.route("/documents/<slug>")
@login_required
def admin_document_view(slug):
    """Redirect legacy document view route to modern v1 version."""
    logger.info(f"Redirecting legacy document view for slug '{slug}' to v1.")
    return redirect(url_for("v1_docs.v1_document_view", slug=slug), code=302)

@admin_bp.route("/documents/<slug>/edit", methods=["GET", "POST"])
@login_required
def admin_document_edit(slug):
    """Redirect legacy document edit route to modern v1 version."""
    logger.info(f"Redirecting legacy document edit for slug '{slug}' to v1.")
    return redirect(url_for("v1_docs.v1_document_edit", slug=slug), code=302)

@admin_bp.route("/documents/<slug>/export")
@login_required
def admin_document_export(slug):
    """Redirect legacy document export route to modern v1 version."""
    logger.info(f"Redirecting legacy document export for slug '{slug}' to v1.")
    return redirect(url_for("v1_docs.v1_document_export", slug=slug), code=302)

@admin_bp.route("/documents/export-all")
@login_required
def admin_documents_export_all():
    """Redirect legacy bulk export route to modern v1 version."""
    logger.info("Redirecting legacy bulk export to v1.")
    return redirect(url_for("v1_docs.v1_documents_export_all"), code=302)

@admin_bp.route("/documents/import", methods=["POST"])
@login_required
def admin_document_import():
    """Redirect legacy document import route to modern v1 version."""
    logger.info("Redirecting legacy document import to v1.")
    return redirect(url_for("v1_docs.v1_document_import"), code=302)
