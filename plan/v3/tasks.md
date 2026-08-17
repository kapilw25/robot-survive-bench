# v3 - tasks (the ONE list to read)

RobotSurviveBench: swap the brain, keep the executor frozen, measure if competence survives an OOD surprise (dTSR). All zero-shot, no training. Start here; older detail lives in `../v2/`.

## ✅ Done - demo on the TOY substrate (laptop)
- ✅ **Metrics coded** - TSR, dTSR, WAS + LHCR/RSR/SPR in `metrics/scores.py`; only the 4 behavioural metrics are computable zero-shot, the other 6 are N/A for action-only brains.
- ✅ **Dataset gallery** - 5 different-type LIBERO frames (Spatial/Object/Goal/Long) pulled from HuggingFace and shown as looping video rollouts on the dashboard.
- ✅ **Dashboard** - `docs/` page: Dataset / Metrics / Models / System-design tabs, light-default with dark toggle, live scores, per-model limitations, mermaid flow diagram.
- ✅ **5 brains wired** - gemini-er2 + glm/kimi/qwen/deepseek (one Fireworks key) run closed-loop and get scored; GPT/Claude/Llama/Cosmos/RoboBrain still blocked on keys, credits, or GPU.
- ✅ **Vision-required toy** - red/blue mug, refer by side only; vision brains 100% on normal vs text-blind ~50%, and the transparent OOD collapses the edge (a real dTSR demo).

## ⬜ Next - make it REAL (needs a GPU/Linux box; "Option A")
- ⬜ **Stand up LIBERO** - install LIBERO/MuJoCo (py3.10, `MUJOCO_GL=egl`) on a GPU box and run the shipped `libero_env.py` so a brain drives a real physics episode.
- ⬜ **Motion primitives** - fill the one TODO `_skill_to_primitive`: map each skill call (pick/place/move) to low-level OSC arm motions with real grasping that can actually fail.
- ⬜ **Pixels-only** - drop the coordinate "cheat sentence" from `state_text` so the brain must read the camera image; this is where vision becomes genuinely required.
- ⬜ **Real OOD** - replace the colour-tint and drawn-box hacks with real transparent/reflective materials and occlusion in the render (ClearGrasp / GraspNet as perception sources).
- ⬜ **Run baselines** - execute the fixed VLA/LWM/WAM policies (pi0-FAST / V-JEPA-2-AC / DreamZero) so WAS gets a real denominator; today the WAS column shows "-".
- ⬜ **Real success + safety** - use LIBERO BDDL goal checks and inject perturbations, so success is semantic and LHCR/RSR/SPR stop being flat (this answers Aman's discriminative-power point).
- ⬜ **Scale runs** - all 10 LIBERO-Long tasks across many seeds (not n=3), so TSR and dTSR per model are statistically meaningful.

## ⬜ Roster + ship
- ⬜ **Wire remaining brains** - as access arrives: GPT (add OpenAI credits), Claude (Anthropic key), Llama (Together key), Cosmos-Reason1 / RoboBrain2 (self-host on GPU).
- ⬜ **Go live** - CI on each new model release updates the 2 leaderboards (all / open-weight) and auto-drafts a social post, RoboArena-style.
- ⬜ **Ship datasheet** - pin model IDs and seeds, publish the datasheet plus Croissant metadata, and provide an "add your model in one PR" path.
