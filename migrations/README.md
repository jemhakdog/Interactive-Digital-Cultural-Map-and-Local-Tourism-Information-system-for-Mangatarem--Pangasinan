# Database Migrations for Mangatarem Cultural Heritage & Tourism System

This directory contains SQL migration files for managing the database schema across different environments (SQLite for development, PostgreSQL/Supabase for production).

## Migration Files

### Current Migrations

- **001_initial_schema_sqlite.sql** - Initial schema for SQLite development databases
- **001_initial_schema_postgresql.sql** - Initial schema for PostgreSQL/Supabase production databases

### Important Note

**These are the ONLY SQL migration files that should exist in the project.** All other SQL files have been consolidated into these migrations to avoid confusion and schema conflicts.

If you find other `.sql` files in the project (e.g., in `docs/`, `db_update_package/`, or root directory), they are **deprecated** and should be deleted.

## Tables Included

The following tables are created by these migrations (all models from `models.py`):

### Core Tables
- `user` - User accounts with roles (admin, contributor, user)
- `heritage_profile` - Base model for all cultural heritage documentation
- `attraction` - Tourism attractions and spots
- `event` - Local events and festivals
- `gallery_item` - Photo and video gallery items
- `barangay_info` - Barangay-level cultural information

### Analytics & User Engagement Tables
- `page_view` - Page view tracking for analytics
- `favorite` - User favorite attractions
- `event_interest` - User interest in events
- `review` - User reviews and ratings for attractions

### Heritage Detail Tables (Tourism Forms)
- `natural_heritage_details` - Form 01A: Natural Resources and Land Formations
- `built_heritage_details` - Form 02A: Tangible Immovable Heritage
- `movable_heritage_details` - Form 03A: Archaeological Heritage
- `intangible_heritage_details` - Form 04A: Oral Traditions and Expressions
- `personality_details` - Form 05: Significant Personalities
- `institution_details` - Form 06: Cultural Institutions
- `lgu_program_details` - Form 07: LGU Culture Programs

## Tables Skipped (Not in Models)

The following tables were found in old SQL files but are **NOT** used in the current models:

- `attractions` (plural) - Old schema, replaced by `attraction` (singular)
- `events` (plural) - Old schema, replaced by `event` (singular)

## Running Migrations

### Prerequisites

For PostgreSQL support, install the required driver:
```bash
pip install psycopg2-binary
```

### SQLite (Development)

```bash
# Run all pending migrations
python run_migrations.py

# Dry run (see what would be executed)
python run_migrations.py --dry-run
```

### PostgreSQL/Supabase (Production)

```bash
# Using command line argument
python run_migrations.py --database postgresql://user:pass@localhost/dbname

# Using environment variable
export DATABASE_URL=postgresql://user:pass@localhost/dbname
python run_migrations.py

# Dry run
python run_migrations.py --database postgresql://user:pass@localhost/dbname --dry-run
```

## Verifying Schema

After running migrations, verify the schema matches the models:

```bash
# Verify SQLite database
python verify_schema.py

# Verify PostgreSQL database
python verify_schema.py --database postgresql://user:pass@localhost/dbname

# Verbose output
python verify_schema.py --verbose
```

## Migration Tracking

The system uses a `_migrations` table to track which migrations have been applied:

```sql
CREATE TABLE _migrations (
    id SERIAL PRIMARY KEY,
    migration_name VARCHAR(255) UNIQUE NOT NULL,
    applied_at TIMESTAMP DEFAULT NOW()
);
```

This ensures migrations are only run once and can be tracked across deployments.

## Creating New Migrations

When adding new tables or modifying the schema:

1. Create a new SQL file in the `migrations/` directory
2. Use sequential numbering: `002_description.sql`, `003_description.sql`, etc.
3. Make migrations idempotent (safe to run multiple times)
4. Use `CREATE TABLE IF NOT EXISTS` and `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`
5. Test with `--dry-run` first

### Example Migration Template

```sql
-- ============================================================
-- Migration: 002_add_new_feature
-- Database: SQLite & PostgreSQL
-- Generated: 2026-02-18
-- Description: Add new feature table
-- ============================================================

CREATE TABLE IF NOT EXISTS new_feature (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_new_feature_name ON new_feature(name);
```

## Database-Specific Notes

### SQLite
- Foreign keys must be enabled with `PRAGMA foreign_keys = ON`
- Uses `AUTOINCREMENT` for auto-incrementing primary keys
- Uses `DATETIME DEFAULT CURRENT_TIMESTAMP` for timestamps
- JSON columns use `JSON` type

### PostgreSQL/Supabase
- Uses `SERIAL` for auto-incrementing primary keys
- Uses `TIMESTAMP DEFAULT NOW()` for timestamps
- JSON columns use `JSONB` for better performance
- Supports Row Level Security (RLS) policies
- Supports CHECK constraints for data validation

## Troubleshooting

### Migration Fails

If a migration fails:
1. Check the error message for the specific SQL statement that failed
2. Verify the database connection
3. Ensure you have proper permissions
4. Check if the migration was partially applied

### Schema Mismatch

If `verify_schema.py` reports issues:
1. Run migrations: `python run_migrations.py`
2. Check if new models were added to `models.py` without updating migrations
3. Manually inspect the database if needed

### Reset Database (Development Only)

For SQLite development, you can reset the database:
```bash
# Delete the database file
rm instance/mangatarem.db

# Run migrations again
python run_migrations.py
```

**Warning:** Never reset production databases without proper backups!

## Best Practices

1. **Always test migrations locally** before deploying to production
2. **Back up production databases** before running migrations
3. **Use transactions** for migrations that modify existing data
4. **Keep migrations idempotent** so they can be safely re-run
5. **Document schema changes** in CHANGES.md or a migration log
6. **Test rollback procedures** for critical migrations

## Support

For issues or questions about migrations:
- Check the error logs from `run_migrations.py`
- Review the SQL files for syntax errors
- Verify database connection settings
- Consult the project documentation in `docs/`
