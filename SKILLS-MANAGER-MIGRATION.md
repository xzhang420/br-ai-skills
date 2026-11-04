# Skills Manager: multi-device setup

User decision: 2026-11-03. Replace the old scripts and device-ownership rules
with Skills Manager. On 2026-11-04 the shared library removed device prefixes
from skill names. Keep the `godzilla` tag where useful; `personal`, `workstation`,
and `shared` tags are retired. Tags do not restrict editing or execution.

This guide is a historical-repository copy of the setup plan. On migrated
devices, also read `~/.skills-manager/skills/DEVICE-SETUP.md` and the live
`codex-device-onboarding` skill before acting: they can be newer than this repo.

## New arrangement

- Library: `~/.skills-manager/skills/` (Windows: `%USERPROFILE%\.skills-manager\skills`).
- Private backup: https://github.com/xzhang420/skills-manager-backup
- Workstation is the designated author-update checker: Daily / 24 hours.
- **Apply updates automatically: Off (notify only).** Review before applying.
- Other devices: use the same backup; leave author checks Off to avoid duplicate work.
- Cross-device backup runs in the app independently of author-update checks.
  Saved unfinished edits may be backed up. This is not a validated-release gate.
- In version 1.43.3, backup/sync runs at startup and after local changes settle
  (about two minutes), not as a continuous remote poll while idle. When switching
  to an already-running device, use Backup > Back Up Again to refresh it.
- The app must be running and online. Minimize to tray. This workstation has a
  Windows sign-in shortcut; configure startup separately on the other devices.
- This old br-ai-skills checkout is retained for recovery, not live editing.
- Codex-managed .system/plugin/runtime content is not part of the new backup.

## Device roles and everyday sync

| Device | Live library | Author checks | Automatic application | Backup/sync |
| --- | --- | --- | --- | --- |
| Workstation | Skills Manager | Daily / 24 hours | Off; approval after review | On |
| Personal PC | Skills Manager | Off | Off | On |
| Godzilla | Skills Manager after verified migration | Off | Off | On after restore |

Before editing on another device, refresh Backup and resolve any Needs attention
items. Edit the canonical library, let backup finish, then refresh on the other
device. Avoid editing the same skill on two devices at once. A clean historical
Git checkout does not establish that the live library is synchronized. Check
both the app's backup state and its actual agent deployments.

Saved files, uncommitted Git changes, and committed-but-unpushed changes are
different states. Git cannot detect text still unsaved in an editor. Inventory
all three disk states before switching discovery paths; preserve local commits
in a verified Git bundle and keep the old checkout available for comparison.
Do not automatically re-import skills removed from the shared library or
recreate old names after a rename. Consult backup history first.

## Personal PC (Windows)

1. Save open skill edits. Back up any local-only skills before migration.
2. Install the current Windows release from
   https://github.com/xingkongliang/skills-manager/releases/latest
3. Open Skills Manager. Choose **restore from a backup**, using:
   `https://github.com/xzhang420/skills-manager-backup.git`.
   Authenticate with your own GitHub account on this device when prompted.
   Do not create another backup repository or import br-ai-skills as the remote.
4. Compare the restored library with local skills, matching renamed skills as
   well as exact folder names. Preserve differing local versions separately;
   do not apply old third-party versions over the restored library automatically.
5. In Global Workspace, deploy the library to Codex. If an existing folder/link
   blocks deployment, back it up and migrate it; never click through an uncertain
   overwrite. Preserve local system/runtime skills outside the backup library.
6. Settings: author checks Off; automatic application Off. Leave Automatic backup
   and Skill-aware sync merge ON. Use Minimize to tray and launch after sign-in
   (add the installed app to Windows Startup if desired). Name the device personal.
7. Confirm the Backup page reaches an up-to-date state and Codex discovers skills.
8. Find and pause all old skill-pull and third-party-update tasks on this PC,
   including weekly or biweekly jobs, not just tasks whose names say daily.
   Replace the old br-ai-skills maintenance block in global AGENTS.md with the
   policy below. Keep unrelated instructions unchanged.

## Godzilla (Ubuntu/Linux)

Follow the same restore/deploy/verification steps with the matching official
Linux release (.deb for Debian/Ubuntu, AppImage where suitable). Preserve local
Godzilla skill differences before replacing old links. Use the device's own GitHub
authentication. Author checks and automatic application remain Off here.
Leave Automatic backup and Skill-aware sync merge ON. Name the device godzilla;
add the installed app to your desktop session's Startup Applications if desired.
Pause old skill-sync schedules only after verifying the restored library.
Do not copy Windows paths, credentials, or the Windows app database to Linux.

