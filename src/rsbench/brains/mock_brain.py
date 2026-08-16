"""MockBrain: emits the canonical plan so the mock loop succeeds with no external deps.

Lets steps 1-2 run today; under OOD the env may still slip, so dTSR is non-trivial.
"""
from __future__ import annotations

from rsbench.brains.base import Brain
from rsbench.skills.api import SkillAPI
from rsbench.types import Observation, SkillCall

_PLAN = [
    SkillCall("open", {"object": "drawer"}),
    SkillCall("pick", {"object": "apple"}),
    SkillCall("place", {"target": "drawer"}),
    SkillCall("done", {}),
]


class MockBrain(Brain):
    name = "mock"
    is_open_weight = True  # trivially "open"; used only for smoke tests

    def reset(self, task: str, skills: SkillAPI) -> None:
        super().reset(task, skills)
        self._i = 0

    def act(self, obs: Observation) -> SkillCall:
        call = _PLAN[min(self._i, len(_PLAN) - 1)]
        self._i += 1
        return call
