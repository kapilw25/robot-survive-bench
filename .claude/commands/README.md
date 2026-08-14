# Project slash commands · `.claude/commands/`

Reflexive commands to interrogate the most recent assistant artifact from different angles. Each is its own file; type `/<name>` (or `/<name> <target>`).

| When you want to ... | Run |
|---|---|
| Be told what's WRONG with the artifact (harsh, no softener) | `/brutal` |
| Hear the strongest argument for the OPPOSITE of your position | `/steelman` |
| Re-explain a concept with zero jargon + an everyday analogy | `/eli5` |
| Enumerate what's ABSENT (edge cases, assumptions, stakeholders) | `/missing` |
| See the path to 10x better (speed / cost / scale / value) | `/10x` |

Decision-tree shortcut: critique-of-what's-there -> `/brutal`; critique-of-what's-NOT-there -> `/missing`; argue-opposite -> `/steelman`; future-growth -> `/10x`; translate-complex-to-simple -> `/eli5`.

All take an optional argument (file path, claim, or topic). With no arg they target the most recent significant artifact in this conversation.

## Harness command

| Command | Purpose |
|---|---|
| `/improve-harness` | After an audit miss, diagnose it, generalise a reusable check, and patch `parity-auditor.md` + a `.claude/audit/` rule so the whole class is caught next time |