## Policy for migrated devices

Skills Manager is the live skill library and backup/sync manager. Use its
supported app/CLI for installation, source metadata, deployment, and backup.
Edit user-maintained content in its canonical library, not the historical
br-ai-skills checkout. Keep automatic author updates OFF; review and obtain user
approval before applying. Skill names have no device prefixes; the `godzilla`
tag is organizational, not a device ownership or execution gate.
Never sync credentials, full .codex state, system skills, plugins, or caches.
Do not reinstall the old Git-script schedules or auto-commit policy.

## Reviewing a third-party update

On workstation, open the Library's available update, inspect the diff and local
adaptations, then apply only after approval. Same-named files can be overwritten;
the app's removed-file warning does not protect those edits. Preserve licensing
and review new scripts, dependencies, permissions, and changed behavior.
Check Backup after applying so approved content reaches the other devices.

## Recovery

The old checkout and GitHub history remain. A pre-migration Git bundle and global
instruction backup were saved on workstation under
`C:\Users\zhang_x3\.codex\backups\skills-manager-migration-20261103`.
Do not run both old and new synchronization against the same live library.
Keep the old checkout on workstation: local system/runtime links still use it.
Other-device setup is not complete merely because this guide is available.

## Personal PC migration record: 2026-11-04

- Checked out current `br-ai-skills` main at `7495790` into
  `C:\Users\X\Documents\ChatGPT\br-ai-skills`; fast-forward pull was up to date.
- The old `C:\Users\X\dev\br-codex-skillset` checkout and its two known detached
  worktrees had no uncommitted changes. The old checkout contained commit
  `eceec31` (third-party updates), absent from the downloaded repository history.
  Its cached `origin/main` was stale; the old remote URL now resolves to the
  current `br-ai-skills` main. Do not push or rebase that old checkout to repair it.
- Saved and verified a full Git bundle, the previous global instructions, the
  old automation configuration, and a file comparison under
  `C:\Users\X\.codex\backups\skills-manager-migration-20261104`.
- Installed official Skills Manager 1.43.3 after checking its published SHA-256.
  Restored the existing private backup at `3724243`, with 41 library skills and
  zero commits ahead or behind at restore time. Backup history records intentional
  skill removals and prefix removal; the 41-skill count is a snapshot, not a quota.
- Compared 66 old non-system skill folders: 33 matched restored names after
  normalization, 17 of those had differing old files, and 33 were absent from
  the restored library. The old versions remain in the unchanged legacy checkout.
  Detailed paths are in the recovery folder's `local-skill-comparison.json`.
- Moved the old `.codex\skills` junction to the recovery folder as `skills-before`.
  Deployed all 41 library skills to a new `.codex\skills` directory through the
  supported CLI and verified readable `SKILL.md` files. Its `.system` junction
  still points to the legacy checkout's local `.system` folder.
- Installed the migrated-device policy in the previously empty global
  `C:\Users\X\.codex\AGENTS.md` and added a Skills Manager sign-in shortcut.
- During verification, eight newer skills arrived from the existing shared
  backup. Deployed those through the CLI too: final library/deployment count was
  49/49, with every deployed SKILL.md readable. The library was clean and zero
  commits ahead/behind at `1a4beff` when checked. This count can change on later syncs.
- Verified in the app: device name `personal`, Automatic backup ON, Skill-aware
  sync merge ON, author checks OFF, automatic application OFF. Set close behavior
  to Minimize to tray. A manual Back Up Again completed with the app showing
  Backed up; the existing private remote and main branch were retained.
- The old `biweekly-third-party-codex-skill-upstream-check` automation remains
  ACTIVE: the supported app tool returned `Failed to update automation`, and its
  old project is absent from the current project list. Pause it manually in its
  owning scheduler. The new global policy directs any old updater invocation to
  stop without changing or publishing skills; this is not a verified scheduler pause.
- Pending: pause the legacy updater and verify discovery in a fresh Codex
  session. The 49 deployed skill paths are verified; this existing chat may
  retain its older skill catalog until restarted.
- Godzilla was not accessed or migrated in this session. Run its own inventory,
  restore, deployment, backup, and schedule-retirement checks on that device.
