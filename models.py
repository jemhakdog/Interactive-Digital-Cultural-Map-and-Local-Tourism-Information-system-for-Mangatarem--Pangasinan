from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets

# auth models shim
from modules.auth.models import User, PasswordResetToken

# attractions models shim
from modules.attractions.models import Attraction, AttractionReview, ReviewPhoto, UserFavoriteAttraction

# events models shim
from modules.events.models import Event, UserEventInterest

# business models shim
from modules.business.models import Establishment, EstablishmentRoom, EstablishmentMenuItem, EstablishmentReview, UserFavoriteEstablishment

# barangay models shim
from modules.barangay.models import BarangayInfo

# heritage models shim
from modules.heritage.models import HeritageProfile

# gallery models shim
from modules.gallery.models import GalleryItem

# analytics models shim
from modules.analytics.models import AnalyticsPageView, DatabaseAuditLog, VisitorLog

# notifications models shim
from modules.notifications.models import NewsletterSubscriber


# === Heritage Models (Tourism Forms) ===

# Import heritage models to register them with SQLAlchemy
# === Heritage Models (Tourism Forms - Detail Tables) ===
from heritage_models.natural_heritage import NaturalHeritage  # Form 01A
from heritage_models.built_heritage import BuiltHeritage      # Form 02A
from heritage_models.movable_heritage import MovableHeritage  # Form 03A
from heritage_models.intangible_heritage import IntangibleHeritage  # Form 04A
from heritage_models.personality_profile import PersonalityProfile  # Form 05
from heritage_models.cultural_institution import CulturalInstitution  # Form 06
from heritage_models.lgu_culture_program import LGUCultureProgram  # Form 07
