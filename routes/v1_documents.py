import os
import logging
from datetime import datetime
from flask import Blueprint, render_template, request, send_from_directory
from flask_login import login_required, current_user

# Import constants and helpers from the original documents module
from .admin.documents import (
    FORM_MAPPING, 
    GATHERED_DIR, 
    _load_all_forms,
    _require_admin
)

# Create the v1 documents blueprint
v1_docs_bp = Blueprint("v1_docs", __name__, url_prefix="/admin")
logger = logging.getLogger(__name__)

def _get_icon_for_cat(category):
    """Return an icon name based on category."""
    cat_lower = category.lower()
    if "natural" in cat_lower: 
        return "folder"
    if "built" in cat_lower: 
        return "image"
    if "archaeological" in cat_lower: 
        return "camera"
    return "folder"

@v1_docs_bp.route("/v1/documents")
@login_required
def v1_documents_view():
    """
    Modernized version of the documents management page (v1).
    Uses real data from the original documents system.
    """
    admin_check = _require_admin()
    if admin_check:
        return admin_check
        
    search_query = request.args.get('q', '').strip().lower()
    logger.info(f"V1 Documents page accessed by user {current_user.username}. Search: {search_query}")
    
    # 1. Load data from original system
    _load_all_forms()
    
    # Fetch recent heritage records
    from models import HeritageProfile
    from extensions import db
    from sqlalchemy import func
    
    # Get entry counts per asset type
    entry_counts = db.session.query(
        HeritageProfile.asset_type, 
        func.count(HeritageProfile.id)
    ).group_by(HeritageProfile.asset_type).all()
    entry_map = {t: c for t, c in entry_counts if t}
    
    # Fetch recent records for the dashboard
    records = HeritageProfile.query.filter(HeritageProfile.template_slug.isnot(None))\
                                 .order_by(HeritageProfile.created_at.desc())\
                                 .limit(10).all()
    
    # Get all docx files and their stats
    docx_files_stats = []
    if os.path.exists(GATHERED_DIR):
        for f in os.listdir(GATHERED_DIR):
            if f.endswith('.docx'):
                if search_query and search_query not in f.lower():
                    continue
                    
                f_path = os.path.join(GATHERED_DIR, f)
                try:
                    stats = os.stat(f_path)
                    docx_files_stats.append({
                        "name": f,
                        "mtime": stats.st_mtime,
                        "size_kb": round(stats.st_size / 1024, 1),
                        "updated_at": datetime.fromtimestamp(stats.st_mtime).strftime('%b %d, %Y')
                    })
                except OSError:
                    continue
    
    # Sort files by modification time descending
    docx_files_stats.sort(key=lambda x: x["mtime"], reverse=True)
    
    # Process folders (Categories)
    folders_map = {}
    for _, meta in FORM_MAPPING.items():
        cat = meta["category"]
        h_type = meta.get("heritage_type")
        if cat not in folders_map:
            folders_map[cat] = {
                "count": 0, 
                "entries": entry_map.get(h_type, 0) if h_type else 0,
                "icon": _get_icon_for_cat(cat)
            }
        folders_map[cat]["count"] += 1

    # Format folders for template (Folders Details)
    folder_list = []
    for name, info in folders_map.items():
        folder_list.append({
            "name": name,
            "count": info["count"],
            "entries": info["entries"],
            "icon": info["icon"],
            "users": ["BS"]
        })

    # Process documents for the table
    doc_list = []
    for stats in docx_files_stats[:20]:
        label = stats["name"]
        slug = None
        is_shared = False
        for s, meta in FORM_MAPPING.items():
            if meta["file"].split('.')[0] in stats["name"]:
                label = meta["label"]
                slug = s
                is_shared = True
                break
        
        doc_list.append({
            "id": stats["mtime"], 
            "name": stats["name"],
            "label": label,
            "slug": slug,
            "modified": stats["updated_at"],
            "access": "Shared" if is_shared else "Only you",
            "users": ["BS", "JD"] if is_shared else ["BS"]
        })
    
    return render_template(
        "admin/documents_v1.html",
        folders=folder_list,
        documents=doc_list,
        records=records,
        search_query=search_query,
        form_mapping=FORM_MAPPING
    )

@v1_docs_bp.route("/v1/documents/download/<filename>")
@login_required
def v1_document_download(filename):
    """Directly download a docx file."""
    admin_check = _require_admin()
    if admin_check:
        return admin_check
    return send_from_directory(GATHERED_DIR, filename, as_attachment=True)
