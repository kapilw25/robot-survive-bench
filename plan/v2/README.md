# 📊 v2 - LIVE frontier-brain robot-execution board (current direction)

🎯 Closed-loop robot execution in sim, but 🔒 fix the executor and 🔀 swap the brain: rank frontier LLMs by whether competence survives the OOD surprise (📉 dTSR); new model drops -> 🔌 plug in -> ▶️ run -> 📣 post -> 📚 cite.

## 🥊 Roster, datasets and design
| 🏷️ Aspect | 📄 Detail (click to verify) |
|---|---|
| 🥊 Contestants (general brains) | 🟢 [GPT](https://openai.com/) · 🅰️ [Claude](https://www.anthropic.com/claude) · 🔮 [Gemini](https://ai.google.dev/gemini-api/docs) · 🔷 [GLM](https://z.ai/) · 🌙 [Kimi](https://www.moonshot.ai/) · 🐦 [Qwen](https://github.com/QwenLM) · 🐋 [DeepSeek](https://github.com/deepseek-ai) · 🦙 [Llama](https://www.llama.com/) |
| 🤖 Contestants (robot-specialized brains) | 🛰️ [Gemini Robotics-ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) · 🌌 [Cosmos-Reason1](https://github.com/nvidia-cosmos/cosmos-reason1) · 🦿 [RoboBrain 2.0](https://huggingface.co/BAAI/RoboBrain2.0-7B) |
| 📌 Fixed baselines | ⚡ [pi0-FAST](https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README.md) · 🧠 [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985) · 🎬 [DreamZero](https://arxiv.org/html/2602.15922v1) (keeps the world-model thesis) |
| 🧪 Substrate | [LIBERO](https://huggingface.co/datasets/lerobot/libero) (MuJoCo) - where a frontier API can drive a closed loop |
| 🔍🗑️ OOD split | transparent/clutter, camera-only shift (source perception sets: [ClearGrasp](https://github.com/Shreeyak/cleargrasp) · [GraspNet-1B](https://dl.acm.org/doi/abs/10.1177/02783649231193710)) |
| 🔌 Interface | FIXED skill/primitive API between LLM and sim ([code-as-policies](https://code-as-policies.github.io/) style); LLM never emits raw actions |
| 📉 Metric / headline | TSR; dTSR = TSR(OOD) - TSR(normal) per model |
| 📤 Ship | pinned model IDs + seeds + datasheet + [Croissant](https://github.com/mlcommons/croissant) + "add your model in 1 PR" |
| 🆕 Novelty gap | full 13-rival table -> [`novelty_map.md`](novelty_map.md); open niche = live x closed-loop EXECUTION x frontier-LLM brains x OOD-survival (dTSR); measurement infra, not a new metric |
| 🛡️ The one rule | score = closed-loop task SUCCESS (TSR/dTSR), NEVER multiple-choice VQA - the line vs 📝 [ManipBench](https://arxiv.org/abs/2505.09698) |
| 📎 Refs | deep dive [`plan_PIVOT_live_frontier.md`](../legacy/plan_PIVOT_live_frontier.md) · shared [`../plan_dataset.md`](../plan_dataset.md) · [`../plan_rejections_risks.md`](../plan_rejections_risks.md) · pre-pivot [`../v1/`](../v1/README.md) |

## 🚀 Build steps (max 5)
| # | 🚀 Step | 📋 Detail |
|---|---|---|
| 1️⃣ | 🔁 One closed loop | one frontier API (start `gemini-robotics-er-2-preview`) drives one [LIBERO](https://huggingface.co/datasets/lerobot/libero)-Long episode via a fixed skill API; prints success/fail |
| 2️⃣ | 📏 Metric | TSR over the 10 tasks (behavioural only; ignore prediction/calibration) |
| 3️⃣ | 🔀 Swap the brain | freeze the skill API; route 💭 general (🟢 [GPT](https://openai.com/) · 🅰️ [Claude](https://www.anthropic.com/claude) · 🔮 [Gemini](https://ai.google.dev/gemini-api/docs) · 🔷 [GLM](https://z.ai/) · 🌙 [Kimi](https://www.moonshot.ai/) · 🐦 [Qwen](https://github.com/QwenLM) · 🐋 [DeepSeek](https://github.com/deepseek-ai) · 🦙 [Llama](https://www.llama.com/)) + 🤖 robot-specialized (🛰️ [Gemini Robotics-ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) · 🌌 [Cosmos-Reason1](https://github.com/nvidia-cosmos/cosmos-reason1) · 🦿 [RoboBrain 2.0](https://huggingface.co/BAAI/RoboBrain2.0-7B)) through the IDENTICAL interface; rank all |
| 4️⃣ | 📉 OOD | add the transparent/clutter split; report dTSR = TSR(OOD) - TSR(normal) per model (baselines fixed) |
| 5️⃣ | 📡 Go live | CI on each release -> update 2 boards (all / open-weight, like [RoboArena](https://arxiv.org/abs/2506.18123)) -> auto-draft social post |
