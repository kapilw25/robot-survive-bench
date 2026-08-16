from rsbench.metrics.scores import (
    behavioural_scores,
    dtsr,
    lhcr,
    rsr,
    spr,
    tsr,
    tsr_by_split,
    was,
)
from rsbench.types import EpisodeResult


def _r(success, ood="normal", **kw):
    return EpisodeResult("mock", "MockEnv", "t", success, 1, ood, **kw)


def test_tsr():
    assert tsr([_r(True), _r(False), _r(True), _r(True)]) == 0.75
    assert tsr([]) == 0.0


def test_dtsr():
    assert dtsr(0.4, 0.9) == -0.5


def test_was():
    assert was(0.8, 0.4) == (0.8 - 0.4) / (0.4 + 1e-6)


def test_tsr_by_split():
    rows = [_r(True, "normal"), _r(False, "normal"), _r(False, "clutter")]
    by = tsr_by_split(rows)
    assert by["normal"] == 0.5 and by["clutter"] == 0.0


def test_lhcr_from_subgoals():
    rows = [_r(False, subgoals_total=4, subgoals_done=3),
            _r(True, subgoals_total=2, subgoals_done=2)]
    assert lhcr(rows) == (3 + 2) / (4 + 2)


def test_lhcr_degrades_to_tsr_without_annotations():
    rows = [_r(True), _r(False), _r(True), _r(True)]
    assert lhcr(rows) == tsr(rows) == 0.75


def test_rsr():
    rows = [_r(True, failure_events=2, recoveries=1), _r(False, failure_events=2, recoveries=1)]
    assert rsr(rows) == 2 / 4
    assert rsr([_r(True), _r(True)]) == 1.0          # vacuous: no failure events


def test_spr():
    assert spr([_r(True), _r(True, unsafe=True), _r(False), _r(True)]) == 1.0 - 1 / 4
    assert spr([]) == 1.0


def test_behavioural_scores_bundle():
    rows = [_r(True, failure_events=1, recoveries=1), _r(False, unsafe=True)]
    b = behavioural_scores(rows)
    assert set(b) == {"tsr", "lhcr", "rsr", "spr", "n_episodes", "n_failure_events"}
    assert b["tsr"] == 0.5 and b["n_episodes"] == 2 and b["n_failure_events"] == 1
