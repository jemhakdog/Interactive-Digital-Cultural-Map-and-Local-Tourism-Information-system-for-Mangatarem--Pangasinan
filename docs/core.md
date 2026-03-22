# Core System Overview

The **Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan** is a GIS-based platform designed to document, map, and promote the cultural, historical, and tourism assets of Mangatarem.

## System Goals

- **Documentation**: Digitally preserve Mangatarem's cultural heritage.
- **Mapping**: Provide an interactive GIS interface for tourists and locals.
- **Sustainability**: Enable barangay-level contributors to maintain asset accuracy.
- **Standardization**: Align with national tourism and heritage registry standards (Forms 01-07).

---

## Tech Stack (2025 Edition)

- **Backend**: Python 3.12+ / Flask 3.1+
- **Database**: 
  - **Development**: SQLite (`instance/app.db`)
  - **Production**: Supabase PostgreSQL (Managed)
- **Frontend**: Jinja2 / Tailwind CSS 4.0 / Vanilla JS
- **Mapping**: Leaflet.js
- **Deployment**: Vercel (Edge Optimized)

---

## Database Models and Structure

The system utilizes 19+ core database models:

### 1. User Management
- `USER`: Handles authentication and roles (`admin`, `contributor`, `user`).
- `PASSWORD_RESET_TOKEN`: Secure account recovery.

### 2. Tourism and Map Data
- `ATTRACTION`: Geo-located points of interest (coordinates: `latitude`, `longitude`).
- `EVENT`: Community activities and festivals.
- `BARANGAY_INFO`: Cultural background profiles for each barangay.

### 3. Cultural Heritage Registry (Structured Data)
- `HERITAGE_PROFILE`: Base registry model.
- **Form 01A - 07 Details**: 7 specialized detail models for Natural, Built, Movable, Intangible Heritage, Personality Profiles, Cultural Institutions, and LGU Programs.

### 4. User Engagement
- `FAVORITE`: Personal bookmarks.
- `EVENT_INTEREST`: Event RSVPs.
- `REVIEW`: Community feedback and ratings.
- `ANALYTICS_PAGE_VIEW`: Internal engagement telemetry.

---

## Key Features

### Interactive GIS Cultural Map
A real-time mapping interface built on Leaflet.js that identifies attractions, heritage sites, and events with marker clustering and custom barangay boundaries.

### Cultural Heritage Registry (Forms 01-07)
A first-of-its-kind digital implementation of the standardized heritage forms, allowing for complex data entry and structured archival of local history.

### Barangay Contributor Workflow
Distributed content management where each barangay can update its own historical and cultural data, subject to administrative review.

### Edge-Optimized Deployment
Tailored for Vercel with smart caching, ProxyFix for reverse proxy headers, and lazy-loading for heavy database drivers to ensure sub-second cold starts.