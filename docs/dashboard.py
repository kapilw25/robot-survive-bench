"""Build the RobotSurviveBench demo dashboard as a single self-contained HTML string.

Pulls everything LIVE from the repo so the page is always current:
  - Dataset : docs/samples.json (5 different-type LIBERO frames, fetched by scripts/fetch_libero_samples.py)
  - Metrics : the professor's 10-metric suite (p2 5.2-5.6); marks the 4 behavioural ones as the
              only metrics computable zero-shot for action-only brains, plus derived dTSR / WAS.
  - Models  : the roster from rsbench.brains.registry (wired vs stub, key set?) with any scores
              found in data/results/*.jsonl (TSR / dTSR / LHCR / RSR / SPR).

No web framework needed for the static build:
  python docs/dashboard.py              # writes docs/index.html
Live (auto-refreshing) server:
  python docs/app.py                    # Flask wrapper around this same builder
"""
from __future__ import annotations

import glob
import html
import json
import os
import sys
from dataclasses import fields
from pathlib import Path

# make the src-layout package importable when run as a plain script
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rsbench.brains import providers as _prov          # noqa: E402
from rsbench.brains.registry import REGISTRY            # noqa: E402
from rsbench.metrics.scores import behavioural_scores, dtsr, was  # noqa: E402
from rsbench.types import EpisodeResult                 # noqa: E402

DOCS = Path(__file__).resolve().parent
RESULTS_GLOB = str(ROOT / "data" / "results" / "*.jsonl")
VLA_REFS = ("pi0-fast", "vjepa2-ac", "dreamzero")       # fixed baselines for WAS (when run)

# ------------------------------------------------------------------ metrics suite
# (group, abbr, name, formula, scored-zero-shot?, note)  -- verbatim from p2 5.2-5.6
METRICS = [
    ("Behavioural", "TSR",  "Task Success Rate",              "N_success / N_total",                 True,  "primary competence signal"),
    ("Behavioural", "LHCR", "Long-Horizon Completion Rate",   "completed subgoals / total subgoals", True,  "partial credit on multi-stage tasks"),
    ("Behavioural", "RSR",  "Recovery Success Rate",          "recovered / failure events",          True,  "recover after a perturbation"),
    ("Behavioural", "SPR",  "Safety Preservation Rate",       "1 - unsafe episodes / episodes",      True,  "fraction of safe trajectories"),
    ("Predictive",  "HSLA", "Hidden-State Localization Acc.", "correct hidden queries / hidden queries", False, "needs a prediction head"),
    ("Predictive",  "CSA",  "Counterfactual Selection Acc.",  "optimal futures / counterfactual trials", False, "needs future simulation"),
    ("Predictive",  "FRE",  "Future Rollout Error",           "mean d(s_hat_t, s_t)",                False, "needs a world model rollout"),
    ("Predictive",  "ACPE", "Action Consequence Pred. Error", "mean d(o_hat_i, o_i)",                False, "needs consequence prediction"),
    ("Calibration", "ECE",  "Expected Calibration Error",     "sum |acc(b) - conf(b)| |B_b|/N",      False, "needs confidences"),
    ("Calibration", "RCS",  "Risk-Calibrated Success",        "TSR / (1 + ECE)",                     False, "needs ECE"),
]
DERIVED = [
    ("dTSR", "Delta Task Success Rate", "TSR(OOD) - TSR(normal)", "HEADLINE: does the edge survive the OOD surprise?"),
    ("WAS",  "World Advantage Score",   "(success_model - success_VLAref) / (success_VLAref + eps)", "assessed vs a fixed VLA baseline; credited to prior work, not adopted as ours"),
]

# Honest, current limitation of each brain (why its row looks the way it does / why it cannot run).
LIMITS = {
    "gemini-er2":     "preview model; robot-specialized; only exercised on the toy cartoon here",
    "kimi":           "vision OK (Fireworks); reasoning-style, verbose think tokens",
    "qwen":           "vision OK (Fireworks); large MoE, slower per step",
    "glm":            "text-blind on this Fireworks model -> must guess the side",
    "deepseek":       "text-blind + prone to max-steps loops -> must guess the side",
    "gpt":            "key valid but account has 0 credits (429) - needs billing",
    "claude":         "no ANTHROPIC_API_KEY in .env",
    "gemini":         "vision-capable but _complete() not wired (stub)",
    "llama":          "not served on this Fireworks account (needs Together/Meta key)",
    "cosmos-reason1": "open-weight VLM; GPU self-host only (no hosted API)",
    "robobrain2":     "open-weight; GPU self-host only (no hosted API)",
    "mock":           "offline scripted reference, not a real brain",
}


