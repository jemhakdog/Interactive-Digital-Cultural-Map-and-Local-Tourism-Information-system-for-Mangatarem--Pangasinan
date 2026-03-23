# PLAN: User Login Flowchart

Project Type: **BACKEND/DOCUMENTATION**

## Overview
This plan outlines the creation of a comprehensive user login flowchart for the Mangatarem Digital Map project. The flowchart will cover manual login, Google OAuth login, registration approval flows, and password reset mechanisms, reflecting the current implementation in `routes/auth.py`.

## Tech Stack
- **Diagramming**: Mermaid.js (for high-fidelity embedded diagrams).
- **Interoperability**: Draw.io XML/Compressed format.
- **Documentation**: Markdown (`docs/user-login-flowchart.md`).

## File Structure
- `docs/user-login-flowchart.md` [NEW]: Contains the Mermaid diagram and explanations.
- `docs/user-login-flowchart.drawio` [NEW]: XML file for Draw.io.

## Task Breakdown

### Phase 1: Analysis & Design
- **Task 1**: Draft Mermaid flowchart logic covering:
  - Standard Login (Username/Password).
  - Google OAuth Logic (User creation vs. existing account).
  - Role-based redirection (Admin, Contributor, User).
  - Approval check for Contributors.
  - Password Reset flow.
- **Agent**: `orchestrator`
- **Skill**: `frontend-design` (for UX flow)
- **VERIFY**: Check all routes in `auth.py` are accounted for.

### Phase 2: Implementation
- **Task 2**: Create `docs/user-login-flowchart.md` with the Mermaid code.
- **Task 3**: Generate Draw.io compatible XML and save as `docs/user-login-flowchart.drawio`.
- **Agent**: `orchestrator`
- **Skill**: `clean-code`
- **VERIFY**: Mermaid diagram renders correctly.

## Phase X: Verification
- [ ] Verified manual login flow (Success/Fail/Approval).
- [ ] Verified Google OAuth flow.
- [ ] Verified Password Reset flow.
- [ ] Verified Flowchart renders in Markdown preview.
- [ ] Verified Draw.io file is created correctly.
