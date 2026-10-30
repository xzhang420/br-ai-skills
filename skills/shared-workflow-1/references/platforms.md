# Shared workflow and local device setup

The shared core is `shared-workflow-1/`. The installer derives the current home
and `CODEX_HOME`, installs profiles/agents there, and writes a local entry-point
pointer. No source file should embed another device's absolute installation path.
The chat invocation stays `$workflow-1` on Ubuntu and Windows alike.

## Ubuntu / Linux

From the repository root, with Python 3.10+ and Codex already installed:

```bash
python3 skills/shared-workflow-1/scripts/install.py
python3 skills/shared-workflow-1/scripts/install.py --apply --replace-legacy
python3 skills/shared-workflow-1/scripts/orchestrate.py doctor
```

Existing repo-wide `~/.codex/skills` links are reused. Without one, the installer
links `~/.agents/skills/workflow-1` to this source. Project paths are selected
per run via `--project`, independently of the shared checkout.

## Windows / PowerShell

From the same repository root, using the installed Python 3.10+ launcher:

```powershell
py -3 .\skills\shared-workflow-1\scripts\install.py
py -3 .\skills\shared-workflow-1\scripts\install.py --apply --replace-legacy
py -3 .\skills\shared-workflow-1\scripts\orchestrate.py doctor
```

If `py` is unavailable, use the actual Python executable or `python` after
checking `python --version`. Existing repository directory links are reused.
Otherwise `--skill-install auto` tries a symlink, then falls back to a managed
copy if symlink permissions are unavailable. `--skill-install copy` selects the
copy explicitly and requires no symlink privilege. A copied installation must be
refreshed by rerunning the installer after pulling repository updates. Old copies
and replaced settings are backed up. An existing unmanaged skill requires the
explicit `--replace-legacy` migration option.

The installer does not change Windows execution policy or require an elevated
shell. It installs only into the user's directories unless CODEX_HOME points
elsewhere. Native Windows end-to-end validation remains a separate device test;
Ubuntu integration tests and mocked Windows-specific adapters are not that test.

## Local settings, not shared settings

Each device gets `<CODEX_HOME>/workflow1-local.json` (normally
`~/.codex/workflow1-local.json`). The installer creates it only if absent and
preserves existing content. `config/device-settings.example.json` is a portable
empty template, not a place for machine paths or credentials.

Default `commands: {}` uses `codex` and `claude` from this device's PATH. Override
only when necessary, using JSON argument arrays rather than shell strings:

```json
{
  "schema_version": 1,
  "commands": {
    "codex": ["C:/Tools/Codex/codex.exe"],
    "claude": ["C:/Tools/Claude/claude.exe"]
  },
  "env_file": "C:/Users/your-name/private/workflow1.env"
}
```

Those Windows paths are examples; use real local paths. On Linux the same fields
can name executables under that user's home or a different software directory.
An env-file path can also be relative to the local settings file. Omit env_file
or use null when credentials come from the environment/provider's own login.
Store secret values only in the private env file or provider credential store.

`doctor`, `plan` and `execute` accept `--device-config PATH` for an alternate
local settings file. Explicit `--env-file` overrides its env_file. The Python
interpreter is selected by the caller: use the appropriate project environment
for analysis/tests and the SDK environment for Gemini. Account/model access must
be checked separately on every device; local executable discovery is not proof
of authentication or access. Model/effort fallback is never silently relabeled.

Python on Windows may launch `.cmd`/`.bat` wrappers via a command shell even
with shell=False. For provider prompts, this coordinator requires a native
executable, or a native launcher plus script, e.g.
`["C:/Program Files/nodejs/node.exe", "C:/Tools/codex/cli.js"]` with real paths.
It deliberately reports a clear error for batch wrappers instead of guessing a
quoting scheme. See https://docs.python.org/3/library/subprocess.html.

## Test commands and Windows paths

`--test` retains POSIX-style argument quoting on every OS. For paths containing
spaces or backslashes, `--test-argv` accepts a JSON argument list. For compatibility
with both Windows PowerShell and PowerShell 7, prefer a JSON file:

```powershell
@'
["C:/Research/project/.venv/Scripts/python.exe","-m","unittest","-v","test_metrics.py"]
'@ | Set-Content -Encoding UTF8 test-command.json
py -3 .\scripts\orchestrate.py test --run 'C:/Research/project/.workflow1/runs/ID' --test-argv-file .\test-command.json --artifact 'C:/Research/project/metrics.py' --artifact 'C:/Research/project/test_metrics.py'
```

Run the example from the skill directory, or use the script's absolute path.
The same JSON forms work on Linux with Linux paths. The helper never evaluates
these argument lists as shell commands. Logs/specifications are explicitly UTF-8
so Greek symbols and international paths do not depend on the Windows code page.
JSON input/settings and private env files also accept a UTF-8 BOM, as emitted by
Windows PowerShell's UTF8 encoding.

## Optional Gemini SDK environment

Keep the SDK environment outside the shared repository. On Linux:

```bash
python3 -m venv ~/.local/share/workflow1/venv
~/.local/share/workflow1/venv/bin/python -m pip install google-genai
```

On Windows PowerShell:

```powershell
py -3 -m venv "$env:LOCALAPPDATA\Workflow1\venv"
& "$env:LOCALAPPDATA\Workflow1\venv\Scripts\python.exe" -m pip install google-genai
```

Invoke orchestrate.py with that environment's interpreter for research. Each
device requires its own approved credential setup and cost/data authorization.
Claude is installed and logged in separately; credentials never travel in Git.
