#!/usr/bin/env bash
# Eyeball the eval substrate: save a contact sheet of N LIBERO-Long episodes.
#   scripts/visualize_dataset.sh 5 data/ood/libero_long_samples.png
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="src:${PYTHONPATH:-}"
N="${1:-5}"
OUT="${2:-data/ood/libero_long_samples.png}"
python -m rsbench.utils.visualize --n "$N" --out "$OUT"
echo "Open $OUT to eyeball the samples. Or browse in-browser:"
echo "  https://huggingface.co/datasets/lerobot/libero_10_image  (Dataset Viewer tab)"
