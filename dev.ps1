param()

$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
}

if (-not (Test-Path "frontend/node_modules")) {
    Write-Host "Installing frontend dependencies..."
    Push-Location frontend
    npm install
    Pop-Location
}

$PythonCmd = "python"
if (Test-Path ".venv/Scripts/python.exe") {
    $PythonCmd = "$ProjectRoot\.venv\Scripts\python.exe"
}

Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$PythonCmd' -m uvicorn backend.app.main:app --port 8000 --reload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$ProjectRoot\frontend'; npm run dev"

Write-Host "Both servers launched."
