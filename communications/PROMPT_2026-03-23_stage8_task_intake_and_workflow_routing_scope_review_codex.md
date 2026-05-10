Audit the proposed Stage 8 scope memo against the live codebase and the larger roadmap.

Primary target:

- `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_scope.md`

Also consult:

- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
- `communications/PROOF_2026-03-23_stage7_aoi_source_to_composition_bridge.md`
- `communications/MEMO_2026-03-23_stage7_aoi_source_to_composition_bridge_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`
- `docs/MEMO_2026-02-19_orchestrator_vision.md`
- any recent communications/docs memos that materially bear on task intake, workflow routing, planner integration, or host contract

You must:

1. test whether the memo’s assumptions are actually supported by the current code
2. evaluate whether the memo fits the larger program objective rather than only the local AOI path
3. identify any places where the memo overstates how “ready” the current orchestrator/objective/routing substrate is
4. identify any hidden coupling to AOI/the-critic that the memo is underplaying
5. state explicitly if no relevant Perspective docs folder exists after checking

Prioritize inspection of:

- `src/orchestrator/planner.py`
- `src/orchestrator/adaptive_planner.py`
- `src/orchestrator/pipeline.py`
- `src/orchestrator/catalog.py`
- `src/orchestrator/schemas.py`
- `src/api/routes/orchestrator.py`
- `src/objectives/definitions/`
- `src/api/routes/presenter.py`
- `src/presenter/compose_from_intent.py`
- `src/presenter/composition_source_bridge.py`
- any the-critic code that matters to the host-contract claim

Output requirements:

- save your audit to:
  - `communications/REPORT_Codex_STAGE8_Task_Intake_And_Workflow_Routing_Scope_Audit_2026-03-23.md`
- begin with a verdict:
  - `Approve`
  - `Approve after revision`
  - `Do not approve`
- findings first
- keep summaries secondary
- be explicit about:
  - code seams
  - contract mismatches
  - missing proof requirements
  - stage-ordering mistakes if any

Do not modify code.
