import os
import sys

# Add project root to path so imports work from the build/ directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flaskwebgui import FlaskUI
from app import create_app

# Set environment variable to indicate desktop mode
os.environ["IS_DESKTOP"] = "True"
os.environ["FLASK_ENV"] = "development"  # Ensure local mode

# Application Factory
app = create_app()

@app.before_request
def redirect_to_admin():
    from flask import request, redirect, url_for
    # If in desktop mode and accessing root, redirect to admin
    if os.environ.get("IS_DESKTOP") == "True" and request.path == "/":
        return redirect(url_for("admin.admin_dashboard"))

if __name__ == "__main__":
    # Configuration for the desktop window
    # We use 'flask' server type as we are running the app instance directly
    ui = FlaskUI(
        app=app,
        server="flask",
        width=1200,
        height=800,
        port=5005,
    )
    
    ui.run()
