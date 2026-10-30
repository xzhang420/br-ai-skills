# Workflow 1

A skill-first scientific workflow: Astra plans/interprets, Sol implements,
Terra optionally checks figures, Claude independently critiques/reviews, and
Gemini optionally researches public literature. Native OpenAI fallback review
is labeled explicitly. Human scientific acceptance remains separate.

The folder `shared-workflow-1` is the canonical workflow shared across devices. The
frontmatter name `workflow-1` preserves the requested `$workflow-1` invocation.
The content and helper code are portable; secrets and runtime state are not synced.
Device configuration is resolved locally; Ubuntu and Windows use the same core.

## Install from the shared checkout

```bash
python3 skills/shared-workflow-1/scripts/install.py
python3 skills/shared-workflow-1/scripts/install.py --apply --replace-legacy
```

Run from your `br-ai-skills` checkout. On Windows PowerShell use:

```powershell
py -3 .\skills\shared-workflow-1\scripts\install.py
py -3 .\skills\shared-workflow-1\scripts\install.py --apply --replace-legacy
```

Use Python 3.10+; replace `py -3` with your Python executable if needed.
Dry-run is the default. The installer:

- Reuses the existing `~/.codex/skills -> <checkout>/skills` sync link when it
  exposes this exact canonical skill; otherwise creates one user-scope symlink
  at `~/.agents/skills/workflow-1`. If symlinks are unavailable, `auto` falls back
  to a managed copy; `--skill-install copy` selects that explicitly.
- Backs up earlier standalone/device-owned copies before retiring duplicate entries.
- Installs both profile overlays and eight explicit mode-specific agent TOMLs.
- Adds a short pointer to the global `AGENTS.md`; keeps unrelated guidance.
- Creates `~/.codex/workflow1-local.json` only if absent, for this device's
  command paths and optional private env-file path.
- Never edits base `config.toml`, installs credentials, runs Git, or pushes.

Backups and an exact action manifest live under `~/.codex/backups/workflow1-*`.
The earlier ZIP/extracted tools folder is not needed by this skill and is left
untouched. Do not rerun its old installer, which would restore a duplicate skill.

Keep the checkout in a permanent location. After `git pull`, rerun the installer
to update copied skills, profiles and agent definitions on each device. Existing
device settings remain local and are preserved. You do not need to run the general
repository bootstrap, which also imports and publishes unrelated local skills.

For a new Linux checkout:

```bash
mkdir -p ~/dev
git clone https://github.com/xzhang420/br-ai-skills.git ~/dev/br-ai-skills
cd ~/dev/br-ai-skills
python3 skills/shared-workflow-1/scripts/install.py --apply
```

For a new Windows checkout:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\dev" | Out-Null
git clone https://github.com/xzhang420/br-ai-skills.git "$env:USERPROFILE\dev\br-ai-skills"
Set-Location "$env:USERPROFILE\dev\br-ai-skills"
py -3 .\skills\shared-workflow-1\scripts\install.py --apply
```

If the checkout already exists, use `git pull --rebase --autostash` there instead
of cloning again. The same shared skill is maintained through explicit authorized
updates; device-owned review automations should not independently fork it.
See [platform setup](references/platforms.md) for executable paths, Windows
argument lists, private env files and Python environment differences.

## Invoke from a chat

In VS Code select GPT-6 Astra with High or Extra High, then enter:

```text
$workflow-1 Use lower efforts. Plan [your task].
PLAN ONLY; do not implement yet.
```

Use `higher` for Higher Efforts. The selected request stays with that workflow.
Natural-language requests cannot silently change an existing parent runtime.
The skill must report mismatches. Mode-specific subagents carry explicit effort.

In a terminal, from your project:

```bash
codex --profile workflow1-lower
# or:
codex --profile workflow1-higher
```

These launch profiles do not change an existing VS Code chat. Use `/skills` or
the `$` selector to check discovery and `/subagents` to inspect actual delegation.
If discovery is stale, restart Codex. See [effort levels](references/effort-levels.md).

## Local run records

The helper uses Python 3.10+ and the standard library for native/Claude operation:

```bash
python3 scripts/orchestrate.py init --project /path/to/project \
  --objective "Compare synthetic plating coverage and uniformity" --mode lower
