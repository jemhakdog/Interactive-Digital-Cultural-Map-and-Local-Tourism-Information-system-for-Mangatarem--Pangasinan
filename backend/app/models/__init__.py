"""Central model import hub — mirrors the Flask models.py shim."""
from backend.app.models.base import Base  # noqa: F401

# Auth
from backend.app.models.user import User  # noqa: F401

# Attractions
from backend.app.models.attractions import Attraction, Review, UserFavorite, MapFeedback  # noqa: F401

# Events
from backend.app.models.events import Event  # noqa: F401

# Barangay
from backend.app.models.barangay import BarangayInfo  # noqa: F401

# Business
from backend.app.models.business import (
    Establishment,
    EstablishmentRoom,
    EstablishmentMenuItem,
    BusinessVerification,
)  # noqa: F401

# Heritage
from backend.app.models.heritage import HeritageProfile  # noqa: F401

# Gallery
from backend.app.models.gallery import GalleryItem  # noqa: F401

# Analytics
from backend.app.models.analytics import AnalyticsPageView, DatabaseAuditLog, VisitorLog  # noqa: F401

# Notifications
from backend.app.models.notifications import (
    NewsletterSubscriber,
    NewsletterHistory,
    UserNotification,
)  # noqa: F401

# Chat
from backend.app.models.chat import ChatRoom, ChatParticipant, ChatMessage  # noqa: F401

# Booking
from backend.app.models.booking import BookableAsset, BookingSlot, Reservation  # noqa: F401

# Gamification
from backend.app.models.gamification import AchievementBadge, UserPassport, TouristCheckIn  # noqa: F401

# Documents
from backend.app.models.document import Document  # noqa: F401

# Announcements
from backend.app.models.announcements import Announcement  # noqa: F401
