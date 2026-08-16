"""The FIXED skill / primitive API - the one interface EVERY brain plans through.

This is the contract that must stay identical across all contestants (step 3): swapping
the brain must never change the executor. Skills are loaded from configs/skills.yaml so the
contract is versioned and auditable.
"""
from __future__ import annotations

from dataclasses import dataclass

from rsbench.types import SkillCall

# Default primitive set; keep in sync with configs/skills.yaml.
DEFAULT_SKILLS: dict[str, list[str]] = {
    "move_to": ["target"],       # move end-effector above a named object / pose
    "pick": ["object"],          # close gripper on a named object
    "place": ["target"],         # open gripper over a named target
    "open": ["object"],          # open an articulated object (drawer/door)
    "close": ["object"],         # close an articulated object
    "done": [],                  # declare the task complete
}


@dataclass
class SkillAPI:
    """Validates brain output against the frozen skill schema and renders the prompt spec."""
    skills: dict[str, list[str]]

    @classmethod
    def default(cls) -> "SkillAPI":
        return cls(skills=dict(DEFAULT_SKILLS))

    def names(self) -> list[str]:
        return list(self.skills)

    def validate(self, call: SkillCall) -> None:
        if call.name not in self.skills:
            raise ValueError(f"unknown skill '{call.name}'; allowed: {self.names()}")
        required = set(self.skills[call.name])
        missing = required - set(call.args)
        if missing:
            raise ValueError(f"skill '{call.name}' missing args {sorted(missing)}")

    def describe(self) -> str:
        """Human/LLM-readable spec handed to every brain (identical for all)."""
        lines = ["Available skills (call exactly one per step):"]
        for name, args in self.skills.items():
            sig = ", ".join(args) if args else ""
            lines.append(f"- {name}({sig})")
        return "\n".join(lines)
