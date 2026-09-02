# Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan

A comprehensive, interactive web platform dedicated to cultural mapping, heritage preservation, and local tourism promotion for the municipality of **Mangatarem, Pangasinan, Philippines**.

This system helps tourists, researchers, and locals explore Mangatarem's rich history, discover local attractions and businesses, plan travel routes, book guides or accommodations, interact in real-time forums, and participate in gamified cultural exploration.

---

## Table of Contents

- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [How to Run the System](#how-to-run-the-system)
- [Environment Configuration](#environment-configuration)
- [Database Seed Data](#database-seed-data)
- [Security Features](#security-features)

---

## Key Features

- 🗺️ **Interactive Digital Cultural Map**: Dynamic visualization of barangays, heritage sites, local attractions, and businesses.
- 🏛️ **Heritage & Cultural Profile**: Comprehensive records of local history, cultural properties, historical facts, and barangay information.
- 🌴 **Tourism & Attractions Directory**: Complete directory of tourist spots, natural landscapes, and historical locations with reviews, photos, and ratings.
- 💼 **Local Establishments & Businesses**: Verified directories for accommodations, restaurants, stores, and local tour guides, including menu/room booking details.
- 📅 **Events & Festivals**: Local festival calendars, barangay events, and community activities.
- 🗺️ **Smart Routing & Navigation**: Interactive route optimization tool helping visitors discover the most efficient paths between local spots.
- 💬 **Real-Time Community Chat**: Built-in chat module using WebSockets (Socket.io) for discussion channels and tourist inquiries.
- 🎟️ **Booking & Reservations**: Built-in asset booking slots for scheduling guides, room reservations, and activity bookings.
- 🏅 **Gamification Engine**: Explore Mangatarem to earn achievement badges, check-in to locations, and unlock achievements.
- 📊 **Administration & Analytics**: Administrative dashboards for local government and tourism offices with user audit logs, page views, and visitor metrics.

---

## System Architecture

The application is built using a **Modular Monolith** structure, separating domain models, business logic, routes, and views into self-contained modules located in the `modules/` directory:

- **auth**: User registration, role-based login (Tourists, Business Owners, Tour Guides, Admin), password resets.
- **barangay**: Cultural profiles, festival schedules, and local history for Mangatarem's barangays.
- **attractions**: Management of tourist spots, reviews, rating aggregates, and favorites.
- **business**: Directory for accommodations, dining, retail, and local tour guides, including rooms and menu listings.
- **heritage**: Cultural heritage documentation, profile questionnaires, and history logs.
- **booking**: Resource scheduling for rooms, tour guides, and activities.
- **chat**: WebSocket-based chatrooms for real-time discussion and inquiries.
- **gamification**: Badge creation, user check-ins, leaderboards, and tourist passports.
- **analytics**: Traffic monitoring, visitor counts, page views, and administrative audit logs.
- **routing**: Tour itinerary planning and route optimization.
- **notifications**: Event updates and newsletter distribution.

---

## Technology Stack

- **Backend**: FastAPI (Python 3.11+) with async SQLAlchemy ORM, served by uvicorn.
- **API**: REST under `/api/*` (19 routers), auto docs at `/docs`.
- **Frontend**: Next.js (React 19) + Tailwind CSS v4 + MapLibre GL for the interactive map.
- **Database**: SQLite (default for development/testing, stored in `instance/mangatarem.db`).
- **Package Manager**: Astral `uv` for environment management and dependency installation.

---

## How to Run the System

1. **Install uv:**
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Get the code (Clone or Download):**
   ```bash
   git clone https://github.com/jemhakdog/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan.git
   cd Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   cd frontend && npm install && cd ..
   ```

4. **Run the system (backend + frontend):**
   ```bash
   npm run dev
   ```
   - Backend (FastAPI): `http://127.0.0.1:8000` — API docs at `http://127.0.0.1:8000/docs`
   - Frontend (Next.js): `http://127.0.0.1:3000`

   Or run separately:
   ```bash
   npm run dev:backend   # uvicorn backend.app.main:app --port 8000
   npm run dev:frontend  # Next.js dev server
   ```

---

## Environment Configuration

Create a `.env` file in the root directory and configure the environment variables as needed:

```ini
SECRET_KEY=your-secure-secret-key
# Optional overrides (defaults shown):
# DATABASE_URL=sqlite:///instance/mangatarem.db
# CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

---

## Database

Tables are created automatically on startup (`create_all`) in development. The schema lives in `backend/app/models/`.

---

## Security Features

- **Authentication**: JWT (python-jose) access tokens + Google OAuth sign-in.
- **Password Storage**: Werkzeug password hashing (bcrypt via passlib for legacy hashes).
- **Input Validation**: Pydantic schemas validate all request bodies at the API boundary.
- **File Uploads**: Extension + size whitelist on upload endpoints (`/api/uploads`).
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries.
