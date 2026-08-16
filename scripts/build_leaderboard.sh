#!/usr/bin/env bash
# Step 5: build the 2 boards (all / open-weight) + draft a social post from a results JSONL.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="src:${PYTHONPATH:-}"
RESULTS="${1:-data/results/swap_brains.jsonl}"
python -m rsbench.leaderboard.build --results "$RESULTS" --out boards
python -m rsbench.leaderboard.social --results "$RESULTS" | tee boards/social_draft.txt
echo "Boards in boards/  (board_all.md, board_open_weight.md, social_draft.txt)"
