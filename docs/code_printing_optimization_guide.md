# Capstone Source Code Printing Optimization Guide

This guide details strategies and practices to minimize page count, save paper, and reduce printing and bookbinding costs when preparing the source code appendix for your capstone thesis/documentation.

---

## 📋 1. Files and Directories to Exclude (DO NOT PRINT)

Do not print any dependencies, build outputs, auto-generated code, or configuration files that do not contain core logic.

| Category | Directories / Files | Reason |
| :--- | :--- | :--- |
| **Virtual Environments** | `.venv/`, `node_modules/` | Contain thousands of pages of standard library and external package code. |
| **Database Migrations** | `migrations/` | Automatically generated SQL/Python migration history; highly repetitive. |
| **Caches & Build Directories** | `__pycache__/`, `.pytest_cache/`, `build/`, `.git/` | Binary or temporary system logs that are not readable source code. |
| **Static External Assets** | Standard vendor libraries (e.g., Bootstrap, jQuery, Leaflet) | These are third-party files. Only print custom JS/CSS. |
| **Environment & Configs** | `.env`, `.gitignore`, `uv.lock`, `package-lock.json` | Lockfiles and system configuration parameters containing no logic. |
| **Test Suites** | `tests/` | Unless explicitly required by your panel, test suites can be excluded. |

---

## 💻 2. What to Include (Core Logic Only)

To satisfy the requirements of a source code appendix, focus only on the custom files that define your unique capstone functionality.

1. **Database Schema & Models:**
   * File: [models.py](file:///d:/porjects/capstone_system/models.py)
   * Description: Shows the database design and relationship structure of your system data.
2. **Main Application Routing / Controllers:**
   * Main Entrypoint: [app.py](file:///d:/porjects/capstone_system/app.py)
   * API v1 Routes: [public.py](file:///d:/porjects/capstone_system/modules/api_v1/public.py)
   * Business/Establishment Routes: [routes.py](file:///d:/porjects/capstone_system/modules/business/routes.py)
   * Description: Shows how HTTP requests, API calls, and business rules are handled.
3. **Core Interactive Frontend Scripts:**
   * Map & Proximity Script: [map_v2.js](file:///d:/porjects/capstone_system/static/js/pages/map_v2.js)
   * Description: Custom mapping logic, GPS tracking, and coordinate validation handlers.
4. **Custom Layout Handlers:**
   * Main Interactive Map Template: [map_v2.html](file:///d:/porjects/capstone_system/templates/pagez/map_v2.html)
   * Attraction Details Template: [detail_v1.html](file:///d:/porjects/capstone_system/templates/pagez/detail_v1.html)
   * Description: Key layout containers and custom template views. Do not print general, repetitive boilerplate templates.

---

## 🖨️ 3. Formatting Tricks to Maximize Page Economy

When pasting the code into your word processor (MS Word, Google Docs, or LaTeX), use these adjustments to condense the pages:

*   **Two-Column Layout:** Format the appendix pages into two columns. Since source code lines are short, standard single-column pages waste over 50% of the horizontal space.
*   **Small Monospace Font:** Set your code font to `Consolas`, `Courier New`, or `Fira Code` at **8pt** or **9pt** size.
*   **Single Line Spacing:** Adjust paragraph spacing to `0pt` before/after and line spacing to single (`1.0`).
*   **Narrow Margins:** Change the margins of your appendix section to **0.5 inches (Narrow)** on all sides.
*   **Strip Code Comments & Blank Lines:** Create a copy of the target files and strip empty lines and long docstrings/comments to make the printed content compact.

---

## 🔗 4. The "Hybrid Documentation" Strategy (Recommended)

To present a professional, industry-standard documentation package while keeping the book thin:

1. **Include a System Directory Tree:**
   * Print a high-level visual map of your project files using a directory list (e.g., using `tree` in your terminal). This shows structure without printing the code content.
2. **Setup a Code Repository:**
   * Push your codebase to a repository provider (GitHub or GitLab).
3. **Insert QR Code and Repository Link:**
   * Place a clear section at the beginning of the Appendix containing a QR code and a clickable URL linking to the codebase.
   * *Example text:*
     > "The full, active source code for the Mangatarem Interactive Map and Tourism System is version-controlled and hosted on GitHub. Scan the QR code below or visit [Repository URL] to view the complete implementation, commit history, and deployment assets."
4. **Print "Selected Core Snippets":**
   * Only print the absolute core files (e.g. `models.py`, `app.py`) in the paper, explaining to the panel that the rest is available via the QR code repository.
