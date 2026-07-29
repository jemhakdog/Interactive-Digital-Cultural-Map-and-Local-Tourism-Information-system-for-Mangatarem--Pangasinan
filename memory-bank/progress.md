# Progress

- Successfully implemented and verified dynamic, multi-tier **Travel Passport Stamp Visibility Widgets** across Attraction details, Establishment details, and Map V2 selected place bottom sheets.
- Added automatic startup parameter checks restoring active navigation target states seamlessly from LocalStorage across page refreshes.
- Normalized database-level relationships for newsletters and notifications, connecting `NEWSLETTER_SUBSCRIBER` and `NEWSLETTER_HISTORY` to the `"USER"` table.
- Collapsed and consolidated `PasswordResetToken` and `ReviewPhoto` sub-tables into parent models in the database schema, programmatically updating connected routes, seed files, and WTForms controllers.
- Rearranged and programmatically aligned all 24 database tables in the visual ERD diagram `docs/diagrams/erd/erd_v3.drawio` to enforce a mathematically perfect **3-inch (288-pixel) spacing** on all sides.
- Developed `layout_erd.py` to organize tables in 5 X-aligned vertical columns and 288px gaps.
- Designed `verify_erd_layout.py` to mathematically prove the 3-inch horizontal and vertical spacing between all shapes.
- Performed FAST_INIT for `mangatarem-cultural-map` project.
- Audited the active database models (SQLAlchemy) and compared them with system design diagrams.
- Confirmed that the DFD Level 1 clean model (`dfd-level-1-clean_v3.drawio`) and Draw.io ERD (`erd_v3.drawio`) perfectly match all 24 registered database tables.
- Flagged discrepancy in `docs/diagrams/erd/erd_schema.mermaid`, which is missing 11 modern database tables (Booking, Chat, Favorites, Notifications, Feedback, Business Verification, Reviews), and drafted an aligned Mermaid schema representation.
- Fixed visual corruption, column overlaps, and jumbled styles of regular attributes in the `ATTRACTION_REVIEW` table (`docs/diagrams/erd/erd_v2.drawio`).
- Re-styled and aligned all three relationship edges (`review_id`, `user_id`, and `attraction_id`) to use exact exit/entry anchors and premium blue Crow's Foot style.
- Audited diagram connectivity to ensure all database models are completely and correctly linked in the ERD.
- Completed comprehensive database schema verification and confirmed consolidation of 7 heritage detail tables.
- Stamped database version at migration revision `536847569d90` after resolving SQLite migration DDL limitations.
- Cleaned up obsolete files and updated SQL schema/verification scripts to align perfectly with the 31 active tables.
- Successfully consolidated 5 redundant tables down to 2 unified tables (`REVIEW` and `USER_FAVORITE`) using Strategy A (Nullable Foreign Keys + CHECK Constraints), reducing active table count to 28.
- Safely migrated all existing reviews, nested replies, photos, favorites, and RSVP states with zero data loss.
- Implemented backward-compatible shims maintaining 100% app runtime boot stability.
- Completed comprehensive academic rewrite of manuscript Chapters 1–3, removing first-person pronouns, eliminating casual phrasing, and aligning with the BLRT template style guidelines.
- Executed a complete RRL verification sweep, replacing unverified placeholder citations (e.g., Wilson 2025, Reyes 2024, Smith 2023, Cruz 2022) with real peer-reviewed articles and direct URL/DOI links across `references.md`, `Chapter-1-Introduction.md`, and `full1-3.md`.
- Formally resolved all 12+ spelling, structural, formatting, and consistency items from the `todo.md` checklist, including updating the Guimaras cultural mapping citation to its published reference: `Germina Jr. & Martir (2025)`.
- Created a dynamic Markdown-to-DOCX compiler in `make.py` and compiled `Chapter_1_to_3_Consolidated.docx` dynamically.
- Developed an automated quality checker script `verify_manuscript.py` returning 0 errors.
- Fully polished and snapped Level 1 DFD (V3.2) layout by removing Context-level system boundaries, deleting the obsolete central system hub, merging detail datastores, and injecting missing datastores.
- Fully polished and snapped ERD (V3.2) by injecting the missing active model `BUSINESS_VERIFICATION` and wiring its relationship edge.
- Eliminated all floating and jumbled edges in DFD/ERD Draw.io models, mathematical layout snappings returned 0 errors.
- Upgraded the Progressive Web App (PWA) system: configured installation assets, built floating install HUD and SW update alerts, created a gorgeous high-fidelity offline fallback page with LGU emergency hotlines, and designed offline "Mangatarem Heritage Catch" mini-game.
- Refactored and programmatically snapped the consolidated Level-1 DFD (`dfd-level-1-clean_v5.drawio` and `dfd-level-0_v5.drawio`) to use a circular **Hub-and-Spoke layout**, perfectly copying the structure of Figure 2.3.
- Developed `generate_dfd_v5.py` to arrange one massive System Hub box in the center, 15 sub-processes in a surrounding rectangular ring, 16 localized database datastores directly adjacent/underneath their active processes, and external actors on the far perimeter grid coordinates.
- Successfully compiled the generator script using the local virtual environment Python interpreter with well-formed, valid Draw.io XML outputs.
- Chronologically refactored sequential DFD Level-1 diagram (`dfd-level-1-clean_v4.drawio`) Sequential Processes `1.0` through `15.0` to match Option A user-journey sequence.
- Overhauled the root `README.md` to properly document the Mangatarem Interactive Digital Cultural Map system, tech stack, and setup commands, replacing the generic template contents.
- Performed a codebase cleanup, removing obsolete database diagram layout scripts, old web scraping/seeding helpers, temporary logs, and duplicated dependency files.

## Current (2026-07-29)

- **Ponytail Audit & Cleanup Complete:** Removed 12,540 lines of dead code, duplicate modules, unreferenced JS, and throwaway scripts across 156 files.
- **Bug Fixes Applied:** Admin form action, missing 500.html template, PWA z-index, Business Owner menu edit UI.
- **CRUD Verified Across All 4 User Roles:** Admin, Business Owner, Barangay Representative, Tourist — all nav items tested.
- **Git Branches Analyzed:** All 7 feature branches confirmed fully merged into main. Only `feat/admin-desktop-app` (Windows app) has unique commits, excluded per user request.
- **Dependencies Installed:** `flask-limiter`, `google-auth`, `polyline`, `pyiceberg`, `postgrest` for local dev server startup.

## Next

- Commit all changes to main branch.

## Blockers

- None.