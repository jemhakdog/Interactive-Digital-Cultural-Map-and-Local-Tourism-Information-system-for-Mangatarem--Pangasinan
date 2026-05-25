# Decisions

Record important project decisions here.

### 2026-05-25 — DFD Level 1 and ERD Consolidated Layout Snapping & Verification

Status: Accepted

Context: The V3.2 database consolidation left several diagram edges and connectors floating or jumbled in both the Entity-Relationship Diagram (ERD) and Level 1 Data Flow Diagram (DFD). Draw.io utilizes hardcoded absolute source/target offset coordinates and intermediate mxPoint control arrays inside XML <mxGeometry> elements. These overrides force arrows to float in space or overlap other components when nodes are consolidated, deleted, or moved, disrupting the layout.

Decision:
1. Conducted deep layout polishing on the Level 1 DFD (`dfd-level-1-clean_v3.drawio`) to eliminate Context-level system boundaries and remove the central hub bubble. Rerouted all 13+ related data flow edges directly between external entities/sub-processes and datastores.
2. Deleted legacy heritage detail datastores (D10, D11, D12, D13, D14, D16, D17) and consolidated their flows to point directly to the single active D15 `Heritage_Profile` datastore.
3. Injected missing active datastores: D30 `Map_Feedback_db` and D31 `Business_Verification_db`, and wired their flows.
4. Corrected duplicate process numbering (Booking renumbered to `14.0`, Chat to `15.0`, Media Gallery to `12.0`, Newsletter to `13.0`).
5. Polished the ERD (`erd_v3.drawio`) to inject the active `BUSINESS_VERIFICATION` model and wire its relationship edge to `USER`.
6. Purged absolute source/target offsets and custom control point arrays from all DFD (21 offsets, 28 arrays) and ERD (12 offsets, 16 arrays) edges. This forces Draw.io to route clean, straight orthogonal paths (`edgeStyle=orthogonalEdgeStyle;rounded=1`) snapped dynamically to the boundary of the connected shapes.

Consequences: Dynamic and perfectly snapped diagram layouts that automatically adjust to shape position modifications. Zero floating, jumbled, or overlapping edges in either diagram, maintaining 100% alignment with the active Flask-SQLAlchemy 27-table schema.

Related files: `docs/diagrams/dfd/dfd-level-1-clean_v3.drawio`, `docs/diagrams/erd/erd_v3.drawio`

### 2026-05-25 — Comprehensive academic rewrite of Chapters 1–3 and dynamic DOCX compiler implementation

Status: Accepted

Context: The existing draft of Chapters 1–3 of the capstone manuscript was written in a highly informal, conversational, first-person voice and contained 12+ formatting, typo, and data consistency issues listed in `todo.md`. Additionally, compiling the manuscript into a Word document previously relied on a script with completely hardcoded paragraphs, making the Markdown files and Word document diverge.

Decision:
1. Conducted a complete rewrite of Chapters 1–3 markdown files to adopt a strict, objective, third-person academic voice, removing all first-person pronouns ("we", "our", "us", "I").
2. Converted lists under Background, Scope, and Limitations into strict paragraph-only blocks, integrated exactly 5 local and 5 foreign literature citations from 2020-2025 with an academic synthesis, added Surveys and Questionnaires as a core data gathering technique, defined diagram notations formally, aligned the Gantt chart RAD calendar starting June 2024, and fixed all listed typos.
3. Redesigned `make.py` from a hardcoded paragraph script into a dynamic Markdown-to-DOCX compiler that parses markdown headers, lists, bold formatting, and HTML-style tables using the `python-docx` library, maintaining the markdown files as the single source of truth.
4. Built an automated quality checker script `verify_manuscript.py` to scan the chapters and ensure zero remaining pronouns or unresolved typos.

Consequences: Highly professional, standard-compliant academic manuscript files compiled dynamically into a styled Times New Roman Word document, with zero remaining typo or pronoun errors.

