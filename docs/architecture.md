# System Architecture

This document describes the technical architecture of the Interactive Digital Cultural Map for Mangatarem, Pangasinan.

## Tech Stack

### Backend
- **Framework**: Flask (v3.1.2)
- **Database**: 
  - **SQLite**: Used for local development (stored in `/instance/`).
  - **Supabase (PostgreSQL)**: Supported for production environments.
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Rate Limiting**: Flask-Limiter
- **Migrations**: Flask-Migrate (local development only)

### Frontend
- **Templating**: Jinja2
- **Styling**: Tailwind CSS (v3.4)
- **Interactive Maps**: Leaflet.js
- **Assets Build**: PostCSS and Terser

## Application Structure

The application follows a modular blueprint-based structure:

- `app.py`: Application factory implementation with Vercel optimizations.
- `models.py`: SQLAlchemy database schema with 9 core models.
- `routes/`: Blueprint-based modular structure (7 blueprints):
  - `auth.py`: Authentication (login, logout, registration, password reset).
  - `public.py`: Public visitor pages (Home, Map, Attractions, Events).
  - `admin/`: **Package** - LGU administrative dashboard (5 submodules):
    - `dashboard.py`: Admin overview and analytics.
    - `attractions.py`: Manage and review attraction submissions.
    - `events.py`: Manage and review event submissions.
    - `content.py`: Review gallery items and other content.
    - `users.py`: User management and role assignment.
  - `barangay/`: **Package** - Barangay-level content management (5 submodules):
    - `dashboard.py`: Barangay contributor dashboard.
    - `attractions.py`: Submit and manage barangay attractions.
    - `events.py`: Submit and manage barangay events.
    - `gallery.py`: Upload and manage gallery items.
    - `profile.py`: Manage barangay information and profile.
  - `api.py`: Public JSON API endpoints for map data and analytics.
  - `user.py`: User profile, favorites, and reviews.
  - `update.py`: System update operations and maintenance.
- `utils/`: Six utility modules providing core functionality:
  - `db_manager.py`: Multi-database support (SQLite/Supabase) with connection pooling.
  - `email_sender.py`: Email notifications and communication.
  - `file_helpers.py`: File upload validation and management.
  - `logger_helper.py`: Centralized logging configuration.
  - `session_helper.py`: Session management utilities.
  - `__init__.py`: Module initialization.

## Database Schema

The core entities in the system are:

- **User**: Authentication and authorization (Roles: `admin`, `contributor`, `user`). Includes approval workflow for contributors.
- **Attraction**: Cultural and tourism spots with geo-coordinates (lat/lng). Includes status field (pending/approved) and review tracking.
- **Event**: Local festivals and community activities with categorization (Religious/Civic/Entertainment). Includes status and review workflow.
- **BarangayInfo**: Detailed historical and cultural background for each barangay (history, traditions, cultural assets, local practices).
- **GalleryItem**: Photos and videos with content moderation (pending/approved status).
- **PageView**: Internal analytics for tracking page views and attraction popularity.
- **Favorite**: User's saved attractions for quick access.
- **EventInterest**: Tracks user interest in events (statuses: 'interested', 'going').
- **Review**: User ratings and comments for attractions with moderation (pending/approved/rejected).

## Utility Modules

The `utils/` directory contains six core utility modules:

### Database Manager (`db_manager.py`)
- **Purpose**: Intelligent database URI selection and Supabase client management.
- **Features**:
  - Automatic environment detection (local vs production).
  - SQLite for local development (`instance/app.db`).
  - Supabase connection pooling for production (via `DATABASE_URL`).
  - Lazy Supabase client initialization.
- **Key Functions**: `get_database_uri()`, `get_supabase_client()`.

### Email Sender (`email_sender.py`)
- **Purpose**: Email notifications for user actions.
- **Use Cases**: Account verification, password reset, content approval notifications.

