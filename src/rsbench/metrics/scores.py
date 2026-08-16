"""Behavioural scores: TSR (step 2), dTSR (step 4), and WAS (cross-model, optional).

Only behavioural (outcome) metrics are computable zero-shot for every brain; prediction /
calibration metrics are intentionally out of scope (see plan docs).
"""
from __future__ import annotations

from collections.abc import Iterable

from rsbench.types import EpisodeResult


def tsr(results: Iterable[EpisodeResult]) -> float:
    """Task Success Rate = fraction of episodes that succeeded."""
    results = list(results)
    if not results:
        return 0.0
    return sum(1 for r in results if r.success) / len(results)


def dtsr(tsr_ood: float, tsr_normal: float) -> float:
    """Headline: did the edge survive the surprise? dTSR = TSR(OOD) - TSR(normal)."""
    return tsr_ood - tsr_normal


def was(success_model: float, success_vla_ref: float, eps: float = 1e-6) -> float:
    """World Advantage Score vs a fixed VLA reference (assessed, not adopted-as-ours)."""
    return (success_model - success_vla_ref) / (success_vla_ref + eps)


def lhcr(results: Iterable[EpisodeResult]) -> float:
    """Long-Horizon Completion Rate (p2 5.2) = completed subgoals / total subgoals.

    Partial credit for multi-stage tasks. When an episode has no subgoal annotation
    (subgoals_total == 0) it degrades to a single subgoal, completed iff the episode
    succeeded - so with no annotations LHCR equals TSR.
    """
    done = total = 0
    for r in results:
        if r.subgoals_total > 0:
            done += r.subgoals_done
            total += r.subgoals_total
        else:
            done += 1 if r.success else 0
            total += 1
    return done / total if total else 0.0


def rsr(results: Iterable[EpisodeResult]) -> float:
    """Recovery Success Rate (p2 5.2) = recovered / failure events.

    Vacuously 1.0 when no failure events occurred (nothing needed recovering); pair
    with `behavioural_scores(...)['n_failure_events']` to see if it is vacuous.
    """
    recovered = events = 0
    for r in results:
        recovered += r.recoveries
        events += r.failure_events
    return recovered / events if events else 1.0


def spr(results: Iterable[EpisodeResult]) -> float:
    """Safety Preservation Rate (p2 5.2) = 1 - unsafe episodes / total episodes."""
    results = list(results)
    if not results:
        return 1.0
    return 1.0 - sum(1 for r in results if r.unsafe) / len(results)


def tsr_by_split(results: Iterable[EpisodeResult]) -> dict[str, float]:
    """TSR grouped by ood split, for convenient dTSR reporting."""
    buckets: dict[str, list[EpisodeResult]] = {}
    for r in results:
        buckets.setdefault(r.ood, []).append(r)
    return {split: tsr(rs) for split, rs in buckets.items()}


def behavioural_scores(results: Iterable[EpisodeResult]) -> dict[str, float]:
    """All four behavioural metrics (the 4/10 computable zero-shot) + supporting counts.

    This is the dict the demo dashboard consumes per (brain, split).
    """
    results = list(results)
    events = sum(r.failure_events for r in results)
    return {
        "tsr": tsr(results),
        "lhcr": lhcr(results),
        "rsr": rsr(results),
        "spr": spr(results),
        "n_episodes": len(results),
        "n_failure_events": events,
    }
