# Original User Request

## Initial Request — 2026-06-10T06:36:18+08:00

Restyle the Barangay List page to inherit the dark, premium dashboard aesthetic shown in the user's mockup image (dark mode theme, rounded content cards, lime green primary CTA buttons, statistics pills, left-hand sidebar navigation).

Working directory: d:/porjects/capstone_system/

## Requirements

### R1. Restyle Layout to Modern Premium Dark Dashboard
- Implement a cohesive dark mode theme matching the mockup: deep charcoal/black background (`#121212` or similar), charcoal panels (`#1a1a1a`), and light gray text hierarchy.
- Re-align the Barangay Directory / List page layout to follow the bi-column structure: a left-hand navigation sidebar and a main content workspace with top utilities.
- Use a neon/lime-green accent color (`#a3e635` or `#85e024`) for active states, interactive items, and primary CTA buttons.

### R2. Barangay Cards Aesthetics
- Present each Barangay as a card with:
  - A large, beautifully-rounded feature image.
  - The Barangay name aligned to the left of a lime-green "View" button.
  - Labeled statistics boxes displaying the number of attractions, events, and other metrics in small dark containers.
  - Key information fields at the bottom (e.g., Barangay code, name, and attributes) in input-style or pills display.

## Acceptance Criteria

### Visual Fidelity & Styling
- [ ] UI must be dark themed with rounded borders (`rounded-2xl` or `rounded-3xl` equivalents) and premium glassmorphic overlays if applicable.
- [ ] Active link indicator on left sidebar uses a lime-green accent border or block.
- [ ] Cards layout matches the design hierarchy: Image on top, Title + Lime Green View Button below it, grid of metrics boxes, then bottom metadata attributes.
- [ ] Adheres to the strict Purple Ban (no purple or violet colors in the layout).

## Follow-up — 2026-06-12T13:02:22+08:00

Verify and synchronize the database schema definition (`db_schemas/schema.sql` and `db_schemas/schema_postgis.sql`) to be 100% correct, precise, and accurately reflect all Flask models, fields, constraints, tables, and relationships defined in the current codebase (guided by the ERD v3 configuration).

Working directory: d:\porjects\capstone_system
Integrity mode: development

## Requirements

### R1. Align Base Schema Tables
Update `db_schemas/schema.sql` to match the exact physical model structure of the Python codebase:
- Consolidate legacy split review tables (`ATTRACTION_REVIEW`, `ESTABLISHMENT_REVIEW`) into a single `REVIEW` table with a `ck_review_target` check constraint.
- Consolidate legacy favorite tables (`USER_FAVORITE_ATTRACTION`, `USER_EVENT_INTEREST`) into a single `USER_FAVORITE` table with a `ck_favorite_target` check constraint.
- Drop the separate `PASSWORD_RESET_TOKEN` table and add `reset_token`, `reset_token_expires_at`, and `reset_token_used` directly to the `USER` table to match the current python User model shim.

### R2. Add Missing Module Tables
Add full table schemas for all missing modules in `db_schemas/schema.sql`:
- **Gamification**: `ACHIEVEMENT_BADGE`, `USER_PASSPORT`, `TOURIST_CHECK_IN`
- **Booking & Reservations**: `BOOKABLE_ASSET`, `BOOKING_SLOT`, `RESERVATION`
- **Chat/Messages**: `CHAT_ROOM`, `CHAT_PARTICIPANT`, `CHAT_MESSAGE`
- **Announcements**: `ANNOUNCEMENT`
- **Map Feedback**: `MAP_FEEDBACK`
- **Notifications**: `USER_NOTIFICATION`
- **Business Verification**: `BUSINESS_VERIFICATION`
- **Visitor Logs**: `VISITOR_LOG`

### R3. Maintain Spatial/PostGIS Schema Alignment
Ensure `db_schemas/schema_postgis.sql` correctly binds PostGIS geography points, indexes, and triggers to the revised tables (`ATTRACTION`, `HERITAGE_PROFILE`, `ESTABLISHMENT`), referencing the correct table names and columns.

## Acceptance Criteria

### Schema Integrity & Correctness
- [ ] No syntax errors exist in either `db_schemas/schema.sql` or `db_schemas/schema_postgis.sql`.
- [ ] Every model in the codebase has a corresponding table in the schema with identical columns, types, foreign key relationships, constraints, and default values.
- [ ] Indices are defined in `schema.sql` for all ForeignKey columns to optimize query speeds.
- [ ] The schema is successfully validated against PostgreSQL/Supabase dialect using a syntax validator or parser.
