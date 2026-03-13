# Implementation Plan - Overall Sequential Process Map

Add a high-level sequential process map (Data Relationship/Flow Diagram) to the `erd_v1.drawio` file as a new page. This map will illustrate the "overall" workflow from manual heritage data collection to digital public access.

## Proposed Changes

### [Documentation & Diagrams]

#### [MODIFY] [erd_v1.drawio](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/diagrams/erd_v1.drawio)
- Append a new `<diagram>` element representing the "Overall Sequential Process Map".
- The map will use a "pure drd" (Data Relationship/Flow Diagram) style, focusing on the sequential flow of data across system actors.

#### [NEW] [add_process_map.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/scripts/add_process_map.py)
- A specialized script to programmatically inject the new diagram page into the XML structure.
- Logic:
  1. Load existing `erd_v1.drawio`.
  2. Define the process nodes (Manual Collection, Digitization, Review, Persistent Storage, GIS Mapping, Public Access).
  3. Generate mxCells with appropriate styling.
  4. Append the diagram to the XML root.
  5. Save the file.

### Process Stages to be Mapped:
1. **Manual Field Survey**: Heritage data collected via Word forms and field notes.
2. **System Digitization**: Encoding data into the digital forms via the Barangay/Admin Dashboard.
3. **Admin Validation**: Quality control and approval by the Municipal Tourism Office.
4. **Database Sync**: Persistence in the Supabase relational database.
5. **Georeferencing**: GIS mapping and thumbnail/gallery generation.
6. **Public Discovery**: Visualization on the Interactive Digital Cultural Map.

## Verification Plan

### Automated Tests
- Run `python scripts/add_process_map.py docs/diagrams/erd_v1.drawio`.
- Verify the output XML structure contains two `<diagram>` elements.
- Check for ID collisions in the new cells.

### Manual Verification
- Open `erd_v1.drawio` in a Draw.io viewer.
- Switch to the new page (likely named "Overall Process Map").
- Visually verify the flow logic and text legibility.
