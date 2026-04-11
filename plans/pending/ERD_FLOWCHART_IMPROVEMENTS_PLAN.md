# ERD and Flowchart Improvements Plan

## Original Location
`/docs/planning/PLAN-erd-improvements.md`

## Status: ⚠️ NEEDS VERIFICATION

### What Was Planned

Improve Entity-Relationship Diagram (ERD) and Flowchart to:
1. Align with manual heritage forms (01A-07)
2. Update flowchart to show manual form bottlenecks
3. Ensure ERD entities match `TOURISM_FORMS_FIELD_REFERENCE.md`
4. Label primary keys and relationships clearly

### Proposed Changes

#### ERD Updates
- Update entities to match heritage form structure
- Label primary keys clearly
- Ensure relationships (user_id foreign keys) are visualized

#### Flowchart Updates
- Insert manual form completion steps
- Highlight bottlenecks in manual filing/retrieval
- Use visual cues for manual vs digital processes

### Current State

⚠️ **Needs Verification:**
- `docs/diagrams/erd_v1.drawio` not found (only `existing_workflow.drawio` and `system-architecture.drawio` exist)
- `docs/diagrams/flowchart.drawio` not found
- Heritage models ARE implemented in main `models.py` (5 heritage types)
- Main models.py does NOT have `reviewed_by`/`reviewed_at` fields (only in `db_update_package/models.py`)

### Priority
Medium (documentation alignment)

### Estimated Effort
2-3 hours

### Next Steps
1. Locate or recreate `erd_v1.drawio` and `flowchart.drawio`
2. Update ERD to match current models.py implementation
3. Add flowchart manual form bottleneck annotations
4. Cross-reference with TOURISM_FORMS_FIELD_REFERENCE.md
