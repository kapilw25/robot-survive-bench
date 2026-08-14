#!/bin/bash
: '
=============================================================================
Git Push Script - Multi-Account Support (CODE PUSH ONLY)
=============================================================================

Pushes code to GitHub only. The HF outputs-upload step was REMOVED (2026-05-30) —
this script no longer touches HuggingFace, so a forgotten flag can never trigger a
slow/destructive HF sync. Credentials (per-account GitHub PATs) are loaded from the
gitignored .env (GITHUB_TOKEN_KAPIL / GITHUB_TOKEN_GAYTRI) — never hardcoded here.

Usage:
    chmod +x git_push.sh           # make it executable (once)
    bash git_push.sh "updating"    # commit + push code (no flags — --code-only was removed)

To back up outputs/ to HF MANUALLY (separate, opt-in — no longer part of this script):
    python -u src/utils/hf_outputs.py upload outputs 2>&1 | tee logs/hf_upload_outputs_$(date +%Y%m%d_%H%M%S).log

Example:
    % ./git_push.sh "testing git push"
    Select account:
    1) Kapil
    2) Gaytri
    Enter choice [1/2]: 1
    ...
    Pushed as Kapil
    Done (code push only)

=============================================================================
'

MESSAGE=""

for arg in "$@"; do
    case "$arg" in
        --*) echo "Error: flags removed — this script is code-push only (no --code-only). Pass just the commit message."; exit 1 ;;
        *) MESSAGE="$arg" ;;
    esac
done

if [ -z "$MESSAGE" ]; then
    echo "Error: Commit message required"
    echo "Usage: ./git_push.sh \"commit message\""
    exit 1
fi

# Load credentials from .env (gitignored) — tokens NEVER live in this tracked script.
ENV_FILE="$(dirname "$0")/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "FATAL: $ENV_FILE not found (needs GITHUB_TOKEN_KAPIL / GITHUB_TOKEN_GAYTRI)"
    exit 1
fi
set -a; . "$ENV_FILE"; set +a

echo "Select account:"
echo "1) Kapil"
echo "2) Gaytri"
read -p "Enter choice [1/2]: " CHOICE

if [ "$CHOICE" = "2" ]; then
    git config user.name "GaytriJena"
    git config user.email "gaytrijena2000@gmail.com"
    USERNAME="GaytriJena"
    TOKEN="$GITHUB_TOKEN_GAYTRI"
    ACCOUNT="Gaytri"
else
    git config user.name "kapilw25"
    git config user.email "kapilw25@gmail.com"
    USERNAME="kapilw25"
    TOKEN="$GITHUB_TOKEN_KAPIL"
    ACCOUNT="Kapil"
fi

if [ -z "$TOKEN" ]; then
    echo "FATAL: GitHub token for $ACCOUNT not set in $ENV_FILE"
    echo "  add GITHUB_TOKEN_KAPIL=<pat> and GITHUB_TOKEN_GAYTRI=<pat> there"
    exit 1
fi

# Preflight: verify the token actually authenticates BEFORE we commit, so an
# expired/revoked/wrong PAT fails fast with a clear message instead of the
# confusing post-commit "Authentication failed" that git prints. Validates auth
# via the GitHub API (GET /user); the token is sent in a header, never printed.
echo "Verifying $ACCOUNT token with GitHub..."
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' \
    -H "Authorization: Bearer $TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/user)

case "$HTTP_CODE" in
    200)
        echo "Token OK (GitHub authenticated $ACCOUNT)."
        ;;
    000|"")
        echo "WARNING: could not reach the GitHub API to preflight the token (offline, or curl missing). Proceeding anyway."
        ;;
    *)
        TOKVAR="GITHUB_TOKEN_$(printf '%s' "$ACCOUNT" | tr '[:lower:]' '[:upper:]')"
        echo "FATAL: GitHub rejected the $ACCOUNT token (HTTP $HTTP_CODE) - nothing was committed."
        echo "  The PAT in $ENV_FILE is likely expired, revoked, or missing scope."
        echo "  Fix: regenerate a PAT (classic: 'repo'; fine-grained: Contents=Read/Write) as $USERNAME,"
        echo "       then update $TOKVAR in $ENV_FILE and re-run."
        exit 1
        ;;
esac

git add .
git commit -m "$MESSAGE"

# Disable credential helper temporarily and use token directly
GIT_TERMINAL_PROMPT=0 git -c credential.helper= push https://${USERNAME}:${TOKEN}@github.com/kapilw25/robot-survive-bench.git main

echo "Pushed as $ACCOUNT"

# HF upload removed (2026-05-30): this script ONLY pushes code — it never touches HuggingFace,
# so there is no longer any HF step to skip (the old --code-only flag was therefore removed).
# HF backup is now a separate, opt-in manual step (run the outputs-upload util directly).
echo "Done (code push only)"
