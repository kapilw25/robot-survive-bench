# docs/ - RobotSurviveBench demo dashboard

A single self-contained page that explains the benchmark at a glance: the **dataset** a brain is
scored against, the **10-metric suite** (with the 4 that are computable zero-shot), and the
**model roster** with live scores. Built from repo data, so it is always current.

## View it

| 🖥️ Mode | ⌨️ Command | 🌐 Opens | 📝 Notes |
|---|---|---|---|
| 📄 Static | `make dashboard` | `docs/index.html` (open in a browser, or GitHub Pages from `docs/`) | zero web deps; a snapshot of current data |
| 🔴 Live | `make serve` (needs `pip install flask`) | `http://127.0.0.1:5000` | re-reads roster + `data/results/*.jsonl` on every request |

`file://` may be blocked by some browsers/extensions; if so run `python -m http.server -d docs` and open `http://127.0.0.1:8000`.

## What each section shows

| 🧩 Section | 🗂️ Source | 📋 Content |
|---|---|---|
| 🖼️ 1 Dataset | `docs/samples.json` (+ `static/samples/*.png`) | 5 different-type LIBERO frames (Spatial / Object / Goal / Long x2), the real instruction, and why each suite is different |
| 📏 2 Metrics | `docs/dashboard.py` (`METRICS`), verbatim from proposal p2 5.2-5.6 | all 10 metrics; the 4 behavioural ones marked `scored` (the rest need a prediction/probability head -> `N/A` for action-only brains); `dTSR` / `WAS` as derived headlines |
| 🤖 3 Models | `rsbench.brains.registry` + `data/results/*.jsonl` | roster (open/closed, wired vs stub, key set?) with TSR / dTSR / LHCR / RSR / SPR / WAS where results exist, else `pending` |

## Regenerate the pieces

```bash
make samples      # re-fetch the 5 LIBERO sample frames (streams from HF; needs HF_HOME writable)
make dashboard    # rebuild docs/index.html from current registry + results
```

## Add a model's scores

1. Wire its `_complete()` in `src/rsbench/brains/providers.py` and set the API key in `.env`.
2. Run it: `PYTHONPATH=src python -m rsbench.loop.runner --brain <name> --suite toy --ood all --out data/results/<name>.jsonl`.
3. `make dashboard` - the new row fills in automatically.
