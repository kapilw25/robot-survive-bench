"""OOD splits (step 4): the observation-space shifts that stay zero-shot on DROID/Franka.

For real envs, apply_ood transforms the camera observation only (never the body/physics):
- transparent: swap target objects to glass/steel/water (non-Lambertian) renders/assets
- clutter: add distractors / occlusion around the target
MockEnv applies OOD internally; this module is the hook + contract for LiberoEnv.
"""
from __future__ import annotations

MODES = ("normal", "transparent", "clutter")


def apply_ood(obs, mode: str):
    """Transform an observation for the given OOD mode. Stub for real (image) envs."""
    if mode not in MODES:
        raise ValueError(f"unknown ood mode '{mode}'; allowed {MODES}")
    if mode == "normal":
        return obs
    # TODO: for LiberoEnv, apply the material swap (transparent) or add distractors (clutter)
    # to obs.image here. Observation-only, so the frozen policy/brain still runs zero-shot.
    return obs
