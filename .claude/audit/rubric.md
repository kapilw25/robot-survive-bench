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

Verdict: MATCH only if 1 through 6 all pass; otherwise PARTIAL naming the exact failing element. Append every confirmed miss to `misses.jsonl`.
