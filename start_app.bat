@echo off
SETLOCAL EnableDelayedExpansion

:: Get the absolute path of the script directory
SET "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo ===================================================
echo NBA Fantasy Dashboard - Quick Start
echo ===================================================

:: 1. Check Python Environment
echo.
echo [1/3] Checking Backend Environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo No virtual environment found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r backend\requirements.txt
)

:: Ensure uvicorn is installed
echo Ensuring all dependencies are installed...
pip install -r backend\requirements.txt --quiet

:: 2. Start Backend
echo.
echo [2/3] Starting Backend Server...
start "NBA Backend (Port 8000)" cmd /k "cd /d "%SCRIPT_DIR%backend" && "%SCRIPT_DIR%.venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: 3. Start Frontend
echo.
echo [3/3] Starting Frontend Server...
start "NBA Frontend (Port 3000)" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo Servers are starting in new windows!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Please wait 10-15 seconds for them to fully load.
echo ===================================================
pause
