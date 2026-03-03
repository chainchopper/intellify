#!/usr/bin/env bash
# setup-intellify.sh — Linux / macOS setup for Intellify Enterprise Hub
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  Intellify Enterprise Hub - Setup"
echo "============================================"
echo ""

# ─────────────────────────────────────────────
# [1/3] Python virtual environment
# ─────────────────────────────────────────────
echo "[1/3] Setting up Python Virtual Environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo " - Created .venv"
else
    echo " - .venv already exists, skipping."
fi

# Activate
# shellcheck disable=SC1091
source "$SCRIPT_DIR/.venv/bin/activate"

# ─────────────────────────────────────────────
# [2/3] Python dependencies
# ─────────────────────────────────────────────
echo ""
echo "[2/3] Installing Python Dependencies..."
pip install --upgrade pip --quiet
pip install -r "$SCRIPT_DIR/core/mcp_hub/requirements.txt"
pip install -r "$SCRIPT_DIR/agents/requirements.txt"
pip install -r "$SCRIPT_DIR/requirements.txt"
echo " - Python dependencies installed."

# ─────────────────────────────────────────────
# [3/3] Dashboard (Node / npm)
# ─────────────────────────────────────────────
echo ""
echo "[3/3] Installing Dashboard Dependencies..."
if ! command -v npm &>/dev/null; then
    echo "[ERROR] npm not found. Install Node.js 18+ from https://nodejs.org"
    exit 1
fi
cd "$SCRIPT_DIR/dashboard"
npm install
cd "$SCRIPT_DIR"
echo " - Dashboard dependencies installed."

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo "  Run ./run-intellify.sh to launch."
echo "============================================"
