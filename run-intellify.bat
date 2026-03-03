@echo off
setlocal enabledelayedexpansion
title Intellify Enterprise Hub
cd /d "%~dp0"

echo ============================================
echo   Intellify Enterprise Hub
echo ============================================
echo.

:: Guard: venv must exist
if not exist "%~dp0.venv\Scripts\activate.bat" (
    echo [ERROR] .venv not found. Please run setup-intellify.bat first.
    pause & exit /b 1
)

:: Guard: dashboard deps must exist
if not exist "%~dp0dashboard\node_modules" (
    echo [ERROR] Dashboard node_modules missing. Please run setup-intellify.bat first.
    pause & exit /b 1
)

:: ─────────────────────────────────────────────
:: Start MCP Hub (FastAPI / uvicorn on port 8080)
:: ─────────────────────────────────────────────
echo Starting MCP Hub on http://localhost:8080 ...
start "Intellify MCP Hub" cmd /k ^
    "cd /d "%~dp0core\mcp_hub" && "%~dp0.venv\Scripts\python.exe" -m uvicorn server:app --host 0.0.0.0 --port 8080 --reload"

:: Brief pause so the hub has a head start before the UI tries to talk to it
timeout /t 3 /nobreak >nul

:: ─────────────────────────────────────────────
:: Start Dashboard (Vite dev server on port 5175)
:: ─────────────────────────────────────────────
echo Starting Dashboard on http://localhost:5175 ...
start "Intellify Dashboard" cmd /k ^
    "cd /d "%~dp0dashboard" && npm run dev -- --host --port 5175"

echo.
echo ============================================
echo   Intellify is running!
echo ============================================
echo   MCP Hub API:  http://localhost:8080/docs
echo   Dashboard:    http://localhost:5175
echo ============================================
echo.
echo Both services launched in separate windows.
echo Close those windows to stop the services.
echo.
pause
