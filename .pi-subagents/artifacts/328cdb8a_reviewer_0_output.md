Now I have the complete picture. Here's the full report.

---

## Review: Ponytail Over-Engineering Audit

### Correct
- `modules/registry.py` is the live blueprint registry (used by `app.py`); no duplication.
- `modules/auth/routes.py` is a clean URL-rule registrar delegating to handler files — a valid pattern.
- `utils/heritage_registry.py` is a data-driven registry for 7 heritage types — legitimate, avoids 7 near-identical route handlers.
- `utils/cache_helpers.py` centralizes Redis cache logic — reasonable abstraction.
- `utils/security.py` and `utils/validators.py` serve distinct purposes (raw validation vs Flask decorators).
- `core/app_setup.py` consolidates app init hooks in one place.
- `extensions.py` initializes Flask extensions without app — standard pattern.

### Findings (ranked by cut size, biggest first)

```
DELETION .kilo/worktrees/quixotic-thyme/ — full 280MB repo copy. rm -rf .kilo/worktrees/
DELETION routes/__init__.py and routes/auth.py — dead code, app.py uses modules.registry not routes/. rm -rf routes/
DELETION core/db_manager.py — byte-for-byte duplicate of utils/db_manager.py (295 lines). rm core/db_manager.py
DELETION core/geo.py — byte-for-byte duplicate of utils/geo.py (28 lines). rm core/geo.py
DELETION core/logger.py — byte-for-byte duplicate of utils/logger_helper.py (50 lines). rm core/logger.py
DELETION core/session.py — byte-for-byte duplicate of utils/session_helper.py, both 12-line shims already inlined in core/app_setup.py. rm core/session.py utils/session_helper.py
YAGNI utils/logger_helper.py — thin wrappers around stdlib logging.info/debug/error adding zero value; stdlib logger does the same thing. replace: `from utils.logger_helper import log_entry` → `logger.info(...)`. [utils/logger_helper.py]
YAGNI utils/email_sender.py — EmailConfig dataclass wraps 4 env vars for a 2-function SMTP helper. stdlib smtplib + os.environ is enough. simplify: inline config loading into send_email(). [utils/email_sender.py]
DELETION build/desktop.py — imports flaskwebgui (not in pyproject.toml dependencies), dead code. rm build/desktop.py
DELETION utils/validators.py:validate_coordinates_fields — dead decorator, zero callers outside its own definition. delete the function at line 354. [utils/validators.py:354]
DELETION modules/analytics/models.py:DatabaseAuditLog — model defined, log_operation classmethod written, but never called anywhere. delete the class. [modules/analytics/models.py:30]
DELETION archive/ — contains Google OAuth client secrets and stale logs, tracked in repo. rm -rf archive/
DELETION code_screenshots/ — 2.7MB of screenshots, not source. rm -rf code_screenshots/
DELETION .antigravitycli/ — empty directory. rm -rf .antigravitycli/
DELETION tmp/verify_newsletter.py — scratch file tracked in repo. rm -rf tmp/
DELETION instance/heritage_page.html — generated file tracked in repo. rm instance/heritage_page.html
DELETION data/scraped_attractions.json data/scraped_events.json data/scraped_heritage.json — intermediate scraping outputs (111KB). rm data/scraped_*.json
YAGNI modules/auth/ over-decomposition — auth routes split across 5 files (routes.py, login.py, register.py, oauth.py, password.py) when the old routes/auth.py (681 lines) was one coherent file. the current split adds indirection with no benefit for a project this size. consolidate: merge back into modules/auth/routes.py. [modules/auth/]
YAGNI utils/validators.py:validate_json_input — complex 80-line decorator that duplicates validate_form_data logic for JSON. only 0 callers exist (validate_form_data covers both). delete. [utils/validators.py:236]
SHRINK utils/validators.py — 400 lines of generic type-checking decorators (validate_integer, validate_float, validate_boolean) used by 1 decorator. stdlib int()/float()/bool() with try/except covers the same ground in 5 lines each. trim: replace validate_integer/float/boolean with inline conversions in validate_form_data. [utils/validators.py]
SHRINK core/app_setup.py:seed_database — 150 lines of inline seeding logic duplicating root seed_data.py and seed_new_data.py. extract: move seeding to a single seed script, call it from app_setup if needed. [core/app_setup.py:155]
SHRINK root-level seed scripts — seed_data.py (9KB), seed_new_data.py (12KB), setup_contributor.py (2.5KB), reset_db.py (1KB) overlap with core/app_setup.py seeding. consolidate into one scripts/seed.py. [seed_data.py, seed_new_data.py, setup_contributor.py, reset_db.py]
NOTE models.py backward-compat aliases (AttractionReview=Review, etc.) — used in 13 files but should be migrated to direct model names. not blocking, but adds a layer of indirection. [models.py:22]
NOTE templates/admin/documents_*_v1.html — 5 v1 templates actively used by modules/api_v1/. the v1/v2 split is over-engineering for a capstone but is live code, not dead. flag for future merge. [templates/admin/]
NOTE tile_generator.py — 300 lines of PostGIS MVT generation that returns empty tiles on SQLite (local dev). half the module is dead code in local mode. flag: consider lazy-loading or conditional import. [utils/tile_generator.py]
```

### Net Summary

| Category | Items | Est. Lines Cut | Est. Bytes Saved |
|---|---|---|---|
| **DELETION** | 12 | ~1,300 Python + 280MB kilo | ~283 MB |
| **YAGNI** | 4 | ~600 | — |
| **SHRINK** | 3 | ~350 | — |
| **Total** | 19 | ~2,250 Python lines + 283 MB | — |

**Biggest single cut**: `.kilo/worktrees/quixotic-thyme/` at 280MB. The rest is mostly dead/duplicate Python (~1,900 lines) that can be removed with no functional impact.

### Structural Note

The codebase has two competing organizational layers — `routes/` (old) and `modules/` (current) — where `app.py` uses `modules.registry` but `routes/__init__.py` is still tracked. Additionally, `core/` and `utils/` have overlapping files where `utils/` is the canonical location for most helpers. Cleaning these up removes ~1,100 lines of pure duplication with zero behavior change.

---