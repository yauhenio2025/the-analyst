Audit the proposed Stage 12 scope memo against the live codebase and the larger roadmap.

Primary target:

- `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`

Also consult:

- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_stage11_rich_semantic_page_planning_completion.md`
- `communications/PROOF_2026-03-24_stage11_rich_semantic_page_planning.md`
- `communications/MEMO_2026-03-23_stage11_rich_semantic_page_planning_scope.md`
- `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md`
- `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_completion.md`
- `communications/PROOF_2026-03-23_stage10_cross_workflow_source_backed_substrate.md`
- `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- any recent memos in `communications/` or `docs/` from the past 48 hours that materially bear on renderer-law strength, presentation restore, transient compose, readiness, or thin-host direction

You must:

1. test whether the memo’s assumptions are actually supported by the current code
2. evaluate whether the memo fits the larger program objective rather than only the local AOI path
3. identify any places where the memo overstates how ready the current renderer/presenter substrate already is
4. identify any hidden contract mismatch between transient compose, job-backed presentation, and consumer support law
5. identify any stage-ordering mistake or false symmetry in the proposed Stage 12 slice
6. say explicitly if you find no additional relevant docs beyond the usual `docs/` and `communications/` materials

Prioritize inspection of:

- `src/presenter/renderer_contract_enforcement.py`
- `src/presenter/manifest_builder.py`
- `src/presenter/presentation_api.py`
- `src/presenter/compose_from_intent.py`
- `src/presenter/view_contract_validator.py`
- `src/presenter/runtime_override_validator.py`
- `src/presenter/composition_source_bridge.py`
- `src/presenter/bounded_dynamic_composition.py`
- `src/analysis_products/result_contract.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/api/routes/results.py`
- `src/api/routes/presenter.py`
- `src/renderers/validator.py`
- `src/renderers/definitions/`
- `src/renderers/definitions/tab.json`
- `src/renderers/schemas.py`
- `src/consumers/definitions/the-critic.json`
- `src/consumers/definitions/analyzer-mgmt.json`
- `tests/test_aoi_contract.py`
- `tests/test_analysis_product_contract.py`
- `tests/test_presentation_api.py`
- `tests/test_compose_from_intent.py`
- `tests/test_manifest_trace.py`
- any other files you judge materially necessary to test the memo’s claims

Be explicit about these questions:

- is Stage 12 really the next missing seam, or is the memo underplaying the remaining Stage 13 host-contract work
- does the codebase actually support a richer served-contract policy beyond `composition_mode`, or would the memo need a more incremental shape
- is the memo now concrete enough about that served-policy layer:
  - function signature or model shape
  - `strict | shadow | warn` cutover states
  - workflow/route decision matrix
- is the proposed sub-renderer law concrete enough, given the current split between:
  - view-contract validation
  - runtime override cleaning
  - final payload validation
- does the genealogy `shadow -> strict` cutover match the normalization-heavy reality in `presentation_api.py`, or is it still understating breakage risk
- does the memo now distinguish correctly between:
  - accordion or nested-sections serve-time sub-renderer law
  - `tab` child-container law
- does the repo already have enough cross-workflow truth to justify AOI plus genealogy as the Stage 12 proof matrix
- is the memo keeping Stage 11 surface-planning work and Stage 13 host work properly out of scope
- is the proof bar strong enough to distinguish real fail-closed renderer law from another saved-JSON success case
- does the fail-closed proof requirement now force a non-AOI served-route rejection case

Output requirements:

- save your audit to:
  - `communications/REPORT_Codex_STAGE12_Cross_Workflow_Renderer_Law_Generalization_Scope_Audit_2026-03-24.md`
- begin with a verdict:
  - `Approve`
  - `Approve after revision`
  - `Do not approve`
- findings first
- keep summaries secondary
- be explicit about:
  - code seams
  - contract mismatches
  - hidden assumptions
  - proof requirements
  - any place where the memo is calling renderer-law substrate universal when it is still only partial

Do not modify code.
