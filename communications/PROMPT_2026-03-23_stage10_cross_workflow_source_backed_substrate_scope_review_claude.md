Review the proposed Stage 10 scope memo as a skeptical strategic reviewer.

Primary target:

- `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md`

Also consult:

- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_scope.md`
- `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md`
- `communications/MEMO_2026-03-23_stage9_aoi_handoff_profile_feasibility_hardening_completion.md`
- `communications/PROOF_2026-03-23_stage9_engine_chain_planner_generalization.md`
- `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_completion.md`
- `communications/MEMO_2026-03-23_stage7_aoi_source_to_composition_bridge_completion.md`
- `communications/MEMO_2026-03-18_snapshot_after_stage9.md`
- `communications/MEMO_2026-03-23_round14_aoi_transient_hot_path_launch_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`
- `docs/MEMO_2026-02-19_orchestrator_vision.md`
- recent communications/docs memos that materially bear on source-backed composition, result manifests, composition modes, or thin-host direction

Inspect the codebase claims against the actual code, especially:

- `src/presenter/composition_source_bridge.py`
- `src/presenter/compose_from_intent.py`
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/presentation_api.py`
- `src/presenter/schemas.py`
- `src/analysis_products/store.py`
- `src/analysis_products/result_contract.py`
- `src/api/routes/results.py`
- `src/api/routes/presenter.py`
- `src/orchestrator/task_planner.py`
- `src/orchestrator/task_router.py`
- `src/objectives/definitions/`
- `src/workflows/definitions/`
- any the-critic seams that matter to the host-contract or downstream-shape argument

Your job:

1. test the robustness of the memo’s assumptions
2. examine the memo in light of the bigger-picture objective:
   - analyzer-v2 as the intelligence layer for dynamic bespoke analytical apps
3. scrutinize the memo’s claims against the current presenter/result/orchestrator code
4. identify what is right
5. identify what is overstated, missing, wrongly ordered, or strategically risky
6. say explicitly if no relevant Perspective docs folder exists after you check

Be especially skeptical about:

- whether genealogy is really the right second workflow for the bounded Stage 10 slice
- whether existing `composition_mode` support is being overstated as if it were already a generic source-backed substrate
- whether the proposed adapter layer is genuinely the next missing seam or is importing Stage 11/13 work too early
- whether the memo is underplaying AOI/the-critic coupling
- whether normalizing output shape while preserving workflow-specific selector unions is the right call

Output requirements:

- save your critique to:
  - `communications/REPORT_Claude_STAGE10_Cross_Workflow_Source_Backed_Substrate_Scope_Critique_2026-03-23.md`
- begin with a verdict:
  - `Approve`
  - `Approve after revision`
  - `Do not approve`
- focus on findings first, ordered by importance
- be concrete about:
  - code seams
  - memo assumptions
  - stage-ordering risks
  - proof/evidence requirements
- distinguish:
  - strategic issues
  - architectural/codebase issues
  - proof/evidence issues

Do not modify code.
