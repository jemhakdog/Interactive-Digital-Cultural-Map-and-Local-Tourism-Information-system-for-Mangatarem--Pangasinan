# Implementation Plan - Database Content Approval & SQLite Migration

This plan outlines the steps to add content approval fields to the database models, generate compatible SQL schemas for both SQLite and Supabase, and configure the local development environment to use SQLite by default.

## Proposed Changes

### [Backend] Database Models
#### [MODIFY] [models.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/models.py)
- Add `reviewed_by` and `reviewed_at` columns to `Attraction`, `Event`, `GalleryItem`, and `Review` models.
- Ensure `reviewed_by` uses a foreign key to the `User` model for local SQLite compatibility.
- Ensure `status` columns use appropriate defaults and indexing.

### [Infrastructure] Database Management
#### [MODIFY] [utils/db_manager.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/utils/db_manager.py)
- Change the default `DB_PROVIDER` to `sqlite` instead of `supabase` in `get_database_uri`.
- Fix the default value consistency between `get_database_uri` and `get_db_config`.

### [Environment] Configuration
#### [MODIFY] [.env](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/.env)
- Explicitly set `DB_PROVIDER=sqlite` for local development.

### [Documentation] SQL Schemas
#### [NEW] [content_approval_sqlite.sql](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/schema/content_approval_sqlite.sql)
- Create SQLite-specific SQL for adding approval fields and indices.
#### [MODIFY] [content_approval.sql](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/schema/content_approval.sql)
- Ensure the Supabase/PostgreSQL schema is optimized and includes all necessary fields for the updated models.

---

## Verification Plan

### Automated Tests
- Run `db.create_all()` in a temporary script to verify SQLite database creation.
- Check model definitions via `flask shell`.

### Manual Verification
1.  **Local SQLite Check**: 
    - Delete the existing SQLite database (if any) or check `instance/mangatarem.db`.
    - Restart the application.
    - Verify that the application starts without database errors.
    - Check the SQLite schema using a CLI tool or via the app's seeding process.
2.  **Schema Comparison**:
    - Compare the generated SQLite and Supabase SQL files to ensure they represent the same logical schema.

> [!IMPORTANT]
> Since SQLite doesn't support native `ENUM` types like PostgreSQL, we will use `TEXT` with `CHECK` constraints to maintain data integrity.
