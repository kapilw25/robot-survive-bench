# robot-survive-bench

A zero-shot (inference only, no training) ROBOTIC-EXECUTION benchmark that asks one question: does a world model's advantage over a direct VLA policy **survive an out-of-distribution surprise**?

## What it is
- Shared arm: DROID / Franka (RoboArena-style closed loop).
- 3 natively zero-shot models, one per family: pi0-FAST (VLA), V-JEPA-2-AC (LWM), DreamZero (WAM). A training-free interface layer (cross-embodiment adapter, encoder-as-cost MPC, planner + scripted PID) extends this to 11 of 15 released models.
- OOD splits that stay zero-shot (observation-space only): transparent / reflective objects, dense clutter / occlusion. Distributions that change the body or physics (deformable, contact-rich, handover) break zero-shot and are out of scope.
- Metric: behavioural Task Success Rate (TSR); headline = dWAS = WAS(OOD) - WAS(normal).

## Positioning (honest)
Measurement / consolidation contribution: a NEW distribution, not a new protocol or metric. The cross-family closed-loop protocol and the World-Advantage-Score idea are credited to prior work (World-in-World, WorldArena, V-JEPA-2-AC, the L0-L7 evaluation ladder). See `plan/plan_rejections_risks.md` for the full competitive scan.

## Repo layout
| 🗂️ Path | 📌 What |
|---|---|
| `plan/v2/` | 📊 **CURRENT**: live frontier-brain board (`README.md` spec, `plan_PIVOT_live_frontier.md` deep dive) |
| `plan/v1/` | 🤖 pre-pivot world-model reproduction (`README.md` spec) |
| `plan/plan_dataset.md` · `plan/plan_rejections_risks.md` | 🔗 shared ref: 📦 dataset menu; 🩸 novelty / scoop ledger |
| `plan/v0_proposal/` · `plan/legacy/` | 📄 original proposal + dashboard; 🗄️ retired full vision |

## Working conventions (follow these)
- NO em-dashes anywhere (use hyphens, or rewrite the sentence).
- Every arXiv / paper reference must be web-verified (exact title, first author, id). Unverifiable = omit, never invent.
- Tables over long prose.
- Commit messages: single-quoted; do NOT add a Co-Authored-By trailer.
- Scope is ROBOTIC EXECUTION ONLY (a robot acting closed-loop). No video-QA / reasoning-QA tasks.
