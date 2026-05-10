Review the proposed next Phase E scope memo:

- `communications/MEMO_2026-03-31_phase_e_transient_consumer_identity_generality_scope.md`

Your task:

1. test the robustness of the memo's assumptions
2. examine the memo against the bigger picture and overall program objectives
3. scrutinize the memo's claims against the actual codebase
4. read any relevant recent memos and proof artifacts in `communications/` that bear on this question
5. identify whether this is truly the next smallest honest Phase E step, or whether a different narrower/stronger step should come first

Important review constraints:

- do not treat the memo as authoritative just because it exists
- explicitly check whether the claimed next variable is honestly only consumer-identity plurality, rather than a disguised harness replay or premature generic consumer architecture
- explicitly check whether the proposed step is stronger than simply broadening `source_profile` or lifecycle on the proof-only harness
- explicitly check whether the codebase still makes consumer admission effectively hard-coded in `src/presenter/compose_from_intent.py`
- explicitly check whether readiness coupling makes the proposed fail-closed story honest
- explicitly check whether the existing proof-only harness repo already proves enough that this next step would be too weak

Files you should inspect at minimum:

- `communications/MEMO_2026-03-31_phase_e_transient_proof_harness_v1_completion.md`
- `communications/MEMO_2026-03-31_phase_e_host_neutral_transient_harness_scope.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `src/presenter/compose_from_intent.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/consumers/definitions/transient-proof-harness.json`
- `tests/test_transient_proof_harness_contract.py`
- `/home/evgeny/projects/transient-proof-harness/src/App.tsx`
- `/home/evgeny/projects/transient-proof-harness/src/lib/transientClient.ts`
- `communications/PROOF_phase_e_transient_proof_harness_source_selection_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_2026-03-31.json`

Output requirements:

- write your review to:
  - `communications/REPORT_Claude_Phase_E_Transient_Consumer_Identity_Generality_Scope_Critique_2026-03-31.md`
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
