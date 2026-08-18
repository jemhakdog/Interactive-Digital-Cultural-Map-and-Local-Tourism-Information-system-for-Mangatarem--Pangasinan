"""
Shared file-upload utilities.

Centralizes allowed-extension checks and file-save logic that was
previously duplicated across admin.py and barangay.py.
"""

import os
import logging
from typing import Optional
from flask import current_app, url_for
from werkzeug.utils import secure_filename
from utils.security import sanitize_filename

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS_DEFAULT = {"png", "jpg", "jpeg", "gif", "mp4"}
VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "wmv"}


def allowed_file(filename: str, allowed_extensions: Optional[set] = None) -> bool:
    """Check if a filename has an allowed extension.

    Args:
        filename: Name of the file to validate.
        allowed_extensions: Optional set of allowed extensions.

    Returns:
        True if the extension is in the allowed set.
    """
    if allowed_extensions is None:
        allowed = current_app.config.get("ALLOWED_EXTENSIONS", ALLOWED_EXTENSIONS_DEFAULT)
    else:
        allowed = allowed_extensions
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


def save_uploaded_file(
    file,
    upload_folder: Optional[str] = None,
    allowed_extensions: Optional[set] = None
) -> Optional[str]:
    """Save an uploaded file and return its static URL.

    Performs double sanitization on filename for security:
    1. secure_filename() from Werkzeug
    2. Custom sanitize_filename() for additional hardening

    Args:
        file: Werkzeug FileStorage object from request.files.
        upload_folder: Override path; defaults to app config UPLOAD_FOLDER.
        allowed_extensions: Optional set of allowed extensions.

    Returns:
        Static URL string for the saved file, or None if the file was
        invalid or empty.
    """
    if not file or not file.filename or not allowed_file(file.filename, allowed_extensions):
        return None

    folder = upload_folder or current_app.config["UPLOAD_FOLDER"]
    
    # Double sanitization for security
    filename = secure_filename(sanitize_filename(file.filename))
    
    # Additional validation after sanitization
    if not filename or not allowed_file(filename, allowed_extensions):
        logger.warning("Rejected uploaded file with invalid name: %s", file.filename)
        return None
    
    file.save(os.path.join(folder, filename))

    logger.debug("Saved uploaded file: %s", filename)
    return url_for("static", filename="uploads/" + filename)


def detect_media_type(filename: str) -> str:
    """Return 'video' or 'photo' based on file extension.

    Args:
        filename: Filename to inspect.

    Returns:
        'video' for video extensions, 'photo' otherwise.
    """
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
    return "video" if ext in VIDEO_EXTENSIONS else "photo"
