# robot-survive-bench: honest positioning + the WAS assess-not-adopt rule

## What this benchmark is
A zero-shot (inference only, no training) ROBOTIC-EXECUTION benchmark: does a world model's advantage over a direct VLA policy SURVIVE an out-of-distribution surprise (transparent objects / dense clutter) on one shared DROID/Franka arm? Metric: behavioural Task Success Rate; headline dWAS = WAS(OOD) - WAS(normal). Three native zero-shot models (pi0-FAST / V-JEPA-2-AC / DreamZero), extended to 11 of 15 released models via a training-free interface layer.

## Honest positioning (do not oversell)
This is a MEASUREMENT / CONSOLIDATION contribution: the novelty is the un-run OOD DISTRIBUTION, not a new protocol or a new metric. The cross-family closed-loop protocol and the "advantage over a VLA baseline" idea are already published; credit them: World-in-World (2510.18135), WorldArena (2602.08971), V-JEPA-2-AC (2506.09985), the L0-L7 evaluation ladder (2606.15032). Both the robotic-execution and the QA/memory directions were adversarially novelty-scanned and came back scooped; the full competitive scan lives in `plan/plan_rejections_risks.md`.

## The WAS rule (anti-circularity)
"World Advantage Score (WAS)" is ACTION-ATLAS's OWN coined metric (its abstract + section 5.6, by Amitava Das), NOT an established metric; it overlaps with the L0-L7 ladder's "optimization lift / policy-ranking agreement" (2606.15032). ASSESS WAS neutrally and credit its originators; never brand it as ours.

## Scope guardrails
ROBOTIC EXECUTION ONLY (a robot acting closed-loop). No video-QA / reasoning-QA / memory-QA tasks. Only observation-space OOD (transparent / clutter) stays zero-shot on the shared arm; distributions that change the body or physics (deformable, contact-rich, handover) break zero-shot and are out of scope. Related: [[prefer_tables_over_prose]].
