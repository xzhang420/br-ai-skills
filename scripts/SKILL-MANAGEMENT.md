# Multi-device skill management

The GitHub repository is the shared source of truth. There are three independent
pieces; pulling this repository alone does not install global instructions or
device-local schedules.

1. After an authorized skill-edit task finishes and validates, commit only its
   portable changes, pull/rebase, push, and verify. No confirmation is needed.
   This is not a filesystem watcher: unfinished/manual edits are not auto-pushed.
2. Every device pulls daily at 09:00 local time using the clean-tree,
   expected-origin, main-only, fast-forward-only guard. No auto-repair.
3. Only `primary_update_device` in `third-party-skills.toml` checks original
   authors daily at 08:30 local time, reviews and validates safe registered
   updates, then commits/pushes. Other devices never update upstreams directly.
   Different device time zones can mean an update arrives on the next day's pull.

## One-time setup on each device

For an existing checkout with linked skills, run from the repository:

```powershell
python scripts/install-device-policy.py --device workstation
```

Use `personal` on the personal computer, `godzilla` on Godzilla, and `python3`
on Linux/macOS. The script appends/replaces only its marked block in the global
Codex AGENTS.md, retains unrelated instructions, makes a one-time local backup,
and writes local `skills-device.json`. It stops if an AGENTS.override.md would
hide the rule or if an existing identity differs. Neither file is Git-synced.
Restart/start a fresh agent session to load the new global instructions.

Use the app's scheduling tools on each device; inspect and update existing jobs
rather than creating duplicates. `prompts/daily-pull.md` is the pull job; only
the primary device gets `prompts/daily-third-party-update.md`. Resolve absolute
paths and verify device identity when installing. The primary assignment is
not a distributed lock: do not register two computers as the same primary.

The schedule needs access to this checkout and GitHub. Test a normal manual run
in the same task context; success under interactive elevation alone does not
prove an unattended job can run. If blocked, report the precise folder/network
permission needed. Do not turn on broad full access or alter security settings
automatically. Local jobs require the computer and app to be running. No tool
for manual scheduler runs means scheduled execution is not yet verified.

On Linux/macOS the pull command is `python3 scripts/sync-skills.py`; Windows
keeps the existing PowerShell script. Both report JSON and fail closed.

For new devices, first follow the onboarding skill to clone/link skills. Inspect
existing local changes before the legacy import bootstrap, which stages broad
paths; do not use it as a routine sync or policy-install command.

## Boundaries and recovery

- Global AGENTS.md covers agents that load it; it is not an account-wide ChatGPT
  memory or a promise that cloud chats can access a computer. For another client,
  place the same scoped rule in that client's supported project instructions.
- Prefixes describe ownership, not which devices may use a portable skill.
- Upstream baseline unknown, local adaptations unclear, validation failure,
  expanded permissions, or license changes: leave that entry unchanged and ask.
- No automatic skill additions/deletions, dependency or executable installation,
  plugin/system updates, credentials, or whole-.codex synchronization.
- Dirty checkout, local commits, divergence, or auth failure: report and leave
  work intact. A failed publish is not completion; report the unpushed commit.
- To disable automation, update its status using the app scheduler. To remove
  global policy, remove only the marked block after user approval; preserve other
  instructions. Do not restore a whole old backup over newer user instructions.

## Acceptance checklist (run separately on every computer)

- Correct repository origin/main and linked skills.
- Correct global instruction block and local device identity.
- One daily pull schedule, with a successful manual/scheduled result in context.
- Only the primary device has one daily upstream-update schedule.
- A real authorized edit reports validation, commit, verified push, and clean
  task state; do not manufacture a skill change solely to test publication.

Instructions are persistent guidance, not an enforcement guarantee. Inspect
these completion reports and scheduled failures rather than assuming success.
