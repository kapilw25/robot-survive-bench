#!/usr/bin/env python3
"""Generate the 200+ work comparison longtable (tab_landscape.tex) from TSVs.

Usage:  python3 gen_landscape.py <combined.tsv> <tags.tsv> <output.tex>

combined.tsv rows: bibkey<TAB>ShortName<TAB>Year<TAB>Venue<TAB>subarea<TAB>focus(<=6 words)
tags.tsv rows:     bibkey<TAB>ships<TAB>learn<TAB>eval<TAB>embod<TAB>selfimpr   ('?' = unverified)

EDIT SUPER/SUBNAME below for the new topic's grouping BEFORE running. Controlled vocab:
ships: weights|code|reward|skill|plan|repr|worldmodel|data|bench|policy
learn: il|rl|offlinerl|llm|selfsup|modelbased|na    eval: real|sim|game|offline|na
embod: arm|mobile|legged|humanoid|hand|multi|na     selfimpr: yes|partial|no
"""
import sys

if len(sys.argv) != 4:
    sys.exit(__doc__)
COMBINED, TAGS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

# ---- EDIT PER TOPIC: (super-category label, [subareas]) in display order ----
SUPER = [
    ("End-to-end \\& generalist policies", ["VLA", "generalist", "pretraining"]),
    ("Imitation \\& diffusion policies", ["imitation", "diffusion-policy"]),
    ("LLM/VLM planning \\& task-and-motion", ["llm-planning", "tamp", "code-policy"]),
    ("LLM reward synthesis \\& data generation", ["reward-synth", "data-gen"]),
    ("Unsupervised skill discovery \\& hierarchical RL", ["skill-discovery", "hierarchical-rl"]),
    ("World models \\& model-based RL", ["world-model", "model-based-rl"]),
    ("Representation learning \\& offline RL", ["repr-control", "offline-rl"]),
    ("Manipulation, dexterity \\& sim-to-real", ["manipulation", "dexterous", "sim2real"]),
    ("Locomotion \\& humanoid control", ["locomotion", "humanoid"]),
    ("Navigation, tactile \\& affordance", ["navigation", "tactile-affordance"]),
    ("Datasets, benchmarks \\& simulators", ["dataset", "benchmark", "simulator"]),
]
SUBNAME = {  # subarea -> italic sub-heading
    "VLA": "Vision-language-action", "generalist": "Generalist / multi-task",
    "pretraining": "Video / action pretraining", "imitation": "Imitation learning",
    "diffusion-policy": "Diffusion policies", "llm-planning": "LLM task planning",
    "tamp": "LLM task-and-motion", "code-policy": "Code / prompt as policy",
    "reward-synth": "LLM reward synthesis", "data-gen": "Generative data / augmentation",
    "skill-discovery": "Unsupervised skill discovery", "hierarchical-rl": "Hierarchical / option RL",
    "world-model": "World models", "model-based-rl": "Model-based RL",
    "repr-control": "Visual representation learning", "offline-rl": "Offline RL",
    "manipulation": "Manipulation / grasping", "dexterous": "Dexterous / in-hand",
    "sim2real": "Sim-to-real transfer", "locomotion": "Legged locomotion",
    "humanoid": "Humanoid control", "navigation": "Visual / language navigation",
    "tactile-affordance": "Tactile \\& affordance", "dataset": "Datasets",
    "benchmark": "Benchmarks", "simulator": "Simulators",
}
VENUE = {"ScienceRobotics": "Sci.~Rob.", "ACL-Findings": "ACL", "arXiv/TMLR": "arXiv"}

def esc(s):
    return s.replace("&", "\\&").replace("#", "\\#").replace("_", "\\_").replace("%", "\\%")

SHIPS = {"weights": "weights", "code": "code", "reward": "reward", "skill": "skill", "plan": "plan",
         "repr": "repr", "worldmodel": "world-model", "data": "data", "bench": "bench", "policy": "policy"}
LEARN = {"il": "IL", "rl": "RL", "offlinerl": "offline-RL", "llm": "LLM", "selfsup": "self-sup",
         "modelbased": "model-based", "na": "--"}
EMBOD = {"arm": "arm", "mobile": "mobile", "legged": "legged", "humanoid": "humanoid",
         "hand": "hand", "multi": "multi", "na": "--"}

def evalcell(t):
    return {"real": "\\dreal", "sim": "\\dsim", "game": "\\dgame",
            "offline": "\\textcolor{gray!70}{\\textsf{offline}}"}.get(t, "\\dm")

def sicell(t):
    return {"yes": "\\yy", "partial": "\\pp", "no": "\\nn"}.get(t, "\\dm")

