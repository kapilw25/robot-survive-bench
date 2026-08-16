#!/usr/bin/env bash
# Step 2: TSR over the 10 tasks (behavioural only). Writes results JSONL.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="src:${PYTHONPATH:-}"
BRAIN="${1:-mock}"
SUITE="${2:-mock}"
python -m rsbench.loop.runner --brain "$BRAIN" --suite "$SUITE" --episodes 1 \
  --ood normal --out "data/results/${BRAIN}_tsr.jsonl"
