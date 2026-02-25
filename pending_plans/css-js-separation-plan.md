# Plan: Separating Inline CSS and JavaScript from HTML Files

## Project Overview
**Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan**

---

## Current State Analysis

### Statistics
- **59 HTML template files** total in `templates/` directory
- **18 files** contain inline CSS in `<style>` tags
- **23 files** contain inline JavaScript in `<script>` tags
- Existing structure: `static/css/` and `static/js/` directories already present

### Files with Inline CSS
1. `templates/auth/register.html`
2. `templates/auth/login.html`
3. `templates/admin/attractions.html`
4. `templates/admin/add_event.html`
5. `templates/admin/dashboard.html`
6. `templates/base.html` (footer marquee animation)
7. `templates/admin/documents_edit.html`
8. `templates/admin/documents_editor.html`
9. `templates/admin/documents_view.html`
10. `templates/pagez/barangays.html`
11. `templates/pagez/barangay_profile.html`
12. `templates/admin/edit_attraction.html`
13. `templates/admin/edit_event.html`
14. `templates/pagez/detail.html`
15. `templates/admin/events.html`
16. `templates/pagez/events.html`
17. `templates/pagez/gallery.html`
18. `templates/pagez/search_results.html`

### Files with Inline JavaScript
1. `templates/auth/login.html`
2. `templates/auth/register.html` (2 instances)
3. `templates/admin/heritage_list.html`
4. `templates/admin/events.html`
5. `templates/admin/edit_attraction.html`
6. `templates/pagez/map.html`
7. `templates/admin/dashboard.html`
8. `templates/pagez/index.html`
9. `templates/admin/attractions.html`
10. `templates/admin/documents_editor.html`
11. `templates/admin/documents_edit.html`
12. `templates/pagez/heritage_detail.html`
13. `templates/admin/documents_dashboard.html`
14. `templates/pagez/gallery.html` (2 instances)
15. `templates/base.html` (3 instances - mobile nav, flash messages, service worker)
16. `templates/pagez/barangay_profile.html`
17. `templates/pagez/events.html`
18. `templates/pagez/detail.html`
19. `templates/pagez/barangays.html`

---

## Target Directory Structure

```
static/
├── css/
│   ├── components/              # Reusable component styles
│   │   ├── mobile-nav.css       # Mobile navigation styles from base.html
│   │   ├── footer.css           # Footer styles including marquee animation
│   │   ├── forms.css            # Form styles for login, register
│   │   ├── cards.css            # Card layouts and bento grids
│   │   ├── sidebar.css          # Sidebar components
│   │   └── modals.css           # Modal and dialog styles
│   ├── pages/                   # Page-specific styles
│   │   ├── home.css             # index.html (hero, bento, experiences)
│   │   ├── map.css              # map.html (sidebar, map controls)
│   │   ├── barangays.css        # barangays.html listing page
│   │   ├── barangay-profile.css # barangay_profile.html detailed view
│   │   ├── events.css           # events.html public events page
│   │   ├── gallery.css          # gallery.html photo gallery
│   │   ├── search.css           # search_results.html
│   │   ├── detail.css           # attraction detail page
│   │   ├── heritage-detail.css  # heritage_detail.html
│   │   ├── heritage-index.css   # heritage_index.html
│   │   ├── heritage-list.css    # heritage_list.html
│   │   └── routes.css           # routes.html
│   └── admin/                   # Admin dashboard styles
│       ├── dashboard.css        # admin dashboard
│       ├── attractions.css      # attractions management
│       ├── events.css           # events management
│       ├── documents.css        # documents editor/viewer
│       ├── edit-attraction.css  # edit attraction form
│       └── edit-event.css       # edit event form
│
└── js/
    ├── components/              # Reusable JavaScript components
    │   ├── mobile-nav.js        # Mobile menu toggle functionality
    │   ├── flash-messages.js    # SweetAlert2 flash message handling
    │   ├── service-worker-registration.js  # PWA service worker registration
    │   ├── delete-confirm.js    # Global delete confirmation dialog
    │   ├── form-validation.js   # Common form validation utilities
    │   └── image-upload.js      # Image upload preview functionality
    ├── pages/                   # Page-specific JavaScript
    │   ├── home.js              # index.html (AOS, scroll reveals, newsletter)
    │   ├── map.js               # map.html (Mapbox integration - already exists)
    │   ├── barangays.js         # barangays.html interactions
    │   ├── barangay-profile.js  # barangay_profile.html interactions
    │   ├── events.js            # events.html calendar/filter logic
    │   ├── gallery.js           # gallery.html lightbox/filter
    │   ├── search.js            # search_results.html filtering
    │   ├── detail.js            # detail.html interactions
    │   └── heritage-*.js        # Heritage page interactions
    └── admin/                   # Admin dashboard JavaScript
        ├── dashboard.js         # Dashboard charts/interactions
        ├── attractions.js       # Attractions management
        ├── events.js            # Events management
        └── documents.js         # Documents editor functionality
```

