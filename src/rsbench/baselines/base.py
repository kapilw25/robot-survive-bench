"""Fixed robot-native reference policies (the world-model thesis yardstick).

pi0-FAST (VLA), V-JEPA-2-AC (LWM), DreamZero (WAM) are held FIXED while brains are swapped.
Unlike brains, these emit actions directly, so they wrap the env's low-level API, not SkillAPI.
Stubs: wire the real checkpoints for the v1 reproduction / as v2 baselines.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Policy(ABC):
    name: str = "abstract"
    family: str = "?"          # VLA | LWM | WAM
    is_open_weight: bool = True

    @abstractmethod
    def act(self, obs):
        """Return a low-level action for the env (not a SkillCall)."""


class Pi0Fast(Policy):
    name, family = "pi0-fast", "VLA"
    def act(self, obs):
        raise NotImplementedError("wire pi0-FAST (openpi DROID checkpoint)")


class VJepa2AC(Policy):
    name, family = "v-jepa-2-ac", "LWM"
    def act(self, obs):
        raise NotImplementedError("wire V-JEPA-2-AC image-goal MPC")


class DreamZero(Policy):
    name, family = "dreamzero", "WAM"
    def act(self, obs):
        raise NotImplementedError("wire DreamZero (native Franka/DROID)")
