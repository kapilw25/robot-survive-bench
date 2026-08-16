"""Tiny JSONL read/write for per-episode results (append-only run logs)."""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any


def append_jsonl(path: str | Path, record: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if dataclasses.is_dataclass(record) and not isinstance(record, type):
        record = dataclasses.asdict(record)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path: str | Path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out
