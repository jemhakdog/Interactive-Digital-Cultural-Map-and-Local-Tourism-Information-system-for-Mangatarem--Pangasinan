# Backend Conventions — Source of Truth

> Extracted by the **Backend conventions extraction** agent (phase: backend conventions extraction).
> Scope: FastAPI backend at `backend/app/`. Domain agents (admin / business / contributor / public / tourist)
> MUST follow the router, auth, DB, model, schema, and endpoint conventions documented here.
> Companion docs: `CONVENTIONS.md` (frontend+backend API surface), `PORT_REPORT.md` (placeholder gaps), `spec-*.md`.

**API base:** `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`). Every backend route is mounted under `/api` (except `/health`, `/`, static mounts). Frontend calls these EXACT mounted URLs.

> NOTE on paths: the task brief referenced `backend/backend/app/...`; the real tree is `backend/app/...` (single `backend/` level). All paths below use the real layout.

---

## 1. Router conventions

### 1.1 Pattern
Every module defines a router with:

```python
from fastapi import APIRouter
router = APIRouter()
```

Endpoints are decorated with `@router.get(...)`, `@router.post(...)`, etc. No per-router `prefix=`/`tags=` is set on the `APIRouter()` object itself — **prefixes and tags are applied centrally in `main.py` via `include_router`**. This is the single source of truth for public URLs.

### 1.2 How prefixes are applied (`main.py`)
`main.py` imports each router and mounts it:

```python
app.include_router(auth_router,        prefix="/api/auth",        tags=["auth"])
app.include_router(public_router,      prefix="/api",             tags=["public"])
app.include_router(attractions_router, prefix="/api/attractions",  tags=["attractions"])
...
```

So a route declared as `@router.get("/")` in `attractions.py` is reachable at `GET /api/attractions/`, and `@router.get("/{attraction_id}")` at `GET /api/attractions/{attraction_id}`.

### 1.3 Full mount-prefix map (authoritative)

| Module file | Router import name | Mounted prefix | Tag |
|---|---|---|---|
| `api/auth.py` | `auth_router` | `/api/auth` | auth |
| `api/public.py` | `public_router` | `/api` | public |
| `api/attractions.py` | `attractions_router` | `/api/attractions` | attractions |
| `api/events.py` | `events_router` | `/api/events` | events |
| `api/business.py` | `business_router` | `/api/business` | business |
| `api/booking.py` | `booking_router` | `/api/booking` | booking |
| `api/chat.py` | `chat_router` | `/api/chat` | chat |
| `api/gallery.py` | `gallery_router` | `/api/gallery` | gallery |
| `api/heritage.py` | `heritage_router` | `/api/heritage` | heritage |
| `api/gamification.py` | `gamification_router` | `/api/gamification` | gamification |
| `api/notifications.py` | `notifications_router` | `/api/notifications` | notifications |
| `api/analytics.py` | `analytics_router` | `/api/analytics` | analytics |
| `api/uploads.py` | `uploads_router` | `/api/uploads` | uploads |
| `api/admin.py` | `admin_router` | `/api/admin` | admin |

Plus app-level (no `/api` prefix): `GET /health`, `GET /`. Static mounts: `/uploads` (StaticFiles → `backend/uploads/`), `/static` (StaticFiles → repo `static/`, only if dir exists).

**New routers to add (referred to by placeholder pages):** `barangays`, `announcements`, `documents`, `contributor`, `user`. Follow the same `include_router(router, prefix="/api/<name>", tags=["<name>"])` pattern in `main.py`.

---

## 2. Auth dependencies available

Defined in `core/dependencies.py`:

| Dependency | Signature | Behavior |
|---|---|---|
| `get_current_user` | `(token: str, db: AsyncSession) -> User` | Decodes JWT (`oauth2_scheme` tokenUrl `/api/auth/login`); 401 if invalid/missing user. Does **not** check role or approval. |
| `get_current_active_user` | `(current_user: User) -> User` | Depends on `get_current_user`; raises 403 if `not user.is_approved`. Does **not** check role. |
| `require_admin` | `(current_user: User) -> User` | Depends on `get_current_user`; raises 403 if `user.role != "admin"`. (Note: does **not** require `is_approved`.) |

`oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")`. Roles are stored on `User.role` and can be one of: `admin`, `contributor`, `business_owner`, `user` (see `schemas/auth.py::UserRole`).

