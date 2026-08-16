"""Live dashboard server: a thin Flask wrapper around docs/dashboard.build_html().

Re-gathers roster + results + samples on every request, so the page reflects new runs and
newly-wired models without a rebuild. For a static snapshot (GitHub Pages / file://) use
`python docs/dashboard.py` instead - same HTML, no server.

  pip install flask
  python docs/app.py            # -> http://127.0.0.1:5000
"""
from __future__ import annotations

from pathlib import Path

from flask import Flask, send_from_directory

import dashboard  # docs/dashboard.py (same directory)

DOCS = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(DOCS / "static"), static_url_path="/static")


@app.route("/")
def index() -> str:
    return dashboard.build_html()


@app.route("/samples.json")
def samples():
    return send_from_directory(DOCS, "samples.json")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
