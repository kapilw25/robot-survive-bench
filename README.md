# robot-survive-bench

**Does a world model's advantage survive an out-of-distribution surprise?**

A zero-shot (inference-only, no training) robotic-execution benchmark. We take frozen policies from three model families - and, in v2, frontier-LLM "brains" - and drop them into a distribution no existing suite covers, then measure whether the world-model advantage over a direct VLA baseline survives.

## ❓ The question

Existing suites (LIBERO, SIMPLER, RoboDojo, World-in-World) test clean, rigid, opaque objects on a tidy tabletop. `robot-survive-bench` changes only what the camera sees - transparent / reflective objects and dense clutter / occlusion - on the same DROID/Franka arm, so frozen policies still run with no training.

## 🧬 Families (zero-shot)

- ⚡ **VLA** (direct action) - pi0-FAST (language)
- 🧠 **LWM** (latent world model) - V-JEPA-2-AC (image-goal MPC)
- 🎬 **WAM** (world-action model) - DreamZero (language)

A training-free interface layer (cross-embodiment adapters, encoder-as-cost MPC, planner + scripted controller) extends coverage to 11 of 15 released models. v2 adds frontier-LLM brains as swappable contestants (see `plan/v2/`).

## 📏 Metric

Behavioural Task Success Rate (TSR). Headline: `dWAS = WAS(OOD) - WAS(normal)` = "did the edge survive?" (per model, `dTSR` in code).

## 🗂️ Codebase layout

```
src/rsbench/                              # the package (src-layout)
  types.py   skills/api.py               # shared types + the FIXED skill contract
  brains/{base,llm_base,mock_brain,providers,registry}.py   # contestants (swap the brain)
  envs/{base,mock_env,libero_env,ood}.py + __init__.py      # substrates + OOD split + factory
  loop/runner.py                         # closed-loop driver + CLI
  metrics/scores.py                      # behavioural: TSR, LHCR, RSR, SPR + derived dTSR, WAS
  leaderboard/{build,social}.py          # 2 boards + social draft
  baselines/base.py                      # fixed pi0-FAST / V-JEPA-2-AC / DreamZero
  utils/{config,io,logging,seeding,visualize}.py
docs/{dashboard.py,app.py,index.html,samples.json,static/samples/*}   # demo dashboard (static + Flask)
scripts/*.sh (+ fetch_libero_samples.py)   configs/{default,skills, suites/*, models/*}
data/{raw,ood,results}/   boards/   logs/   notebooks/   tests/   .github/workflows/ci.yml
pyproject.toml   requirements.txt   Makefile   .env.example
```

## 🚀 Build steps -> code -> run (see `plan/v2/README.md`)

| # | 🚀 Step | 🧩 Wired to | ▶️ Run | 🔧 Stub to fill in |
|---|---|---|---|---|
| 1️⃣ | one closed loop | `loop/runner` + `envs/mock_env` (`libero_env` stub) + `brains` (`gemini-er2`) | `make step1` | `envs/libero_env.py` (LIBERO reset / execute / success) |
| 2️⃣ | TSR over 10 tasks | `metrics/scores.tsr` | `make step2` | - (works on mock) |
| 3️⃣ | swap the brain | `brains/{llm_base,providers,registry}` all through the fixed `skills/api` | `make step3` | `brains/providers.py` `_complete()` (provider SDK, temp=0) |
| 4️⃣ | OOD -> dTSR | `envs/ood` + `metrics.dtsr` | `make step4` | `envs/ood.py` `apply_ood()` (transparent / clutter image transforms) |
| 5️⃣ | go live | `leaderboard/{build,social}` + `.github/workflows/ci.yml` (runs on release) | `make board` | `baselines/base.py` (pi0-FAST / V-JEPA-2-AC / DreamZero checkpoints) |

## ⚡ Quickstart

```bash
make setup     # create venv + install (editable)
make smoke     # end-to-end MOCK loop, no external deps: runs the pipeline + builds boards
make step1     # one closed-loop episode (mock brain + mock env)
make step4     # normal + transparent + clutter -> dTSR
make board RESULTS=data/results/smoke.jsonl   # build the 2 leaderboards + social draft
```

Runs today on the mock with zero external deps: Step 1 prints `SUCCESS` (TSR 1.000), Step 4 reports `dTSR` (transparent -1.000, clutter -0.667), Step 5 writes `boards/board_all.md` + `board_open_weight.md` + a social draft. Model API keys go in `.env` (see `.env.example`); LIBERO + provider SDKs are optional until you fill the stubs above.

## 📊 Demo dashboard (`docs/`)

One self-contained page showing the three moving parts - **Dataset** (5 different-type LIBERO frames), **Metrics** (the 10-metric suite; only the 4 behavioural ones are computable zero-shot), and **Models** (roster with live TSR / dTSR / LHCR / RSR / SPR / WAS). It is wired to real data: `gemini-er2` shows live scores today, the other contestants fill in as keys arrive.

```bash
make samples      # fetch the 5 LIBERO sample frames (one per suite)
make dashboard    # build the static page -> docs/index.html
make serve        # OR live server (needs: pip install flask) -> http://127.0.0.1:5000
```

See [`docs/README.md`](docs/README.md) for how each section is sourced and how to add a model's scores.

## 🧭 Plan docs

| 🗂️ Path | 📌 What | 🔖 Status |
|---|---|---|
| [`plan/v2/`](plan/v2/README.md) | 📊 live frontier-brain robot-execution board (+ [`novelty_map.md`](plan/v2/novelty_map.md)) | ✅ CURRENT |
| [`plan/v1/`](plan/v1/README.md) | 🤖 pre-pivot world-model reproduction | 📌 baselines |
| [`plan/plan_dataset.md`](plan/plan_dataset.md) · [`plan/plan_rejections_risks.md`](plan/plan_rejections_risks.md) | 📦 dataset menu · 🩸 novelty / scoop ledger | 🔗 shared ref |
| [`plan/v0_proposal/`](plan/v0_proposal/) · [`plan/legacy/`](plan/legacy/plan_engineering.md) | 📄 original proposal + dashboard · 🗺️ retired vision | 🕰️ archive |
