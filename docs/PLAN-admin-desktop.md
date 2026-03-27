# PLAN: Admin Desktop Application (Mangatarem Tourism)

This plan outlines the creation of a Windows-based desktop application for the Administrative Dashboard of the Mangatarem Tourism Information System using `flaskwebgui`.

## User Review Required

> [!IMPORTANT]
> - **Local Database**: The app will use a local SQLite database (`instance/mangatarem.db`). Initial data will be seeded from `data/attractions.json`.
> - **Auto-start**: The app will include a PowerShell script to set up a Windows Startup shortcut.
> - **Admin Only**: The desktop app will be configured to open directly to the `/admin/login` or `/admin/dashboard` page.

## Proposed Changes

### [Foundation]

#### [MODIFY] [requirements.txt](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/requirements.txt)
- Add `flaskwebgui>=1.0.0`
- Add `pyinstaller>=6.0.0`

### [Desktop App Shell]

#### [NEW] [desktop.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/desktop.py)
- Create an entry point that initializes the Flask app using the factory pattern.
- Wrap it with `FlaskUI` from `flaskwebgui`.
- Configure it to start maximized and point to `/admin`.

#### [MODIFY] [config.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/config.py)
- Ensure path handling for `BASE_DIR` works correctly when frozen by `PyInstaller` (using `sys._MEIPASS` if needed).

### [Automation]

#### [NEW] [scripts/setup_autostart.ps1](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/scripts/setup_autostart.ps1)
- PowerShell script to create a shortcut in `shell:startup` pointing to the packaged `.exe`.

## Task Breakdown

| Task ID | Name | Agent | Skills | Priority | Dependencies | INPUT → OUTPUT → VERIFY |
|---------|------|-------|--------|----------|--------------|--------------------------|
| 1 | Dependency Update | `backend-specialist` | `clean-code` | P0 | None | Update `requirements.txt` → `pip install` → No conflicts |
| 2 | Desktop Entry Point | `backend-specialist` | `python-patterns` | P1 | 1 | Create `desktop.py` → `python desktop.py` opens window → Window displays Admin Login |
| 3 | Path Normalization | `backend-specialist` | `python-patterns` | P1 | 2 | Adjust `config.py` for PyInstaller compatibility → App runs locally with `flaskwebgui` |
| 4 | Auto-start Script | `devops-engineer` | `powershell-windows` | P2 | 2 | Create `setup_autostart.ps1` → Run script → Shortcut appears in Startup folder |
| 5 | Executable Packaging | `devops-engineer` | `deployment-procedures` | P2 | 3 | Run `pyinstaller --onefile` → `dist/AdminApp.exe` created → EXE runs and starts server |

## Verification Plan

### Automated Tests
- `python desktop.py`: Verify that the GUI window opens and the Flask server starts.
- `ruff check desktop.py`: Ensure linting compliance.

### Manual Verification
1.  **Launch**: Run the packaged `.exe` and verify it automatically opens the Admin login.
2.  **Functionality**: Test a basic admin operation (e.g., adding a temporary attraction) to ensure SQLite persistence.
3.  **Auto-start**: Run the setup script and reboot (or check Startup folder) to verify the process starts with Windows.

## Phase X: Final Verification
- [ ] Security Scan: `python .agent/skills/vulnerability-scanner/scripts/security_scan.py .`
- [ ] UX Audit: `python .agent/skills/frontend-design/scripts/ux_audit.py .`
- [ ] Build Check: `pyinstaller desktop.spec` (or command line) succeeds.
