# Database Migration Guide

**Interactive Digital Cultural Map and Local Tourism Information System**

This guide covers database schema management, migrations, and switching between SQLite (local) and Supabase (production).

---

## Overview

The application uses a dual-database strategy:

- **Local Development**: SQLite database stored in `instance/app.db`
- **Production**: Supabase (PostgreSQL) with connection pooling

Database schema is defined in [models.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/models.py) using SQLAlchemy ORM.

---

## Database Schema Files

### Primary Schema File

**[supabase_schema.sql](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/supabase_schema.sql)**

- Contains PostgreSQL-compatible SQL schema
- Used for production deployment on Supabase
- Should be kept in sync with `models.py`

### SQLAlchemy Models

**[models.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/models.py)**

- Python SQLAlchemy ORM definitions
- Source of truth for application code
- Supports both SQLite and PostgreSQL

---

## Local Development (SQLite)

### Initial Setup

SQLite database is automatically created when you first run the application:

```bash
python app.py
```

**Location**: `instance/app.db`

**Database Creation**:
- `db.create_all()` is called automatically in `app.py` when not on Vercel
- Sample data is seeded from `data/attractions.json` if the database is empty

### Using Flask-Migrate (Local Only)

Flask-Migrate is **only available** for local development:

#### Initialize Migrations (First Time)

```bash
# Ensure you're in local development mode
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development

# Initialize migrations folder
flask db init
```

This creates a `migrations/` directory with Alembic configuration.

#### Create a Migration

When you modify `models.py`:

```bash
# Generate migration based on model changes
flask db migrate -m "Add opening_hours column to attraction"
```

This detects changes and generates a migration script in `migrations/versions/`.

#### Apply Migration

```bash
# Apply pending migrations
flask db upgrade
```

#### Revert Migration

```bash
# Rollback one migration
flask db downgrade
```

### Manual Schema Changes (SQLite)

Alternatively, use SQLite CLI:

```bash
# Open SQLite database
sqlite3 instance/app.db

# View schema
.schema attraction

# Add column manually
ALTER TABLE attraction ADD COLUMN opening_hours TEXT;

# Exit
.exit
```

---

## Production Database (Supabase)

### Initial Schema Application

#### Step 1: Access Supabase SQL Editor

1. Log in to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Navigate to **SQL Editor** (left sidebar)

#### Step 2: Execute Schema

1. Open [supabase_schema.sql](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/supabase_schema.sql)
2. Copy the entire SQL content
3. Paste into Supabase SQL Editor
4. Click **Run** or press `Ctrl/Cmd + Enter`

#### Step 3: Verify Tables

Navigate to **Table Editor** and verify the following tables exist:

- `user`
- `attraction`
- `event`
- `gallery_item`
- `barangay_info`
- `page_view`
- `favorite`
- `event_interest`
- `review`

### Applying Schema Changes in Production

> [!WARNING]
> **Flask-Migrate is disabled on Vercel.** All production migrations must be done via direct SQL execution.

#### Workflow for Schema Changes

1. **Test Locally First**:
   ```bash
   # Test with SQLite
   flask db migrate -m "Description of change"
   flask db upgrade
   
   # Verify application works
   python app.py
   ```

2. **Generate PostgreSQL SQL**:
   - Review the generated migration in `migrations/versions/`
   - Convert to PostgreSQL-compatible SQL if needed
   - Or write SQL manually

3. **Apply to Supabase**:
   - Open Supabase SQL Editor
   - Execute the migration SQL
   - Verify changes in Table Editor

4. **Update Schema File**:
   ```bash
   # Export updated schema from Supabase
   # Or manually update supabase_schema.sql
   git add supabase_schema.sql
   git commit -m "Update schema: add opening_hours column"
   git push
   ```

### Example Migration: Adding a Column

**SQL to execute in Supabase**:

```sql
-- Add new column
ALTER TABLE attraction ADD COLUMN opening_hours TEXT;

-- Set default value for existing rows
UPDATE attraction SET opening_hours = 'Not specified' WHERE opening_hours IS NULL;

-- Add index if needed
CREATE INDEX idx_attraction_opening_hours ON attraction(opening_hours);
```

**Update models.py**:

```python
class Attraction(db.Model):
    # ... existing fields ...
    opening_hours = db.Column(db.Text, nullable=True)
```

---

## Switching Between Databases

### Configuration

Database selection is controlled by `utils/db_manager.py`:

```python
def get_database_uri():
    """Returns appropriate database URI based on environment"""
    database_url = os.environ.get("DATABASE_URL")
    
    if database_url:
        # Production: Use Supabase connection pooler
        return database_url
    else:
        # Local: Use SQLite
        base_dir = os.path.abspath(os.path.dirname(__file__))
        return f"sqlite:///{os.path.join(base_dir, '..', 'instance', 'app.db')}"
```

### Switch to Supabase Locally (Testing)

To test with Supabase during local development:

1. **Get Supabase Connection String**:
   - Supabase Dashboard → Settings → Database
   - Copy **Connection pooling** string (port 6543)

2. **Set Environment Variable**:
   ```bash
   # Create or edit .env file
   DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```

3. **Run Application**:
   ```bash
   python app.py
   ```

### Switch Back to SQLite

Remove or comment out `DATABASE_URL` from `.env`:

```bash
# DATABASE_URL=postgresql://...
```

---

## Database Backup and Restore

### Backup SQLite (Local)

```bash
# Simple file copy
cp instance/app.db instance/app.db.backup

# With timestamp
cp instance/app.db "instance/app.db.$(date +%Y%m%d_%H%M%S).backup"
```

### Backup Supabase (Production)

#### Automated Backups

