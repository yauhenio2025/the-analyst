Audit this scope memo against the real code and recent strategy trail:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md`

This is a docs-only audit. Do not change application code.

What to do:

1. Audit the memo’s assumptions against the live codebase in:
   - `/home/evgeny/projects/analyzer-v2`
   - `/home/evgeny/projects/the-critic`
   - `/home/evgeny/projects/aoi-canary` where sequencing comparisons are relevant
2. Check whether the memo accurately reflects:
   - the actual Stage 3/4 AOI cutover now landed
   - the real remaining gap after Milestone A
   - the current planner-primary AOI seam in the critic
   - the current analyzer planning/compose contract shape
3. Re-read the relevant recent memos in `communications/` and `docs/`, especially:
   - the canonical roadmap memo
   - the draft next-platformization roadmap memo
   - the Stage 3/4/5 AOI exemplar scope memo
   - the Stage 3/4 AOI exemplar cutover completion memo
   - the Stage 13 Tier A second-consumer completion memo
   - recent AOI, Stage 5, Stage 8/9, or Stage 13 memos if they materially affect sequencing honesty
4. Evaluate whether this is the right next step, or whether:
   - the AOI exemplar still needs more structural implementation before an exit gate is meaningful
   - the scope is missing required evidence, thresholds, or negative cases
   - the Stage 2 closure decision is under-specified
   - the exit gate is over- or under-scoped relative to the bigger platform objective

Key questions to answer:

- Is the memo honest about what remains after the Stage 3/4 cutover?
- Is Stage 5 really the immediate next step, or is there still an unclosed Milestone A structural gap?
- Does the fixed eval pack reflect the real current seam, including:
  - the locked non-profile case
  - a real `aoi_selection_blocked` selector-path case
- Does the memo now handle the readiness-discovery gap for the locked non-profile case honestly enough?
- Is the memo specific enough about saving planning provenance and launch artifacts?
- Does the current code actually support the audit surface the memo expects:
  - selected/rejected sources
  - planner rationale
  - blocked reason codes
  - blocked-path provenance
  - compose request artifacts
- Is the artifact-capture method concrete enough given that the current implementation does not auto-persist audit packs?
- Is the memo drawing the right boundary between:
  - AOI exemplar closure
  - and later transient-substrate generalization
- Is the Stage 2 closure decision framed correctly as explicit and evidence-driven rather than automatic?
- Are the Stage 2 non-closure conditions strong and concrete enough?
- Are the remaining host residuals and refresh/deep-link limitations scoped honestly enough?
- Are fixture-backed, execution-backed, and user-initiated case tiers defined well enough, and is the minimum required tier for Stage 2 closure honest?
- Is the rubric timing/threshold shape concrete enough to avoid post-hoc self-certification?
- Is the latency/responsiveness breakdown concrete enough for later audit?
- Is any important deliverable, hidden prerequisite, or likely failure mode missing?

Please save your audit to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_STAGE5_AOI_Exemplar_Exit_Gate_Scope_Audit_2026-03-24.md`

Preferred output shape:

- overall verdict
- concrete findings with code/memo references
- scope/sequence assessment
- missing assumptions or hidden prerequisites
- recommended revisions before implementation
