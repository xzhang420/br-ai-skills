# Daily shared skills pull (every device)

Read the local CODEX_HOME/skills-device.json (default ~/.codex/skills-device.json)
and operate only on its repository path. If missing or mismatched with the
expected br-ai-skills checkout, stop and report setup needed.

On Windows run powershell -NoProfile -ExecutionPolicy Bypass -File
REPO/scripts/sync-skills.ps1, substituting the verified absolute REPO path.
On Linux/macOS run python3 REPO/scripts/sync-skills.py.

Read JSON output and process exit code. These scripts permit only clean-tree
fast-forward pulls from the expected origin/main. Never stage, commit, push,
stash, rebase, reset, delete, resolve conflicts, install software, update
third-party upstreams, or change schedules. These scheduled-pull restrictions
override interactive skill-edit instructions. If the script is missing,
permissions/authentication fail, or it returns needs_attention, stop and report
the blocker without bypassing safeguards. Report before/after commits for
updated, or no changes needed for up_to_date. Do not access other repositories
or devices. Continue daily until the user changes or disables the schedule.
