# Audit rules (context-aware guardrails)

Each file here is ONE recurring problem + its fix, plus a machine-readable trigger. A single
dispatcher hook, `.claude/hooks/audit_guard.py` (PreToolUse), reads every rule, auto-detects the
context of a tool call (which tool, which file, what content or command), and fires the matching
rules: `block` stops the call, `warn` injects a reminder. Em-dashes are handled by the separate,
battle-tested `block_em_dash.py`, so an `em-dash` rule here is documentation only (severity
`delegated`).

## Frontmatter fields (between the `---` fences at the top of each rule file)
- `id`        : short rule id (shown when it fires).
- `tools`     : comma list of tool names it applies to (Edit, Write, MultiEdit, NotebookEdit, Bash).
- `path`      : optional glob on the edited file path (Edit/Write only). Omit = any file.
- `match`     : regex; the rule fires when it matches the target text (a Bash command, or the new
                content/string being written). Prefix with `(?i)` for case-insensitive.
- `antimatch` : optional regex; if it matches, the rule does NOT fire (false-positive guard).
- `severity`  : `block` (exit 2, stops the call) | `warn` (non-blocking reminder) | `delegated` /
                anything else (documentation only, the dispatcher ignores it).

The body below the frontmatter is the message shown when the rule fires. Keep it to a one-line
**Problem** and a one-line **Fix**.

## Add a new rule (no code change)
Drop a new `<id>.md` here with the frontmatter above. The dispatcher picks it up automatically.
Test one call:
```
echo '{"tool_name":"Bash","tool_input":{"command":"bash git_push.sh \"x?\""}}' | python3 ../hooks/audit_guard.py
```
