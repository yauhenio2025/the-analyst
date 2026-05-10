Review the proposed Stage 12 scope memo as a skeptical strategic reviewer.

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
- any recent memos in `communications/` or `docs/` from the past 48 hours that materially bear on renderer contracts, presentation restore, transient compose, readiness, thin-host direction, or stage ordering

Inspect the codebase claims against the live code, especially:

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
- `src/consumers/definitions/`
- `tests/test_aoi_contract.py`
- `tests/test_analysis_product_contract.py`
- `tests/test_presentation_api.py`
- `tests/test_compose_from_intent.py`
- `tests/test_manifest_trace.py`
- any other tests or docs that materially bear on renderer-law strength or sub-renderer validation

Your job:

1. test the robustness of the memo’s assumptions
2. examine the memo in light of the bigger-picture objective:
   - analyzer-v2 as the intelligence layer for dynamic bespoke analytical apps
3. scrutinize the memo’s claims against the current renderer/presenter/results code
4. identify what is right
5. identify what is overstated, missing, wrongly ordered, or strategically risky
6. say explicitly if you find no additional relevant docs beyond the usual `docs/` and `communications/` materials

Be especially skeptical about:

- whether Stage 12 really should come before Stage 13, or whether the memo is underestimating the host-contract gap
- whether “renderer law” is being defined concretely enough, rather than as a slogan
- whether replacing `composition_mode` allowlisting with a richer served-contract policy is the right architectural move
- whether the memo now specifies that served-policy layer concretely enough:
  - function shape
  - decision values
  - decision matrix
- whether the proposed scope is honest about the difference between:
  - route-time warn-mode validation
  - final fail-closed served validation
  - design-time view-contract validation
  - consumer support metadata
- whether the genealogy `shadow -> strict` cutover strategy is concrete and realistic enough given the existing normalization-heavy genealogy path
- whether sub-renderer law is specified tightly enough to be implementable rather than just gesturing at nested configs
- whether the memo now cleanly distinguishes:
  - accordion or nested-sections serve-time sub-renderer law
  - `tab` child-container law
- whether AOI plus genealogy is the right bounded proof matrix
- whether the proof bar is strong enough to show real cross-workflow renderer-law progress rather than another AOI-heavy proof
- whether the fail-closed proof requirement is now genuinely non-AOI
- whether the memo is now keeping Stage 11 grouping/semantic-matcher work and Stage 13 host-contract work properly out of scope

Output requirements:

- save your critique to:
  - `communications/REPORT_Claude_STAGE12_Cross_Workflow_Renderer_Law_Generalization_Scope_Critique_2026-03-24.md`
- begin with a verdict:
  - `Approve`
  - `Approve after revision`
  - `Do not approve`
- focus on findings first, ordered by importance
- be concrete about:
  - code seams
  - architectural risks
  - stage-ordering issues
  - proof/evidence requirements
  - any claim that reads broader than the actual current renderer substrate

Do not modify code.