# ------------------------------------------------------------------ data gathering
def _rows_by_brain() -> dict[str, list[EpisodeResult]]:
    known = {f.name for f in fields(EpisodeResult)}
    out: dict[str, list[EpisodeResult]] = {}
    for path in sorted(glob.glob(RESULTS_GLOB)):
        for row in _read(path):
            er = EpisodeResult(**{k: v for k, v in row.items() if k in known})
            out.setdefault(er.brain, []).append(er)
    return out


def _read(path: str) -> list[dict]:
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def _vla_ref_success(by_brain: dict[str, list[EpisodeResult]]) -> float | None:
    for ref in VLA_REFS:
        rs = [r for r in by_brain.get(ref, []) if r.ood == "normal"]
        if rs:
            return sum(r.success for r in rs) / len(rs)
    return None


def _brain_scores(rs: list[EpisodeResult], vla_ref: float | None) -> dict:
    """Per-brain aggregate: behavioural bundle + dTSR (worst OOD vs normal) + WAS."""
    normal = [r for r in rs if r.ood == "normal"]
    ood_splits = sorted({r.ood for r in rs if r.ood != "normal"})
    b_all = behavioural_scores(rs)
    tsr_n = behavioural_scores(normal)["tsr"] if normal else None
    ood_tsrs = {s: behavioural_scores([r for r in rs if r.ood == s])["tsr"] for s in ood_splits}
    tsr_o = min(ood_tsrs.values()) if ood_tsrs else None
    d = dtsr(tsr_o, tsr_n) if (tsr_o is not None and tsr_n is not None) else None
    w = was(tsr_n, vla_ref) if (tsr_n is not None and vla_ref is not None) else None
    return {"tsr_normal": tsr_n, "tsr_ood": tsr_o, "dtsr": d, "lhcr": b_all["lhcr"],
            "rsr": b_all["rsr"], "spr": b_all["spr"], "was": w, "n": b_all["n_episodes"],
            "ood_splits": ",".join(ood_splits) or "-"}


def _wired(name: str, cls) -> bool:
    if not issubclass(cls, _prov._Provider):
        return True                                     # e.g. mock: offline reference brain
    return cls._complete is not _prov._Provider._complete


def roster_context() -> list[dict]:
    by_brain = _rows_by_brain()
    vla_ref = _vla_ref_success(by_brain)
    out = []
    for name, cls in REGISTRY.items():
        env_key = getattr(cls, "env_key", None)
        vision: bool | None = None
        if issubclass(cls, _prov.GeminiER2):
            vision = True
        elif issubclass(cls, _prov._FireworksProvider):
            vision = bool(cls.send_image)
        row = {
            "name": name,
            "model_id": getattr(cls, "model_id", "-"),
            "open": getattr(cls, "is_open_weight", None),
            "env_key": env_key,
            "key_set": bool(env_key and os.environ.get(env_key)),
            "wired": _wired(name, cls),
            "vision": vision,
            "limit": LIMITS.get(name, ""),
            "scores": _brain_scores(by_brain[name], vla_ref) if name in by_brain else None,
        }
        out.append(row)
    # sort: brains with scores first (by TSR), then wired, then the rest
    def key(r):
        s = r["scores"]
        return (0 if s else 1, -(s["tsr_normal"] or 0) if s else 0, 0 if r["wired"] else 1, r["name"])
    return sorted(out, key=key)


# ------------------------------------------------------------------ html rendering
def _esc(x) -> str:
    return html.escape(str(x))


def _pct(x) -> str:
    return "-" if x is None else f"{100 * x:.0f}%"


def _signed(x) -> str:
    if x is None:
        return "-"
    return f"{x:+.2f}"


def _yn(b, yes="yes", no="no") -> str:
    cls = "ok" if b else "no"
    return f'<span class="pill {cls}">{yes if b else no}</span>'