---

## Files to Create

### CSS Files (24 new files)

#### Component Styles (`static/css/components/`)
1. `mobile-nav.css` - Mobile navigation menu styles
2. `footer.css` - Footer styles with marquee animation
3. `forms.css` - Login/register form styles
4. `cards.css` - Card layouts, bento grids, spotlight cards
5. `sidebar.css` - Sidebar components for map and admin
6. `modals.css` - Modal dialogs and overlays

#### Page Styles (`static/css/pages/`)
7. `home.css` - Homepage (index.html) hero, bento, experiences sections
8. `map.css` - Map page sidebar, controls, floating cards
9. `barangays.css` - Barangays listing page
10. `barangay-profile.css` - Individual barangay profile page
11. `events.css` - Public events page
12. `gallery.css` - Photo gallery page
13. `search.css` - Search results page
14. `detail.css` - Attraction detail page
15. `heritage-detail.css` - Heritage detail page
16. `heritage-index.css` - Heritage index page
17. `heritage-list.css` - Heritage list page
18. `routes.css` - Routes page

#### Admin Styles (`static/css/admin/`)
19. `dashboard.css` - Admin dashboard
20. `attractions.css` - Attractions management
21. `events.css` - Events management
22. `documents.css` - Documents editor/viewer
23. `edit-attraction.css` - Edit attraction form
24. `edit-event.css` - Edit event form

#### Auth Styles (`static/css/auth/`)
25. `login.css` - Login page styles
26. `register.css` - Registration page styles

---

### JavaScript Files (20 new files)

#### Component Scripts (`static/js/components/`)
1. `mobile-nav.js` - Mobile menu toggle
2. `flash-messages.js` - SweetAlert2 flash message handler
3. `service-worker-registration.js` - PWA service worker
4. `delete-confirm.js` - Delete confirmation dialog
5. `form-validation.js` - Form validation utilities
6. `image-upload.js` - Image upload preview

#### Page Scripts (`static/js/pages/`)
7. `home.js` - Homepage (AOS initialization, scroll reveals, newsletter)
8. `barangays.js` - Barangays page interactions
9. `barangay-profile.js` - Barangay profile interactions
10. `events.js` - Events page calendar/filter logic
11. `gallery.js` - Gallery lightbox and filtering
12. `search.js` - Search results filtering
13. `detail.js` - Detail page interactions
14. `heritage-detail.js` - Heritage detail interactions
15. `heritage-index.js` - Heritage index interactions
16. `heritage-list.js` - Heritage list interactions
17. `routes.js` - Routes page interactions

#### Admin Scripts (`static/js/admin/`)
18. `dashboard.js` - Dashboard charts and interactions
19. `attractions.js` - Attractions management
20. `events.js` - Events management
21. `documents.js` - Documents editor functionality

---

## HTML Files to Update (59 files)

All template files will be updated to:
1. Remove `<style>...</style>` blocks
2. Remove inline `<script>...</script>` blocks (except CDN/vendor scripts)
3. Add `<link>` tags referencing new CSS files in `{% block head %}`
4. Add `<script src="...">` tags referencing new JS files in `{% block scripts %}`

### By Category

#### Base Template (1 file)
- `templates/base.html`

#### Authentication (2 files)
- `templates/auth/login.html`
- `templates/auth/register.html`

#### Admin Templates (15 files)
- `templates/admin/dashboard.html`
- `templates/admin/attractions.html`
- `templates/admin/add_attraction.html`
- `templates/admin/edit_attraction.html`
- `templates/admin/events.html`
- `templates/admin/add_event.html`
- `templates/admin/edit_event.html`
- `templates/admin/heritage_dashboard.html`
- `templates/admin/heritage_list.html`
- `templates/admin/heritage_form.html`
- `templates/admin/documents_dashboard.html`
- `templates/admin/documents_list.html`
- `templates/admin/documents_editor.html`
- `templates/admin/documents_edit.html`
- `templates/admin/documents_view.html`

