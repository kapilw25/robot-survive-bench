# CONTEXT: robot-survive-bench

Durable orientation for any session or agent working in this repo. Read this first, then `plan/` for depth. Follows the working conventions below (no em-dashes, tables over prose, verified refs only).

## One line
A zero-shot (inference only, no training) ROBOTIC-EXECUTION benchmark asking one question: does a world model's advantage over a direct VLA policy SURVIVE an out-of-distribution surprise?

## TL;DR
| Field | Value |
|---|---|
| What it measures | Whether a world-model's success-rate edge over a direct VLA survives an OOD observation shift |
| Shared arm | DROID / Franka (RoboArena-style closed loop) |
| OOD splits (stay zero-shot) | transparent / reflective objects; dense clutter / occlusion |
| Metric | behavioural Task Success Rate (TSR) |
| Headline | dWAS = WAS(OOD) - WAS(normal) = "did the edge survive?" |
| WAS formula | WAS = (success_worldmodel - success_VLA) / (success_VLA + epsilon) |
| Contribution type | measurement / consolidation (a NEW distribution, not a new protocol or metric) |
| Status | planning stage; `plan/` holds engineering + dataset + risk docs |

## Families and models (zero-shot)
One native action-emitting checkpoint per family on the shared arm; no fine-tuning by us.

| Family | Native zero-shot model | Instruction interface | Verified ref |
|---|---|---|---|
| VLA (direct action) | pi0-FAST (trained on DROID) | language | openpi DROID example |
| LWM (latent world model) | V-JEPA-2-AC (Franka, image-goal MPC) | goal image | arXiv 2506.09985 |
| WAM (world-action model) | DreamZero (native Franka/DROID) | language / verb | arXiv 2602.15922 |

A training-free interface layer (cross-embodiment adapter, encoder-as-cost MPC, planner + scripted PID) extends coverage to 11 of 15 released models. Native-only feasibility is 3.

## OOD splits: what stays zero-shot vs what is out of scope
Only OBSERVATION-space shifts stay zero-shot on the shared arm (they change only what the camera sees). A shift that changes the body or physics needs a different embodiment = training = out of scope.

| OOD distribution | Zero-shot on DROID/Franka? | Why in / out |
|---|---|---|
| Transparent / reflective (glass, steel, water) | YES | observation-only material swap; depth + video prediction break on non-Lambertian surfaces |
| Dense clutter / occlusion (crammed drawer, heap) | YES | observation-only distractors; hidden-state where a WM should help most |
| Deformable / granular (cloth, cable, pour) | NO | different physics + non-DROID body |
| Contact-rich / force (peg-insert, wipe, cut) | NO | force + different obs interface |
| Human-in-scene handover | NO | scripted human + different interface |

## Honest positioning (do not oversell)
| Rule | Detail |
|---|---|
| Contribution | MEASUREMENT / CONSOLIDATION. The novelty is the un-run OOD DISTRIBUTION, not a new protocol or metric. |
| Credit priors | cross-family closed-loop protocol + "advantage over a VLA baseline" are already published: World-in-World (2510.18135), WorldArena (2602.08971), V-JEPA-2-AC (2506.09985), L0-L7 ladder (2606.15032). |
| WAS is not ours | "World Advantage Score" is ACTION-ATLAS's coined metric (Amitava Das). ASSESS it neutrally and credit originators; never brand it as ours. |
| Anti-fabrication | Helix, H-JEPA, Fast-WAM, tau0-WM have no runnable checkpoint or API; keep listed but EXCLUDED. Never invent baselines or refs. |
| Honest ceilings | answers only the weak "does the edge survive glass/clutter?" question; gap is confounded by model size (DreamZero 14B vs pi0 ~3B) + instruction type. Caveat, do not claim a clean architecture win. |

## Key reality corrections (why this differs from the p2 proposal)
The proposal `plan/p2_ACTION_ATLAS_ARXIV.md` was scoped down after a web-verified feasibility + novelty audit (2026-08-12/13).

| Proposal said | Correction | What we do |
|---|---|---|
| 4 families incl. WFM (Cosmos) | WFM only generates video, cannot act zero-shot | 3 families that act (VLA, LWM, WAM) |
| DenseWorld drive-through-crowds is the core novelty | no model drives zero-shot; needs a trained nav head + photoreal recon | drop from zero-shot benchmark; training-heavy Phase-3 reference only |
| WAS + gamma matrix is our contribution | already published | reuse + credit; do not claim novel |
| 4 capability domains via off-HF sims | each needs a different body + training | one arm the models already know: DROID/Franka |
| Score all 10 metrics (incl. prediction + confidence) | a plain VLA emits only moves | keep the behavioural "did it work?" scores only |

## Repo layout
| Path | What |
|---|---|
| `README.md`, `CLAUDE.md` | project summary + working conventions |
| `plan/plan_engineering.md` | aspirational full-benchmark engineering plan (Phase-2+ reference) |
| `plan/plan_dataset.md` | robot datasets / sims + converged near-term design |
| `plan/plan_rejections_risks.md` | competitive scoop table, risk table, where novelty survives |
| `plan/p2_ACTION_ATLAS_ARXIV.md(.pdf)` | the original proposal reference |
| `.claude/memory/` | project-local knowledge base (positioning, table preference) |
| `.claude/audit/` | audit rules + rubric + ledgers (em-dash, arxiv slop, quoting, etc.) |
| `.claude/agents/` | parity-auditor + improve-harness agents |
| `.claude/hooks/` | em-dash block, audit gate/guard, post-generation audit |

## Working conventions (enforced; some by hooks)
| Rule | Detail |
|---|---|
| No em-dashes | anywhere; use hyphens or rewrite. A hook blocks them. |
| Verify every ref | exact title, first author, arXiv id, web-verified. Unverifiable = omit, never invent. |
| Tables over prose | long prose is hard to eyeball. |
| Commit messages | single-quoted; do NOT add a Co-Authored-By trailer. |
| Scope | ROBOTIC EXECUTION ONLY (a robot acting closed-loop). No video-QA / reasoning-QA / memory-QA. |