### 2.1 IMPORTANT — no role/business/contributor helpers exist
There are **NO** `require_roles`, `require_contributor`, `require_business_owner`, or `require_moderator` dependencies. Where a non-admin role is permitted, endpoints do an **inline** check instead, e.g.:

```python
user: Annotated[User, Depends(get_current_user)]
...
if user.role not in ("admin", "contributor", "business_owner"):
    raise HTTPException(status_code=403, detail="Unauthorized")
```

or `if user.role != "business_owner": raise 403` (see `business.py::create_establishment`). Domain agents adding contributor/business/admin endpoints MUST replicate this inline pattern (or add a shared dependency and update this doc). Do not assume a `require_<role>` helper exists.

---

## 3. Database conventions

- `core/database.py::get_db()` is an async generator yielding `AsyncSession` (from `async_sessionmaker`). Used everywhere as `db: Annotated[AsyncSession, Depends(get_db)]`.
- `get_db()` wraps the session in `try/commit/except rollback`, so endpoints normally just `db.add(...)` / `await db.flush()` / `await db.refresh(...)` and let the dependency commit.
- `init_db()` uses `Base.metadata.create_all` (in `lifespan`, dev environment only). **There are NO migrations (no Alembic).** New models must be added to `models/__init__.py` so they are imported and picked up by `create_all`.
- Tables use `Mapped[...]` / `mapped_column` (SQLAlchemy 2.0 style), `Base` in `models/base.py`. JSON columns use `sqlalchemy.dialects.postgresql.JSON` (noted as SQLite-compatible via the JSON generic in practice).
- Engine: `create_async_engine(settings.async_database_url)`, `pool_pre_ping=True`; pool_size args only set when not sqlite.

---

## 4. Model inventory (all exist; imported in `models/__init__.py`)

