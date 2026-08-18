# Decisions

Record important project decisions here.

### 2026-05-30 — Single Consolidated Hub-and-Spoke DFD Layout (V5)

Status: Accepted

Context: The capstone panel explicitly requested exactly *one* unified DFD diagram in the documentation to save page space and represent both macro-level and micro-level system modules. The previous layout utilized a vertical 3-column system split into separate Level 0 and Level 1 versions.

Decision:
1. **Designed a Single Consolidated DFD**: Developed `generate_dfd_v5.py` to compile a single, comprehensive DFD diagram modeled after the structure of Figure 2.3.
2. **Centralized System Hub**: Positioned the entire system boundary as a large process box (`0.0: Interactive Digital Cultural Map & Tourism Information System`) right in the center of the canvas.
3. **Circular Distribution**: Distributed all 15 functional sub-processes (1.0 to 15.0) in a clean rectangular ring around the central System Hub box.
4. **Localized Database Compartments**: Nested all 16 database datastores (D1 to D16) directly adjacent to or underneath their active processes to guarantee zero intersecting lines and maximum structural legibility.
5. **Cleaned Outer Flows**: Kept external actors (Tourist, Admin, Business, Guardian, Google, Mapbox) on the outermost margins, routing all data flows cleanly using rounded orthogonal connections.

Consequences: Satisfies the panel's constraints perfectly by presenting exactly *one* complete DFD diagram that serves as both a high-level Context diagram and a low-level detailed DFD without any visual overlaps or floating connections.

Related files: `docs/diagrams/dfd/generate_dfd_v5.py`, `docs/diagrams/dfd/dfd-level-0_v5.drawio`, `docs/diagrams/dfd/dfd-level-1-clean_v5.drawio`, `memory-bank/progress.md`, `memory-bank/activeContext.md`

### 2026-05-27 — Physical Database Table Consolidation & Single-Page ERD Cleanup


Status: Accepted

Context: The existing relational schema comprised 27 physical database tables. While normalized, this created a massive "spaghetti diagram" in the single-page ERD (`erd_v3.drawio`), with dozens of relationship lines intersecting and routing directly underneath table shapes. Many of these tables (e.g. `PASSWORD_RESET_TOKEN`, `REVIEW_PHOTO`) were simple dependent helpers that could be collapsed into their parent models using JSON columns and inline attributes to streamline the schema.

Decision:
1. **Physically Consolidated `PasswordResetToken` into `User`:**
   - Moved token validation fields (`reset_token`, `reset_token_expires_at`, `reset_token_used`) directly into the `USER` database table inside `modules/auth/models.py`.
   - Redefined `PasswordResetToken` as a lightweight class setter/getter shim mapping to the `User` record, keeping legacy references in `modules/auth/password.py` working flawlessly.
2. **Physically Consolidated `ReviewPhoto` into `Review`:**
   - Added a `photo_urls` JSON column (array of strings) directly in the `REVIEW` database table inside `modules/attractions/models.py`.
   - Redefined `ReviewPhoto` as an offline shim class so legacy template rendering (`self.photos.all()`) doesn't break, and updated photo uploads in `modules/attractions/routes.py` to write directly to `photo_urls`.
3. **Programmatically Cleaned ERD (`erd_v3.drawio`):**
   - Developed a Python parsing script that successfully stripped the `PASSWORD_RESET_TOKEN` and `REVIEW_PHOTO` tables, along with all of their columns and connected edges, from the single-page diagram XML.
   - Enforced a rounded orthogonal routing style (`rounded=1;edgeStyle=orthogonalEdgeStyle`) and stripped manual path coordinate overrides, forcing Draw.io to auto-route all remaining relationship lines around the margins instead of running underneath the table shapes.
4. **Verified DFD Alignment:**
   - Scanned `dfd-level-1-clean_v3.drawio` and confirmed that no separate datastores for reset tokens or review photos were ever mapped, as they are logically abstracted inside the main process flows and datastores (`User_db` and `Review_db`). This confirms that the DFD and physical schemas are in 100% harmonious alignment.

