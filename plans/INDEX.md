# Plans Index

Master index of all implementation plans for the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan.

---

## 📊 Summary

| Status | Count | Description |
|--------|-------|-------------|
| ✅ Complete | 19 | Plans fully implemented and verified |
| ⚠️ Partial | 2 | Plans partially done or need final checks |
| ❌ Not Started | 3 | Plans not yet implemented |
| **Total** | **24** | All plans tracked |

---

## ✅ Complete Plans (19)

These plans have been **fully implemented** and verified:

1. **CSRF Token Implementation** → [`complete/CSRF_IMPLEMENTATION_PLAN.md`](complete/CSRF_IMPLEMENTATION_PLAN.md)
   - All 35 forms protected with CSRF tokens
   - Status: ✅ FULLY IMPLEMENTED

2. **Business Portal (Accommodations & Dining)** → [`complete/BUSINESS_PORTAL_PLAN.md`](complete/BUSINESS_PORTAL_PLAN.md)
   - Establishment, Room, Menu, Review models complete
   - Business owner dashboard and CRUD operational
   - Status: ✅ FULLY IMPLEMENTED

3. **Admin Desktop Application** → [`complete/ADMIN_DESKTOP_APP_PLAN.md`](complete/ADMIN_DESKTOP_APP_PLAN.md)
   - `desktop.py` with FlaskUI wrapper
   - Status: ✅ FULLY IMPLEMENTED

4. **High Concurrency Map Architecture (MVT)** → [`complete/MAP_CONCURRENCY_PLAN.md`](complete/MAP_CONCURRENCY_PLAN.md)
   - PostGIS ST_AsMVT tile generation
   - Status: ✅ FULLY IMPLEMENTED

5. **CSS/JS Separation** → [`complete/CSS_JS_SEPARATION_PLAN.md`](complete/CSS_JS_SEPARATION_PLAN.md)
   - 23 CSS + 24 JS files, all 59 templates updated
   - Status: ✅ FULLY IMPLEMENTED

6. **Heritage Routes** → [`complete/HERITAGE_ROUTES_PLAN.md`](complete/HERITAGE_ROUTES_PLAN.md)
   - Admin CRUD for 5 heritage types, public pages live
   - Status: ✅ FULLY IMPLEMENTED

7. **Heritage Templates** → [`complete/HERITAGE_TEMPLATES_PLAN.md`](complete/HERITAGE_TEMPLATES_PLAN.md)
   - Admin templates for heritage management
   - Status: ✅ FULLY IMPLEMENTED

8. **Codebase Organization** → [`complete/ORGANIZATION_PLAN.md`](complete/ORGANIZATION_PLAN.md)
   - Files organized, no code affected
   - Status: ✅ FULLY IMPLEMENTED

9. **Database Manager Migration** → [`complete/DB_MANAGER_MIGRATION_PLAN.md`](complete/DB_MANAGER_MIGRATION_PLAN.md)
   - Multi-provider database support (SQLite, MySQL, Supabase)
   - Status: ✅ FULLY IMPLEMENTED

10. **Architecture Diagram** → [`complete/ARCHITECTURE_DIAGRAM_PLAN.md`](complete/ARCHITECTURE_DIAGRAM_PLAN.md)
    - `system-architecture.drawio` updated with modern tech stack
    - Status: ✅ FULLY IMPLEMENTED (2026-03-24)

11. **Remove VENV from Git** → [`complete/REMOVE_VENV_PLAN.md`](complete/REMOVE_VENV_PLAN.md)
    - `.venv/` not tracked, `.gitignore` configured
    - Status: ✅ FULLY IMPLEMENTED

12. **DFD Intersections Removal** → [`complete/DFD_INTERSECTIONS_PLAN.md`](complete/DFD_INTERSECTIONS_PLAN.md)
    - DFD v5 hub-and-spoke layout, all edges snapped
    - Status: ✅ FULLY IMPLEMENTED

13. **Update DFD** → [`complete/UPDATE_DFD_PLAN.md`](complete/UPDATE_DFD_PLAN.md)
    - `dfd-level-1-clean_v5.drawio` + `dfd-level-0_v5.drawio` complete
    - Status: ✅ FULLY IMPLEMENTED

14. **Update ERD** → [`complete/UPDATE_ERD_PLAN.md`](complete/UPDATE_ERD_PLAN.md)
    - `erd_v3.drawio` with all models and relationships wired
    - Status: ✅ FULLY IMPLEMENTED

