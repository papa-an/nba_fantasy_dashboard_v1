Write-Host "NBA Fantasy Backend - Direct Start" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$projectRoot = "D:\personal_project\nba_fantasy_dashboard_v1"
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$backendDir = Join-Path $projectRoot "backend"

Write-Host ""
Write-Host "[1/3] Installing ALL dependencies..." -ForegroundColor Yellow
Set-Location $projectRoot
& $venvPython -m pip install -r backend\requirements.txt --quiet

Write-Host "[2/3] Verifying supabase is installed..." -ForegroundColor Yellow
$testImport = & $venvPython -c "import supabase; print('OK')" 2>&1
if ($testImport -match "OK") {
    Write-Host "✓ Supabase installed successfully" -ForegroundColor Green
}
else {
    Write-Host "✗ Installing supabase directly..." -ForegroundColor Red
    & $venvPython -m pip install supabase
}

Write-Host ""
Write-Host "[3/3] Starting Backend Server..." -ForegroundColor Green
Write-Host "Backend will run on: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

Set-Location $backendDir
& $venvPython -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
