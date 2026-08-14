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
Note: the "emoji on every row" half of this rule is only advisory here; it is enforced as a checkable trigger by the companion rule `table_row_emoji.md`, which scans produced table rows for the marker.
