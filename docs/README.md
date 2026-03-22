# Documentation Overview

Welcome to the technical documentation for the **Interactive Digital Cultural Map of Mangatarem**.

## Document Index

| Document | Purpose | Audience |
|----------|---------|----------|
| [**Architecture**](architecture.md) | High-level system design and data flow. | Developers |
| [**Database Migration**](database_migration.md) | Schema details and migration workflows. | DevOps / DBAs |
| [**API Reference**](api_reference.md) | Endpoint details and JSON structures. | Developers |
| [**Admin Guide**](admin_guide.md) | Content moderation and user management. | LGU Admins |
| [**Contributor Guide**](contributor_guide.md) | asset submission and documentation rules. | Barangay Level |
| [**User Manual**](user_manual.md) | How to explore the map and registry. | Visitors |
| [**Optimization**](optimization.md) | Performance metrics and edge strategies. | Developers |
| [**Deployment Guide**](deployment_guide.md) | Vercel and Supabase cloud setup. | DevOps |
| [**Core System**](core.md) | Project vision, goals, and core features. | All Roles |

## General Guidelines

- **Standardization**: All cultural heritage data must align with the Heritage Registry (Forms 01-07).
- **Security**: Never commit `SECRET_KEY` or `DATABASE_URL` to version control.
- **Formatting**: All documentation uses GitHub Flavored Markdown.
