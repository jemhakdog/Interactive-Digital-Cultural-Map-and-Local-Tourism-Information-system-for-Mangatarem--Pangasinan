import threading
import logging
from datetime import datetime
from flask import current_app
from flask_login import current_user
from extensions import db
from modules.analytics.models import AnalyticsPageView

logger = logging.getLogger(__name__)

def record_view(view_type, item_id=None, page_name=None):
    """
    Record a page view in a background thread to avoid delaying the response.
    Optimized for Serverless: Errors are logged but do not block the main thread.
    """
    if not current_app.config.get("SQLALCHEMY_DATABASE_URI"):
        return

    user_id = current_user.id if current_user.is_authenticated else None
    app = current_app._get_current_object()

    def _async_record():
        with app.app_context():
            try:
                from random import random as random_float
                if random_float() > 0.5: # 50% sampling
                    return

                view = AnalyticsPageView(
                    view_type=view_type,
                    item_id=item_id,
                    page_name=page_name,
                    user_id=user_id,
                    timestamp=datetime.utcnow(),
                )
                db.session.add(view)
                db.session.commit()
            except Exception as e:
                logger.error(f"Analytics Error (background): {e}")
            finally:
                db.session.remove()

    try:
        t = threading.Thread(target=_async_record, daemon=True)
        t.start()
    except Exception as e:
        logger.error(f"Failed to start analytics thread: {e}")