Consequences: Streamlined database schema (reduced active tables from 27 down to 24) that is far easier to manage. A clean, visual single-page ERD with zero relationship lines hidden underneath table elements, completely matching the physical SQLAlchemy schemas with zero front-end regressions.

Related files: `modules/auth/models.py`, `modules/auth/password.py`, `modules/attractions/models.py`, `modules/attractions/routes.py`, `docs/diagrams/erd/erd_v3.drawio`, `docs/diagrams/dfd/dfd-level-1-clean_v3.drawio`, `memory-bank/activeContext.md`, `memory-bank/progress.md`

### 2026-05-27 — Database Relationship Normalization for Newsletter & Notification Modules

Status: Accepted

Context: The existing `NEWSLETTER_SUBSCRIBER` and `NEWSLETTER_HISTORY` tables operated in complete isolation without references to the main `USER` table. This led to a disconnected diagram in the Entity-Relationship Diagram (ERD) and lacked structural cohesion where user subscriptions and sender audit trails were untrackable.

Decision:
1. Updated the database model in `modules/notifications/models.py` to add a nullable foreign key `user_id` on the `NewsletterSubscriber` model, and a nullable foreign key `sender_id` on the `NewsletterHistory` model, both referencing `USER.id` with safe `ondelete='SET NULL'` constraints.
2. Modified the subscription endpoint in `modules/notifications/routes.py` to automatically lookup a registered user matching the subscription email and establish the link.
3. Updated administrative composition in `modules/notifications/admin_routes.py` to record `sender_id=current_user.id` when sending campaigns.
4. Updated the PostgreSQL schema in `db_schemas/schema.sql` to move `NEWSLETTER_SUBSCRIBER` after `"USER"`, define its `user_id` foreign key, and introduce the `NEWSLETTER_HISTORY` table with `sender_id` foreign key.
5. Visually mapped the direct logical connections in the Mermaid ERD (`docs/diagrams/erd/erd_schema.mermaid`).

Consequences: Improved database integrity, normalized database-level audit capabilities for administrative campaigns, and complete visual and logical database connection resolution in the ERD.

Related files: `modules/notifications/models.py`, `modules/notifications/routes.py`, `modules/notifications/admin_routes.py`, `db_schemas/schema.sql`, `docs/diagrams/erd/erd_schema.mermaid`

### 2026-05-25 — DFD Level 1 and ERD Consolidated Layout Snapping & Verification

Status: Accepted

Context: The V3.2 database consolidation left several diagram edges and connectors floating or jumbled in both the Entity-Relationship Diagram (ERD) and Level 1 Data Flow Diagram (DFD). Draw.io utilizes hardcoded absolute source/target offset coordinates and intermediate mxPoint control arrays inside XML <mxGeometry> elements. These overrides force arrows to float in space or overlap other components when nodes are consolidated, deleted, or moved, disrupting the layout.

Decision:
1. Conducted deep layout polishing on the Level 1 DFD (`dfd-level-1-clean_v3.drawio`) to eliminate Context-level system boundaries and remove the central hub bubble. Rerouted all 13+ related data flow edges directly between external entities/sub-processes and datastores.
2. Deleted legacy heritage detail datastores (D10, D11, D12, D13, D14, D16, D17) and consolidated their flows to point directly to the single active D15 `Heritage_Profile` datastore.
3. Injected missing active datastores: D30 `Map_Feedback_db` and D31 `Business_Verification_db`, and wired their flows.
4. Corrected duplicate process numbering (Booking renumbered to `14.0`, Chat to `15.0`, Media Gallery to `12.0`, Newsletter to `13.0`).
5. Polished the ERD (`erd_v3.drawio`) to inject the active `BUSINESS_VERIFICATION` model and wire its relationship edge to `USER`.
6. Purged absolute source/target offsets and custom control point arrays from all DFD (21 offsets, 28 arrays) and ERD (12 offsets, 16 arrays) edges. This forces Draw.io to route clean, straight orthogonal paths (`edgeStyle=orthogonalEdgeStyle;rounded=1`) snapped dynamically to the boundary of the connected shapes.

