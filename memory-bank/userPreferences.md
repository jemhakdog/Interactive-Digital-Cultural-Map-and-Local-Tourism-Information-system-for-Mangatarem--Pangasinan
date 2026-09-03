# User Preferences

This file acts as the `USER.md` system described in advanced agentic memory architectures. It stores the specific behavioral, formatting, and workflow preferences of the human user to ensure the agent aligns with their style without needing constant reminders in the prompt.

## Communication Style
- Tagalog/English mix common (e.g. "i have setted..."); respond clearly and simply.
- Prefers step-by-step, click-by-click guidance for unfamiliar tools (Vercel/Supabase) — avoid deep-dive jargon first, give exact button labels and copy-paste values.
- Likes to be told what to verify next.
- Not deeply familiar with Vercel, Google Cloud Console OAuth, or cloud deployment — assume limited infra background.

## Workflow Habits
- Works in this monorepo with `npm run dev` for local (both servers).
- Uses vercel CLI (authenticated) for deployment tasks when possible.
- Prefers dashboard/UI path when CLI is more complex.
- Wants little-no surprises: "verify things first before applying or making something".

## Formatting Preferences
- Keep changes minimal / surgical.
- Explains errors in plain terms with the actual fix steps.
- Prefers confirmation before actions that copy secrets or change credentials.

**Note to Agents**: Update this file when the user explicitly corrects your behavior or requests a persistent change in how you interact with them.
