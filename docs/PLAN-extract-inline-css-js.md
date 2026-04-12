# PLAN: Extract Inline CSS & JS from Templates

## Context
76 HTML templates currently contain inline CSS and JavaScript. Goal: **zero inline code** — all styles and scripts externalized to static files while preserving functionality.

---

## Current State Analysis

### Inline CSS
| Category | Files | Severity |
|----------|-------|----------|
| `<style>` blocks | 2 files | High |
| Static `style=""` attributes | 12 files | Medium |
| Dynamic `style=""` (data-driven) | 7 files | Low (requires data-passing) |

### Inline JavaScript
| Category | Files | Severity |
|----------|-------|----------|
| `<script>` code blocks | 6 files (excluding acceptable patterns) | High |
| Inline event handlers (`onclick`, etc.) | 14 files | Medium |
| Data-passing scripts (acceptable) | 3 files | None (keep as-is) |

---

## Task Breakdown

### Phase 1: Extract `<style>` Blocks
**Goal**: Move embedded CSS to static files

| # | File | Action | Target CSS File |
|---|------|--------|-----------------|
| 1 | `auth/pending_approval.html` | Extract 37-line keyframe animations | `static/css/animations.css` |
| 2 | `admin/add_attraction.html` | Extract 20-line utility classes | `static/css/admin-forms.css` |

**Subtasks:**
- [ ] Create `static/css/animations.css` with `.animate-pulse-ring`, `.animate-bounce-subtle`, `@keyframes`
- [ ] Create `static/css/admin-forms.css` with `.glass-panel`, `.form-input`, `.heritage-gradient`
- [ ] Add `<link>` tags to respective HTML files
- [ ] Remove `<style>` blocks
- [ ] Test visually

---

### Phase 2: Extract Inline JavaScript Code Blocks
**Goal**: Move all executable JS to external files

| # | File | Action | Target JS File |
|---|------|--------|----------------|
| 3 | `auth/reset_password.html` | Extract password validation (~35 lines) | `static/js/pages/reset_password.js` |
| 4 | `includes/admin_nav.html` | Extract dropdown toggle (~25 lines) | `static/js/components/admin-nav.js` |
| 5 | `admin/attractions.html` | Remove duplicate `confirmDelete` (use existing `delete-confirm.js`) | N/A (delete inline) |
| 6 | `admin/dashboard.html` | Extract Chart.js logic (~55 lines) | `static/js/pages/admin-dashboard.js` |
| 7 | `pagez/establishment_detail.html` | Extract Mapbox init (~25 lines) | `static/js/pages/establishment-map.js` |
| 8 | `pagez/heritage_detail.html` | Extract Leaflet mini-map (~25 lines) | `static/js/pages/heritage-map.js` |

**Data-Passing Pattern (Refactor to `data-*` attributes):**
| # | File | Current Pattern | New Pattern |
|---|------|-----------------|-------------|
| 9 | `admin/dashboard.html` | `{{ engagement_data.dates \| tojson }}` in JS | `<div id="engagement-data" data-dates="..." data-counts="...">` |
| 10 | `pagez/establishment_detail.html` | `{{ establishment.longitude }}` in JS | `<div id="map-container" data-lng="..." data-lat="...">` |
| 11 | `pagez/heritage_detail.html` | `{{ item.lat }}` in JS | `<div id="mini-map" data-lat="..." data-lng="...">` |

**Subtasks:**
- [ ] Create each target JS file
- [ ] Refactor functions to read from `data-*` attributes instead of Jinja2 variables
- [ ] Add `<script src="...">` tags to HTML
- [ ] Remove inline `<script>` blocks
- [ ] Test functionality

---

### Phase 3: Replace Inline Event Handlers
**Goal**: Replace `onclick="..."`, `onsubmit="..."`, `onchange="..."` with `addEventListener` in JS

| # | Handler Pattern | Files Affected | Strategy |
|---|-----------------|----------------|----------|
| 12 | `onclick="confirmDelete(...)"` | 6 files | Add `data-delete-url`, `data-delete-message` attributes, bind in JS |
| 13 | `onclick="toggleAdminMoreDropdown()"` | 1 file | Already in `admin_nav.html`, handled in Phase 2 |
| 14 | `onsubmit="confirm('...')"` | 5 files | Add `data-confirm-message` attribute, bind in JS via delegated listener |
| 15 | `onchange="this.form.submit()"` | 1 file | Add `.auto-submit-form` class, bind in JS |
| 16 | `onclick="drawRoute(...)"`, `clearRoutes()`, `changeMapStyle(...)` | 1 file (`map.html`) | Add `data-*` attributes, bind in `map.js` |
| 17 | `onclick="addToCalendar(...)"` | 1 file (`events.html`) | Add event data attributes, bind in JS |
| 18 | `onclick="handleItemClick(...)"`, `closeLightbox()` | 1 file (`gallery.html`) | Already partially external, verify |
| 19 | `onclick="classList.toggle(...)"` | 2 files | Add delegated listeners in JS |
| 20 | `onclick="window.scrollTo(...)"` | 1 file (`base.html`) | Bind in `base.js` or common utility |

