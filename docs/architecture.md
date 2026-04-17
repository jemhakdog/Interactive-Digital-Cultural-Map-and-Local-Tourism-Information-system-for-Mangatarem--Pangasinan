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

## Community Stewardship Model (CBIS)

The system implements a **Shared Heritage** stewardship model where data management is decentralized at the barangay level:

- **Unified Asset Management**: Barangay Representatives (Stewards) can view and manage all cultural assets (Attractions and Events) within their barangay, regardless of the original contributor.
- **Barangay Infrastructure**: The `BarangayInfo` model acts as the central anchor for all community-specific data, including history, mission, and vision statements.
- **Contributor Roles**: Users with the `contributor` role are automatically mapped to their respective barangays, gaining administrative oversight over local cultural mapping.

## Participatory GIS (PGIS) Mapping

The platform utilizes a participatory mapping approach (PGIS) where community research is directly translated into public geographic data:

- **Harmonized Asset View**: The public map integrates both static cultural attractions and dynamic community events into a single, unified view.
- **Intelligent Framing**: Using `fitBounds` logic, the map automatically centers and zooms to frame all community-wide assets for visitors when viewing a specific barangay profile.
- **Dynamic Iconography**: Distinct visual markers are utilized for diverse asset types (e.g., 🏛️ for Attractions and 📅 for Events), providing immediate visual context.

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
- **Specialized Heritage Details**: (Forms 01-07)
- **BarangayInfo**: The central hub for community narrative (Mission, Vision, History) and geo data; acts as the primary foreign key anchor for all local assets.
- **Attraction**: Cultural and tourism spots, linked to `BarangayInfo` via `barangay_id` for community stewardship.
- **Event**: Local festivals and community activities with integrated geo-coordinates and barangay anchoring.
- **GalleryItem**: Photos and videos with content moderation and user-level attribution.
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
