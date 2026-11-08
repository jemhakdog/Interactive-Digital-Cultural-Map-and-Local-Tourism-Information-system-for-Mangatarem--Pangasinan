#!/usr/bin/env bash
# Run backend (FastAPI :8000) + frontend (Next.js :3000) together. Ctrl-C stops both.
set -euo pipefail
cd "$(dirname "$0")"

[ -f .env ] || cp .env.example .env
[ -d frontend/node_modules ] || (cd frontend && npm install)

pids=()
trap 'kill "${pids[@]}" 2>/dev/null || true' EXIT INT TERM

.venv/bin/uvicorn backend.app.main:app --port 8000 --reload &
pids+=($!)
(cd frontend && npm run dev) &
pids+=($!)

wait
