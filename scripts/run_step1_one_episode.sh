#!/usr/bin/env bash
# Step 1: one brain drives ONE episode via the fixed skill API; prints success/fail.
# Defaults to the mock brain+env (runs with zero external deps). Override with args:
#   scripts/run_step1_one_episode.sh gemini-er2 libero_long
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="src:${PYTHONPATH:-}"
BRAIN="${1:-mock}"
SUITE="${2:-mock}"
python -m rsbench.loop.runner --brain "$BRAIN" --suite "$SUITE" --episodes 1 --ood normal
