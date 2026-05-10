# Prompt: Codex Audit Of Phase D Routing/Planning Governance Family Scope

Audit this scope memo against the live repo and the broader program direction:

- `communications/MEMO_2026-03-30_phase_d_routing_planning_governance_family_scope.md`

Also read enough surrounding material to test whether the memo is strategically honest and codebase-accurate:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-30_phase_d_aoi_standalone_governance_family_v1_completion.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- relevant recent Phase D / Stage 15 review and completion memos in `communications/`

Inspect the codebase directly, especially:

- `src/evaluations/frozen_pack_harness.py`
- `src/evaluations/frozen_pack_definitions.py`
- `src/evaluations/gate_definitions.py`
- `src/evaluations/governance_status.py`
- `src/orchestrator/task_router.py`
- `src/orchestrator/task_planner.py`
- `src/orchestrator/planning_decision_store.py`
- `tests/test_task_router.py`
- `tests/test_task_planner.py`
- `tests/test_frozen_governance_pack.py`
- `tests/test_evaluation_governance_status.py`
- `tests/test_evaluation_governance_status_routes.py`

Audit questions:

1. Is routing/planning governance the right next bounded Phase D step after standalone AOI governance?
2. Does the memo accurately describe the current substrate and its limits?
3. Are the proposed Stage 8/9 proof surfaces and case choices viable for a bounded new evaluator family?
4. Does the memo stay honest about not being Phase E?
5. Are there missing scope constraints, cleaner alternatives, or hidden implementation risks?

If useful, run non-destructive verification commands or focused tests.

Output requirements:

- Write the audit to:
  - `communications/REPORT_Codex_Phase_D_Routing_Planning_Governance_Family_Scope_Audit_2026-03-30.md`
- Give a bottom-line verdict:
  - `Approve`
  - `Approve with corrections`
  - `Reject`
- Summarize the strongest confirmed claims
- Call out concrete scope corrections or risks with file references where relevant
- Distinguish clearly between:
  - strategic disagreement
  - scope correction
  - implementation caution