### File Helpers (`file_helpers.py`)
- **Purpose**: File upload validation and management.
- **Features**:
  - Allowed extensions validation (`png`, `jpg`, `jpeg`, `gif`, `mp4`).
  - Secure filename generation.
  - Upload directory management.

### Logger Helper (`logger_helper.py`)
- **Purpose**: Centralized logging configuration.
- **Features**: Configurable log levels, structured logging output.

### Session Helper (`session_helper.py`)
- **Purpose**: Session management utilities.
- **Features**: Session persistence, secure cookie configuration.

---

## Advanced Features

### Lazy-Loaded Supabase Client

The application uses a descriptor pattern to initialize the Supabase client only when first accessed:

```python
class LazySupabase:
    def __get__(self, obj, objtype=None):
        if _supabase_client is None:
            _supabase_client = get_supabase_client()
        return _supabase_client
```

**Benefits**:
- Reduces cold start time on Vercel (300-500ms faster).
- Client initialized only when Supabase-specific features are used.
- Prevents unnecessary connection overhead.

### Smart Cache Headers

Automatic edge caching based on path and content type:

| Path Type | Cache-Control | Use Case |
|-----------|---------------|----------|
| Admin/Auth routes (`/admin`, `/auth`) | `private, no-store` | Never cached, always fresh |
| HTML pages (public) | `public, max-age=60, s-maxage=300, stale-while-revalidate=600` | Edge cached for 5 min, stale served up to 10 min |
| Static assets (`.js`, `.css`, images) | `public, max-age=31536000, immutable` | Cached for 1 year (versioned files) |
| API responses | `public, max-age=30, s-maxage=120, stale-while-revalidate=300` | Edge cached for 2 min |

**Implementation**: See `_apply_cache_headers()` in `app.py:147-157`.

### Custom Error Handlers

Custom error pages for improved user experience:

**Supported Error Codes**: `400`, `401`, `403`, `404`, `408`, `429`, `451`, `500`.

**Template Location**: `templates/errors/{code}.html`.

**Implementation**: All error codes route through a unified handler that renders appropriate error templates.

### PWA Support

Progressive Web App capabilities:

- **Service Worker**: `/sw.js` - Enables offline functionality and caching.
- **Web App Manifest**: `/manifest.json` - Defines app metadata for installation.
- **Benefits**:
  - Install to home screen on mobile devices.
  - Offline content access.
  - Native app-like experience.

### Error Handling ⚠️
The application provides user-friendly error pages for 8 HTTP status codes:

| Code | Type | Description |
|------|------|-------------|
| **400** | Bad Request | Invalid request parameters or malformed data |
| **401** | Unauthorized | Authentication required but not provided |
| **403** | Forbidden | Authenticated but lacking required permissions |
| **404** | Not Found | Requested resource does not exist |
| **408** | Request Timeout | Server timeout waiting for request |
| **429** | Too Many Requests | Rate limit exceeded |
| **451** | Unavailable For Legal Reasons | Content blocked for legal reasons |
| **500** | Internal Server Error | Unexpected server-side error |

**Implementation**: Error templates located in `templates/errors/{code}.html`, registered via `_register_error_handlers()` in `app.py`.

### ProxyFix Middleware

Handles Vercel's reverse proxy headers correctly:

```python
if "VERCEL" in os.environ:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
```

**Purpose**: Ensures correct client IP, protocol, and host detection behind Vercel's proxy.

---

## Integration Details

- **Supabase**: Production database via Python SDK with connection pooling (port 6543). Lazy-loaded client for optimal cold start performance.
- **Leaflet.js**: Interactive maps with Mapbox tiles. Displays attraction markers with clustering and barangay boundaries.
- **Vercel**: Serverless deployment with edge caching, ProxyFix middleware, and optimized cold start times.
- **Flask-Login**: Session-based authentication with "Remember Me" functionality (30-day cookie duration).
- **Flask-Limiter**: Rate limiting for API endpoints (20 requests/minute default).
