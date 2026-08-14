---
id: hallucinated-refs
tools: Edit, Write, MultiEdit
match: arXiv:|arxiv\.org|\\cite|@(article|inproceedings|misc|book)\{
severity: warn
---
# Verify every reference (anti-hallucination)
Problem: a fabricated arXiv id, or a wrong title / author / year, is an arXiv ban trigger and destroys trust.
Fix: web-verify EACH id against its arXiv or DOI page (exact title, first author, year). Unverifiable = OMIT, never invent. Dedup by bib key AND arXiv id.