| Model | Table | Key columns | Notes |
|---|---|---|---|
| `User` | `USER` | id, username (unique), email (unique), password, role, barangay_id, is_approved, reset_token*, created_at | `set_password`/`check_password` (bcrypt); reset-token helpers. |
| `Attraction` | `ATTRACTION` | id, name, description, category, lat, lng, barangay_id, heritage_profile_id, status, is_featured, physical_status, is_verified, opening_hours, entrance_fee, contact_info, facilities, advisory_*, user_id, created_at | `rating` property is a no-op (always None) — rating computed via async query in API. |
| `Review` | `REVIEW` | id, user_id, attraction_id, establishment_id, rating, comment, status, parent_id (self-FK), photo_urls (JSON), created_at | CHECK: exactly one of attraction_id/establishment_id non-null. |
| `UserFavorite` | `USER_FAVORITE` | id, user_id, attraction_id, establishment_id, event_id, status, created_at | CHECK: exactly one target non-null. |
| `MapFeedback` | `MAP_FEEDBACK` | id, attraction_id, feedback_type, message, status, created_at | |
| `Event` | `EVENT` | id, name, description, date, location, lat, lng, barangay_id, image_url, category, status, user_id, created_at | |
| `BarangayInfo` | `BARANGAY_INFO` | id, name (unique), mission, vision, history, cultural_assets, traditions, local_practices, unique_features, user_id, map_geo_json (JSON), location_data (JSON), created_at | Narrative + geo fields. Used by contributor profile. |
| `Establishment` | `ESTABLISHMENT` | id, name, type, description, address, lat, lng, barangay_id, contact_*, email, website, operating_hours (JSON), price_range, amenities (JSON), cover_image_url, logo_url, owner_id, status, is_featured, rating_avg, review_count, created_at | |
| `EstablishmentRoom` | `ESTABLISHMENT_ROOM` | id, establishment_id (FK CASCADE), name, description, price_per_night, capacity, amenities (JSON), image_urls (JSON), is_available, created_at | |
| `EstablishmentMenuItem` | `ESTABLISHMENT_MENU_ITEM` | id, establishment_id (FK CASCADE), name, description, price, category, image_url, is_available, is_bestseller, created_at | |
| `BusinessVerification` | `BUSINESS_VERIFICATION` | id, user_id, permit_document_url, other_document_url, status, submitted_at | **No schema** exists yet (see §5). |
| `HeritageProfile` | `HERITAGE_PROFILE` | id, asset_type, form_control_number, form_data (JSON), name_of_asset, common_name, barangay_id, location_details, contact_*, ownership_type, owner_administrator, usage_status, lat, lng, significance, conservation_status, template_slug, mapper_name, date_profiled, status, user_id, created_at, updated_at | 5 heritage types in one table via `asset_type`. |
| `GalleryItem` | `GALLERY_ITEM` | id, type, url, caption, user_id, status, created_at | |
| `AnalyticsPageView` | `ANALYTICS_PAGE_VIEW` | id, page_url, view_type, item_id, page_name, user_id, timestamp, session_id, ip_address, device_info | |
| `DatabaseAuditLog` | `DATABASE_AUDIT_LOG` | id, user_id, action, table_name, record_id, ip_address, user_agent, query_summary, status, created_at | Has async `log_operation(...)` classmethod. |
| `VisitorLog` | `VISITOR_LOG` | id, target_type, target_id, visitor_count, visitor_name, visitor_age, visitor_address, is_system_user, visit_date, logged_by, visitor_user_id, notes, created_at | |
| `NewsletterSubscriber` | `NEWSLETTER_SUBSCRIBER` | id, email (unique), is_active, user_id, created_at | |
| `NewsletterHistory` | `NEWSLETTER_HISTORY` | id, subject, content, recipient_count, sender_id, sent_at | |
| `UserNotification` | `USER_NOTIFICATION` | id, user_id, title, message, link, is_read, created_at | |
| `ChatRoom` | `CHAT_ROOM` | id, type, barangay_id, establishment_id, created_at | |
| `ChatParticipant` | `CHAT_PARTICIPANT` | id, chat_room_id, user_id, joined_at, last_read_at | |
| `ChatMessage` | `CHAT_MESSAGE` | id, chat_room_id, sender_id, content, created_at, is_system_msg | |
| `BookableAsset` | `BOOKABLE_ASSET` | id, attraction_id, heritage_profile_id, daily_capacity, requires_approval, booking_instructions, status, created_at | |
| `BookingSlot` | `BOOKING_SLOT` | id, bookable_asset_id, date, total_capacity, booked_count; `available_capacity` property; UNIQUE(asset,date) | |
| `Reservation` | `RESERVATION` | id, user_id, booking_slot_id, party_size, primary_contact, special_requests, status, qr_code_token (unique), created_at, updated_at; UNIQUE(user,slot) | status flow: pending→{confirmed,cancelled}; confirmed→{cancelled,attended,no-show}. |
| `AchievementBadge` | `ACHIEVEMENT_BADGE` | id, title, description, badge_image_url, required_visits, target_locations (JSON), reward_promo (JSON), created_at | |
| `UserPassport` | `USER_PASSPORT` | id, user_id, badge_id, unlocked_at; UNIQUE(user,badge) | |
| `TouristCheckIn` | `TOURIST_CHECK_IN` | id, user_id, attraction_id, establishment_id, lat, lng, distance_meters, verified_at; UNIQUE(user,attraction), UNIQUE(user,establishment) | |
| `Announcement` | `ANNOUNCEMENT` | id, title, content, user_id, barangay_id, status, created_at, updated_at | |

**Missing model needed by placeholder pages:** `Document` (for the `/api/documents` admin router) — does not exist yet; must be created + imported in `models/__init__.py`.

---

## 5. Schema inventory (`schemas/`)

Existing schema files (all under `backend/app/schemas/`):
`analytics.py`, `attraction.py`, `auth.py`, `booking.py`, `business.py`, `chat.py`, `event.py`, `gallery.py`, `gamification.py`, `heritage.py`, `notification.py`.

