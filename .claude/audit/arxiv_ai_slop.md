---
id: arxiv-ai-slop
tools: Edit, Write, MultiEdit
path: *.tex
match: (?i)\b(as an ai|as a language model|lorem ipsum|TODO|TBD|FIXME|placeholder|i hope this helps|let me know if|would you like me to)\b
severity: warn
---
# No AI-slop or placeholders in arXiv source
Problem: AI meta-comments, TODO / TBD / FIXME, or placeholder / illustrative data in submitted `.tex` are an arXiv ban trigger.
Fix: remove them before submission. Every number is real and cited, every section is complete prose, and there are no chatbot leftovers.
