from flask import Blueprint, request, jsonify
from extensions import limiter
from functools import wraps
from flask_login import current_user
import subprocess
import os
import shutil
import logging
import re
import hmac

update_bp = Blueprint("update", __name__)
logger = logging.getLogger(__name__)


def require_update_token(f):
    """
    Decorator to require a valid update token for sensitive operations.
    
    Checks for a token in the request JSON that matches the configured
    UPDATE_TOKEN environment variable. Only admin users can call update endpoints.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated and is admin
        if not current_user.is_authenticated:
            return jsonify({"status": "error", "message": "Authentication required"}), 401
        
        if current_user.role != "admin":
            return jsonify({"status": "error", "message": "Admin access required"}), 403
        
        # Verify update token if provided in request
        token = None
        if request.is_json:
            token = request.get_json().get("token")
        
        expected_token = os.environ.get("UPDATE_TOKEN")
        if expected_token is None:
            logger.error("UPDATE_TOKEN not configured - rejecting request")
            return jsonify({"status": "error", "message": "Server configuration error"}), 500

        if not token or not hmac.compare_digest(token, expected_token):
            logger.warning(f"Invalid update token attempt from user: {current_user.username}")
            return jsonify({"status": "error", "message": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated_function


@update_bp.route("/pull", methods=["GET", "POST"])
@limiter.limit("1 per minute")
@require_update_token
def pull_updates():
    """
    Pull updates from GitHub repository and copy files to specified locations.

    This endpoint pulls the latest changes from the GitHub repository and
    copies the updated files to the production locations as specified:
    - Source: /home/GoMangatarem/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan
    - Destination 1: /home/GoMangatarem/mysite (all folder and files)
    - Destination 2: /home/GoMangatarem (all files)

    Expects a JSON payload with:
    {
        "token": "webhook_token" (optional, for security)
    }

    Returns:
        JSON response with the result of the operation.
    """
    try:
        print("[PROGRESSIVE LOG] [update] > pull_updates > ENTRY")
        logger.info("Pull updates endpoint called - initiating git pull and file copy")

        # For security, you might want to verify a token or check request headers
        # This is a basic implementation - add more security as needed

        # Define paths (hardcoded for security - no user input)
        source_repo = "/home/GoMangatarem/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan"
        dest1 = "/home/GoMangatarem/mysite"
        dest2 = "/home/GoMangatarem"
        
        # Validate paths don't contain dangerous characters
        for path in [source_repo, dest1, dest2]:
            if not re.match(r'^[a-zA-Z0-9/_\-\.]+$', path):
                logger.error(f"Invalid path detected: {path}")
                return jsonify({"status": "error", "message": "Invalid configuration"}), 500

        # Change directory to the source repository
        original_cwd = os.getcwd()
        print(
            f"[PROGRESSIVE LOG] [update] > pull_updates > LOGIC: Changing directory to '{source_repo}'"
        )
        os.chdir(source_repo)

        # Pull the latest changes from GitHub
        print("[PROGRESSIVE LOG] [update] > pull_updates > LOGIC: Executing git pull")
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)

        if result.returncode != 0:
            print(
                f"[PROGRESSIVE LOG] [update] > pull_updates > ERROR: Git pull failed: {result.stderr}"
            )
            return jsonify(
                {"status": "error", "message": f"Git pull failed: {result.stderr}"}
            ), 500

        # Copy all files and folders to dest1 by updating existing files
        print(
            f"[PROGRESSIVE LOG] [update] > pull_updates > LOGIC: Copying files to '{dest1}'"
        )
        if not os.path.exists(dest1):
            os.makedirs(dest1)

        # Use rsync-like behavior: copy files and overwrite existing ones
        for root, dirs, files in os.walk(source_repo):
            # Skip .git directory to avoid copying git metadata
            dirs[:] = [d for d in dirs if d != ".git"]

            for file in files:
                source_file = os.path.join(root, file)
                rel_path = os.path.relpath(source_file, source_repo)
                dest1_file = os.path.join(dest1, rel_path)

                # Create directory structure if it doesn't exist
                dest1_dir = os.path.dirname(dest1_file)
                if not os.path.exists(dest1_dir):
                    os.makedirs(dest1_dir)

                # Copy file to dest1
                shutil.copy2(source_file, dest1_file)

        # Copy only files (not folders) to dest2
        print(
            f"[PROGRESSIVE LOG] [update] > pull_updates > LOGIC: Copying shell files to '{dest2}'"
        )
        for item in os.listdir(source_repo):
            source_item = os.path.join(source_repo, item)
            dest2_item = os.path.join(dest2, item)
            if os.path.isfile(source_item):
                shutil.copy2(source_item, dest2_item)

        # Return to original directory
        os.chdir(original_cwd)

        print(
            "[PROGRESSIVE LOG] [update] > pull_updates > SUCCESS: Pulled updates and synchronized files"
        )
        logger.info("Successfully completed git pull and file copy operations")

        return jsonify(
            {
                "status": "success",
                "message": "Successfully pulled updates and copied files",
                "git_output": result.stdout,
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
