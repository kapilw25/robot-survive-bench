#!/usr/bin/env python3
"""PreToolUse guard: block any Edit/Write/MultiEdit/NotebookEdit that would
introduce an em-dash into a file.

Rationale: the user does not want em-dashes in the writing. A deterministic hook
makes that mechanically impossible instead of relying on a later audit agent to
catch (and sometimes miss) them.

Blocks, in the text a call would WRITE into the file:
  * the Unicode em-dash  U+2014 (—)  and horizontal bar U+2015 (―)  -- in ANY file
  * a LaTeX em-dash  '---'  (exactly three hyphens)  -- in *.tex / *.sty / *.cls
  * the &mdash; / &#8212; / &#x2014; HTML entities  -- in *.html / *.htm / *.md

Deliberately NOT blocked (all legitimate):
  * en-dash ranges  '--'  or  '–'   e.g. 2016--2026, Tables 1--3
  * CLI flags        '--code-only'
  * Markdown / YAML  '---'  front-matter fences and horizontal rules (in .md)
  * longer hyphen runs used as separators  '----'  '% ------'

Exit 0 = allow, exit 2 = block (stderr is fed back to the agent).
Fails OPEN on any internal error so a hook bug can never wedge all editing.
"""
import json
import os
import re
import sys

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}

# exactly three hyphens, not part of a longer run ('----' separators stay legal)
TEX_EMDASH = re.compile(r"(?<!-)---(?!-)")
UNICODE_EMDASH = ("—", "―")  # em dash, horizontal bar
HTML_EMDASH = ("&mdash;", "&#8212;", "&#x2014;", "&#X2014;")


def written_text(tool_name, ti):
    """The strings this call would place into the file (new content only)."""
    if tool_name == "Write":
        return [ti.get("content", "")]
    if tool_name == "Edit":
        return [ti.get("new_string", "")]
    if tool_name == "MultiEdit":
        return [e.get("new_string", "") for e in ti.get("edits", [])]
    if tool_name == "NotebookEdit":
        return [ti.get("new_source", "")]
    return []


def find_hits(texts, ext):
    hits = set()
    for t in texts:
        if not isinstance(t, str):
            continue
        for ch in UNICODE_EMDASH:
            if ch in t:
                hits.add("Unicode em-dash %r" % ch)
        if ext in (".tex", ".sty", ".cls") and TEX_EMDASH.search(t):
            hits.add("LaTeX em-dash '---'")
        if ext in (".html", ".htm", ".md", ".markdown"):
            for ent in HTML_EMDASH:
                if ent in t:
                    hits.add("HTML em-dash entity '%s'" % ent)
    return hits


def run():
    data = json.loads(sys.stdin.read())
    tool_name = data.get("tool_name", "")
    if tool_name not in EDIT_TOOLS:
        return 0
    ti = data.get("tool_input") or {}
    path = ti.get("file_path", "") or ""
    ext = os.path.splitext(path)[1].lower()

    hits = find_hits(written_text(tool_name, ti), ext)
    if hits:
        sys.stderr.write(
            "BLOCKED: this edit introduces an em-dash (" + ", ".join(sorted(hits))
            + ") into " + (path or "the file") + ".\n"
            "The user does not want em-dashes. Rewrite with a comma, colon, "
            "parentheses, or two shorter sentences. En-dash ranges (2016--2026) "
            "and Markdown/YAML '---' fences are fine.\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except SystemExit:
        raise
    except Exception:
        # Fail open: a hook bug must never block legitimate editing.
        sys.exit(0)
