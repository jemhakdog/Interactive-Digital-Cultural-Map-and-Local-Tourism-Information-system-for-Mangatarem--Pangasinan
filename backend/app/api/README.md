# API Routers Contract (`backend/app/api`)

## Overview
The `backend.app.api` package encapsulates all REST endpoint controllers. Routers parse incoming requests, enforce security policies, invoke database operations, and return typed JSON responses.

## Interface
- `auth.router` (`/api/auth`): Registration, login, token refresh, Google OAuth verification, password recovery.
- `public.router` (`/api`): Public unauthenticated homepage data, barangay listings, and community statistics.
- `attractions.router` (`/api/attractions`): Attraction catalog search, filtering, detail retrieval, and reviews.
- `events.router` (`/api/events`): Cultural event and festival listings and CRUD operations.
- `business.router` (`/api/business`): Tourism establishments, lodging rooms, menus, and verifications.
- `booking.router` (`/api/booking`): Real-time asset availability, reservations, and arrival verification.
- `chat.router` (`/api/chat`): Chat room creation and message exchange.
- `gallery.router` (`/api/gallery`): Community photo/video gallery media retrieval and submission.
- `heritage.router` (`/api/heritage`): Cultural heritage asset management.
- `gamification.router` (`/api/gamification`): QR-based check-ins, badge unlocks, and digital passports.
- `notifications.router` (`/api/notifications`): User notifications and newsletter subscription capture.
- `analytics.router` (`/api/analytics`): Telemetry logging (`/log-visitor`) and page view tracking.
- `uploads.router` (`/api/uploads`): Multipart media file uploads with magic-byte validation.
- `admin.router` (`/api/admin`): Administrative dashboard metrics, user approvals, and moderation actions.
- `contributor.router` (`/api/contributor`): Scoped barangay steward dashboard and content management.
- `user.router` (`/api/user`): Authenticated tourist profile, bookmark favorites, and personal visit logs.
- `admin_documents.router` (`/api/documents`): Municipal document vault CRUD operations.
- `admin_newsletter.router` (`/api/newsletter`): Newsletter subscriber management and dispatch history.
- `admin_visitors.router` (`/api`): Visitor log analytics and registry endpoints.

## Invariants
- JWT Bearer auth is required on all non-public endpoints; unauthenticated calls return HTTP 401.
- Unauthorized role access to restricted routes returns HTTP 403.
- Scoped write operations enforce barangay ownership boundaries.
- File uploads validate file magic bytes (MIME signatures) and adhere to a 15MB file size limit.

## Side Effects
- Read and write access to the database via SQLAlchemy async sessions.
- Local filesystem storage writes to `backend/uploads`.
- External HTTP requests to Google OAuth verification endpoints.

## Verification
- Run: `.venv/bin/pytest tests/`
