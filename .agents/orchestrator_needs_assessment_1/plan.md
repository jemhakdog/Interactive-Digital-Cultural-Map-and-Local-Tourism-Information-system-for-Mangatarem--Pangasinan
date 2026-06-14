# Plan: Codebase Needs Assessment Audit

## Objective
Analyze the Mangatarem Cultural Map codebase and produce a detailed audit and gap analysis report detailing exact matches, partial matches, and complete gaps based on the needs assessment requirements.

## Steps
1. **Explore & Analyze**: Spawn `teamwork_preview_explorer` to locate and analyze relevant models, templates, controllers, middleware, and schemas for the following modules:
   - Contributor Module (Barangay Representatives: events, announcements, photos, profile updates)
   - Central Admin Approval Module (LGU Tourism Office reviews, approves/rejects submissions)
   - Centralized Database & Core Features (Map layers with dual-marker/brochures, event calendar, visitor dashboard with stats)
   - Security, Roles, & LGU Policies (Tourists, Contributors, Admins; data privacy)
2. **Review Explorer Handoff**: Synthesize findings, identify files, paths, and missing routes/schemas.
3. **Generate Audit Report**: Spawn `teamwork_preview_worker` to write the audit/gap analysis report markdown file to `docs/gap_analysis.md`.
4. **Final Verification**: Verify file existence and contents, then send the handoff back to the main caller agent.
