@echo off
setlocal enabledelayedexpansion
title Capacity Connect - Portal Launcher
cd /d "%~dp0"

echo ====================================================================
echo   CAPACITY CONNECT - Digital Capacity Building and LMS Portal
echo ====================================================================
echo.

:: 1. Detect Python executable (python or py)
set "PY_CMD="
python --version >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PY_CMD=python"
) else (
    py --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        set "PY_CMD=py"
    )
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python was not detected on this system.
    echo.
    echo To run Capacity Connect:
    echo 1. Download and install Python from: https://www.python.org/downloads/
    echo 2. During installation, make sure to CHECK "Add Python to PATH".
    echo 3. Once installed, double-click run.bat again.
    echo.
    pause
    exit /b 1
)

echo [OK] Using Python: %PY_CMD%
echo.

:: 2. Check if required libraries are installed
%PY_CMD% -c "import flask, flask_sqlalchemy, werkzeug" >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [SETUP] Installing required libraries -- one-time setup...
    %PY_CMD% -m pip install -r ..\requirements.txt
    if !ERRORLEVEL! NEQ 0 (
        echo [ERROR] Failed to install dependencies via pip.
        pause
        exit /b 1
    )
    echo [SETUP] Libraries installed successfully!
    echo.
)

:: 3. Check if database exists; if missing, auto-seed it
if not exist "capacity_connect.db" (
    echo [SETUP] Initializing database with demo data...
    %PY_CMD% seed_data.py
    echo [SETUP] Database initialized!
    echo.
)

:: 4. Launch browser automatically after 2 seconds
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:5000"

:: 5. Start the web server
echo ====================================================================
echo   Server is running at: http://127.0.0.1:5000
echo   Press Ctrl+C in this window to stop the server.
echo ====================================================================
echo.
%PY_CMD% app.py
pause