def plain(t, m):
    v = m.get(t)
    return "\\dm" if (v is None or t in ("?", "na")) else "\\textsf{%s}" % v

papers, order = {}, []
for line in open(COMBINED):
    line = line.rstrip("\n")
    if not line.strip():
        continue
    p = line.split("\t")
    while len(p) < 6:
        p.append("")
    key, name, year, venue, sub, focus = p[:6]
    papers[key] = dict(name=name, year=year, venue=venue.strip(), sub=sub.strip(), focus=focus)
    order.append(key)

tags = {}
try:
    for line in open(TAGS):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        p = line.split("\t")
        while len(p) < 6:
            p.append("?")
        tags[p[0]] = dict(ships=p[1].strip(), learn=p[2].strip(), eval=p[3].strip(),
                          embod=p[4].strip(), si=p[5].strip())
except FileNotFoundError:
    pass

buckets = {lbl: {sa: [] for sa in subs} for lbl, subs in SUPER}
unassigned = []
for key in order:
    sub = papers[key]["sub"]
    for lbl, subs in SUPER:
        if sub in subs:
            buckets[lbl][sub].append(key)
            break
    else:
        unassigned.append(key)

total = len(order)
L = []
L.append("% AUTO-GENERATED by gen_landscape.py; do not hand-edit.")
L.append("{\\scriptsize")
L.append("\\setlength{\\tabcolsep}{4pt}")
L.append("\\renewcommand{\\arraystretch}{1.1}")
L.append("\\begin{longtable}{@{}p{0.27\\textwidth} c l l c l c@{}}")
L.append(("\\caption{\\textbf{The broader landscape: %d representative works, compared on six axes.} "
          "Grouped into areas and sub-grouped by family. Columns: \\textbf{Year}, \\textbf{Ships} "
          "(what the method contributes), \\textbf{Learn} (primary learning signal), \\textbf{Eval} "
          "(\\dreal/\\dsim/\\dgame/offline), \\textbf{Embod.} (embodiment), and run-time \\textbf{S.I.} "
          "(self-improvement: \\yy\\ yes, \\pp\\ partial, \\nn\\ no). A \\dm\\ marks not-applicable or "
          "unverified. Every entry is a real, individually citeable paper.}"
          "\\label{tab:landscape}\\\\" % total))
hdr = ("\\textbf{System / work} & \\textbf{Year} & \\textbf{Ships} & \\textbf{Learn} & "
       "\\textbf{Eval} & \\textbf{Embod.} & \\textbf{S.I.}\\\\")
L += ["\\toprule", hdr, "\\midrule", "\\endfirsthead",
      "\\multicolumn{7}{@{}l}{\\scriptsize\\emph{Table~\\ref{tab:landscape} (continued)}}\\\\",
      "\\toprule", hdr, "\\midrule", "\\endhead", "\\bottomrule", "\\endlastfoot"]

emitted = 0
for lbl, subs in SUPER:
    grpn = sum(len(buckets[lbl][sa]) for sa in subs)
    if grpn == 0:
        continue
    L.append("\\multicolumn{7}{@{}l}{\\rule{0pt}{2.6ex}\\textbf{\\textsf{%s}}~\\textcolor{gray}{(%d)}}\\\\[1pt]"
             % (lbl, grpn))
    for sa in subs:
        keys = buckets[lbl][sa]
        if not keys:
            continue
        keys.sort(key=lambda k: (papers[k]["year"], papers[k]["name"].lower()))
        L.append("\\multicolumn{7}{@{}l}{\\hspace{0.6em}\\emph{%s}}\\\\" % SUBNAME.get(sa, sa))
        for k in keys:
            p, t = papers[k], tags.get(k, {})
            L.append("\\hspace{0.6em}\\textbf{%s}~\\cite{%s} & %s & %s & %s & %s & %s & %s\\\\" % (
                esc(p["name"]), k, esc(p["year"]), plain(t.get("ships", "?"), SHIPS),
                plain(t.get("learn", "?"), LEARN), evalcell(t.get("eval", "?")),
                plain(t.get("embod", "?"), EMBOD), sicell(t.get("si", "?"))))
            emitted += 1
    L.append("\\addlinespace[2pt]")
L += ["\\end{longtable}", "}"]
open(OUT, "w").write("\n".join(L) + "\n")
print("wrote", OUT, "| total", total, "| emitted", emitted, "| unassigned", len(unassigned),
      "| tagged", len(tags))
for k in unassigned:
    print("  UNASSIGNED", k, papers[k]["sub"])
