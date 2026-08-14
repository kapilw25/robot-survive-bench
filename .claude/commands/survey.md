---
description: ONE-SHOT end-to-end survey builder for a NEW topic - novelty scan, scaffold, taxonomy loop, tables, prose, audit fleet. Arms the Stop-hook so the agent CANNOT stop until every intended file exists, compiles, and carries a current ALL-AUDITS-CLEAN bill.
argument-hint: <new topic, e.g. "tactile sensing for dexterous manipulation">
---

Load the **survey-pipeline** skill (`.claude/skills/survey-pipeline/SKILL.md`). Build a complete
CSUR-format survey for the topic: **$ARGUMENTS**

This is the MASTER pipeline. You do not decide when it is finished -- the Stop hook does. Audit
findings are never a reason to stop; they are the next work item.

## Step 0 -- ARM THE FULL LOOP (do this before anything else)
Write `.claude/state/survey_loop.json`:
```json
{"workspace": "<ABSOLUTE path>/survey_<slug>", "topic": "$ARGUMENTS",
 "status": "in_progress", "iteration": 0, "max_iterations": 40,
 "full_pipeline": true,
 "min_refs": 60, "min_taxonomy_systems": 40,
 "min_sections": 10, "min_tables": 6,
 "render_png": "", "eyeball_confirmed": false}
```
With `full_pipeline: true` the hook enforces ALL gates before any stop is allowed:
G1 novelty · G2 verified refs · G3 hero taxonomy figure · G4 clean compile · G5 fresh render ·
G6 eyeballed · **G7 every intended file substantive (sections, tables, timeline, main_flat)** ·
**G8 a CURRENT `audit_report.md` containing 'ALL AUDITS CLEAN'** (it goes stale automatically if
any source changes afterwards -- edits re-open the loop by design).

## Phases (follow each command file's instructions, including its own adversarial audit agent)
1. **`/novelty-scan $ARGUMENTS`** (.claude/commands/novelty-scan.md) -- websearch >=10 real
   surveys, coverage matrix, empty cell, `novelty_gap.md` with `NOVELTY CONFIRMED:`; audit agent
   must return ACHIEVED. If the gap is refuted, pivot the axis and repeat -- do not proceed.
2. **`/survey-init $ARGUMENTS`** (.claude/commands/survey-init.md) -- scaffold the tree from
   templates into the workspace; skeleton must compile; audit agent ACHIEVED.
3. **`/taxonomy-loop`** (.claude/commands/taxonomy-loop.md) -- parallel verified ref harvesting,
   hero grouped-cell figure, compile, render, eyeball; audit agent samples+web-verifies entries.
4. **Tables + prose + corpus figures**: build the manifest tables (definitions, compare_main,
   per-branch, skill-senses analogue, branch_limits, capability matrix, future_metrics, landscape
   via `tools/gen_landscape.py`); the corpus-at-a-glance stats figure (`fig_corpus_overview`) and
   the per-year / evaluation / learning-signal / embodiment distribution charts (`fig_corpus_dist`),
   both from the landscape data with recomputed real numbers, placed in a MAIN-BODY "corpus at a
   glance" overview subsection (e.g. \S2.x, together with the Phase-5 compilation galleries) -- NOT
   the appendix, which holds only the landscape table and the provenance table -- with captions that
   cite the landscape table and add an explicit "(..., Appendix~X)" pointer since that table sits
   later; and all prose sections (British spelling, zero em-dashes, neutral tone, membership
   conditions per rung, appendix after refs).
5. **Compilation galleries** (BUILD unless the subject is not visually depictable) -- these are
   MANDATED main-body deliverables, not optional. Scrape source-paper figures and build a
   **subject gallery**, a **results gallery**, and a **corpus-at-a-glance collage**. Steps:
   contact-sheet ALL scraped candidates (`tools/build_contact_sheets.py`); vision-classify every
   tile {subject-present / results-plot / neither}; PURGE 'neither' from the pool (log count +
   reason); VERIFY each surviving panel's source figure number against the paper's PDF (fan out one
   fetch+read agent per paper -- filenames can be cross-wired vs content; DROP any panel whose
   figure cannot be located). Render each gallery as a VECTOR TikZ grid via
   `tools/gen_compilation_figure.py` (full-resolution tiles, per-tile `\href` + printed figure
   number, labels on the PAGE background in the doc link colour with NO dark strip, light tile
   border), place it in the MAIN BODY and `\ref` it in running text, and emit a per-panel provenance
   table. See SKILL 'Scraped-asset compilation' and memory `scraped_asset_subject_audit.md`.
6. **`/survey-audit`** (.claude/commands/survey-audit.md) -- the 6-agent fleet (fabrication,
   metric-tags, consistency, tone/COI, build-hygiene, and scraped-asset subject-presence). **When an
   auditor finds mistakes: fix, message the SAME agent to re-verify, repeat.** Only when every agent
   returns VERDICT: CLEAN in the same round, write `<workspace>/audit_report.md` (per-dimension
   verdicts + date) ending with the exact line `ALL AUDITS CLEAN`, then regenerate `main_flat.tex`.

## Self-improvement of the pipeline itself (each audit round)
When an auditor exposes a mistake CLASS the pipeline allowed (not just an instance) -- e.g. a
hallucinated ref that slipped a harvest prompt, a tag vocabulary gap, a convention the templates
missed -- PATCH the pipeline so it cannot recur: update the relevant
`.claude/commands/*.md`, `.claude/skills/survey-pipeline/SKILL.md`, templates, or
`tools/gen_landscape.py`, and append one line to the `## Lessons` section of SKILL.md (create it
if absent) recording what was hardened and why.

## Discipline
- Never end the turn early; if you try, the hook re-prompts you with the failing gates.
- Never write `ALL AUDITS CLEAN` while any auditor reports issues -- that is falsifying the gate.
- Never set state `status` to done yourself; the hook flips it when reality passes.
- Escape hatches for the USER only: delete `.claude/state/survey_loop.json`, or raise/lower
  `max_iterations` (40 default; on cap the status becomes `stalled` and stopping is allowed).
- Do not git push -- the user pushes themselves.

Finish (= when the hook finally releases) by presenting: the rendered taxonomy PNG, the gate
report (`python3 .claude/hooks/survey_loop_stop.py --check`), the audit table, page count, and
the suggested `git_push.sh` message for the user to run.
