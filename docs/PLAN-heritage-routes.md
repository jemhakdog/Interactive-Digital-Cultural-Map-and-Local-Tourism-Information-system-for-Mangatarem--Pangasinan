# Heritage Routes Implementation Plan

> Admin-only CRUD routes for the 5 new heritage tables, with auto-approval.

---

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Access** | Admin-only | Forms are official LGU tourism office documents |
| **Approval** | Auto-approved on create | Admin creates = trusted data, no review needed |
| **Architecture** | Unified type-based routes | Avoids 5x code duplication |
| **Barangay routes** | ❌ Not needed | Tourism office staff enters this data |

---

## Route Architecture

### Type Registry → `utils/heritage_registry.py` [NEW]

Maps URL slugs to models. Single source of truth for all heritage route handlers.

```python
HERITAGE_TYPES = {
    "natural":     {"model": NaturalHeritage,     "label": "Natural Heritage",       "form": "01A", "has_coords": True},
    "intangible":  {"model": IntangibleHeritage,   "label": "Intangible Heritage",    "form": "04A", "has_coords": False},
    "personality": {"model": PersonalityProfile,   "label": "Significant Personality", "form": "05",  "has_coords": False},
    "institution": {"model": CulturalInstitution,  "label": "Cultural Institution",   "form": "06",  "has_coords": True},
    "program":     {"model": LGUCultureProgram,    "label": "LGU Culture Program",    "form": "07",  "has_coords": False},
}
```

---

## Proposed Routes

### Admin Routes → `routes/admin/heritage.py` [NEW]

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/admin/heritage` | GET | `admin_heritage_dashboard` | Overview with counts per type |
| `/admin/heritage/<type>` | GET | `admin_heritage_list` | List all entries of a type |
| `/admin/heritage/<type>/add` | GET/POST | `admin_heritage_add` | Create new entry (auto-approved) |
| `/admin/heritage/<type>/edit/<id>` | GET/POST | `admin_heritage_edit` | Edit existing entry |
| `/admin/heritage/<type>/delete/<id>` | POST | `admin_heritage_delete` | Delete entry |

### API Routes → `routes/api.py` [MODIFY]

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/api/heritage/<type>` | GET | `api_heritage_list` | JSON list with pagination |
| `/api/heritage/<type>/<id>` | GET | `api_heritage_detail` | Single item detail |

### Public Routes → `routes/public.py` [MODIFY]

| Route | Method | Function | Description |
|-------|--------|----------|-------------|
| `/heritage` | GET | `heritage_index` | Heritage catalog landing page |
| `/heritage/<type>` | GET | `heritage_type_list` | Browse by type |
| `/heritage/<type>/<id>` | GET | `heritage_detail` | Detail page for single entry |

---

## Files To Create/Modify

### New Files (4)

| File | Purpose |
|------|---------|
| `utils/heritage_registry.py` | Type config + model resolver |
| `routes/admin/heritage.py` | Admin CRUD routes |
| `templates/admin/heritage_dashboard.html` | Dashboard with counts |
| `templates/admin/heritage_form.html` | Dynamic add/edit form |
| `templates/admin/heritage_list.html` | Type-specific list view |
| `templates/pagez/heritage_index.html` | Public heritage landing |
| `templates/pagez/heritage_detail.html` | Public detail view |

### Modified Files (4)

| File | Change |
|------|--------|
| `routes/admin/__init__.py` | Add `heritage` import |
| `routes/api.py` | Add heritage API endpoints |
| `routes/public.py` | Add heritage public pages |
| `templates/includes/admin_nav.html` | Add Heritage menu link |

---

## Implementation Phases

### Phase 1: Backend Foundation
1. Create `utils/heritage_registry.py`
2. Create `routes/admin/heritage.py` (all 5 CRUD routes)
3. Update `routes/admin/__init__.py`

### Phase 2: Admin Templates
4. Create `templates/admin/heritage_dashboard.html`
5. Create `templates/admin/heritage_list.html`
6. Create `templates/admin/heritage_form.html`
7. Update `templates/includes/admin_nav.html`

### Phase 3: API + Public Pages
8. Add heritage endpoints to `routes/api.py`
9. Add heritage public routes to `routes/public.py`
10. Create `templates/pagez/heritage_index.html`
11. Create `templates/pagez/heritage_detail.html`

---

## Verification

- [ ] Admin can access heritage dashboard
- [ ] Admin can add entries for all 5 types
- [ ] New entries are auto-approved (status='approved')
- [ ] Admin can edit/delete entries
- [ ] API returns paginated JSON
- [ ] Public pages display approved heritage
- [ ] Non-admin users get "Access denied"
