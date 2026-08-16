"""Step 5: turn results JSONL into the two boards (all models / open-weight only)."""
from __future__ import annotations

import argparse
from pathlib import Path

from rsbench.brains.registry import REGISTRY
from rsbench.utils.io import read_jsonl


def _agg(rows: list[dict]) -> dict[str, dict]:
    """brain -> {tsr_normal, tsr_ood(min over ood splits), dtsr, n}."""
    per: dict[str, dict[str, list[bool]]] = {}
    for r in rows:
        per.setdefault(r["brain"], {}).setdefault(r.get("ood", "normal"), []).append(bool(r["success"]))
    out = {}
    for brain, splits in per.items():
        def rate(s):
            xs = splits.get(s, [])
            return sum(xs) / len(xs) if xs else float("nan")
        tsr_n = rate("normal")
        ood_splits = [s for s in splits if s != "normal"]
        tsr_o = min((rate(s) for s in ood_splits), default=float("nan"))
        out[brain] = {"tsr_normal": tsr_n, "tsr_ood": tsr_o,
                      "dtsr": (tsr_o - tsr_n) if ood_splits else float("nan"),
                      "n": sum(len(v) for v in splits.values())}
    return out


def _table(agg: dict[str, dict], open_only: bool) -> str:
    rows = sorted(agg.items(), key=lambda kv: (-(kv[1]["tsr_normal"] if kv[1]["tsr_normal"] == kv[1]["tsr_normal"] else -1)))
    head = "| rank | brain | open? | TSR(normal) | TSR(OOD) | dTSR |\n|---|---|---|---|---|---|"
    lines = [head]
    rank = 0
    for brain, m in rows:
        ow = getattr(REGISTRY.get(brain, object), "is_open_weight", None)
        if open_only and ow is not True:
            continue
        rank += 1
        lines.append(f"| {rank} | {brain} | {ow} | {m['tsr_normal']:.3f} | {m['tsr_ood']:.3f} | {m['dtsr']:.3f} |")
    return "\n".join(lines)


def build(results_path: str, out_dir: str = "boards") -> None:
    rows = read_jsonl(results_path)
    agg = _agg(rows)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    (Path(out_dir) / "board_all.md").write_text(
        "# RobotSurviveBench - all models\n\n" + _table(agg, open_only=False) + "\n", encoding="utf-8")
    (Path(out_dir) / "board_open_weight.md").write_text(
        "# RobotSurviveBench - open-weight only\n\n" + _table(agg, open_only=True) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="build the 2 leaderboards")
    ap.add_argument("--results", default="data/results/run.jsonl")
    ap.add_argument("--out", default="boards")
    args = ap.parse_args()
    build(args.results, args.out)


if __name__ == "__main__":
    main()
