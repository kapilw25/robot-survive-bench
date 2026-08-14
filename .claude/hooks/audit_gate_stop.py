#!/usr/bin/env python3
"""Stop hook: the AUDIT GATE (independent-agent-only, ledger-authoritative).

The gate is satisfied ONLY when every deliverable that was flagged event="required" (by the
PostToolUse hook) has a LATER event="audited" record with verdict="CLEAN" in
.claude/audit/audit_ledger.jsonl. That "audited" record is written ONLY by a spawned parity-audit
agent (per .claude/agents/parity-auditor.md). Consequences:
  - Emptying pending_audit.txt by hand does NOT satisfy the gate (the ledger still shows required
    without a later CLEAN audit).
  - An inline self-audit does NOT satisfy the gate (no agent = no CLEAN ledger record).
  - Editing a deliverable again adds a new later "required", so it must be re-audited.
So "done" can only be reached after an independent agent audit ran and returned CLEAN.

Escape hatch (only if the user explicitly says skip): touch .claude/audit/AUDIT_OVERRIDE.
Safety cap: after MAX_BLOCKS consecutive blocks it stops blocking so it can never hard-lock.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDITDIR = os.path.join(HERE, "..", "audit")
LEDGER = os.path.join(AUDITDIR, "audit_ledger.jsonl")
OVERRIDE = os.path.join(AUDITDIR, "AUDIT_OVERRIDE")
COUNTER = os.path.join(AUDITDIR, ".stop_block_count")
MAX_BLOCKS = 8


def load_ledger():
    rows = []
    try:
        for ln in open(LEDGER):
            ln = ln.strip()
            if ln:
                rows.append(json.loads(ln))
    except Exception:
        pass
    return rows


def unaudited(rows):
    """paths whose latest 'required' has no later 'audited'+CLEAN."""
    req, ok = {}, {}
    for r in rows:
        p = r.get("path")
        if not p:
            continue
        s = r.get("seq", 0) or 0
        e = r.get("event")
        if e == "required":
            req[p] = max(req.get(p, 0), s)
        elif e == "audited" and r.get("verdict") == "CLEAN":
            ok[p] = max(ok.get(p, 0), s)
    return [p for p, rs in req.items() if ok.get(p, -1.0) < rs]


def rm(p):
    try:
        os.remove(p)
    except Exception:
        pass


def main():
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    if os.path.exists(OVERRIDE):
        return 0
    bad = unaudited(load_ledger())
    if not bad:
        rm(COUNTER)
        return 0
    try:
        n = int(open(COUNTER).read().strip())
    except Exception:
        n = 0
    names = ", ".join(os.path.basename(p) for p in bad)
    if n >= MAX_BLOCKS:
        rm(COUNTER)
        print(json.dumps({"decision": "block", "reason":
              "AUDIT GATE safety cap (" + str(MAX_BLOCKS) + " blocks) hit; allowing turn-end, but "
              + str(len(bad)) + " deliverable(s) never got an independent CLEAN agent audit: " + names
              + ". Audit them next turn."}))
        return 0
    with open(COUNTER, "w") as f:
        f.write(str(n + 1))
    lines = "\n".join("  - " + p for p in bad)
    reason = ("AUDIT GATE (independent-agent-only): cannot end the turn. These deliverables were "
              "generated and have NO later CLEAN audit from a spawned agent:\n" + lines + "\n\n"
              "For EACH: re-render, VIEW the pixels, then SPAWN a general-purpose agent told to "
              "READ+APPLY .claude/agents/parity-auditor.md on it (run_in_background: false). The "
              "agent returns a PARITY VERDICT and records {path, event:\"audited\", verdict:\"CLEAN\"} "
              "in .claude/audit/audit_ledger.jsonl. INLINE self-audit and hand-clearing pending do "
              "NOT satisfy this gate. If FLAGGED, fix and re-audit until CLEAN.\n"
              "Escape hatch only if the user says skip: touch .claude/audit/AUDIT_OVERRIDE.")
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
