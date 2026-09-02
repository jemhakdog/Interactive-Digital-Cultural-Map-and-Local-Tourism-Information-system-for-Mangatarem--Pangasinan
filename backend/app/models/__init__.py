"""Central model import hub — mirrors the Flask models.py shim."""
# Analytics
from backend.app.models.analytics import (
    AnalyticsPageView,
    DatabaseAuditLog,
    VisitorLog,
)

# Announcements
from backend.app.models.announcements import Announcement

# Attractions
from backend.app.models.attractions import (
    Attraction,
    MapFeedback,
    Review,
    UserFavorite,
)

# Barangay
from backend.app.models.barangay import BarangayInfo
from backend.app.models.base import Base

# Booking
from backend.app.models.booking import (
    BookableAsset,
    BookingSlot,
    Reservation,
)

# Business
from backend.app.models.business import (
    BusinessVerification,
    Establishment,
    EstablishmentMenuItem,
    EstablishmentRoom,
)

# Chat
from backend.app.models.chat import ChatMessage, ChatParticipant, ChatRoom

# Documents
from backend.app.models.document import Document

# Events
from backend.app.models.events import Event

# Gallery
from backend.app.models.gallery import GalleryItem

# Gamification
from backend.app.models.gamification import (
    AchievementBadge,
    TouristCheckIn,
    UserPassport,
)

# Heritage
from backend.app.models.heritage import HeritageProfile

# Notifications
from backend.app.models.notifications import (
    NewsletterHistory,
    NewsletterSubscriber,
    UserNotification,
)

# Auth
from backend.app.models.user import User
