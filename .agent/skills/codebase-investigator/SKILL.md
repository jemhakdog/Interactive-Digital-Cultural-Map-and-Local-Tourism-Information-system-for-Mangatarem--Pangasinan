---
name: codebase-investigator
description: Investigate and research the codebase for specific patterns, file types, or issues (e.g., finding SQL codes, duplicate imports). Use when the user requests a deep dive or research task within the project. Results must be saved in the 'investigation' folder as .md files.
---

# Codebase Investigator

This Skill enables deep research and investigation of the codebase to identify specific patterns, technologies, or structural issues.

## Instructions

1. **Understand the Goal**: Identify exactly what the user wants to find or analyze (e.g., "all SQL queries", "duplicate CSS selectors", "unused functions").
2. **Perform Research**:
   - Use `grep_search` for text patterns.
   - Use `find_by_name` for specific file types or filenames.
   - Use `list_dir` and `view_file` to explore the structure and content.
3. **Analyze Findings**: Synthesize the gathered information into a structured report.
4. **Output Results**:
   - Create a new markdown file in the `investigation/` directory at the project root.
   - The filename should be descriptive (e.g., `sql_investigation.md`, `duplicate_cdn_report.md`).
   - The report should include:
     - **Summary of Findings**
     - **Detailed list of files/locations**
     - **Code snippets (if relevant)**
     - **Recommendations or next steps**
5. **Notify the User**: Once the report is saved, inform the user of the path to the report.

## Examples

### Investigating SQL-related code
- User: "Find all files with sql related codes."
- Action: Search for "SELECT", "INSERT", "UPDATE", "DELETE", ".sql", "sqlite", "SQLAlchemy" etc.
- Output: `investigation/sql_results.md`

### Finding duplicated CDN links
- User: "Find duplicated cdn in frontend folder."
- Action: Grep for common CDN patterns (e.g., `https://cdnjs.cloudflare.com/`, `https://cdn.jsdelivr.net/`) in `templates/` or `static/`.
- Output: `investigation/duplicated_cdn_report.md`

## Best practices

- **Consistency**: Always save reports in the `investigation/` folder.
- **Clarity**: Use clear, descriptive headings in reports.
- **Actionable**: Whenever possible, suggest fixes or improvements based on the investigation.
