---
name: meta-prompting
description: Executes tasks in two phases - Refining the user request into an expert prompt, and Executing it as that expert.
when_to_use: "When the user wants highly detailed, optimized, and expert-level answers using the Refiner-Executor pattern."
allowed-tools: Write, Read
---

# Meta-Prompting Skill (Refiner & Executor Pattern)

## Purpose
This skill transforms simple user requests into highly optimized, expert-level outputs by splitting the AI's processing into two distinct phases:
1. **The Refiner (Manager):** Analyzes the raw request and expands it into an extremely detailed instruction set (prompt) tailored for a domain-specific expert.
2. **The Executor (Worker):** Adopts the defined expert persona, follows all constraints, and executes the generated prompt to produce the final response.

---

## Workflow

### Step 1: The Refiner
When a request is received, analyze it and construct a `SELF-GENERATED PROMPT`. This prompt must define:
- **Persona:** The exact expert needed (e.g., Senior Systems Architect, Creative Copywriter, Principal Security Auditor).
- **Context & Scope:** Key details needed to make the solution complete.
- **Constraints:** Quality standards, formatting rules, anti-patterns to avoid.
- **Tone:** Professional, objective, and clear.

### Step 2: The Executor
Adopt the defined persona and execute the `SELF-GENERATED PROMPT` precisely.

---

## Response Format
Every response using this skill must follow this exact output structure:

```markdown
>>> SELF-GENERATED PROMPT:

[Insert the refined, expert-level prompt here]

>>> FINAL RESPONSE:

[Insert the expert execution and final solution here]
```
