Audit the proposed Stage 10 scope memo against the live codebase and the larger roadmap.

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
- any recent communications/docs memos that materially bear on source-backed composition, result manifests, runtime composition modes, or host-contract direction

You must:

1. test whether the memo’s assumptions are actually supported by the current code
2. evaluate whether the memo fits the larger program objective rather than only the local AOI path
3. identify any places where the memo overstates how ready the current result/presenter substrate already is
4. identify any hidden coupling to AOI/the-critic that the memo is underplaying
5. identify any stage-ordering mistake or false symmetry in the proposed Stage 10 slice
6. state explicitly if no relevant Perspective docs folder exists after checking

Prioritize inspection of:

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
- any the-critic code that matters to the host-contract or downstream-handoff claim

Be explicit about these questions:

- is the proposed Stage 10 seam really “workflow-owned source-backed substrate,” or is the memo just renaming a mixture of AOI bridge code and existing runtime composition modes?
- does the repo actually support genealogy as a second workflow source-backed slice, or only genealogy result restore with runtime view recomposition?
- is the suggestion to preserve workflow-specific selector unions defensible, or should the stage force a single selector contract?
- does the memo correctly avoid importing Stage 11 page-planning and Stage 13 host-contract work too early?

Output requirements:

- save your audit to:
  - `communications/REPORT_Codex_STAGE10_Cross_Workflow_Source_Backed_Substrate_Scope_Audit_2026-03-23.md`
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
  - any place where the memo is calling reusable substrate what is still workflow-specific plumbing

Do not modify code.
