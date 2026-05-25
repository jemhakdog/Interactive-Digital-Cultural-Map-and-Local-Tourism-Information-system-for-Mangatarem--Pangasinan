# Active Context

## Current focus

- Successfully completed the comprehensive rewrite of Chapters 1–3 of the capstone manuscript to align with the formal third-person academic voice of the BLRT template, resolving all 12+ items in the `todo.md` checklist.
- Developed a dynamic Markdown-to-DOCX compiler in `make.py` that automatically translates formatting styles, lists, and tables into a clean Times New Roman Word file.
- Completed full Level 1 DFD (V3.2) and ERD (V3.2) layout polishing and dynamic snaps: purged absolute source/target offset overrides and custom intermediate control point arrays to allow dynamic orthogonal edge routing, injected the missing `BUSINESS_VERIFICATION` table, resolved duplicate process numbering, and aligned all data stores perfectly with the consolidated active SQLAlchemy V3 schema.

## Recent changes

- Rewrote `Chapter-1-Introduction.md` to enforce strict third-person paragraphs (removing all background/scope/limitation bullets) and fully integrated 5 local and 5 foreign citations (2020-2025) with a comprehensive synthesis.
- Rewrote `Chapter-2-Methodology-and-Design.md` to formally integrate Surveys and Questionnaires, define spatial diagram notations and symbols, underline primary keys, and align the RAD Gantt chart timeline with a realistic academic calendar starting June 2024.
- Rewrote `Chapter-3-Results-and-Discussion.md` to organize features by user roles, align Historical Data Archives with the Municipal Archives source, correct testing typos, and document ISO/IEC 25010 testing plans.
- Consolidated individual markdown files into `full chapters.md` and compiled `Chapter_1_to_3_Consolidated.docx` dynamically using `make.py` with zero errors.
- Executed automated quality validation audits via `verify_manuscript.py`, returning 0 pronoun warnings and 0 unresolved typos.
- Polished `docs/diagrams/dfd/dfd-level-1-clean_v3.drawio` to remove Context-level boundaries, delete the central hub bubble, consolidate legacy heritage detail tables directly to D15 `Heritage_Profile`, renumber duplicate processes, and inject new missing datastores (`Map_Feedback_db` and `Business_Verification_db`).
- Polished `docs/diagrams/erd/erd_v3.drawio` to inject the missing active model `BUSINESS_VERIFICATION` and wire its relationship to `USER`.
- Cleaned up edge routing by removing all hardcoded `sourcePoint`/`targetPoint` overrides and `mxPoint` arrays in both diagrams, resolving floating arrows and ensuring dynamic orthogonal snapping layout.

## Next step

- Return active focus to developing the Map V2 frontend design and interface.