def _dataset_cards() -> str:
    manifest = DOCS / "samples.json"
    if not manifest.exists():
        return '<p class="empty">Run <code>scripts/fetch_libero_samples.py</code> to populate samples.</p>'
    cards = []
    for s in json.loads(manifest.read_text()):
        media = s.get("gif") or s["file"]           # animated rollout if we have it, else the still
        badge = '<span class="live">&#9654; rollout</span>' if s.get("gif") else ""
        cards.append(
            f'<figure class="card"><div class="media">'
            f'<img src="{_esc(media)}" alt="{_esc(s["suite"])}" loading="lazy">{badge}</div>'
            f'<figcaption><span class="tag">{_esc(s["suite"])}</span>'
            f'<span class="why">{_esc(s["why"])}</span>'
            f'<span class="task">"{_esc(s["task"])}"</span></figcaption></figure>'
        )
    return '<div class="grid">' + "".join(cards) + "</div>"


def _metrics_table() -> str:
    rows = []
    for group, abbr, name, formula, scored, note in METRICS:
        badge = _yn(scored, "scored", "N/A")
        rows.append(
            f'<tr class="{"scored" if scored else "na"}"><td>{_esc(group)}</td>'
            f'<td class="abbr">{_esc(abbr)}</td><td>{_esc(name)}</td>'
            f'<td class="mono">{_esc(formula)}</td><td>{badge}</td>'
            f'<td class="note">{_esc(note)}</td></tr>'
        )
    for abbr, name, formula, note in DERIVED:
        rows.append(
            f'<tr class="derived"><td>Derived</td><td class="abbr">{_esc(abbr)}</td>'
            f'<td>{_esc(name)}</td><td class="mono">{_esc(formula)}</td>'
            f'<td><span class="pill hl">headline</span></td><td class="note">{_esc(note)}</td></tr>'
        )
    body = "".join(rows)
    return (
        '<table class="metrics"><thead><tr><th>group</th><th>abbr</th><th>metric</th>'
        '<th>formula</th><th>zero-shot?</th><th>note</th></tr></thead>'
        f'<tbody>{body}</tbody></table>'
    )


def _models_table(roster: list[dict]) -> str:
    rows = []
    for r in roster:
        s = r["scores"]
        open_pill = ('<span class="pill open">open</span>' if r["open"] is True
                     else '<span class="pill closed">closed</span>' if r["open"] is False
                     else '<span class="pill">-</span>')
        status = (_yn(True, "wired", "") if r["wired"] else '<span class="pill no">stub</span>')
        keyp = _yn(r["key_set"], "set", "unset")
        sees = ('<span class="pill open">image</span>' if r["vision"] is True
                else '<span class="pill">text</span>' if r["vision"] is False
                else '<span class="pill">-</span>')
        if s:
            cells = (f'<td>{_pct(s["tsr_normal"])}</td><td>{_pct(s["tsr_ood"])}</td>'
                     f'<td class="{"neg" if (s["dtsr"] or 0) < 0 else "pos"}">{_signed(s["dtsr"])}</td>'
                     f'<td>{_pct(s["lhcr"])}</td><td>{_pct(s["rsr"])}</td><td>{_pct(s["spr"])}</td>'
                     f'<td>{_signed(s["was"])}</td><td>{s["n"]}</td>')
        else:
            cells = '<td colspan="8" class="pending">pending - supply API key, then run scripts/run_step2_tsr.sh</td>'
        idcell = (f'<td class="idcell"><span class="mono small">{_esc(r["model_id"])}</span>'
                  f'<span class="limit">&#9888; {_esc(r["limit"])}</span></td>')
        rows.append(
            f'<tr><td class="abbr">{_esc(r["name"])}</td>{idcell}'
            f'<td>{open_pill}</td><td>{status}</td><td>{keyp}</td><td>{sees}</td>{cells}</tr>'
        )
    body = "".join(rows)
    return (
        '<table class="models"><thead><tr><th>brain</th><th>model id &middot; limitation</th><th>type</th>'
        '<th>impl</th><th>key</th><th>sees</th><th>TSR<br>normal</th><th>TSR<br>OOD</th><th>dTSR</th>'
        '<th>LHCR</th><th>RSR</th><th>SPR</th><th>WAS</th><th>n</th></tr></thead>'
        f'<tbody>{body}</tbody></table>'
    )


