@echo off
setlocal

cd /d "%~dp0"

if not exist .env (
    if exist .env.example (
        copy .env.example .env
    )
)

if not exist frontend\node_modules (
    echo Installing frontend dependencies...
    cd frontend && call npm install && cd ..
)

set PYTHON_CMD=python
if exist .venv\Scripts\python.exe (
    set PYTHON_CMD=.venv\Scripts\python.exe
)

echo Starting backend and frontend servers...
start "Backend (FastAPI)" cmd /k "%PYTHON_CMD% -m uvicorn backend.app.main:app --port 8000 --reload"
start "Frontend (Next.js)" cmd /k "cd frontend && npm run dev"

echo Both servers launched in separate windows.
