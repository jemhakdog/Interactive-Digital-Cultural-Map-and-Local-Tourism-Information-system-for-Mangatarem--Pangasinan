# Plan: Remove PocketBase Dependencies

This plan outlines the steps to completely remove all PocketBase-related code and files from the Mangatarem Tourism Information System codebase. These components appear to be experimental or legacy scripts that are no longer needed.

## Proposed Changes

### Dependencies Removal

- Remove `pocketbase` from `requirements.txt`
- Remove `pocketbase` from `pyproject.toml`
- Update `uv.lock`

### File Deletion

- Delete `scripts/auth/` (All files)
- Delete `scripts/pocketbasesample.py`
- Delete `scripts/api-rules.py`
- Delete `utils/apirules.py`

### Documentation Update

- Update `scripts/README.md` to remove PocketBase references.

## Verification Plan

- Run `uv lock`
- Verify Flask app starts
- Confirm file deletions
