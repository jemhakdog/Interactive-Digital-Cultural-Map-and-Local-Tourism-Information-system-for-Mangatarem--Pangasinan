# Core Model Shim (Import Hub)
# This file bridges the modular monolith structure, allowing old code and routes 
# to import models from a single central location while keeping model definitions
# beautifully isolated in their respective modules/ directories.

from extensions import db

# === Auth Module Models ===
from modules.auth.models import User, PasswordResetToken

# === Attractions Module Models ===
from modules.attractions.models import Attraction, Review, ReviewPhoto, UserFavorite

# === Events Module Models ===
from modules.events.models import Event

# === Barangay Module Models ===
from modules.barangay.models import BarangayInfo

# === Business Module Models ===
from modules.business.models import Establishment, EstablishmentRoom, EstablishmentMenuItem, BusinessVerification

# === Backward Compatibility Shims ===
AttractionReview = Review
EstablishmentReview = Review
UserFavoriteAttraction = UserFavorite
UserFavoriteEstablishment = UserFavorite
UserEventInterest = UserFavorite

# === Heritage Module Models ===
from modules.heritage.models import HeritageProfile

# === Gallery Module Models ===
from modules.gallery.models import GalleryItem

# === Analytics Module Models ===
from modules.analytics.models import AnalyticsPageView, DatabaseAuditLog, VisitorLog

# === Notifications Module Models ===
from modules.notifications.models import NewsletterSubscriber, NewsletterHistory

# === Heritage Models (Forms 01-07) ===
# These are now merged into HeritageProfile.form_data

# === Chat Module Models ===
from modules.chat.models import ChatRoom, ChatParticipant, ChatMessage

# === Booking Module Models ===
from modules.booking.models import BookableAsset, BookingSlot, Reservation

# === Gamification Module Models ===
from modules.gamification.models import AchievementBadge, UserPassport, TouristCheckIn

# === Announcements Module Models ===
from modules.announcements.models import Announcement


