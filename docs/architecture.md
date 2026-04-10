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
- **Styling**: Vanilla CSS with Tailwind CSS (v4.0)
- **Interactive Maps**: Mapbox GL JS with Mapbox Vector Tiles (MVT)
- **Assets Build**: PostCSS and Terser

## High-Concurrency Map Architecture

The map system uses a high-performance architecture optimized for Vercel's serverless free tier:

- **Vector Tile Generation**: PostGIS `ST_AsMVT` functions generate Mapbox Vector Tiles (.pbf) directly in the database.
- **Tile Endpoint**: Flask route `/tiles/<z>/<x>/<y>.pbf` serves binary MVT data with `application/x-protobuf` content type.
- **Caching Layers**:
  - **Primary**: Vercel Edge Cache with `Cache-Control: public, s-maxage=3600` headers.
  - **Secondary**: Upstash Redis for dynamic hot-data caching (< 50ms response time).
- **Frontend**: Mapbox GL JS consumes vector tiles instead of GeoJSON, enabling instant map loads and smooth interactions.

## Application Structure

The application follows a modular blueprint-based structure:

- `app.py`: Application factory implementation with Vercel optimizations.
- `models.py`: SQLAlchemy database schema with 20+ core models including Heritage Registry.
- `routes/`: Blueprint-based modular structure:
  - `auth.py`: Authentication (login, logout, registration, password reset).
  - `public.py`: Public visitor pages (Home, Map, Attractions, Events).
  - `admin/`: **Package** - Administrative dashboard (7 submodules):
    - `dashboard.py`: Admin overview and analytics.
    - `attractions.py`: Manage attraction submissions.
    - `events.py`: Manage event submissions.
    - `heritage.py`: Review Cultural Heritage Registry (Forms 01-07).
    - `documents.py`: Manage administrative documents and reports.
    - `newsletter.py`: Manage newsletter subscribers and campaigns.
    - `users.py`: User management and role assignment.
  - `barangay/`: **Package** - Barangay-level content management.
  - `api.py`: Public JSON API endpoints and Heritage Registry API.
  - `user.py`: User profile and favorites.
  - `update.py`: System update operations.
- `utils/`: Core utility modules:
    - `heritage_registry.py`: Registry configuration and model mapping.
    - `db_manager.py`: Multi-database support (SQLite/Supabase).
    - `email_sender.py`: Notification system.
    - `file_helpers.py`: File validation.
    - `logger_helper.py`: Logging.

## Database Schema

The system implements a comprehensive schema aligned with the Cultural Heritage Registry (Forms 01-07):

- **User**: Authentication (Roles: `admin`, `contributor`, `user`).
- **HeritageProfile**: Base model for all cultural registry entries. Links to specialized detail tables.
- **Specialized Heritage Details**:
    - `NATURAL_HERITAGE_DETAIL` (Form 01A)
    - `BUILT_HERITAGE_DETAIL` (Form 02A)
    - `MOVABLE_HERITAGE_DETAIL` (Form 03A)
    - `INTANGIBLE_HERITAGE_DETAIL` (Form 04A)
    - `PERSONALITY_PROFILE_DETAIL` (Form 05)
    - `CULTURAL_INSTITUTION_DETAIL` (Form 06)
    - `LGU_CULTURE_PROGRAM_DETAIL` (Form 07)
- **Attraction**: Tourism spots with `latitude` and `longitude`. Optional link to `HeritageProfile`.
- **Event**: Local festivals and community activities.
- **BarangayInfo**: Historical and cultural background for each barangay.
- **GalleryItem**: Photos and videos with content moderation.
- **AnalyticsPageView**: Page view tracking and engagement.
- **PasswordResetToken**: Secure, time-limited tokens for account recovery.
- **NewsletterSubscriber**: Opt-in mailing list management.

---

## Utility Modules

The `utils/` directory contains core functionality:

### Heritage Registry (`heritage_registry.py`)
- **Purpose**: Central configuration for the 7 heritage form types.
- **Features**: Model mapping, field labels, and UI generation metadata.

### Database Manager (`db_manager.py`)
- **Purpose**: Intelligent database URI selection and Supabase client management.
- **Features**: Automatic environment detection, SQLite for local, Supabase for production.

### Email Sender (`email_sender.py`)
- **Purpose**: Email notifications for account verification and password resets.

---

## Advanced Features

### Cultural Heritage Registry (Forms 01-07)
The system fully implements the structured cultural heritage documentation required by national tourism standards. Each profile includes significant history, conservation status, and mapping coordinates.

### Lazy-Loaded Supabase Client
Cold start optimization on Vercel by initializing the Supabase client only when first accessed.

### Smart Cache Headers
Automatic edge caching based on path and content type (HTML: 5-10 min, Static: 1 year, API: 2 min).

### ProxyFix Middleware
Handles Vercel's reverse proxy headers to ensure correct IP and protocol detection.

---

## Integration Details

- **Supabase**: Production PostgreSQL database via connection pooling (port 6543).
- **Mapbox GL JS**: Interactive maps with vector tile rendering and 3D buildings.
- **Vercel**: Serverless deployment with edge caching and optimized performance.
- **Flask-Login**: Session-based authentication (30-day "Remember Me").
- **Flask-Limiter**: Rate limiting (20 requests/minute API default).
