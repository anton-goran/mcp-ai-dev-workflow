#!/bin/bash

# Setup script for MCP demo environment (alternative to uv)
# Run from repo root: ./scripts/dev.sh

set -e

echo "Setting up Python virtual environment..."

# Check Python version
python3 --version

# Create venv if not exists
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies from pyproject.toml (minimal runtime set)
pip install fastmcp "mcp[cli]" fastapi aioconsole anthropic

echo "Setup complete. Activate with: source .venv/bin/activate"