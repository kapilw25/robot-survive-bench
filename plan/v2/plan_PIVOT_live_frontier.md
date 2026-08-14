# 📊 PIVOT: a LIVE robotic-execution board for frontier-LLM brains

> 🎯 One line: keep the metric 100% robotic-execution (closed-loop task success in sim), but 🔒 **fix the executor and** 🔀 **swap the brain**. Every frontier LLM (⚡ GLM / 🌙 Kimi / 🅰️ Claude / 🟢 GPT / 🐦 Qwen) plans through the SAME skill API; rank them by whether their competence **survives the OOD surprise** (🔍 transparent / 🗑️ clutter). 🆕 New model drops -> 🔌 plug the API in -> ▶️ run harness -> 📣 post -> 📚 collect citations.

## 🥊 Roster (contestants = brains; baselines = robot-native policies)
| 🎭 Tier | 🤝 Who (click to verify) | 🔓 Open? | 🔖 Role |
|---|---|---|---|
| 💭 General frontier brains | 🟢 [GPT](https://openai.com/) · 🅰️ [Claude](https://www.anthropic.com/claude) · 🔮 [Gemini](https://ai.google.dev/gemini-api/docs) (standard multimodal: text/image/code) · 🔷 [GLM](https://z.ai/) · 🌙 [Kimi](https://www.moonshot.ai/) · 🐦 [Qwen](https://github.com/QwenLM) · 🐋 [DeepSeek](https://github.com/deepseek-ai) · 🦙 [Llama](https://www.llama.com/) · 💎 [Gemma](https://ai.google.dev/gemma) · 🌬️ [Mistral](https://mistral.ai/) · 🟩 [Nemotron](https://huggingface.co/nvidia) · ♾️ [MiniMax](https://github.com/MiniMax-AI) · ✖️ [Grok](https://x.ai/) | mixed | plan through the FIXED skill API |
| 🤖 Robot-specialized brains (embodied-reasoning, built for robots) | 🛰️ [Gemini Robotics-ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) (`gemini-robotics-er-2-preview`, closed) · 🌌 [Cosmos-Reason1](https://github.com/nvidia-cosmos/cosmos-reason1) ([2503.15558](https://arxiv.org/abs/2503.15558)) · 🦿 [RoboBrain 2.0](https://huggingface.co/BAAI/RoboBrain2.0-7B) · 🕺 [MolmoAct2](https://arxiv.org/abs/2605.02881) (action-reasoning; blurs brain/VLA) · ✨ [Magma](https://github.com/microsoft/Magma) ([2502.13130](https://arxiv.org/abs/2502.13130); acts too) · ⏳ [RynnBrain](https://arxiv.org/html/2602.14979) | mostly OPEN | purpose-built planners; the natural high-scorers |
| 📌 Reference baselines (robot-native policies, FIXED) | ⚡ [pi0-FAST](https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README.md) (VLA) · 🧠 [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985) (LWM) · 🎬 [DreamZero](https://arxiv.org/html/2602.15922v1) (WAM) | mixed | fixed yardstick; keeps the world-model thesis alive |

🔬 **Key controlled axis:** 🔮 standard [Gemini](https://ai.google.dev/gemini-api/docs) (general brain) vs 🛰️ [Gemini Robotics-ER 2](https://deepmind.google/models/gemini-robotics/embodied-reasoning/) (same vendor, robot-specialized brain) = does robot-specializing the brain help competence SURVIVE the OOD surprise? The open robot-brains (🌌 Cosmos-Reason1 / 🦿 RoboBrain 2.0 / ⏳ RynnBrain) let us ask the same question with no API paywall.

## 🛡️ The one rule that keeps it "robotic execution ONLY"
🛡️ Score = closed-loop task SUCCESS on the arm (TSR / dTSR). NEVER multiple-choice VQA. That single line is what separates this from the offline VLM-manipulation boards (see scoop map).

## 📏 Metrics (no new metric invented; all reuse priors)
| 📏 Metric | 🧮 Definition | 🎯 Use |
|---|---|---|
| 📊 TSR(normal), TSR(OOD) | closed-loop task success rate | raw leaderboard rank |
| 📉 **dTSR** (headline) | `TSR(OOD) - TSR(normal)` per model | "whose competence survives the surprise" (within-model robustness) |
| 🏆 WAS (optional, cross-model) | `(TSR_model - TSR_VLAref)/(TSR_VLAref + eps)` vs a fixed VLA reference | gain-over-baseline view; `dWAS = WAS(OOD) - WAS(normal)` as in the other plan docs |

## 🩸 Prior-art / scoop map (web-verified 2026-08; ids checked, first authors TODO)
| 🩸 Prior work | 🔍 What it is | 🎯 Our wedge vs it |
|---|---|---|
| 📊 [RoboArena](https://arxiv.org/abs/2506.18123) (2506.18123) | LIVE, real-robot DROID board, crowd-sourced pairwise | ranks robot **policies (VLAs)**, not frontier-LLM brains; real-robot can't run 20 APIs continuously. We are the **sim + frontier-brain** complement |
| 📊 [RoboDojo](https://arxiv.org/abs/2607.04434) (2607.04434) | unified sim+real, continuously-updated board, 30 policies | again **policies**, not LLM brains; no OOD-survival headline |
| 🧊 [VLABench](https://arxiv.org/abs/2412.18194) (2412.18194) | MuJoCo language-conditioned manip, foundation-model agents | **static**, no auto-integrate-on-release, no dTSR |
| 📝 [ManipBench](https://arxiv.org/abs/2505.09698) (2505.09698) | 33 VLMs (GPT/Gemini/o1/Qwen) on manip reasoning | **12.6k multiple-choice = offline VQA**, NOT closed-loop execution. ⚠️ The thing we must NOT become |
| 🧩 [Embodied Agent Interface](https://arxiv.org/abs/2410.07166) (2410.07166) | LLM embodied decision-making (VirtualHome/BEHAVIOR) | **module-level planning eval**, not physics-sim arm success; static |
| 🔄 [SWE-bench-Live](https://swe-bench-live.github.io/) | auto-updating agent board (text) | proves "live + auto-update = citation magnet"; no robot analog exists yet |
| 🧪 [RoboBench](https://arxiv.org/abs/2510.17801) (2510.17801) | evaluates MLLMs as an "embodied brain" | ⚠️ CLOSEST near-neighbor - VERIFY it is offline QA (not closed-loop execution) and static; our wedge holds only if it does NOT run live closed-loop dTSR |

**✅ Open niche = the intersection nobody occupies:** 🔄 live/auto-integrate-on-release x 🤖 closed-loop robot execution x 🧠 frontier-LLM brains x 📉 OOD-survival (dTSR). Any one axis alone is scooped; the four together is the wedge. 🙏 Honesty: this is measurement infrastructure, NOT a new metric or protocol.

## 🎡 Why the flywheel actually works here
| 💡 Reason | 📝 Detail |
|---|---|
| 🔋 Feasibility flips in our favor | can't cheaply re-run V-JEPA-2-AC every news cycle, but CAN hit GLM/Kimi/GPT/Qwen APIs on release day. Live cadence is achievable with API brains, not with robot-native weights |
| 📣 Built-in news pegs | frontier models ship every few weeks -> "Model X debuts rank N, edge drops Y% under clutter" -> the board URL becomes the citation anchor (RoboArena / SWE-bench playbook) |
| 🔬 Keeps the science | 3 robot-native families stay as reference baselines, so the world-model thesis survives inside the board |

## ⚠️ Brutal risks + fixes (address or it desk-rejects)
| # | ⚠️ Risk | 🛠️ Fix |
|---|---|---|
| 1️⃣ | 🎭 Benchmarking the WRAPPER, not the model (weak LLM + strong skill API looks good) | state plainly "we measure planning competence THROUGH a fixed executor"; keep executor identical for all |
| 2️⃣ | ⚖️ Fairness across modalities (image vs text context, tool budgets) | one interface contract: same skill API, same #planning calls, same obs format |
| 3️⃣ | 🔀 API version drift (models mutate behind endpoints) | pin model IDs + dates + seeds; log all; re-tag on version bumps |
| 4️⃣ | 💰 Cost (steps x episodes x models x API calls) | per-run token caps; start with a small task subset |
| 5️⃣ | 🧪 Sim-only discount (CoRL/RSS) | frame sim-first; RoboArena is the real-robot complement, not a rival |

## 🏗️ Minimal architecture (reuses the Phase-1 harness)
| 🧩 Piece | ⚙️ Choice |
|---|---|
| 🧪 Substrate | LIBERO (MuJoCo) first; add transparent/clutter observation OOD later |
| 🔌 Interface | obs (image + state text) -> LLM emits plan as calls to a FIXED skill/primitive API (or code-as-policies) -> fixed low-level controller executes -> loop |
| 📏 Metric | TSR; headline dTSR = TSR(OOD) - TSR(normal) per model |
| 📊 Boards | two, like RoboArena: "all models" + "open-weight only" |
| 🔄 Cadence | new release -> CI runs harness -> updates board -> auto-drafts social post |
| 🎯 Venue | NeurIPS D&B / Evaluations track (live board + maintenance plan fits); workshop demo |

## 🚀 Next steps (ordered; see `README.md` in this folder for the build checklist)
1. 🔁 One closed loop: one frontier API drives one LIBERO-Long episode, prints success/fail.
2. 🔌 Freeze a skill/primitive API between LLM and sim; route 3+ models through it.
3. 🔍🗑️ Add the transparent/clutter OOD split; report dTSR per model.
4. 📡 Wrap in CI-on-release + two leaderboards + an auto-drafted social post.
5. 📤 Ship datasheet + Croissant + pinned versions + a "add your model in 1 PR" path.

## 🔗 Sources
- 📊 Live robot boards: [RoboArena 2506.18123](https://arxiv.org/abs/2506.18123) · [RoboDojo 2607.04434](https://arxiv.org/abs/2607.04434)
- 📝 Frontier-VLM manipulation (mostly offline / static): [VLABench 2412.18194](https://arxiv.org/abs/2412.18194) · [ManipBench 2505.09698](https://arxiv.org/abs/2505.09698) · [Embodied Agent Interface 2410.07166](https://arxiv.org/abs/2410.07166)
- 🔄 Live-board-as-citation-magnet precedent (text): [SWE-bench-Live](https://swe-bench-live.github.io/)
- 🧭 Context: [What robotics leaderboards tell us](https://itcanthink.substack.com/p/what-do-robotics-leaderboards-tell)
- 📌 TODO before any writeup: add exact first author for each arXiv id (ids + titles web-verified; authors not yet).
