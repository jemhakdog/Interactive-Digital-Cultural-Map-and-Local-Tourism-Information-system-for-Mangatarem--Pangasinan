# PLAN: Update Data Flow Diagram (DFD)

This plan outlines the updates required for the Data Flow Diagram (DFD) to reflect the recent modular transformation of the heritage schema (Profile + 1:1 Detail tables).

## User Review Required

> [!IMPORTANT]
> Please provide feedback on these structural decisions before implementation:
> 1. **Data Store Granularity**: Should we add `Heritage Profile` as a central data store linking to details, or keep it logical?
> 2. **Process Refinement**: Is `P9.0: Heritage Management` sufficient, or do we need sub-processes for the modular flow?
> 3. **Missing Stores**: Should `Built Heritage` and `Movable Heritage` be added as explicit stores?

## Proposed Changes

### [DFD Level 1]
- [ ] **[MODIFY] [generate_dfd.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/diagrams/generate_dfd.py)**:
    - Update `ELEMENTS` to include `Heritage_Profile` data store.
    - Add missing heritage detail stores: `Built_Heritage`, `Movable_Heritage`.
    - Update `FLOWS` to route data through the Profile store.
    - Adjust layout positions to maintain a clean Hub-and-Spoke visual.

## Verification Plan

### Automated Tests
- [ ] Run `python docs/diagrams/generate_dfd.py` and verify zero errors.
- [ ] Check `docs/diagrams/dfd-level-1-clean_v1.drawio` for visual correctness.

### Manual Verification
- [ ] Review the generated XML in Draw.io to ensure no line intersections.
- [ ] Confirm all heritage types match the latest SQL schema.
