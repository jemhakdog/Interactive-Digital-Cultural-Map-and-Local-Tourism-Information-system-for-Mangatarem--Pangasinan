# PLAN-dfd-intersections - Remove DFD Intersections

> **Goal:** Remodel the Level 1 DFD to eliminate ALL line intersections by duplicating entities and data stores where necessary.

## 1. Context Analysis
- **Current State:** The DFD contains multiple crossing lines (e.g., Tourist accessing multiple processes, centralized Data Stores with incoming/outgoing flows from distant nodes).
- **Constraint:** "Remove all intersections".
- **Allowed Helper:** "Create another copy of the block" (Duplication of External Entities and Data Stores).
- **Target File:** `docs/diagrams/dfd-level-1.drawio`.

## 2. Strategy: Decentralized Layout
To achieve zero intersections, we will move from a "Entity-Centric" layout to a "flow-centric" layout.

### A. Duplicate External Entities
Instead of one central "Tourist" node, we will place a local copy of the "Tourist" entity next to each process that interacts with it.
- **Tourist (Copy 1):** Near P3.0 (Map Display)
- **Tourist (Copy 2):** Near P4.0 (Content Discovery)
- **Tourist (Copy 3):** Near P6.0 (User Engagement)
- **Admin (Copy 1):** Near P5.0 (Admin Approval)
- **Admin (Copy 2):** Near P7.0 (Analytics)
- **Contributor (Copy 1):** Near P2.0 (Content Management)

### B. Duplicate Data Stores
Data stores accessed by multiple processes will be duplicated locally to avoid long traversing lines.
- **D1 USER:** Connect purely to P1.0 (and P2/P6 if needed locally).
- **D2 ATTRACTION:** Critical hub. Needs copies near P2.0 (Write), P3.0 (Read), P4.0 (Read/Search).
- **D5-D9 (Reviews/Events/etc):** Place immediately adjacent to their consuming processes (P6, P7).

### C. Vertical Layout Flow
Organize the diagram logically from top to bottom or left to right to ensure flow lines don't cross.
- **Top:** Authentication & Input (P1, P2)
- **Middle:** Processing & Admin (P5)
- **Bottom:** Consumption & Output (P3, P4, P6, P7)

## 3. Implementation Steps

### Step 1: Flatten the Graph
- Break the current rigid structure.
- Move P1-P7 into an intersection-free arrangement (likely a wide horizontal spread or separated vertical lanes).

### Step 2: Entity Duplication
- **[ACTION]** Create 3 copies of "Tourist / Public User".
- **[ACTION]** Create 2 copies of "System Administrator".
- **[ACTION]** Create 2 copies of "Barangay Contributor".
- *Note:* Use the standard DFD notation for duplicates (e.g., a diagonal slash in the corner or dashed border, if supported, otherwise exact visual copies).

### Step 3: Data Store Distribution
- **[ACTION]** Duplicate D2 (Attraction) for P2, P3, P4.
- **[ACTION]** Duplicate D3 (Event) for P2, P4.
- **[ACTION]** Duplicate D1, D4, D5, D6, D7, D8, D9 to be exclusively next to their connected processes.

### Step 4: Reconnect Edges
- Delete existing crossing edges.
- Draw short, direct, non-intersecting lines between the Process and its local Entity/Data Store copy.

## 4. Verification Checklist
- [ ] No lines cross each other.
- [ ] Every Process (P1-P7) has all its required inputs and outputs.
- [ ] All 9 Data Stores are present (duplicates allowed).
- [ ] All 5 External Entities are present (duplicates allowed).
- [ ] Labels are preserved ("Map Request", "Results", etc.).

## 5. Agent Assignment
- **Agent:** `orchestrator` (to manage the logic) or `project-planner` (for oversight).
- **Execution:** Can be performed by editing the XML structure of the `.drawio` file directly (complex) or providing instructions for the user. *Since I can edit the file, I will rewrite the XML.*

## 6. Questions for User (Socratic Gate)
1. **Verification:** Are you okay with the diagram becoming significantly "larger" or "wider" due to all the duplicated blocks?
2. **Notation:** Do you prefer a specific visual marker for duplicated blocks (e.g., an asterisk `*` in the label, like `Tourist *`)?
