# Models Module Contract (`backend/app/models`)

## Overview
The `backend.app.models` package declares all relational persistence entities for the Mangatarem Cultural Map system using SQLAlchemy 2.0 `DeclarativeBase`.

## Interface
- `Base`: Declarative root base class (`backend.app.models.base.Base`).
- `User`: User entity with bcrypt-hashed passwords, RBAC roles (`admin`, `contributor`, `business_owner`, `user`), and single-use reset tokens.
- `Attraction`, `Review`, `UserFavorite`: Points of interest, ratings, user reviews, and saved bookmarks.
- `BarangayInfo`: Official administrative barangays with geographic boundaries and contact details.
- `Establishment`, `EstablishmentMenuItem`, `EstablishmentRoom`, `BusinessVerification`: Commercial tourism entities, dining menus, accommodations, and accreditation documents.
- `BookableAsset`, `BookingSlot`, `Reservation`: Bookable inventory, capacity slots, and user reservations.
- `ChatMessage`, `ChatParticipant`, `ChatRoom`: Chat rooms and peer/admin messaging.
- `Document`: Administrative and municipal tourism documents.
- `Event`: Local cultural events and festival calendars.
- `GalleryItem`: Public and contributor media assets.
- `AchievementBadge`, `TouristCheckIn`, `UserPassport`: Gamified tourist badges, QR location check-ins, and digital passport stamps.
- `HeritageProfile`: Cultural heritage profiles categorized by type (`built`, `natural`, `intangible`, `movable`, `mixed`).
- `UserNotification`, `NewsletterSubscriber`, `NewsletterHistory`: In-app notification alerts and newsletter dispatches.
- `AnalyticsPageView`, `VisitorLog`, `DatabaseAuditLog`: Telemetry logs, visitor registries, and administrative audit trails.

## Invariants
- All tables register with `Base.metadata`.
- Passwords and auth credentials undergo one-way cryptographic hashing; plaintext storage is forbidden.
- Foreign key constraints enforce referential integrity across barangays, users, attractions, and establishments.

## Side Effects
- Generates SQL DDL schemas and DML queries executed against SQLite/PostgreSQL.

## Verification
- Run: `.venv/bin/pytest tests/`