| Schema file | What it provides | Status |
|---|---|---|
| `attraction.py` | AttractionCreate/Update/Response, ReviewCreate/Response, ReviewSummary/List, PaginationMeta | present |
| `event.py` | EventCreate/Update/Response, EventListResponse, PaginationMeta | present |
| `business.py` | Establishment\*, Room\*, MenuItem\*, Review\* | present |
| `booking.py` | Availability/Reserve/Reservation/UpdateStatus/VerifyArrival schemas | present |
| `heritage.py` | HeritageProfile\*, HeritageType\*, PaginationMeta | present |
| `gamification.py` | StartNavigation/Checkin/Passport/Badge schemas | present |
| `chat.py` | ChatRoom/Message schemas, SendMessage\* | present |
| `gallery.py` | GalleryItemResponse, GalleryListResponse | present |
| `auth.py` | UserRole enum, Login/Register/Google/Reset/Refresh, TokenResponse, **UserResponse**, RefreshRequest | present (UserResponse covers read-only profile) |
| `notification.py` | Subscribe\*, Notification\* (public subscribe + user notifications) | present (no admin newsletter send/list schema) |
| `analytics.py` | VisitorLogRequest/Response, AnalyticsSummaryResponse, **VisitorItem/VisitorListResponse**, TopPageItem | present (visitor *response* schemas exist; no admin router schemas) |

### MISSING schemas (must be created for the placeholder pages)
| Missing schema | Router that needs it | Backing model | Notes |
|---|---|---|---|
| `announcements.py` | `/api/announcements` (contributor + public) | `Announcement` (exists) | Create/Update/Response + list. |
| `barangay.py` | `/api/barangays` | `BarangayInfo` (exists) | List + profile Response; PUT (manager edit). |
| `verification.py` | `/api/business/verification` (owner) + admin verify-merchant | `BusinessVerification` (exists) | Submit + admin approve/reject. |
| `document.py` | `/api/documents` (admin) | `Document` (**missing model**) | Needs new model too. |
| `newsletter.py` (admin) | `/api/admin/newsletter` | `NewsletterSubscriber`, `NewsletterHistory` (exist) | Admin send/list/unsubscribe schemas. |
| `visitor.py` (admin) | `/api/admin/visitors`, `/api/admin/visits` | `VisitorLog` (exists; `VisitorItem` already in analytics.py) | Registry read/export + per-target history. |
| `user.py` (profile/dashboard/favorites/visits) | `/api/user` | `User`, `UserFavorite`, `VisitorLog` (exist) | Profile update, dashboard stats, favorites toggle/list, visits list. |
| `contributor.py` | `/api/contributor` | `Attraction`, `Event`, `Review`, `GalleryItem`, `BarangayInfo` (exist) | Dashboard stats, barangay-scoped aggregates. |
| `moderation.py` | `/api/admin/*` | `Review`, `Establishment`, `User` (exist) | Approve/reject review, establishment, user. |

> `user` schema note: read-only `UserResponse` already exists in `auth.py`; the missing pieces are profile-update, favorites, visits, and dashboard schemas (NOT yet in a `user.py`).

---

## 6. Existing endpoint reference table

Auth-role legend: **public** = no auth; **user** = `get_current_user`; **active** = `get_current_active_user`; **admin** = `require_admin`; **inline** = `get_current_user` + inline `role` check.

### App-level (`main.py`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/health` | public | Health check. |
| GET | `/` | public | API name/version/docs links. |

### Auth (`/api/auth`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| POST | `/api/auth/login` | public | Email+password → JWT pair. |
| POST | `/api/auth/register` | public | Create user → JWT pair. |
| POST | `/api/auth/google` | public | Google OAuth credential → JWT pair. |
| POST | `/api/auth/forgot-password` | public | Generate reset token (opaque response). |
| POST | `/api/auth/reset-password` | public | Reset password with token. |
| GET | `/api/auth/me` | user | Current user profile (`UserResponse`). |
| POST | `/api/auth/refresh` | public | Refresh token → new JWT pair. |
| POST | `/api/auth/logout` | public | Stateless logout (noop). |

### Public (`/api`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/api/` | public | Homepage featured attractions + events. |
| GET | `/api/search` | public | Unified search (attractions, events, barangays) + filter options. |
| GET | `/api/map` | public | Map markers (approved attractions w/ coords). |

### Attractions (`/api/attractions`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/api/attractions/` | public | List approved attractions (paginated, filter, geo-radius). |
| GET | `/api/attractions/{attraction_id}` | public | Attraction detail (+ computed rating). |
| POST | `/api/attractions/` | admin | Create attraction (forced `status="approved"`). |
| PUT | `/api/attractions/{attraction_id}` | admin | Update attraction. |
| DELETE | `/api/attractions/{attraction_id}` | admin | Delete attraction. |
| GET | `/api/attractions/{attraction_id}/reviews` | public | List approved reviews + summary. |
| POST | `/api/attractions/{attraction_id}/reviews` | active | Post review (or reply via `parent_id`). |

