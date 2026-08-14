#!/usr/bin/env python3
"""PostToolUse hook: flag every figure / table / deliverable-PDF generation as needing an
INDEPENDENT AGENT audit (inline self-audit is no longer accepted).

Fires after Edit|Write|MultiEdit|Bash. When the touched file is a P3 figure/table source
(figures/*.tex, tables/*.tex) or a deliverable PDF (deliverables/*.pdf), it:
  1. runs a fast static lint for the malformed-xcolor bug (e.g. cat-skill!75!black!black),
  2. records the file as event="required" in .claude/audit/audit_ledger.jsonl (append-only) and in
     pending_audit.txt, and
  3. injects an instruction that a general-purpose agent applying parity-auditor.md MUST audit it.

The Stop gate (audit_gate_stop.py) is now satisfied ONLY when every "required" deliverable has a
later "audited"+verdict=CLEAN entry in the ledger -- an entry only the spawned parity-audit agent
writes. Emptying pending by hand, or an inline self-audit, no longer clears the gate. A hook cannot
spawn the agent; it makes skipping the independent audit impossible.
"""
import json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDITDIR = os.path.join(HERE, "..", "audit")
PENDING = os.path.join(AUDITDIR, "pending_audit.txt")
LEDGER = os.path.join(AUDITDIR, "audit_ledger.jsonl")


def is_deliverable(path):
    p = path.replace("\\", "/")
    return (("/figures/" in p and p.endswith(".tex")) or
            ("/tables/" in p and p.endswith(".tex")) or
            ("/deliverables/" in p and p.endswith(".pdf")))


def lint_colors(path):
    warns = []
    try:
        txt = open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        return warns
    if re.search(r'!black!(?=[A-Za-z])', txt):
        warns.append("chained/duplicated colour mix like '!black!black' (a replace_all collision)")
    if re.search(r'!!', txt):
        warns.append("doubled '!!' in a colour/option")
    return warns


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ti = data.get("tool_input", {}) or {}
    # Flag ONLY on source edits (Edit/Write/MultiEdit of figures/tables/*.tex) -- the real
    # generation event. NEVER parse Bash commands: an audit agent's own render/read commands
    # mention the deliverable path and would spuriously re-arm the gate after it audited.
    path = ti.get("file_path", "") or ""
    if not path or not is_deliverable(path):
        return 0
    abspath = os.path.abspath(path)

    try:
        os.makedirs(AUDITDIR, exist_ok=True)
        have = set()
        if os.path.exists(PENDING):
            have = set(l.strip() for l in open(PENDING) if l.strip())
        have.add(abspath)
        with open(PENDING, "w") as f:
            f.write("\n".join(sorted(have)) + "\n")
        with open(LEDGER, "a") as f:
            f.write(json.dumps({"path": abspath, "event": "required", "seq": time.time()}) + "\n")
    except Exception:
        pass

    warns = lint_colors(path) if path.endswith(".tex") else []
    msg = ("AUDIT REQUIRED (independent agent) for: " + os.path.basename(path) + ".\n"
           "Before ending this turn you MUST: (1) re-render the deliverable, (2) VIEW the pixels, "
           "(3) SPAWN a general-purpose agent told to READ+APPLY .claude/agents/parity-auditor.md on "
           "this deliverable and return a PARITY VERDICT. INLINE self-audit is NO LONGER accepted: "
           "the Stop gate is satisfied ONLY by a CLEAN verdict the agent records in "
           ".claude/audit/audit_ledger.jsonl. Do NOT clear pending_audit.txt or the ledger by hand -- "
           "only the spawned agent may write an 'audited' record. A source edit is never a result.")
    if warns:
        msg += "\nLINT (fix before rendering): " + "; ".join(warns)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                             "additionalContext": msg}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
