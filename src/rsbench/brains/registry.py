"""name -> Brain factory. `get_brain("mock")` works today; providers need keys/SDKs."""
from __future__ import annotations

from rsbench.brains import providers as _p
from rsbench.brains.base import Brain
from rsbench.brains.mock_brain import MockBrain

REGISTRY: dict[str, type[Brain]] = {
    "mock": MockBrain,
    "gpt": _p.GPT,
    "claude": _p.Claude,
    "gemini": _p.Gemini,
    "gemini-er2": _p.GeminiER2,
    "glm": _p.GLM,
    "kimi": _p.Kimi,
    "qwen": _p.Qwen,
    "deepseek": _p.DeepSeek,
    "llama": _p.Llama,
    "cosmos-reason1": _p.CosmosReason1,
    "robobrain2": _p.RoboBrain2,
}


def get_brain(name: str) -> Brain:
    if name not in REGISTRY:
        raise KeyError(f"unknown brain '{name}'; available: {sorted(REGISTRY)}")
    return REGISTRY[name]()


def brain_names() -> list[str]:
    return sorted(REGISTRY)
