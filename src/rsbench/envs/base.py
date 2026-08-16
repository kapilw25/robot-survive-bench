"""Env ABC: a closed-loop robot substrate the brain drives via SkillCalls."""
from __future__ import annotations

from abc import ABC, abstractmethod

from rsbench.types import Observation, SkillCall, StepResult


class Env(ABC):
    """LIBERO / mock / etc. implement this. Success is the only thing TSR reads."""

    @abstractmethod
    def task_list(self) -> list[str]:
        """The task ids in this suite (e.g. the 10 LIBERO-Long tasks)."""

    @abstractmethod
    def reset(self, task: str, ood: str = "normal", seed: int = 0) -> Observation:
        """Start a task; ood in {normal, transparent, clutter} applies the split (step 4)."""

    @abstractmethod
    def execute(self, call: SkillCall) -> StepResult:
        """Run one primitive in the loop and return the next observation + success flag."""

    def close(self) -> None:  # optional
        pass