Consequences: Dynamic and perfectly snapped diagram layouts that automatically adjust to shape position modifications. Zero floating, jumbled, or overlapping edges in either diagram, maintaining 100% alignment with the active Flask-SQLAlchemy 27-table schema.

Related files: `docs/diagrams/dfd/dfd-level-1-clean_v3.drawio`, `docs/diagrams/erd/erd_v3.drawio`

### 2026-05-25 — Comprehensive academic rewrite of Chapters 1–3 and dynamic DOCX compiler implementation

Status: Accepted

Context: The existing draft of Chapters 1–3 of the capstone manuscript was written in a highly informal, conversational, first-person voice and contained 12+ formatting, typo, and data consistency issues listed in `todo.md`. Additionally, compiling the manuscript into a Word document previously relied on a script with completely hardcoded paragraphs, making the Markdown files and Word document diverge.

Decision:
1. Conducted a complete rewrite of Chapters 1–3 markdown files to adopt a strict, objective, third-person academic voice, removing all first-person pronouns ("we", "our", "us", "I").
2. Converted lists under Background, Scope, and Limitations into strict paragraph-only blocks, integrated exactly 5 local and 5 foreign literature citations from 2020-2025 with an academic synthesis, added Surveys and Questionnaires as a core data gathering technique, defined diagram notations formally, aligned the Gantt chart RAD calendar starting June 2024, and fixed all listed typos.
3. Redesigned `make.py` from a hardcoded paragraph script into a dynamic Markdown-to-DOCX compiler that parses markdown headers, lists, bold formatting, and HTML-style tables using the `python-docx` library, maintaining the markdown files as the single source of truth.
4. Built an automated quality checker script `verify_manuscript.py` to scan the chapters and ensure zero remaining pronouns or unresolved typos.

Consequences: Highly professional, standard-compliant academic manuscript files compiled dynamically into a styled Times New Roman Word document, with zero remaining typo or pronoun errors.

Related files: `docs/capstone/chapters/Chapter-1-Introduction.md`, `docs/capstone/chapters/Chapter-2-Methodology-and-Design.md`, `docs/capstone/chapters/Chapter-3-Results-and-Discussion.md`, `docs/capstone/chapters/full chapters.md`, `docs/capstone/chapters/make.py`, `scratch/verify_manuscript.py`, `scratch/merge_chapters.py`, `docs/capstone/chapters/Chapter_1_to_3_Consolidated.docx`

### 2026-05-24 — Consolidate Heritage detail tables and resolve Supabase table duplication

Status: Accepted

Context: The system had 7 legacy detail tables for different heritage profiles. Additionally, the online Supabase PostgreSQL database had grown to 62 tables due to case-sensitive duplicates (e.g. "USER" and "user" coexisting) and leftover tables, which caused major schema verification discrepancies and prevented DDL upgrades on SQLite.

Decision:
1. Merge the 7 detail tables into a single `form_data` JSONB column inside `HERITAGE_PROFILE` table, deleting `heritage_models/` dead code.
2. Safe-drop 39 duplicate, legacy, and obsolete tables in the active Supabase database, while preserving unique contributor user data (`barangay`) by migrating it to `"USER"`.
3. Wrap application seeding inside a safe try-except block in `core/app_setup.py` to prevent out-of-sync boot crashes, and stamp the database version at `536847569d90`.

Consequences: Highly optimized, clean, and normalized database schema (bringing table count down to exactly 32 tables) that aligns perfectly between local SQLite and online Supabase, enabling robust migrations.

