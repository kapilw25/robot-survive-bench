# CONTEXT: robot-survive-bench

Durable orientation for any session or agent working in this repo; read this first, then `plan/` for depth (working conventions: no em-dashes, tables over prose, verified refs only).

## 🧭 What it is, families, OOD splits, positioning
| 🏷️ Aspect | 📄 Detail |
|---|---|
| 🎯 One line | zero-shot (inference only, no training) ROBOTIC-EXECUTION benchmark: does a world model's advantage over a direct VLA policy SURVIVE an out-of-distribution surprise? |
| 📊 Measures | whether a world-model's success-rate edge over a direct VLA survives an OOD observation shift |
| 🦾 Shared arm | DROID / Franka (RoboArena-style closed loop) |
| 📏 Metric | behavioural Task Success Rate (TSR); headline dWAS = WAS(OOD) - WAS(normal) = "did the edge survive?"; WAS = (success_worldmodel - success_VLA) / (success_VLA + epsilon) |
| 🧬 Contribution | measurement / consolidation (a NEW distribution, not a new protocol or metric) |
| 🚦 Status | planning stage; `plan/` holds engineering + dataset + risk docs |
| ⚡ Family VLA | pi0-FAST (trained on DROID); language instruction (openpi DROID example); native |
| 🧠 Family LWM | V-JEPA-2-AC (Franka, image-goal MPC); goal-image instruction (arXiv 2506.09985); native |
| 🎬 Family WAM | DreamZero (native Franka/DROID); language / verb (arXiv 2602.15922); native |
| 🔌 Interface layer | training-free (cross-embodiment adapter · encoder-as-cost MPC · planner + scripted PID) extends coverage to 11 of 15 released models; native-only feasibility is 3 |
| 🔍 OOD transparent / reflective | glass/steel/water; zero-shot YES - observation-only material swap; depth + video prediction break on non-Lambertian surfaces |
| 🗑️ OOD dense clutter / occlusion | crammed drawer / heap; zero-shot YES - observation-only distractors; hidden-state where a WM should help most |
| 🧵 OOD deformable / granular | cloth, cable, pour; zero-shot NO - different physics + non-DROID body |
| 🔨 OOD contact-rich / force | peg-insert, wipe, cut; zero-shot NO - force + different obs interface |
| 🧑 OOD human-in-scene handover | zero-shot NO - scripted human + different interface |
| 🙏 Positioning | MEASUREMENT / CONSOLIDATION; the novelty is the un-run OOD DISTRIBUTION, not a new protocol or metric |
| 📚 Credit priors | cross-family closed-loop + "advantage over a VLA baseline" already published: World-in-World (2510.18135), WorldArena (2602.08971), V-JEPA-2-AC (2506.09985), L0-L7 ladder (2606.15032) |
| 📏 WAS is not ours | "World Advantage Score" is ACTION-ATLAS's coined metric (Amitava Das); assess it neutrally and credit originators, never brand it as ours |
| 🚫 Anti-fabrication | Helix, H-JEPA, Fast-WAM, tau0-WM have no runnable checkpoint or API; keep listed but EXCLUDED; never invent baselines or refs |
| ⚠️ Honest ceilings | answers only the weak "does the edge survive glass/clutter?"; gap confounded by model size (DreamZero 14B vs pi0 ~3B) + instruction type; do not claim a clean architecture win |
| 🔀 Reality correction 1 | proposal said 4 families incl. WFM (Cosmos); WFM only generates video, cannot act zero-shot; so 3 acting families (VLA, LWM, WAM) |
| 🔀 Reality correction 2 | proposal made DenseWorld drive-through-crowds the core novelty; no model drives zero-shot (needs trained nav head + photoreal recon); dropped to training-heavy Phase-3 reference |
| 🔀 Reality correction 3 | proposal claimed WAS + gamma matrix as our contribution; already published; reuse + credit, do not claim novel |
| 🔀 Reality correction 4 | proposal used 4 capability domains via off-HF sims; each needs a different body + training; cut to one arm the models know = DROID/Franka |
| 🔀 Reality correction 5 | proposal scored all 10 metrics (incl. prediction + confidence); a plain VLA emits only moves; keep the behavioural "did it work?" scores only |

## 🗂️ Repo layout + working conventions (enforced, some by hooks)
| 🗂️ Path / rule | 📄 What |
|---|---|
| 📄 `README.md`, `CLAUDE.md` | project summary + working conventions |
| 📊 `plan/v2/` (CURRENT) | live frontier-brain robot-execution board: `README.md` spec, `novelty_map.md`, `notes_robobench.md`, `plan_PIVOT_live_frontier.md` |
| 🤖 `plan/v1/README.md` | pre-pivot world-model reproduction spec |
| 📦 `plan/plan_dataset.md` | robot datasets / sims + converged near-term design |
| 🩸 `plan/plan_rejections_risks.md` | competitive landscape table, risk table, where novelty survives |
| 🗺️ `plan/legacy/plan_engineering.md` | aspirational full-benchmark engineering plan (Phase-2+ reference, retired) |
| 📄 `plan/v0_proposal/p2_ACTION_ATLAS_ARXIV.md` (.pdf) | the original proposal reference + gap dashboard |
| 🧠 `.claude/memory/` | project-local knowledge base (positioning, table preference) |
| 🛡️ `.claude/audit/` | audit rules + rubric + ledgers (em-dash, arxiv slop, quoting, table-sprawl) |
| 🤝 `.claude/agents/` | parity-auditor + improve-harness agents |
| 🪝 `.claude/hooks/` | em-dash block, audit gate/guard, post-generation audit |
| 📏 Rule: no em-dashes | anywhere; use hyphens or rewrite (a hook blocks them) |
| 🔗 Rule: verify every ref | exact title, first author, arXiv id, web-verified; unverifiable = omit, never invent |
| 📊 Rule: tables over prose | long prose is hard to eyeball; keep <=2 tables per working-doc md, content inside the tables |
| 💬 Rule: commit messages | single-quoted; do NOT add a Co-Authored-By trailer |
| 🎯 Rule: scope | ROBOTIC EXECUTION ONLY (a robot acting closed-loop); no video-QA / reasoning-QA / memory-QA |
