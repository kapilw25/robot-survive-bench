from rsbench.brains.registry import get_brain
from rsbench.envs import make_env
from rsbench.loop.runner import run_episode, run_suite
from rsbench.metrics.scores import tsr_by_split
from rsbench.skills.api import SkillAPI


def test_mock_episode_succeeds_normal():
    brain, env = get_brain("mock"), make_env("mock")
    r = run_episode(brain, env, env.task_list()[0], SkillAPI.default(), "normal", seed=0)
    assert r.success is True and r.error is None


def test_mock_suite_all_splits_runs():
    results = run_suite("mock", "mock", episodes=2, oods=["normal", "transparent", "clutter"], seed=0, out=None)
    assert len(results) == 10 * 2 * 3
    by = tsr_by_split(results)
    # normal should be perfect; OOD should degrade (dTSR < 0), exercising step 4 end-to-end
    assert by["normal"] == 1.0
    assert by["transparent"] <= by["normal"]
