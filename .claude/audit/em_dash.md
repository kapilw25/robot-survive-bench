---
id: em-dash
tools: Edit, Write, MultiEdit, NotebookEdit
severity: delegated
---
# No em-dashes
Problem: the user does not want em-dashes anywhere in the writing.
Fix: use a comma, colon, parentheses, or two shorter sentences. En-dash ranges (2016--2026) and Markdown/YAML `---` fences are fine.
Enforced by a dedicated hook, `.claude/hooks/block_em_dash.py`, so this dispatcher leaves em-dashes alone.