Related files: `docs/capstone/chapters/Chapter-1-Introduction.md`, `docs/capstone/chapters/Chapter-2-Methodology-and-Design.md`, `docs/capstone/chapters/Chapter-3-Results-and-Discussion.md`, `docs/capstone/chapters/full chapters.md`, `docs/capstone/chapters/make.py`, `scratch/verify_manuscript.py`, `scratch/merge_chapters.py`, `docs/capstone/chapters/Chapter_1_to_3_Consolidated.docx`

### 2026-05-24 — Consolidate Heritage detail tables and resolve Supabase table duplication

Status: Accepted

Context: The system had 7 legacy detail tables for different heritage profiles. Additionally, the online Supabase PostgreSQL database had grown to 62 tables due to case-sensitive duplicates (e.g. "USER" and "user" coexisting) and leftover tables, which caused major schema verification discrepancies and prevented DDL upgrades on SQLite.

Decision:
1. Merge the 7 detail tables into a single `form_data` JSONB column inside `HERITAGE_PROFILE` table, deleting `heritage_models/` dead code.
2. Safe-drop 39 duplicate, legacy, and obsolete tables in the active Supabase database, while preserving unique contributor user data (`barangay`) by migrating it to `"USER"`.
3. Wrap application seeding inside a safe try-except block in `core/app_setup.py` to prevent out-of-sync boot crashes, and stamp the database version at `536847569d90`.

Consequences: Highly optimized, clean, and normalized database schema (bringing table count down to exactly 32 tables) that aligns perfectly between local SQLite and online Supabase, enabling robust migrations.

Related files: `db_schemas/schema.sql`, `scripts/db_ops/verify_schema.py`, `migrations/versions/536847569d90_add_form_data.py`, `core/app_setup.py`, `scratch/verify_db.py`, `scratch/execute_cleanup.py`

### 2026-05-09 — Add cross-model continuity layer

Status: Accepted

Context: User runs Gemini Ultra (Antigravity), Claude Teams, ChatGPT Teams, and OpenRouter free models on the same project. The Memory Bank had no contract for handing off mid-task between models.

Decision: Add `memory-bank/handoff.md` as a single rolling handoff pointer with a fixed schema, plus `workflows/handoff.md` for write/read procedure. AGENTS.md startup path includes handoff as step 3. FAST_INIT update list includes `handoff.md`.

Consequences: Any model can resume work from another model's stopping point in one extra small read. `handoff.md` is volatile; durable knowledge still lives in `activeContext.md`/`progress.md`.

Related files: `AGENTS.md`, `memory-bank/handoff.md`, `memory-bank/00-index.md`, `memory-bank/startup.md`, `workflows/handoff.md`

### 2026-05-09 — Add per-model context budgets and cache-stable file list

Status: Accepted

Context: One global FAST_INIT was too coarse for the mix of large-context (Gemini 1M), cache-friendly (Claude 200K), small-context (OpenRouter free), and turn-sensitive (ChatGPT 128K) models.

Decision: Rewrite `memory-bank/model-routing.md` with per-model budgets/tactics, a cache-stable file list (so Claude prompt-cache hits stay warm), Antigravity sub-agent notes, and concrete current defaults.

Consequences: Each model can be used near-optimally without changing the template. Avoids editing cache-stable files casually.

Related files: `memory-bank/model-routing.md`

### 2026-05-09 — Add Copilot, Cursor, and Codex adapters

Status: Accepted

Context: AGENTS.md is the canonical file across the OpenAI/Cursor agents standard, but additional ecosystems benefit from explicit one-line pointer files.

Decision: Add `.github/copilot-instructions.md`, `.cursor/rules/agents.mdc`, and `.codex/AGENTS.md` as thin adapters. Validator enforces all adapters reference `AGENTS.md`.

Consequences: Copilot, Cursor, and Codex CLI/sub-agents pick up canonical rules natively. No new dependencies.

Related files: `.github/copilot-instructions.md`, `.cursor/rules/agents.mdc`, `.codex/AGENTS.md`, `scripts/check-template.py`

### 2026-05-09 — Enforce zero drift between mirrored workflows and skills

