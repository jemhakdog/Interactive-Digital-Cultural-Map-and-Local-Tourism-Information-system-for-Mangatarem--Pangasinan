# 🗺️ Interactive Digital Cultural Map for Mangatarem, Pangasinan

An interactive, web-based platform showcasing the cultural identity, community highlights, and tourism offerings of Mangatarem, Pangasinan.

## 📍 Project Overview
This platform serves as a central digital resource for residents, students, and visitors to explore the rich cultural heritage and tourism spots of Mangatarem. It emphasizes interactive storytelling through maps and multimedia, promoting local pride and supporting educational use.

## ✨ Key Features
- **Interactive Cultural Map**: Explore barangay-level highlights using Mapbox GL JS with vector tile rendering for high-performance display.
- **High-Concurrency Map Architecture**: Mapbox Vector Tiles (MVT) generated via PostGIS ST_AsMVT with Vercel Edge Caching and Redis caching layers.
- **Cultural Heritage Registry**: Full implementation of standardized Heritage Forms 01-07 for deep historical archival.
- **Tourism Information Portal**: Detailed profiles of local attractions, traditions, and eateries.
- **Events & Festival Directory**: Stay updated with local festivities and community celebrations.
- **Multimedia Gallery**: High-quality photo and video collections of local traditions.
- **Admin & Contributor Dashboard**: Secure management for LGU and barangay representatives to review and update content.
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
Detailed documentation is available in the [docs/](docs/README.md) directory:
- [Architecture Guide](docs/architecture.md)
- [Database Migration](docs/database_migration.md)
- [API Reference](docs/api_reference.md)
- [User Manual](docs/user_manual.md)
- [Administrative Guide](docs/admin_guide.md)
- [Contributor Guide](docs/contributor_guide.md)
- [Performance Optimization](docs/optimization.md)

## 📂 Project Structure
- `/app.py`: Main application entry point and factory.
- `/models.py`: Database schema (20+ models including Heritage Registry).
- `/routes/`: Blueprint-based route handling (Admin, Barangay, Public, Auth, API, User, Update).
- `/heritage_models/`: Specialized models for Forms 01-07.
- `/templates/`: Jinja2 templates for UI.
- `/static/`: CSS, JS, and uploaded assets.
- `/utils/`: Core utility modules (Registry, DB Manager, Email Sender).

## 👤 Stakeholders
- **LGU Mangatarem**: Primary beneficiary for tourism promotion and cultural archival.
- **Barangay Representatives**: Local content contributors.
- **Students & Researchers**: For educational and historical reference.
- **Visitors**: Digital guide for tourism.

---
*Built for Mangatarem, Pangasinan.*

