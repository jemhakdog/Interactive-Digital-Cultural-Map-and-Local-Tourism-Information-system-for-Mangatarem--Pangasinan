# Codebase Organization Plan

## Current State Analysis
The application is a Flask-based web application for an Interactive Digital Cultural Map and Tourism Information System for Mangatarem, Pangasinan. It has a modular structure with routes, models, and templates but could benefit from better organization.

## Proposed Organizational Structure

### 1. Root Directory Cleanup
- Move configuration files to a dedicated `config/` directory
- Consolidate utility scripts into `scripts/` directory
- Create a proper `.env.example` file for environment variables

### 2. Backend Structure Reorganization
```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── attraction.py
│   │   ├── event.py
│   │   └── ...
│   ├── routes/              # API/blueprint routes
│   │   ├── __init__.py
│   │   ├── public.py
│   │   ├── auth.py
│   │   ├── admin.py
│   │   └── ...
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── attraction_service.py
│   │   └── ...
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── config.py            # Configuration settings
├── migrations/              # Database migrations
├── tests/                   # Test files
└── requirements.txt
```

### 3. Frontend Structure Reorganization
```
frontend/
├── src/
│   ├── css/                 # Source CSS files
│   │   ├── components/
│   │   ├── pages/
│   │   └── globals.css
│   ├── js/                  # Source JavaScript files
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   └── assets/              # Images, videos, etc.
├── dist/                    # Built assets
└── package.json
```

### 4. Templates Restructuring
```
templates/
├── base.html                # Base template
├── partials/                # Reusable components
│   ├── header.html
│   ├── footer.html
│   └── ...
├── public/                  # Public-facing pages
│   ├── index.html
│   ├── map.html
│   └── ...
├── auth/                    # Authentication pages
│   ├── login.html
│   └── register.html
└── admin/                   # Admin pages
    ├── dashboard.html
    ├── attractions/
    └── events/
```

### 5. Data and Content Organization
```
data/
├── seeds/                   # Database seed files
│   ├── attractions.json
│   ├── events.json
│   └── ...
├── uploads/                 # User uploads
│   ├── images/
│   └── videos/
└── reports/                 # Generated reports
```

### 6. Documentation and Configuration
```
docs/
├── architecture.md
├── api.md
├── deployment.md
└── user_manual.md

config/
├── development.py
├── production.py
├── testing.py
└── base.py
```

### 7. Testing Strategy
- Create a comprehensive test suite with unit, integration, and end-to-end tests
- Organize tests by feature/module
- Implement test fixtures and factories

### 8. Deployment and Infrastructure
```
deployment/
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── compose.yaml
├── nginx.conf
└── scripts/
    ├── deploy.sh
    └── backup.sh
```

### 9. Development Tools and Scripts
- Set up pre-commit hooks
- Create development and production environment scripts
- Standardize linting and formatting configurations

### 10. Security and Performance Enhancements
- Implement proper security headers
- Add caching strategies
- Optimize database queries
- Set up monitoring and logging