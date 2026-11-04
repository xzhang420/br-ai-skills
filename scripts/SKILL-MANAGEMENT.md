# Retired custom skill synchronization

The user replaced this workflow with Skills Manager on 2026-11-03.
See [the migration guide](../SKILLS-MANAGER-MIGRATION.md).

Do not rerun install-device-policy.py, legacy bootstraps, or daily pull/upstream
prompts as normal onboarding. These files remain for deliberate recovery only.

Skills Manager handles background backup and cross-device synchronization.
Workstation checks author sources daily; automatic application stays OFF.
Updates require review and user approval. Other devices restore the same private
backup, with upstream checks Off. Live skill names no longer carry device prefixes;
the godzilla tag is organizational, not an ownership gate.

Refresh Backup before changing devices, edit the canonical Skills Manager
library, and verify backup completes afterwards. Background backup can publish
saved unfinished work; it is not a validation or release gate. In version 1.43.3,
use Back Up Again to refresh an already-running idle device.

Before retiring a legacy checkout, check uncommitted files, local-only commits,
other worktrees, renamed/removed skills, and runtime links. Preserve a verified
recovery bundle and local differences. Never push old versions over the curated
backup merely to make Git status look synchronized. Pause legacy jobs regardless
of whether their cadence is daily, weekly, or biweekly.
