# Skills management moved

Since 2026-11-03, Skills Manager is the live library and synchronization tool.
This repository is retained for migration history and recovery.

- [Device setup and migration guide](SKILLS-MANAGER-MIGRATION.md)
- [New private backup repository](https://github.com/xzhang420/skills-manager-backup)

Do not run the legacy sync, bootstrap, or author-update scripts on a migrated
device. Keep the old checkout: this workstation still uses its local system
and runtime folders, which are intentionally excluded from the new backup.

Third-party author checks run daily on workstation while Skills Manager is
running. Automatic application is OFF; review and approval are required.
Other devices still need the setup steps in the guide.
