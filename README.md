# robot-survive-bench

**Does a world model's advantage survive an out-of-distribution surprise?**

A zero-shot (inference-only, no training) robotic-execution benchmark. We take frozen policies from three model families and drop them into a distribution no existing suite covers, then measure whether the world-model advantage over a direct VLA baseline survives.

## The question

Existing suites (LIBERO, SIMPLER, RoboDojo, World-in-World) test clean, rigid, opaque objects on a tidy tabletop. `robot-survive-bench` changes only what the camera sees - transparent / reflective objects and dense clutter / occlusion - on the same DROID/Franka arm, so frozen policies still run with no training.

## Families and models (zero-shot)

| Family | Native zero-shot model | Instruction interface |
|---|---|---|
| VLA (direct action) | pi0-FAST | language |
| LWM (latent world model) | V-JEPA-2-AC | image-goal MPC |
| WAM (world-action model) | DreamZero | language |

A training-free interface layer (cross-embodiment adapters, encoder-as-cost MPC, planner + scripted controller) extends coverage to 11 of 15 released models.

## Metric

Behavioural Task Success Rate (TSR). Headline: `dWAS = WAS(OOD) - WAS(normal)` = "did the edge survive?"

## Status

Planning stage. See `plan/` for the engineering plan, dataset plan, and the competitive / rejection-risk analysis.
