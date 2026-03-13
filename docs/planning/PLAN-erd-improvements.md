# PLAN: ERD and Flowchart Improvements

This plan outlines the steps to improve the Entity-Relationship Diagram (ERD) and the Flowchart of the current process to better reflect the use of manual heritage forms and their digital integration into the system.

## Overview
The goal is to align the project's documentation with the manual Word forms (01A-07) used by the Mangatarem Tourism Office.
1. **Flowchart**: Will be updated to show the manual "Forms" as steps and identify them as bottlenecks.
2. **ERD**: Will be refined to ensure each form corresponds to a clear entity with attributes mapped from the form fields, identifying appropriate primary keys.

## User Review Required
> [!IMPORTANT]
> - Should the flowchart specifically name each form (e.g., "Form 01A") or use a general "Manual Heritage Form" label?
> - For the ERD, do you prefer a consolidated "HeritageItem" table with a type discriminator, or separate tables for each form as currently implemented in `heritage_models/`?

## Proposed Changes

### Documentation & Diagrams
#### [MODIFY] [erd_v1.drawio](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/diagrams/erd_v1.drawio)
- Update entities to match the structure defined in `docs/TOURISM_FORMS_FIELD_REFERENCE.md`.
- Label primary keys (e.g., `id` for each heritage table).
- Ensure relationships (e.g., `user_id` as foreign key to `USER`) are clearly visualized.

#### [MODIFY] [flowchart.drawio](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/diagrams/flowchart.drawio)
- Insert steps representing manual form completion.
- Use visual cues (e.g., different colors or annotations) to highlight bottlenecks in manual filing and retrieval.

### Database Models (Reference)
#### [MODIFY] [models.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/models.py)
- Ensure all heritage models are accurately reflected in the ERD.

## Verification Plan
### Manual Verification
- Review updated `erd_v1.drawio` in Draw.io to confirm all forms from `docs/interview_data/gathered_froms/` are represented.
- Review `flowchart.drawio` to ensure the manual "bottlenecks" are clearly identifiable.
- Cross-reference `docs/TOURISM_FORMS_FIELD_REFERENCE.md` with the ERD attributes.
