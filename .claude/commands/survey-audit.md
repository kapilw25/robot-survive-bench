---
description: Final adversarial audit fleet for a survey draft - fabrication, metric tags, consistency, tone/COI, build hygiene (+ scraped-asset subject-presence when the survey scraped source-paper figures); fix and re-audit until every agent returns CLEAN, then refresh main_flat.tex
argument-hint: [workspace-dir, default: overleaf_draft/p1_weights_or_skills]
---

Load the **survey-pipeline** skill (`.claude/skills/survey-pipeline/SKILL.md`). Run the audit
fleet on the workspace (default `overleaf_draft/p1_weights_or_skills/`). This is a LOOP: it ends only when every
auditor returns `VERDICT: CLEAN` — never on your own assessment.

## Round 1 — launch parallel audit agents (one dimension each)
1. **Fabrication** (highest priority): web-verify >=35 sampled bib entries (prioritise recent +
   less-famous): exact title, first author, year, arXiv ID. Duplicate keys, malformed entries.
   Its stance is to REFUTE: a reference is presumed hallucinated until the web search confirms it.
   ALSO: for any figure with hardcoded counts (bar charts / stats figures), INDEPENDENTLY re-tally
   the source table (parse it row by row) and match every number; flag any mismatch and confirm the
   sums reconcile. Confirm schematic/illustrative figures are labelled as such (no fake data as real).
2. **Metric-tag accuracy**: spot-check >=30 comparison-table rows against the actual papers; flag
   only CLEAR errors (real-only system tagged sim; simulator/dataset given a learning paradigm;
   false self-improvement claims).
3. **Consistency**: every count in prose vs actual table row counts (count rows yourself) vs
   figure totals; all \ref resolve; caption counts = real counts. PLACEMENT EXPLAINABILITY: when
   the corpus is PARTITIONED into a core taxonomy (N systems) and a larger landscape/appendix set
   (M works), the methodology must state the EXPLICIT criteria that place a verified work in one set
   vs the other (a decision rule such as axis-placeable / distinct / fully-characterisable), because
   "how each set was harvested" is not the same as "why a work is core vs appendix". FAIL if the N/M
   split appears in counts, captions, or the abstract but no stated placement rule explains it:
   reviewers read an unexplained core-vs-appendix split as arbitrary.
4. **Tone/COI**: read EVERY line of every .tex; promotional emphasis of any single system,
   personal notes/TODOs, em-dashes (including comments), spelling-convention breaks, grammar.
5. **Build hygiene + figure LEGIBILITY**: rebuild; overfull >5pt, undefined refs/citations,
   missing \Description, float-too-large, longtable header repetition. CRITICAL legibility gate
   (an overlap/style-only check MISSES this): for EVERY figure, render its page
   (`pdftoppm -png -r 150`) and compare the figure's rendered text height to the body-paragraph
   text height on the same page. Any figure whose text is SMALLER than body text is a FAIL. Root
   cause is almost always `\resizebox{\textwidth}{!}` wrapping a picture wider than the text
   column, which scales the font DOWN. Also confirm each figure is fully on-page (not clipped) and
   horizontally centred (near-equal left/right margins). COLOUR CONTRAST (data figures) -- a
   text-size-only legibility check MISSES this: on the same render, check every chart's data marks
   (bars / lines / points / wedges) are dark and saturated enough to (a) stand out from the white
   page and (b) be told apart from each other where colour encodes a category. A fill that is a
   light tint of an already-pastel palette (e.g. `!55!white`, or a `!300`-level Tailwind hue tinted
   toward white) washes out against the page and against adjacent bars -- FAIL. Chart fills must be
   mixed toward BLACK (e.g. `hue!70!black`), never toward white; keep the taxonomy figure's pale
   cells as-is but darken the data-viz fills. CATEGORICAL charts (each bar/segment a distinct
   labelled category -- year, domain, embodiment, learning signal) must give each category a
   DISTINCT colour from a categorical palette; a single flat fill across all bars (monochrome) is a
   FAIL -- it reads as drab and forces the reader onto the labels alone. "Reserve the pole colours"
   means the categorical palette AVOIDS the pole hues (teal/blue), NOT that stat charts are stripped
   to one neutral colour.
