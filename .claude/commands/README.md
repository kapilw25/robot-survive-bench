# Project slash commands · `.claude/commands/`

Five reflexive commands to interrogate the most recent assistant artifact from different angles. Each is its own file; type `/<name>` (or `/<name> <target>`).

```text
┌─────────────┬─────────────────────────────────────────────────────────────────────────────┐
│ When you want to ...                                              │ Run                  │
├─────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ Be told what's WRONG with the artifact (harsh, no softener)       │ /brutal              │
│ Hear the strongest argument for the OPPOSITE of your position     │ /steelman            │
│ Re-explain a concept with zero jargon + an everyday analogy       │ /eli5                │
│ Enumerate what's ABSENT (edge cases, assumptions, stakeholders)   │ /missing             │
│ See the path to 10× better (speed / cost / scale / value)         │ /10x                 │
└─────────────┴─────────────────────────────────────────────────────────────────────────────┘
```

Decision-tree shortcut: critique-of-what's-there → `/brutal`; critique-of-what's-NOT-there → `/missing`; argue-opposite → `/steelman`; future-growth → `/10x`; translate-complex-to-simple → `/eli5`.

All five take an optional argument (file path, claim, or topic). With no arg they target the most recent significant artifact in this conversation.

Each command file ends with a `**Distinction from sibling commands**` block — read that line if you're ever unsure which to pick.

## Survey-pipeline commands (added 2026-07; see .claude/skills/survey-pipeline/SKILL.md)

| Command | Purpose |
|---|---|
| `/novelty-scan <topic>` | WEBSEARCH >=10 real surveys, coverage matrix, find the empty cell; adversarial audit agent must return ACHIEVED; writes `novelty_gap.md` |
| `/survey-init <topic>` | Scaffold the full CSUR acmart tree from templates (gated on NOVELTY CONFIRMED); audit agent verifies scaffold + compile |
| `/taxonomy-loop` | Arms `.claude/state/survey_loop.json`; Stop hook BLOCKS finishing until gates G1-G6 pass (refs harvested+verified, hero taxonomy compiles, renders, eyeballed); audit agent refutes-or-confirms before release |
| `/survey-audit` | 5-agent audit fleet (fabrication/tags/consistency/tone/build); fix + re-audit same agents until all CLEAN; refresh main_flat.tex |

Loop engine: `.claude/hooks/survey_loop_stop.py` (registered in `.claude/settings.json`).
Manual gate check: `python3 .claude/hooks/survey_loop_stop.py --check`. Disarm: delete `.claude/state/survey_loop.json`.

### One-shot master: `/survey <new topic>`
Runs the WHOLE pipeline (novelty-scan -> init -> taxonomy-loop -> tables/prose -> audit fleet) with
`full_pipeline: true`, adding gates G7 (all files substantive: sections/tables/timeline/main_flat)
and G8 (current `audit_report.md` with 'ALL AUDITS CLEAN'; goes stale on any source edit). The agent
cannot stop on audit failures -- it must fix, re-audit, and also patch the pipeline files themselves
(Lessons section in SKILL.md) when an auditor exposes a recurrable mistake class.
