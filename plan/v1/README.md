# 🤖 v1 - Honest robot-native reproduction (pre-pivot)

🎯 **One line:** run 3 frozen robot-native models on ONE 🦾 DROID/Franka arm, change ONLY what the camera sees (🔍 transparent / 🗑️ clutter), and measure whether the world-model's success edge survives. 📐 Measurement / consolidation, not a new metric.

📎 Backing detail: [`../plan_dataset.md`](../plan_dataset.md) (design + dataset menu), [`../plan_rejections_risks.md`](../plan_rejections_risks.md) (novelty ledger). ➡️ Current direction is [`../v2/`](../v2/README.md) (this v1 is superseded but kept as the reference baselines).

## 🆕 a) Novelty gap (web-verified; every ref linked)

**🤖 Lens 1 - vs robotic-execution benchmarks:** the protocol and metric are already published; only the OOD DISTRIBUTION is open.
| 🧩 Wedge we might have claimed | 🩸 Already shipped by (click to verify) | ⚖️ Verdict |
|---|---|---|
| 🔁 cross-family zero-shot closed-loop WM-vs-VLA | [V-JEPA-2-AC (2506.09985)](https://arxiv.org/abs/2506.09985) · [WorldArena (2602.08971)](https://arxiv.org/abs/2602.08971) · [World-in-World (2510.18135)](https://arxiv.org/abs/2510.18135) | 🩸 [SCOOPED](../plan_rejections_risks.md) |
| 📏 WAS "advantage over VLA" metric | [DreamZero "2x" (2602.15922)](https://arxiv.org/html/2602.15922v1) · [L0-L7 ladder (2606.15032)](https://arxiv.org/abs/2606.15032) | 🩸 [SCOOPED](../plan_rejections_risks.md) |
| 📊 live cross-policy harness | [RoboArena (2506.18123)](https://arxiv.org/abs/2506.18123) · [RoboDojo (2607.04434)](https://arxiv.org/abs/2607.04434) | 🩸 [SCOOPED](../plan_rejections_risks.md) |
| 🔍🗑️ **transparent/reflective + dense-clutter OOD on DROID/Franka** | no closed-loop suite covers it; nearest is perception-only [ClearGrasp](https://github.com/Shreeyak/cleargrasp) · [GraspNet-1B](https://dl.acm.org/doi/abs/10.1177/02783649231193710) · [MetaGraspNet](https://dl.acm.org/doi/10.1109/CASE49997.2022.9926427) | ✅ **[OPEN](../plan_rejections_risks.md) (the only gap)** |

**🧠 Lens 2 - vs frontier-model benchmarks:** ⛔ NOT ENGAGED. v1 tests robot-native models, not frontier LLMs. See [`../v2/README.md`](../v2/README.md) for that lens.

## 📦 b) Datasets (every set linked)
| 🎯 Use | 🗂️ What (click to verify) | 📝 Note |
|---|---|---|
| 🦾 Substrate | [DROID](https://huggingface.co/datasets/cadene/droid) / Franka, [RoboArena](https://arxiv.org/abs/2506.18123)-style closed loop | the shared arm all 3 families know |
| 🧪 Sim harness check | [LIBERO](https://huggingface.co/datasets/lerobot/libero) | Phase-1 plumbing only |
| 🔍🗑️ Curate (OOD) | swap objects to glass/steel (transparent); add distractors (clutter) | observation-only; physics/controls untouched = stays zero-shot |
| 🖼️ Curate FROM (perception-only, wrong-embodiment) | [ClearGrasp](https://github.com/Shreeyak/cleargrasp) · [GraspNet-1B](https://dl.acm.org/doi/abs/10.1177/02783649231193710) · [MetaGraspNet](https://dl.acm.org/doi/10.1109/CASE49997.2022.9926427) | source material, not runnable robot sets |
| 🚫 NOT used | [SIMPLER](https://github.com/simpler-env/SimplerEnv) (WidowX/Google-robot = VLA-only) · DenseWorld (nav, not zero-shot) · [SoftGym](https://github.com/Xingyu-Lin/softgym) / [DaXBench](https://daxbench.github.io/) / [HandoverSim](https://arxiv.org/abs/2205.09747) | break zero-shot or the cross-family comparison |
| 📤 Ship | datasheet + [Croissant](https://github.com/mlcommons/croissant) on [HuggingFace](https://huggingface.co/datasets) | D&B artifact bar |

## 🚀 c) Start steps (max 5; models linked)
1. 🦾 Stand up the [DROID](https://huggingface.co/datasets/cadene/droid)/Franka closed loop; get ONE pick-and-place episode with ⚡ [pi0-FAST](https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README.md) logging success/fail.
2. ➕ Add 🧠 [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985) (image-goal MPC) + 🎬 [DreamZero](https://arxiv.org/html/2602.15922v1) (language); TSR on the normal split, same arm.
3. 🔍🗑️ Curate the OOD split: glass/steel objects + clutter/occlusion (camera-only change).
4. 🏆 Run all 3 on OOD; report TSR + headline dWAS = WAS(OOD) - WAS(normal), with >=5 seeds + 95% CI.
5. 📤 Ship the artifact (datasheet + [Croissant](https://github.com/mlcommons/croissant) + runner + logs); frame as measurement/consolidation, credit priors.
