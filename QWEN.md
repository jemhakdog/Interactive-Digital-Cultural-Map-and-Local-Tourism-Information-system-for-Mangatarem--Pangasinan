# QWEN.md — Project Context

## Project Overview

**Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan**

A Flask-based web platform that showcases the cultural identity, community highlights, and tourism offerings of Mangatarem, Pangasinan, Philippines. The platform provides an interactive map experience using Mapbox GL JS, a cultural heritage registry (Forms 01–07), tourism information portal, events directory, multimedia gallery, and admin/contributor dashboards.

### Key Stakeholders
- **LGU Mangatarem** — Primary beneficiary for tourism promotion and cultural archival
- **Barangay Representatives** — Local content contributors
- **Students & Researchers** — Educational and historical reference
- **Visitors** — Digital guide for tourism

---

## Tech Stack

### Backend
- **Framework**: Flask 3.1.2 (application factory pattern)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Database Migrations**: Flask-Migrate (Alembic)
- **Authentication**: Flask-Login
- **Rate Limiting**: Flask-Limiter
- **CSRF Protection**: Flask-WTF CSRF
- **Production Database**: Supabase (PostgreSQL) with connection pooling
- **Development Database**: SQLite (`/instance/app.db`)
- **Caching**: Upstash Redis (optional, for production)
- **Email**: (via `utils/email_sender.py`)

### Frontend
- **Styling**: Tailwind CSS 4.0 (CSS-first configuration)
- **Maps**: Mapbox GL JS with Vector Tile (MVT) support
- **Build Tools**: Tailwind CLI v3.4.17, Terser for JS minification
- **Animations**: AOS (Animate On Scroll) library

### Deployment
- **Primary**: Vercel (serverless Python, edge caching)
- **Alternative**: Cloudflare Workers (wrangler.toml configured)
- **Desktop**: PyInstaller build support (`build/desktop.py`, `build/desktop.spec`)

---

## Project Structure

```
├── app.py                    # Application factory (create_app)
├── config.py                 # Configuration classes (dev/prod/test)
├── extensions.py             # Flask extensions (db, login_manager, limiter, csrf)
├── models.py                 # SQLAlchemy models (20+ models)
├── requirements.txt          # Python dependencies (uv-managed)
├── tailwind.config.js        # Tailwind CSS configuration
├── wrangler.toml             # Cloudflare Workers config
│
├── routes/                   # Blueprint-based route modules
│   ├── __init__.py           # Blueprint registration
│   ├── public.py             # Public-facing pages
│   ├── auth.py               # Authentication routes
│   ├── api.py                # API endpoints
│   ├── map_routes.py         # Map-specific routes
│   ├── business.py           # Business portal routes
│   ├── user.py               # User dashboard routes
│   ├── update.py             # Content update routes
│   ├── admin/                # Admin blueprint
│   └── barangay/             # Barangay admin blueprint
│
├── heritage_models/          # Cultural heritage forms (01-07)
│   ├── natural_heritage.py   # Form 01A
│   ├── built_heritage.py     # Form 02A
│   ├── movable_heritage.py   # Form 03A
│   ├── intangible_heritage.py# Form 04A
│   ├── personality_profile.py# Form 05
│   ├── cultural_institution.py # Form 06
│   └── lgu_culture_program.py # Form 07
│
├── utils/                    # Utility modules
│   ├── db_manager.py         # Database connection manager
│   ├── email_sender.py       # Email utilities
│   ├── geo.py                # Geospatial utilities
│   ├── heritage_registry.py  # Heritage data registry
│   ├── security.py           # Security utilities
│   ├── template_filters.py   # Jinja2 filters (sanitize, encode)
│   ├── tile_generator.py     # MVT tile generation
│   └── validators.py         # Input validation
│
├── templates/                # Jinja2 HTML templates
├── static/                   # Static assets (CSS, JS, images, uploads)
├── data/                     # JSON seed data (attractions, establishments)
├── build/                    # Build scripts (Tailwind, PyInstaller)
├── migrations/               # Alembic database migrations
├── tests/                    # pytest test suite
├── docs/                     # Project documentation
├── scripts/                  # Utility scripts
├── plans/                    # Project plans and specs
├── docker/                   # Docker configuration
├── instance/                 # Local SQLite database
└── archive/                  # Archived code/configs
```

---

## Database Models

Core models defined in `models.py`:
- **User** — User accounts with roles (admin, contributor, user, business_owner)
- **BarangayInfo** — Barangay (village/district) information and geo data
- **Attraction** — Tourism attractions with categories and status workflow
- **Event** — Community events and festivals
- **HeritageProfile** — Base cultural heritage profiles
- **GalleryItem** — Photo/video gallery items
- **Establishment** — Business listings (inns, restaurants, cafes)
- **EstablishmentRoom** — Room listings for accommodations
- **EstablishmentMenuItem** — Menu items for dining establishments
- **EstablishmentReview** — User reviews for establishments
- **AttractionReview** — User reviews for attractions
- **UserFavoriteAttraction** — User favorited attractions
- **UserEventInterest** — User event interest tracking
- **NewsletterSubscriber** — Newsletter subscriptions
- **PasswordResetToken** — Password reset tokens
- **AnalyticsPageView** — Page view analytics
- **DatabaseAuditLog** — Security audit logging

