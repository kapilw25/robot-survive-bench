import pytest

from rsbench.skills.api import SkillAPI
from rsbench.types import SkillCall


def test_validate_ok():
    api = SkillAPI.default()
    api.validate(SkillCall("pick", {"object": "apple"}))


def test_validate_unknown_skill():
    api = SkillAPI.default()
    with pytest.raises(ValueError):
        api.validate(SkillCall("teleport", {}))


def test_validate_missing_arg():
    api = SkillAPI.default()
    with pytest.raises(ValueError):
        api.validate(SkillCall("pick", {}))


def test_describe_lists_skills():
    text = SkillAPI.default().describe()
    assert "pick(object)" in text and "done(" in text