Supabase provides automatic daily backups:
- **Free Plan**: 7 days retention
- **Pro Plan**: 30 days retention

Access backups:
1. Supabase Dashboard → Database → Backups
2. Select backup point
3. Click **Restore** or **Download**

#### Manual Backup (pg_dump)

```bash
# Install PostgreSQL client tools
# Get direct connection string (port 5432)

pg_dump "postgresql://postgres.[project-ref]:[password]@db.[project-ref].supabase.co:5432/postgres" \
  > backup_$(date +%Y%m%d).sql
```

### Restore from Backup

#### SQLite

```bash
# Restore from backup file
cp instance/app.db.backup instance/app.db
```

#### Supabase

**Via Dashboard**:
1. Database → Backups
2. Select backup
3. Click **Restore**

**Via SQL Import**:
1. SQL Editor → New query
2. Paste backup SQL
3. Run

---

## Data Migration Between Environments

### Export from SQLite

```bash
# Install sqlite3
sqlite3 instance/app.db .dump > sqlite_export.sql
```

### Convert SQLite to PostgreSQL

Use online tools or scripts:

```bash
# Install pgloader (optional)
pgloader instance/app.db postgresql://user:pass@host:5432/database
```

Or manually adjust SQL:
- Change `AUTOINCREMENT` to `SERIAL`
- Update data types (e.g., `DATETIME` → `TIMESTAMP`)
- Fix quote styles

### Import to Supabase

1. Prepare PostgreSQL-compatible SQL
2. Open Supabase SQL Editor
3. Execute import SQL

---

## Common Migration Tasks

### Adding a New Table

1. **Update models.py**:
   ```python
   class TripPlan(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
       name = db.Column(db.String(100))
       created_at = db.Column(db.DateTime, default=datetime.utcnow)
   ```

2. **Local Migration**:
   ```bash
   flask db migrate -m "Add trip_plan table"
   flask db upgrade
   ```

3. **Production SQL** (Supabase):
   ```sql
   CREATE TABLE trip_plan (
       id SERIAL PRIMARY KEY,
       user_id INTEGER REFERENCES "user"(id),
       name VARCHAR(100),
       created_at TIMESTAMP DEFAULT NOW()
   );
   ```

4. **Update supabase_schema.sql**:
   Add the CREATE TABLE statement to the schema file.

### Modifying a Column

1. **Update models.py**:
   ```python
   description = db.Column(db.Text, nullable=False)  # Changed from nullable=True
   ```

2. **Production SQL**:
   ```sql
   -- Make column NOT NULL
   ALTER TABLE attraction ALTER COLUMN description SET NOT NULL;
   
   -- Or change type
   ALTER TABLE attraction ALTER COLUMN description TYPE TEXT;
   ```

### Adding an Index

```sql
-- For faster queries on frequently searched columns
CREATE INDEX idx_attraction_category ON attraction(category);
CREATE INDEX idx_event_date ON event(date);
CREATE INDEX idx_review_attraction ON review(attraction_id, status);
```

---

## Best Practices

### 1. Test Locally First

Always test schema changes with SQLite before applying to production:

```bash
# Test migration
flask db migrate -m "Change description"
flask db upgrade

# Test application
python app.py

# Verify functionality
```

### 2. Backup Before Changes

Always backup before applying migrations:

```bash
# Supabase: Use dashboard backup feature
# Or pg_dump for manual backup
```

### 3. Use Transactions

Wrap complex migrations in transactions:

```sql
BEGIN;

ALTER TABLE attraction ADD COLUMN new_field TEXT;
UPDATE attraction SET new_field = 'default_value';

COMMIT;  -- Or ROLLBACK if errors occur
```

### 4. Keep Schema File Synced

After every production migration:
1. Update `supabase_schema.sql`
2. Commit changes to version control
3. Document changes in commit message

### 5. Version Control Migrations

Commit migration files to Git:

```bash
git add migrations/versions/*.py
git commit -m "Migration: add opening_hours to attraction"
```

---

## Troubleshooting

### Issue: Migration Generates Empty File

**Cause**: Models and database are already in sync.

**Solution**: Verify you saved changes to `models.py` and the model changes are detected.

### Issue: "Table already exists" Error

**Cause**: Trying to create a table that exists.

**Solution**: 
```sql
-- Use IF NOT EXISTS
CREATE TABLE IF NOT EXISTS new_table (...);
```

### Issue: Data Type Mismatch

**Cause**: SQLite and PostgreSQL have different type systems.

**Solution**: Use SQLAlchemy types that map correctly:
- `db.String` → `VARCHAR`
- `db.Text` → `TEXT`
- `db.Integer` → `INTEGER`
- `db.DateTime` → `TIMESTAMP`

### Issue: Foreign Key Constraint Violation

**Cause**: Referenced record doesn't exist.

**Solution**:
```sql
-- Temporarily disable constraints (PostgreSQL)
SET CONSTRAINTS ALL DEFERRED;

-- Perform migration

-- Re-enable
SET CONSTRAINTS ALL IMMEDIATE;
```

---

## Additional Resources

- **Flask-Migrate Docs**: [flask-migrate.readthedocs.io](https://flask-migrate.readthedocs.io/)
- **SQLAlchemy Docs**: [docs.sqlalchemy.org](https://docs.sqlalchemy.org/)
- **Supabase Docs**: [supabase.com/docs/guides/database](https://supabase.com/docs/guides/database)
- **PostgreSQL Docs**: [postgresql.org/docs](https://www.postgresql.org/docs/)
- **Deployment Guide**: [deployment_guide.md](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/deployment_guide.md)

---

**Last Updated**: 2026-02-12