Heritage models (Forms 01–07) are in `heritage_models/`.

---

## Building and Running

### Prerequisites
- Python 3.12+
- uv (Python package manager) — https://github.com/astral-sh/uv
- Internet connection (for library installs)

### Installation
```bash
# Clone and navigate to project
cd Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan

# Create virtual environment and install dependencies with uv
uv venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# Install dependencies
uv pip install -r requirements.txt
```

### Build Frontend Assets
```bash
uv run python build/build.py          # Build Tailwind CSS (minified)
uv run python build/build.py --watch  # Watch mode for development
```

### Run the Application
```bash
uv run python app.py                  # Starts Flask dev server on http://127.0.0.1:5002
```

### Environment Variables
Key environment variables (set via `.env` or platform config):
- `SECRET_KEY` — Application secret key
- `FLASK_ENV` — Environment: `development`, `production`, `testing`
- `DB_PROVIDER` — Database provider: `sqlite` or `supabase`
- `SUPABASE_URL` / `SUPABASE_KEY` — Supabase credentials
- `UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_TOKEN` — Redis caching credentials
- `mapbox_token` — Mapbox access token
- `MAIL_*` — Email configuration variables

### Database Migrations
```bash
uv run flask db migrate -m "description"   # Generate migration
uv run flask db upgrade                    # Apply migrations
uv run flask db downgrade                  # Rollback migration
```

### Running Tests
```bash
uv run pytest tests/                       # Run all tests
uv run pytest tests/test_security.py       # Run specific test file
```

---

## Development Conventions

### Code Style
- **Application Factory Pattern**: `create_app()` in `app.py` centralizes app creation
- **Blueprints**: Routes are organized in `routes/` directory by functional area
- **Model Naming**: Database table names use uppercase (e.g., `USER`, `ATTRACTION`)
- **Status Workflow**: Content items use `status` field (`pending`, `approved`, `rejected`)
- **Role-Based Access**: User roles control access (`admin`, `contributor`, `user`, `business_owner`)

### Security Practices
- **XSS Prevention**: CSP headers, input sanitization (bleach), output encoding (Jinja2 filters: `|sanitize`, `|escape_strict`, `|safe_url`)
- **Session Security**: HttpOnly cookies, SameSite=Lax, Secure flag in production
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, HSTS, Referrer-Policy, Permissions-Policy
- **CSRF Protection**: Flask-WTF CSRF tokens on all forms
- **File Uploads**: Double filename sanitization + extension validation
- **Rate Limiting**: On authentication endpoints
- **Audit Logging**: `DatabaseAuditLog` model tracks CRUD operations

### Template Conventions
- All templates use Jinja2 with custom security filters
- Mapbox token injected via context processor (`mapbox_token`)
- Error pages in `templates/errors/` (400, 401, 403, 404, 429, 500, 451)

### Testing Practices
- Tests use pytest with Flask test client
- `conftest.py` provides shared fixtures
- Test coverage includes security, email, MVT implementation, SQL injection prevention, and Vercel performance

---

## Deployment

### Vercel (Primary)
- Optimized for Vercel serverless Python
- Edge caching for static assets and API responses
- Redis caching via Upstash for performance
- `VERCEL` environment variable triggers production behavior

### Cloudflare Workers (Alternative)
- Configured via `wrangler.toml`
- Python Workers compatibility
- Static assets served via Cloudflare edge

### Desktop Application
- PyInstaller build support in `build/`
- `flaskwebgui` for desktop app wrapper (platform-dependent version)

---

## Key Configuration Files

| File | Purpose |
|------|---------|
| `app.py` | Application factory, error handlers, security headers, seeding |
| `config.py` | Development/Production/Testing configurations |
| `extensions.py` | Flask extensions initialization |
| `models.py` | SQLAlchemy model definitions |
| `tailwind.config.js` | Tailwind CSS with custom colors, fonts, animations |
| `wrangler.toml` | Cloudflare Workers deployment config |
| `requirements.txt` | Python dependencies (autogenerated by uv) |

---

## Default Credentials (Development)
- **Admin**: `admin` / `admin123`
- **Dining Owner**: `dining_owner` / `dining123`
- **Hospitality Owner**: `hospitality_owner` / `hospitality123`

> ⚠️ These are seeded automatically on first run. Change them in production.

---

## Documentation

Core documentation is available in `docs/`:
- `docs/README.md` — Project overview and getting started
- `docs/architecture.md` — System architecture
- `docs/database_migration.md` — Database migration guide
- `docs/api_reference.md` — API documentation
- `docs/user_manual.md` — User guide
- `docs/admin_guide.md` — Administration guide
- `docs/contributor_guide.md` — Contributor guidelines
- `docs/SECURITY_IMPLEMENTATION.md` — Security architecture
- `docs/SECURITY_BEST_PRACTICES.md` — Developer security guidelines
- `docs/MVT_IMPLEMENTATION.md` — Mapbox Vector Tiles implementation
- `docs/TESTING_GUIDE.md` — Testing procedures
