# Prompt: Claude Review Of Phase E Representative Composition Matrix Scope

Read and critique:

- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_scope.md`

Ground the review in the bigger picture and the current codebase.

At minimum, inspect:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_v1_completion.md`
- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_scope.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- any recent completion or review memos in `communications/` that materially bear on the shift from Phase D to Phase E
- relevant live proof artifacts and persisted snapshots if they matter

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

Questions to answer:

1. Is this the right first Phase E slice, or is it still drifting inside Phase D habits?
2. Is the memo honest about what this matrix would and would not prove?
3. Are the proposed three composition families the right representative matrix over the live substrate?
4. Is keeping `consumer_key=the-critic` fixed the right isolation choice for this first Phase E move?
5. Is the memo accurate about the codebase and current route/contract reality?
6. Is there a smaller or cleaner first Phase E step that would better serve the analyzer-v2-as-brain objective?

Output requirements:

- Write the output to:
  - `communications/REPORT_Claude_Phase_E_Representative_Composition_Matrix_Scope_Critique_2026-03-30.md`
- Start with a clear verdict:
  - `Approve`
  - `Approve with revisions`
  - `Reject`
- Prioritize concrete findings, strategic risks, contradictions, and scope corrections
- Be explicit about what the memo gets right
- Keep the distinction between strategic disagreement and implementation/detail correction clear
