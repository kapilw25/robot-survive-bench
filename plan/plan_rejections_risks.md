# 🧨 ACTION-ATLAS: Novelty Reality + Rejection Risks (single file)

> 🎯 **FOCUS: Benchmarking Zero-shot (No training) ROBOTIC EXECUTION ONLY** for 4 families: ⚡ **VLA** (baseline) vs the predictive trio 🧠 **LWM** / 🎬 **WAM** / 🌌 **WFM**. A frozen checkpoint acting in a closed loop on a robot task; no fine-tuning, no video-QA, no non-robot tasks.
>
> 🧊 **Cold reality (web-verified, 2026-08):** stripped to zero-shot robotic execution, this benchmark has **no standalone novelty left**. Every intended contribution is already published (scoop table below):
> - 📏 **WAS** is a rename of existing "embodied-utility gain" / "2x over VLA" / "optimization lift".
> - 🔁 the **cross-family zero-shot closed-loop** comparison (⚡ VLA vs 🧠 LWM vs 🎬 WAM) already lives in [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985)'s own baseline table (beats Octo-VLA 80% vs 15%, 16x faster than Cosmos), and in [WorldArena](https://arxiv.org/abs/2602.08971) + [World-in-World](https://arxiv.org/abs/2510.18135).
> - 🌌 **WFM (Cosmos) has NO zero-shot action instance** - it only generates/grades video ([WorldBench](https://world-bench.github.io/)), so the honest execution set is **3 families** (⚡🧠🎬), not 4.
> - 🗺️ **DenseWorld zero-shot nav is infeasible** - no family drives without a trained action head + photoreal reconstruction (breaks both no-training and GPU-light).
>
> 🧭 **Honest decision:** do NOT ship a standalone benchmark. 🔀 **Fold into Paper-1 (the survey)** as (a) a neutral 📊 **WAS assessment** crediting the priors, and (b) a small 🔁 **reproduction table** running the 3 zero-shot models (**π0-FAST** / **V-JEPA-2-AC** / **DreamZero**) on one shared 🤖 **DROID/Franka** arm (claimed as measurement/consolidation, not novelty). This matches the two-paper plan: **assess WAS, do not adopt it**.

## 🔬 Scoop table - why the benchmark novelty is gone (hyperlinked)

| 🏷️ Prior work | 🧩 What it already ships | 🩸 Scoops our... |
|---|---|---|
| 🌍 [World-in-World](https://arxiv.org/abs/2510.18135) (ICLR'26 Oral) · [site](https://world-in-world.github.io/) · [code](https://github.com/World-In-World/world-in-world) | Closed-loop manip (RLBench): base policy vs world-model-augmented; reports **gain over direct baseline** (44.5 to 46.5% SR); headline "visual quality ≠ embodied utility" | 📏 the WAS metric + 📈 the prediction-vs-execution finding |
| 🏟️ [WorldArena](https://arxiv.org/abs/2602.08971) + [2.0](https://arxiv.org/html/2605.17912v1) | 14 embodied world models on perception + functional utility; explicitly reports **WM < VLA (π0.5)** and a "perception-functionality gap"; live public leaderboard | 🔁 the WM-vs-VLA head-to-head + 📉 the gap chart |
| 🧠 [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985) | Zero-shot closed-loop manip; latent-WM vs **VLA (Octo)** vs **video-WM (Cosmos)** in ONE table (80% vs 15% Octo; 16x faster than Cosmos) | 🔁 the whole **3-family, zero-shot, closed-loop** comparison |
| 🎬 [DreamZero](https://arxiv.org/html/2602.15922v1) · [site](https://dreamzero0.github.io/) | WAM zero-shot closed-loop vs VLA baselines, reports **2x** advantage | 📏 "advantage over VLA" = WAS by another name |
| 🪜 [WM-Eval position: L0-L7 ladder](https://arxiv.org/abs/2606.15032) | Decision-making-centric world-model evaluation ladder; L5 = reward/outcome fidelity = "optimization lift / policy ranking" | 📏 WAS-as-concept |
| 🔩 [RoboWM-Bench](https://arxiv.org/abs/2604.19092) | Converts WM videos to actions, executes in sim; slices spatial / contact / distortion | 🩻 the diagnostic capability-slicing wedge |
| 🤖 [RoboDojo](https://arxiv.org/abs/2607.04434) | Unified sim+real harness; **XPolicyLab integrates 30 policies**, 5 capability axes, leaderboard | 🧰 the unified-interface + capability-slicing wedge (adding our 3 models is a plug-in, not a paper) |
| 🧪 [VLA-JEPA](https://arxiv.org/abs/2602.10098) | Latent-world-model-augmented VLA; beats prior methods on **SIMPLER + LIBERO** (highest avg SR on Google Robot) using <1% of the training data | 🎯 latent-WM vs VLA on the exact suites we named |
| 🎚️ [TD-Calibration for VLA](https://arxiv.org/pdf/2604.20472) | ECE-style calibration on VLA action heads | 🎲 the calibration/uncertainty (ECE/RCS) wedge |

🩸 **Every wedge is dead.** No un-done concept remains; only a **measurement consolidation** (3 zero-shot models on one public harness), and RoboDojo's XPolicyLab is already its natural home.

## 🧠 QA/memory alt-direction (the Gemini-ER dashboard) - ALSO scooped (adversarial novelty scan, 2026-08-13)

> The off-proposal alternative was an **embodied-reasoning / world-state MEMORY-QA** benchmark for ER APIs (Gemini-Robotics-ER 2). A full web sweep + an independent adversarial auditor found **every probe already published**: **NOVELTY NOT CONFIRMED (scooped / recombination)**. So *both* directions (robotic execution AND QA/memory) are taken. The "inference-only on a frontier ER API" framing is the **standard eval mode** ([ERQA-Plus](https://arxiv.org/html/2606.17639v2), [FindingDory](https://arxiv.org/pdf/2506.15635) already do it), not a differentiator.

**Table A - the dashboard's 4 probes vs their near-exact published match**

| 🧪 Dashboard probe | 🩸 Near-exact published match (web-verified) |
|---|---|
| **A** · object permanence across turns | [RoboMME](https://arxiv.org/abs/2603.04639) explicit "Permanence" suite · [MemoBench](https://arxiv.org/abs/2606.27537) "disappear-and-reappear object permanence" · ["World Models Lack a Persistent State Core"](https://arxiv.org/abs/2606.20545) ("consistency measured on return") |
| **B** · mid-task re-instruction robustness | [InterruptBench](https://arxiv.org/html/2604.00892) (addition / revision / retraction) · [AdaPlanBench](https://arxiv.org/pdf/2606.05622) · [AgentChangeBench](https://arxiv.org/pdf/2510.18170) |
| **C** · two-agent world-state coherence | [Embodied Multi-Agent Coordination via Dialogue](https://arxiv.org/abs/2605.12920) = *literally this probe* (observation convergence + belief-sensitive messaging) |
| **D** · memory to rollout correlation | [ERIQ](https://arxiv.org/abs/2512.24125) = "ER score correlates with VLA generalization / real-world success" = identical methodology |

**Table B - QA/memory rival landscape by slice (web-verified 2026-08-13)**

| 🗂️ Slice | Status | 🩸 Rival benchmarks (hyperlinked) |
|---|---|---|
| Generic embodied / spatial QA | 🔴 crowded | OpenEQA · VSI-Bench · ERQA · [ERQA-Plus](https://arxiv.org/html/2606.17639v2) · [ESI-Bench](https://arxiv.org/html/2605.18746v1) · [CityEQA](https://arxiv.org/pdf/2502.12532) · [Point-It-Out](https://arxiv.org/pdf/2509.25794) · [Embodied-R1.5](https://arxiv.org/pdf/2606.11324) |
| Episodic / world-state memory QA | 🔴 crowded | [WorldLines](https://arxiv.org/abs/2606.18847) · [FindingDory](https://arxiv.org/pdf/2506.15635) · [eMEM](https://arxiv.org/pdf/2606.03374) · [VL-KnG](https://arxiv.org/pdf/2510.01483) · [RoboMemArena](https://arxiv.org/abs/2605.10921) · [Mem-World](https://arxiv.org/abs/2606.18960) |
| Mid-task re-instruction / intervention | 🔴 occupied | [InterruptBench](https://arxiv.org/html/2604.00892) · [AgentChangeBench](https://arxiv.org/pdf/2510.18170) · [CostBench](https://arxiv.org/html/2511.02734) · [AdaPlanBench](https://arxiv.org/pdf/2606.05622) · [REI-Bench](https://arxiv.org/html/2505.10872) |
| Multi-robot shared world-state | 🔴 occupied | [Embodied Multi-Agent Coordination via Dialogue](https://arxiv.org/abs/2605.12920) · [VIKI-R](https://arxiv.org/pdf/2506.09049) · [AgentComm-Bench](https://arxiv.org/html/2603.20285) · [Gamma-World](https://arxiv.org/pdf/2605.28816) · [3D-Belief](https://arxiv.org/pdf/2605.11367) |

🥇 **Verdict: NOVELTY NOT CONFIRMED for QA/memory too.** Both directions are scooped; the only lane with daylight is a new **execution OOD distribution** (transparent / clutter on DROID/Franka; see the distribution table at the bottom).

## 📐 Cross-venue bar (if the reproduction is written up)
- 🧵 **Workshop / survey section:** the honest home - a measurement note, or the survey's WAS-assessment subsection.
- 📊 **NeurIPS D&B / Evaluations track:** possible fit for a *reproduction/consolidation* - needs executable + documented code, **Croissant** metadata, hosting + licence + maintenance. Non-executable artifact = **desk reject**.
- 🎨 **CVPR / ICCV / ICML main track:** will reject on novelty (the scoop table is the reviewer's ammunition). Do NOT target as a novel benchmark.
- 🤖 **CoRL / RSS:** value real-robot evidence; a sim-only reproduction must justify physical relevance.

## 🧨 Risks and honest moves (extended)

| # | 🧨 Reject axis | 📋 Where it bites | ❌ Why it fails | 🛠️ FIX / honest move |
|---|---|---|---|---|
| **1** | 🆕 Novelty of benchmark | 🎨 CVPR/ICCV/ICML | Fully scooped: [World-in-World](https://arxiv.org/abs/2510.18135), [WorldArena](https://arxiv.org/abs/2602.08971), [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985) baselines already do closed-loop cross-family WM-vs-VLA utility (see scoop table) | 🧭 Do NOT claim novelty. Fold into the survey as a WAS assessment + a reproduction table; credit all priors |
| **2** | 📏 Novelty of metric (WAS) | 🎨 ARR/ICML | "gain over VLA" = World-in-World embodied utility = [DreamZero](https://arxiv.org/html/2602.15922v1) "2x" = [L0-L7 ladder](https://arxiv.org/abs/2606.15032) optimization lift | 📊 Present WAS as an *assessed prior* metric (per-capability curve + CI); cite the three originators; do NOT brand it as ours |
| **3** | 🧪 Ablations | 📊 ICML/CVPR | No matched-budget protocol, no seeds/CI, no human ceiling | 🔬 Fix ONE zero-shot interface; ≥5 seeds, mean + 95% CI; add human ceiling + blind floor (still worth doing for the reproduction table) |
| **4** | 🗃️ Dataset + artifact | 📊 NeurIPS D&B (desk-reject) | No datasheet, no executable harness, no Croissant | 📦 Reuse **DROID/Franka** + [LIBERO](https://www.emergentmind.com/topics/libero) (existing datasheets); release the runner + configs + logs; host with Croissant + maintenance |
| **5** | 🤖 No real-robot evidence | 🦾 CoRL/RSS | Sim/API-only reads as not about physical robots | 🦿 **DROID/Franka is a REAL arm** ([RoboArena](https://arxiv.org/html/2506.18123v1) eval) = genuine real-robot evidence; keep claims to the tested arm, do NOT overclaim |
| **6** | 🎯 Venue fit | 📚 ARR (NLP) | A scooped robotics reproduction is out-of-scope for main tracks | 🧵 Target a workshop / D&B *reproduction* slot, or the survey subsection; not a main-track benchmark |
| **7** | 👻 Fabricated baselines | ⚠️ all (fatal) | `Fast-WAM`, `τ₀-WM`, "Cosmos 3", `H-JEPA` are not real releases | ✅ Cite only web-verified checkpoints: ⚡ [OpenVLA](https://github.com/openvla/openvla)/π0, 🧠 [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985), 🎬 [DreamZero](https://arxiv.org/html/2602.15922v1); drop the rest |
| **8** | 🔬 Claims vs experiments | ⚠️ all (soundness) | Findings written before runs exist | 🧾 Run the 3-model **DROID/Franka** harness (π0-FAST / V-JEPA-2-AC / DreamZero) end-to-end before writing any number; release logs + configs |
| **9** | 🌌 WFM cannot act zero-shot | 🧊 the core design | Cosmos has NO zero-shot action head - it only generates/grades video ([WorldBench](https://world-bench.github.io/)); the "4-family" claim is really 3 | 🎬 State plainly: the execution comparison is **3-family** (⚡🧠🎬). Report WFM only as a *video-quality reference* (WorldBench), never as a robot |
| **10** | 🗺️ DenseWorld zero-shot nav | 🧊 the "core novelty" | No family drives zero-shot; needs a trained nav head + photoreal 3DGS recon (breaks no-training + GPU-light) | ❌ Drop DenseWorld from the zero-shot benchmark. If ever built, it is a training-heavy Phase-3, not zero-shot execution - label it so |
| **11** | 🧊 Zero-shot interface mismatch | 🧊 fairness of WAS | Families emit different outputs (action vs latent vs video); only **3 of 9** listed models act zero-shot on one arm | 🔌 Fix ONE interface on the **DROID/Franka** arm: ⚡ **π0-FAST** (actions, language), 🎬 **DreamZero** (actions, language), 🧠 **V-JEPA-2-AC** (image-goal MPC). The other 6 (OpenVLA, I-JEPA, V-JEPA 2, MC-JEPA, UVA, Cosmos-Policy) are encoders or need per-embodiment training = OUT. Footnote the image-goal-vs-language mismatch |

🥇 **Decision (honest):** retire the standalone P2 benchmark. 🔀 Fold into Paper-1 as **📊 WAS-assessment (credit priors) + 🔁 3-model DROID/Franka reproduction table (π0-FAST / V-JEPA-2-AC / DreamZero)**. Lead with measurement/consolidation value, never novelty.

## 🔗 Sources
- 🌍 Priors (execution / utility): [World-in-World 2510.18135](https://arxiv.org/abs/2510.18135) · [site](https://world-in-world.github.io/) · [code](https://github.com/World-In-World/world-in-world) · [WorldArena 2602.08971](https://arxiv.org/abs/2602.08971) · [WorldArena 2.0 2605.17912](https://arxiv.org/html/2605.17912v1) · [RoboWM-Bench 2604.19092](https://arxiv.org/abs/2604.19092) · [RoboDojo 2607.04434](https://arxiv.org/abs/2607.04434) · [WorldSimBench](https://iranqin.github.io/WorldSimBench.github.io/assets/WorldSimBenchmark.pdf)
- 🤖 Families (zero-shot policies): ⚡ [OpenVLA](https://github.com/openvla/openvla) · 🧠 [V-JEPA-2-AC 2506.09985](https://arxiv.org/abs/2506.09985) · 🎬 [DreamZero 2602.15922](https://arxiv.org/html/2602.15922v1) · [site](https://dreamzero0.github.io/)
- 🎯 Harness (reuse, no training): [SimplerEnv](https://github.com/simpler-env/SimplerEnv) · 📚 [LIBERO](https://www.emergentmind.com/topics/libero)
- 🌌 WFM video-quality (not execution): [WorldBench](https://world-bench.github.io/)
- 🧪 Related scoopers: [VLA-JEPA 2602.10098](https://arxiv.org/abs/2602.10098) · [TD-Calibration-VLA 2604.20472](https://arxiv.org/abs/2604.20472) · [WM-Eval L0-L7 position 2606.15032](https://arxiv.org/abs/2606.15032)
- 📐 Venue guidelines: [CVPR 2025](https://cvpr.thecvf.com/Conferences/2025/ReviewerGuidelines) · [ICCV 2025](https://iccv.thecvf.com/Conferences/2025/ReviewerGuidelines) · [NeurIPS D&B](https://neurips.cc/Conferences/2023/DatasetsAndBenchmarks/ReviewGuidelines) · [NeurIPS 2026 Eval&Datasets](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets) · [CoRL 2026](https://www.corl.org/contributions/instruction-for-reviews) · [RSS](https://roboticsconference.org/reviewps/) · [ARR](http://aclrollingreview.org/reviewerguidelines)


## 🆕 Where novelty survives: the OOD *distribution* (protocol + metric are already taken)

> "Distribution" = the stuff the robot faces (objects, scenes, physics), not the scoring. Every suite tests one narrow distribution; the one open move is dropping the same 3 zero-shot models into a distribution no suite covers and asking *"does the world-model advantage survive here?"* ⚠️ Only **observation-space** shifts stay zero-shot on the shared 🤖 **DROID/Franka** arm; a shift that changes the **body or physics** needs a different embodiment = training = out.

| 🆕 OOD distribution | 🎯 vs today's suites (taken) | 🤔 Why it's OOD / interesting | 🤖 Zero-shot on DROID/Franka? | 📦 Nearest existing data (wrong-embodiment) |
|---|---|---|---|---|
| 🔍 **Transparent / reflective** (glass, steel, water) | opaque, well-lit objects | depth + video prediction break on non-Lambertian surfaces | ✅ **YES** - observation-only (material swap) | ClearGrasp, DREDS (perception-only → curate on DROID) |
| 🗑️ **Dense clutter / occlusion** (crammed drawer, retrieve-from-heap) | tidy, ≤5 objects | hidden-state + long-tail; where a WM *should* help most | ✅ **YES** - observation-only (add distractors) | GraspNet-1B, MetaGraspNet (perception-only) |
| 🧵 **Deformable / granular** (cloth, cable, pour rice, dough) | rigid, opaque objects | rigid-body WMs cannot roll out deformation | ❌ **NO** - different physics + non-DROID body | SoftGym, DaXBench (FleX / JAX) |
| 🔨 **Contact-rich / force** (peg-insert, wipe, cut, screw) | quasi-static pick-place | dynamics / friction the video WMs never modeled | ❌ **NO** - force + different obs interface | ManiSkill, FurnitureBench, IndustReal |
| 🧑 **Human-in-scene handover** (person hands / blocks the object) | robot alone | reactive social forecasting under a real manipulator | ❌ **NO** - Panda + scripted human, diff interface | HandoverSim, DexH2R |

✅ **Bottom line:** only **transparent + dense-clutter** stay zero-shot on the shared arm (they change *only what the camera sees*) - that is the feasible novel split: a **measurement/consolidation** contribution (new distribution, not new protocol/metric). The other 3 change the body or physics, so they break zero-shot and become a training-heavy Phase-3.
