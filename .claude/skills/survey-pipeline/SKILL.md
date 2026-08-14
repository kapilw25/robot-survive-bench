---
name: survey-pipeline
description: Build a CSUR-style survey paper for ANY topic - websearch novelty-gap discovery first, then verified reference harvesting, grouped-cell forest taxonomy figure, comparison tables, audit fleet, and a loop that does not stop until the taxonomy compiles. Use for "new survey", "novelty gap", "taxonomy figure", "survey paper on X".
---

# Survey Pipeline

Reproduces the methodology that built *"Weights or Skills? A Survey of Robot-Learning Techniques"*
(ACM CSUR format, 33 pp, 310 verified refs, 1 hero taxonomy). Command flow:

```
/survey <topic>   <-- ONE-SHOT master: arms full_pipeline gates G1-G8 and chains all phases
  = /novelty-scan -> /survey-init -> /taxonomy-loop -> tables + prose + corpus figures ->
      (gate G1)        (scaffold)     (gates G2-G6)     (gate G7)
    compilation galleries (subject / results / collage, MAIN BODY) -> /survey-audit
      (only if the subject is visually depictable)                     (gate G8: ALL AUDITS CLEAN)
```
Every phase ends with a fresh ADVERSARIAL AUDIT agent (default-REFUTED stance) that must return
`AUDIT VERDICT: ACHIEVED`; audit failures are work items, never stop conditions. When an auditor
exposes a recurrable mistake class, patch the pipeline itself (commands/templates/this file) and
log it under `## Lessons` below.

**Iron rules (apply to every phase):**
1. **Websearch-verified only.** Every paper cited must be confirmed real by web search: exact
   title, first author, year, arXiv ID. Unverifiable -> OMIT. Never invent metadata.
2. **Novelty before writing.** No scaffolding until `novelty_gap.md` holds `NOVELTY CONFIRMED:
   <organizing axis>` backed by a coverage matrix of >=10 real surveys (the "empty cell").
3. **Publication tone.** No em-dashes anywhere (use `--` in comments, rewritten prose otherwise).
   British spelling (organise/generalise). No personal notes, TODOs, venue self-reference, or
   promotional emphasis of any one system (COI). Appendices AFTER references (`\clearpage`,
   `\appendix`). Every figure gets `\Description{}` (ACM accessibility requirement).

## File manifest (what a finished survey contains; mirror of overleaf_draft/p1_weights_or_skills/)