python3 scripts/orchestrate.py status --run /path/printed/by/init
python3 scripts/orchestrate.py record --help
python3 scripts/orchestrate.py mode --run /path/to/run --mode higher
```

Run these from this skill directory, or use the script's absolute path. `init`
creates `.workflow1/runs/<id>/` in the chosen project. `record` saves native-agent
reports and their provenance; prior contents are retained as versions. Freeze,
approval and acceptance are distinct steps. Mode changes invalidate active
approval/evidence without relabeling older results.

No runtime files belong in this shared checkout. Do not include confidential raw
data in reports submitted to external providers. An authenticated CLI does not
authorize sharing project contents.

## Optional cross-provider coordinator

Claude Code must be installed and authenticated separately. Run `claude auth login`
and `claude auth status` locally if needed. The coordinator requests the pinned
Opus model with mode-specific effort and records returned model identity where
available; provider restrictions may cap effort or change available models.

```bash
python3 scripts/orchestrate.py doctor
python3 scripts/orchestrate.py plan --run /path/to/run \
  --reviewer claude --allow-external
```

`doctor` reads `<CODEX_HOME>/workflow1-local.json` when present. Default command
names come from this device's PATH. Optional `--device-config PATH` and
`--env-file PATH` select local overrides without changing the shared source.
Its availability checks do not make model calls or prove account access.

`--allow-external` asserts the user's authorization to send the specified project
reports and approved artifacts to Claude. Plan ends at a frozen specification.
Read it and record the user's approval with `approve --run ...` before execution.
Execution requires a real deterministic test command and an explicit manifest
of the code, tests and inputs whose contents must match the validation evidence:

```bash
python3 scripts/orchestrate.py execute --run /path/to/run \
  --test 'python3 -m unittest -v test_metrics.py' \
  --artifact metrics.py --artifact test_metrics.py \
  --reviewer claude --allow-external
```

List every relevant code/input/test file with repeated `--artifact` options;
directories are not scanned implicitly. The test command's actual exit code,
output log and file hashes are recorded; source mutation invalidates acceptance.
Files omitted from this explicit manifest are not covered by that hash check.
Use `--test-argv` or `--test-argv-file` instead of `--test` for literal Windows
paths. A JSON argument-list file avoids PowerShell version-specific quoting;
see the [Windows example](references/platforms.md#test-commands-and-windows-paths).
Arguments are passed directly to a process, without shell evaluation.
Native orchestration can use the same deterministic gate via `test --run ...
--test ... --artifact ...`. Native independent reviews start with `DECISION:`;
test-validation reports start with `VERDICT:`. Record a separate `stage-report`
from Astra after successful validation.

Repairs are bounded to two rounds; methodological failures return to planning.
Astra prepares interpretation and the workflow waits for human acceptance.
Only after the user's decision use `accept --run ... --decision accept|reject
--reason 'the user decision and rationale'`. This is a recorded human decision,
not an automatic reviewer vote or an authentication mechanism.
`--reviewer codex` deliberately selects the labeled OpenAI fallback; no automatic
provider substitution occurs.

For Gemini Deep Research use a separate environment **outside this repository**:

```bash
python3 -m venv ~/.local/share/workflow1/venv
~/.local/share/workflow1/venv/bin/python -m pip install google-genai
```

Windows SDK setup uses `venv/Scripts/python.exe`; see
[platform setup](references/platforms.md#optional-gemini-sdk-environment).

If Ubuntu has no ensurepip but `uv` is installed, the venv interpreter created by
the first command can be populated with `uv pip install --python
~/.local/share/workflow1/venv/bin/python google-genai`.

Obtain a Gemini API key privately from https://aistudio.google.com/apikey. Set
`GEMINI_API_KEY` in the launching environment or put it in a private local env
file outside Git (restrict file permissions). Never paste secrets into a chat.
`--env-file` parses only known credential assignments literally, without sourcing
shell code. Existing environment values take precedence. No credentials or billing
are created by the installer.

```bash
~/.local/share/workflow1/venv/bin/python scripts/orchestrate.py plan \
  --run /path/to/run --reviewer claude --research \
  --env-file /private/path/workflow1.env \
  --allow-external --allow-research-cost
```

Only use the research flags after the user approves the data scope and API cost.
Gemini CLI login is unrelated to Deep Research API credentials. A timed-out
background research task may continue on Google's service; its saved interaction
ID supports polling again rather than silently launching duplicate paid work.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 scripts/install.py
python3 scripts/orchestrate.py doctor
```

Offline tests exercise real state/approval/routing and process handling with
clearly labeled provider stubs. They do not prove live model access. Installation
evidence and synthetic live tests are stored separately on the target device.
The shared promotion was tested on Ubuntu, including real process execution,
copy installs and migration. Windows argv/batch-wrapper/termination adapters were
tested with platform-specific contracts and mocks. A native Windows installation
and provider run must still be validated on the target computer.

Official references:
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/config-file/config-advanced
- https://code.claude.com/docs/en/model-config
- https://ai.google.dev/gemini-api/docs/deep-research
