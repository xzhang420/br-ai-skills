# Agents and provider boundaries

Native Codex roles are configured by `scripts/install.py` from `config/agents/`.
Per-device executable locations and optional private env-file paths belong in
`<CODEX_HOME>/workflow1-local.json`, not in the shared agent definitions.
Read [platform setup](platforms.md) when installing on another operating system.
The skill defines the sequence; the host supplies the actual spawn/wait tools.
Use independent review contexts. An OpenAI reviewer is a fallback, never Claude.

## Default Claude review and readiness

Claude participates at both planning critique and post-implementation independent
review unless the user explicitly selects an OpenAI fallback or opts out. This
applies to native orchestration as well as the helper's default
`--reviewer claude`. The coordinator must not choose `--reviewer codex` on the user's behalf
because native delegation is easier, readiness is untested, or consent is unclear.

At the start, inspect `orchestrate.py doctor` and the configured Claude CLI's
`auth status`; reuse current evidence for the same device/configuration. Record
whether installation/authentication/model access is verified or still untested.
An installed CLI is not authenticated access, and authentication is not proof of
the pinned model. The first authorized scoped review can verify model access;
do not add a paid probe when that real review supplies the evidence.

Check existing provider, artifact and cost authorization. If incomplete, prepare
the actual minimal review packet and ask once, early, for the missing scope:
files/artifact types, planning/validation stages, permitted revisions and excluded
data. Reuse permission within those bounds; a one-version approval remains a
one-version approval. Public/synthetic material or explicitly approved unpublished
excerpts/derived reports may be sent. Never infer blanket source-folder access.
Include the definitions and evidence the reviewer needs within the approved
packet; a reference to an unavailable file is not a self-contained review.

Missing consent keeps Claude **pending**, not unavailable. For a genuine CLI,
auth, model, quota, network or host blocker, record the observed error and offer
resolving it or explicitly choosing the native fallback. Continue useful native
preparation, but do not call the required review complete or silently substitute
providers. Never activate billing, copy credentials or weaken permissions.

Record each real review's provider, input version/hashes, data scope, requested
and observed model/effort, output, exit and verdict. Reconciliation by Astra/Sol
does not turn Claude's REVISE into PASS or make a new version Claude-reviewed.
State that distinction in the handoff. A planning critique can be reconciled by
Astra into a revised specification without requiring Claude to PASS every revision;
resolve or surface material objections before coding. This is not a replacement
for the fresh default Claude review after implementation.

CLI reviewer/consent flags apply per invocation; the helper does not persist the
user's run-wide fallback choice or encode artifact/version/stage scope. Record
those decisions in run notes and carry the matching flags into later commands.
If the project contains material outside the approved scope, use prompt-only
snapshots or an isolated packet directory; the consent flag and tool restrictions
alone do not enforce a file-sharing boundary.

## Provider execution and boundaries

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
keep that provider pending and continue independent native work. The flags record
the caller's actual authorization; default Claude selection never sets them for
the user. An explicit `--reviewer codex` likewise asserts the user's fallback
choice, not an automatic recovery policy.

Provider metadata is stronger evidence than prose claims about identity.
Keep requested model/effort separate from observed fields; note provider
fallbacks or settings caps. An API result may not expose resolved effort.
