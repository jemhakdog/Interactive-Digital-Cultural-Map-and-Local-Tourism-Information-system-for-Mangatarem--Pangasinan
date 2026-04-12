# CSRF Token Implementation Plan

## 📋 Current Status: **NO CSRF PROTECTION** ⚠️

The application currently has **zero CSRF protection** across all forms. All POST/PUT/DELETE operations are vulnerable to Cross-Site Request Forgery attacks.

---

## 🎯 Implementation Strategy

### Phase 1: Backend Setup (Infrastructure)
### Phase 2: Template Updates (Form Protection)
### Phase 3: AJAX/Fetch Integration (API Protection)
### Phase 4: Testing & Verification

---

## 📁 FILES REQUIRING MODIFICATIONS

### **Phase 1: Backend Infrastructure Setup**

#### 1. `requirements.txt`
**Action:** Add Flask-WTF package
```
flask-wtf
```

---

#### 2. `extensions.py`
**Action:** Initialize CSRFProtect extension
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
```

---

#### 3. `app.py`
**Action:** Import and initialize CSRF in app factory
```python
from extensions import csrf
# Inside create_app():
csrf.init_app(app)
```

---

#### 4. `config.py`
**Action:** Update configuration
- ✅ `SECRET_KEY` already exists (required for CSRF token signing)
- ❌ Remove or update `WTF_CSRF_ENABLED = False` in `TestingConfig` (line ~60)
- ➕ Add optional CSRF settings:
  ```python
  WTF_CSRF_TIME_LIMIT = None  # Optional: token expiration time
  WTF_CSRF_SSL_STRICT = True  # Enforce HTTPS for CSRF
  ```

---

### **Phase 2: Template Files - CSRF Token Addition**

> **Rule:** Add `{{ csrf_token() }}` hidden field to **ALL forms** (both POST and GET methods for consistency)

#### **Authentication Forms** (3 files)

| # | File | Forms to Update |
|---|------|----------------|
| 1 | `templates/auth/login.html` | Login form |
| 2 | `templates/auth/register.html` | User registration form |
| 3 | `templates/auth/register_business.html` | Business registration form |
| 4 | `templates/auth/forgot_password.html` | Password reset request form |
| 5 | `templates/auth/reset_password.html` | Reset password with token form |

---

#### **User Profile Forms** (1 file)

| # | File | Forms to Update |
|---|------|----------------|
| 6 | `templates/user/profile.html` | Profile update form |

---

#### **Business Management Forms** (3 files)

| # | File | Forms to Update |
|---|------|----------------|
| 7 | `templates/business/manage_rooms.html` | Add room form, Delete room forms (multiple) |
| 8 | `templates/business/manage_menu.html` | Add menu item form, Delete menu item forms (multiple) |
| 9 | `templates/business/edit_establishment.html` | Edit establishment form |

---

#### **Barangay Management Forms** (7 files)

| # | File | Forms to Update |
|---|------|----------------|
| 10 | `templates/barangay/profile.html` | Barangay profile update form |
| 11 | `templates/barangay/add_attraction.html` | Add attraction form |
| 12 | `templates/barangay/edit_attraction.html` | Edit attraction form |
| 13 | `templates/barangay/add_event.html` | Add event form |
| 14 | `templates/barangay/edit_event.html` | Edit event form |
| 15 | `templates/barangay/add_gallery.html` | Add gallery item form |
| 16 | `templates/barangay/edit_gallery.html` | Edit gallery item form |

---

#### **Admin Forms** (10 files)

| # | File | Forms to Update |
|---|------|----------------|
| 17 | `templates/admin/add_attraction.html` | Add attraction form |
| 18 | `templates/admin/edit_attraction.html` | Edit attraction form |
| 19 | `templates/admin/add_event.html` | Add event form |
| 20 | `templates/admin/edit_event.html` | Edit event form |
| 21 | `templates/admin/heritage_form.html` | Add/edit heritage form |
| 22 | `templates/admin/heritage_list.html` | Delete heritage forms (multiple) |
| 23 | `templates/admin/establishments.html` | Approve/reject/delete establishment forms (multiple) |
| 24 | `templates/admin/documents_edit.html` | Document edit form |
| 25 | `templates/admin/documents_dashboard.html` | Import documents form |
| 26 | `templates/admin/document_editor.html` | Save document form |
| 27 | `templates/admin/newsletter/compose.html` | Compose newsletter form |
| 28 | `templates/admin/newsletter/index.html` | Delete subscriber forms (multiple) |

---

#### **Public-Facing Forms** (5 files)

| # | File | Forms to Update |
|---|------|----------------|
| 29 | `templates/pagez/index.html` | Search form, Newsletter subscription form |
| 30 | `templates/pagez/search_results.html` | Search form |
| 31 | `templates/pagez/events.html` | Events filter form |
| 32 | `templates/pagez/establishments.html` | Establishments filter form |
| 33 | `templates/pagez/establishment_detail.html` | Submit review form |

---

#### **Base Template Forms** (1 file)

| # | File | Forms to Update |
|---|------|----------------|
| 34 | `templates/base.html` | Navbar search form, Mobile search form |

---

### **Phase 3: AJAX/Fetch Request Protection**

#### Files with AJAX POST Requests

| # | File | AJAX Endpoint | Action Required |
|---|------|---------------|----------------|
| 1 | `templates/pagez/index.html` | `/subscribe` (newsletter) | Add CSRF token to request headers |
| 2 | Any JavaScript files making fetch/AJAX calls | All POST endpoints | Include CSRF token in `X-CSRFToken` header |

**Implementation Pattern:**
```html
<!-- In <head> section of base.html -->
<meta name="csrf-token" content="{{ csrf_token() }}">
```

```javascript
// In JavaScript files
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

