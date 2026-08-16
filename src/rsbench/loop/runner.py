"""Closed-loop driver + CLI. Implements steps 1-4: run a brain through a suite/OOD, score.

Examples:
  python -m rsbench.loop.runner --brain mock --suite mock --episodes 1            # step 1
  python -m rsbench.loop.runner --brain mock --suite mock --ood all --out data/results/run.jsonl
"""
from __future__ import annotations

import argparse

from rsbench.brains.registry import get_brain
from rsbench.envs import make_env
from rsbench.envs.base import Env
from rsbench.metrics.scores import dtsr, tsr, tsr_by_split
from rsbench.skills.api import SkillAPI
from rsbench.types import EpisodeResult
from rsbench.utils.io import append_jsonl
from rsbench.utils.logging import get_logger
from rsbench.utils.seeding import set_seed

log = get_logger()


def _episode(brain, env, task, ood, seed, success, steps, step, error=None) -> EpisodeResult:
    """Assemble an EpisodeResult, pulling any behavioural annotations the env chose to emit
    on the terminal StepResult.info (subgoals / failure events / recoveries / safety)."""
    info = (step.info or {}) if step is not None else {}
    return EpisodeResult(
        brain.name, env.__class__.__name__, task, success, steps, ood, seed, error=error,
        subgoals_total=int(info.get("subgoals_total", 0)),
        subgoals_done=int(info.get("subgoals_done", 0)),
        failure_events=int(info.get("failure_events", 0)),
        recoveries=int(info.get("recoveries", 0)),
        unsafe=bool(info.get("unsafe", False)),
    )


def run_episode(brain, env: Env, task: str, skills: SkillAPI, ood: str, seed: int,
                max_steps: int = 20) -> EpisodeResult:
    set_seed(seed)
    step = None
    try:
        obs = env.reset(task, ood=ood, seed=seed)
        brain.reset(task, skills)
        for _ in range(max_steps):
            call = brain.act(obs)
            step = env.execute(call)
            obs = step.obs
            if step.done:
                return _episode(brain, env, task, ood, seed, step.success, obs.step, step)
        return _episode(brain, env, task, ood, seed, False, max_steps, step, error="max_steps")
    except Exception as exc:  # a crashed brain/env = a failed episode, logged
        return _episode(brain, env, task, ood, seed, False, 0, step,
                        error=f"{type(exc).__name__}: {exc}")


def run_suite(brain_name: str, suite: str, episodes: int, oods: list[str], seed: int,
              out: str | None, max_steps: int = 20) -> list[EpisodeResult]:
    brain = get_brain(brain_name)
    env = make_env(suite)
    skills = SkillAPI.default()
    results: list[EpisodeResult] = []
    for ood in oods:
        for task in env.task_list():
            for ep in range(episodes):
                r = run_episode(brain, env, task, skills, ood, seed + ep, max_steps=max_steps)
                results.append(r)
                if out:
                    append_jsonl(out, r)
                log.info("[%s|%s|%s] %s (%s)", brain_name, ood, task,
                         "SUCCESS" if r.success else "FAIL", r.error or "ok")
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description="rsbench closed-loop runner")
    ap.add_argument("--brain", default="mock")
    ap.add_argument("--suite", default="mock", help="mock | libero_long")
    ap.add_argument("--episodes", type=int, default=1)
    ap.add_argument("--ood", default="normal", help="normal | transparent | clutter | all")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None, help="results JSONL path")
    ap.add_argument("--max-steps", type=int, default=20, help="cap skill calls per episode")
    args = ap.parse_args()

    oods = list(("normal", "transparent", "clutter")) if args.ood == "all" else [args.ood]
    results = run_suite(args.brain, args.suite, args.episodes, oods, args.seed, args.out,
                        max_steps=args.max_steps)

    by_split = tsr_by_split(results)
    log.info("TSR overall = %.3f", tsr(results))
    for split, v in by_split.items():
        log.info("  TSR[%s] = %.3f", split, v)
    if "normal" in by_split:
        for split in ("transparent", "clutter"):
            if split in by_split:
                log.info("  dTSR[%s] = %.3f", split, dtsr(by_split[split], by_split["normal"]))


if __name__ == "__main__":
    main()
