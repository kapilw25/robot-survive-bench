#!/usr/bin/env bash
# Step 4: run normal + transparent + clutter; report dTSR = TSR(OOD) - TSR(normal).
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="src:${PYTHONPATH:-}"
BRAIN="${1:-mock}"
SUITE="${2:-mock}"
python -m rsbench.loop.runner --brain "$BRAIN" --suite "$SUITE" --episodes 3 \
  --ood all --out "data/results/${BRAIN}_ood.jsonl"
