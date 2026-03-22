# Database Schema and Migrations Guide

This guide details the database schema management, migrations workflow, and the process of switching between SQLite and Supabase.

## Database Core Logic

- **Local Development**: Uses SQLite (`instance/app.db`).
- **Production**: Uses Supabase PostgreSQL.
- **Connection Logic**: Managed in `utils/db_manager.py`. The system automatically detects the environment and selects the appropriate URI.

---

## Current Schema (ERD Aligned)

The system consists of 19+ core tables managed via SQLAlchemy:

### Base Tables
1. **USER**: Authentication and roles (`admin`, `contributor`, `user`).
2. **BARANGAY_INFO**: Background data for each barangay.
3. **ATTRACTION**: Tourism spots with `latitude` and `longitude`.
4. **EVENT**: Festivals and community activities.
5. **GALLERY_ITEM**: Medial assets (photos/videos).
6. **ANALYTICS_PAGE_VIEW**: Engagement tracking.
7. **FAVORITE**: User bookmarked attractions.
8. **EVENT_INTEREST**: User RSVPs for events.
9. **REVIEW**: Ratings and comments.
10. **PASSWORD_RESET_TOKEN**: Recovery tokens.
11. **NEWSLETTER_SUBSCRIBER**: Mailing list.

### Cultural Heritage Registry (HeritageProfile System)
12. **HERITAGE_PROFILE**: Central registry entry.
13. **NATURAL_HERITAGE_DETAIL**: Form 01A details.
14. **BUILT_HERITAGE_DETAIL**: Form 02A details.
15. **MOVABLE_HERITAGE_DETAIL**: Form 03A details.
16. **INTANGIBLE_HERITAGE_DETAIL**: Form 04A details.
17. **PERSONALITY_PROFILE_DETAIL**: Form 05 details.
18. **CULTURAL_INSTITUTION_DETAIL**: Form 06 details.
19. **LGU_CULTURE_PROGRAM_DETAIL**: Form 07 details.

---

## Migration Workflow

### 1. Local Development (SQLite)

We use **Flask-Migrate (Alembic)** for local schema changes.

```bash
# Initialize migrations (only once)
flask db init

# Create a migration script
flask db migrate -m "Description of change"

# Apply changes to local SQLite
flask db upgrade
```

### 2. Production (Supabase/PostgreSQL)

> [!IMPORTANT]
> **Flask-Migrate is disabled in production.** Schema changes on Supabase must be applied as manual SQL scripts.

1. Generate the SQL for your changes (usually by inspecting the alembic script or using `flask db upgrade --sql`).
2. Log in to the **Supabase Dashboard**.
3. Open the **SQL Editor**.
4. Paste and execute the SQL script.
5. Verify the changes in the **Table Editor**.

---

## Schema Verification

To verify that all tables are correctly created in a new environment, run the following SQL query in the Supabase SQL Editor:

```sql
SELECT tablename 
FROM pg_catalog.pg_tables 
WHERE schemaname = 'public';
```

**Expected Output Checklist:**
- [ ] `USER`
- [ ] `BARANGAY_INFO`
- [ ] `ATTRACTION` (Verify columns: `latitude`, `longitude`)
- [ ] `EVENT`
- [ ] `GALLERY_ITEM`
- [ ] `ANALYTICS_PAGE_VIEW`
- [ ] `FAVORITE`
- [ ] `EVENT_INTEREST`
- [ ] `REVIEW`
- [ ] `PASSWORD_RESET_TOKEN`
- [ ] `NEWSLETTER_SUBSCRIBER`
- [ ] `HERITAGE_PROFILE`
- [ ] `NATURAL_HERITAGE_DETAIL`
- [ ] `BUILT_HERITAGE_DETAIL`
- [ ] `MOVABLE_HERITAGE_DETAIL`
- [ ] `INTANGIBLE_HERITAGE_DETAIL`
- [ ] `PERSONALITY_PROFILE_DETAIL`
- [ ] `CULTURAL_INSTITUTION_DETAIL`
- [ ] `LGU_CULTURE_PROGRAM_DETAIL`
- [ ] `alembic_version`

---

## Common Issues

### 1. Schema Drift
If the `models.py` doesn't match the database, you will see `UndefinedColumn` or `AttributeError`. 
- **Fix**: Run `flask db migrate` locally and apply the resulting SQL to Supabase.

### 2. Geometry/Coordinate Changes
Older versions of the docs used `lat` and `lng`. The current system uses `latitude` and `longitude`.
- **Warning**: Ensure all SQL scripts use the full names to avoid migration failures.
