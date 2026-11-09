# Mangatarem Cultural Map & Tourism Information System Blueprint

## System Overview
A full-stack municipal digital cultural mapping, heritage preservation, and tourism information platform for Mangatarem, Pangasinan, Philippines. It integrates an asynchronous Python/FastAPI backend, Supabase/PostgreSQL and local SQLite data layers, and a Next.js (React 19) App Router frontend with MapLibre GL geospatial rendering.

## Local Interface & Invariants
- Dev orchestration scripts:
  - `dev.sh` / `dev.bat` / `dev.ps1`: Concurrently launches FastAPI backend (`uvicorn backend.app.main:app`) on port 8000 and Next.js frontend on port 3000.
  - Root `package.json`: NPM runner scripts (`dev`, `dev:backend`, `dev:frontend`, `build`).
- Root Invariants:
  - Python virtual environment runs on Python >=3.11 with dependencies managed in `pyproject.toml`.
  - Next.js web application is located in `frontend/` and communicates with the backend via `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`).

## Subdirectories & System Boundaries
- [`backend`](./backend/README.md): FastAPI service application blueprint (routers, core settings, database pooling, declarative models, and Pydantic schemas).
- [`frontend`](./frontend/README.md): Next.js 16+ App Router web portal, MapLibre GL mapping components, and authentication context.
- [`api`](./api/README.md): Vercel serverless ASGI entrypoint bridging Vercel Python runtime to `backend.app.main:app`.
- [`db_schemas`](./db_schemas/README.md): Relational PostgreSQL/Supabase DDL schema specifications, constraints, and indexes.

## Global Invariants
- **Database Connection Strategy**: Asynchronous dialect (`sqlite+aiosqlite:///` locally or `postgresql+asyncpg:///` in production via Supabase transaction pooler port 6543 with `statement_cache_size=0`).
- **Security & Authorization**: Bearer JWT tokens with HMAC SHA-256 signing via `SECRET_KEY`, Google OAuth token verification, and role-based access control (`admin`, `contributor`, `business_owner`, `user`).
- **Geospatial & Fallback Resilience**: Map visualization utilizes MapLibre GL with Carto basemaps; falls back gracefully to curated local static points if backend is cold.

## Global Side Effects
- Mutates relational tables (PostgreSQL/SQLite) across 19 domain subsystems.
- Stores uploaded media files locally in `backend/uploads/` (or cloud storage bucket).
- Communicates with Google OAuth verification services.

## System Verification
- Backend tests: `.venv/bin/pytest tests/`
- Frontend build & validation: `cd frontend && npm run build && npm run lint`
- End-to-end dev runner: `npm run dev`

---

## Architectural Notes (Preserved)

### Key Features
- 🗺️ **Interactive Digital Cultural Map**: Dynamic visualization of barangays, heritage sites, local attractions, and businesses.
- 🏛️ **Heritage & Cultural Profile**: Comprehensive records of local history, cultural properties, historical facts, and barangay information.
- 🌴 **Tourism & Attractions Directory**: Complete directory of tourist spots, natural landscapes, and historical locations with reviews, photos, and ratings.
- 💼 **Local Establishments & Businesses**: Verified directories for accommodations, restaurants, stores, and local tour guides, including menu/room booking details.
- 📅 **Events & Festivals**: Local festival calendars, barangay events, and community activities.
- 🗺️ **Smart Routing & Navigation**: Interactive route optimization tool helping visitors discover the most efficient paths between local spots.
- 💬 **Real-Time Community Chat**: Chat module for discussion channels and tourist inquiries.
- 🎟️ **Booking & Reservations**: Built-in asset booking slots for scheduling guides, room reservations, and activity bookings.
- 🏅 **Gamification Engine**: Explore Mangatarem to earn achievement badges, check-in to locations, and unlock achievements.
- 📊 **Administration & Analytics**: Administrative dashboards for local government and tourism offices with user audit logs, page views, and visitor metrics.

### Technology Stack
- **Backend**: FastAPI (Python 3.11+) with async SQLAlchemy ORM, served by uvicorn.
- **API**: REST under `/api/*` (19 routers), auto docs at `/docs`.
- **Frontend**: Next.js (React 19) + Tailwind CSS v4 + MapLibre GL for the interactive map.
- **Database**: SQLite (default for development/testing, stored in `instance/mangatarem.db`) and PostgreSQL (Supabase) in production.
- **Package Manager**: Astral `uv` and `npm`.
