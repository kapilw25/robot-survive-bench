"""Shared data types passed between brain, skill API, and env (kept dependency-free)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SkillCall:
    """A single call the brain makes into the FIXED skill API (e.g. pick(obj))."""
    name: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass
class Observation:
    """What the brain sees each step. image may be None for text-only substrates."""
    task: str
    state_text: str = ""
    image: Any = None
    step: int = 0


@dataclass
class StepResult:
    """Result of executing one SkillCall in the env."""
    obs: Observation
    done: bool
    success: bool
    info: dict[str, Any] = field(default_factory=dict)


@dataclass
class EpisodeResult:
    """One closed-loop episode outcome (the unit TSR/dTSR are computed from)."""
    brain: str
    suite: str
    task: str
    success: bool
    steps: int
    ood: str = "normal"          # "normal" | "transparent" | "clutter"
    seed: int = 0
    error: str | None = None
    # --- extra behavioural signals (p2 5.2); default 0 => degrade to TSR-only ---
    subgoals_total: int = 0      # LHCR denominator (0 => count success as 1/1)
    subgoals_done: int = 0       # LHCR numerator: subgoals completed this episode
    failure_events: int = 0      # RSR denominator: perturbations / failures encountered
    recoveries: int = 0          # RSR numerator: failure events recovered from
    unsafe: bool = False         # SPR: episode violated a safety constraint
