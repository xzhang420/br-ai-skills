<!-- br-ai-skills:begin -->
## Shared skill maintenance

This device is `{{DEVICE}}`. The shared skills checkout is `{{REPO}}`.
Before creating, installing, editing, or updating a user-maintained skill,
including through a linked skills directory or from another project, read that
checkout's `AGENTS.md` and `third-party-skills.toml`. Work in the shared checkout,
not in a duplicate local copy. Preserve device ownership and third-party rules.

After completing and validating an authorized skill change, stage only this
task's portable files, commit, pull/rebase, and push without asking again.
Do not finish silently with an unpublished change: report the commit, push
result, and any remaining changes or blocker. Never include unrelated work,
secrets, runtime state, plugins, caches, or `skills/.system/`. Never force-push.
Stop on conflicts, authentication failures, or uncertain overwrites.

This is task-completion behavior, not a file watcher and not permission to
edit additional skills. Read-only tasks do not authorize commits or pushes.
Scheduled pulls are a separate, strictly pull-only workflow; their safeguards
take precedence over the interactive pull/rebase/autostash instructions.
Only the primary device in the registry may run third-party upstream updates.
If filesystem/network access is missing, report it; do not weaken permissions.
<!-- br-ai-skills:end -->
