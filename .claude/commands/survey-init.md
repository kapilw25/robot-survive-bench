---
description: Scaffold a full CSUR-format survey project (acmart, sections, tables, figures, styles) for a topic whose novelty gap is already confirmed
argument-hint: <topic> [workspace-dir]
---

Load the **survey-pipeline** skill (`.claude/skills/survey-pipeline/SKILL.md`). Topic: **$ARGUMENTS**

## Pre-flight gate
The workspace's `novelty_gap.md` MUST exist and contain `NOVELTY CONFIRMED:`. If it does not,
STOP and run `/novelty-scan` first — no scaffolding without a confirmed gap.

## Scaffold (mirror the manifest table in SKILL.md)
1. Create the tree: `sections/ tables/ figures/ styles/` in the workspace
   (default `survey_<slug>/`, or the second argument if given). Also create `no_upload/` (local-only
   material never uploaded to Overleaf: raw scrape pool, spare tiles, legacy, references) and a
   `.latexmkrc` with `$out_dir='no_upload/build';` so build artifacts route out of the source tree
   and the uploaded tree stays source-only (Overleaf caps manual uploads at ~180 files).
2. `main.tex` <- `templates/main_TEMPLATE.tex` with placeholders filled for this topic
   (title, authors TBD, CCS, keywords; branch label macros renamed to the topic's branches).
3. `styles/taxonomy_style.tex` <- copy from templates verbatim (topic-agnostic palette).
4. Section stubs `0_abstract` through `10_conclusion` + `limitations`, `future_work`,
   `appendix_landscape` — each with `\section`/`\subsection` heading and a one-line scope comment.
5. `tables/tab_survey_compare.tex` + `figures/fig_survey_timeline.tex` from the novelty-scan
   outputs (these are real content already, not stubs).
5b. Reviewer-mandated artifacts (see SKILL.md Lessons; stub now, fill during the pipeline):
   `figures/fig_prisma.tex` (methodology flow; log harvest counts from day one so the figure
   never needs estimates), `tables/tab_future_metrics.tex` (metric/definition/testbed/family),
   and plan `tab_branch_limits` as the families-x-six-axes spec matrix.
6. `refs.bib` seeded with the verified surveys from `novelty_gap.md` (keys `survey_*`).
7. Verify the skeleton compiles: `latexmk -pdf -interaction=nonstopmode main.tex` — fix until
   EXIT 0 before reporting done.

## Conventions locked in from the start
British spelling; zero em-dashes; neutral tone (no system singled out promotionally); every figure
gets `\caption` + `\Description`; appendix input goes AFTER `\bibliography` behind `\clearpage`.

## MANDATORY adversarial audit (scaffold gate)
Spawn a fresh **general-purpose Agent** to REFUTE the scaffold before you call it done:
- "Compile the workspace yourself (`latexmk -pdf`), confirm EXIT 0 and 0 undefined citations.
  Check every manifest file from SKILL.md exists and is non-empty. Cross-check that every survey
  cited in `tables/tab_survey_compare.tex` and `refs.bib` appears verbatim in `novelty_gap.md`
  (anything extra was hallucinated during scaffolding — flag it). Check conventions: 0 em-dashes,
  `\Description` present in figure stubs, appendix input after `\bibliography`. End with exactly
  `AUDIT VERDICT: ACHIEVED` or `AUDIT VERDICT: REFUTED` + findings."
- If REFUTED: fix and re-audit with a new agent until ACHIEVED.

Finish by printing the tree, the compile result, the audit verdict, and recommending `/taxonomy-loop`.
