# PLAN: Update ERD to Modular Heritage Schema

This plan outlines the steps to update the Entity-Relationship Diagram (ERD) to reflect the recent database refactoring, where heritage data was split into a central `HeritageProfile` and specialized `_details` tables.

## User Review Required
> [!IMPORTANT]
> To ensure the ERD is as useful as possible, please clarify:
> 1. **Old Tables**: Remove old redundant tables (`natural_heritage`, etc.) from the diagram? (Assumed: YES)
> 2. **Layout**: Keep the 4-column layout or use a "Hub-and-Spoke" layout for the `HeritageProfile` and its 7 detail tables? (Assumed: Grouped/Hub-and-Spoke)
> 3. **Field Density**: List all fields or just key identifying attributes? (Assumed: Core fields only for clarity)

## Proposed Changes

### Diagram Generation Script
#### [MODIFY] [generate_erd.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/diagrams/generate_erd.py)
- Update the `TABLES` dictionary to include:
    - `HERITAGE_PROFILE`: The central hub for shared metadata.
    - Specialized detail tables: `built_heritage_details`, `movable_heritage_details`, `natural_heritage_details`, `intangible_heritage_details`, `personality_details`, `institution_details`, `lgu_program_details`.
- Update `RELATIONSHIPS` to show:
    - 1:1 relationships between `HERITAGE_PROFILE` and each detail table.
    - 1:1 relationship between `ATTRACTION` and `HERITAGE_PROFILE`.
- Adjust layout logic to group heritage detail tables around the central profile.

### Visual Document
#### [MODIFY] [erd_v1.drawio](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/erd_v1.drawio)
- Run the updated `generate_erd.py` to overwrite/update the visual diagram.

## Verification Plan
### Automated Verification
- Run `python docs/diagrams/generate_erd.py` and ensure it completes without error.
- Check the generated XML structure for correct entity counts.

### Manual Verification
- Open `erd_v1.drawio` in Draw.io.
- Verify that the relationships between `ATTRACTION` -> `HERITAGE_PROFILE` -> `DETAILS` are correctly paths.
- Confirm field types (JSONB, Date, etc.) match the refactored SQL schema.
