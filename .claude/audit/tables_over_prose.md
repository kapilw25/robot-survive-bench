---
id: tables-over-prose
tools: Edit, Write
path: *.md
match: ^(?!.*\|)(?![ \t]*[-*>#]).{450,}$
antimatch: data:|https?://|base64|<svg
severity: warn
---
# Comparison TABLES, not long paragraphs
Problem: a wall-of-text paragraph is hard to eyeball; the user rejected this twice.
Fix: convert any comparison of 3+ items or 2+ dimensions into a TABLE (or short bullet lines); add an emoji to every row; keep standalone prose to 1-2 line lead-ins. (Working docs only; a published paper `.tex` keeps academic prose.)
