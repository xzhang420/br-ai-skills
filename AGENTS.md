# Skills Manager migration

The user retired the custom Git-script and device-ownership policy on 2026-11-03.
Skills Manager replaces it for live skill management and cross-device sync.
This checkout remains migration history and recovery material, not a second
automatic writer to the live library. Read SKILLS-MANAGER-MIGRATION.md.

- Do not run legacy bootstrap, policy installers, pull schedules, or automatic
  upstream-update prompts as the normal workflow.
- Work in the Skills Manager library on migrated devices. Read its DEVICE-SETUP.md
  and codex-device-onboarding skill for the latest migration state. Device prefixes
  were removed from live skill names on 2026-11-04; keep useful godzilla tags,
  but do not recreate personal/workstation/shared tags or ownership restrictions.
- Check authors daily on workstation, with automatic application OFF. Review
  differences and obtain user approval before applying third-party updates.
- Preserve licenses and local adaptations during review. Never synchronize
  auth, sessions, logs, databases, caches, plugins, or system/runtime skills.
- Do not copy the entire .codex directory or overwrite unrelated local work.
- For authorized maintenance of this historical checkout, stage only task files,
  validate, commit and push. Never force-push. Report publication blockers.
