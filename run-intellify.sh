#!/usr/bin/env bash
# run-intellify.sh — Linux / macOS launcher for Intellify Enterprise Hub
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  Intellify Enterprise Hub"
echo "============================================"
echo ""

# Guards
if [ ! -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    echo "[ERROR] .venv not found. Please run ./setup-intellify.sh first."
    exit 1
fi

if [ ! -d "$SCRIPT_DIR/dashboard/node_modules" ]; then
    echo "[ERROR] dashboard/node_modules missing. Please run ./setup-intellify.sh first."
    exit 1
fi

# Activate venv
# shellcheck disable=SC1091
source "$SCRIPT_DIR/.venv/bin/activate"

# ─────────────────────────────────────────────
# MCP Hub (port 8080)
# ─────────────────────────────────────────────
echo "Starting MCP Hub on http://localhost:8080 ..."
cd "$SCRIPT_DIR/core/mcp_hub"
python -m uvicorn server:app --host 0.0.0.0 --port 8080 --reload &
MCP_PID=$!
echo " - MCP Hub PID: $MCP_PID"

# Give hub a moment before the UI tries to connect
sleep 2

# ─────────────────────────────────────────────
# Dashboard (port 5175)
# ─────────────────────────────────────────────
echo "Starting Dashboard on http://localhost:5175 ..."
cd "$SCRIPT_DIR/dashboard"
npm run dev -- --host --port 5175 &
DASH_PID=$!
echo " - Dashboard PID: $DASH_PID"

cd "$SCRIPT_DIR"

echo ""
echo "============================================"
echo "  Intellify is running!"
echo "============================================"
echo "  MCP Hub API:  http://localhost:8080/docs"
echo "  Dashboard:    http://localhost:5175"
echo "============================================"
echo ""
echo "Press Ctrl+C to stop all services."

# Wait for both processes; Ctrl+C kills both
trap "echo 'Stopping...'; kill $MCP_PID $DASH_PID 2>/dev/null; exit 0" INT TERM
wait $MCP_PID $DASH_PID