**Subtasks:**
- [ ] Create `static/js/components/event-handlers.js` for common patterns
- [ ] Add `data-*` attributes to replace inline function calls
- [ ] Write delegated event listeners (use `document.addEventListener('click', ...)`)
- [ ] Remove inline handler attributes
- [ ] Test all interactions

---

### Phase 4: Refactor Static Inline Styles
**Goal**: Replace `style=""` attributes with CSS classes

| # | Pattern | Files | Strategy |
|---|---------|-------|----------|
| 21 | `style="animation-delay: -5s;"` | 5 auth files | Create `.animation-delay-blob` utility class |
| 22 | `style="animation-delay: {{ loop.index0 * N }}ms"` | 2 files | Create CSS custom property `--stagger-delay`, set via `style` (unavoidable) OR generate classes `.stagger-0` to `.stagger-20` |
| 23 | `style="transition-delay: 200ms"` | 1 file | Same as #22 |
| 24 | `style="display: none;"` | 1 file | Replace with Tailwind `hidden` class |
| 25 | `style="grid-column: span 12; width: 100%;"` | 1 file | Replace with Tailwind `col-span-12 w-full` |
| 26 | `style="border-radius: 2.5rem;"` | 1 file | Replace with Tailwind `rounded-[2.5rem]` |
| 27 | `style="margin-top: 2rem;"` | 1 file | Replace with Tailwind `mt-8` |
| 28 | `style="background-image: radial-gradient(...)"` | 1 file (`gallery.html`) | Create `.bg-dot-pattern` class in CSS |
| 29 | `style="color: #064e3b !important"` (14 instances) | 1 file (`map.html`) | Create semantic color classes (e.g., `.text-emerald-900`) |

**Acceptable Inline Styles (Keep):**
- `style="background-image: url(...)"` — data-driven URLs (7 files, inherently dynamic)
- Map marker HTML in JS string — Leaflet `divIcon` content

**Subtasks:**
- [ ] Create utility CSS classes
- [ ] Replace static `style=""` with Tailwind/classes
- [ ] Test visual parity

---

### Phase 5: Cleanup & Verification
**Goal**: Ensure zero regressions

| # | Task | Details |
|---|------|---------|
| 30 | Grep all HTML files for `<style>` | Should return 0 results (except acceptable patterns) |
| 31 | Grep all HTML files for inline `<script>` with code | Should return 0 results (except data-passing) |
| 32 | Grep all HTML files for `onclick=`, `onsubmit=`, `onchange=` | Should return 0 results |
| 33 | Run linting | `npm run lint` or project equivalent |
| 34 | Manual testing | Visit each affected page, verify functionality |
| 35 | Update template includes | Ensure new CSS/JS files are linked in `base.html` or relevant includes |

---

## Agent Assignments

| Phase | Agent Type | Priority |
|-------|-----------|----------|
| Phase 1 | CSS extraction | P1 |
| Phase 2 | JS extraction | P1 |
| Phase 3 | Event handler refactoring | P2 |
| Phase 4 | Inline style refactoring | P2 |
| Phase 5 | Verification & testing | P3 |

---

## File Structure (New Files)

```
static/
├── css/
│   ├── animations.css          (Phase 1)
│   └── admin-forms.css         (Phase 1)
└── js/
    ├── components/
    │   ├── admin-nav.js        (Phase 2)
    │   └── event-handlers.js   (Phase 3)
    └── pages/
        ├── reset_password.js   (Phase 2)
        ├── admin-dashboard.js  (Phase 2)
        ├── establishment-map.js (Phase 2)
        └── heritage-map.js     (Phase 2)
```

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Jinja2 template variables in JS lose context | Use `data-*` attributes to pass data from server to JS |
| Event delegation breaks existing behavior | Test each handler thoroughly; use specific selectors |
| CSS class conflicts with Tailwind | Prefix custom classes (e.g., `.custom-*`) or use Tailwind config |
| Browser caching breaks after changes | Append query strings to new CSS/JS files during testing |

---

## Verification Checklist

- [ ] Zero `<style>` blocks in HTML (except acceptable)
- [ ] Zero inline `<script>` code blocks (except data-passing)
- [ ] Zero `onclick`, `onsubmit`, `onchange` attributes
- [ ] All new CSS/JS files properly linked
- [ ] All pages render correctly
- [ ] All interactions functional (forms, modals, maps, charts)
- [ ] No console errors
- [ ] Linting passes

---

## Acceptable Patterns (Do NOT Extract)

1. `<script type="application/json">` — data blocks (e.g., flash messages in `base.html`)
2. `tailwind.config` — required inline for CDN runtime
3. `window.MAPBOX_TOKEN` — token passing (or refactor to `data-*`)
4. `style="background-image: url({{ dynamic_url }})"` — data-driven backgrounds
5. Map marker HTML strings in JS — Leaflet `divIcon` content
