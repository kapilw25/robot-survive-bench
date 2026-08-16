"""Minimal YAML config loader (falls back gracefully if pyyaml is absent)."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def load_yaml(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # keep import-safe; tell the user how to fix
        raise ImportError("pyyaml is required to read configs: pip install pyyaml") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
