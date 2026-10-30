# Runtime effort selection

| Role | Model | LOWER | HIGHER |
|---|---|---|---|
| Leader / interpretation | gpt-6-astra | high | xhigh |
| Implementer | gpt-6.1-sol | high | xhigh |
| Native fallback critic/reviewer | gpt-6.1-sol | high | xhigh |
| Figure QA | gpt-6.1-terra | medium | high |
| External critic/reviewer | claude-opus-5-5 | high | max |
| Literature researcher | Gemini Deep Research | deep-research-preview-04-2026 | deep-research-max-preview-04-2026 |

These are requested runtime parameters, not promises about hidden reasoning or
scientific quality. Record provider-returned model identity when available;
requested identity and an agent's self-description alone are not verification.

## CLI

From the target project, launch `codex --profile workflow1-lower` or
`codex --profile workflow1-higher`. Codex 0.165.0 reads the corresponding
`~/.codex/<profile>.config.toml` overlay. These are not `[profiles.*]` tables in
the base config. The base file remains unchanged. Check `/model` and the launch
header. Project settings and explicit CLI flags can override profile values.

## VS Code / existing chats

Choose GPT-6 Astra and High or Extra High in the Codex model/effort controls,
then invoke `$workflow-1` with the selected mode. A CLI profile does not change
an already-open extension conversation. If the UI cannot select the required
setting, start a new CLI session with the profile, or disclose the actual
available setting and obtain a deliberate choice rather than silently claiming
an exact match. Refresh/restart the extension if the skill is not listed.

For native specialists use `w1_implementer_lower/higher`,
`w1_critic_lower/higher`, `w1_reviewer_lower/higher`, and
`w1_visual_lower/higher`. Their TOMLs pin both model and effort, so switching
the requested workflow mode selects different roles without relying on the
parent's effort. Do not reuse a lower-mode child as a higher-mode child.
Spawn fresh contexts for independent reviews and wait for real outputs.

The legacy unsuffixed `w1_critic`, `w1_reviewer`, `w1_implementer` roles from the
earlier installer may still exist. Prefer the explicit mode-specific roles.

When a run changes mode, update requested mode and record which settings were
actually verified. A new stage/specification is appropriate if its scope changes.
Never relabel earlier evidence as if it used the new mode.

Sources (verified 2026-10-29):
- https://learn.chatgpt.com/docs/config-file/config-advanced
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://code.claude.com/docs/en/model-config
- https://ai.google.dev/gemini-api/docs/deep-research
