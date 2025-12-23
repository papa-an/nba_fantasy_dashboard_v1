@echo off
echo Starting debug > d:\personal_project\nba_fantasy_dashboard_v1\start_debug.txt
echo Checking Python... >> d:\personal_project\nba_fantasy_dashboard_v1\start_debug.txt
d:\personal_project\nba_fantasy_dashboard_v1\.venv\Scripts\python.exe --version >> d:\personal_project\nba_fantasy_dashboard_v1\start_debug.txt 2>&1
if %errorlevel% neq 0 (
    echo Python from venv failed. Trying global python... >> d:\personal_project\nba_fantasy_dashboard_v1\start_debug.txt
    python --version >> d:\personal_project\nba_fantasy_dashboard_v1\start_debug.txt 2>&1
)

echo Checking NPM... >> d:\personal_project\nba_fantasy_dashboard_v1\start_debug.txt
call npm --version >> d:\personal_project\nba_fantasy_dashboard_v1\start_debug.txt 2>&1

echo Done. >> d:\personal_project\nba_fantasy_dashboard_v1\start_debug.txt