### Events (`/api/events`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/api/events/` | public | List events (default approved; filter by status/category). |
| GET | `/api/events/{event_id}` | public | Event detail. |
| POST | `/api/events/` | admin | Create event (forced `status="approved"`). |
| PUT | `/api/events/{event_id}` | admin | Update event. |
| DELETE | `/api/events/{event_id}` | admin | Delete event. |

### Business (`/api/business`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/api/business/` | public | List approved establishments (paginated/filter/geo). |
| GET | `/api/business/{establishment_id}` | public | Establishment detail (+ rooms/menu/reviews). |
| POST | `/api/business/` | active (role=business_owner) | Create establishment (status `pending`; one per owner; inline 403). |
| PUT | `/api/business/{establishment_id}` | active (owner or admin) | Update establishment (inline ownership check). |
| GET | `/api/business/rooms/list` | active | Owner's rooms list. |
| POST | `/api/business/rooms` | active | Add room (owner-scoped). |
| PUT | `/api/business/rooms/{room_id}` | active | Edit room (owner-scoped). |
| DELETE | `/api/business/rooms/{room_id}` | active | Delete room (owner-scoped). |
| GET | `/api/business/menu/list` | active | Owner's menu items list. |
| POST | `/api/business/menu` | active | Add menu item (owner-scoped). |
| PUT | `/api/business/menu/{item_id}` | active | Edit menu item (owner-scoped). |
| DELETE | `/api/business/menu/{item_id}` | active | Delete menu item (owner-scoped). |
| POST | `/api/business/{establishment_id}/reviews` | active | Submit establishment review + recalc rating. |
| POST | `/api/business/reviews/{review_id}/reply` | active | Owner reply to review. |

### Booking (`/api/booking`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/api/booking/availability/{asset_id}` | public | Available capacity for a date. |
| POST | `/api/booking/reserve` | user | Create reservation (idempotent). |
| POST | `/api/booking/admin/update-status` | inline (admin/contributor/business_owner) | Transition reservation status. |
| POST | `/api/booking/verify-arrival` | user | GPS arrival verification (booking + navigation). |

### Chat (`/api/chat`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/api/chat/` | user | List current user's chat rooms. |
| GET | `/api/chat/{room_id}` | user | Room messages (membership/barangay auth). |
| POST | `/api/chat/{room_id}/messages` | user | Send message. |

### Gallery (`/api/gallery`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/api/gallery/` | public | List approved gallery items (filter by type/barangay). |
| POST | `/api/gallery/` | **public** | Submit gallery item (status `pending`). ⚠️ unauthenticated, url-only. |

### Heritage (`/api/heritage`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/api/heritage/` | public | List all approved heritage items. |
| GET | `/api/heritage/types` | public | Heritage types with approved counts. |
| GET | `/api/heritage/{heritage_type}` | public | List by type (built/natural/intangible/movable/mixed). |
| GET | `/api/heritage/{heritage_type}/{item_id}` | public | Item detail. |
| POST | `/api/heritage/{heritage_type}` | active | Create profile (status defaults to request value / pending). |
| PUT | `/api/heritage/{heritage_type}/{item_id}` | active | Update profile. |
| DELETE | `/api/heritage/{heritage_type}/{item_id}` | admin | Delete profile. |

### Gamification (`/api/gamification`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| POST | `/api/gamification/start-navigation` | user | Lock active nav route (Redis, 24h TTL). |
| POST | `/api/gamification/stop-navigation` | user | Clear active nav route. |
| GET | `/api/gamification/active-navigation` | user | Get active nav session. |
| POST | `/api/gamification/checkin` | user | GPS-validated QR check-in + badge unlock. |
| GET | `/api/gamification/passport` | user | View tourist passport (badges, coupons, check-ins). |

### Notifications (`/api/notifications`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| POST | `/api/notifications/subscribe` | public | Newsletter subscribe. |
| POST | `/api/notifications/mark-read` | user | Mark all read. |
| POST | `/api/notifications/mark-read/{notification_id}` | user | Mark one read. |
| GET | `/api/notifications/` | user | List user notifications. |
| GET | `/api/notifications/unread` | user | Unread count. |

