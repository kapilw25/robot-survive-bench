#!/usr/bin/env bash
# Create a venv, install rsbench (editable) + deps. Run once.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
echo "Done. Activate with: source .venv/bin/activate"
echo "Model API keys go in .env (see .env.example). LIBERO is optional until step 1 goes real."
