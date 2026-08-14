# P3 (action-bench): two-paper plan + the WAS assess-not-adopt rule

INTERNAL project strategy. Do NOT state the two-paper plan anywhere in the published survey.

## The plan
- **Paper 1 (current focus):** an arXiv SURVEY of the benchmark / evaluation landscape for "when
  world modeling helps a robot ACT" (framing B). Working title (chosen 2026-08-04): "Do World
  Models Make Better Robots? A Survey of Benchmarks for Predictive Embodied Intelligence". Its remit INCLUDES assessing whether ACTION-ATLAS
  (the benchmark in `overleaf_draft/p3_action_bench/p2_ACTION_ATLAS_ARXIV.pdf`, by Amitava Das) is
  actually novel. Evidence: `overleaf_draft/p3_action_bench/novelty_gap_B_benchmark.md`
  (NOVELTY CONFIRMED, adversarially audited, ACHIEVED). Framing A (a systems / taxonomy survey) is
  archived in `novelty_gap_A_systems.md`.
- **Paper 2 (later):** using paper 1's findings, modify the novelty in the ACTION-ATLAS proposal and
  build + publish the actual benchmark (distributed inference + evaluation + ablation).

## The WAS rule (anti-circularity)
"World Advantage Score (WAS)" is ACTION-ATLAS's OWN coined metric (its abstract + section 5.6), NOT
an established metric. It overlaps conceptually with Yang Yu 2606.15032's "optimization lift /
policy-ranking agreement". So the survey must ASSESS WAS neutrally, never ADOPT it as the survey's
organizing currency (adopting it would be circular). The survey's real novelty is the comprehensive
evaluation-landscape mapping (open-loop vs closed-loop, by capability, by VLA-vs-world-model family),
independent of WAS. `novelty_gap_B_benchmark.md` was de-circularized on 2026-08-04 accordingly.

## Keep it a SURVEY, not a POSITION paper
Paper 1 must be a survey by construction, not a thesis argued in prose. Enforce with the pipeline's
survey artifacts: PRISMA methodology + inclusion/exclusion criteria, a 150-300+ work benchmark
landscape table, a descriptive taxonomy figure, and balanced per-camp assessment. The "prediction
must earn a closed-loop advantage" idea is a FINDING the survey reports, never the paper's stance.
See [survey_reviewer_artifacts.md](survey_reviewer_artifacts.md).