fetch('/endpoint', {
  method: 'POST',
  headers: {
    'X-CSRFToken': csrfToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
});
```

---

## 📊 Summary Statistics

| Category | Count |
|----------|-------|
| **Total Template Files with Forms** | 34 |
| **Total POST/PUT/DELETE Route Handlers** | 42 |
| **Backend Files to Modify** | 4 |
| **AJAX/Fetch Handlers to Update** | 1+ |

---

## 🔧 Implementation Details

### **CSRF Token Syntax for HTML Forms**

Add this hidden field as the **first element** inside every `<form>` tag:

```html
<form method="POST" action="{{ url_for('route.name') }}">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  <!-- rest of form -->
</form>
```

**Alternative (Flask-WTF auto-injection):**
Configure Jinja2 to auto-inject CSRF tokens globally (requires customization in `app.py`).

---

### **Priority Order**

1. **🔴 CRITICAL** - Authentication forms (login, register, password reset)
2. **🔴 CRITICAL** - Admin management forms (delete, approve, reject)
3. **🟡 HIGH** - Business management forms (rooms, menu, establishment)
4. **🟡 HIGH** - Barangay management forms (all CRUD operations)
5. **🟢 MEDIUM** - User profile forms
6. **🟢 MEDIUM** - Public-facing forms (reviews, subscriptions)
7. **🔵 LOW** - Search/filter forms (GET methods - optional but recommended for consistency)

---

## ✅ Verification Checklist

After implementation, verify:

- [ ] All POST/PUT/DELETE forms include `{{ csrf_token() }}` hidden field
- [ ] All AJAX requests include `X-CSRFToken` header
- [ ] `Flask-WTF` added to `requirements.txt`
- [ ] CSRFProtect initialized in `extensions.py`
- [ ] CSRF initialized in `app.py`
- [ ] `WTF_CSRF_ENABLED = False` removed from testing config
- [ ] Test all forms submit successfully
- [ ] Test with browser dev tools (Network tab) to verify token presence
- [ ] Verify CSRF meta tag present in `<head>` for JavaScript access

---

## 🧪 Testing Strategy

1. **Manual Testing:** Submit each form and verify it works with CSRF token
2. **Negative Testing:** Attempt form submission without CSRF token (should fail with 400 Bad Request)
3. **Automated Testing:** Update test suite to include valid CSRF tokens in POST requests
4. **Security Testing:** Use tools like OWASP ZAP to verify CSRF protection is effective

---

## ⚠️ Important Notes

- **SECRET_KEY** must be kept secure and consistent across deployments
- **HTTPS** should be enforced in production for CSRF protection to be effective
- **Token Expiration:** Consider setting `WTF_CSRF_TIME_LIMIT` for high-security forms
- **SameSite Cookies:** Consider adding SameSite attribute to session cookies as defense-in-depth

---

## 📚 Reference Documentation

- Flask-WTF Docs: https://flask-wtf.readthedocs.io/
- CSRF Protection Pattern: https://owasp.org/www-community/attacks/csrf
- Flask Security Best Practices: https://flask.palletsprojects.com/en/latest/security/

---

**Generated:** 2026-04-10  
**Status:** Plan - Ready for Implementation  
**Estimated Effort:** 2-4 hours (depending on form count and testing depth)