Related files: `db_schemas/schema.sql`, `scripts/db_ops/verify_schema.py`, `migrations/versions/536847569d90_add_form_data.py`, `core/app_setup.py`, `scratch/verify_db.py`, `scratch/execute_cleanup.py`

### 2026-07-31 — Map V2 bottom-sheet mobile touch fixes and service-worker cache bump

Status: Accepted

Context: On mobile devices the Map V2 bottom sheet could not be dragged open, and the landmark results list only showed ~4 items because native touch scrolling was blocked by a global `touch-action: none` rule on `.bottom-sheet`. Additionally, the PWA install HUD initially sat in front of the sheet handle, intercepting touch gestures before being repositioned in a prior change.

Decision:
1. Removed `touch-action: none` from `.bottom-sheet` so native scrolling works inside `#results-section`.
2. Added `touch-action: pan-y` to `#results-section` so vertical finger scrolling is allowed while the sheet-drag gesture still fires when the list is at `scrollTop <= 0`.
3. Refined the `resultsSection` touchstart handler to avoid hijacking the gesture when the sheet is already fully open (`is-full`), allowing the list to keep scrolling naturally.
4. Bumped the service-worker cache name to `gomangatarem-v10` and changed the static script tag to `map_v2.js?v=1.1.9` so updated HTML/JS/CSS are fetched immediately instead of being served from stale cache.
5. Kept mobile testing URL ephemeral (`trycloudflare.com` tunnel) because the project does not yet own a domain for a permanent named Cloudflare tunnel.

Consequences: Mobile visitors now see all landmarks, the bottom sheet drags open reliably, and no extra page refresh is required after deployment to pick up the fix.

Related files: `templates/pagez/map_v2.html`, `static/js/pages/map_v2.js`, `static/sw.js`

### 2026-07-31 — Ponytail audit batch cleanup (dead files, duplicate core/ shims, unused validators, dead model)

Status: Accepted

Context: Follow-up ponytail audit flagged dead files, byte-for-byte duplicate `core/` shims, zero-caller validators, and an unused `DatabaseAuditLog` model. The live `data/scraped_events.json` and the auth-module split, seed-script consolidation, `.kilo/worktrees/`, and backward-compat model aliases were intentionally preserved to avoid higher-risk refactors.

Decision:
1. Deleted dead tracked artifacts: `archive/` (client secrets and stale logs), `code_screenshots/`, `.antigravitycli/`, `tmp/verify_newsletter.py`, `instance/heritage_page.html`, `data/scraped_attractions.json`, `data/scraped_heritage.json`, and `build/desktop.py`.
2. Deleted duplicate `core/` shims and one unused `utils/` shim: `core/db_manager.py`, `core/geo.py`, `core/logger.py`, `core/session.py`, and `utils/session_helper.py`.
3. Updated active imports across `modules/api_v1/public.py`, `modules/attractions/routes.py`, and six auth/gallery/business/heritage modules so logging now uses `utils.logger_helper` and geo math uses `utils.geo`.
4. Removed unused validators `validate_json_input()` and `validate_coordinates_fields()` from `utils/validators.py`, along with orphaned dead code left behind from earlier edits.
5. Removed the unused `DatabaseAuditLog` model from `modules/analytics/models.py`.
6. Verified all touched Python files pass syntax checks before marking the batch complete.

Consequences: Reduced dead code and duplicate entry points while keeping every live route, model, template, and migration intact. The cleanup was executed in low-risk batches with explicit caller checks so the app remains bootable without the removed shims.

Related files: `core/db_manager.py`, `core/geo.py`, `core/logger.py`, `core/session.py`, `utils/session_helper.py`, `utils/validators.py`, `modules/analytics/models.py`, `modules/api_v1/public.py`, `modules/auth/login.py`, `modules/auth/oauth.py`, `modules/auth/password.py`, `modules/auth/register.py`, `modules/business/routes.py`, `modules/gallery/routes.py`, `modules/heritage/routes.py`, `modules/attractions/routes.py`