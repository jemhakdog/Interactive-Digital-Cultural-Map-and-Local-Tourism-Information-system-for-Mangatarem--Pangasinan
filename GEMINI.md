# GEMINI.md - Mangatarem Interactive Digital Cultural Map

> This file serves as the central intelligence hub and context anchor for the **Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan**.

---

## 🏛️ PROJECT INFORMATION

- **Project Name**: Interactive Digital Cultural Map for Mangatarem, Pangasinan
- **Objective**: To provide a centralized, interactive, and community-driven platform for mapping cultural heritage, local attractions, and tourism information for the municipality of Mangatarem.
- **Methodology**: **RAD (Rapid Application Development)** - Prioritizing iterative prototyping and community feedback.
- **Core Philosophy**: **Shared Heritage Stewardship** - Decentralized data management at the barangay level (CBIS Model).

---

## 💻 TECH STACK

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.12+, Flask 3.1.2, Gunicorn/Waitress |
| **Database** | **PostgreSQL (Supabase)** for Production, **SQLite** for Local Development |
| **Caching** | **Upstash Redis** (Edge Caching), Vercel Edge Cache |
| **Frontend** | Jinja2 Templates, **Tailwind CSS v4.0**, Mapbox GL JS |
| **Mapping** | **Mapbox Vector Tiles (MVT)** generated via PostGIS `ST_AsMVT` |
| **Infrastructure** | **Vercel** (Serverless), GitHub Actions |
| **Auth/Security** | Flask-Login, Flask-WTF (CSRF), Flask-Limiter, Werkzeug |

---

## 📁 DIRECTORY STRUCTURE

```text
capstone_system/
├── app.py                  # Application Factory & Vercel Entry Point
├── config.py               # Environment-based Configuration
├── extensions.py           # Flask Extensions (DB, Login, Limiter, CSRF)
├── models.py               # Core Model Shim (Import Hub)
├── modules/                # FEATURE MODULES (Logic + Models)
│   ├── analytics/          # Page views & Audit Logs
│   ├── attractions/        # Tourism Spots & Reviews
│   ├── auth/               # User Models & Permission Logic
│   ├── barangay/           # Barangay-level stewardship (CBIS)
│   ├── business/           # Hospitality & Dining (Rooms, Menus)
│   ├── events/             # Local Festivals & Interest Tracking
│   ├── heritage/           # Cultural Heritage Registry Logic
│   └── notifications/      # Newsletter & User Alerts
├── routes/                 # MODULAR BLUEPRINTS
│   ├── admin/              # Multi-module Admin Dashboard
│   ├── api/                # Public & Heritage Registry JSON APIs
│   ├── auth.py             # Authentication Routes
│   ├── map_routes.py       # Mapbox & MVT Tile Endpoints
│   └── public.py           # Visitor Pages (Home, Explore, Barangay)
├── heritage_models/        # Detailed Heritage Forms (01-07)
├── static/                 # CSS (Tailwind), JS, & Uploaded Media
├── templates/              # Jinja2 Layouts & Component Fragments
├── docs/                   # Technical & User Documentation
└── instance/               # Local SQLite Database (Local only)
```

---

## 🚀 MODULES & FUNCTIONALITIES

### 1. Interactive Cultural Map
- **High-Concurrency Tiles**: Directly serving MVT from PostgreSQL for < 50ms rendering.
- **Participatory GIS (PGIS)**: Dynamic layer integration of attractions and events.
- **Intelligent Framing**: Automatic zoom/bounds adjustment for barangay-specific views.

### 2. Cultural Heritage Registry (Forms 01-07)
- **National Standards**: Full implementation of cultural heritage documentation.
- **Heritage Profiles**: Comprehensive tracking of natural, built, movable, and intangible heritage.

### 3. Local Tourism & Business Directory
- **Establishments**: Dining and hospitality management (Business Owner Role).
- **Commerce Features**: Menu items, room availability, and price ranges.

### 4. Community Stewardship (CBIS)
- **Barangay Representatives**: Local stewards manage assets within their jurisdiction.
- **Harmonized Assets**: Unified view of community-driven mapping and official records.

### 5. Security & Performance
- **Content Security Policy (CSP)**: Strict protection against XSS and injection.
- **Lazy-Loading**: Supabase client initialization optimized for serverless cold starts.
- **Edge Caching**: Global distribution of assets and dynamic content via Vercel Edge.

---

## 🧠 AI OPERATIONAL PROTOCOL

> 🔴 **MANDATORY FOR AGENTS**: Before performing ANY implementation, read `docs/architecture.md` and `CODEBASE.md`.

1. **Modular Consistency**: Always maintain the separation of logic between `modules/` and `routes/`.
2. **Database Integrity**: Respect the `models.py` shim. Do not define models directly in root; use specialized module files.
3. **Security First**: Ensure all new routes apply appropriate decorators (`@login_required`, `@role_required`) and CSRF protection.
4. **Clean UI**: Follow the design tokens defined in the `design-system/` and Tailwind v4.0 patterns.

---