15. **ERD and Flowchart Improvements** → [`complete/ERD_FLOWCHART_IMPROVEMENTS_PLAN.md`](complete/ERD_FLOWCHART_IMPROVEMENTS_PLAN.md)
    - ERD v1-v3 exist, heritage models implemented, flowcharts complete
    - Status: ✅ FULLY IMPLEMENTED

16. **Documents Dashboard Enhancement** → [`complete/DOCUMENTS_DASHBOARD_ENHANCEMENT_PLAN.md`](complete/DOCUMENTS_DASHBOARD_ENHANCEMENT_PLAN.md)
    - 11 templates, JS component, full editor suite
    - Status: ✅ FULLY IMPLEMENTED

17. **ERD Entity Naming** → [`complete/ERD_ENTITY_NAMING_PLAN.md`](complete/ERD_ENTITY_NAMING_PLAN.md)
    - Consistent PK/FK annotations in mermaid schema
    - Status: ✅ FULLY IMPLEMENTED

18. **Admin Docs** → [`complete/ADMIN_DOCS_PLAN.md`](complete/ADMIN_DOCS_PLAN.md)
    - Defense guides, team briefings, and chapter coverage
    - Status: ✅ FULLY IMPLEMENTED

19. **Remove PocketBase Dependencies** → [`complete/REMOVE_POCKETBASE_PLAN.md`](complete/REMOVE_POCKETBASE_PLAN.md)
    - No `pocketbase` in requirements, no source/test files, cache cleaned
    - Status: ✅ FULLY IMPLEMENTED

---

## ⚠️ Partial/Needs Verification (2)

These plans are **partially implemented** or need final verification:

1. **Capstone Docs** → [`pending/CAPSTONE_DOCS_PLAN.md`](pending/CAPSTONE_DOCS_PLAN.md)
   - Chapters exist but `todo.md` has ~15 unresolved items (typos, RRL verification, Mermaid→image conversion)
   - Priority: High
   - Status: ⚠️ PARTIALLY IMPLEMENTED

2. **Content Approval & SQLite Migration** → [`pending/CONTENT_APPROVAL_SQLITE_MIGRATION_PLAN.md`](pending/CONTENT_APPROVAL_SQLITE_MIGRATION_PLAN.md)
   - DB manager done, but `reviewed_by`/`reviewed_at` fields missing from `models.py`
   - Priority: High
   - Estimated: 2-3 hours
   - Status: ⚠️ PARTIALLY IMPLEMENTED

---

## ❌ Not Started (3)

1. **Trip Cost Estimator** → [`pending/TRIP_COST_ESTIMATOR_PLAN.md`](pending/TRIP_COST_ESTIMATOR_PLAN.md) — 16-22 hours
2. **Process Map** → [`pending/PROCESS_MAP_PLAN.md`](pending/PROCESS_MAP_PLAN.md) — 2-3 hours
3. **Defense Printable Docs** → [`pending/DEFENSE_PRINTABLE_DOCS_PLAN.md`](pending/DEFENSE_PRINTABLE_DOCS_PLAN.md) — 2-3 hours

---

## 📁 Original Plan Locations

Plans were originally scattered across:

- Root directory: `CSRF_IMPLEMENTATION_PLAN.md`
- `docs/` directory: 5 PLAN-*.md files
- `docs/planning/` directory: 17 PLAN-*.md files
- `db_update_package/`: implementation_plan.md
- `archive/`: 1 archived plan

---

## 🔄 How This Index Works

- **Complete plans** are moved to `plans/complete/` with verification evidence
- **Pending plans** remain in `plans/pending/` with next steps
- Each plan file contains:
  - Original location reference
  - Implementation status with verification evidence
  - What was planned vs what was implemented
  - Priority level and effort estimates
  - Next steps (for pending plans)

---

## 📋 Next Actions

### High Priority
1. Implement Trip Cost Estimator (16-22 hours)
2. Add `reviewed_by`/`reviewed_at` content approval fields to `models.py` (2-3 hours)
3. Fix ~15 capstone doc typos and formatting items in `todo.md` (2-3 hours)

### Medium Priority
4. Create Defense Printable Docs handout (2-3 hours)
5. Create Process Map diagram (2-3 hours)

---

**Last Updated:** 2026-07-29
**Total Plans:** 24 (19 complete, 2 partial, 3 not started)
**Original plan files:** Remain in their source locations (`docs/`, `docs/planning/`, root, etc.)
**Organized plans:** This `/plans/` directory contains verified status reports
