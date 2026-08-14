---
description: WEBSEARCH-first novelty-gap discovery for a new survey topic - find the organizing axis no existing survey covers (the "empty cell") before any writing begins
argument-hint: <topic, e.g. "tactile sensing for manipulation">
---

Load the **survey-pipeline** skill first (`.claude/skills/survey-pipeline/SKILL.md`), then run
the novelty scan for topic: **$ARGUMENTS**

## Phase 1 — sweep for existing surveys (WebSearch, multi-modal)
Run ALL of these query shapes (not just one), collecting every hit:
- `"$ARGUMENTS" survey`  ·  `survey of $ARGUMENTS`  ·  `"$ARGUMENTS" systematic review`
- `comprehensive survey $ARGUMENTS 2024..2026 arXiv`
- `$ARGUMENTS survey "ACM Computing Surveys"`  (venue-targeted)
- 2-3 reformulations using synonyms/subfield names of the topic
Also sweep adjacent/parent fields (a survey one level up may already cover the topic as a section).

For EVERY candidate survey, verify it is real (exact title, first author, year, venue, arXiv ID via
web search). Target: **>= 10 verified closest surveys**. Fewer after honest effort is itself evidence
(document it).

## Phase 2 — coverage matrix and the empty cell
1. Propose 3-5 candidate organizing axes for the topic (analogous to "degree of self-improvement"
   for code-as-policy). Good axes are mechanisms/progressions, not application lists.
2. Build the matrix: rows = candidate sub-topics + each candidate axis; columns = the >=10 surveys;
   marks = covered / partial / absent.
3. The **novelty gap** = an axis (or axis x sub-topic cell) where EVERY existing column is empty
   but the literature has real systems to populate it.
4. **If no empty cell survives scrutiny: DO NOT stop.** Pivot to the next candidate axis, or narrow/
   broaden the topic one notch, and re-run Phase 1 queries for that angle. Repeat until either a
   defensible gap is found or 3 full pivots have failed (then report NOT CONFIRMED honestly).

## Phase 3 — write the evidence (into the survey workspace dir, default `survey_<slug>/`)
- `novelty_gap.md` — the verdict file. MUST contain, in this order:
  - `## Surveys found` — the verified list (title / venue / year / arXiv ID)
  - `## Coverage matrix` — the markdown matrix from Phase 2
  - `## The gap` — one paragraph naming the empty cell and why it matters
  - final line, verbatim format: `NOVELTY CONFIRMED: <organizing axis>` (or `NOVELTY NOT CONFIRMED`)
- Draft `tables/tab_survey_compare.tex` (coverage matrix as the paper's Table 1, our column full)
  and note timeline data (year, venue per survey) for `figures/fig_survey_timeline.tex`.

## Phase 4 — MANDATORY adversarial audit (anti-hallucination gate)
After writing `novelty_gap.md`, spawn a fresh **general-purpose Agent** (it must NOT reuse your
findings — only the file) with this brief:
- "Read `novelty_gap.md`. Your job is to REFUTE it. (a) Web-verify EVERY listed survey: exact
  title, first author, year, arXiv ID — flag any that does not exist or whose metadata is wrong
  (hallucination = automatic REFUTED). (b) Adversarially search for a survey that DOES cover the
  claimed gap axis — use different query phrasings than obvious ones, and check the related-work
  sections of the 3 closest surveys. (c) Check the coverage-matrix marks for the 3 closest
  surveys against their actual abstracts/TOCs. Default to REFUTED if uncertain. Return findings
  most-severe-first, ending with exactly `AUDIT VERDICT: ACHIEVED` or `AUDIT VERDICT: REFUTED`."
- If **REFUTED**: fix `novelty_gap.md` (drop fake surveys, correct marks, pivot the axis if the
  gap is disproven) and re-run the audit with a NEW agent. Loop until ACHIEVED — the scan is not
  done on your own say-so, only on the auditor's.
- Record the final verdict line inside `novelty_gap.md` under `## Audit`.

Anti-hallucination is absolute: no invented surveys, no invented coverage claims. The Stop-hook
gate G1 reads `novelty_gap.md` and will not release a `/taxonomy-loop` without `NOVELTY CONFIRMED`.
Finish by reporting the gap in one sentence, the audit verdict, and recommending
`/survey-init $ARGUMENTS`.
