# Remove PocketBase Dependencies Plan

## Original Location
`/docs/planning/PLAN-remove-pocketbase.md`

## Status: ⚠️ PARTIALLY IMPLEMENTED (Files deleted, but references remain)

### What Was Planned

Complete removal of all PocketBase-related code and files from the codebase.

### Proposed Changes

#### Dependencies Removal
- ❌ Remove `pocketbase` from `requirements.txt` - **NOT VERIFIED** (needs checking)
- ❌ Remove `pocketbase` from `pyproject.toml` - **NOT VERIFIED**
- ❌ Update `uv.lock` - **NOT VERIFIED**

#### File Deletion
- ❓ Delete `scripts/auth/` - **NEEDS VERIFICATION**
- ❓ Delete `scripts/pocketbasesample.py` - **NEEDS VERIFICATION**
- ❓ Delete `scripts/api-rules.py` - **NEEDS VERIFICATION**
- ❓ Delete `utils/apirules.py` - **NEEDS VERIFICATION**

#### Documentation Update
- ❓ Update `scripts/README.md` to remove PocketBase references - **NEEDS VERIFICATION**

### Current State

⚠️ **PocketBase references still exist:**
- `tests/test_pb_auth.py` still contains PocketBase mock tests
- This suggests `utils/pb_auth.py` may still exist
- PocketBase auth tests indicate the dependency might still be in use

### Why It's Pending/Incomplete

1. **Test files remain**: `tests/test_pb_auth.py` still has PocketBase auth tests
2. **Unclear if utils/pb_auth.py exists**: Needs verification
3. **Dependencies not confirmed removed**: PocketBase may still be in requirements

### Priority
Medium (cleanup technical debt)

### Estimated Effort
1-2 hours

### Next Steps
1. Check if `utils/pb_auth.py` exists
2. Delete PocketBase-related scripts and utilities
3. Remove PocketBase from requirements.txt and pyproject.toml
4. Delete or update `tests/test_pb_auth.py`
5. Update documentation
6. Run `uv lock` to update dependencies
7. Verify app still starts without errors
