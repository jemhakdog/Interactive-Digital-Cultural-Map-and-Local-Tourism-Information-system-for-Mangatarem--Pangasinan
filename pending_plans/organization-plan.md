# Codebase Organization Plan

## Goal
Organize non-code files that don't affect the codebase logic, code structure, or application functionality into appropriate folders for better project maintainability.

## Files to Organize

### 1. Personal/Academic Files → `personal/` folder
- `mygrades.json` - Personal academic records
- **Action**: Create `personal/` folder and move file

### 2. Report Files → `reports/` folder
- `lint_report.txt` - Linting results
- `final_lint_report.txt` - Final linting report
- `security_report_summary.txt` - Security scan summary
- `security_report_full.json` - Full security scan JSON
- `final_security_report.txt` - Final security report
- **Action**: Move all to existing `reports/` folder

### 3. Documentation/Reference Files → `docs/` folder
- `all_local_files.txt` - File listing reference
- `tracked_files_full.txt` - Tracked files reference
- `supabase_schema.sql` - Database schema reference (if not actively used)
- **Action**: Move to `docs/reference/` subfolder

### 4. Build/Configuration Files (KEEP IN ROOT)
These affect the build process and should stay:
- `package.json` - Node.js dependencies
- `package-lock.json` - Node.js lock file
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Python project metadata
- `uv.lock` - UV lock file
- `tailwind.config.js` - Tailwind configuration
- `terser-config.json` - Terser JS minifier config
- `wrangler.toml` - Cloudflare Workers config
- `config.py` - Application config
- `.gitignore` - Git ignore rules

### 5. Core Application Files (KEEP IN ROOT)
These are essential application files:
- `app.py` - Main application entry
- `models.py` - Database models
- `extensions.py` - Flask extensions
- `list_routes.py` - Route listing utility (used in development)
- `update_erd.py` - ERD update script
- `update_flowchart.py` - Flowchart update script

### 6. Documentation (KEEP IN ROOT)
- `README.md` - Project readme
- `PROJECT_DESCRIPTION.md` - Project description
- `CHANGES.md` - Changelog
- `QWEN.md` - Project context/guide

## Tasks

- [x] **Task 1**: Create `personal/` folder → Verify: Folder exists in root
- [x] **Task 2**: Move `mygrades.json` to `personal/` → Verify: File moved successfully
- [x] **Task 3**: Move lint reports to `reports/` → Verify: `lint_report.txt`, `final_lint_report.txt` moved
- [x] **Task 4**: Move security reports to `reports/` → Verify: `security_report_summary.txt`, `security_report_full.json`, `final_security_report.txt` moved
- [x] **Task 5**: Create `docs/reference/` subfolder → Verify: Folder exists
- [x] **Task 6**: Move reference files to `docs/reference/` → Verify: `all_local_files.txt`, `tracked_files_full.txt`, `supabase_schema.sql` moved
- [x] **Task 7**: Update `.gitignore` if needed → Verify: New folders are properly tracked/ignored
- [x] **Task 8**: Verify application imports → Verify: Python can import app module (database error is pre-existing, unrelated to file moves)

## Done When
- [x] All personal files moved to `personal/`
- [x] All report files consolidated in `reports/`
- [x] All reference documentation in `docs/reference/`
- [x] No code files or build configs moved
- [x] Application imports successfully (database migration needed for full run)
- [x] Git tracking new file locations

## Notes
- This reorganization is purely for file management
- No code logic, imports, or application structure will be affected
- All moved files are either personal data, generated reports, or reference documentation
- Git will track these as renames, preserving history