### Analytics (`/api/analytics`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| POST | `/api/analytics/log-visitor/{target_type}/{target_id}` | active | Log a visitor (owner/admin/contributor barangay rep; inline role checks). |
| GET | `/api/analytics/summary` | inline (admin) | Totals only (visitors, page views, 7d). |

### Uploads (`/api/uploads`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| POST | `/api/uploads/image` | user | Upload single image (png/jpg/jpeg/gif; ≤10MB). |
| POST | `/api/uploads/multiple` | user | Upload multiple (≤10; png/jpg/jpeg/gif/mp4). |

### Admin (`/api/admin`)
| Method | Mounted URL | Auth | Purpose |
|---|---|---|---|
| GET | `/api/admin/users` | admin | Paginated user list (`UserResponse`). |

---

## 7. MISSING endpoints the placeholder pages need

Each row: which router it belongs in, the exact mounted URL the frontend calls, and the model/schema it needs. Derived from `PORT_REPORT.md` §3–4 + `CONVENTIONS.md` §7 + the created React pages. All are currently **MISSING** (placeholder UI renders local/empty state).

### 7.1 Barangays (`/api/barangays` — NEW router)
| Frontend page(s) | Mounted URL | Method | Auth | Model | Schema needed |
|---|---|---|---|---|---|
| `admin/attractions/new`, `admin/attractions/[id]/edit`, `admin/events/new`, `admin/events/[id]/edit` | `/api/barangays` | GET | admin (or public) | `BarangayInfo` | `barangay.py` (list) |
| `public/barangays`, `public/barangays/[id]` | `/api/barangays/{id}` | GET | public | `BarangayInfo` | `barangay.py` (profile) |
| `contributor/profile` | `/api/barangays/{id}` | PUT | active (manager) | `BarangayInfo` | `barangay.py` (update) |

### 7.2 Admin moderation (`/api/admin` — extend existing router)
| Frontend page | Mounted URL | Method | Auth | Model | Schema needed |
|---|---|---|---|---|---|
| `admin/users` | `/api/admin/users/{id}/approve` | PUT | admin | `User` | `moderation.py` |
| `admin/reviews` | `/api/admin/reviews` | GET | admin | `Review` | `moderation.py` (list) |
| `admin/reviews` | `/api/admin/reviews/{id}` | PUT | admin | `Review` | `moderation.py` (approve/reject) |
| `admin/establishments` | `/api/admin/establishments` | GET | admin | `Establishment` | `moderation.py` (all-status list) |
| `admin/establishments` | `/api/admin/establishments/{id}/status` | PUT | admin | `Establishment` | `moderation.py` (approve/reject) |
| `admin/establishments` | `/api/admin/establishments/{id}` | DELETE | admin | `Establishment` | existing |
| `admin/verify-merchants` | `/api/admin/verify-merchants` | GET | admin | `BusinessVerification` | `verification.py` (list) |
| `admin/verify-merchants` | `/api/admin/verify-merchants/{id}` | PUT | admin | `BusinessVerification` | `verification.py` (approve/reject) |
| `admin/documents` | `/api/documents` | GET/POST | admin | `Document` (**new model**) | `document.py` |
| `admin/documents` | `/api/documents/{id}` | GET/PUT/DELETE | admin | `Document` | `document.py` |
| `admin/newsletter` | `/api/admin/newsletter/send` | POST | admin | `NewsletterSubscriber`, `NewsletterHistory` | `newsletter.py` (admin) |
| `admin/newsletter` | `/api/admin/newsletter` | GET | admin | `NewsletterHistory` | `newsletter.py` (list) |
| `admin/newsletter/unsubscribe/{id}` | PUT | admin | `NewsletterSubscriber` | `newsletter.py` |
| `admin/visitor-registry` | `/api/admin/visitors` | GET | admin | `VisitorLog` | `visitor.py` (registry; `VisitorItem` exists in analytics.py) |
| `admin/visitor-registry` | `/api/admin/visitors/export` | GET | admin | `VisitorLog` | `visitor.py` (export) |
| `admin/visits` | `/api/analytics/summary` (expand) | GET | admin | `VisitorLog`, `AnalyticsPageView` | extend analytics summary (period/top-location/comparison) |
| `admin/bookings` | `/api/booking/reservations` | GET | admin | `Reservation` | `booking.py` (add `ReservationResponse` list) |
| `admin/heritage/*` (NCCA export) | `/api/heritage/export` (or `/api/admin/heritage/export`) | GET | admin | `HeritageProfile` | `heritage.py` (export) |

