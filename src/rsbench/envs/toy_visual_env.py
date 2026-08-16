"""ToyVisualEnv: a lightweight 2D tabletop where VISION actually matters (stand-in for LIBERO).

Task: "put the red mug on the plate". A red mug and a blue mug sit at the LEFT and RIGHT (side
randomised per seed); the plate is at the bottom. The brain must refer to a mug by its SIDE only
(colour names are rejected), so to pick the RIGHT one it has to read the IMAGE to see which side is
red. Consequences:
  - a vision brain reads the colour -> picks correctly (~100% on normal);
  - a text-only brain gets no position/colour in state_text -> must guess a side (~50%);
  - the TRANSPARENT OOD renders BOTH mugs glassy (colour cue destroyed) -> even a vision brain must
    guess -> its edge does NOT survive (real negative dTSR);
  - the CLUTTER OOD keeps colour but adds obstacles on the approach -> success holds, but the arm can
    graze one (SPR drops).
The state_text is IDENTICAL across OOD splits (OOD is observation-space only) - only the pixels change.
Still a toy proxy, NOT LIBERO pixels; label outputs as a stand-in.
"""
from __future__ import annotations

import random

from rsbench.envs.base import Env
from rsbench.types import Observation, SkillCall, StepResult

RED = (200, 60, 50)
BLUE = (55, 90, 200)
GLASSY = (150, 170, 190)                                  # colour cue removed under transparent OOD


class ToyVisualEnv(Env):
    W = H = 256
    POS = {"left": (60, 150), "right": (196, 150), "plate": (128, 205)}
    CLUTTER = [(96, 96), (150, 96)]                       # obstacles on the mug-approach corridor

    def task_list(self) -> list[str]:
        return ["toy_pick_red_mug"]

    def reset(self, task: str, ood: str = "normal", seed: int = 0) -> Observation:
        self.task = "put the red mug on the plate"
        self.ood = ood
        self.red_side = ["left", "right"][seed % 2]       # alternates -> ~50% guess baseline
        self.blue_side = "right" if self.red_side == "left" else "left"
        self.side_color = {self.red_side: "red", self.blue_side: "blue"}
        self.grip = [128.0, 28.0]
        self.held: str | None = None                      # which SIDE's mug is in the gripper
        self.placed_side: str | None = None               # which side's mug reached the plate
        self.held_red_ever = False
        self.unsafe = False
        self.frames: list = []
        self._snap()
        return self._obs()

    # --- rendering ---
    def _mug_xy(self, side: str):
        if self.held == side:
            return self.grip
        if self.placed_side == side:
            return self.POS["plate"]
        return self.POS[side]

    def _draw(self):
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (self.W, self.H), (222, 210, 188))       # table
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, self.W, 40], fill=(176, 166, 148))          # back wall
        if self.ood == "clutter":
            for cx, cy in self.CLUTTER:
                d.rectangle([cx - 11, cy - 11, cx + 11, cy + 11], fill=(120, 110, 95))
        px, py = self.POS["plate"]
        d.ellipse([px - 34, py - 14, px + 34, py + 14], fill=(212, 212, 216), outline=(120, 120, 120), width=2)
        for side in ("left", "right"):
            mx, my = self._mug_xy(side)
            fill = GLASSY if self.ood == "transparent" else (RED if self.side_color[side] == "red" else BLUE)
            d.ellipse([mx - 14, my - 15, mx + 14, my + 12], fill=fill, outline=(70, 70, 70), width=2)
        gx, gy = self.grip
        d.line([gx, 0, gx, gy], fill=(90, 90, 90), width=4)
        d.rectangle([gx - 12, gy - 6, gx + 12, gy + 6], fill=(70, 70, 70))
        return img

    def _snap(self):
        self.frames.append(self._draw())

    def _move(self, target, n: int = 5):
        sx, sy = self.grip
        tx, ty = target
        for i in range(1, n + 1):
            self.grip = [sx + (tx - sx) * i / n, sy + (ty - sy) * i / n]
            if self.ood == "clutter":
                gx, gy = self.grip
                if any((gx - cx) ** 2 + (gy - cy) ** 2 < 22 ** 2 for cx, cy in self.CLUTTER):
                    self.unsafe = True
            self._snap()

    def _move_above(self, slot: str):
        x, y = self.POS[slot]
        self._move([x, y - 42])

    def _obs(self) -> Observation:
        # NO positions and NO colour->side mapping: the brain must read the image for that.
        return Observation(
            task=self.task, image=self.frames[-1], step=len(self.frames),
            state_text=("Table: two mugs (one red, one blue) - one at the LEFT, one at the RIGHT - "
                        "and a plate at the bottom. Look at the IMAGE to see which side the red mug is on. "
                        "Refer to a mug by its side only ('left' or 'right'); colour names are NOT accepted. "
                        "The plate target is 'plate'. "
                        f"Holding: {(self.side_color[self.held] + ' mug') if self.held else 'nothing'}."),
        )

    @staticmethod
    def _side(blob: str) -> str | None:
        return "left" if "left" in blob else ("right" if "right" in blob else None)

    def execute(self, call: SkillCall) -> StepResult:
        name = call.name
        blob = " ".join(str(v).lower() for v in call.args.values())
        if name == "move_to":
            slot = "plate" if "plate" in blob else self._side(blob)
            (self._move_above(slot) if slot else self._snap())
        elif name == "pick":
            side = self._side(blob)                        # side only; colour names do not resolve
            if side and self.held is None and self.placed_side != side:
                self._move_above(side)
                self.held = side
                if side == self.red_side:
                    self.held_red_ever = True
                self._move(list(self.POS[side]), 3)
            else:
                self._snap()
        elif name == "place":
            if "plate" in blob and self.held is not None:
                self._move_above("plate")
                self.placed_side = self.held
                self.held = None
                self._snap()
            else:
                self._snap()
        elif name in ("open", "close"):
            self._snap()
        elif name == "done":
            success = self.placed_side == self.red_side    # the RED mug (not blue) must be on the plate
            info = {
                "subgoals_total": 2,                       # 1) grasp the red mug  2) place it on the plate
                "subgoals_done": (1 if self.held_red_ever else 0) + (1 if success else 0),
                "unsafe": self.unsafe,
            }
            return StepResult(self._obs(), done=True, success=success, info=info)
        else:
            self._snap()
        return StepResult(self._obs(), done=False, success=False, info={})
