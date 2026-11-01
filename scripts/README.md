# Codex Skill Sync Bootstrap

Use these scripts when adding a new computer to the shared Codex skill repo.

For ongoing daily synchronization, single-device third-party updates, and
persistent commit/push instructions, follow [SKILL-MANAGEMENT.md](SKILL-MANAGEMENT.md).
Existing devices should use `install-device-policy.py`, not rerun the import bootstrap.

## Windows

Install Git for Windows, then clone the repo:

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\dev" -Force
git clone https://github.com/xzhang420/br-ai-skills.git "$env:USERPROFILE\dev\br-ai-skills"
cd "$env:USERPROFILE\dev\br-ai-skills"
```

Run the bootstrap script with the device prefix you want that computer to own:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\bootstrap-windows.ps1 -DevicePrefix personal
```

If prompted for GitHub authentication, complete it. If the script reports an authentication failure, run `gh auth login` or sign in through Git Credential Manager, then rerun the script.

## Linux

Install Git, then clone the repo:

```bash
mkdir -p ~/dev
git clone https://github.com/xzhang420/br-ai-skills.git ~/dev/br-ai-skills
cd ~/dev/br-ai-skills
```

Run the bootstrap script with the device prefix you want that computer to own:

```bash
bash scripts/bootstrap-linux.sh godzilla
```

If GitHub rejects the push, run `gh auth login` or configure a personal access token, then rerun the script.

## What The Scripts Do

- Pull the latest shared repo.
- Merge existing local `~/.codex/skills` into the repo without overwriting repo files, while skipping Codex-managed `.system` skills.
- Back up the old local skills folder.
- Link `~/.codex/skills` to the shared repo's `skills` folder.
- Commit and push any newly imported local skills.
- Print the ownership line to add to that computer's biweekly skill-review automation prompt.

Restart Codex after the script finishes.

## Safe periodic pulls

`sync-skills.ps1` synchronizes only this repository's `main` checkout with
`origin/main`. Run it with PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-skills.ps1
```

It requires the expected remote and a clean working tree, including no untracked
files. It skips local-only commits, divergence, other branches, and active Git
operations. It uses fast-forward-only pulls, disables autostash, and never commits
or pushes. Authentication is non-interactive. Exit code 1 means attention is
needed; do not automatically repair, stash, reset, or rebase after a failed run.

The script serializes its own runs with a local Git-directory lock. It rechecks
the checkout after fetching; it cannot lock out every external editor or Git
client, so avoid editing while a pull is running.

Use the app's supported scheduler to run this script daily on each
device that needs it. Local scheduled tasks need the computer on and the app
running. Schedule registration is device-local, not installed by a Git pull.
No startup trigger or background push is installed by this script.

Test safeguards using disposable local repositories:

```powershell
python scripts/test_sync_skills.py
```

## Agent-Reach runtime

The portable skill is registered in `third-party-skills.toml`. Git synchronizes
its instructions, not the executable or account state. Install the runtime
separately on each device using the upstream installation guide:
https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md

Use the official GitHub release, not the unrelated PyPI `agent-reach` package.
Default setup provides GitHub, YouTube, Bilibili, V2EX, and web channels. Run live
checks to distinguish installed dependencies from working platform access.
Optional account-based channels and speech-to-text keys are separate setup steps.
Keep all login state and keys outside this repository. Upstream setup may also
install skill copies for other detected agents; those local copies are not Git
sources of truth. Runtime updates can refresh the shared copy if it is registered
with `agent-reach skill link`, so review resulting changes before committing.