### 7.3 Business owner verification (`/api/business` — extend existing)
| Frontend page | Mounted URL | Method | Auth | Model | Schema needed |
|---|---|---|---|---|---|
| `business/[id]/verify` | `/api/business/verification` | POST | active (business_owner) | `BusinessVerification` | `verification.py` (submit) |
| `business/[id]/reviews` | `/api/business/{id}/reviews` | GET | active (owner) | `Review` | `business.py` (owner all-status list) |

### 7.4 Contributor scope (`/api/contributor` — NEW router)
| Frontend page | Mounted URL | Method | Auth | Model | Schema needed |
|---|---|---|---|---|---|
| `contributor/dashboard` | `/api/contributor/dashboard` | GET | active (contributor) | `Attraction`/`Event`/`Review`/`GalleryItem` | `contributor.py` (stats) |
| `contributor/attractions/*` | `/api/contributor/attractions` | GET/POST | active (contributor) | `Attraction` | `attraction.py` (exists) |
| `contributor/attractions/*` | `/api/contributor/attractions/{id}` | GET/PUT/DELETE | active (contributor, barangay-scoped) | `Attraction` | `attraction.py` |
| `contributor/events/*` | `/api/contributor/events` | GET/POST | active (contributor) | `Event` | `event.py` (exists) |
| `contributor/events/*` | `/api/contributor/events/{id}` | GET/PUT/DELETE | active (contributor) | `Event` | `event.py` |
| `contributor/gallery/*` | `/api/contributor/gallery` | GET/POST | active (contributor) | `GalleryItem` | `gallery.py` (authed create; existing POST `/api/gallery` is public) |
| `contributor/gallery/*` | `/api/contributor/gallery/{id}` | PUT/DELETE | active (contributor) | `GalleryItem` | `gallery.py` |
| `contributor/announcements/*` | `/api/announcements` | GET/POST | active (contributor) | `Announcement` | `announcements.py` |
| `contributor/announcements/*` | `/api/announcements/{id}` | GET/PUT/DELETE | active (contributor) | `Announcement` | `announcements.py` |
| `public/announcements` | `/api/announcements` | GET | public | `Announcement` | `announcements.py` (approved list) |
| `contributor/reviews` | `/api/contributor/reviews` | GET | active (contributor) | `Review` | `contributor.py` (barangay-scoped aggregate) |
| `contributor/profile` | `/api/barangays/{id}` | GET/PUT | active (manager) | `BarangayInfo` | `barangay.py` (see §7.1) |

### 7.5 Tourist user (`/api/user` — NEW router)
| Frontend page | Mounted URL | Method | Auth | Model | Schema needed |
|---|---|---|---|---|---|
| `profile` | `/api/user/profile` | GET/PUT | user | `User` | `user.py` (profile update; `UserResponse` exists in auth.py) |
| `dashboard` | `/api/user/dashboard` | GET | user | — (aggregates) | `user.py` (stats) |
| `user/favorites` (not yet built) | `/api/user/favorites` | GET/POST/DELETE | user | `UserFavorite` | `user.py` (favorites) |
| `user/visits` (not yet built) | `/api/user/visits` | GET | user | `VisitorLog` | `user.py` (visits; `VisitorItem` exists in analytics.py) |
| `reviews` | photo upload pairing | POST | active | `Review` | extend `ReviewCreate` or use `/api/uploads/multiple` |

### 7.6 Notes for domain agents
- Add every new router to `main.py` with `include_router(router, prefix="/api/<name>", tags=["<name>"])`, imported at the bottom alongside the others.
- Add every new model to `models/__init__.py` (no migrations — `init_db()` is `create_all`).
- Reuse existing schemas where they exist (`attraction.py`, `event.py`, `business.py`, `gallery.py`, `auth.UserResponse`, analytics `VisitorItem`). Create the MISSING schemas in §5.
- Honor the auth pattern: use `get_current_user` / `get_current_active_user` / `require_admin` deps, and **inline `user.role` checks** for contributor/business_owner (no role helper exists).
- Gallery `POST /api/gallery/` is currently public + url-only; contributor authed create should live under `/api/contributor/gallery` to avoid loosening the public route.
