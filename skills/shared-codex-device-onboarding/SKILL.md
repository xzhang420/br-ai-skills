---
name: shared-codex-device-onboarding
description: Set up Skills Manager on another Windows, Linux, or macOS device and restore the shared skill library without losing local skills. Use for multi-device skill onboarding and synchronization setup.
---

# Skills Manager device onboarding

The user replaced the br-ai-skills Git-script policy on 2026-11-03. Do not
reinstall its daily pull jobs, automatic upstream-update job, or device-prefix
ownership restrictions. Prefixes remain labels; renaming is unnecessary.

## Current arrangement

- Official app: https://github.com/xingkongliang/skills-manager
- Private backup: https://github.com/xzhang420/skills-manager-backup
- Default library: ~/.skills-manager/skills/ on each device.
- Workstation checks author sources daily (24h).
- Apply updates automatically: OFF (notify only).
- Other devices restore the same backup; author checks can stay Off there.
- Background backup may publish saved edits before a larger task finishes.
  Backup synchronization and downloading new author versions are separate.

## Onboard

1. Inventory existing skills, links, local edits, and old schedules. Back up
   local-only skills and global instructions before changing discovery paths.
2. Install an official OS release and verify published checksums. Use this
   device's own authentication; never transfer tokens or SQLite databases.
3. Restore the private backup through the Backup page or supported CLI. Do not
   import br-ai-skills as a second backup remote.
4. Compare restored content with local-only or different skills. Review before
   replacement; do not force an overwrite or silently discard differences.
5. Deploy library skills to Codex with Skills Manager. Preserve .system and
   plugin/runtime content outside the synchronized library. Preserve required
   compatibility paths until dependent chats and scripts have been checked.
6. Verify discovery and a backup round. Background jobs require the app running;
   use tray behavior and OS-supported sign-in startup when authorized.
7. Pause old skill-pull and author-update jobs through the device's scheduler.
   Replace only the old skill-maintenance block in global AGENTS.md; keep
   unrelated project-location and scientific-workflow instructions.

## Review author updates

Keep automatic application off. Review local customizations, licenses, new
dependencies and permissions before asking to apply an update. Same-named files
can be overwritten by author updates. Backups do not establish update safety.

Use the current CLI help or manage-skills skill for install/deploy/check actions.
Do not edit the app database to bypass missing controls.

## Completion

Report version, library count, deployment path, backup result, check/apply
settings, paused old jobs, and manual steps. Never claim another device is
configured merely because a guide or repository was published.
