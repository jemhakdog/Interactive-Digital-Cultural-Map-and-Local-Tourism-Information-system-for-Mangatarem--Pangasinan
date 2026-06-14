# Project: Database Schema Synchronization

## Architecture
- Mapping Flask models (SQLAlchemy) to physical PostgreSQL DDL files (`db_schemas/schema.sql` and `db_schemas/schema_postgis.sql`).
- Maintain exact types, columns, foreign keys, constraints, and default values.
- Ensure appropriate indexes on all foreign key columns.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Exploration & Analysis | Map all Python Flask models and cross-reference with existing schemas | None | IN_PROGRESS (Conv: 8074ed60-d9b5-4e6d-9f60-4b261b472112) |
| 2 | Align Base Schema (R1) | Consolidate review and favorite tables, add password reset tokens to User | M1 | PLANNED |
| 3 | Add Missing Modules (R2)| Add gamification, booking, chat, announcements, feedback, notifications, verification, logs tables | M1 | PLANNED |
| 4 | Spatial Alignment (R3) | Bind PostGIS geography points, indexes, and triggers to revised tables | M2, M3 | PLANNED |
| 5 | Validation & Integrity | Run validation scripts, ensure syntax and dialect correctness, verify indexes | M4 | PLANNED |

## Code Layout
- `db_schemas/schema.sql` — Main schema DDL containing tables, columns, constraints, foreign keys, and indexes.
- `db_schemas/schema_postgis.sql` — Spatial schema DDL containing PostGIS extensions, geometry/geography columns, spatial indexes, and triggers.
- `models.py` — Legacy/base models.
- `modules/*/models.py` — Module-specific Flask models.
- `scripts/db_ops/verify_schema.py` — Schema verification script.
