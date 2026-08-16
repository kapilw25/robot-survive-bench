# 🤖 v1 - Honest robot-native reproduction (pre-pivot)

🎯 3 frozen robot-native models on ONE 🦾 DROID/Franka arm; change only what the camera sees (🔍 transparent / 🗑️ clutter); measure whether the world-model edge survives (measurement/consolidation, not a new metric). Backing: [`../plan_dataset.md`](../plan_dataset.md) · [`../plan_rejections_risks.md`](../plan_rejections_risks.md); current direction [`../v2/`](../v2/README.md).

## 🆕 Novelty gap (web-verified; every ref linked)
| 🧩 Wedge | 🩸 Already shipped by (click) | ⚖️ Verdict |
|---|---|---|
| 🔁 cross-family zero-shot closed-loop WM-vs-VLA | [V-JEPA-2-AC (2506.09985)](https://arxiv.org/abs/2506.09985) · [WorldArena (2602.08971)](https://arxiv.org/abs/2602.08971) · [World-in-World (2510.18135)](https://arxiv.org/abs/2510.18135) | 🩸 [SCOOPED](../plan_rejections_risks.md) |
| 📏 WAS "advantage over VLA" metric | [DreamZero "2x" (2602.15922)](https://arxiv.org/html/2602.15922v1) · [L0-L7 ladder (2606.15032)](https://arxiv.org/abs/2606.15032) | 🩸 [SCOOPED](../plan_rejections_risks.md) |
| 📊 live cross-policy harness | [RoboArena (2506.18123)](https://arxiv.org/abs/2506.18123) · [RoboDojo (2607.04434)](https://arxiv.org/abs/2607.04434) | 🩸 [SCOOPED](../plan_rejections_risks.md) |
| 🔍🗑️ **transparent + dense-clutter OOD on DROID/Franka** | no closed-loop suite covers it; nearest perception-only [ClearGrasp](https://github.com/Shreeyak/cleargrasp) · [GraspNet-1B](https://dl.acm.org/doi/abs/10.1177/02783649231193710) · [MetaGraspNet](https://dl.acm.org/doi/10.1109/CASE49997.2022.9926427) | ✅ **[OPEN](../plan_rejections_risks.md) - the only gap** |
| 🧠 vs frontier-model benchmarks (Lens 2) | not engaged here; v1 tests robot-native models, not frontier LLMs | ➡️ see [`../v2/README.md`](../v2/README.md) |

## 📦 Datasets + 🚀 build steps (every set/model linked)
| 🔧 Kind | 🎯 Item | 📄 Detail / action |
|---|---|---|
| 📦 Dataset | 🦾 Substrate | [DROID](https://huggingface.co/datasets/cadene/droid) / Franka, [RoboArena](https://arxiv.org/abs/2506.18123)-style closed loop (shared arm all 3 families know) |
| 📦 Dataset | 🧪 Sim harness check | [LIBERO](https://huggingface.co/datasets/lerobot/libero) (Phase-1 plumbing only) |
| 📦 Dataset | 🔍🗑️ Curate (OOD) | swap objects to glass/steel + add clutter/occlusion; observation-only = stays zero-shot |
| 📦 Dataset | 🖼️ Curate FROM (perception-only) | [ClearGrasp](https://github.com/Shreeyak/cleargrasp) · [GraspNet-1B](https://dl.acm.org/doi/abs/10.1177/02783649231193710) · [MetaGraspNet](https://dl.acm.org/doi/10.1109/CASE49997.2022.9926427) (source material, not runnable) |
| 📦 Dataset | 🚫 NOT used | [SIMPLER](https://github.com/simpler-env/SimplerEnv) (VLA-only) · DenseWorld (not zero-shot) · [SoftGym](https://github.com/Xingyu-Lin/softgym) / [DaXBench](https://daxbench.github.io/) / [HandoverSim](https://arxiv.org/abs/2205.09747) |
| 📦 Dataset | 📤 Ship | datasheet + [Croissant](https://github.com/mlcommons/croissant) on [HuggingFace](https://huggingface.co/datasets) (D&B artifact bar) |
| 🚀 Step 1 | 🦾 stand up closed loop | one [DROID](https://huggingface.co/datasets/cadene/droid)/Franka pick-and-place with ⚡ [pi0-FAST](https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README.md) logging success/fail |
| 🚀 Step 2 | ➕ add the other 2 families | 🧠 [V-JEPA-2-AC](https://arxiv.org/abs/2506.09985) (image-goal MPC) + 🎬 [DreamZero](https://arxiv.org/html/2602.15922v1) (language); TSR on the normal split |
| 🚀 Step 3 | 🔍🗑️ curate OOD split | glass/steel objects + clutter/occlusion (camera-only change) |
| 🚀 Step 4 | 🏆 run all 3 on OOD | report TSR + headline dWAS = WAS(OOD) - WAS(normal), with >=5 seeds + 95% CI |
| 🚀 Step 5 | 📤 ship artifact | datasheet + [Croissant](https://github.com/mlcommons/croissant) + runner + logs; frame as measurement/consolidation, credit priors |