#### Barangay Templates (10 files)
- `templates/barangay/dashboard.html`
- `templates/barangay/add_attraction.html`
- `templates/barangay/edit_attraction.html`
- `templates/barangay/attractions.html`
- `templates/barangay/add_event.html`
- `templates/barangay/edit_event.html`
- `templates/barangay/events.html`
- `templates/barangay/add_gallery.html`
- `templates/barangay/edit_gallery.html`
- `templates/barangay/gallery.html`
- `templates/barangay/profile.html`

#### Public Pages (14 files)
- `templates/pagez/index.html`
- `templates/pagez/map.html`
- `templates/pagez/barangays.html`
- `templates/pagez/barangay_profile.html`
- `templates/pagez/detail.html`
- `templates/pagez/events.html`
- `templates/pagez/gallery.html`
- `templates/pagez/search_results.html`
- `templates/pagez/routes.html`
- `templates/pagez/heritage_index.html`
- `templates/pagez/heritage_list.html`
- `templates/pagez/heritage_detail.html`

#### User Templates (5 files)
- `templates/user/dashboard.html`
- `templates/user/profile.html`
- `templates/user/favorites.html`
- `templates/user/my_events.html`
- `templates/user/contributions.html`

#### Error Templates (8 files)
- `templates/errors/400.html`
- `templates/errors/401.html`
- `templates/errors/403.html`
- `templates/errors/404.html`
- `templates/errors/408.html`
- `templates/errors/429.html`
- `templates/errors/451.html`
- `templates/errors/base_error.html`

#### Includes (4 files)
- `templates/includes/admin_nav.html`
- `templates/includes/barangay_nav.html`
- `templates/includes/guest_nav.html`
- `templates/includes/user_nav.html`

---

## Implementation Steps

### Phase 1: Foundation (Priority: High)
1. ✅ Create directory structure (`static/css/components/`, `static/css/pages/`, `static/css/admin/`, `static/js/components/`, `static/js/pages/`, `static/js/admin/`)
2. Extract base.html inline styles and scripts
3. Create component CSS files (mobile-nav.css, footer.css)
4. Create component JS files (mobile-nav.js, flash-messages.js, service-worker-registration.js, delete-confirm.js)
5. Update base.html to reference external files

### Phase 2: Public Pages (Priority: High)
6. Extract index.html (homepage) styles and scripts
7. Extract map.html styles and scripts
8. Extract barangays.html, barangay_profile.html
9. Extract events.html, gallery.html, search_results.html, detail.html
10. Update all public page templates

### Phase 3: Authentication (Priority: Medium)
11. Extract login.html styles and scripts
12. Extract register.html styles and scripts
13. Update auth templates

### Phase 4: Admin Dashboard (Priority: Medium)
14. Extract admin dashboard styles and scripts
15. Extract attractions management pages
16. Extract events management pages
17. Extract documents editor pages
18. Update all admin templates

### Phase 5: Barangay & User Portals (Priority: Low)
19. Extract barangay portal pages
20. Extract user portal pages
21. Update all barangay and user templates

### Phase 6: Verification & Optimization (Priority: High)
22. Update package.json build scripts to include new CSS/JS files
23. Test all pages for proper styling and functionality
24. Optimize and minify new CSS/JS files
25. Verify caching headers and CDN configuration

---

## Code Extraction Examples

### Example: Extracting from base.html

#### Current (Inline CSS in base.html lines 331-355):
```html
<style>
    @keyframes marquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .animate-marquee {
        display: flex;
        width: max-content;
        animation: marquee 60s linear infinite;
    }
    .pause {
        animation-play-state: paused;
    }
</style>
```

#### Target (static/css/components/footer.css):
```css
/* ========================================
   Footer Component Styles
   ======================================== */

@keyframes marquee {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-50%);
    }
}

.animate-marquee {
    display: flex;
    width: max-content;
    animation: marquee 60s linear infinite;
}

.pause {
    animation-play-state: paused;
}
```

#### Updated base.html reference:
```html
{% block head %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/components/footer.css') }}">
{% endblock %}
```

---

#### Current (Inline JS in base.html lines 143-151):
```html
<script>
    document.addEventListener('DOMContentLoaded', function () {
        const btn = document.getElementById('mobile-menu-btn');
        const menu = document.getElementById('mobile-menu');

        if (btn && menu) {
            btn.addEventListener('click', () => {
                menu.classList.toggle('hidden');
            });
        }
    });
</script>
```

