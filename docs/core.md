Comprehensive Analysis: Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan
Based on my analysis of the codebase, I can provide you with a detailed explanation of this capstone project:

Core Goal and Purpose
The Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan is a web-based platform designed to showcase the cultural identity, community highlights, and tourism offerings of Mangatarem, Pangasinan. The system serves as a central digital resource for residents, students, and visitors to explore the rich cultural heritage and tourism spots of Mangatarem through an interactive map and multimedia content.

The primary purpose is to promote local tourism, preserve cultural heritage, and provide an accessible digital platform for discovering Mangatarem’s attractions and cultural assets.

Technology Stack
Backend Technologies
Framework: Flask 3.1.2 (Python web framework)
Database: SQLite (local development) with compatibility for PostgreSQL/MySQL via SQLAlchemy ORM
Authentication: Flask-Login for user session management
Rate Limiting: Flask-Limiter to prevent abuse
ORM: SQLAlchemy for database abstraction
Migrations: Flask-Migrate for database schema versioning
Environment Management: python-dotenv for configuration
Frontend Technologies
Styling: Tailwind CSS 3.4 for responsive design
Interactive Maps: Leaflet.js for mapping functionality
Build Tools: Terser for JavaScript minification, PostCSS for Tailwind processing
Fonts: Noto Sans TC and Noto Serif TC
Assets: Static files served directly from Flask
Deployment
Platform: Optimized for Vercel deployment with special handling for temporary SQLite databases
Environment: Python 3.x runtime
Problems the System Aims to Solve
Limited Digital Presence for Local Tourism: Addresses the lack of a centralized digital platform to showcase Mangatarem’s cultural and tourism assets.

Cultural Heritage Preservation: Provides a digital repository for preserving and sharing local traditions, history, and cultural practices.

Accessibility Issues: Makes information about local attractions and cultural sites accessible to a wider audience, including tourists and researchers.

Content Management Challenges: Offers a structured system for local government units (LGU) and barangay representatives to manage and update content.

Tourism Promotion: Helps promote local tourism by making attractions more discoverable and engaging through interactive maps and multimedia.

Community Engagement: Allows local communities to contribute content and share their cultural assets with the world.

Database Models and Structure
The system implements a comprehensive data model with the following key entities:

User: Manages user accounts with roles (admin, contributor, user), authentication, and authorization
Attraction: Stores tourism spots with location coordinates, descriptions, categories, and approval status
Event: Tracks local events and festivals with dates, locations, and categories
GalleryItem: Manages photos and videos with moderation capabilities
BarangayInfo: Contains detailed information about each barangay’s history and cultural assets
PageView: Tracks analytics and user engagement metrics
Favorite: Allows users to save favorite attractions
EventInterest: Tracks user interest in upcoming events
Review: Enables user reviews and ratings with moderation
Key Features and Functionalities
Interactive Cultural Map: Explore barangay-level highlights using an interactive Leaflet-based map with location markers for attractions.

Tourism Information Portal: Detailed profiles of local attractions, traditions, and eateries with descriptions, images, and ratings.

Events & Festival Directory: Stay updated with local festivities and community celebrations with date-based filtering.

Multimedia Gallery: High-quality photo and video collections of local traditions with moderation capabilities.

Admin & Contributor Dashboard: Secure management interface for LGU and barangay representatives to update content with role-based access control.

Analytics Dashboard: Insights into popular locations and user engagement levels with tracking capabilities.

Content Moderation: Multi-tier approval system for attractions, events, and gallery items submitted by contributors.

Responsive Design: Mobile-friendly interface that works across devices using Tailwind CSS.

Progressive Web App (PWA): Offline functionality and app-like experience with service worker and manifest.

User Authentication: Secure login system with role-based permissions and account management.

Stakeholders and Target Users
LGU Mangatarem: Primary beneficiaries for tourism promotion and cultural preservation
Barangay Representatives: Local content contributors who can submit and manage information about their areas
Students & Researchers: Academic users interested in cultural and historical references
Visitors/Tourists: Digital guide for exploring Mangatarem’s attractions
Local Community Members: Residents who want to learn about their own cultural heritage
Additional System Characteristics
Automatic Database Seeding: Includes sample attractions, admin, and contributor accounts for local development
Security Features: Password hashing, rate limiting, input validation, and secure session management
Development Standards: Follows PEP 8 for Python, consistent naming conventions, and proper code organization
Testing Support: Unit and integration tests framework with database seeding for development environments