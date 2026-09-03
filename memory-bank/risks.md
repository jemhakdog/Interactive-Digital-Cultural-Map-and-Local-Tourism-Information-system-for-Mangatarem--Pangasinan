# Risks

## High-risk areas

- Tool-specific rules drifting away from `AGENTS.md`.
- Adding project-specific stack assumptions to the base template.

## Security-sensitive areas

- `.env` and provider API keys — **a real Supabase DB password was shared in chat this session; advise the user to rotate it** (Supabase → Settings → Database → Reset password). Vercel env vars are encrypted at rest, but the chat copy is public to the conversation.
- Google OAuth client `794547070676-80dbt1j3a724hacci5684s7b7v93j1fh` — client ID is public by design; the allowlist currently has localhost + stale `gomangatarem.vercel.app` origins.
- Vercel env `SECRET_KEY` (production) — set; do not commit to repo.
- Public GitHub repo — `.env` must remain gitignored (it is); do not commit `.vercel/` (now gitignored). Anyway, secrets in chat should be rotated.
- MCP server configs & provider tokens.

## Performance / reliability (deployment)

- **Serverless cold starts + Postgres connections**: Supabase transaction pooler :6543 mitigates pool exhaustion; keep using 6543, not 5432.
- **Ephemeral uploads** on Vercel: uploaded images disappear after instance recycle. Accepted for capstone demo; production needs object storage (Supabase Storage/Cloudflare R2/S3). See `docs/VERCEL_ARCH_DECISION.md`.
- **`init_db()` runs only in development**: production tables are NOT auto-created; a one-time seed/migration is required before first real login. No Alembic yet.
- **Google OAuth allowlist** — resolved (short public frontend URL added; login confirmed working). Keep the allowlist in mind if the frontend domain ever changes.
- **Supabase pooler + asyncpg prepared statements** — fixed via `statement_cache_size=0`; if deploying to a different Postgres host, revisit.
- Frontend `NEXT_PUBLIC_API_URL` not persisted as project env (only `--build-env` at deploy); a future bare push deploy would bake `http://localhost:8000`. Add it as a project env var.

## Migration risks

- The 2026-09-01 Flask→FastAPI migration: completed (86→13 tests ported). No known active migration risk for the deployed stack.
- Any future schema change needs a real migration path (Alembic) rather than `create_all()`.