Status: Accepted

Context: `workflows/`, `.clinerules/workflows/`, and `.agents/workflows/` had drifted in places. Same risk for skills.

Decision: Use `workflows/` as canonical for workflows and `.cline/skills/` as canonical for skills. Synced all mirrors. Validator computes SHA-256 hashes and fails on any drift in full-mode.

Consequences: Tool-specific paths preserved; drift impossible without test failure.

Related files: `scripts/check-template.py`, `workflows/`, `.clinerules/workflows/`, `.agents/workflows/`, `.cline/skills/`, `.agents/skills/`

### 2026-05-09 — Add token benchmark to validator and bootstrap

Status: Accepted

Context: The improvement brief asked for a measurable startup-path size metric. Users need a single command to see "what does FAST_INIT cost me" in chars/tokens.

Decision: Add `python scripts/check-template.py --benchmark` and include benchmark output in `scripts/init-fast.py`. Uses chars/4 heuristic.

Consequences: Token cost visible in 1 command without external libraries. Heuristic is approximate but stable across runs and models.

Related files: `scripts/check-template.py`, `scripts/init-fast.py`

### 2026-05-07 — Adopt balanced initialization model (FAST_INIT default, DEEP_AUDIT explicit)

Status: Accepted

Context: Initialization on copied projects consumed excessive tokens when agents interpreted broad prompts as permission for deep repository inspection.

Decision: Add explicit initialization modes in `AGENTS.md`, make `FAST_INIT` the default for low-token initialization, define strict read/update boundaries, and reserve `DEEP_AUDIT` for explicit full-review requests or verified escalation needs.

Consequences: Multi-agent support remains intact while default initialization becomes significantly cheaper and more predictable. Deep inspection remains available when required.

Related files: `AGENTS.md`, `README.md`, `workflows/init-lite.md`, `memory-bank/model-routing.md`, `memory-bank/startup.md`, `memory-bank/systemPatterns.md`

### 2026-05-07 — Add optional fast validator mode for FAST_INIT workflows

Status: Accepted

Context: Full template validation is valuable for publish readiness but heavier than needed during routine low-token initialization workflows.

Decision: Add `--fast` mode to `scripts/check-template.py` that validates core startup/integration requirements, adapter pointers, context budgets, and required `.gitignore` patterns while skipping repository-wide secret hygiene scanning.

Consequences: Maintainers can run cheap validation during FAST_INIT-style work, while preserving full validation for release/publication checks.

Related files: `scripts/check-template.py`, `README.md`, `memory-bank/techContext.md`, `memory-bank/progress.md`, `memory-bank/activeContext.md`

### 2026-05-07 — Add one-command FAST_INIT bootstrap helper

Status: Accepted

Context: Even with improved policies, users still needed to run a command and manually copy a longer initialization prompt.

Decision: Add `scripts/init-fast.py` to run `check-template.py --fast` and print a concise ready-to-paste FAST_INIT prompt for new context windows.

Consequences: Fresh-start initialization is faster and easier, reducing user friction and accidental prompt drift.

Related files: `scripts/init-fast.py`, `README.md`, `scripts/README.md`, `memory-bank/techContext.md`, `memory-bank/progress.md`, `memory-bank/activeContext.md`

### 2026-05-07 — Initialize copied repository as template baseline before product specialization

Status: Accepted

Context: This repository was initialized from the master AI Agent Project Template and required Memory Bank grounding with accurate current facts.

Decision: Treat the current repository state as a template-baseline project (not yet product-specialized), update Memory Bank files with verified template facts, and keep unknown product-specific details as `TBD` until requirements are provided.

Consequences: Agents can work immediately with accurate operational context while avoiding invented product assumptions; next planning step must define actual product scope and stack.

Related files: `memory-bank/projectbrief.md`, `memory-bank/productContext.md`, `memory-bank/activeContext.md`, `memory-bank/progress.md`

### 2026-05-06 — Optimize startup context with lazy loading

Status: Accepted

