# 📊 v2 - LIVE frontier-brain robot-execution board (current direction)

🎯 **One line:** closed-loop robot execution in sim, but 🔒 FIX the executor and 🔀 SWAP THE BRAIN - every frontier LLM plans through the same skill API; rank by whether competence survives the OOD surprise (📉 dTSR). 🆕 New model drops -> 🔌 plug in -> ▶️ run -> 📣 post -> 📚 cite. 🥊 Contestants = 💭 general frontier brains (🟢 [GPT](https://openai.com/) / 🅰️ [Claude](https://www.anthropic.com/claude) / 🔮 [Gemini](https://ai.google.dev/gemini-api/docs) / 🔷 [GLM](https://z.ai/) / 🌙 [Kimi](https://www.moonshot.ai/) / 🐦 [Qwen](https://github.com/QwenLM) / 🐋 [DeepSeek](https://github.com/deepseek-ai) / 🦙 [Llama](https://www.llama.com/) / ...) + 🤖 robot-specialized brains (🛰️ [Gemini Robotics-ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) / 🌌 [Cosmos-Reason1](https://github.com/nvidia-cosmos/cosmos-reason1) / 🦿 [RoboBrain 2.0](https://huggingface.co/BAAI/RoboBrain2.0-7B) / ...); 📌 fixed baselines = ⚡ pi0-FAST / 🧠 V-JEPA-2-AC / 🎬 DreamZero. Full roster: [`plan_PIVOT_live_frontier.md`](plan_PIVOT_live_frontier.md).

📎 Deep dive: [`plan_PIVOT_live_frontier.md`](plan_PIVOT_live_frontier.md) (full scoop map, risks, architecture). 🔗 Shared refs: [`../plan_dataset.md`](../plan_dataset.md), [`../plan_rejections_risks.md`](../plan_rejections_risks.md). ⬅️ Pre-pivot version: [`../v1/`](../v1/README.md).

## 🆕 a) Novelty gap (web-verified; every ref linked)

**🤖 Lens 1 - vs robotic-execution benchmarks:** live robot boards exist, but they rank robot policies, not frontier-LLM brains.
| 🩸 Prior (click to verify) | 🔍 What it is | 🎯 Our wedge |
|---|---|---|
| 📊 [RoboArena (2506.18123)](https://arxiv.org/abs/2506.18123) | LIVE real-robot DROID board, crowd-sourced pairwise | ranks robot **policies (VLAs)**; real-robot can't run 20 APIs continuously |
| 📊 [RoboDojo (2607.04434)](https://arxiv.org/abs/2607.04434) | unified sim+real, continuously-updated, 30 policies | again **policies**, not LLM brains; no OOD-survival headline |

**🧠 Lens 2 - vs frontier-model benchmarks:** frontier-VLM-on-manipulation boards are offline/static, and the general frontier boards are 100% digital.
| 🩸 Prior (click to verify) | 🔍 What it is | 🎯 Our wedge |
|---|---|---|
| 📝 [ManipBench (2505.09698)](https://arxiv.org/abs/2505.09698) | 33 VLMs (GPT/Gemini/o1/Qwen) | **12.6k multiple-choice = offline VQA**, NOT closed-loop execution. ⚠️ The thing we must NOT become |
| 🧊 [VLABench (2412.18194)](https://arxiv.org/abs/2412.18194) | MuJoCo foundation-model manip | **static**, no auto-integrate / no live cadence |
| 🧩 [Embodied Agent Interface (2410.07166)](https://arxiv.org/abs/2410.07166) | LLM planning modules (VirtualHome/BEHAVIOR) | **module-level planning**, not physics-sim arm success |
| 💻 the chart's benchmarks ([SWE-bench](https://www.swebench.com/), Terminal-Bench, HLE, cyber gyms) | frontier agentic | **100% digital, zero embodiment** |
| 🔄 [SWE-bench-Live](https://swe-bench-live.github.io/) | auto-updating agent board (text) | proves "live = citation magnet", but **text only, no robot analog** |
| 🧪 [RoboBench](https://arxiv.org/abs/2510.17801) | MLLMs-as-embodied-brain eval | ⚠️ closest near-neighbor; verify offline-QA vs closed-loop before claiming daylight |

✅ **Open niche = the intersection nobody occupies:** 🔄 live/auto-integrate x 🤖 closed-loop robot EXECUTION x 🧠 frontier-LLM brains x 📉 OOD-survival (dTSR). 🙏 Honesty: measurement infrastructure, not a new metric.

## 📦 b) Datasets (every set linked)
| 🎯 Use | 🗂️ What (click to verify) | 📝 Note |
|---|---|---|
| 🧪 Substrate | [LIBERO](https://huggingface.co/datasets/lerobot/libero) (MuJoCo) | where a frontier API can drive a closed loop |
| 🔍🗑️ OOD | same transparent/clutter shift as v1 ([ClearGrasp](https://github.com/Shreeyak/cleargrasp) · [GraspNet-1B](https://dl.acm.org/doi/abs/10.1177/02783649231193710) source) | camera-only change |
| 🔌 Interface | FIXED skill/primitive API between LLM and sim ([code-as-policies](https://code-as-policies.github.io/) style) | LLM never emits raw actions |
| 📌 Reference baselines | ⚡ [pi0-FAST](https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README.md) · 🧠 [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985) · 🎬 [DreamZero](https://arxiv.org/html/2602.15922v1) | fixed yardstick (keeps the world-model thesis) |
| 📤 Ship | pinned model IDs + seeds + datasheet + [Croissant](https://github.com/mlcommons/croissant) + "add your model in 1 PR" | live-board reproducibility |

## 🚀 c) Start steps (max 5; refs linked)
1. 🔁 One closed loop: one frontier API (start `gemini-robotics-er-2-preview`) drives one [LIBERO](https://huggingface.co/datasets/lerobot/libero)-Long episode via a fixed skill API; prints success/fail.
2. 📏 TSR over the 10 tasks (behavioural only; ignore prediction/calibration metrics).
3. 🔀 Freeze the skill API; route 💭 general brains (🟢 [GPT](https://openai.com/) / 🅰️ [Claude](https://www.anthropic.com/claude) / 🔮 [Gemini](https://ai.google.dev/gemini-api/docs) / 🔷 [GLM](https://z.ai/) / 🌙 [Kimi](https://www.moonshot.ai/) / 🐦 [Qwen](https://github.com/QwenLM) / 🐋 [DeepSeek](https://github.com/deepseek-ai) / 🦙 [Llama](https://www.llama.com/)) AND 🤖 robot-specialized brains (🛰️ [Gemini Robotics-ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) / 🌌 [Cosmos-Reason1](https://github.com/nvidia-cosmos/cosmos-reason1) / 🦿 [RoboBrain 2.0](https://huggingface.co/BAAI/RoboBrain2.0-7B)) through the IDENTICAL interface; rank all.
4. 📉 Add the transparent/clutter OOD split; report dTSR = TSR(OOD) - TSR(normal) per model (baselines fixed).
5. 📡 Go live: CI on each release -> update 2 boards (all / open-weight, like [RoboArena](https://arxiv.org/abs/2506.18123)) -> auto-draft social post.

🛡️ **The one rule that keeps it robotic-execution ONLY:** score = closed-loop task SUCCESS on the arm (TSR / dTSR), NEVER multiple-choice VQA. That is the line that separates us from 📝 [ManipBench](https://arxiv.org/abs/2505.09698).
