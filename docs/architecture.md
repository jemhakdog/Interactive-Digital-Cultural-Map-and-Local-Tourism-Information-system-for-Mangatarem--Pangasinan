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
- **Migrations**: Flask-Migrate

### Frontend
- **Templating**: Jinja2
- **Styling**: Tailwind CSS (v3.4)
- **Interactive Maps**: Leaflet.js
- **Assets Build**: PostCSS and Terser

## Application Structure

The application follows a modular blueprint-based structure:

- `app.py`: Main entry point, configures the Flask app, database, login manager, and error handlers.
- `models.py`: Defines the SQLAlchemy database schema.
- `routes/`: Contains logic for different parts of the application:
  - `auth.py`: Login, logout, and registration.
  - `public.py`: Main visitor pages (Home, Map, Attractions).
  - `admin.py`: LGU administrative dashboard and content management.
  - `barangay.py`: Special routes for Barangay-level content management.
  - `api.py`: JSON endpoints for map data and analytics.
- `utils/`: Helper modules (e.g., `db_manager` for multi-db support).

## Database Schema

The core entities in the system are:

- **User**: Authentication and authorization (Roles: `admin`, `contributor`, `user`).
- **Attraction**: Cultural and tourism spots with geo-coordinates (lat/lng).
- **Event**: Local festivals and community activities.
- **BarangayInfo**: Detailed historical and cultural background for each barangay.
- **GalleryItem**: Photos and videos associated with the culture.
- **PageView**: Internal analytics for tracking popularity.
- **Review**: User ratings and comments for attractions.

## Integration Details

- **Supabase**: Used via the Supabase Python SDK for cloud database and potentially storage interactions.
- **Leaflet.js**: Integrates with Mapbox or OSM tiles to display attraction markers and barangay boundaries.
- **Vercel**: Optimized for serverless deployment with specific handling for temporary file storage and proxy headers.
