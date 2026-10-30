# Validation and run records

Each run belongs to its project, under `.workflow1/runs/<id>/`. The helper creates
objective.md, plan.md, critique.md, specification.md, implementation.md,
validation.md, review.md, stage-report.md, acceptance.md and status.json. Empty/not-yet-run artifacts are
not evidence of completion. Versioned artifacts and JSON events preserve history.

Record native outputs using `record --phase ... --file ...`, giving requested
model/effort and observed identity only where actually verified. `--source native`
means an actual native agent supplied it; `manual` is human/coordinator material.
Keep test logs and scientific products in the project, not the shared skill.
Native independent review uses `DECISION: PASS|REVISE|REPLAN|BLOCKED` in review.md;
validation.md uses `VERDICT: PASS|REVISE|BLOCKED` plus real TEST_COMMAND and
TEST_EXIT_CODE lines. Those reports do not replace the deterministic `test` helper.
Use `test --run DIR --test 'COMMAND' --artifact CODE --artifact TEST` to capture
the actual exit, hashed output and source/input manifest. Enumerate every relevant
file; no implicit data-tree scan occurs. Source changes invalidate that evidence.

Freeze the specification before implementation. Approval is bound to its content
hash, and edits invalidate it. User scientific acceptance is a separate explicit
decision after validation. Never use an approval command to approve on behalf of
the user without authorization. See `--help` for each state operation.

Validation must cover relevant numerical invariants, units, physical assumptions,
uncertainty/error propagation, input provenance, reproducibility and edge cases.
Tests should challenge plausible mistakes rather than duplicate implementation.
Record commands, exit codes and artifact paths. Real scientific data is not needed
for installation tests. Use a synthetic disk/footprint example with known area
ratios and translation/rotation invariants; distinguish coverage from uniformity.

Feedback routing:
- REVISE plus failed deterministic checks: repair implementation, at most twice.
- REPLAN: stop implementation and revisit methodology; a new frozen spec needs
  renewed implementation authorization.
- Unknown verdict or missing evidence: unresolved, not PASS.
- PASS requires actual tests with exit 0 and an adequate independent review.
- PASS ends at awaiting human scientific acceptance, not automatic acceptance.

Test provider adapters offline with clearly labeled stubs. Stub PASS results do
not verify live account access, models, APIs, or scientific results. For live
tests retain CLI/session model and effort metadata, actual review outputs and
deterministic test logs. Provider/model failures remain pending or failed.
