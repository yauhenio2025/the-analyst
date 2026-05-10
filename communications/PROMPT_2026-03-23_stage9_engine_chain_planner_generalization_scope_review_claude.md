Review the proposed Stage 9 scope memo as a skeptical strategic reviewer.

Primary target:

- `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_scope.md`

Also consult:

- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_scope.md`
- `communications/PROOF_2026-03-23_stage8_task_intake_and_workflow_routing.md`
- `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_completion.md`
- `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
- `communications/PROOF_2026-03-23_stage7_aoi_source_to_composition_bridge.md`
- `communications/MEMO_2026-03-23_stage7_aoi_source_to_composition_bridge_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`
- `docs/MEMO_2026-02-19_orchestrator_vision.md`
- recent round/stage memos in `communications/` that are relevant to routing, planner generalization, composition handoff, or host-contract direction

Inspect the codebase claims against the actual code, especially:

- `src/orchestrator/task_router.py`
- `src/orchestrator/task_routing_schemas.py`
- `src/orchestrator/planner.py`
- `src/orchestrator/adaptive_planner.py`
- `src/orchestrator/pipeline.py`
- `src/orchestrator/catalog.py`
- `src/orchestrator/schemas.py`
- `src/orchestrator/pipeline_schemas.py`
- `src/api/routes/orchestrator.py`
- `src/objectives/definitions/`
- `src/presenter/composition_source_bridge.py`
- `src/presenter/compose_from_intent.py`
- relevant the-critic seams if they matter to the host-contract or downstream-shape argument

Your job:

1. test the robustness of the memo’s assumptions
2. examine the memo in light of the bigger-picture objective:
   - analyzer-v2 as the intelligence layer for dynamic bespoke analytical apps
3. scrutinize the memo’s claims against the current orchestrator/planner code
4. identify what is right
5. identify what is overstated, missing, wrongly ordered, or strategically risky
6. say explicitly if no relevant Perspective docs folder exists after you check

Output requirements:

- save your critique to:
  - `communications/REPORT_Claude_STAGE9_Engine_Chain_Planner_Generalization_Scope_Critique_2026-03-23.md`
- begin with a verdict:
  - `Approve`
  - `Approve after revision`
  - `Do not approve`
- focus on findings first, ordered by importance
- be concrete about:
  - code seams
  - memo assumptions
  - what must change before execution planning
- distinguish:
  - strategic issues
  - architectural/codebase issues
  - proof/evidence issues

Do not modify code.