#### Target (static/js/components/mobile-nav.js):
```javascript
/**
 * Mobile Navigation Toggle
 * Handles opening/closing of mobile menu
 */
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const btn = document.getElementById('mobile-menu-btn');
        const menu = document.getElementById('mobile-menu');

        if (btn && menu) {
            btn.addEventListener('click', function() {
                menu.classList.toggle('hidden');
            });
        }
    });
})();
```

#### Updated base.html reference:
```html
{% block scripts %}
<script src="{{ url_for('static', filename='js/components/mobile-nav.js') }}" defer></script>
{% endblock %}
```

---

## Build Script Updates

### Current package.json:
```json
{
  "scripts": {
    "build:css": "npx tailwindcss -i ./static/css/input.css -o ./static/css/main.css --minify",
    "build:js": "terser static/js/*.js --compress --mangle --output static/js/main.min.js",
    "build": "npm run build:css && npm run build:js"
  }
}
```

### Updated package.json:
```json
{
  "scripts": {
    "build:css": "npx tailwindcss -i ./static/css/input.css -o ./static/css/main.css --minify && npx tailwindcss -i ./static/css/components/*.css -o ./static/css/components.min.css --minify && npx tailwindcss -i ./static/css/pages/*.css -o ./static/css/pages.min.css --minify",
    "build:js": "terser static/js/components/*.js --compress --mangle --output static/js/components.min.js && terser static/js/pages/*.js --compress --mangle --output static/js/pages.min.js",
    "build:css:components": "npx tailwindcss -i ./static/css/components/footer.css -o ./static/css/components/footer.min.css --minify",
    "build:js:components": "terser static/js/components/mobile-nav.js --compress --mangle --output static/js/components/mobile-nav.min.js",
    "build": "npm run build:css && npm run build:js",
    "watch:css": "npx tailwindcss -i ./static/css/input.css -o ./static/css/main.css --watch",
    "watch:js": "chokidar \"static/js/**/*.js\" -c \"npm run build:js\""
  }
}
```

---

## Benefits

### Maintainability
- Clear separation of concerns
- Easier to locate and update specific styles/functionality
- Reduced HTML file sizes

### Performance
- Browser caching of CSS/JS files
- Parallel downloading of resources
- Potential for code splitting and lazy loading

### Collaboration
- Frontend developers can work on CSS/JS independently
- Backend developers can focus on templates
- Better version control diffs

### Best Practices
- Follows modern web development standards
- Enables use of CSS preprocessors if needed
- Facilitates automated testing of JavaScript

---

## Testing Checklist

After implementation, verify:

- [ ] Mobile navigation toggle works on all pages
- [ ] Footer marquee animation plays correctly
- [ ] Flash messages display with SweetAlert2
- [ ] Service worker registers successfully
- [ ] Delete confirmations show proper dialogs
- [ ] Homepage scroll animations function
- [ ] Map interactions work (pan, zoom, markers)
- [ ] Form validations trigger correctly
- [ ] Image uploads preview properly
- [ ] All pages render without console errors
- [ ] CSS loads correctly in production build
- [ ] JavaScript minification doesn't break functionality

---

## Timeline Estimate

| Phase | Estimated Time | Files Affected |
|-------|---------------|----------------|
| Phase 1: Foundation | 2-3 hours | 5 files |
| Phase 2: Public Pages | 4-5 hours | 14 files |
| Phase 3: Authentication | 1-2 hours | 2 files |
| Phase 4: Admin Dashboard | 4-5 hours | 15 files |
| Phase 5: Barangay & User | 3-4 hours | 15 files |
| Phase 6: Verification | 2-3 hours | All files |
| **Total** | **16-22 hours** | **59 files** |

---

## Notes

1. **Preserve existing functionality**: All extracted code must maintain current behavior
2. **Add JSDoc comments**: Document JavaScript functions for maintainability
3. **Use CSS custom properties**: Where applicable, use CSS variables for theming
4. **Maintain Tailwind compatibility**: New CSS should complement existing Tailwind classes
5. **Consider RTL support**: Future-proof for right-to-left languages if needed
6. **Accessibility**: Ensure extracted JS maintains ARIA attributes and keyboard navigation

---

**Document Created**: February 18, 2026  
**Status**: Pending Implementation  
**Priority**: High (Foundation phase first)
