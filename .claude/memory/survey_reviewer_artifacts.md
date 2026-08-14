# Reviewer-mandated survey artifacts (build these in EVERY survey paper)

Origin: CSUR reviewer feedback on *"Weights or Skills?"* (2026-07). Three artifacts a CSUR-grade
survey must contain from the first draft. The `/survey` pipeline (`.claude/skills/survey-pipeline/`)
must generate all three; `tab_landscape` + taxonomy alone are not enough.

## Artifact 1 — Survey Methodology subsection + PRISMA-2020 flow figure

**What:** a `\subsection{Survey methodology...}` (place it as §2.x, NOT a new top-level section, so
hardcoded `\S3.x` strings never renumber) + `figures/fig_prisma.tex`, a two-column PRISMA-2020
flow (ref: `prisma2020` = Page et al., BMJ 2021, doi:10.1136/bmj.n71;
https://www.prisma-statement.org/prisma-2020-flow-diagram).

**Prose must state:** sources searched (arXiv, ACM DL, IEEE Xplore, Google Scholar, venue
proceedings: CoRL/RSS/ICRA/IROS/NeurIPS/ICML/ICLR/CVPR), the date window, representative search
strings, and explicit INCLUSION and EXCLUSION criteria + the metadata-verification protocol.

**Figure must show:** stages Identification -> Screening -> Included, with recorded counts per
stage, in two columns (structured web-search sweeps for the landscape corpus; seed-and-snowball
curation for the taxonomy corpus), merging into one Included box.

**HONESTY RULE (non-negotiable):** only put counts that were actually RECORDED. If a stage's count
was not logged (e.g. candidates discarded at harvest), say so in a dashed "count not logged" box —
never invent a number. Our real recorded numbers: 237 web-search candidates -> 12 duplicates ->
225 verified (landscape) ; 77 curated taxonomy systems ; 7 prior surveys ; 302 systems / 310 refs.

## Artifact 2 — Family comparison as a spec-sheet matrix (not marks-only)

**What:** `tables/tab_branch_limits.tex` as a families x six-axes matrix.
Rows/axes: **data needs, task horizon, transfer, interpretability, safety, characteristic failure
mode.** Columns: the technique families (VLA / code-as-policy / reward synthesis / RL skills /
market skills). Each cell = a house-style mark (`\yy` green check / `\pp` orange tilde / `\nn` red
cross) + a short grounded phrase + a citation. Anchor evidence in Open X-Embodiment (`openx`,
data/transfer) and LIBERO (`libero`, horizon/reuse). Marks-only tables read as thin.

## Artifact 3 — Metric-anchored future directions

**What:** `tables/tab_future_metrics.tex` (metric / definition / named testbed / family stressed)
+ rewritten `sections/future_work.tex` tying each direction to a measurable quantity.
The four metrics: **success-vs-interactions curve, skill-library reuse rate, cross-embodiment
transfer drop, provenance check.** Testbeds: LIBERO-style lifelong streams (`libero`;
https://github.com/Lifelong-Robot-Learning/LIBERO) and Open X-Embodiment held-out-embodiment
splits (`openx`; https://github.com/google-deepmind/open_x_embodiment).

## LaTeX pitfalls (mistakes never to repeat)

- `>{\raggedright\arraybackslash}p{...}` columns REQUIRE `\usepackage{array}` in the preamble
  (compile dies with "Undefined control sequence" otherwise).
- Size a table's label column to its LONGEST bold header — "Interpretability" overflowed
  `0.105\textwidth` at scriptsize (6.7pt overfull); widened to `0.125\textwidth`.
- Narrow comparison cells must be ragged-right; justified text overfulls.
- Avoid forced `\\` inside tikz box text (ugly hyphen breaks); shorten the phrase instead.
- Add every new `\citep` key to `refs.bib` in the SAME edit as the citation.
- Every figure needs `\Description{}` (ACM accessibility) — including `fig_prisma`.
- NO reviewer/rebuttal provenance in the shared source: not in `%` header comments AND not in
  RENDERED text (captions/prose). Sweep BOTH: `grep -rniE "reviewer|referee|rebuttal"` over all
  .tex generally, and again over non-comment lines. Phrase captions by purpose ("the ambiguous
  boundary cases"), never "the reviewer-relevant cases".
- DELIVERABLE TYPE (2026-07-14): when a reviewer asks for a DIAGRAM / plot / "curves" (e.g. F3's
  success-vs-interaction curves), BUILD the figure -- a table + prose does NOT satisfy it, and
  reporting "done" with only a table is an overstatement. Reviewer references that are other papers'
  DATA figures (LIBERO fig1, Open-X data-analysis/overview) are reproduced in STYLE using OUR
  corpus's real recomputed numbers, never their numbers. For a metric with no real results yet
  (future work), draw a SCHEMATIC figure and label it "schematic / target shapes, not measured
  results" in both caption and \Description.
- DATA-FIGURE AUDIT: any figure with hardcoded counts (bar charts, stats) must be audited by an
  agent that INDEPENDENTLY re-tallies the source table (parse tab_landscape row by row) and matches
  every value; sums must reconcile (e.g. all four distribution charts sum to 225). Cite the source
  table in the caption so the numbers are traceable.
- FIGURE LEGIBILITY (audit blind spot fixed 2026-07-14): every figure's rendered text must be
  >= body-text size. `\resizebox{\textwidth}{!}` on a picture WIDER than one text column shrinks
  the font below body (unreadable). The PRISMA fix: UPRIGHT two-column flow with the exclusion
  boxes folded INLINE (red italic sub-line) so it is 2 boxes across, fits the column, and
  resizebox scales the font UP; do NOT use a rotated sidewaysfigure (centring/clipping is fiddly
  on acmsmall). The visual audit MUST render each figure page and compare figure-text height to
  body-text height -- an overlap/style check does not catch tiny fonts.
- CHART COLOUR (2026-07-15): two separate failure modes, both audited on the render. (1) CONTRAST:
  bar/line fills must be mid-dark -- mix toward BLACK (`hue!70!black`), never toward white (`!55`
  pastels wash out against the page). (2) CATEGORICAL DISTINCTNESS: in a chart where each bar/segment
  is a distinct labelled category (year / domain / embodiment / learning signal), give each category
  a DISTINCT colour from a categorical palette; a single flat/monochrome fill across categories is a
  legibility FAIL (drab, reader falls back on labels). Reserving the thesis pole colours (teal =
  weights, blue = skills) means the categorical palette AVOIDS those two hues -- it does NOT mean
  neutralising stat charts to one slate (that over-correction is itself the bug we hit).
- After edits: recompile, then regenerate `main_flat.tex`
  (`latexpand --empty-comments --expand-bbl main.bbl main.tex > main_flat.tex`).

## Verified locations in the current paper (for eyeballing)
§2.1 methodology p5 ; Fig 3 PRISMA p6 ; Table 8 family matrix p14 ; Table 9 metrics p16 ;
§6 future directions p15. Build: 35 pp, 0 errors, 0 undefined, 0 overfull >5pt.
