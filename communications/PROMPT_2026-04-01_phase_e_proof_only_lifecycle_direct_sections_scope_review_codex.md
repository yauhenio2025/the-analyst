Audit the proposed next Phase E scope memo:

- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_scope.md`

Audit goals:

1. test the robustness of the memo's assumptions
2. examine the memo in light of the broader roadmap and overall program objectives
3. verify or falsify its codebase claims directly
4. inspect relevant recent memos and proof artifacts in `communications/`
5. decide whether this is truly the next smallest honest bounded Phase E slice

Please verify at minimum:

- whether `ComposeSessionSaveRequest` and `PersistedComposeSession` are still `ComposeFromIntentRequest`-shaped in `src/presenter/schemas.py`
- whether that makes genealogy `direct_sections` the smallest honest standalone-harness lifecycle target
- whether AOI `source_selection` lifecycle would silently require session-schema widening
- whether keeping consumer identity fixed after plurality is the right isolation discipline
- whether the memo overstates what a proof-only lifecycle direct-sections slice would prove
- whether the existing March 28 lifecycle proof already covers enough that this next slice would be too weak
- whether the standalone proof-harness boundary makes this lifecycle slice meaningfully stronger than the earlier the-critic-based lifecycle proof
- whether the harness must surface `session_id` explicitly rather than continuing to show `planning_decision_id` as visible identity
- whether reopen must pass `consumer_key=transient-proof-harness` explicitly to avoid a truthful `409`

Files to inspect at minimum:

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

- write the audit to:
  - `communications/REPORT_Codex_Phase_E_Proof_Only_Lifecycle_Direct_Sections_Scope_Audit_2026-04-01.md`
- begin with a verdict:
  - `Approve`
  - `Approve with corrections`
  - `Reject`
- keep the audit code-backed and specific
- call out any mismatch between the memo's framing and the actual code seams
- if you think another next step should come first, state it explicitly and explain the tradeoff
