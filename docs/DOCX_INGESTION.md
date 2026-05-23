# DOCX Ingestion and Rapid Editor Integration

> [!NOTE]
> This document outlines the technical implementation and workflow for importing community-provided `.docx` files (Forms 01-07) and pre-filling the Rapid Editor for validation before saving to the database.

## Architecture Overview

The DOCX ingestion pipeline is designed to automate the extraction of data from official Mangatarem Cultural Heritage and Local Tourism forms. By allowing barangay representatives and mappers to upload their filled Word documents, the system reduces manual data entry and minimizes human error.

The workflow consists of three primary phases:
1. **File Upload & Parsing**: The user uploads a `.docx` file via the Admin UI. The backend parses the document using the `python-docx` library, applying specific heuristics to detect the form type and extract key-value pairs.
2. **Session Storage**: The extracted data is temporarily stored in the secure Flask session state.
3. **Validation via Rapid Editor**: The user is redirected to the Rapid Editor (Visual Canvas) where the extracted data is pre-filled. The user must review, edit if necessary, and explicitly save the record to persist it to the PostgreSQL database.

## Core Components

### 1. The Parser (`routes/v1/documents.py`)

The core parsing logic is handled by the `_parse_docx_file(filepath)` function. 

**Two-Pass Form Detection Algorithm:**
Early implementations suffered from "keyword leaks" (e.g., a document containing the word "intangible" anywhere would be misclassified as Form 04A). To solve this, a two-pass detection algorithm is used:
* **Pass 1 (Prefix Check)**: The parser scans the first 10 paragraphs of the document for exact form prefixes (e.g., `FORM 04-A`, `FORM 07`).
* **Pass 2 (Global Fallback Check)**: If no prefix is found, the parser falls back to a global search for specific keywords throughout the document.

**Extraction Heuristics:**
* **Paragraph Blocks**: For standard forms, the parser iterates through paragraphs. When it detects a known keyword (e.g., "NAME:"), it extracts the value from the same paragraph or looks ahead to the subsequent paragraphs for multi-line values.
* **Matrix Parsing (Form 07)**: Form 07 (LGU Program) relies heavily on tables/matrices. The parser includes specialized logic to traverse the document's tables, extracting specific cells for fields like `vision`, `mission`, `goals`, `brief_history`, and `strategies`.

### 2. Admin UI Integration

**Import Interface (`templates/admin/documents_v1.html`)**
* The Admin UI features an "Import Filled Form (.docx)" button.
* When a file is selected, a full-screen, blurred loading overlay with a spinner is displayed to provide immediate visual feedback while the server processes the file.

**Rapid Editor Pre-filling (`templates/admin/documents_rapid_editor_v1.html`)**
* Upon successful parsing, the `/v1/documents/import` route redirects the user to the `/v1/documents/create/<slug>?prefilled=1` route.
* The pre-filled data is popped from the session and passed to the Jinja template as the `prefilled_data` variable.
* The template uses an intelligent fallback mechanism to populate input fields:
  `value="{{ record[f_key] if record else (detail[f_key] if detail else (prefilled_data.get(f_key, '') if prefilled_data else '')) }}"`
* This ensures that the extracted data is seamlessly merged into both the visual canvas inputs and the Detailed Information Registry fields.

## Security and Integrity

* **No Direct Inserts**: The parser **never** inserts data directly into the database. All ingested data must pass through the Rapid Editor and be manually saved by an administrator or authorized user. This ensures a human-in-the-loop validation step.
* **CSRF Protection**: All file uploads and form submissions are protected by Flask-WTF CSRF tokens.
* **Session Management**: Extracted data is stored in the session and popped (removed) immediately upon rendering the Rapid Editor to prevent state leakage across requests.

## Adding Support for New Forms

To add support for a new DOCX form format:
1. Update the `SLUG_MAPPING` dictionary in `_parse_docx_file` to map the new form's prefix/keywords to its internal slug (e.g., `form_08_new_type`).
2. If the form uses standard paragraph blocks, add the expected labels to the generic keyword-based extraction loop.
3. If the form uses complex tables or matrices, implement custom extraction logic specifically for that form type, similar to the existing `form_07_lgu_program` logic.
4. Ensure the corresponding heritage model (e.g., `heritage_models/new_form_type.py`) contains the appropriate fields to receive the extracted data.
5. Add unit tests to `tests/test_docx_import.py` to verify the new parsing logic.