def _findings_html() -> str:
    """A data-derived 'what this run shows' readout (observed outcome, not just the expectation)."""
    by = _rows_by_brain()

    def split_tsr(rows, ood):
        xs = [r.success for r in rows if r.ood == ood]
        return (sum(xs) / len(xs)) if xs else None

    vis, txt = [], []
    for name, cls in REGISTRY.items():
        if name not in by:
            continue
        if issubclass(cls, _prov.GeminiER2):
            v = True
        elif issubclass(cls, _prov._FireworksProvider):
            v = bool(cls.send_image)
        else:
            continue                                     # skip mock / unclassified
        (vis if v else txt).append(name)

    def mean(names, ood):
        vals = [split_tsr(by[n], ood) for n in names if split_tsr(by[n], ood) is not None]
        return (sum(vals) / len(vals)) if vals else None

    if not vis and not txt:
        return ""
    vn, vt, vc = mean(vis, "normal"), mean(vis, "transparent"), mean(vis, "clutter")
    tn = mean(txt, "normal")
    dv = (vt - vn) if (vt is not None and vn is not None) else None
    bits = []
    if vn is not None:
        bits.append(f"Vision brains ({', '.join(vis)}) averaged <b>{_pct(vn)}</b> on normal")
    if tn is not None:
        bits.append(f"text-blind brains ({', '.join(txt)}) sat at <b>{_pct(tn)}</b> (guessing the side)")
    line1 = (" vs ".join(bits) + " - so vision helps.") if len(bits) == 2 else ((bits[0] + ".") if bits else "")
    line2 = ""
    if vt is not None and vn is not None:
        clause_c = f" while <b>clutter</b> (colour kept) held at <b>{_pct(vc)}</b>" if vc is not None else ""
        line2 = (f" Under the <b>transparent</b> OOD the colour cue is wiped: vision brains fell to "
                 f"<b>{_pct(vt)}</b> (mean transparent-vs-normal = <b>{_signed(dv)}</b>){clause_c} - "
                 f"the edge did <b>not survive</b> the surprise.")
    return f'<div class="findings"><b>What this run shows (toy, n=4/split).</b> {line1}{line2}</div>'


