.PHONY: setup step1 step2 step3 step4 board social test lint smoke samples dashboard serve
export PYTHONPATH := src:$(PYTHONPATH)

setup:            ## create venv + install (editable)
	bash scripts/setup_env.sh

step1:            ## one closed-loop episode (mock by default)
	bash scripts/run_step1_one_episode.sh $(BRAIN) $(SUITE)

step2:            ## TSR over the 10 tasks
	bash scripts/run_step2_tsr.sh $(BRAIN) $(SUITE)

step3:            ## swap the brain: route all contestants through the fixed API
	bash scripts/run_step3_swap_brains.sh $(SUITE)

step4:            ## OOD: normal + transparent + clutter, report dTSR
	bash scripts/run_step4_ood.sh $(BRAIN) $(SUITE)

board:            ## build the 2 leaderboards + social draft
	bash scripts/build_leaderboard.sh $(RESULTS)

social:           ## draft a social post from results
	python -m rsbench.leaderboard.social --results $(RESULTS)

test:             ## run unit + smoke tests
	pytest -q

lint:
	ruff check src tests

smoke:            ## end-to-end mock smoke (no external deps)
	python -m rsbench.loop.runner --brain mock --suite mock --ood all --out data/results/smoke.jsonl
	python -m rsbench.leaderboard.build --results data/results/smoke.jsonl --out boards

samples:          ## fetch 5 different-type LIBERO frames for the demo gallery
	python scripts/fetch_libero_samples.py

dashboard:        ## build the static demo page -> docs/index.html
	python docs/dashboard.py

serve:            ## live dashboard server (needs flask); re-reads data each request
	python docs/app.py
