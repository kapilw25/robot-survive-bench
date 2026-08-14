---
description: Loop-engineered taxonomy builder - harvest verified refs, build the grouped-cell hero taxonomy figure, and DO NOT STOP until it compiles, renders, and passes all gates (Stop hook enforces)
argument-hint: [workspace-dir, default: most recent survey_* dir]
---

Load the **survey-pipeline** skill (`.claude/skills/survey-pipeline/SKILL.md`). This command runs
until the taxonomy deliverable is REAL — the project Stop hook mechanically blocks ending the turn
while gates fail, so do not attempt to wrap up early.

## Arm the loop (first action)
Write `.claude/state/survey_loop.json`:
```json
{"workspace": "<ABSOLUTE path to the survey dir>", "topic": "<topic>",
 "status": "in_progress", "iteration": 0, "max_iterations": 15,
 "min_refs": 60, "min_taxonomy_systems": 40,
 "render_png": "", "eyeball_confirmed": false}
```
Gates (checked by `.claude/hooks/survey_loop_stop.py`; run manually anytime with `--check`):
G1 novelty confirmed · G2 >=min_refs verified deduped refs · G3 hero figure matches the
grouped-cell spec with >=min_taxonomy_systems citations · G4 clean fresh compile · G5 fresh PNG
render · G6 eyeball confirmed.

## Work phases (iterate freely; the hook re-prompts you with whatever still fails)
1. **Harvest refs**: launch 3-5 parallel research agents, each owning a branch of the taxonomy;
   each returns bibtex + TSV for VERIFIED papers only (exact title, first author, year, arXiv ID;
   omit if unverifiable). Dedup by bibkey AND arXiv id before appending to `refs.bib`.
2. **Build the figure**: `figures/fig_taxonomy_main.tex` from
   `templates/fig_taxonomy_REFERENCE.tex` — grouped cells (one per sub-family), one line per
   paper `\textbf{Name}: <trimmed real title>~\citep{key}`, graduated fonts, novelty-axis branch
   shaded secAl->secEl, `\resizebox{!}{0.88\textheight}`, caption + `\Description`.
3. **Compile** (`latexmk -pdf -interaction=nonstopmode`), fix every error/undefined citation.
4. **Render** the figure page (`pdftoppm -png -r 110`), record its path as `render_png` in the
   state file, **Read the PNG** and check: all nodes connected to root, one page, legible leaves,
   no wrapped lines. Only then set `"eyeball_confirmed": true`.

## MANDATORY adversarial audit (before the loop may release)
With gates green, spawn a fresh **general-purpose Agent** to REFUTE the taxonomy:
- "Read `figures/fig_taxonomy_main.tex` and `refs.bib` in <workspace>. (a) Sample 15 random
  figure entries and web-verify each cited paper exists with that title/author/year/arXiv ID —
  any fabrication = REFUTED. (b) Check every figure line's `Name: title` against the refs.bib
  title — a paraphrase that changes meaning = flag. (c) Verify branch assignment sanity for 10
  entries (does the paper actually belong in that sub-family?). (d) Recompile and confirm EXIT 0.
  (e) LEGIBILITY: render the taxonomy figure's page (`pdftoppm -r 150`) and confirm its leaf text
  is NOT smaller than the body-paragraph text; a figure squeezed so small its text is sub-body-size
  is REFUTED (readability failure) even if every entry is correct.
  Default to REFUTED when uncertain. End with exactly `AUDIT VERDICT: ACHIEVED` or
  `AUDIT VERDICT: REFUTED` + findings."
- If REFUTED: remove/fix the offending entries, recompile, re-render, and re-audit with a NEW
  agent. Do NOT set the state to done yourself — the hook flips it when gates pass; the audit
  verdict must be ACHIEVED before you present the result as finished.

Escape hatches: `max_iterations` caps the loop (status becomes `stalled`); the user can disarm by
deleting `.claude/state/survey_loop.json`. Finish by showing the rendered PNG page, the gate
report, and the audit verdict.
