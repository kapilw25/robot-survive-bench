#!/usr/bin/env python3
"""PreToolUse audit dispatcher.

Reads the rule catalog in .claude/audit/*.md, auto-detects the context of a tool
call (which tool, which file, what content or command), and fires matching rules:

  severity block -> exit 2  (stops the call; stderr is fed back to the agent)
  severity warn  -> exit 0  with hookSpecificOutput.additionalContext (non-blocking reminder)
  severity delegated / anything else -> ignored (documented, enforced elsewhere)

One hook, N rules. Add a rule by dropping a new .claude/audit/<id>.md file (see that
dir's README for the frontmatter). Em-dashes are enforced by block_em_dash.py, not here.

Fails OPEN on any error so a hook bug can never wedge tool use.

Manual test:
  echo '{"tool_name":"Bash","tool_input":{"command":"bash git_push.sh \"x?\""}}' | python3 audit_guard.py
"""
import json
import os
import re
import sys
import fnmatch

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT_DIR = os.path.join(HERE, "..", "audit")


def target_text(tool, ti):
    if tool == "Write":
        return ti.get("content", "") or ""
    if tool == "Edit":
        return ti.get("new_string", "") or ""
    if tool == "MultiEdit":
        return "\n".join(e.get("new_string", "") for e in ti.get("edits", []) if isinstance(e, dict))
    if tool == "NotebookEdit":
        return ti.get("new_source", "") or ""
    if tool == "Bash":
        return ti.get("command", "") or ""
    return ""


def parse_rule(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    if not txt.startswith("---"):
        return None
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return None
    fm, body = parts[1], parts[2].strip()
    meta = {"_body": body}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def load_rules():
    out = []
    try:
        for fn in sorted(os.listdir(AUDIT_DIR)):
            if fn.endswith(".md") and fn.lower() != "readme.md":
                r = parse_rule(os.path.join(AUDIT_DIR, fn))
                if r:
                    out.append(r)
    except Exception:
        pass
    return out


def fires(rule, tool, path, text):
    sev = rule.get("severity", "").lower()
    if sev not in ("block", "warn"):
        return False
    tools = [t.strip() for t in re.split(r"[ ,]+", rule.get("tools", "")) if t.strip()]
    if tools and tool not in tools:
        return False
    glob = rule.get("path", "")
    if glob:
        if not path:  # a path-scoped rule cannot apply to a tool with no file path (e.g. Bash)
            return False
        if not (fnmatch.fnmatch(path, glob) or fnmatch.fnmatch(os.path.basename(path), glob)):
            return False
    m = rule.get("match", "")
    if m:
        try:
            if not re.search(m, text, re.MULTILINE):
                return False
        except re.error:
            return False
    am = rule.get("antimatch", "")
    if am:
        try:
            if re.search(am, text, re.MULTILINE):
                return False
        except re.error:
            pass
    return True


def run():
    data = json.loads(sys.stdin.read())
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    path = ti.get("file_path", "") or ""
    text = target_text(tool, ti)
    if not text:
        return 0

    blocks, warns = [], []
    for r in load_rules():
        if fires(r, tool, path, text):
            (blocks if r.get("severity", "").lower() == "block" else warns).append(r)

    if blocks:
        ids = ", ".join(b.get("id", "?") for b in blocks)
        sys.stderr.write("BLOCKED by audit rule(s): " + ids + "\n\n"
                         + "\n\n".join(b["_body"] for b in blocks) + "\n")
        return 2

    if warns:
        ctx = ("AUDIT reminder(s) for this " + tool + " call (.claude/audit/):\n\n"
               + "\n\n".join(w["_body"] for w in warns))
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "additionalContext": ctx}}))
        return 0

    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except SystemExit:
        raise
    except Exception:
        # Fail open: a hook bug must never block legitimate tool use.
        sys.exit(0)
