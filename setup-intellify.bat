@echo off
setlocal enabledelayedexpansion
title Intellify Enterprise Hub - Setup
echo ============================================
echo   Intellify Enterprise Hub - Setup
echo ============================================
echo.

:: Always work from the directory this .bat lives in
cd /d "%~dp0"

:: ─────────────────────────────────────────────
:: [1/3] Python virtual environment
:: ─────────────────────────────────────────────
echo [1/3] Setting up Python Virtual Environment...
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] python not found. Please install Python 3.10+ and add it to PATH.
        pause & exit /b 1
    )
    echo  - Created .venv
) else (
    echo  - .venv already exists, skipping creation.
)

:: Activate venv
call "%~dp0.venv\Scripts\activate.bat"

:: ─────────────────────────────────────────────
:: [2/3] Python dependencies
:: ─────────────────────────────────────────────
echo.
echo [2/3] Installing Python Dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r "%~dp0core\mcp_hub\requirements.txt"
pip install -r "%~dp0agents\requirements.txt"
pip install -r "%~dp0requirements.txt"
echo  - Python dependencies installed.

:: ─────────────────────────────────────────────
:: [3/3] Dashboard (Node/npm)
:: ─────────────────────────────────────────────
echo.
echo [3/3] Installing Dashboard Dependencies...
cd /d "%~dp0dashboard"
where npm >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm not found. Please install Node.js 18+ from https://nodejs.org
    pause & exit /b 1
)
call npm install
echo  - Dashboard dependencies installed.

:: Back to root
cd /d "%~dp0"

echo.
echo ============================================
echo   Setup Complete!
echo ============================================
echo   Run run-intellify.bat to launch.
echo ============================================
pause
