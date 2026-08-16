"""LLMBrain: shared prompt-build + response-parse for every frontier-LLM contestant.

Subclasses (providers.py) only implement _complete(prompt) -> str. The prompt (skill spec
+ observation + history) is IDENTICAL across providers - that is the "fixed interface" that
makes the swap-the-brain comparison fair (step 3).
"""
from __future__ import annotations

import re
from abc import abstractmethod

from rsbench.brains.base import Brain
from rsbench.skills.api import SkillAPI
from rsbench.types import Observation, SkillCall

_CALL_RE = re.compile(r"([a-zA-Z_]\w*)\s*\((.*?)\)", re.S)


class LLMBrain(Brain):
    """Turns model text into one SkillCall. Providers supply model_id + _complete()."""

    model_id: str = "unset"

    def reset(self, task: str, skills: SkillAPI) -> None:
        super().reset(task, skills)
        self._history: list[str] = []

    @abstractmethod
    def _complete(self, prompt: str, image=None) -> str:
        """Call the provider API (image optional, for multimodal brains) and return text; temp=0."""

    def _prompt(self, obs: Observation) -> str:
        return (
            f"You are the high-level brain of a robot arm. Task: {obs.task}\n"
            f"{self._skills.describe()}\n"
            f"Observation: {obs.state_text}\n"
            f"History: {' -> '.join(self._history) or '(none)'}\n"
            "Reply with EXACTLY one skill call, e.g. pick(object=apple). No prose."
        )

    def act(self, obs: Observation) -> SkillCall:
        text = self._complete(self._prompt(obs), image=obs.image)
        call = self._parse(text, spec=self._skills.skills)
        self._skills.validate(call)
        self._history.append(f"{call.name}({call.args})")
        return call

    @staticmethod
    def _parse(text: str, spec: dict[str, list[str]] | None = None) -> SkillCall:
        """Extract one SkillCall. Tolerates reasoning-style brains (GLM/Qwen/DeepSeek/Kimi):
        strip any <think>...</think>, prefer a call whose name is a known skill (the first such is
        the decision in a 'plan then act' reply), and map POSITIONAL args (move_to(plate)) onto the
        skill's expected parameter names as well as keyword args (move_to(target=plate))."""
        cleaned = re.sub(r"<think>.*?</think>", " ", text, flags=re.S | re.I)
        matches = list(_CALL_RE.finditer(cleaned))
        if spec:
            named = [m for m in matches if m.group(1) in spec]
            matches = named or matches
        if not matches:
            raise ValueError(f"could not parse a skill call from: {text!r}")
        m = matches[0]
        name, raw = m.group(1), m.group(2).strip()
        expected = (spec or {}).get(name, [])
        args: dict[str, str] = {}
        pos = 0
        for part in (raw.split(",") if raw else []):
            part = part.strip()
            if not part:
                continue
            if "=" in part:
                k, v = part.split("=", 1)
                args[k.strip()] = v.strip().strip("'\"")
            elif pos < len(expected):                 # positional -> next expected param
                args[expected[pos]] = part.strip("'\"")
                pos += 1
        return SkillCall(name=name, args=args)
