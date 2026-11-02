# Visual human review at every checkpoint

Apply this standard whenever the user must review, validate, approve, choose or
accept something in Workflow 1. It applies to native orchestration and CLI
handoffs, not just the first plan or the final scientific report. Do not create
extra approval pauses: use the standard at decisions already required by scope,
scientific method, provider boundaries or the host.

## Required review surface

Make the decision understandable before the reader opens technical detail.

- **Start with a summary:** status, decision needed now, recommendation and its
  practical consequence. Aim for 150-250 words of front-page prose for a
  substantive checkpoint. Put the most important point first.
- **Highlight selectively:** bold the decision, key scope boundary and up to
  three facts, assumptions or unresolved issues that could change the choice.
  Use short headings, bullets, whitespace and compact comparison tables.
  Explain specialist terms at first use; do not lead with internal phase IDs.
- **Include a useful visual:** every substantive review/approval document needs
  at least one rendered diagram, schematic, comparison graphic or evidence-based
  plot. Choose visuals that answer a real review question. Text alone, a list of
  links or an unrendered diagram code block does not meet this standard.
- **Use progressive detail:** give one clear starting document. For a large
  pipeline use an illustrated overview, normally 2-4 short pages, with a concise
  opening decision page. Put equations, full specifications, provenance, hashes,
  test logs and long review exchanges in linked technical appendices or clearly
  labeled expandable sections. Keep all material assumptions and limitations
  visible in the brief; brevity must not hide them.
- **Make the response concrete:** identify the exact version and scope, then
  offer a natural-language reply such as "Approve specification <version> and
  proceed" and "Request changes: ...". For final acceptance ask the user to name
  supported uses and unresolved limitations. Users reply in chat; the coordinator
  records the decision. Never ask users to operate state commands.
- **Show it:** include the short summary directly in chat and embed a relevant
  figure when possible, then link or open the illustrated document. A bare file
  link is not a handoff. If the interface cannot render diagrams, export a
  standalone image/PDF rather than relying on diagram source.

A single missing value or native host permission dialog can use a few highlighted
lines instead of a full booklet. Where the host dialog cannot contain figures,
put any substantive choice and visual in the companion brief. Do not bury a
simple question in a decorative report or bypass the host's required UI.

## Choose the visual for the decision

| Human checkpoint | Lead with | Useful visual and required context |
| --- | --- | --- |
| Specification / plan approval | What will be built, outputs and success criteria | Pipeline graph plus system schematic or milestone map; distinguish current scope from later work and unknown experimental inputs. |
| A method or scope revision | What changed and how it changes the decision | Before/after comparison or marked dependency diagram; remaining objections stay visible. |
| Provider / data / cost authorization or runtime fallback | Actual options, exact sharing/action scope and consequence | Small data-flow or choice diagram, with included/excluded artifacts, provider and cost boundary; missing consent is not provider failure. |
| Resource, hardware, publication or deployment decision | Concrete reviewed action and its impact | Action/impact diagram or options table with evidence; preserve the relevant authorization boundary. |
| A blocker or methodological dispute requiring input | What is unresolved and the smallest decision needed | Dependency/issue map or comparison; separate observation, interpretation and missing evidence. |
| Validation review / final scientific acceptance | What actually passed, findings, uncertainty and supported uses | Actual result plots with provenance when quantitative results exist, plus a gate/status diagram; separate software verification, physical validation and human acceptance. |

Match the visual to available evidence. Before computation, use clearly labeled
**conceptual schematics / proposed outputs**, not invented curves, mock measured
images, progress percentages or estimated performance presented as results.
For quantitative graphs label units, uncertainty, sample size, source and whether
data are synthetic, simulated or measured. Preserve negative and null results.
Do not imply chemical identity, physical accuracy or calibration from an
illustration. Use status text/symbols as well as color.

Use Mermaid for compact structure when the actual review surface renders it;
export SVG/PNG if needed. Use standard plotting tools for scientific result
figures, save source data and captions with the figure, and inspect the rendered
artifact. Use a self-contained local HTML or PDF review when it improves reading;
do not upload restricted material or require an online renderer to view it.

## Evidence, versions and presentation changes

Name what is **proposed**, **documented**, **computed/tested**, **measured** or
**unresolved**. Technical PASS is not experimental validation or human scientific
acceptance. Limited-use acceptance is valid only where the approved criteria
already permit that scope; it cannot waive a failed required criterion. Narrowing
scientific requirements is a specification revision, not a presentation edit.
Report the provider's actual reviewed version and verdict; a later
native reconciliation is not a new Claude review. Mark missing inputs explicitly.

For a presentation-only remake, preserve the frozen specification/hash and
existing valid approval. Version the review surface separately, link it to the
exact frozen specification and check that the summary did not change scientific
scope, estimand, method or acceptance criteria. Do not re-record plan/critique or
re-freeze just to restyle documents. If the science changes, use a revised
specification and the normal approval path. A visual summary never replaces the
authoritative requirements or grants approval itself.

## Before handing it to the user

Inspect the actual rendered document, including every exported PDF page and
figure: legible labels at normal reading size, no overlap/clipping, readable
contrast, captions/status, working links and a clear next action. Verify the
diagram agrees with the specification and that axes/units match source data.
Check a narrow viewport for HTML; verify the primary interaction if interactive.
If rendering is unavailable, state that limitation and provide the clearest
accessible fallback; do not claim visual QA that was not performed.

The reader should be able to answer, from the opening view: **Where are we?
What am I deciding? What will I get? What remains uncertain? How do I respond?**
If those answers require reading the entire specification, remake the handoff.

## Avoid repeated permission requests

| Situation | Action |
| --- | --- |
| Routine computer action inside approved scope | Proceed and verify. |
| Tests, bounded repairs or review already authorized | Continue; report meaningful progress. |
| Existing approval matches the unchanged frozen specification | Reuse it, including after a presentation-only remake. |
| Missing scientific input | Inspect sources, then bundle only essential questions. |
| New method, material scope/cost/data exposure or consequential action | Prepare the concrete visual choice and ask once. |
| Host permission or runtime blocks execution | Explain the exact boundary and smallest required change; continue independent work. |

Do not substitute scientific approval for OS permission, bypass host rejection,
or change security settings to reduce prompts. If automatic approval review
rejects an action and no compliant alternative works, identify the action, state
the reviewer's reason and explain the remaining required approval.
