# Cleanup Unused Files and Junks

**Type:** Task
**Created:** 2026-02-21
**Status:** Planning
**Context File:** `.claude/prds/context/2026-02-21-cleanup-unused-files-task.json`

## Overview

### Problem/Goal
The project directory contains several leftover scripts, backup folders, outdated diagrams, and historical reports that are no longer actively required for running or developing the application. Identifying and removing these files will reduce clutter, prevent confusion, and improve the maintainability of the repository.

### Success Criteria
- [ ] Root directory only contains necessary configuration and entrypoint files.
- [ ] Known backup or temporary directories (e.g., `instance_backup`, `archive`, `pending_plans`) are removed.
- [ ] Leftover Python utility scripts not used in the application flow are removed.
- [ ] The application starts successfully and all core features work after the cleanup.

## Technical Approach

We will perform a systematic audit and deletion of files in specific categories:
1. **Unused Root Scripts**: e.g., `update_flowchart.py`, `update_flowchart_ppt.py`, `verify_schema.py`, `list_routes.py`. These scripts were originally used for diagram updates or listing endpoints, but might not be actively needed.
2. **Historical/Backup Directories**: e.g., `archive/`, `pending_plans/`, `reports/`, `instance_backup/`, `db_update_package/`. These likely served as temporary storage for past tasks.
3. **Diagrams**: e.g., `erd_v1.drawio`.
4. **Tool-specific Folders**: e.g., `.qwen/` and `QWEN.md`.

## Implementation Checklist

### Preparation
- [ ] Identify all target files and directories for deletion.
- [ ] Confirm with the user if any of these identified files should be preserved.

### Execution
- [ ] Delete `instance_backup/` directory.
- [ ] Delete `archive/` directory.
- [ ] Delete `pending_plans/` directory.
- [ ] Delete `reports/` directory.
- [ ] Delete `db_update_package/` directory.
- [ ] Delete `.qwen/` directory and `QWEN.md`.
- [ ] Delete unused scripts: `update_flowchart.py`, `update_flowchart_ppt.py`, `verify_schema.py`, `list_routes.py`.
- [ ] Delete intermediate diagrams like `erd_v1.drawio`.

### Validation
- [ ] Restart server to confirm no runtime errors or missing essential files.

**Status:** ⏳ Not Started

## Testing Strategy
Basic smoke test. Run the server, verify no missing import errors.

## Rollback Plan
Restore files using `git checkout` or `git restore` if any deletion breaks functionality.

## Dependencies
None.
