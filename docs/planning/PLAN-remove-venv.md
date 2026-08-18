# PLAN: Remove Virtual Environment from Git Tracking

Remove the virtual environment folder (e.g., `.venv`, `venv`) from the repository's tracking to prevent it from being pushed to GitHub, while keeping it locally for development.

## User Review Required

> [!IMPORTANT]
> This plan assumes you want to **keep** the virtual environment folder on your local machine. If you want it deleted entirely from your computer, please let me know.

## Proposed Changes

### Git Configuration & Clean-up

#### [MODIFY] [.gitignore](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/.gitignore)
- Ensure `.venv/`, `venv/`, and `env/` are all present. (Currently `.venv/`, `env/`, and `venv/` are already there).

#### [EXECUTE] Untrack Folders
- Run `git rm -r --cached .venv` (and other variants if found).
- This removes the folder from Git's index without deleting the local files.

#### [EXECUTE] Commit Changes
- Commit the removal and the `.gitignore` update (if any).
- This will effectively delete the folder from GitHub in the next push.

---

## Verification Plan

### Automated Tests
1. **Verify Index**:
   ```powershell
   git ls-files .venv
   git ls-files venv
   git ls-files env
   ```
   *Expected: No results for these commands.*

2. **Verify Git Status**:
   ```powershell
   git status
   ```
   *Expected: Clean working tree (after commit) with no pending additions of venv files.*

---
## After Planning

Tell user:
```
[OK] Plan created: docs/PLAN-remove-venv.md

Next steps:
- Review the plan
- Run `/create` to start implementation
- Or modify plan manually
```
