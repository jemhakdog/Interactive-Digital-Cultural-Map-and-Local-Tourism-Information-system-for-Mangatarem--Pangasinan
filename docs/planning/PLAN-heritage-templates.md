# Heritage Templates & Migration Plan

Backend routes for heritage data are complete (12 endpoints). This plan covers the remaining frontend templates and SQL migration fix.

---

## Scope

| Deliverable | Count | Description |
|---|---|---|
| **Admin Templates** | 3 | Dashboard overview, type list table, add/edit form |
| **Public Templates** | 3 | Heritage catalog, type browse list, item detail |
| **Admin Nav** | 1 | Add Heritage link to `admin_nav.html` |
| **SQL Fix** | 1 | Quote `reference_sources` (reserved word) in migration |

---

## Design Constraints (from existing codebase)

| Element | Pattern |
|---|---|
| Base Layout | `{% extends 'base.html' %}` with `{% block content %}` |
| Admin Style | `.glass-card` glassmorphism + `.heritage-gradient` emerald header + Tailwind utilities |
| Admin Tables | `<table>` inside `.glass-card` with status badges, search input, edit/delete actions |
| Admin Forms | Form fields with `rounded-md border-gray-300` inputs, green submit buttons |
| Public Style | Editorial hero (80vh) + aurora blur + `font-cultural` (Playfair Display) + `font-body-premium` (Plus Jakarta Sans) |
| Public Cards | White cards with `rounded-[2.5rem]`, shadow, emerald accent borders |
| Mini-Map | Leaflet with CartoDB dark tiles, custom emerald pin, `rounded-2rem`, 300px height |
| Colors | Emerald primary (`#065f46`→`#064e3b`), amber accents, no purple/violet |

---

## Proposed Changes

### Component 1: Admin Templates

#### [NEW] `templates/admin/heritage_dashboard.html`

Admin overview page showing all 5 heritage types as stat cards in a grid. Each card shows:
- Heritage type label + form number (e.g., "Form 01A")
- Total / Approved / Pending counts
- Link to type-specific list page
- Uses existing `.glass-card` + `.heritage-gradient` header pattern from `dashboard.html`

**Template variables** (from `routes/admin/heritage.py → admin_heritage_dashboard`):
- `type_stats`: list of dicts with `slug`, `label`, `label_plural`, `form`, `total`, `approved`, `pending`

---

#### [NEW] `templates/admin/heritage_list.html`

Table view listing all entries for one heritage type. Matches `attractions.html` structure:
- Heritage-gradient header with breadcrumb (Back to Heritage Dashboard)
- Quick stats row (Total, Approved, Pending counts)
- "Add New" button linking to add form
- Table with columns: Name, Status, Created, Actions (Edit/Delete)
- Client-side search filter (JS `input` event on name column)
- `confirmDelete()` JS function for delete confirmation

**Template variables** (from `admin_heritage_list`):
- `items`: list of model instances
- `heritage_type`: slug string
- `config`: dict with `label`, `label_plural`, `form`, `fields`, `name_field`

---

#### [NEW] `templates/admin/heritage_form.html`

Dynamic form that renders fields based on `config["fields"]` from the registry. Works for both add and edit:
- Heritage-gradient header with "Add New {type}" or "Edit {name}"
- Loops through `config["fields"]` to render appropriate input types:
  - `text` → `<input type="text">`
  - `textarea` → `<textarea>`
  - `number` → `<input type="number">`
  - `date` → `<input type="date">`
  - `select` → `<select>` with choices from `config["{field}_choices"]`
  - `json` → `<textarea>` with JSON placeholder text
- Pre-fills values when `is_edit=True` using `item.{field_name}`
- Submit button: "Create {type}" or "Update {type}"
- Cancel link back to list page

**Template variables** (from `admin_heritage_add` / `admin_heritage_edit`):
- `heritage_type`, `config`, `item` (None for add), `is_edit` (bool)

---

### Component 2: Admin Navigation

#### [MODIFY] `templates/includes/admin_nav.html`

Add a Heritage nav link between Events and View Site:
- SVG icon: building/museum icon (24×24)
- Label: "Heritage"
- Active state: highlights when `request.endpoint` starts with `admin.admin_heritage`
- URL: `{{ url_for('admin.admin_heritage_dashboard') }}`

