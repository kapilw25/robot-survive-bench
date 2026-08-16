# Parity / replica audit rubric

Run this on the COMPILED render BEFORE saying "replica / matches / no discrepancy / done".
It is NOT automatic; eyeballing only what you just edited is exactly how misses ship (see `misses.jsonl`).

## 0. Run it. Every time. On the rendered output, not the source.

## 1. Enumerate the reference (this list IS the checklist)
List EVERY visible element of the reference: title, bands, each label, each number / section-number / numbering scheme, markers, boxes, arrows, legend, notes, colours, per-item citations.

## 2. Element-by-element diff
For each reference element, confirm the replica has it. Content may differ; the element and any numbering scheme must be present. A missing element (e.g. section 3.x.y sub-numbers) is a DISCREPANCY even when structure and type match.

## 3. Type parity
Same KIND of artifact (collage vs collage, diagram vs diagram, chart vs chart). A type swap is a fail, never "close enough".

## 4. Media parity + provenance
If the reference uses real media (photos / figures), the replica must too, per sub-element, each viewed on-subject and provenance-logged. Placeholder cards / boxes = PARTIAL.

## 5. Render quality on EVERY box
Zoom into every box (root/title, branches, sub-labels, cells): no text past a border, no clipping, no overlapping labels, no overfull box, no sub-body-size text. Check ALL boxes, not just the ones you edited.

## 6. No hallucination
Every fact / number / cite is real and recorded. Unlogged counts are marked "not logged", never invented.

## 7. Working-doc house style (produced markdown under `plan/` or `.claude/`, never a published `.tex`)
Scan the PRODUCED file's own rows, do not trust the soft PreToolUse reminder was honoured. Every table row and header (a `^\|` line that is not the `|---|` separator) carries a colourful emoji marker; a 3+ item / 2+ dimension comparison is a table, not a wall-of-text paragraph; a paper / URL reference cell is a clickable link. A row with zero emoji is a HOUSE-STYLE-VIOLATION even when the content is right. Generalise: any formatting invariant that exists only as a soft reminder must be verified against the artifact itself. Edit-time companions: `table_row_emoji.md`, `tables_over_prose.md`.

## 8. Table-count cap (produced working-doc markdown under `plan/` or `.claude/`, never a published `.tex`)
Each working-doc `.md` holds AT MOST 2 markdown tables. Count the table SEPARATOR rows in the produced file (a `|---|` divider line: a stripped line of only `|`, `:`, `-`, spaces with at least one `-` and one `|`); each separator row is one table. A count of >= 3 means the doc sprawled into 3+ tables and buried its key content: verdict TABLE-SPRAWL. Fix by SPLITTING into focused files (one concept per file, each with at most 2 tables); at minimum add a top-of-file pointer to the single canonical table. Edit-time companions: the count runs in `.claude/hooks/post_generation_audit.py`, catalogued as `table_sprawl.md`.

Verdict: MATCH only if 1 through 8 all pass; otherwise PARTIAL (or TABLE-SPRAWL) naming the exact failing element. Append every confirmed miss to `misses.jsonl`.