| File | Role | How it is produced |
|---|---|---|
| `main.tex` | acmart shell: class, forest/tikz pkgs, mark macros (\yy \nn \pp \dm), \input order, bib, appendix after refs | from `templates/main_TEMPLATE.tex` |
| `refs.bib` | ALL references | parallel research agents; verified title+author+year+arXiv; dedup by key AND arXiv id |
| `styles/taxonomy_style.tex` | forest style + colour palette (cat-*, secA-G, leaf-*, tx-root) | copy `templates/taxonomy_style.tex` verbatim (topic-agnostic) |
| `figures/fig_taxonomy_main.tex` | THE hero grouped-cell taxonomy (spec below) | from `templates/fig_taxonomy_REFERENCE.tex` |
| `figures/fig_survey_timeline.tex` | related surveys on a horizontal timeline; star = ours | from novelty-scan survey list |
| `figures/fig_architectures.tex` | tikz pipeline of the paper's core mechanism/loop | hand-built per topic |
| `tables/tab_survey_compare.tex` | coverage matrix: topics x prior surveys, OUR column full, others show the empty cell | direct output of novelty-scan |
| `tables/tab_definitions.tex` | operational iff-definitions of the taxonomy's mechanisms ("counts iff" / "does not count") | resolves reviewer boundary cases |
| `tables/tab_compare_main.tex` | longtable: representative systems x (Year, Venue, Ships, Eval, Self-impr.) grouped by branch | counts must reconcile with the figure |
| `tables/tab_compare_<branch>.tex` | per-branch deep-dive matrices (e.g. F/M/S per rung) | one per deep-dive branch |
| `tables/tab_skill_senses.tex` | disambiguation of the field's overloaded term, coloured marks | 4-6 senses x 4 properties |
| `tables/tab_branch_limits.tex` | FULL family spec-sheet: families x six axes (data needs, task horizon, transfer, interpretability, safety, failure mode); mark + grounded phrase + citation per cell | marks-only versions read as thin (reviewer-mandated) |
| `sections/2_*.tex` §2.1 + `figures/fig_prisma.tex` | "Survey methodology" subsection + PRISMA-2020-style flow figure: sources, window, query strings, in/exclusion criteria, verification protocol, counts per stage, and (when a core taxonomy is split from a landscape/appendix set) the explicit core-vs-appendix placement rule (axis-placeable / distinct / fully-characterisable) | ONLY recorded counts; unlogged stages get a dashed "not logged" box, never estimates; subsection placement avoids §-renumbering (reviewer-mandated) |
| `tables/tab_future_metrics.tex` | metric-anchored future work: metric / definition / named testbed / family stressed (e.g. LIBERO lifelong, Open-X held-out embodiments) | future_work prose ties each direction to its metric (reviewer-mandated) |
| `tables/tab_capability_matrix.tex` | one exemplar per camp x ~10 dimensions | neutral: name the CELL, not one system |
| `tables/tab_landscape.tex` | AUTO-GENERATED 200+ work comparison matrix (6 axes, two-tier grouping) | `tools/gen_landscape.py` -- never hand-edit |
| `figures/fig_corpus_overview.tex` | "corpus at a glance": stat callouts (systems, refs, branches, span) + per-area bar chart. MAIN-BODY overview subsection (with the galleries), NOT the appendix | hand-built from the landscape tallies; caption cites `tab_landscape` + `(..., Appendix~X)` pointer; independent re-tally must reconcile |
| `figures/fig_corpus_dist.tex` | distribution charts of the corpus (publication year / evaluation domain / learning signal / embodiment). MAIN-BODY overview subsection, NOT the appendix | recomputed real numbers from the landscape data (never a source paper's numbers); caption cites the table + `(..., Appendix~X)` pointer |
| `figures/fig_subject_gallery.tex`, `figures/fig_results_gallery.tex`, `figures/fig_corpus_glance.tex` | MAIN-BODY vector TikZ galleries built from source-paper figures: subject images, results plots, and a dense collage around a stats card. Per-tile `\href` + printed figure number, labels on the page background in the doc link colour (no dark strip), light tile border | `tools/build_contact_sheets.py` (contact-sheet + classify + PURGE) -> per-paper PDF figure-number verification -> `tools/gen_compilation_figure.py`; only if the subject is visually depictable |
| `tables/tab_panel_provenance.tex` | per-panel source paper + VERIFIED figure number for every gallery tile; every row hyperlinked to arXiv | emitted with the galleries; a panel with no locatable figure is DROPPED, never guessed |
| `sections/0_abstract ... 10_conclusion, limitations, future_work` | prose; §3 = one subsection per branch, deep-dive branch gets per-rung "Membership condition:" sentences | after taxonomy locks |
| `sections/appendix_landscape.tex` | Appendix A framing the landscape table ("focused survey" defence) | after landscape table |
| `main_flat.tex` | single-file copy for sharing | `latexpand --empty-comments --expand-bbl main.bbl main.tex > main_flat.tex` |

## Hero taxonomy figure spec (the fig_taxonomy_main pattern)

See `templates/fig_taxonomy_REFERENCE.tex` for the working example. Non-negotiables:
- `forest`, `grow=east`, forked edges via the shared style; ONE page: `\begin{figure*}[p]` +
  `\resizebox{!}{0.88\textheight}{...}`.
- **Grouped cells**: each sub-family is ONE terminal cell; each line inside =
  `\textbf{Name}: <trimmed REAL paper title>~\citep{key}\\` -- titles trimmed from refs.bib,
  never invented; one line per paper, no wrapping (cell `text width=33em, align=left`).
- **Graduated fonts**: `where n children=0{font=\footnotesize,align=left}{font=\normalsize},
  where level=1{font=\large}, where level=0{font=\Large}` (root > branch > sub-branch > leaf).
- **Font physics**: displayed size = base x min(width-scale, height-scale). Keep the tree
  HEIGHT-bound (width fill < 100%) or leaf text shrinks. ~77 systems -> leaves render ~5pt.
- The novelty-axis branch gets **graduated shading** (secAl -> secEl) encoding the axis
  (e.g. degree of self-improvement); caption explains the shading; `\Description{}` after caption.
- 5-7 branches; deep-dive branch split into rungs/sub-families; every node connected (no
  phantom roots -- use `[, draw=none, fill=none, ...]` if a hidden root is ever needed).

## Landscape matrix (200+ works, reviewer-proofing "too thin")

1. 4-6 parallel agents harvest 45-55 verified papers each in complementary sub-areas
   (avoid-list = all existing bibkeys); output bibtex + TSV `key name year venue subarea focus`.
2. Same agents then tag their own papers on the 6 axes with controlled vocab
   (Ships/Learn/Eval/Embod/SelfImpr); rule: unsure -> `?` (rendered as --), never guess.
3. Dedup (key + arXiv id), then `python3 tools/gen_landscape.py <combined.tsv> <tags.tsv> <out.tex>`
   -- edit SUPER/SUBNAME groupings in the script per topic first.
4. Pure simulators/datasets get Learn = `--` unless defined around one paradigm.

## Scraped-asset compilation (montages/collages built from source-paper figures)

If a survey scrapes figures from cited papers (e.g. to build a subject overview collage), the
CANDIDATE POOL must be subject-audited BEFORE any compilation -- "largest raster file" is NOT a
proxy for "relevant figure" and drags in boilerplate (logos, mascots, icons, stock/nature photos,
dataset object catalogs, UI/prompt/text screenshots, boxes-and-arrows schematics, game
screenshots, empty-scene photos).

1. Contact-sheet ALL candidates (grid, ~24 tiles/sheet, each tile stamped with a global INDEX +
   source key/filename; `montage` / `pdftoppm`).
2. Vision-classify EVERY tile into {subject-present, results-plot, neither} in a manifest
   (`index, class, source_path`). Default-REJECT: ambiguous or busy annotated diagram = neither.
3. PURGE every 'neither' from the pool (log count + reason; never silently keep).
4. Two-bucket compilation: ONE montage of subject images + ONE montage of results plots (mirrors a
   strong dataset paper's overview collage + data-analysis panel).
5. Provenance per panel: source paper + figure number within it (grep the paper's LaTeX for the
   `\includegraphics` filename, or read the source PDF for embedded rasters); mark UNVERIFIABLE
   when it cannot be resolved. This gate is auditor (6) in `/survey-audit`; see
   `.claude/memory/scraped_asset_subject_audit.md`.

## Audit fleet (run via /survey-audit until every agent says CLEAN)

Five parallel agents, one dimension each: (1) fabrication -- web-verify 35+ refs; (2) metric-tag
accuracy; (3) numeric/cross-ref consistency (count table rows yourself); (4) tone/COI/meta-notes
(read every line); (5) build hygiene (overfull >5pt, undefined refs, \Description, float fit).
PLUS a conditional (6) **scraped-asset subject-presence** -- run ONLY when the survey scraped
figures/images from source papers: contact-sheet EVERY scraped candidate, classify each tile
subject-present / results-plot / neither, PURGE the 'neither' from the pool, and confirm every
compiled panel carries traceable provenance (default-REJECT; see the memory note below).
Apply fixes, then SendMessage the SAME agents to re-verify their own findings. Loop until every
agent returns `VERDICT: CLEAN`. Then regenerate `main_flat.tex` and bump the shared PDF version (vN).

## Loop engineering (how "don't stop until taxonomy" works)

`/taxonomy-loop` arms `.claude/state/survey_loop.json` (`status: in_progress`). The project Stop
hook (`.claude/hooks/survey_loop_stop.py`) then BLOCKS every attempt to end the turn and feeds
back the failing gates G1-G6 as the next prompt, until all pass (or `max_iterations`, default 15,
is hit -> status `stalled`). Manual check anytime:
`python3 .claude/hooks/survey_loop_stop.py --check`. Disarm: set `"status":"done"` or delete the
state file.

## Lessons

- 2026-07-13 (reviewer round 2): every survey MUST ship, from the first draft: (1) a Survey
  Methodology subsection + PRISMA-2020 flow (recorded counts only; unlogged stages declared in a
  dashed box, never estimated) that ALSO states the core-vs-appendix placement criteria
  (axis-placeable / distinct / fully-characterisable) whenever a core taxonomy is split from a
  landscape appendix; (2) the family comparison as a families-x-six-axes spec-sheet
  matrix (data needs / task horizon / transfer / interpretability / safety / failure mode) with
  grounded phrases and citations, not marks alone; (3) future directions anchored on measurable
  metrics with named testbeds (success-vs-interactions curve, reuse rate, transfer drop,
  provenance check).
- LaTeX pitfalls: `>{\raggedright\arraybackslash}p{}` needs `\usepackage{array}` (add to the
  main template preamble); size a table's label column to its LONGEST bold header (e.g.
  "Interpretability" overflows 0.105\textwidth at scriptsize); avoid forced `\\` inside tikz box
  text (ugly hyphen breaks); narrow comparison cells must be ragged-right; every new \citep key
  must be added to refs.bib in the same edit.
- Insert new numbered sections as SUBSECTIONS of existing early sections (e.g. methodology as
  §2.1) so hardcoded \S3.x strings in figures/prose never renumber.
- 2026-07-14 (figure LEGIBILITY -- audit blind spot): a figure's rendered text must be at least
  body size, ideally a hair larger. `\resizebox{\textwidth}{!}` on a picture WIDER than one text
  column scales the font DOWN below body size (unreadable). The visual audit must RENDER each
  figure and compare its text height to the body text -- an overlap/house-style check misses this.
  For a wide multi-column diagram (e.g. a two-column PRISMA with side exclusion boxes = 3 boxes
  across), fold the side boxes INLINE (red italic sub-line) so it is only 2 boxes across; then it
  fits the column and `\resizebox` scales the font UP. Avoid rotated `sidewaysfigure` on the small
  acmsmall trim -- centring/clipping is very fiddly.
- 2026-07-14 (deliverable type + data-figure audit): a reviewer asking for a DIAGRAM/curves needs a
  FIGURE, not a table+prose (do not report "done" on a table alone). Reproduce exemplar DATA figures
  (e.g. LIBERO/Open-X style) in STYLE using OUR corpus's recomputed real numbers, never theirs; a
  "survey at a glance" stats figure and per-year/eval/embodiment distribution charts are strong,
  honest additions. Future-work metrics with no results yet -> SCHEMATIC figure labelled "target
  shapes, not measured results". EVERY hardcoded-count figure must be audited by INDEPENDENT re-tally
  of the source table (sums must reconcile), and its caption must cite that table.
- 2026-07-14 (scraped-asset subject audit -- audit blind spot): when a survey scrapes figures from
  source papers to build a montage/collage, the "keep the largest N raster files" heuristic pulls in
  masses of subject-IRRELEVANT junk (logos, mascots, icons, stock/nature photos, dataset object
  catalogs, UI/prompt/text screenshots, boxes-and-arrows schematics, game screenshots, empty-scene
  photos). Auditing only the FINAL montage panels misses this -- ~123 of 362 scraped tiles stayed in
  the repo as junk until caught by hand. Fix: audit the whole CANDIDATE POOL. Contact-sheet every
  tile, three-way classify {subject-present, results-plot, neither}, PURGE 'neither' (default-REJECT
  the ambiguous / busy-diagram tiles), compile the two-bucket way (subject montage + results-plot
  montage), and rebuild per-panel provenance (source paper + figure number) since "largest-file"
  scrapes lose it. Auditor (6) in `/survey-audit`; details in
  `.claude/memory/scraped_asset_subject_audit.md`.
- 2026-07-14 (pipeline reproducibility -- the compilation galleries were a QUALITY gate but not a
  BUILD deliverable): the subject/results/corpus-at-a-glance galleries existed in the reference
  survey but nothing in `/survey` created them for a NEW topic -- no build phase, not in the file
  manifest, audit (6) fired only "if already scraped", and there was no reusable builder (the
  scratch scripts were ephemeral). Hardened: `/survey` Phase 5 now MANDATES the galleries (main
  body) when the subject is visually depictable; the manifest lists `fig_subject_gallery` /
  `fig_results_gallery` / `fig_corpus_glance` / `tab_panel_provenance` / `fig_corpus_overview` /
  `fig_corpus_dist`; audit (6) FAILs when a mandated gallery is absent; and two committed tools
  encode the recipe -- `tools/build_contact_sheets.py` (contact-sheet + classify + purge) and
  `tools/gen_compilation_figure.py` (vector TikZ grid/collage: `[tp]` main body, per-tile `\href`
  + printed figure number, name in ACMDarkBlue on the page background, muted-grey figure number,
  light tile border -- NO dark label strip). Lesson: a convention only lives if a phase builds it,
  the manifest lists it, an auditor fails its absence, AND a committed tool reproduces it.
- 2026-07-14 (figure placement): the corpus-stats figures (`fig_corpus_overview` +
  `fig_corpus_dist`) belong in the MAIN-BODY "corpus at a glance" overview subsection (e.g. \S2.x),
  TOGETHER with the compilation galleries -- not the appendix. The appendix holds only the landscape
  table and the provenance table. Any main-body figure whose counts come from an appendix table must
  carry an explicit `(Table~N, Appendix~X)` caption pointer, and both figures take `[tp]` so the
  overview float cluster settles near its `\ref` instead of drifting.
- 2026-07-14 (chart colour contrast -- legibility blind spot): bar/line/point fills in data figures
  must be mid-dark and saturated. The palette hues are `!300`-level pastels; tinting them toward
  WHITE (`!55`/`!60`) washed the corpus bar charts out so adjacent categories and bar-vs-background
  were hard to tell apart. Fix: mix chart fills toward BLACK (`hue!70!black`), never white -- the
  taxonomy figure keeps its pale cells, but data-viz fills are darkened. The legibility auditor (5)
  now checks colour contrast on the render, not just text size.
- 2026-07-15 (colour contrast, correction -- MONOCHROME is also a fail): darkening was right, but I
  over-corrected by neutralising a MULTI-category chart (the year/domain/embodiment/learning
  distributions) to a single slate -- drab, distinguishable only by label. "Reserve teal/blue for
  the poles" means give categorical charts a distinct-per-bar palette that AVOIDS the pole hues, NOT
  strip them to one colour. Auditor (5) now FAILs a categorical bar chart rendered in a single flat
  fill.
- 2026-07-14 (thesis hero -- Figure 1 must sell the IDEA, not the size): a scope collage (a wall of
  subject photos + a counts card) grabs the eye but communicates breadth, not the survey's
  organising axis; as Figure~1 it sells the wrong story. The Figure-1/teaser must visualise the
  THESIS the title poses. Fix used here: reworked the corpus collage into a two-pole hero -- WEIGHTS
  (frozen VLA policies, left) vs SKILLS (executable, self-improving code-as-policy, right) with a
  "what ships?" spine down the middle and real robots on each side -- placed as Figure~1 on p.2
  (taxonomy -> Figure~2). If you cannot make a photo hero carry the thesis, keep the
  taxonomy/framework figure as Figure~1. Auditor (6) now FAILs a Figure~1 that shows only
  scope/breadth.
- 2026-07-15 (figure-axis coherence -- do NOT force one axis onto every figure): put the organising
  axis only on the argument-making figures (hero + taxonomy). Let supporting figures keep their most
  informative axis (year / embodiment / evaluation / chart type) and bind them to the thesis with
  (a) a one-line caption tie-back and (b) a shared palette that RESERVES the thesis colours for the
  poles (teal = weights, blue = skills), while pole-agnostic stat charts use a distinct-per-bar
  categorical palette that avoids those hues (never a single flat/monochrome fill).
  Re-slicing every figure by the thesis axis reads as thin and loses information. A per-pole-over-
  time chart is a strong thesis-reinforcing addition, but its counts MUST be extracted from the
  taxonomy's own systems + refs.bib years (never invented) with a caption that states the coverage
  bias. Auditor (6) now checks figure-axis coherence.
- 2026-07-15 (Overleaf packaging -- keep the upload tree SOURCE-ONLY): Overleaf caps a manual upload
  at ~180 files and chokes on the raw scrape pool. Keep only the images actually `\includegraphics`'d
  in the tree: `grep -rhoE '\\includegraphics[^{]*\{[^}]+\}'` the live .tex, copy JUST those into
  `figures/img/`, and move the raw per-paper pool, spare tiles, `legacy/`, and reference notes into a
  `no_upload/` folder you do NOT upload to Overleaf (65 tiles vs a 500 MB pool -> ~112 upload files).
  Add a `.latexmkrc` with `$out_dir='no_upload/build'` so every local `latexmk` routes ALL build
  artifacts (pdf/aux/log/fls/fdb/out/blg/bbl) out of the source tree; the committed eyeball PDF is
  `no_upload/build/main.pdf`. Do NOT upload `.latexmkrc` to Overleaf ($out_dir breaks its preview).
  Commit `figures/img/` (the used tiles) so a `git clean` cannot wipe the figures (it did once).
