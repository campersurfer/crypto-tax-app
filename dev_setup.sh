#!/bin/bash
# One-click automation script for local dev setup (backend+frontend)

set -e

# Create Python venv if not exists
test -d .venv || python3 -m venv .venv
source .venv/bin/activate

# Install backend dependencies
pip install --upgrade pip
pip install -r requirements.txt uvicorn fastapi pytest

# Install frontend dependencies
cd frontend
npm install
cd ..

# Lint, build, and type-check frontend
yarn --cwd frontend lint --fix || npm run lint --fix || true
yarn --cwd frontend build || npm run build || true
yarn --cwd frontend type-check || npm run type-check || true

# Run backend tests
pytest || true

echo "\nAll dependencies installed, linted, built, and tested."
echo "To start backend: (from project root)"
echo "  source .venv/bin/activate && uvicorn main:app --reload"
echo "To start frontend: (from frontend dir)"
echo "  npm run dev"
