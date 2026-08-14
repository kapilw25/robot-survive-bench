---
id: table-row-emoji
tools: Edit, Write, MultiEdit
path: *.md
match: ^\|(?![-\s:|]*$)(?:(?![\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF\U000025A0-\U000025FF\U00002300-\U000023FF\U0000FE0F\U00002139])[^\n])*$
severity: warn
---
# Emoji on every table row (fast-eyeball house style)
Problem: a produced markdown table row / header with NO colourful emoji violates the standing house style ("add an emoji to every row/header so it is fast to eyeball"); this fired because a written table DATA row (a `^\|` line that is not the `|---|` separator) carries zero emoji.
Fix: prefix every data row and header cell with a colourful emoji marker (see `plan/v1/README.md` / `plan/v2/README.md` for the pattern); the `|---|` separator is exempt. Working docs only; a published paper `.tex` keeps academic prose. This is the checkable companion to `tables_over_prose.md`.
