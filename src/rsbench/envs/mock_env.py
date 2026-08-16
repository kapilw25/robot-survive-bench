"""A dependency-free MockEnv so steps 1-2 run before LIBERO / real APIs are wired.

Each task has a known-correct skill sequence; the env succeeds when the brain matches it.
The OOD flag (transparent/clutter) deterministically perturbs difficulty so dTSR (step 4)
is exercisable end-to-end with the mock brain. Replace with LiberoEnv for real runs.
"""
from __future__ import annotations

import random

from rsbench.envs.base import Env
from rsbench.types import Observation, SkillCall, StepResult

# task -> the correct ordered plan (the "solution")
_TASKS: dict[str, list[tuple[str, dict]]] = {
    f"libero_long_{i:02d}": [
        ("open", {"object": "drawer"}),
        ("pick", {"object": "apple"}),
        ("place", {"target": "drawer"}),
        ("done", {}),
    ]
    for i in range(1, 11)
}


class MockEnv(Env):
    """Deterministic toy substrate: matches the reference plan step-by-step."""

    def __init__(self, max_steps: int = 8) -> None:
        self.max_steps = max_steps

    def task_list(self) -> list[str]:
        return list(_TASKS)

    def reset(self, task: str, ood: str = "normal", seed: int = 0) -> Observation:
        if task not in _TASKS:
            raise KeyError(f"unknown task {task}; have {self.task_list()}")
        self._task = task
        self._plan = _TASKS[task]
        self._idx = 0
        self._ood = ood
        self._rng = random.Random(seed)
        # OOD deterministically injects a chance the executor "misreads" a step.
        self._slip = {"normal": 0.0, "transparent": 0.35, "clutter": 0.25}.get(ood, 0.0)
        return Observation(task=task, state_text=f"[{ood}] step 0; drawer closed, apple on table")

    def execute(self, call: SkillCall) -> StepResult:
        want_name, want_args = self._plan[self._idx]
        correct = call.name == want_name and all(call.args.get(k) == v for k, v in want_args.items())
        # under OOD, a correct call can still slip (models must be robust to the surprise)
        if correct and self._rng.random() < self._slip:
            correct = False
        if not correct:
            return StepResult(
                obs=Observation(task=self._task, state_text="misstep; task failed", step=self._idx),
                done=True, success=False, info={"expected": want_name},
            )
        self._idx += 1
        done = self._idx >= len(self._plan)
        return StepResult(
            obs=Observation(task=self._task, state_text=f"ok; {self._idx}/{len(self._plan)} done", step=self._idx),
            done=done, success=done, info={},
        )
