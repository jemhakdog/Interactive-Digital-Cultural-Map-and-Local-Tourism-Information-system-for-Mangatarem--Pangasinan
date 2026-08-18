# Process Map Implementation Plan

## Original Location
`/docs/planning/PLAN-process-map.md`

## Status: ❌ NOT IMPLEMENTED

### What Was Planned

Add a sequential process map (Data Relationship/Flow Diagram) to `erd_v1.drawio` as a new page showing:
1. Manual Field Survey → Heritage data collection
2. System Digitization → Digital form encoding
3. Admin Validation → Quality control/approval
4. Database Sync → Supabase persistence
5. Georeferencing → GIS mapping
6. Public Discovery → Interactive map visualization

### Proposed Changes

#### File Modifications
- Append new `<diagram>` element to `erd_v1.drawio`
- Create `scripts/add_process_map.py` to programmatically inject diagram

### Current State

❌ **Not Implemented:**
- `erd_v1.drawio` not found in `docs/diagrams/`
- `scripts/add_process_map.py` does not exist
- No process map diagram exists

### Priority
Medium (documentation clarity)

### Estimated Effort
2-3 hours

### Next Steps
1. Create or locate `erd_v1.drawio`
2. Create `scripts/add_process_map.py`
3. Define process nodes and flows
4. Inject new diagram page
5. Verify in Draw.io viewer
