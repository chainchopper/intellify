@echo off
title Intellify Environment Setup
echo ============================================
echo   Intellify Enterprise Hub - Setup
echo ============================================

cd /d "%~dp0"

echo [1/3] Setting up Python Virtual Environment...
if not exist .venv (
    python -m venv .venv
    echo  - Created .venv
) else (
    echo  - .venv already exists
)

echo.
echo [2/3] Installing Backend Dependencies...
call .venv\Scripts\activate.bat
pip install -r core\mcp_hub\requirements.txt
pip install -r agents\requirements.txt
pip install -r requirements.txt
echo  - Backend setup complete.

echo.
echo [3/3] Installing Frontend Dependencies...
cd dashboard
call npm install
echo  - Frontend setup complete.

echo.
echo ============================================
echo   Setup Complete
echo ============================================
echo   Run "run-intellify.bat" to start the Hub.
pause
