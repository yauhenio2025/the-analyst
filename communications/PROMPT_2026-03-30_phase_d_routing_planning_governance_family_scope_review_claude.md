# Prompt: Claude Review Of Phase D Routing/Planning Governance Family Scope

Read and critique:

- `communications/MEMO_2026-03-30_phase_d_routing_planning_governance_family_scope.md`

Ground the review in the bigger picture and the current codebase.

At minimum, inspect:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-30_phase_d_aoi_standalone_governance_family_v1_completion.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- any recent review/completion memos in `communications/` that materially bear on Stage 15 / Phase D governance scope
- relevant code and tests around:
  - `src/evaluations/frozen_pack_harness.py`
  - `src/evaluations/frozen_pack_definitions.py`
  - `src/evaluations/gate_definitions.py`
  - `src/evaluations/governance_status.py`
  - `src/orchestrator/task_router.py`
  - `src/orchestrator/task_planner.py`
  - `tests/test_task_router.py`
  - `tests/test_task_planner.py`
  - `tests/test_frozen_governance_pack.py`
  - `tests/test_evaluation_governance_status.py`

Questions to answer:

1. Is this the right next Phase D slice, or is it drifting?
2. Is the memo honest about the distinction between Phase D governance progress and Phase E generality proof?
3. Are the codebase claims accurate?
4. Is the proposed evaluator-family expansion appropriately bounded?
5. Is there a smaller or cleaner next step that would better serve the program?

Output requirements:

- Write the output to:
  - `communications/REPORT_Claude_Phase_D_Routing_Planning_Governance_Family_Scope_Critique_2026-03-30.md`
- Start with a clear verdict:
  - `Approve`
  - `Approve with revisions`
  - `Reject`
- Prioritize concrete findings, risks, contradictions, and scope corrections
- Be explicit about what the memo gets right
- Keep the distinction between strategic disagreement and implementation/detail corrections clear
