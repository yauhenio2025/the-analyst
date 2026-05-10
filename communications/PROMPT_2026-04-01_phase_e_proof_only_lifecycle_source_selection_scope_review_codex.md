Audit the proposed next Phase E scope memo:

- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_scope.md`

Audit goals:

1. test the robustness of the memo's assumptions
2. examine the memo in light of the broader roadmap and overall program objectives
3. verify or falsify its codebase claims directly
4. inspect relevant recent memos and proof artifacts in `communications/`
5. decide whether this is truly the next smallest honest bounded Phase E slice

Please verify at minimum:

- whether `ComposeSessionSaveRequest` and `PersistedComposeSession` are still `ComposeFromIntentRequest`-shaped
- whether `compose_from_selection()` already lowers into an internal `ComposeFromIntentRequest`
- whether the current public `compose-from-selection` response exposes the exact lowered request or only lineage/section metadata
- whether one optional `persistable_intent_request` field on `ComposeFromIntentResponse` is the smallest honest concrete mechanism
- whether the harness could honestly reconstruct the lowered request today, or whether that would be host-local fabrication
- whether the existing analyzer lowering fetch is direct-sections-only and therefore not a current AOI `source_selection` escape hatch
- whether exposing analyzer-owned lowered request truth is the smallest honest next bridge
- whether a tiny dedicated analyzer-owned save bridge would be smaller or stronger than the response-field approach
- whether a generic save-schema union is unnecessary for this slice but still honestly deferred as a later architectural option
- whether keeping consumer identity fixed at `transient-proof-harness` is the right isolation discipline after plurality and direct-sections lifecycle are complete
- whether `source_profile` should remain out of scope
- whether this slice overstates what source-selection lifecycle broadening would prove
- whether the harness save call must send the analyzer-owned lowered request rather than the original selection fixture
- whether `source_v2_job_id` provenance must be included for AOI source-selection save

Files to inspect at minimum:

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

- write the audit to:
  - `communications/REPORT_Codex_Phase_E_Proof_Only_Lifecycle_Source_Selection_Scope_Audit_2026-04-01.md`
- begin with a verdict:
  - `Approve`
  - `Approve with corrections`
  - `Reject`
- keep the audit code-backed and specific
- call out any mismatch between the memo's framing and the actual code seams
- if you think another next step should come first, state it explicitly and explain the tradeoff
