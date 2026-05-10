# Prompt: Claude Review Of Phase E Transient Second-Consumer Live Proof Closeout Scope

Read and critique:

- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md`

Ground the review in both the bigger program objective and the live code reality.

At minimum, inspect:

- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md`
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json`
- any recent completion or review memos in `communications/` that materially bear on the representative matrix, transient second-consumer implementation, and the live-proof-closeout question

Inspect analyzer-v2 directly, especially:

- `src/presenter/compose_from_intent.py`
- `src/api/routes/presenter.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/consumers/definitions/aoi-canary.json`
- `tests/test_compose_from_intent.py`
- `tests/test_aoi_canary_contract.py`
- `tests/test_representative_composition_matrix.py`

Inspect the current `aoi-canary` repo directly, especially:

- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts`
- `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-selection.json`
- `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts`
- `/home/evgeny/projects/aoi-canary/README.md`

Questions to answer:

1. Is a live-proof closeout the right next step after the transient second-consumer implementation landed, or should the program move on and treat the replay proof as sufficient?
2. Is the memo honest about the current boundary:
   - contract-level implementation claim earned
   - browser/network proof still pending
   - blocker appears unrelated to the second-consumer contract question?
3. Is the memo disciplined enough about keeping the exact same proof target:
   - `aoi-canary`
   - AOI `source_selection`
   - `compose-from-selection`
   - `transient_proof`
4. Is the memo accurate about what must be shown to prove thin-hostness in live evidence?
5. Is the blocker-handling rule scoped correctly, or is it inviting too much unrelated infrastructure work?
6. Does the memo stay calibrated against the bigger program objective:
   - live documentary closeout of one landed second-consumer path
   - not a new generality variable
   - not a new architecture tranche?

Output requirements:

- Write the output to:
  - `communications/REPORT_Claude_Phase_E_Transient_Second_Consumer_Live_Proof_Closeout_Scope_Critique_2026-03-30.md`
- Start with a clear verdict:
  - `Approve`
  - `Approve with revisions`
  - `Reject`
- Prioritize concrete findings, scope corrections, strategic risks, and documentary-honesty issues
- Be explicit about what the memo gets right
- Keep the distinction between:
  - strategic disagreement
  - scope correction
  - implementation caution
  clear throughout
