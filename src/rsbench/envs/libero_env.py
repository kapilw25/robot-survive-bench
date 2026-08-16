"""LIBERO-Long closed-loop wrapper (Option A: the real substrate for step 1).

Runs on a Linux box (LIBERO/robosuite/MuJoCo, py3.10, MUJOCO_GL=egl for headless). Not on the
M1 Air (py3.13 + mac headless-GL incompatibility). Everything here is real EXCEPT
_skill_to_primitive(), which is the one integration TODO: mapping a high-level SkillCall to a
low-level OSC action sequence (the grasp/place motion primitives) for your controller.

Install (GPU/Linux box):
  conda create -n rsbench python=3.10 -y && conda activate rsbench
  pip install -e ".[dev]" google-genai
  pip install git+https://github.com/Lifelong-Robot-Learning/LIBERO.git
  export MUJOCO_GL=egl GEMINI_API_KEY=...        # key: https://aistudio.google.com/apikey
Run:
  bash scripts/run_step1_one_episode.sh gemini-er2 libero_long
"""
from __future__ import annotations

from rsbench.envs.base import Env
from rsbench.envs.ood import apply_ood
from rsbench.types import Observation, SkillCall, StepResult


class LiberoEnv(Env):
    def __init__(self, camera: int = 256) -> None:
        try:
            from libero.libero import benchmark, get_libero_path  # type: ignore
            from libero.libero.envs import OffScreenRenderEnv       # type: ignore
        except Exception as exc:  # import-safe on machines without LIBERO
            raise NotImplementedError(
                "LIBERO not installed - run on a Linux+py3.10 box (see module docstring). "
                "Use suite 'toy' or 'mock' here."
            ) from exc
        self._suite = benchmark.get_benchmark_dict()["libero_10"]()   # LIBERO-Long
        self._get_path = get_libero_path
        self._OffScreen = OffScreenRenderEnv
        self.camera = camera
        self._env = None
        self._task = ""
        self._ood = "normal"

    def task_list(self) -> list[str]:
        return [self._suite.get_task(i).name for i in range(self._suite.n_tasks)]

    def _task_index(self, task: str) -> int:
        names = self.task_list()
        return names.index(task) if task in names else int(task.split("_")[-1]) - 1

    def reset(self, task: str, ood: str = "normal", seed: int = 0) -> Observation:
        import os
        t = self._suite.get_task(self._task_index(task))
        bddl = os.path.join(self._get_path("bddl_files"), t.problem_folder, t.bddl_file)
        self._env = self._OffScreen(bddl_file_name=bddl, camera_heights=self.camera, camera_widths=self.camera)
        self._env.seed(seed)
        self._task, self._ood = task, ood
        return self._to_obs(self._env.reset())

    def execute(self, call: SkillCall) -> StepResult:
        info: dict = {}
        last = None
        for action in self._skill_to_primitive(call):        # low-level OSC steps
            last, _reward, _done, info = self._env.step(action)
        success = bool(self._env.check_success()) if hasattr(self._env, "check_success") \
            else bool(info.get("success", False))
        done = success or call.name == "done"
        return StepResult(self._to_obs(last if last is not None else self._env._get_observations()),
                          done=done, success=success, info=info)

    def _to_obs(self, obs) -> Observation:
        import numpy as np
        img = obs["agentview_image"][::-1]                   # LIBERO agentview is vertically flipped
        img = apply_ood(img, self._ood)                      # observation-only OOD (step 4)
        eef = np.round(obs.get("robot0_eef_pos", []), 3).tolist()
        state = f"eef_pos={eef}; gripper={obs.get('robot0_gripper_qpos')}"
        return Observation(task=self._task, image=img, state_text=state)

    def _skill_to_primitive(self, call: SkillCall) -> list:
        """TODO (the one integration point): map a SkillCall -> a list of low-level OSC actions.

        Reliable primitives (use object poses from self._env.sim / obs):
          move_to(target): servo EE above target xyz
          pick(object):    approach above -> descend -> close gripper -> lift
          place(target):   move above target -> descend -> open gripper -> retract
          open/close:      actuate the articulated object; done: no-op
        Return a list of 7-dim OSC action vectors (dx,dy,dz,droll,dpitch,dyaw,gripper).
        """
        raise NotImplementedError("implement skill -> OSC motion primitives for your controller")
