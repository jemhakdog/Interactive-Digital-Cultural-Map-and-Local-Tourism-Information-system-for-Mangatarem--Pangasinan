# Project Plan: ERD Entity Naming Improvement & Preventive Measure

## Overview

The objective is to refine ambiguous entity names in the database schema (e.g., `favorite`, `review`) to be more specific, avoiding confusion such as "favorite of what?" or "review of what?". As a preventive measure, we will update these specific table names comprehensively across the SQL migration scripts and the final ERD and DFD diagrams located in `docs/diagrams/final`.

## Project Type
BACKEND / DATABASE

## Success Criteria
- Vague table names (`favorite`, `review`) are consistently renamed across the schema to reflect their specific relationships (e.g., `user_favorite` or `attraction_favorite`).
- The SQL migration scripts (`001_initial_schema_postgresql.sql` and `001_initial_schema_sqlite.sql`) are updated with the new table names.
- The ERD (`erd_v1.drawio`) and DFD (`dfd-level-1-clean_v1.drawio`) in `docs/diagrams/final` are updated to reflect the new, specific entity names.
- All backend references (queries, ORM models) to these tables have been updated to match the new schema names.

## Tech Stack
- **Database**: PostgreSQL / SQLite (via SQL migration files)
- **Diagrams**: Draw.io (XML format)
- **Backend/API**: Python (Flask) / SQLAlchemy (if applicable - needs verification during implementation)

## File Structure
- `migrations/001_initial_schema_postgresql.sql`
- `migrations/001_initial_schema_sqlite.sql`
- `docs/diagrams/final/erd_v1.drawio`
- `docs/diagrams/final/dfd-level-1-clean_v1.drawio`
- Application Models / API routes (to be updated based on new names)

## Task Breakdown

### 1. Rename Entities in SQL Migrations
- **Agent**: `database-architect`
- **Skill**: `database-design`
- **Priority**: P0
- **INPUT**: `migrations/001_initial_schema_postgresql.sql` and `001_initial_schema_sqlite.sql` containing `favorite` and `review` tables.
- **OUTPUT**: Updated migration files where:
  - `favorite` -> `user_favorite_attraction` (or similar clear name depending on Socratic context).
  - `review` -> `attraction_review`.
  - Corresponding indices and dependencies are also renamed.
- **VERIFY**: Run a schema validation check (e.g. SQLite syntax check).

### 2. Update ERD Diagram
- **Agent**: `database-architect`
- **Priority**: P0
- **INPUT**: `docs/diagrams/final/erd_v1.drawio`
- **OUTPUT**: Updated `.drawio` file text content, replacing all instances of the old entity name labels with the specific new ones.
- **VERIFY**: Validate the XML structure visually or by loading.

### 3. Update DFD Diagram
- **Agent**: `database-architect`
- **Priority**: P0
- **INPUT**: `docs/diagrams/final/dfd-level-1-clean_v1.drawio`
- **OUTPUT**: Updated `.drawio` file text content replacing old data store names (`favorite`, `review`) with the specific new names.
- **VERIFY**: Validate the XML structure visually or by loading.

### 4. Update Backend Codebase References
- **Agent**: `backend-specialist`
- **Skill**: `api-patterns`
- **Priority**: P1
- **Dependencies**: Task 1
- **INPUT**: Entire backend Python codebase.
- **OUTPUT**: Source code updates replacing `review` and `favorite` table references with `attraction_review` and `user_favorite_attraction` respectively.
- **VERIFY**: Run `pytest` or `test_runner.py` to ensure no broken references remain.

## Phase X: Verification
- [ ] Lint: Backend syntax uses proper table names.
- [ ] Schema: Manual verification of SQL syntax in both PostgreSQL and SQLite scripts.
- [ ] Tests: Backend test suite passes without issues.
