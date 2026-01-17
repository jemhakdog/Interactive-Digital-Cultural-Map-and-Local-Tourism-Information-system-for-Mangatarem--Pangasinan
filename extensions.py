from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Instantiate Limiter without the app
# The app will be initialized later in flask_app.py using limiter.init_app(app)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=["100 per minute"],
)
