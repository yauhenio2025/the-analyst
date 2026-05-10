Review the proposed next Phase E scope memo:

- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_scope.md`

Your task:

1. test the robustness of the memo's assumptions
2. examine the memo against the bigger picture and overall program objectives
3. scrutinize the memo's claims against the actual codebase
4. read any relevant recent memos and proof artifacts in `communications/` that bear on this question
5. identify whether this is truly the next smallest honest Phase E step, or whether a different narrower/stronger step should come first

Important review constraints:

- do not treat the memo as authoritative just because it exists
- explicitly check whether `direct_sections` is truly the smallest honest standalone-harness lifecycle target on the proof-only line
- explicitly check whether `source_selection` lifecycle would silently require compose-session schema widening
- explicitly check whether keeping consumer identity fixed is the right isolation discipline now that plurality is complete
- explicitly check whether the memo overstates what a proof-only lifecycle direct-sections slice would prove
- explicitly check whether the already-complete March 28 bounded lifecycle proof makes this next slice too weak, or whether the standalone harness boundary makes it materially stronger
- explicitly check whether the harness must surface `session_id` explicitly rather than continuing to present `planning_decision_id` as the visible identity
- explicitly check whether reopen must pass `?consumer_key=transient-proof-harness` to avoid a truthful `409`

Files you should inspect at minimum:

- `communications/MEMO_2026-04-01_phase_e_transient_consumer_identity_plurality_v1_completion.md`
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_scope.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_implementation_completion.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_completion.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `src/presenter/schemas.py`
- `src/presenter/compose_session_store.py`
- `src/api/routes/presenter.py`
- `tests/test_compose_sessions.py`
- `src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/transient-proof-harness/src/App.tsx`
- `/home/evgeny/projects/transient-proof-harness/src/lib/transientClient.ts`
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_2026-04-01.json`
- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_live_closeout_2026-04-01.json`

Output requirements:

- write your review to:
  - `communications/REPORT_Claude_Phase_E_Proof_Only_Lifecycle_Direct_Sections_Scope_Critique_2026-04-01.md`
- start with a clear verdict:
  - `Approve`
  - `Approve with corrections`
  - `Reject`
- make the review concrete and code-backed
- distinguish clearly between:
  - strategic objections
  - implementation corrections
  - wording/documentary corrections
- if you think a different next step should come first, name it explicitly and explain why
