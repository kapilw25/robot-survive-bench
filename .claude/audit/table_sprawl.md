---
id: table-sprawl
tools: Edit, Write, MultiEdit
path: *.md
severity: delegated
---
# At most 2 tables per working-doc .md (no table sprawl)
Problem: a working doc grows to 3+ markdown tables, so the reader cannot find the key one ("I see lots of tables which are confusing ... where is the NOVELTY table?"). The house rule, stated firmly and twice, is that each working-doc `.md` holds AT MOST 2 tables.
Fix: SPLIT a doc that needs more into focused files (one concept per file), each with at most 2 tables; at minimum add a top-of-file pointer to the single canonical table. Working docs under `plan/` and `.claude/` only; a published paper `.tex` is exempt (same precedent as `tables_over_prose.md` / `table_row_emoji.md`).
Enforced by the PostToolUse hook `.claude/hooks/post_generation_audit.py`, which reads the produced file and COUNTS its table separator rows (a `|---|` divider line: a stripped line of only `|`, `:`, `-`, spaces with at least one `-` and one `|`); a count of >= 3 means 3+ tables and warns. This PreToolUse dispatcher is single-line-regex only and cannot count across a file (and on an Edit sees only the fragment), so it leaves the count to that hook and to parity-auditor Procedure step 8; this rule is documentation only (`severity: delegated`).
