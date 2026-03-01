@echo off
title Intellify Enterprise Hub
echo Starting Intellify Hybrid Orchestrator and Dashboard...

cd /d "%~dp0"

:: Check if .venv exists
if not exist .venv (
    echo [ERROR] .venv not found! Please run setup-intellify.bat first.
    pause
    exit /b
)

:: Start Python MCP Orchestrator Hub
start "Intellify MCP Hub" cmd /k "cd /d "%~dp0core\mcp_hub" ^&^& ..\..\.venv\Scripts\python -m uvicorn server:app --host 0.0.0.0 --port 8080 --reload"

:: Start Dashboard
start "Intellify Dashboard" cmd /k "cd /d "%~dp0dashboard" ^&^& npm run dev -- --host --port 5175"

echo.
echo ============================================
echo   Intellify Started
echo ============================================
echo   MCP Hub:      http://localhost:8080/docs
echo   Dashboard:    http://localhost:5175
echo ============================================
echo.
pause
