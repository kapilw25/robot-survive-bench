---
id: commit-shell-quoting
tools: Bash
match: git_push\.sh\s+"
severity: warn
---
# Commit-message shell quoting
Problem: inner double-quotes in `git_push.sh "..."` close the shell quote early, so a `?` or `!` in the title hits zsh globbing ("no matches found").
Fix: wrap the whole message in SINGLE quotes: `bash git_push.sh '...'`. Then the double quotes, `?`, `()`, and `+` are all literal. If the message itself has an apostrophe, drop the inner quotes instead.
