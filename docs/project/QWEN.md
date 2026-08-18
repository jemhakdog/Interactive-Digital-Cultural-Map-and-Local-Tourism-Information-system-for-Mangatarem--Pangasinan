# Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan

## Project Overview

This is a web-based interactive platform designed to showcase the cultural identity, community highlights, and tourism offerings of Mangatarem, Pangasinan. The application serves as a central digital resource for residents, students, and visitors to explore the rich cultural heritage and tourism spots of Mangatarem through an interactive map and multimedia content.

### Key Features
- **Interactive Cultural Map**: Explorer barangay-level highlights using an interactive Leaflet-based map
- **Tourism Information Portal**: Detailed profiles of local attractions, traditions, and eateries
- **Events & Festival Directory**: Stay updated with local festivities and community celebrations
- **Multimedia Gallery**: High-quality photo and video collections of local traditions
- **Admin & Contributor Dashboard**: Secure management for LGU and barangay representatives to update content
- **Analytics Dashboard**: Insights into popular locations and user engagement levels

## Technical Architecture

### Backend Technologies
- **Framework**: Flask 3.1.2
- **Database**: SQLite (Local) / PostgreSQL/MySQL compatible via SQLAlchemy
- **Authentication**: Flask-Login
- **Rate Limiting**: Flask-Limiter
- **ORM**: SQLAlchemy
- **Migrations**: Flask-Migrate

### Frontend Technologies
- **Styling**: Tailwind CSS 3.4
- **Interactive Maps**: Leaflet.js
- **Build Tools**: Terser for JS minification, PostCSS for Tailwind processing
- **Fonts**: Noto Sans TC and Noto Serif TC

### Deployment
- **Platform**: Optimized for Vercel (includes `/tmp` SQLite handling)
- **Environment**: Python 3.x

## Project Structure

```
├── app.py                  # Main application entry point
├── models.py               # Database schema and models
├── extensions.py           # Flask extensions initialization
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies and build scripts
├── pyproject.toml          # Project metadata and dependencies
├── tailwind.config.js      # Tailwind CSS configuration
├── wrangler.toml           # Cloudflare Workers configuration
├── CHANGES.md              # Change log
├── README.md               # Project documentation
├── data/
│   └── attractions.json    # Sample attractions data
├── routes/                 # Blueprint-based route handling
│   ├── __init__.py         # Blueprint registration
│   ├── admin.py            # Admin routes
│   ├── api.py              # API routes
│   ├── auth.py             # Authentication routes
│   ├── barangay.py         # Barangay-specific routes
│   ├── public.py           # Public-facing routes
│   ├── update.py           # Update routes
│   └── user.py             # User routes
├── templates/              # Jinja2 templates organized by feature
│   ├── admin/              # Admin dashboard templates
│   ├── auth/               # Authentication templates
│   ├── barangay/           # Barangay templates
│   ├── errors/             # Error page templates
│   ├── includes/           # Reusable template components
│   ├── pagez/              # Page templates
│   ├── user/               # User templates
│   ├── users/              # Additional user templates
│   └── base.html           # Base template
├── static/                 # Static assets
│   ├── css/                # Stylesheets
│   ├── fonts/              # Font files
│   ├── img/                # Image assets
│   ├── js/                 # JavaScript files
│   ├── uploads/            # Uploaded content
│   ├── vendor/             # Third-party libraries
│   ├── favicon.ico         # Favicon
│   ├── manifest.json       # PWA manifest
│   └── sw.js               # Service worker
├── docs/                   # Documentation
├── migrations/             # Database migration files
├── tests/                  # Test files
└── utils/                  # Utility modules
```

## Database Models

The application uses SQLAlchemy ORM with the following main models:

- **User**: User accounts with roles (admin, contributor, user)
- **Attraction**: Tourism spots with location, description, and approval status
- **Event**: Local events and festivals
- **GalleryItem**: Photos and videos
- **BarangayInfo**: Information about each barangay
- **PageView**: Analytics tracking
- **Favorite**: User favorites
- **EventInterest**: User interest in events
- **Review**: User reviews and ratings

## Building and Running

### Prerequisites
- Python 3.8+
- Node.js & npm (for Tailwind/JS build)

### Installation Steps
1. Setup Python Environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Setup Frontend Assets:
   ```bash
   npm install
   npm run build
   ```

### Running Locally
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000`.

### Build Commands
- `npm run build:css`: Builds and minifies CSS using Tailwind
- `npm run build:js`: Minifies JavaScript using Terser
- `npm run build`: Runs both CSS and JS builds

## Development Conventions

### Code Style
- Python: Follows PEP 8 standards
- JavaScript: Standard formatting
- HTML/CSS: Consistent indentation and semantic markup

### Naming Conventions
- Python: snake_case for variables and functions
- JavaScript: camelCase for variables and functions
- Database: snake_case for table and column names

### Security Practices
- Password hashing using Werkzeug security utilities
- Session management with secure cookies in production
- Rate limiting to prevent abuse
- Input validation and sanitization

### Testing
- Unit tests in the `tests/` directory
- Integration tests for critical workflows
- Database seeding functions for development environments

## Stakeholders

- **LGU Mangatarem**: Primary beneficiary for tourism promotion
- **Barangay Representatives**: Local content contributors
- **Students & Researchers**: For educational and historical reference
- **Visitors**: Digital guide for tourism

## Special Features

### Database Seeding
The application includes automatic database seeding with sample attractions, admin, and contributor accounts when run locally.

### Responsive Design
Built with Tailwind CSS for responsive layouts that work on mobile, tablet, and desktop devices.

### Progressive Web App (PWA)
Includes service worker and manifest for offline functionality and app-like experience.

### Content Moderation
Multi-tier approval system for attractions, events, and gallery items submitted by contributors.