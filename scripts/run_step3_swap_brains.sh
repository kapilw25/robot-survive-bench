#!/usr/bin/env bash
# Step 3: freeze the skill API, route every contestant through the IDENTICAL interface.
# Appends all brains' results to one JSONL for the leaderboard. Providers need API keys (.env).
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="src:${PYTHONPATH:-}"
SUITE="${1:-mock}"
OUT="data/results/swap_brains.jsonl"
: > "$OUT"
BRAINS="${BRAINS:-mock gemini-er2 gpt claude gemini glm kimi qwen deepseek llama cosmos-reason1 robobrain2}"
for b in $BRAINS; do
  echo "=== $b ==="
  python -m rsbench.loop.runner --brain "$b" --suite "$SUITE" --episodes 1 --ood normal --out "$OUT" || \
    echo "  ($b failed - likely missing API key/SDK; skipping)"
done
echo "Wrote $OUT"
