---
description: Improve the AUDIT HARNESS after a miss - diagnose why an audit agent missed a discrepancy, generalise it into a reusable check, and patch parity-auditor.md (+ a .claude/audit rule when the miss is edit-time detectable) with a dated regression case, so the whole class is caught next time.
argument-hint: [the miss: what was wrong + how it was caught; default: the most recent hand-caught miss in this conversation]
---

A discrepancy that an audit agent SHOULD have caught was instead caught by hand (by the user or later review). Spawn a `general-purpose` agent (run synchronously, `run_in_background: false`) told to READ and APPLY `.claude/agents/improve-harness.md` on the described miss (default: the most recent hand-caught miss in this conversation). It must:

1. **Intake + root-cause**: restate the miss in one sentence; name the audit that missed it (parity-auditor, or an ad-hoc consistency audit) and the EXACT gap. If truth was taken from a requester-supplied "source of truth" rather than the primary document, that is itself the root cause (class 8).
2. **Generalise** to the CLASS, not the instance - a fix that only catches the exact instance is a FAIL; it must catch siblings.
3. **Patch `parity-auditor.md` additively**: add the new check + a dated entry under `## Regression cases`; preserve its frontmatter and section structure; never delete or weaken an existing check.
4. **Edit-time defence (only if rule-shaped)**: if a PreToolUse hook could catch it by tool/file/content, add a rule file under `.claude/audit/` in the existing catalog format. Do NOT add a brittle keyword rule for a semantic miss (that overfits).
5. **Log**: append one line to `.claude/agents/improve-harness.log` and one JSON line to `.claude/audit/misses.jsonl`; keep `.claude/audit/rubric.md` current.
6. **Verify (TRACE)**: quote the new check and show, step by step, that it would have flagged the reported miss. If it would not, revise and repeat.

Guardrails: additive only; one class per invocation; never fabricate a date, path, or "would-catch" trace; read the primary document yourself rather than trusting a summary. If a scoping/strictness decision is genuinely ambiguous, ask the user ONE multiple-choice question first.

End with the agent's one-line verdict: `AUDITOR STRENGTHENED: would now catch <class>` (trace above it) or `NO CHANGE NEEDED: <why the existing checks already cover it>`.
