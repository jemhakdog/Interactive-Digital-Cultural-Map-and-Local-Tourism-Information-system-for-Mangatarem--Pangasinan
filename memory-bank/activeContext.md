# Active Context

## Current focus

- Implementing and optimizing Progressive Web App (PWA) features to deliver high-fidelity offline mapping capabilities, rich install prompts, and automatic system updates.
- Maintaining alignment and integrity across structural design models (ERD, DFD) and the active database schema.

## Recent changes

- **Physical Database Schema Table Consolidation:**
  - Physically consolidated and collapsed two redundant tables in the database schema to reduce database complexity from 27 tables down to 24 tables:
    - **Merged `PasswordResetToken` into `User`:** Stored token validation attributes (`reset_token`, `reset_token_expires_at`, `reset_token_used`) directly in the `USER` table, deprecating the `PASSWORD_RESET_TOKEN` table.
    - **Merged `ReviewPhoto` into `Review`:** Added `photo_urls` JSON column (array of strings) directly to the `REVIEW` table, deprecating the `REVIEW_PHOTO` table.
  - Implemented extremely robust SQLAlchemy backward-compatibility shims inside `modules/auth/models.py` and `modules/attractions/models.py` to prevent breaking existing WTForms validations, templates (`self.photos.all()`), or database seed scripts.
  - Updated campaign route validations in `modules/auth/password.py` and file upload handlers in `modules/attractions/routes.py` to target the consolidated JSON/column paths directly.
- **Visual ERD Diagram Alignment and Spacing (`erd_v3.drawio`):**
  - Programmatically parsed, aligned, and optimized the single-page ERD diagram in `erd_v3.drawio` to enforce a mathematically perfect **3-inch (288-pixel) spacing** on all sides.
  - Aligned all 24 database tables across 5 vertical columns, setting exact horizontal gap boundaries of 288 pixels and vertical spacing of 288 pixels between adjacent elements.
  - Stripped manual bend/route points from all 36 relationship edges to trigger clean orthogonal auto-routing around table shapes.
  - Mathematically verified the layout using a custom validation script `verify_erd_layout.py` which returned 0 errors.

- **Sequential DFD Level-1 Chronological Refactoring & Line Optimization (`dfd-level-1-clean_v4.drawio`):**
  - Re-architected the DFD Level-1 diagram (`dfd-level-1-clean_v4.drawio`) from scratch using a custom Python script (`generate_dfd_v4.py`) executed with `uv run`.
  - Refactored all 15 core system processes to match the **Chronological User-Journey sequence** (Option A: Onboarding -> Exploration -> Discovery -> Feedback -> Booking -> Contributions -> Verification -> Analytics -> Auditing).
  - Consolidated datastores to match the active optimized schema of **21 tables** (collapsing legacy columns and sub-tables).
  - Enforced a spacious **5-column visual layout** with clean orthogonal routing and background label masking, eliminating all overlapping and jumbled data flow lines.
  - **Drawn DFD V4.1/V4.2/V4.3 local datastore & entity duplication:**
    - Duplicated D2 `Attraction_db`, D3 `Event_db`, and D6 `Favorite_db` to establish local-routing datastores directly positioned next to the backend management processes (processes `9.0`, `10.0`, `13.0`, and `14.0`).
    - Duplicated the massive **TOURIST** entity into localized, task-focused nodes (e.g., Onboarding tourist, review tourist, messaging tourist) positioned locally down Column 1. This completely removes the massive spider-web of routing lines traveling across the entire vertical height of Column 1, ensuring every edge routes locally with zero vertical crossovers.
    - **Y-Axis Alignment (V4.3):** Placed every datastore at the precise vertical Y-coordinate matching its corresponding horizontal process. (e.g., aligning P4.0 with `Review_db` at Y: 690, P6.0 with `Booking_db` at Y: 1050, and P7.0 with `Chat_db` at Y: 1230). This achieves a completely horizontal, crossover-free grid pattern for datastore read/write flows.



 
## Next step
 
- Return active focus to developing the Map V2 frontend design and interface.