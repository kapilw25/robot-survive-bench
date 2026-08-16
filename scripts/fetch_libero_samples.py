"""Fetch ONE representative frame from each different-type LIBERO suite for the demo gallery.

Each LIBERO suite stresses a different kind of generalization (spatial layout, new objects,
new goals, long horizon), so one frame per suite gives 5 genuinely different sample types -
exactly what a frontier brain is scored against. Streams from HuggingFace LeRobot mirrors, so
it never downloads a whole dataset.

  python scripts/fetch_libero_samples.py
Writes:  docs/static/samples/<suite>.png  (+ gallery.png contact sheet)  and  docs/samples.json
Deps:    datasets, pillow  (already in .venv)
"""
from __future__ import annotations

import io
import json
from pathlib import Path

# (suite label, why-it-is-different, HF dataset).  The 4 canonical LIBERO suites.
SUITES = [
    ("LIBERO-Spatial", "same objects, new spatial arrangements", "lerobot/libero_spatial_image"),
    ("LIBERO-Object", "same layout, unseen objects", "lerobot/libero_object_image"),
    ("LIBERO-Goal", "same objects, new goal/instruction", "lerobot/libero_goal_image"),
    ("LIBERO-Long", "long-horizon, multi-stage tasks", "lerobot/libero_10_image"),
]
BACKFILL = ("LIBERO-Long", "a second, different long-horizon task", "lerobot/libero_10_image")
TARGET = 5
OUT_DIR = Path("docs/static/samples")
MANIFEST = Path("docs/samples.json")


def _find_image(row):
    from PIL import Image
    for k, v in row.items():
        if "image" not in k.lower():
            continue
        if isinstance(v, Image.Image):
            return v
        if isinstance(v, dict) and v.get("bytes"):
            return Image.open(io.BytesIO(v["bytes"]))
        if isinstance(v, dict) and v.get("path"):
            return Image.open(v["path"])
    return None


def _task_map(dataset: str) -> dict[int, str]:
    """Resolve task_index -> human instruction from LeRobot v3 meta/tasks.parquet.

    In v3 the parquet has a `task_index` column with the instruction string as the row index.
    """
    try:
        import pyarrow.parquet as pq
        from huggingface_hub import hf_hub_download
        path = hf_hub_download(dataset, "meta/tasks.parquet", repo_type="dataset")
        df = pq.read_table(path).to_pandas()          # index = task string, col = task_index
        return {int(idx): str(task) for task, idx in df["task_index"].items()}
    except Exception as exc:
        print(f"  (task map unavailable for {dataset}: {type(exc).__name__})")
        return {}


def _grab_tasks(dataset: str, k: int, skip_tasks: set[int]):
    """First frame for up to k distinct task_index values (excluding skip_tasks)."""
    from datasets import load_dataset
    tmap = _task_map(dataset)
    ds = load_dataset(dataset, split="train", streaming=True)
    seen: dict[int, dict] = {}
    for row in ds:
        ti = int(row.get("task_index", 0))
        if ti in seen or ti in skip_tasks:
            continue
        img = _find_image(row)
        if img is None:
            continue
        seen[ti] = {"img": img.convert("RGB"), "episode": int(row.get("episode_index", 0)),
                    "task": tmap.get(ti, f"task_index={ti}"), "task_index": ti}
        if len(seen) >= k:
            break
    return list(seen.values())


def _episode_gif(dataset: str, episode: int, out: Path,
                 max_frames: int = 28, stride: int = 6, size: int = 224) -> int:
    """Assemble one episode's frames into a small looping GIF (the closed-loop rollout)."""
    from datasets import load_dataset
    ds = load_dataset(dataset, split="train", streaming=True)
    frames = []
    i = 0
    for row in ds:
        ep = int(row.get("episode_index", 0))
        if ep < episode:
            continue
        if ep > episode:
            break
        if i % stride == 0:
            img = _find_image(row)
            if img is not None:
                frames.append(img.convert("RGB").resize((size, size)))
        i += 1
        if len(frames) >= max_frames:
            break
    if len(frames) < 2:
        return 0
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=90, loop=0, optimize=True)
    return len(frames)


def _record(picked: list, label: str, why: str, dataset: str, g: dict, fname: str) -> None:
    g["img"].resize((256, 256)).save(OUT_DIR / fname)
    entry = {"suite": label, "why": why, "dataset": dataset, "episode": g["episode"],
             "task": g["task"], "file": f"static/samples/{fname}"}
    gifname = fname[:-4] + ".gif"
    if _episode_gif(dataset, g["episode"], OUT_DIR / gifname):
        entry["gif"] = f"static/samples/{gifname}"
    picked.append(entry)
    print(f"ok  {label}: ep{g['episode']} :: {g['task'][:60]}" + ("  +gif" if "gif" in entry else ""))


def main() -> None:
    from PIL import Image, ImageDraw
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    picked = []
    used_long_tasks: set[int] = set()
    for label, why, dataset in SUITES:
        try:
            got = _grab_tasks(dataset, 1, set())
        except Exception as exc:
            print(f"skip {label} ({dataset}): {type(exc).__name__}: {str(exc)[:80]}")
            continue
        if not got:
            print(f"skip {label} ({dataset}): no image column")
            continue
        g = got[0]
        if "Long" in label:
            used_long_tasks.add(g["task_index"])
        _record(picked, label, why, dataset, g,
                f"{len(picked)+1}_{label.lower().replace('libero-', '')}.png")

    # backfill to TARGET with additional distinct tasks (default: more LIBERO-Long tasks)
    if len(picked) < TARGET:
        label, why, dataset = BACKFILL
        for g in _grab_tasks(dataset, TARGET - len(picked), used_long_tasks):
            _record(picked, label, why, dataset, g, f"{len(picked)+1}_long{g['task_index']}.png")

    if not picked:
        raise SystemExit("no suites loaded - check network / dataset names")

    # combined contact sheet
    tw, cap = 256, 34
    sheet = Image.new("RGB", (tw * len(picked), 256 + cap), "white")
    d = ImageDraw.Draw(sheet)
    for i, p in enumerate(picked):
        sheet.paste(Image.open(OUT_DIR / Path(p["file"]).name), (i * tw, cap))
        d.text((i * tw + 3, 3), p["suite"], fill="black")
        d.text((i * tw + 3, 17), p["task"][:40], fill="#555")
    sheet.save(OUT_DIR / "gallery.png")

    MANIFEST.write_text(json.dumps(picked, indent=2))
    print(f"\nwrote {len(picked)} samples -> {OUT_DIR}/ and manifest -> {MANIFEST}")


if __name__ == "__main__":
    main()
