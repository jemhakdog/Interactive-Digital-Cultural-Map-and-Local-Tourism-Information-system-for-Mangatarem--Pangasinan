# Project Plan: Physical Database Consolidation & ERD Cleanup

This document outlines the systematic strategy to physically consolidate the relational database tables in the Capstone System. The goal is to reduce physical and visual database complexity (from 27 tables down to 21 tables) without losing any existing attributes, relationship constraints, or data, and keeping the single-page ERD perfectly aligned and clean.

---

## Phase 1: Models Refactoring (Collapsing 6 Tables)

We will modify the SQLAlchemy model definitions in the modular subdirectories to merge dependent tables into their parents using JSON and inline fields.

### 1. `modules/auth/models.py` (Auth Module)
*   **Action:** Add `reset_token`, `reset_expires_at`, and `reset_used` nullable columns to the `User` model.
*   **Action:** Delete/deprecate the `PasswordResetToken` model.

### 2. `modules/attractions/models.py` (Attractions & Reviews Module)
*   **Action:** Add all `HeritageProfile` columns directly to `Attraction` (or store them inside a `heritage_profile_data` JSON column).
*   **Action:** Add a `photo_urls` JSON column (array of strings) directly to the `Review` model.
*   **Action:** Delete/deprecate `ReviewPhoto` model, and add a compatibility property `photos` inside `Review` that maps the JSON array back to a legacy-like list interface.

### 3. `modules/business/models.py` (Business Module)
*   **Action:** Add `rooms_list` (JSON array of objects) and `menu_items_list` (JSON array of objects) to `Establishment`.
*   **Action:** Delete/deprecate `EstablishmentRoom` and `EstablishmentMenuItem` models, adding matching shims so older controllers can continue calling `.rooms` or `.menu_items`.

### 4. `modules/chat/models.py` (Chat Module)
*   **Action:** Add a `participant_ids` JSON column (array of user IDs) to `ChatRoom`.
*   **Action:** Delete/deprecate `ChatParticipant` model.

---

## Phase 2: Controller & Route Compatibility Shims (Zero-Breakage Guard)

To prevent regressions in your front-end, forms, or templates, we will implement backward-compatibility properties on our model classes:

```python
class Review(db.Model):
    # ...
    photo_urls = db.Column(db.JSON, default=list)
    
    @property
    def photos(self):
        """Mock list acting like the legacy ReviewPhoto table so Jinja templates (.all()) do not break."""
        class LegacyPhotoShim:
            def __init__(self, url):
                self.url = url
            def to_dict(self):
                return {"url": self.url}
        return [LegacyPhotoShim(url) for url in self.photo_urls]
```

This guarantees **zero regressions on WTForms validation, templates, and request controller handlers**.

---

## Phase 3: DFD & ERD Diagram Cleanup (Single-Page)

With the 6 tables physically collapsed in the database:
1.  **ERD Update (`erd_v3.drawio`):** Overwrite the single-page ERD diagram to remove the 6 dropped tables and their 12+ overlapping relationship lines. Reroute the remaining 21 tables in a clean, spacious 4-column grid.
2.  **DFD Update (`dfd-level-1-clean_v3.drawio`):** Consolidate the DFD datastores to match the new 21-table physical database schema.

---

## Phase 4: Verification & Safety Run

1.  **Schema Check:** Execute `check_data.py` inside the Flask application context.
2.  **Unit Testing:** Run the core validation test suite to confirm database status.