def build_html() -> str:
    roster = roster_context()
    n_wired = sum(1 for r in roster if r["wired"] and r["name"] != "mock")
    n_scored = sum(1 for r in roster if r["scores"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RobotSurviveBench - demo dashboard</title>
<style>{_CSS}</style>{_THEME_HEAD}</head>
<body>
{_THEME_BTN}
<header>
  <h1>RobotSurviveBench <span class="sub">demo dashboard</span></h1>
  <p class="tagline">Zero-shot robotic-execution benchmark: does a brain's competence
     <strong>survive an out-of-distribution surprise?</strong> Headline = dTSR.</p>
  <div class="stats">
    <span class="stat"><b>{len(roster)}</b> models in roster</span>
    <span class="stat"><b>{n_wired}</b> wired</span>
    <span class="stat"><b>{n_scored}</b> with scores</span>
    <span class="stat"><b>4 / 10</b> metrics scored zero-shot</span>
  </div>
</header>

<section>
  <h2>1 &middot; Dataset <span class="h2sub">what the brain is scored against (5 different-type LIBERO frames)</span></h2>
  <p class="lead">Each frame is a real Franka agent-view from a different LIBERO suite. The brain sees
     this image + the instruction, plans through a fixed skill API, and a shared executor acts.</p>
  {_dataset_cards()}
</section>

<section>
  <h2>2 &middot; Metrics <span class="h2sub">the 10-metric suite; only the 4 behavioural ones are computable for action-only brains</span></h2>
  <p class="lead">Predictive + calibration metrics need a prediction / probability head that a VLA or
     skill-API brain does not expose, so they are out of scope for this zero-shot execution benchmark.</p>
  {_metrics_table()}
</section>

<section>
  <h2>3 &middot; Models <span class="h2sub">the frontier-brain roster; scores fill in as API keys arrive</span></h2>
  <p class="lead">Contestants are swapped through one fixed executor + skill API. Wired today:
     <code>gemini-er2</code> (vision) and <code>glm</code> / <code>kimi</code> / <code>qwen</code> /
     <code>deepseek</code> (via one Fireworks key); the rest are stubs awaiting a key.</p>
  <div class="caveat"><b>Vision-required toy.</b> The toy <code>state_text</code> no longer gives positions:
     a red and a blue mug sit at left/right (side randomised per seed) and the brain may refer to a mug by
     <i>side only</i> - so it must <b>read the image</b> to know which side is red. <code>gemini-er2</code>,
     <code>kimi</code>, <code>qwen</code> see the image (<span class="pill open">image</span>);
     <code>glm</code>, <code>deepseek</code> are text-blind here (<span class="pill">text</span>) and must
     guess (~50%). The <b>transparent OOD wipes the colour cue</b> (both mugs go glassy) so even vision
     brains must guess - the edge should <b>not survive</b> (negative dTSR); the <b>clutter OOD</b> keeps
     colour but obstructs the approach (SPR drops, TSR holds). Still a tiny proxy on <b>n=6/split</b>, not
     LIBERO - the real substrate makes pixels the <i>only</i> source of identity and pose.</div>
  {_models_table(roster)}
  {_findings_html()}
  <p class="foot">Sources: roster from <code>rsbench.brains.registry</code>; scores from
     <code>data/results/*.jsonl</code>; metrics from the ACTION-ATLAS proposal (p2 5.2-5.6).
     Regenerate: <code>python docs/dashboard.py</code>.</p>
</section>
{_THEME_SCRIPT}
</body></html>
"""


_CSS = """
/* LIGHT is the default (bare :root); DARK overrides under [data-theme=dark]. */
:root{
  --bg:#f6f7f9;--card:#ffffff;--line:#dfe3ea;--rowline:#eef1f5;--hover:#eef3f9;
  --fg:#1a1f29;--mut:#5c6672;--acc:#a4670a;
  --ok:#1a7f4b;--no:#c62828;--pos:#1a7f4b;--neg:#c62828;--open:#1565c0;--closed:#6a3fb5;
  --code-bg:#eef1f5;--code-fg:#8a5a00;--derived-bg:#fbf4e2;
  --header-a:#ffffff;--header-b:#eceff4;
  --caveat-bg:#fdf6e3;--caveat-bd:#e6d8a8;--caveat-fg:#6b5510;
  --findings-bg:#ecfaf1;--findings-bd:#bce3cb;--findings-fg:#155c33;--findings-strong:#148a4f;
  --limit:#b0532a;--btn-bg:#ffffff;--btn-bd:#dfe3ea;--imgbg:#e9edf2;--shadow:rgba(20,30,50,.12);
}
:root[data-theme="dark"]{
  --bg:#0f1115;--card:#171a21;--line:#262b36;--rowline:#1c212b;--hover:#1a1f29;
  --fg:#e6e9ef;--mut:#9aa4b2;--acc:#ffd23f;
  --ok:#37d67a;--no:#ef5350;--pos:#37d67a;--neg:#ef5350;--open:#4aa3ff;--closed:#b48cff;
  --code-bg:#0b0d12;--code-fg:#e6c96b;--derived-bg:#15130a;
  --header-a:#141821;--header-b:#0f1115;
  --caveat-bg:#1c1608;--caveat-bd:#4a3b12;--caveat-fg:#d9c9a3;
  --findings-bg:#0f2016;--findings-bd:#245038;--findings-fg:#bfe6cf;--findings-strong:#7fe0a3;
  --limit:#d98b6b;--btn-bg:#171a21;--btn-bd:#2a3140;--imgbg:#000;--shadow:rgba(0,0,0,.4);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;padding:0 0 60px}
.themebtn{position:fixed;top:14px;right:16px;z-index:50;cursor:pointer;background:var(--btn-bg);
  color:var(--fg);border:1px solid var(--btn-bd);border-radius:20px;padding:6px 12px;font-size:13px;
  font-weight:600;box-shadow:0 1px 4px var(--shadow)}
header{padding:28px 28px 20px;border-bottom:1px solid var(--line);background:linear-gradient(180deg,var(--header-a),var(--header-b))}
h1{margin:0;font-size:26px}h1 .sub{color:var(--acc);font-weight:500;font-size:16px}
.tagline{color:var(--mut);margin:8px 0 14px;max-width:820px}
.tagline strong{color:var(--fg)}
.stats{display:flex;gap:10px;flex-wrap:wrap}
.stat{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 12px;color:var(--mut);font-size:13px}
.stat b{color:var(--acc);font-size:16px}
section{padding:24px 28px;border-bottom:1px solid var(--line)}
h2{font-size:19px;margin:0 0 4px}
.h2sub{color:var(--mut);font-weight:400;font-size:13px;display:block;margin-top:2px}
.lead{color:var(--mut);max-width:900px;margin:6px 0 16px}
code{background:var(--code-bg);border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:13px;color:var(--code-fg)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}
.card{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.media{position:relative}
.card img{width:100%;display:block;aspect-ratio:1/1;object-fit:cover;background:var(--imgbg)}
.live{position:absolute;top:8px;left:8px;background:rgba(239,83,80,.92);color:#fff;font-size:11px;
  font-weight:700;letter-spacing:.02em;padding:3px 8px;border-radius:20px;box-shadow:0 1px 4px rgba(0,0,0,.4)}
figcaption{padding:10px 12px;display:flex;flex-direction:column;gap:4px}
.tag{color:var(--acc);font-weight:600;font-size:13px}
.why{color:var(--mut);font-size:12px}
.task{font-size:12px;color:var(--fg);font-style:italic}
table{width:100%;border-collapse:collapse;font-size:13px;overflow-x:auto;display:block}
thead th{text-align:left;color:var(--mut);font-weight:600;border-bottom:1px solid var(--line);padding:8px 10px;white-space:nowrap}
tbody td{padding:8px 10px;border-bottom:1px solid var(--rowline);white-space:nowrap}
tbody tr:hover{background:var(--hover)}
.abbr{color:var(--acc);font-weight:600}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.small{font-size:11px;color:var(--mut)}
.note{color:var(--mut)}
tr.na td{opacity:.62}
tr.derived td{background:var(--derived-bg)}
.pill{display:inline-block;border-radius:20px;padding:2px 9px;font-size:11px;font-weight:600;border:1px solid var(--line);color:var(--mut)}
.pill.ok{background:rgba(55,214,122,.16);color:var(--ok);border-color:transparent}
.pill.no{background:rgba(239,83,80,.16);color:var(--no);border-color:transparent}
.pill.hl{background:rgba(255,190,40,.20);color:var(--acc);border-color:transparent}
.pill.open{background:rgba(21,101,192,.14);color:var(--open);border-color:transparent}
.pill.closed{background:rgba(106,63,181,.14);color:var(--closed);border-color:transparent}
.pos{color:var(--pos)}.neg{color:var(--neg)}
.pending{color:var(--mut);font-style:italic}
.idcell{white-space:normal;min-width:240px;max-width:320px}
.findings{background:var(--findings-bg);border:1px solid var(--findings-bd);border-radius:8px;padding:11px 14px;margin:16px 0 0;
  color:var(--findings-fg);font-size:13px;line-height:1.55}
.findings b{color:var(--findings-strong)}
.limit{display:block;margin-top:3px;color:var(--limit);font-size:11.5px;line-height:1.4}
.empty{color:var(--mut)}
.caveat{background:var(--caveat-bg);border:1px solid var(--caveat-bd);border-radius:8px;padding:10px 14px;margin:0 0 16px;
  color:var(--caveat-fg);font-size:13px;line-height:1.55}
.caveat b{color:var(--acc)}
.foot{color:var(--mut);font-size:12px;margin-top:14px}
@media (max-width:640px){header,section{padding-left:16px;padding-right:16px}.themebtn{top:10px;right:10px}}
"""

# Applied in <head> BEFORE paint so a saved dark choice does not flash light first.
_THEME_HEAD = ("<script>(function(){try{if(localStorage.getItem('rsb-theme')==='dark')"
               "document.documentElement.setAttribute('data-theme','dark');}catch(e){}})();</script>")

_THEME_BTN = '<button id="themeToggle" class="themebtn" aria-label="Toggle light or dark theme">Dark</button>'

# Toggle handler (kept as a plain string so its braces are literal inside the f-string page).
_THEME_SCRIPT = """<script>
(function(){
  var b=document.getElementById('themeToggle');
  function label(){var dark=document.documentElement.getAttribute('data-theme')==='dark';
    b.textContent=dark?'☀ Light':'\U0001F319 Dark';}
  label();
  b.addEventListener('click',function(){
    var dark=document.documentElement.getAttribute('data-theme')==='dark';
    if(dark){document.documentElement.removeAttribute('data-theme');}
    else{document.documentElement.setAttribute('data-theme','dark');}
    try{localStorage.setItem('rsb-theme',dark?'light':'dark');}catch(e){}
    label();
  });
})();
</script>"""


def main() -> None:
    out = DOCS / "index.html"
    out.write_text(build_html(), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
