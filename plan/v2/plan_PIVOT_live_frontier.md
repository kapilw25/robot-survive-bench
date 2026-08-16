# 📊 PIVOT: a LIVE robotic-execution board for frontier-LLM brains

> 🎯 One line: closed-loop robotic execution in sim, but 🔒 **fix the executor and** 🔀 **swap the brain** - every frontier LLM plans through the SAME skill API; rank by whether competence **survives the OOD surprise** (🔍 transparent / 🗑️ clutter). 🆕 New model drops -> 🔌 plug in -> ▶️ run -> 📣 post -> 📚 cite.

## 🥊 Roster (contestants = brains; baselines = robot-native policies)
| 🎭 Tier | 🤝 Who (click to verify) | 🔓 Open? | 🔖 Role |
|---|---|---|---|
| 💭 General frontier brains | 🟢 [GPT](https://openai.com/) · 🅰️ [Claude](https://www.anthropic.com/claude) · 🔮 [Gemini](https://ai.google.dev/gemini-api/docs) (standard multimodal: text/image/code) · 🔷 [GLM](https://z.ai/) · 🌙 [Kimi](https://www.moonshot.ai/) · 🐦 [Qwen](https://github.com/QwenLM) · 🐋 [DeepSeek](https://github.com/deepseek-ai) · 🦙 [Llama](https://www.llama.com/) · 💎 [Gemma](https://ai.google.dev/gemma) · 🌬️ [Mistral](https://mistral.ai/) · 🟩 [Nemotron](https://huggingface.co/nvidia) · ♾️ [MiniMax](https://github.com/MiniMax-AI) · ✖️ [Grok](https://x.ai/) | mixed | plan through the FIXED skill API |
| 🤖 Robot-specialized brains (embodied-reasoning, built for robots) | 🛰️ [Gemini Robotics-ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) (`gemini-robotics-er-2-preview`, closed) · 🌌 [Cosmos-Reason1](https://github.com/nvidia-cosmos/cosmos-reason1) ([2503.15558](https://arxiv.org/abs/2503.15558)) · 🦿 [RoboBrain 2.0](https://huggingface.co/BAAI/RoboBrain2.0-7B) · 🕺 [MolmoAct2](https://arxiv.org/abs/2605.02881) (action-reasoning; blurs brain/VLA) · ✨ [Magma](https://github.com/microsoft/Magma) ([2502.13130](https://arxiv.org/abs/2502.13130); acts too) · ⏳ [RynnBrain](https://arxiv.org/html/2602.14979) | mostly OPEN | purpose-built planners; the natural high-scorers |
| 📌 Reference baselines (robot-native policies, FIXED) | ⚡ [pi0-FAST](https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README.md) (VLA) · 🧠 [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985) (LWM) · 🎬 [DreamZero](https://arxiv.org/html/2602.15922v1) (WAM) | mixed | fixed yardstick; keeps the world-model thesis alive |

## 🧭 Spec, flywheel, risks, build plan, sources
| 🗂️ Aspect | 📄 Detail |
|---|---|
| 🛡️ The one rule | score = closed-loop task SUCCESS on the arm (TSR / dTSR), NEVER multiple-choice VQA - that is what separates us from offline VLM-manipulation boards |
| 📊 Metric TSR | TSR(normal), TSR(OOD) = closed-loop task success rate -> raw leaderboard rank |
| 📉 Metric dTSR (headline) | `TSR(OOD) - TSR(normal)` per model -> "whose competence survives the surprise" (within-model robustness) |
| 🏆 Metric WAS (optional) | `(TSR_model - TSR_VLAref)/(TSR_VLAref + eps)` vs a fixed VLA reference; `dWAS = WAS(OOD) - WAS(normal)` (cross-model view) |
| 🔬 Controlled axis | 🔮 standard [Gemini](https://ai.google.dev/gemini-api/docs) (general) vs 🛰️ [Gemini Robotics-ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) (same vendor, robot-specialized) = does robot-specializing the brain help survival? Open robot-brains (Cosmos-Reason1 / RoboBrain 2.0 / RynnBrain) ask it with no API paywall |
| ✅ Open niche | 🔄 live/auto-integrate x 🤖 closed-loop EXECUTION x 🧠 frontier-LLM brains x 📉 OOD-survival (dTSR); any one axis alone is scooped, the four together is the wedge; measurement infrastructure, NOT a new metric |
| 🩸 Scoop map | full rival-by-rival table in [`novelty_map.md`](novelty_map.md); [RoboBench](https://arxiv.org/abs/2510.17801) is the closest near-neighbor, VERIFIED offline-QA (see [`notes_robobench.md`](notes_robobench.md)) so our execution wedge holds |
| 🔋 Flywheel: feasibility | can't cheaply re-run V-JEPA-2-AC every news cycle, but CAN hit GLM/Kimi/GPT/Qwen APIs on release day (live cadence achievable with API brains) |
| 📣 Flywheel: news pegs | models ship every few weeks -> "Model X debuts rank N, edge drops Y% under clutter" -> the board URL becomes the citation anchor (RoboArena / SWE-bench playbook) |
| 🔬 Flywheel: keeps science | the 3 robot-native families stay as reference baselines, so the world-model thesis survives inside the board |
| 🧪 Arch: substrate | LIBERO (MuJoCo) first; add transparent/clutter observation OOD later |
| 🔌 Arch: interface | obs (image + state text) -> LLM emits plan as calls to a FIXED skill/primitive API (or code-as-policies) -> fixed low-level controller executes -> loop |
| 📊 Arch: boards | two, like RoboArena: "all models" + "open-weight only" |
| 🔄 Arch: cadence | new release -> CI runs harness -> updates board -> auto-drafts social post |
| 🎯 Arch: venue | NeurIPS D&B / Evaluations track (live board + maintenance plan fits); workshop demo |
| 🚀 Build 1 | one frontier API (start `gemini-robotics-er-2-preview`) drives one LIBERO-Long episode, prints success/fail |
| 🚀 Build 2 | freeze a skill/primitive API between LLM and sim; route 3+ models through it |
| 🚀 Build 3 | add the transparent/clutter OOD split; report dTSR per model |
| 🚀 Build 4 | wrap in CI-on-release + two leaderboards + an auto-drafted social post |
| 🚀 Build 5 | ship datasheet + Croissant + pinned versions + a "add your model in 1 PR" path (see [`README.md`](README.md) for the checklist) |
| ⚠️ Risk 1 | benchmarking the WRAPPER not the model (weak LLM + strong skill API looks good) -> state "we measure planning competence THROUGH a fixed executor"; keep executor identical for all |
| ⚠️ Risk 2 | fairness across modalities (image vs text context, tool budgets) -> one interface contract: same skill API, same #planning calls, same obs format |
| ⚠️ Risk 3 | API version drift (models mutate behind endpoints) -> pin model IDs + dates + seeds; log all; re-tag on bumps |
| ⚠️ Risk 4 | cost (steps x episodes x models x API calls) -> per-run token caps; start with a small task subset |
| ⚠️ Risk 5 | sim-only discount (CoRL/RSS) -> frame sim-first; RoboArena is the real-robot complement, not a rival |
| ⚠️ Risk 6 | [RoboBench](https://arxiv.org/abs/2510.17801) already benchmarks MLLM-brains (QA, 5 dims, 18 models) -> do NOT claim "first to benchmark MLLM brains"; CITE it; our only claims = direct closed-loop EXECUTION + LIVE cadence + OOD-survival dTSR |
| 🔗 Sources: live robot boards | [RoboArena 2506.18123](https://arxiv.org/abs/2506.18123) · [RoboDojo 2607.04434](https://arxiv.org/abs/2607.04434) |
| 🔗 Sources: frontier-VLM manip (offline/static) | [VLABench 2412.18194](https://arxiv.org/abs/2412.18194) · [ManipBench 2505.09698](https://arxiv.org/abs/2505.09698) · [Embodied Agent Interface 2410.07166](https://arxiv.org/abs/2410.07166) |
| 🔗 Sources: live-board precedent + context | [SWE-bench-Live](https://swe-bench-live.github.io/) · [What robotics leaderboards tell us](https://itcanthink.substack.com/p/what-do-robotics-leaderboards-tell); TODO add first authors (ids web-verified) |
