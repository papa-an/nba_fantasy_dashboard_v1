@echo off
echo ========================================
echo Testing Backend Startup with Fix
echo ========================================
echo.

cd /d "%~dp0backend"

echo [1/2] Testing Python import...
"%~dp0.venv\Scripts\python.exe" -c "from dotenv import load_dotenv; load_dotenv(); from app.main import app; print('✓ Import successful')" 2>&1

if %errorlevel% neq 0 (
    echo ✗ Import failed! Check error above.
    pause
    exit /b 1
)

echo.
echo [2/2] Starting Backend Server...
echo Press Ctrl+C when you see "Application startup complete"
echo.

"%~dp0.venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
