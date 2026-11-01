---
name: workflow-1
description: "Use Workflow 1 for multi-agent scientific planning, implementation, independent validation, and human scientific acceptance. Recognizes lower/higher efforts and persists the selected mode for follow-ups in the same workflow."
---

# Multi-Agent Workflow 1

Use this skill when the user requests Workflow 1. The shared repository folder
is `shared-workflow-1`; the invocation name is `$workflow-1` on every device.
Local paths and provider credentials remain device-specific.
Read [effort-levels](references/effort-levels.md) before selecting agents and
[agents](references/agents.md) before external provider calls.

## Start or resume

- "Use Workflow 1" starts LOWER unless resuming a run with a saved mode.
  "Use Workflow 1 with lower/higher efforts" selects that mode; "Use lower/higher
  efforts" changes the active workflow's requested mode. Keep it for follow-ups
  until changed, not for unrelated tasks.
- Verify the coordinator's **actual** model and reasoning effort from runtime
  metadata or UI. Astra needs high (LOWER) or xhigh (HIGHER). If mismatched or
  unknown, explain the model/profile switch; never claim words changed runtime.
  Mode-specific specialist roles pin their own efforts.
- Use native Codex orchestration from the current chat by default. The Python
  helper records state and optionally coordinates external CLI/API processes;
  it is not required to spawn native subagents.
- On a different device, read [platform setup](references/platforms.md) and run
  `scripts/orchestrate.py doctor` with that device's Python interpreter. Resolve
  local commands/settings before external calls. Never copy another device's
  absolute paths, credentials, environments or run records into the shared skill.
- For an actionable run, create or resume `<project>/.workflow1/runs/<id>/` using
  `scripts/orchestrate.py init/status`. Store state outside the skills checkout.
  Record objective, plans, critique, frozen specification, implementation,
  validation, acceptance and status. Preserve older versions when revising.
  Discussion-only requests need no files. PLAN ONLY authorizes no implementation.
- Preserve requested settings separately from observed model/effort metadata.
  Record real participants, input/output paths, commands and exits, objections,
  uncertainties, decisions, and next action. Mark unverified settings honestly.

## Computer actions and human decisions

- Carry forward the user's authorization within its original scope. Proceed with
  routine reads, searches, navigation, reversible local edits, tests and bounded
  repairs without asking permission for each action. Prefer purpose-built tools
  or APIs; use computer UI actions when needed, under the same authorization.
- Check the actual project folder and writable roots early. Use the authorized
  workspace and established command approvals to avoid repeated escalations.
  A skill cannot expand filesystem/network permissions or disable host approval
  review. Use the host's escalation mechanism when needed; do not ask the same
  permission again in chat before submitting that request.
- Batch related missing inputs or consequential decisions into one concise
  request after completing independent preparation. Reuse authorized provider
  and data scopes; ask again only for a material change in scope, cost, exposure
  or risk, or where the host requires it. Login alone is not authorization.
- Normally the scientific decisions are approval of the concrete specification
  and acceptance of the validated results. Once implementation is approved,
  continue through tests, authorized independent review and up to two repair
  rounds. A methodological change returns to planning. Honor explicit user
  instructions about approval; never infer approval from silence.
- Before any human input/approval request or scientific handoff, read
  [human review](references/human-review.md). Present a short, readable decision
  brief in chat, link the full evidence and give an exact reply the user can send.
  Identify whether the pause comes from a scientific decision, missing input,
  host permission or runtime selection; cite the specific requirement when a
  rule causes the pause. Do not make the user interpret raw state JSON.

## Four stages

1. **Plan — Astra.** Define objective, assumptions, evidence, dimensional and
   statistical checks, deliverables and measurable acceptance criteria. Seek
   independent criticism, preferably before presenting a preferred conclusion.
   Claude Opus is the external critic when available and authorized. Otherwise
   disclose the native Sol fallback. Gemini literature research is optional and
   needs explicit cost/data authorization. Reconcile material objections with
   evidence or tests, then freeze a versioned specification. Agent agreement
   is not evidence. Resolve or surface methodological objections before coding.
   Present the specification's decision brief; record the user's authorization
   for that frozen version before implementation, reusing an existing valid
   authorization instead of asking again.
2. **Implement — Sol.** Delegate bounded work to `w1_implementer_lower` or
   `w1_implementer_higher`. Assign file ownership, remind agents they share the
   workspace, and wait for results. Use `w1_visual_lower/higher` for accessible
   plots/images when useful. Preserve inputs, provenance, and reproducibility.
   Run preliminary tests. Never let agents concurrently edit the same files.
3. **Validate — tests plus independent review.** Read actual code, outputs and
   test evidence. Prefer a fresh Claude review if authorized; otherwise disclose
   `w1_reviewer_lower/higher` as OpenAI fallback. Technical failure returns to
   implementation, invalid assumptions to planning, insufficient evidence to an
   unresolved status. Preserve valid surprising/null/negative results. Limit
   repairs to two rounds and surface unresolved methodological disputes.
4. **Scientific acceptance — Astra, then user.** Separate verified computation
   from interpretation, uncertainty and alternatives. Report concise evidence,
   limitations and open objections using the human review brief. Technical PASS
   is not human scientific acceptance. Record the user's decision and rationale;
   rejection returns to the appropriate earlier stage. Never manufacture approval.

Use [validation](references/validation.md) for evidence and state operations,
and [README](README.md) for installation and executable coordinator examples.

## Boundaries

- Preserve raw measurements, null/negative findings and validated results.
- Do not autonomously operate beamline/instrument hardware or execute trades.
- Ask for authorization for consequential experiments, external sharing of
  restricted/unpublished data, publishing or deployment. Existing explicit
  authorization remains valid within its scope.
- A provider login does not authorize sending arbitrary project content.
  Use only approved public/synthetic artifacts for external calls. Record their
  scope. Do not send credentials or raw confidential data to review agents.
- Runtime logs, run outputs, environments, credentials and backups stay outside
  the skills repository. Never commit them.
- LumaCam: reduction reconstructs raw detector data; processing corrects images;
  analysis/visualization measures processed products. A request for analysis
  does not authorize rerunning reduction or correction.
