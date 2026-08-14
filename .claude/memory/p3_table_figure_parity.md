# P3 tables/figures must match P1 formatting (reference main_preprint.pdf)

For EVERY new P3 table or figure, the formatting must match the proven P1 survey. Workflow:

1. **Name the P1 analog.** Point the user to the corresponding artifact in
   `overleaf_draft/p1_weights_or_skills/no_upload/build/main_preprint.pdf` (its Table/Figure number
   and page) so they can eyeball parity.
2. **Match P1 exactly:** same environment (scriptsize `longtable` / `figure*` with `\resizebox`),
   same mark macros (`\yy \nn \pp \dm`, eval markers `\dreal \dsim \dgame`), same caption style,
   same two-tier grouping, and **`\cite` (numbered references), not `\href`**.
3. **Reproducible + compile-tested.** P3 tables are generated from the canonical
   `docs/assets/catalog_p3.js` (e.g. `no_upload/gen_landscape_p3.py`); build refs.bib so `\cite`
   resolves; compile-test each artifact via a `no_upload/` standalone wrapper and compare the PDF to
   the P1 one.

Key scheme for refs.bib: bibkey = normalized name (lowercase alphanumerics, drop parenthetical and
post-slash, `+`->`p`), disambiguate collisions with the year. The generator and refs.bib must use
the SAME keys. Related: [[p3_two_paper_plan]].
