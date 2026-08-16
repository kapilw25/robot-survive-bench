"""Env factory: suite name -> Env instance."""
from __future__ import annotations

from rsbench.envs.base import Env


def make_env(suite: str) -> Env:
    if suite == "mock":
        from rsbench.envs.mock_env import MockEnv
        return MockEnv()
    if suite in ("libero_long", "libero"):
        from rsbench.envs.libero_env import LiberoEnv
        return LiberoEnv()
    if suite in ("toy", "toy_visual"):
        from rsbench.envs.toy_visual_env import ToyVisualEnv
        return ToyVisualEnv()
    raise KeyError(f"unknown suite '{suite}'; use 'mock', 'toy', or 'libero_long'")
