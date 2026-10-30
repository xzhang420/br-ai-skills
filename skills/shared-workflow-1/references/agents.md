# Agents and provider boundaries

Native Codex roles are configured by `scripts/install.py` from `config/agents/`.
Per-device executable locations and optional private env-file paths belong in
`<CODEX_HOME>/workflow1-local.json`, not in the shared agent definitions.
Read [platform setup](platforms.md) when installing on another operating system.
The skill defines the sequence; the host supplies the actual spawn/wait tools.
Use independent review contexts. An OpenAI reviewer is a fallback, never Claude.

Claude uses the locally authenticated Claude Code CLI, a fresh nonpersistent
session, pinned `claude-opus-5-5`, and `--effort high|max`. Review can read
approved artifacts; shell/write tools and unrelated MCP servers are excluded.
Those tool controls are not a substitute for an OS security boundary. Restrict
the project to approved material before authorizing external reads. Review
findings cite actual files and tests, not only the implementer's account.

Gemini CLI and Gemini Deep Research are different interfaces. This workflow's
research helper uses `google-genai` and the Interactions API with background
execution, an interaction ID, polling, timeout and resume. A Gemini CLI login
does not supply API credentials. Both research IDs are preview services;
recheck official availability if a call fails. Never silently substitute an
ordinary Gemini chat model for Deep Research.

Provider prerequisites can be inspected with `orchestrate.py doctor` without
running inference. It reports availability, not guaranteed account access.
Use `claude auth status` for Claude login; never copy auth files into the repo.
An optional local `--env-file` loads only supported credential keys without
executing shell text. Do not put the file inside the skill or shared repo.

Cross-provider commands require `--allow-external`; Gemini also requires
`--allow-research-cost`. Set these only after user authorization covering the
data and cost. A flag records the caller's authorization; it does not infer it.
No billing activation or credential creation is automated. Without credentials,
keep that provider pending and continue independent native work.

Provider metadata is stronger evidence than prose claims about identity.
Keep requested model/effort separate from observed fields; note provider
fallbacks or settings caps. An API result may not expose resolved effort.