---

### Component 3: Public Templates

#### [NEW] `templates/pagez/heritage_index.html`

Heritage catalog landing page. Shows 5 type cards in a responsive grid:
- Each card shows: type label, form code, approved count, representative photo (if available)
- Cards link to `/heritage/<type>` for browsing
- Uses editorial style matching `index.html` — hero section with emerald gradient, white content area below
- No mini-map (this is an overview page)

**Template variables** (from `routes/public.py → heritage_index`):
- `type_stats`: list with `slug`, `label`, `label_plural`, `form`, `has_coords`, `count`, `photo`

---

#### [NEW] `templates/pagez/heritage_list.html`

Paginated browse page for one heritage type:
- Header with type label and count
- Search input bar
- Card grid (3 columns desktop, 1 mobile) — each card shows item name, creation date, photo thumbnail
- Pagination controls (Previous / Next) using `pagination` object
- Cards link to `/heritage/<type>/<id>`

**Template variables** (from `heritage_type_list`):
- `items`, `pagination`, `heritage_type`, `config`, `search_term`

---

#### [NEW] `templates/pagez/heritage_detail.html`

Full detail page for a single heritage item. Matches `detail.html` editorial style:
- **Hero section**: Photo or emerald gradient fallback, item name, type badge
- **Main content (2/3)**: Structured card layout showing ALL fields from `config["fields"]`:
  - Groups fields by section (identity, description, significance, documentation)
  - Each field as a labeled row: `label: value`
  - JSON fields rendered as formatted lists
  - Empty fields hidden (only show populated data)
- **Sidebar (1/3)**:
  - Mini-map with Leaflet (only for types with `has_coords=True`: natural, institution)
  - Coordinates display + Google Maps navigation link
  - Metadata: mapper name, date profiled, form number
  - Cultural Protocol box (amber)

**Template variables** (from `heritage_detail`):
- `item`, `heritage_type`, `config`, `display_name`

---

### Component 4: SQL Migration Fix

#### [MODIFY] `migrations/supabase_tourism_forms_schema.sql`

Fix the `reference_sources` reserved word issue. In PostgreSQL, `references` is a keyword. The column name `reference_sources` is close enough to trigger parsing issues in some contexts.

**Fix**: Quote `reference_sources` as `"reference_sources"` in:
- Line 49 (ALTER TABLE attraction)
- Line 76 (natural_heritage CREATE)
- Line 120 (intangible_heritage)
- Line 156 (personality_profile)
- Line 199 (cultural_institution)
- Line 246 (lgu_culture_program)
- Lines 368 (ROLLBACK script)

Also add RLS policies for Flask app's service-role connection (INSERT/UPDATE/DELETE for authenticated app users).

---

## File Summary

| # | File | Action | Priority |
|---|---|---|---|
| 1 | `templates/admin/heritage_dashboard.html` | NEW | P1 |
| 2 | `templates/admin/heritage_list.html` | NEW | P1 |
| 3 | `templates/admin/heritage_form.html` | NEW | P1 |
| 4 | `templates/includes/admin_nav.html` | MODIFY | P1 |
| 5 | `templates/pagez/heritage_index.html` | NEW | P2 |
| 6 | `templates/pagez/heritage_list.html` | NEW | P2 |
| 7 | `templates/pagez/heritage_detail.html` | NEW | P2 |
| 8 | `migrations/supabase_tourism_forms_schema.sql` | MODIFY | P1 |

---

## Verification Plan

### Automated
- `python -c "from app import app"` — confirm app loads with new templates registered
- Visit `/admin/heritage` — dashboard renders with 5 type cards
- Visit `/admin/heritage/natural/add` — form renders with all fields
- Visit `/heritage` — public catalog shows 5 types
- API: `GET /api/heritage/types` returns JSON
- SQL: Run fixed migration in Supabase SQL Editor — no syntax errors

### Manual
- Verify admin nav shows "Heritage" link and highlights correctly
- Verify form submission creates entry (via admin add page)
- Verify public detail page renders mini-map for `natural` type
- Confirm `reference_sources` column is created without SQL errors
