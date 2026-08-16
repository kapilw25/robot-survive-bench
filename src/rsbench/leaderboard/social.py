"""Step 5: auto-draft a short social post from a freshly built board (never auto-posts)."""
from __future__ import annotations

import argparse

from rsbench.leaderboard.build import _agg
from rsbench.utils.io import read_jsonl


def draft(results_path: str, model: str | None = None) -> str:
    agg = _agg(read_jsonl(results_path))
    if not agg:
        return "No results yet."
    top = max(agg.items(), key=lambda kv: (kv[1]["tsr_normal"] if kv[1]["tsr_normal"] == kv[1]["tsr_normal"] else -1))
    name, m = top
    focus = model if (model and model in agg) else name
    fm = agg[focus]
    return (
        f"New on RobotSurviveBench: {focus} scores TSR {fm['tsr_normal']:.0%} on LIBERO-Long, "
        f"but its edge drops {abs(fm['dtsr']):.0%} under the OOD surprise (dTSR {fm['dtsr']:+.0%}). "
        f"Current top brain: {name} ({m['tsr_normal']:.0%}). Does the world-model advantage survive? "
        f"Leaderboard + how to add your model: <repo-url>  #robotics #VLA #worldmodels"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="draft a social post from results")
    ap.add_argument("--results", default="data/results/run.jsonl")
    ap.add_argument("--model", default=None, help="highlight this brain")
    print(draft(ap.parse_args().results, ap.parse_args().model))


if __name__ == "__main__":
    main()
