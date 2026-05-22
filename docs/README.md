# 🗺️ Interactive Digital Cultural Map for Mangatarem, Pangasinan

An interactive, web-based platform showcasing the cultural identity, community highlights, and tourism offerings of Mangatarem, Pangasinan.

## 📍 Project Overview
This platform serves as a central digital resource for residents, students, and visitors to explore the rich cultural heritage and tourism spots of Mangatarem. It emphasizes interactive storytelling through maps and multimedia, promoting local pride and supporting educational use.

## ✨ Key Features
- **CBIS Community Stewardship**: Barangay Representatives can manage all cultural assets within their community jurisdiction through a shared heritage model.
- **Harmonized PGIS Map**: Integrated view of Attractions and Events with auto-fit framing and dual-marker iconography.
- **Interactive Cultural Map**: Explore barangay-level highlights using Mapbox GL JS with vector tile rendering and mobile-responsive interactions.
- **Cultural Heritage Registry**: Full implementation of standardized Heritage Forms 01-07 for deep historical archival.
- **Tourism Information Portal**: Detailed profiles of local attractions, traditions, and eateries.
- **Multimedia Gallery**: High-quality photo and video collections of local traditions.
- **Administrative & Stakeholder Portal**: Secure unified management for LGU (Tourism Office) and Barangay Representatives to review, verify, and update municipal content.
- **Analytics Dashboard**: Insights into popular locations and user engagement levels.

## 🛠️ Technical Stack
### Backend
- **Framework**: [Flask 3.1.2](https://flask.palletsprojects.com/)
- **Database**: 
  - **Local Development**: SQLite (stored in `/instance/app.db`)
  - **Production**: Supabase (PostgreSQL) with connection pooling (Port 6543)
  - **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: [Flask-Login](https://flask-login.readthedocs.io/)
- **Rate Limiting**: [Flask-Limiter](https://flask-limiter.readthedocs.io/)

### Frontend
- **Styling**: [Tailwind CSS 4.0](https://tailwindcss.com/) (Vanilla CSS engine)
- **Interactive Maps**: [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js) with Vector Tile (MVT) support
- **Build Tools**: PostCSS and Terser for optimized production assets.

### Deployment
- **Platform**: Optimized for [Vercel](https://vercel.com/) with Edge Caching and ProxyFix support.
- **Environment**: Python 3.12+

## 🛡️ Security Features

This platform implements comprehensive security measures to protect against common web vulnerabilities:

### XSS Prevention
- **Content Security Policy (CSP)**: Restricts resource loading to trusted sources only
- **Input Sanitization**: All user inputs validated and sanitized using the `bleach` library
- **Output Encoding**: Context-aware encoding via custom Jinja2 filters (`|sanitize`, `|escape_strict`, `|safe_url`)
- **Defense-in-Depth**: 6 layers of protection against injection attacks

### Session Security
- **HttpOnly Cookies**: Prevents JavaScript access to session cookies
- **SameSite=Lax**: Protects against cross-site request forgery (CSRF)
- **Secure Flag**: Enforced in production (HTTPS only)

### Additional Protections
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, HSTS, Referrer-Policy
- **File Upload Security**: Double filename sanitization + extension validation
- **Rate Limiting**: Prevents brute-force attacks on authentication endpoints
- **CSRF Protection**: Flask-WTF CSRF tokens on all forms

📖 **Learn More**: [Security Implementation Guide](SECURITY_IMPLEMENTATION.md) | [Developer Best Practices](SECURITY_BEST_PRACTICES.md)

---

## 🚀 Getting Started
### Prerequisites
- Python 3.12+
- Internet connection (for initial library installs)

### Installation
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Mangatarem-Cultural-Map
   ```

2. **Setup Python Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Build Frontend Assets**:
   ```bash
   python build/build.py
   ```

### Running Locally
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000`.

## 📚 Documentation

### Core Documentation
- [Architecture Guide](architecture.md)
- [Database Migration](database_migration.md)
- [API Reference](api_reference.md)
- [User Manual](user_manual.md)
- [Administrative Guide](admin_guide.md)
- [Contributor Guide](contributor_guide.md)
- [Performance Optimization](optimization.md)
- [Redis Caching & Security](REDIS_CACHING_SYSTEM.md)

### Security Documentation
- [Security Implementation Guide](SECURITY_IMPLEMENTATION.md) - Comprehensive security architecture and implementation details
- [Developer Security Best Practices](SECURITY_BEST_PRACTICES.md) - Guidelines for developers on secure coding practices
- [Deployment Security Checklist](DEPLOYMENT_SECURITY_CHECKLIST.md) - Pre-deployment and post-deployment security verification

### Technical Documentation
- [MVT Implementation](MVT_IMPLEMENTATION.md) - Mapbox Vector Tiles implementation
- [Real-Time Routing & Navigation](ROUTING_NAVIGATION.md) - Directions API and Car Icon Integration
- [Testing Guide](TESTING_GUIDE.md) - Testing procedures and test coverage
- [Bug Fix: LngLat NaN Error](BUGFIX_lnglat_nan_error.md) - Bug fix documentation

## 📂 Project Structure
- `/app.py`: Main application entry point and factory.
- `/models.py`: Database schema (20+ models including Heritage Registry).
- `/routes/`: Blueprint-based route handling (Admin, Barangay, Public, Auth, API, User, Update).
- `/heritage_models/`: Specialized models for Forms 01-07.
- `/templates/`: Jinja2 templates for UI.
- `/static/`: CSS, JS, and uploaded assets.
- `/utils/`: Core utility modules (Registry, DB Manager, Email Sender).

## 👥 User Categories
- **Category 1: Administrative and Stakeholders**: LGU Tourism Office (Primary Stakeholder/Admin) and Barangay Representatives (Contributors) responsible for data governance.
- **Category 2: General Public and Academic Users**: Tourists, Visitors, Students, and Researchers who utilize the platform for exploration and reference.

---
*Built for Mangatarem, Pangasinan.*