Context: The initial `AGENTS.md` and Memory Bank startup files used too much context before agents reached project source files.

Decision: Keep `AGENTS.md` compact, add `memory-bank/startup.md`, and lazy-load all deeper docs, workflows, skills, and Memory Bank files only when relevant.

Consequences: First-start overhead is much smaller, preserving context for actual project code.

Related files: `AGENTS.md`, `memory-bank/startup.md`, `memory-bank/00-index.md`, `scripts/check-template.py`

### 2026-05-06 — Distill Karpathy-style engineering behavior into a small skill

Status: Accepted

Context: Karpathy-style guidance is useful but too verbose to embed in full startup context.

Decision: Put the four core principles in `AGENTS.md` and add `karpathy-engineer` as a concise optional skill for coding/debugging/refactoring.

Consequences: Agents get better engineering defaults without large prompt overhead.

Related files: `AGENTS.md`, `.cline/skills/karpathy-engineer/SKILL.md`, `.agents/skills/karpathy-engineer/SKILL.md`

### 2026-05-06 — Use AGENTS.md as canonical instruction file

Status: Accepted

Context: The previous template used `GEMINI.md` as the main command file and `ops/`, `resources/`, and `env/` as the primary structure.

Decision: Use `AGENTS.md` as the single model-agnostic instruction file. Keep `GEMINI.md`, `CLAUDE.md`, `.clinerules/`, and `.agents/rules/` as thin adapters.

Consequences: Cline, Google Antigravity, Gemini, Claude, Codex/OpenAI-style agents, and OpenRouter-backed workflows can share one consistent source of truth.

Related files: `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.clinerules/00-master.md`, `.agents/rules/00-master.md`

### 2026-05-06 — Replace legacy ops/resources/env structure

Status: Accepted

Context: The previous structure was useful but narrowly framed around Python resources, ops documents, and a committed `env/` folder.

Decision: Use `workflows/`, `scripts/`, `.mcp/`, `.env.example`, `.gitignore`, and `.clineignore` instead.

Consequences: The template is more conventional, stack-agnostic, safer for secrets, and easier for multiple coding agents to understand.

Related files: `workflows/`, `scripts/`, `.mcp/`, `.env.example`, `.gitignore`, `.clineignore`

## Decision template

### YYYY-MM-DD — Decision title

Status: Proposed / Accepted / Rejected / Superseded

Context:

Decision:

Consequences:

Related files:

### 2026-04-12 — Implement Defense-in-Depth Security

Status: Accepted

Context: Need to protect the platform from XSS, CSRF, and SQL injections, especially with user-generated content from Barangay representatives.

Decision: Implement 6 layers of security including CSP, HttpOnly/SameSite cookies, Bleach HTML sanitization, Jinja2 strict escaping, secure file uploads, and SQLAlchemy ORM parameterization.

Consequences: Highly secure platform; requires developers to use `sanitize` and `escape_strict` explicitly in templates.

Related files: `utils/security.py`, `SECURITY_IMPLEMENTATION.md` (Archived)

### 2026-04-15 — Mapbox Vector Tiles (MVT) for High Concurrency

Status: Accepted

Context: Leaflet with GeoJSON clusters struggled with performance when displaying large numbers of heritage locations to many concurrent users.

Decision: Transition to Mapbox GL JS and generate Vector Tiles using PostGIS `ST_AsMVT` dynamically, cached at the edge.

Consequences: Map load time reduced to <200ms. Requires PostGIS extension.

Related files: `utils/tile_generator.py`, `routes/api/map_routes.py`

### 2026-04-18 — Multi-Stop Route Optimization

Status: Accepted

Context: Tourists need an optimal path (TSP) for visiting multiple destinations.

Decision: Use OSRM public API to solve TSP. Since OSRM has a strict 1 req/sec rate limit, use Upstash Redis to aggressively cache identical tourist routes.

Consequences: Free, highly scalable routing, but requires Redis caching to avoid rate limit bans.

Related files: `ROUTING_NAVIGATION.md` (Archived)