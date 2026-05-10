Review the proposed next Phase E scope memo:

- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_scope.md`

Your task:

1. test the robustness of the memo's assumptions
2. examine the memo against the bigger picture and overall program objectives
3. scrutinize the memo's claims against the actual codebase
4. read any relevant recent memos and proof artifacts in `communications/` that bear on this question
5. identify whether this is truly the next smallest honest Phase E step, or whether a different narrower/stronger step should come first

Important review constraints:

- do not treat the memo as authoritative just because it exists
- explicitly check whether AOI `source_selection` is now the next smallest honest lifecycle target after standalone-harness `direct_sections` lifecycle closed
- explicitly check whether the current public save seam still only persists `ComposeFromIntentRequest`
- explicitly check whether `compose_from_selection()` already lowers into an internal `ComposeFromIntentRequest`
- explicitly check whether the current public `compose-from-selection` response truth does or does not expose the exact lowered `prose_sections`
- explicitly check whether adding one optional `persistable_intent_request` field to `ComposeFromIntentResponse` is in fact the smallest honest concrete mechanism
- explicitly check whether the memo is right to prefer analyzer-owned lowered-request persistence truth over harness-local reconstruction
- explicitly check whether the existing analyzer lowering fetch is direct-sections-only and therefore not a current AOI `source_selection` escape hatch
- explicitly check whether a bounded response-side lowered-request field is smaller/honester than a generic save-schema union
- explicitly check whether a tiny dedicated analyzer-owned save bridge would actually be smaller or stronger than the response-field approach
- explicitly check whether keeping consumer identity fixed at `transient-proof-harness` is the right isolation discipline now that proof-only plurality and direct-sections lifecycle are both complete
- explicitly check whether `source_profile` should remain out of scope for this slice
- explicitly check whether the harness save call must send the analyzer-owned lowered request rather than the original selection fixture
- explicitly check whether `source_v2_job_id` provenance must be included for AOI source-selection save

Files you should inspect at minimum:

- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_v1_completion.md`
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_scope.md`
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_scope.md`
- `communications/MEMO_2026-04-01_phase_e_transient_consumer_identity_plurality_v1_completion.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `src/presenter/compose_from_intent.py`
- `src/presenter/composition_source_bridge.py`
- `src/presenter/schemas.py`
- `src/api/routes/presenter.py`
- `src/api/routes/orchestrator.py`
- `src/orchestrator/direct_sections_compose_harness.py`
- `src/presenter/compose_session_store.py`
- `tests/test_compose_sessions.py`
- `/home/evgeny/projects/transient-proof-harness/src/App.tsx`
- `/home/evgeny/projects/transient-proof-harness/src/lib/transientClient.ts`
- `communications/PROOF_phase_e_transient_proof_harness_source_selection_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_source_selection_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_saved_session_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_reopen_segment_2026-04-01.json`

Output requirements:

- write your review to:
  - `communications/REPORT_Claude_Phase_E_Proof_Only_Lifecycle_Source_Selection_Scope_Critique_2026-04-01.md`
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
