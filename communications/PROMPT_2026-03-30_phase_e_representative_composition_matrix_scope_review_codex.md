# Prompt: Codex Audit Of Phase E Representative Composition Matrix Scope

Audit this scope memo against the live repo and the broader program direction:

- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_scope.md`

Also read enough surrounding material to test whether the memo is strategically honest and codebase-accurate:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_v1_completion.md`
- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_scope.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- relevant recent completion/review memos in `communications/` that materially bear on the Phase D -> Phase E pivot

Inspect the codebase directly, especially:

- `src/api/routes/presenter.py`
- `src/presenter/compose_from_intent.py`
- `src/presenter/schemas.py`
- `src/orchestrator/task_router.py`
- `src/orchestrator/task_planner.py`
- `src/api/routes/orchestrator.py`
- `tests/test_compose_from_intent.py`
- `tests/test_task_router.py`
- `tests/test_task_planner.py`
- `tests/test_run_contract.py`

Inspect relevant live artifacts or persisted examples if needed to test the memo’s claims about current supported handoff families.

Audit questions:

1. Is a representative composition matrix the right first Phase E slice after Phase D exit?
2. Does the memo accurately describe the currently live compose surfaces and their differences?
3. Is the proposed three-case matrix the smallest honest proof of generality available right now?
4. Does the memo stay honest about proving representative composition law rather than arbitrary engine/pass composition?
5. Is keeping the consumer fixed to `the-critic` the right default for isolating the Phase E question?
6. Is there a smaller cleaner first Phase E step that would still materially advance the analyzer-v2-as-brain proof?

If useful, run non-destructive verification commands or focused tests.

Output requirements:

- Write the audit to:
  - `communications/REPORT_Codex_Phase_E_Representative_Composition_Matrix_Scope_Audit_2026-03-30.md`
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
