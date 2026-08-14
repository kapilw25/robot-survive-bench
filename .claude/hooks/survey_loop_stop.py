#!/usr/bin/env python3
"""Survey-pipeline loop engine (Stop hook + manual gate checker).

Stop-hook mode (default): reads hook JSON on stdin. If .claude/state/survey_loop.json
exists with status=="in_progress", runs the taxonomy gates; on any failure it emits
{"decision":"block","reason":"<actionable next steps>"} so Claude keeps working.
The reason text IS the next prompt Claude acts on -- keep it imperative.

Manual mode:  python3 survey_loop_stop.py --check   (prints gate report, exit 1 on fail)

Safety valves: iteration cap (default 15) stored in the state file; delete the state
file or set "status":"done" to disarm the loop at any time.
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "..", "state", "survey_loop.json")


def load_state():
    try:
        with open(STATE) as f:
            return json.load(f)
    except Exception:
        return None


def save_state(s):
    with open(STATE, "w") as f:
        json.dump(s, f, indent=2)


def gates(state):
    """Return a list of failing-gate messages (empty == all gates pass)."""
    fails = []
    ws = state.get("workspace", "")
    if not os.path.isdir(ws):
        return [f"G0 workspace: '{ws}' does not exist -- fix 'workspace' in .claude/state/survey_loop.json"]

    # G1 -- websearch novelty gap confirmed
    ng = os.path.join(ws, "novelty_gap.md")
    if not os.path.isfile(ng):
        fails.append("G1 novelty: novelty_gap.md missing -- run /novelty-scan; websearch >=10 existing "
                     "surveys, build the coverage matrix, and write novelty_gap.md with a "
                     "'NOVELTY CONFIRMED: <axis>' line")
    else:
        t = open(ng, errors="ignore").read()
        if "NOVELTY CONFIRMED" not in t:
            fails.append("G1 novelty: no 'NOVELTY CONFIRMED:' verdict in novelty_gap.md -- the empty cell "
                         "is not established; pivot the candidate axis and re-search until an uncovered "
                         "organizing axis is confirmed")

    # G2 -- verified reference base
    bib = os.path.join(ws, "refs.bib")
    if not os.path.isfile(bib):
        fails.append("G2 refs: refs.bib missing -- harvest verified references (real titles + arXiv IDs)")
    else:
        keys = re.findall(r"@\w+\{([^,\s]+),", open(bib, errors="ignore").read())
        need = int(state.get("min_refs", 60))
        if len(keys) < need:
            fails.append(f"G2 refs: {len(keys)}/{need} entries -- launch parallel research agents to "
                         "harvest more VERIFIED papers (exact title, first author, year, arXiv ID; omit "
                         "anything unverifiable)")
        dup = sorted({k for k in keys if keys.count(k) > 1})
        if dup:
            fails.append(f"G2 refs: duplicate bibkeys {dup[:6]} -- dedup refs.bib")

    # G3 -- hero taxonomy figure in the grouped-cell style
    fig = os.path.join(ws, "figures", "fig_taxonomy_main.tex")
    if not os.path.isfile(fig):
        fails.append("G3 taxonomy: figures/fig_taxonomy_main.tex missing -- build it from "
                     ".claude/skills/survey-pipeline/templates/fig_taxonomy_REFERENCE.tex")
    else:
        t = open(fig, errors="ignore").read()
        checks = {
            "forest environment":       "\\begin{forest}" in t,
            "resizebox page-fit":       "\\resizebox" in t,
            ">=5 grouped leaf cells":   t.count("align=left]") >= 5,
            "caption":                  "\\caption" in t,
            "ACM \\Description":        "\\Description" in t,
        }
        for name, ok in checks.items():
            if not ok:
                fails.append(f"G3 taxonomy: '{name}' check failed in fig_taxonomy_main.tex -- match the "
                             "grouped-cell template spec")
        ncite = len(re.findall(r"\\citep?\{", t))
        minsys = int(state.get("min_taxonomy_systems", 40))
        if ncite < minsys:
            fails.append(f"G3 taxonomy: only {ncite}/{minsys} cited systems in the figure -- populate "
                         "every branch with verified systems")

    # G4 -- clean compile, fresh PDF (main_flat.tex is generated output, not a source)
    pdf, log = os.path.join(ws, "main.pdf"), os.path.join(ws, "main.log")
    texs = [f for f in glob.glob(os.path.join(ws, "**", "*.tex"), recursive=True)
            if os.path.basename(f) != "main_flat.tex"] + [bib]
    newest = max((os.path.getmtime(f) for f in texs if os.path.isfile(f)), default=0)
    if not (os.path.isfile(pdf) and os.path.isfile(log)):
        fails.append("G4 compile: main.pdf/main.log missing -- run latexmk -pdf -interaction=nonstopmode main.tex")
    elif os.path.getmtime(pdf) < newest:
        fails.append("G4 compile: main.pdf is older than the .tex/.bib sources -- recompile")
    else:
        lt = open(log, errors="ignore").read()
        if re.search(r"undefined references|Citation .+? undefined", lt, re.I):
            fails.append("G4 compile: undefined references/citations in main.log -- fix keys and recompile")
        if re.search(r"^! ", lt, flags=re.M):
            fails.append("G4 compile: LaTeX errors ('!' lines) in main.log -- fix and recompile")

    # G5 -- fresh render of the taxonomy page
    png = state.get("render_png", "")
    if not (png and os.path.isfile(png)):
        fails.append("G5 render: render the taxonomy page (pdftoppm -png -r 110) and record its absolute "
                     "path as 'render_png' in .claude/state/survey_loop.json")
    elif os.path.isfile(pdf) and os.path.getmtime(png) < os.path.getmtime(pdf):
        fails.append("G5 render: render_png is stale (older than main.pdf) -- re-render and re-eyeball")

    # G6 -- visual confirmation by actually Reading the PNG
    if not state.get("eyeball_confirmed"):
        fails.append("G6 eyeball: Read the render PNG and verify: every node connected to the root, fits "
                     "one page, leaf text legible, branch labels graduated; then set "
                     "\"eyeball_confirmed\": true in .claude/state/survey_loop.json")

    # ---- full-pipeline gates (only when state has "full_pipeline": true, i.e. /survey) ----
    if state.get("full_pipeline"):
        # G7 -- every intended file exists and is substantive
        secs = [f for f in glob.glob(os.path.join(ws, "sections", "*.tex")) if os.path.getsize(f) >= 500]
        need_s = int(state.get("min_sections", 10))
        if len(secs) < need_s:
            fails.append(f"G7 completeness: {len(secs)}/{need_s} substantive section files (>=500B) in "
                         "sections/ -- write the remaining prose sections per the SKILL.md manifest")
        tabs = [f for f in glob.glob(os.path.join(ws, "tables", "*.tex")) if os.path.getsize(f) >= 300]
        need_t = int(state.get("min_tables", 6))
        if len(tabs) < need_t:
            fails.append(f"G7 completeness: {len(tabs)}/{need_t} tables in tables/ -- build the manifest "
                         "tables (survey_compare, definitions, compare_main, per-branch, branch_limits, "
                         "landscape)")
        if not os.path.isfile(os.path.join(ws, "figures", "fig_survey_timeline.tex")):
            fails.append("G7 completeness: figures/fig_survey_timeline.tex missing -- build it from the "
                         "novelty-scan survey list")
        flat = os.path.join(ws, "main_flat.tex")
        if not os.path.isfile(flat):
            fails.append("G7 completeness: main_flat.tex missing -- run: latexpand --empty-comments "
                         "--expand-bbl main.bbl main.tex > main_flat.tex")
        elif os.path.isfile(pdf) and os.path.getmtime(flat) < os.path.getmtime(pdf):
            fails.append("G7 completeness: main_flat.tex is stale (older than main.pdf) -- regenerate it")

        # G8 -- the audit fleet has a CURRENT clean bill (goes stale if any source changes after it)
        ar = os.path.join(ws, "audit_report.md")
        if not os.path.isfile(ar):
            fails.append("G8 audit: audit_report.md missing -- run the /survey-audit 5-agent fleet, loop "
                         "fix+re-audit until every agent returns VERDICT: CLEAN, then write "
                         "audit_report.md ending with the line 'ALL AUDITS CLEAN'")
        else:
            at = open(ar, errors="ignore").read()
            if "ALL AUDITS CLEAN" not in at:
                fails.append("G8 audit: audit_report.md lacks 'ALL AUDITS CLEAN' -- auditors found "
                             "mistakes; fix them and re-audit with the SAME agents; only write the line "
                             "when all five are CLEAN")
            elif os.path.getmtime(ar) < newest:
                fails.append("G8 audit: sources changed AFTER the last clean audit -- the clean bill is "
                             "stale; re-run the audit fleet and refresh audit_report.md")

    return fails


def main():
    if "--check" in sys.argv:                      # manual gate report
        state = load_state()
        if not state:
            print("no active survey loop (no state file)"); return 0
        fails = gates(state)
        if fails:
            print("GATES FAILING:"); [print(" -", f) for f in fails]; return 1
        print("ALL GATES PASS"); return 0

    # ---- Stop-hook mode ----
    try:
        json.load(sys.stdin)                       # hook input (unused fields ok)
    except Exception:
        pass
    state = load_state()
    if not state or state.get("status") != "in_progress":
        return 0                                   # loop disarmed -> allow stop

    fails = gates(state)
    if not fails:
        state["status"] = "done"
        save_state(state)
        return 0                                   # all gates pass -> allow stop

    it = int(state.get("iteration", 0)) + 1
    state["iteration"] = it
    cap = int(state.get("max_iterations", 15))
    if it > cap:
        state["status"] = "stalled"                # give up gracefully, never infinite-loop
        save_state(state)
        return 0
    save_state(state)

    reason = (f"[survey taxonomy loop {it}/{cap}] The taxonomy deliverable is not finished. "
              "Fix these failing gates now, in order, then the loop will release automatically:\n"
              + "\n".join(f"- {f}" for f in fails)
              + "\nConsult .claude/skills/survey-pipeline/SKILL.md for the exact spec of each artifact.")
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
