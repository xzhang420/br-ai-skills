# Retired custom skill synchronization

The user replaced this workflow with Skills Manager on 2026-11-03.
See [the migration guide](../SKILLS-MANAGER-MIGRATION.md).

Do not rerun install-device-policy.py, legacy bootstraps, or daily pull/upstream
prompts as normal onboarding. These files remain for deliberate recovery only.

Skills Manager handles background backup and cross-device synchronization.
Workstation checks author sources daily; automatic application stays OFF.
Updates require review and user approval. Other devices restore the same private
backup, with upstream checks Off. Device prefixes are labels, not ownership gates.
