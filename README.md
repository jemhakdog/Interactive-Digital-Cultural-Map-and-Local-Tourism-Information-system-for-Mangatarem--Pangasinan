# 🗺️ Interactive Digital Cultural Map for Mangatarem, Pangasinan

An interactive, web-based platform showcasing the cultural identity, community highlights, and tourism offerings of Mangatarem, Pangasinan.

## 📍 Project Overview
This platform serves as a central digital resource for residents, students, and visitors to explore the rich cultural heritage and tourism spots of Mangatarem. It emphasizes interactive storytelling through maps and multimedia, promoting local pride and supporting educational use.

## ✨ Key Features
- **Interactive Cultural Map**: Explorer barangay-level highlights using an interactive Leaflet-based map.
- **Tourism Information Portal**: Detailed profiles of local attractions, traditions, and eateries.
- **Events & Festival Directory**: Stay updated with local festivities and community celebrations.
- **Multimedia Gallery**: High-quality photo and video collections of local traditions.
- **Admin & Contributor Dashboard**: Secure management for LGU and barangay representatives to update content.
- **Analytics Dashboard**: Insights into popular locations and user engagement levels.

## 🛠️ Technical Stack
### Backend
- **Framework**: [Flask 3.1.2](https://flask.palletsprojects.com/)
- **Database**: 
  - **Local Development**: SQLite (stored in `/instance/app.db`)
  - **Production**: Supabase (PostgreSQL) with connection pooling
  - **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: [Flask-Login](https://flask-login.readthedocs.io/)
- **Rate Limiting**: [Flask-Limiter](https://flask-limiter.readthedocs.io/)

### Frontend
- **Styling**: [Tailwind CSS 3.4](https://tailwindcss.com/)
- **Interactive Maps**: [Leaflet.js](https://leafletjs.com/)
- **Build Tools**: Terser for JS minification, PostCSS for Tailwind.

### Deployment
- **Platform**: Optimized for [Vercel](https://vercel.com/) (includes `/tmp` SQLite handling).
- **Environment**: Python 3.x

## 🚀 Getting Started
### Prerequisites
- Python 3.8+
- Node.js & npm (for Tailwind/JS build)

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

3. **Setup Frontend Assets**:
   ```bash
   npm install
   npm run build
   ```

### Running Locally
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000`.

## 📚 Documentation
Detailed documentation is available in the [docs/](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/README.md) directory:
- [Architecture Guide](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/architecture.md)
- [API Reference](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/api_reference.md)
- [Deployment Guide](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/deployment_guide.md)
- [User Manual](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/user_manual.md)
- [Administrative Guide](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/admin_guide.md)

## 📂 Project Structure
- `/app.py`: Main application entry point.
- `/models.py`: Database schema and models.
- `/routes/`: Blueprint-based route handling (7 blueprints: Admin, Barangay, Public, Auth, API, User, Update).
- `/templates/`: Jinja2 templates for UI.
- `/static/`: CSS, JS, and uploaded assets.
- `/instance/`: Local database storage.

## 👤 Stakeholders
- **LGU Mangatarem**: Primary beneficiary for tourism promotion.
- **Barangay Representatives**: Local content contributors.
- **Students & Researchers**: For educational and historical reference.
- **Visitors**: Digital guide for tourism.

---
*Built for Mangatarem, Pangasinan.*

