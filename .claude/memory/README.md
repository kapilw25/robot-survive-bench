# Survey knowledge base (project-local memory)

Reusable lessons so every new survey paper (built via the `/survey` pipeline in
`.claude/skills/survey-pipeline/`) ships the reviewer-mandated artifacts and never repeats known
mistakes. One file per topic; this README is the index.

- [survey_reviewer_artifacts.md](survey_reviewer_artifacts.md) — the 3 CSUR-reviewer-mandated
  artifacts every survey must contain (PRISMA methodology figure, family x 6-axes spec matrix,
  metric-anchored future work) + the LaTeX pitfalls hit building them.
- [scraped_asset_subject_audit.md](scraped_asset_subject_audit.md) — when a survey scrapes figures
  from source papers, audit the whole CANDIDATE POOL: classify every tile subject-present /
  results-plot / neither, purge the 'neither', keep provenance. "Largest raster file" is not a
  proxy for "relevant figure".
- [p3_two_paper_plan.md](p3_two_paper_plan.md): INTERNAL. P3 is two papers (survey assessing
  ACTION-ATLAS novelty, then a modified benchmark). WAS is ACTION-ATLAS's own metric: assess, never
  adopt. Keep paper 1 a SURVEY, not a position paper.
- [prefer_tables_over_prose.md](prefer_tables_over_prose.md): user preference for comparison TABLES
  over long paragraphs in working docs; long prose is hard to eyeball.
- [p3_table_figure_parity.md](p3_table_figure_parity.md): every new P3 table/figure must match the P1
  formatting; name the P1 analog in main_preprint.pdf, use \cite (numbered refs) not \href, generate
  reproducibly, and compile-test vs the P1 PDF.
