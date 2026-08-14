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

# Preflight: BEFORE committing, verify the chosen account can actually PUSH to
# THIS repo - not merely that the token is valid. This catches both failure
# modes we hit: an expired/revoked PAT (HTTP 401) AND a valid token whose owner
# lacks write access (a post-commit HTTP 403 "denied to <user>" from git). It
# queries the repo API and reads permissions.push; the token is sent in a
# header, never printed. Retries once after a short pause so a freshly created
# token / collaborator grant that is still activating is not falsely rejected.
REPO_SLUG="kapilw25/robot-survive-bench"

check_push_access() {
    local resp code body
    resp=$(curl -s -w $'\n%{http_code}' \
        -H "Authorization: Bearer $TOKEN" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "https://api.github.com/repos/$REPO_SLUG")
    code=$(printf '%s' "$resp" | tail -n1)
    body=$(printf '%s' "$resp" | sed '$d')
    case "$code" in
        200) if printf '%s' "$body" | grep -qE '"push":[[:space:]]*true'; then echo OK; else echo NOPUSH; fi ;;
        401) echo BADTOKEN ;;
        403) echo FORBIDDEN ;;
        404) echo NOREPO ;;
        000|"") echo NONET ;;
        *) echo "HTTP_$code" ;;
    esac
}

echo "Verifying $ACCOUNT push access to $REPO_SLUG..."
ACCESS=$(check_push_access)
if [ "$ACCESS" != "OK" ] && [ "$ACCESS" != "NONET" ]; then
    echo "  (got '$ACCESS' - retrying in 3s in case a new token/grant is still activating...)"
    sleep 3
    ACCESS=$(check_push_access)
fi

TOKVAR="GITHUB_TOKEN_$(printf '%s' "$ACCOUNT" | tr '[:lower:]' '[:upper:]')"
case "$ACCESS" in
    OK)
        echo "Access OK ($ACCOUNT can push to $REPO_SLUG)."
        ;;
    NONET)
        echo "WARNING: could not reach the GitHub API (offline, or curl missing). Proceeding anyway."
        ;;
    NOPUSH|FORBIDDEN)
        echo "FATAL: $ACCOUNT ($USERNAME) authenticated but has NO push access to $REPO_SLUG - nothing was committed."
        echo "  Add $USERNAME as a collaborator with Write, or pick the account that owns the repo."
        echo "  (Fine-grained PATs also need Repository access = this repo, Contents = Read and write.)"
        exit 1
        ;;
    BADTOKEN)
        echo "FATAL: GitHub rejected the $ACCOUNT token (HTTP 401) - nothing was committed."
        echo "  The PAT in $ENV_FILE is likely expired or revoked."
        echo "  Fix: regenerate a PAT as $USERNAME, then update $TOKVAR in $ENV_FILE and re-run."
        exit 1
        ;;
    NOREPO)
        echo "FATAL: $ACCOUNT ($USERNAME) cannot see $REPO_SLUG (private repo without access, or it does not exist) - nothing was committed."
        echo "  Confirm the repo name, and that $USERNAME has access to it."
        exit 1
        ;;
    *)
        echo "FATAL: unexpected GitHub API response ($ACCESS) verifying push access - nothing was committed."
        echo "  Re-run; if it persists, check https://www.githubstatus.com/ and your network."
        exit 1
        ;;
esac

git add .
git commit -m "$MESSAGE"

# Disable credential helper temporarily and use token directly
GIT_TERMINAL_PROMPT=0 git -c credential.helper= push https://${USERNAME}:${TOKEN}@github.com/${REPO_SLUG}.git main

echo "Pushed as $ACCOUNT"

# HF upload removed (2026-05-30): this script ONLY pushes code — it never touches HuggingFace,
# so there is no longer any HF step to skip (the old --code-only flag was therefore removed).
# HF backup is now a separate, opt-in manual step (run the outputs-upload util directly).
echo "Done (code push only)"
