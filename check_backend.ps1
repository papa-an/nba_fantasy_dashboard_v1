Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "NBA Fantasy Backend - Dependency Check" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$venvPath = "D:\personal_project\nba_fantasy_dashboard_v1\.venv"
$pipPath = Join-Path $venvPath "Scripts\pip.exe"
$pythonPath = Join-Path $venvPath "Scripts\python.exe"

Write-Host "[1/4] Checking Python version..." -ForegroundColor Yellow
& $pythonPath --version

Write-Host ""
Write-Host "[2/4] Installing/Upgrading all backend requirements..." -ForegroundColor Yellow
& $pipPath install -r backend\requirements.txt --upgrade --quiet

Write-Host ""
Write-Host "[3/4] Verifying supabase package..." -ForegroundColor Yellow
$supabaseInstalled = & $pipPath show supabase 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ supabase package is installed" -ForegroundColor Green
    $supabaseInstalled | Select-String -Pattern "Version|Location"
}
else {
    Write-Host "✗ supabase package NOT found" -ForegroundColor Red
    Write-Host "Installing supabase explicitly..." -ForegroundColor Yellow
    & $pipPath install supabase --upgrade
}

Write-Host ""
Write-Host "[4/4] Testing backend import..." -ForegroundColor Yellow
$testResult = & $pythonPath -c "from dotenv import load_dotenv; load_dotenv(); from backend.app.main import app; print('SUCCESS')" 2>&1

if ($testResult -match "SUCCESS") {
    Write-Host "✓ Backend imports successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "All checks passed! Backend is ready." -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
}
else {
    Write-Host "✗ Import failed with error:" -ForegroundColor Red
    Write-Host $testResult -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