6. **Scraped-asset subject-presence** (RUN whenever the survey's subject is visually depictable —
   a robot, a molecule, a chip die-shot, a cell, a UI): the subject gallery, results gallery, and
   corpus-at-a-glance collage are MANDATED main-body deliverables. FIRST check they EXIST: if the
   subject is visually depictable and any of the three is absent, that is a FAIL (missing
   deliverable), not a skip. When they exist, audit the whole CANDIDATE POOL, not
   just the panels that reached the final figure. "Largest raster file" is NOT a proxy for
   "relevant figure". Render ALL scraped candidates into labelled CONTACT SHEETS (a grid,
   ~24 tiles/sheet, each tile stamped with a global INDEX + source key/filename; use `montage` /
   `pdftoppm`). A vision pass READS every sheet and classifies EVERY tile into exactly one of
   {subject-present, results-plot, neither}, written to a classification manifest
   (`index, class, source_path`):
   - **subject-present** = the image actually depicts the survey's SUBJECT (define the subject
     class per topic — e.g. a real robot for a robotics survey);
   - **results-plot** = a genuine data/results figure (bar / line / pie / heatmap / scatter /
     coverage);
   - **neither** = EVERYTHING ELSE -> PURGE. Default-REJECT: if a tile is ambiguous, or is a busy
     annotated pipeline/method diagram rather than a clean subject photo or clean plot, mark it
     neither. Typical purge classes: publisher/lab logos, cartoon mascots, decorative icons,
     stock/nature photos, dataset object catalogs (objects with no subject), UI/prompt/text
     screenshots, boxes-and-arrows schematics, game screenshots, empty-scene photos.
   Move every 'neither' tile OUT of the candidate pool (never silently keep); log the purged count
   + a reason per tile. Only 'subject-present' and 'results-plot' survivors may feed compilation
   figures — build the two-bucket way: ONE montage of subject images + ONE montage of results
   plots. PROVENANCE: every compiled panel must carry its source paper + the figure number within
   that paper it was cropped from; reconstruct it by grepping the paper's LaTeX for the
   `\includegraphics` filename (named files) or reading the source PDF (embedded rasters), and mark
   UNVERIFIABLE explicitly when unresolvable. VERIFY each figure number against the actual source
   PDF (fan out one fetch+read agent per paper) — filenames can be cross-wired vs. content; if a
   panel's figure cannot be located, DROP the panel rather than ship it. VECTOR + HYPERLINKED: the
   compilation figure must be a vector figure (TikZ grid or equivalent) with vector text labels and
   each photo embedded at full resolution (pre-cropped, not downscaled) so it zooms without
   pixelation — NEVER a single flat rasterised `.png` montage. Every tile must be a
   `\href{https://arxiv.org/abs/<id>}{...}` hyperlink printing its verified figure number, mirrored
   in a provenance table; confirm the links compiled by decompressing the PDF streams and counting
   `/Subtype/Link` + `arxiv.org/abs/` URIs (plain `strings` misses compressed annotations). LABELS +
   PLACEMENT: per-tile labels must sit on the PAGE background (no baked dark `\fill` strip behind
   each name), with the hyperlinked paper name in the document's own link colour (acmart: node
   `text=ACMDarkBlue`, matching `urlcolor`) and a light tile border so tiles separate on white —
   keep only the figure title/section-band headers dark. Primary compilation/overview figures
   (subject gallery, results gallery, corpus-at-a-glance) belong in the MAIN BODY at the relevant
   section (each `\ref`d in running text), NOT the appendix. FAIL while any un-purged 'neither' tile
   remains in the pool, any compilation figure draws from an unaudited pool, is a flat raster PNG,
   has any panel lacking a traceable hyperlinked figure provenance, has per-tile names on a dark
   strip instead of the page background, or is buried in the appendix when it is a primary overview
   figure. THESIS HERO: Figure~1 (the teaser / first figure the reader meets) must convey the
   survey's ORGANISING AXIS -- the dividing question its title poses -- not merely scope or breadth.
   A scope collage, a photo wall, or a corpus-stats figure placed as Figure~1 is a FAIL: either
   rework the hero so it visualises the thesis (e.g. two labelled poles either side of the axis, with
   the question down the middle) or keep the taxonomy/framework figure as Figure~1. FAIL when
   Figure~1 shows only how much the survey covers rather than what its organising idea is.
   FIGURE-AXIS COHERENCE: the organising axis belongs on the ARGUMENT-MAKING figures (the hero and
   the taxonomy); supporting figures (corpus stats, galleries, methodology, timeline) keep their own
   most-informative axis (year / embodiment / evaluation / chart type) and connect to the thesis via
   (i) a one-line caption tie-back and (ii) a shared palette in which the thesis colours are RESERVED
   for the poles (e.g. teal = weights, blue = skills), while pole-agnostic stat charts get a
   distinct-per-bar categorical palette that AVOIDS the pole hues -- never a single flat/monochrome
   fill). FAIL if every figure is forced onto the thesis axis (monotony and
   information loss), or if a supporting figure neither ties back to the thesis in its caption nor
   shares the palette.
Each returns findings most-severe-first + `VERDICT: CLEAN` or `VERDICT: ISSUES`.

## Fix + re-audit loop
- Triage findings (verify each is real before acting — auditors can be wrong; push back with
  evidence when they are). Apply fixes; recompile clean.
- **SendMessage the SAME agents** (context intact) listing exactly what you changed; each must
  re-verify its own findings and return a fresh verdict. New issues -> fix -> repeat.
- Exit condition: EVERY auditor launched reports `VERDICT: CLEAN` in the same round.

## After the clean bill
1. Write `<workspace>/audit_report.md`: date, per-dimension verdict table (every round), list of
   fixes applied, ending with the exact line `ALL AUDITS CLEAN` (this feeds Stop-hook gate G8 —
   NEVER write that line while any auditor still reports issues).
2. Regenerate the single-file copy: `latexpand --empty-comments --expand-bbl main.bbl main.tex >
   main_flat.tex`; verify it compiles standalone to the same page count; diff-check it is current.
3. Report a final status table (dimension x round verdicts), page count, and remind the user to
   bump the shared PDF version (vN) — do NOT git push (the user pushes themselves).
