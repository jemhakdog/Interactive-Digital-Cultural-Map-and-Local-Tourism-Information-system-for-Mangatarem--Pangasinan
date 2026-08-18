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

- **Backend**: Flask (Python 3.11+) with SQLAlchemy ORM.
- **Real-Time**: Flask-SocketIO (WebSockets powered by Eventlet).
- **Caching**: Redis support for session caching and rate-limiting.
- **Storage/Auth Support**: Supabase integration for media assets and external authentication options.
- **Frontend**: HTML5, Vanilla CSS, Tailwind CSS v4, JavaScript.
- **Database**: SQLite (default for development/testing), PostgreSQL support for production deployments.
- **Package Manager**: Astral `uv` for environment virtualenv management and rapid dependency installation.

---

## How to Run the System

Follow these steps to set up and run the system locally:

1. **Install uv:**
   Open PowerShell and run the following command to install the `uv` package manager:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   Once done, proceed to the next step.

2. **Get the code (Clone or Download):**
   - **Option A: Clone the repository (Recommended)**
     ```bash
     git clone https://github.com/jemhakdog/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan.git
     cd Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan
     ```
   - **Option B: Download the ZIP**
     Alternatively, you can download the source code as a ZIP archive:
     [Download Source Code (ZIP)](https://github.com/jemhakdog/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/archive/refs/tags/v0.5.0.zip) and extract it to your preferred directory.

3. **Install dependencies:**
   Open a **new** command prompt (`cmd`), navigate to the project folder, and run:
   ```cmd
   uv sync
   ```

4. **Run the system:**
   Start the application by running:
   ```bash
   uv run app.py
   ```
   The Flask application will start on `http://127.0.0.1:5002` (configurable via `app.py`).

---

## Environment Configuration

Create a `.env` file in the root directory and configure the environment variables as needed:

```ini
FLASK_ENV=development
SECRET_KEY=your-secure-secret-key
DATABASE_URL=sqlite:///mangatarem_map.db
# (Optional) REDIS_URL for Redis Caching
# (Optional) SUPABASE_URL & SUPABASE_KEY for Media Storage/Auth
```

---

## Database Seed Data

The system comes equipped with automatic database seeding. During local execution, the application initializes and seeds default information, which includes:
- Municipal barangays of Mangatarem.
- Pre-configured tourist attractions and heritage sites.
- Sample local business listings.
- Standard gamification badges.

You can manually trigger database resets or seeding using utility scripts in the project:
```bash
uv run reset_db.py
uv run seed_new_data.py
```

---

## Security Features

- **XSS Protection**: Secure HTML output escaping using Bleach filters.
- **CSRF Protection**: Flask-WTF CSRF protection enabled globally.
- **SQL Injection Prevention**: Safe SQLAlchemy parameter bind syntax.
- **Session Security**: HttpOnly and SameSite cookie policies enforced.
- **Rate Limiting**: Flask-Limiter configured for auth routes to prevent brute-force attacks.
