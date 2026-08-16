"""Brain ABC: a contestant (frontier LLM or robot-specialized brain) that PLANS.

A brain never emits raw actions; it emits SkillCalls into the fixed SkillAPI. Concrete
brains live in this package (registry.py wires names -> factories). See plan/v2 roster.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from rsbench.skills.api import SkillAPI
from rsbench.types import Observation, SkillCall


class Brain(ABC):
    """Contract every contestant implements. Keep providers behind this interface."""

    #: display name used on the leaderboard
    name: str = "abstract"
    #: True = open weights (feeds the "open-weight only" board in step 5)
    is_open_weight: bool = False

    def reset(self, task: str, skills: SkillAPI) -> None:
        """Called once per episode with the task string and the frozen skill spec."""
        self._task = task
        self._skills = skills

    @abstractmethod
    def act(self, obs: Observation) -> SkillCall:
        """Return exactly one SkillCall for the current observation (closed loop)."""
        raise NotImplementedError
