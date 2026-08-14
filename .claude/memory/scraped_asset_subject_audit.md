# Scraped-asset subject-presence audit (purge irrelevant figures before ANY compilation)

Origin: robot-learning survey, 2026-07-14. To build a real-robot montage we scraped candidate
figures from each cited paper's arXiv e-print / PDF, keeping "the largest N raster files". That
proxy dragged in ~123 of 362 assets that do NOT depict the subject: publisher/lab logos (NVIDIA,
DeepMind), cartoon mascots, decorative icons (snowflakes, reward badges), stock/nature photos (a
COCO cat), dataset object catalogs (YCB fruit, gears, blocks — no robot), game screenshots
(Minecraft frames from LLM-agent papers), boxes-and-arrows pipeline/method diagrams, prompt/text
screenshots, and empty-scene photos (a kitchen). The montage audit only checked "is each MONTAGE
panel a real robot" — it never audited the CANDIDATE POOL, so the junk sat in the repo until the
user caught it by hand.

## The rule (generalises to ANY survey subject)

When a survey scrapes figures/images from source papers, EVERY scraped asset must be verified to
depict the survey's SUBJECT (or be a legitimate results plot) BEFORE it enters any compilation.
"Largest raster file" is NOT a proxy for "relevant figure". Classify every tile into exactly one:
- **subject-present** — the image actually shows the thing the survey is about (define the subject
  class per topic: a real robot, a molecule, a chip die-shot, a UI, a cell — whatever the survey
  studies).
- **results-plot** — a genuine data/results figure: bar / line / pie / heatmap / scatter /
  coverage.
- **neither** — EVERYTHING ELSE -> PURGE. Default-REJECT: if a tile is ambiguous, or is a busy
  annotated pipeline/method diagram rather than a clean subject photo or clean plot, it is neither.

Typical purge classes (boilerplate a "largest-file" scrape drags in): publisher/lab logos,
mascots, decorative icons, stock/nature photos, dataset object catalogs (objects, no subject),
UI/prompt/text screenshots, pure schematic/boxes-and-arrows diagrams, game screenshots,
empty-scene photos.

## Mechanical gate (see /survey-audit — scraped-asset subject-presence agent)

1. Render ALL scraped candidates into labelled CONTACT SHEETS — a grid, ~24 tiles/sheet, each tile
   stamped with a global INDEX + source key/filename (`montage` / `pdftoppm`).
2. A vision pass Reads every sheet and writes a classification manifest — `index, class,
   source_path` for EVERY tile (class in {subject-present | results-plot | neither}).
3. PURGE every 'neither' tile out of the candidate pool; log the count + a reason per tile — never
   silently keep. Only 'subject-present' and 'results-plot' survivors may feed compilation figures.
4. Two-bucket compilation: build ONE montage of subject images and ONE montage of results plots
   (mirrors how strong dataset papers pair an overview collage with a data-analysis panel).
5. PROVENANCE (anti-hallucination): every compiled panel must carry its source paper + the figure
   number within that paper it was cropped from. Reconstruct by grepping the paper's LaTeX for the
   `\includegraphics` filename (named files) or by reading the source PDF (embedded rasters); mark
   UNVERIFIABLE explicitly when it cannot be resolved. "Largest-file" scrapes lose provenance, so
   it must be rebuilt, never guessed. VERIFY figure numbers against the actual source PDF (fan out
   one fetch+read agent per paper); do not trust filenames — they can be cross-wired (we caught two
   RT-2 panels whose filenames were swapped vs. content). If a panel's figure cannot be located in
   the source, DROP the panel (we dropped a SPiRL maze that did not exist as a figure) rather than
   ship an untraceable image.

## Vector-PDF, zoomable, hyperlinked (never ship a flat raster montage)

A pre-rendered PNG montage fails two things reviewers need: it pixelates on zoom (text + photos
baked to one raster) and it is not verifiable (no way to reach the source). Build compilation
figures as a VECTOR figure instead (TikZ grid, or equivalent):
- **Vector text**: band headers and per-tile labels are real text nodes (crisp at any zoom), not
  pixels baked into a PNG.
- **Full-resolution photos**: place each source photo with its own `\includegraphics` at native
  resolution (pre-crop to the tile aspect WITHOUT downscaling), so zooming shows real detail. Save
  tiles as `.jpg`; never rasterise the whole figure to a single `.png`.
- **Per-panel hyperlinks**: wrap every tile in `\href{https://arxiv.org/abs/<id>}{...}` and print
  the verified figure number on the tile, so a reviewer can click any artifact to reach its paper.
  Mirror the same links in a provenance table. Confirm the links compiled by decompressing the PDF
  streams and counting `/Subtype/Link` + `arxiv.org/abs/` URIs (`strings` misses them — they live
  in compressed object streams).
- **Label styling — page background, document link colour**: per-tile labels must sit on the PAGE
  background (white), NOT on a baked dark label strip (a `\fill[black!..]` box behind each name).
  A dark strip fights the page and looks pasted-on; the user rejected it. Colour the hyperlinked
  paper name in the document's own link colour (for acmart, `\href` uses `urlcolor=ACMDarkBlue`, so
  set the TikZ node `text=ACMDarkBlue` — inside a node the node's `text=` wins over hyperref's
  colouring), keep the figure number a muted grey (`black!60`), and give each tile a light border
  (`black!35`) so tiles still separate on white. Keep the figure TITLE bar and section-band headers
  dark — only the per-tile paper-name strips must go.
- **Placement — main body, not appendix**: the primary survey compilation/overview figures (subject
  gallery, results gallery, corpus-at-a-glance collage) belong in the MAIN BODY at the relevant
  section (e.g. right after the taxonomy/scope, referenced in the running text), NOT buried in the
  appendix. Add a short subsection that `\ref`s each figure so every figure is cited in text; the
  provenance table may stay in the appendix and be cross-referenced.
