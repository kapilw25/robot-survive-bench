"""Save a contact sheet of N LIBERO-Long episodes so you can eyeball the eval substrate.

This renders what a frontier brain is scored against: the agent-view RGB frame + the task
instruction, one per episode. Streams from a LeRobot LIBERO-10 dataset on HuggingFace, so it
does not download the whole thing.

Usage:
  python -m rsbench.utils.visualize --n 5 --out data/ood/libero_long_samples.png
Deps: pip install datasets pillow
"""
from __future__ import annotations

import argparse
import io
from pathlib import Path


def _find_image(row):
    from PIL import Image  # type: ignore
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


def _find_task(row):
    for k in ("task", "language_instruction", "language", "instruction"):
        if isinstance(row.get(k), str):
            return row[k]
    return f"task_index={row.get('task_index', '?')}"


def make_sheet(dataset: str, n: int, out: str) -> None:
    from datasets import load_dataset  # type: ignore
    from PIL import Image, ImageDraw  # type: ignore

    ds = load_dataset(dataset, split="train", streaming=True)
    picked: dict = {}
    for row in ds:
        ep = row.get("episode_index", len(picked))
        if ep in picked:
            continue
        img = _find_image(row)
        if img is None:
            continue
        picked[ep] = (img.convert("RGB"), _find_task(row))
        if len(picked) >= n:
            break
    if not picked:
        raise SystemExit(f"no image column found in {dataset}; inspect the schema")

    tw, cap_h = 256, 22
    thumbs = []
    for ep, (img, task) in picked.items():
        w, h = img.size
        thumbs.append((img.resize((tw, int(h * tw / w))), f"ep{ep}: {task[:44]}"))
    height = max(t.size[1] for t, _ in thumbs) + cap_h
    sheet = Image.new("RGB", (tw * len(thumbs), height), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (t, cap) in enumerate(thumbs):
        sheet.paste(t, (i * tw, cap_h))
        draw.text((i * tw + 3, 5), cap, fill="black")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"wrote {out} ({len(picked)} samples)")
    for ep, (_, task) in picked.items():
        print(f"  ep{ep}: {task}")


def make_gif(dataset: str, episode: int, out: str, fps: int = 15, stride: int = 2,
             max_frames: int = 160) -> None:
    """Assemble ONE full episode's frames into an animated GIF (the closed-loop rollout)."""
    from datasets import load_dataset  # type: ignore

    ds = load_dataset(dataset, split="train", streaming=True)
    frames, target, task, i = [], None, None, 0
    for row in ds:
        ep = row.get("episode_index", 0)
        if target is None and (episode is None or ep == episode):
            target = ep
        if target is None:
            continue
        if ep != target:
            break                         # episode finished
        if task is None:
            task = _find_task(row)
        if i % stride == 0:
            img = _find_image(row)
            if img is not None:
                frames.append(img.convert("RGB").resize((256, 256)))
        i += 1
        if len(frames) >= max_frames:
            break
    if not frames:
        raise SystemExit(f"no frames found for episode {episode} in {dataset}")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=int(1000 / fps), loop=0, optimize=True)
    print(f"wrote {out} (episode {target}, {len(frames)} frames @ {fps}fps, task {task})")


def main() -> None:
    ap = argparse.ArgumentParser(description="visualize LIBERO-Long: contact sheet or episode GIF")
    ap.add_argument("--dataset", default="lerobot/libero_10_image", help="a LeRobot LIBERO-10 dataset")
    ap.add_argument("--n", type=int, default=5, help="sheet: number of episodes")
    ap.add_argument("--out", default="data/ood/libero_long_samples.png")
    ap.add_argument("--gif", default=None, help="GIF output path (switches to gif mode)")
    ap.add_argument("--episode", type=int, default=0, help="gif: which episode")
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--stride", type=int, default=2, help="gif: keep every Nth frame")
    a = ap.parse_args()
    if a.gif:
        make_gif(a.dataset, a.episode, a.gif, a.fps, a.stride)
    else:
        make_sheet(a.dataset, a.n, a.out)


if __name__ == "__main__":
    main()
