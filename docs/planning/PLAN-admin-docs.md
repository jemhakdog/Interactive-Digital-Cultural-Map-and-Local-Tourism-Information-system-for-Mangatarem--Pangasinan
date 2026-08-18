# Admin Document Management Routes

Complete admin section for managing interview data forms — view, edit the JSON structure, download/export `.docx` originals, and import new `.docx` forms.

## Data Inventory

| Form | File | Category |
|------|------|----------|
| Form 01A | Natural Resources - Land formation | Natural Heritage |
| Form 02A | Tangible Immovable - Govt/Commercial Buildings | Built Heritage |
| Form 03A | Tangible Movable - Archaeological | Archaeological |
| Form 04A | Intangible Heritage - Oral Traditions | Intangible |
| Form 05 | Personalities | Personalities |
| Form 06 | Cultural Institutions | Institutions |
| Form 07 | LGU Programs/Projects | LGU Programs |

- **Source JSON**: `docs/interview_data/forms_structure_analysis.json` — parsed structure of each form (paragraphs, tables, fields)
- **DOCX Originals**: `docs/interview_data/gathered_froms/` — 7 `.docx` files

---

## Proposed Changes

### Backend Routes

#### [NEW] `routes/admin/documents.py`

New admin sub-module following the existing pattern in `routes/admin/`. All routes require admin login.

| Route | Method | Purpose |
|-------|--------|---------|
| `/admin/documents` | GET | Dashboard — card grid of all 7 forms with stats (paragraph count, table count) |
| `/admin/documents/<form_key>` | GET | View — read-only display of a form's parsed structure (paragraphs + tables) |
| `/admin/documents/<form_key>/edit` | GET/POST | Edit — JSON editor for modifying the form's structure in `forms_structure_analysis.json` |
| `/admin/documents/<form_key>/export` | GET | Export — download the matching `.docx` file from `gathered_froms/` |
| `/admin/documents/export-all` | GET | Export All — zip all 7 `.docx` files and download |
| `/admin/documents/import` | POST | Import — upload a new `.docx` file, parse it, update the JSON |

**Key implementation details:**
- Forms are loaded from `forms_structure_analysis.json` at runtime (no DB model needed)
- A `FORM_REGISTRY` dict maps JSON keys → slugified route keys + display metadata
- Export uses `flask.send_from_directory` for individual `.docx`; uses `zipfile` for bulk export
- Import uses `python-docx` to parse uploaded `.docx` → updates the JSON file
- Edit route provides a `<textarea>` with the form's JSON, validates on save

---

#### [MODIFY] `routes/admin/__init__.py`

Add `documents` to the import list:

```diff
-from . import dashboard, users, attractions, events, content, heritage  # noqa: F401
+from . import dashboard, users, attractions, events, content, heritage, documents  # noqa: F401
```

---

### Templates

#### [NEW] `templates/admin/documents_dashboard.html`

Card grid extending `admin/dashboard.html`. Each card shows:
- Form name, category label, paragraph/table counts
- Buttons: View | Edit | Export (.docx)
- Top action bar: "Export All" + "Import Form"
- Follows existing glass-card + emerald accent dark theme

#### [NEW] `templates/admin/documents_view.html`

Read-only view of a single form's parsed structure:
- Sections rendered from paragraphs with index highlighting
- Tables rendered as HTML `<table>` with borders
- Back button + Edit/Export actions

#### [NEW] `templates/admin/documents_edit.html`

Edit form with:
- JSON `<textarea>` (monospace font, syntax-highlighted via CSS)
- Preview panel showing rendered paragraphs/tables
- Save + Cancel buttons
- Client-side JSON validation before submit

#### [NEW] `templates/admin/documents_import.html`

Modal or inline form:
- File upload input (`.docx` only)
- Form name input (auto-detected from filename)
- Import button with confirmation

---

### Navigation

#### [MODIFY] `templates/includes/admin_nav.html`

Add "Documents" link between Heritage and View Site, with a document icon SVG. Active state when endpoint starts with `admin.admin_documents`.

---

### Dependencies

> [!NOTE]
> `python-docx` is required for import functionality. If it's not already installed, it will need to be added. The project already used it previously for `forms_structure_analysis.json` generation.

---

## User Review Required

> [!IMPORTANT]
> **No database changes needed** — all data lives in flat files (`JSON` + `DOCX`). This means no migrations, but also means concurrent edits could cause data loss. For a single-admin system this is acceptable.

> [!WARNING]
> **Import replaces form data** — importing a `.docx` for an existing form key will overwrite its entry in the JSON. The old `.docx` file in `gathered_froms/` will also be replaced. A backup copy is saved with a timestamp suffix before overwrite.

**Questions:**
1. Should the import create a backup of the old `.docx` and JSON entry before overwriting, or is a simple replace acceptable?
2. Do you want the edit page to also allow editing individual paragraph text inline (richer UI), or is a raw JSON editor sufficient for now?
3. Should "Export All" include the `forms_structure_analysis.json` in the zip alongside the `.docx` files?

---

## Verification Plan

### Manual Verification

1. **Start dev server**: `python app.py` → navigate to `http://localhost:5000/admin/documents`
2. **Dashboard**: Verify all 7 form cards render with correct counts
3. **View**: Click each form → verify paragraphs and tables display correctly
4. **Edit**: Edit a form's JSON → save → verify changes persist in the JSON file
5. **Export**: Download a single `.docx` → verify it opens in Word
6. **Export All**: Download zip → verify all 7 files present
7. **Import**: Upload a `.docx` → verify it appears in the dashboard and JSON is updated
8. **Nav**: Verify "Documents" link appears in admin nav and highlights correctly

### Automated Tests

> No existing tests cover document management. Since this is a file-based feature (no DB), the most pragmatic approach is manual verification for the initial implementation. Unit tests can be added later for the JSON parsing/validation logic if needed.
