# Prompt: Codex Audit Of Phase E Transient Second-Consumer Live Proof Closeout Scope

Audit this scope memo against the live codebase, the broader program direction, and the current Phase E boundary:

- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_live_proof_closeout_scope.md`

Also read enough surrounding material to test whether the memo is strategically honest and codebase-accurate:

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
- relevant recent Phase E and Stage 13 review/completion memos in `communications/`

Inspect the analyzer-v2 codebase directly, especially:

- `src/presenter/compose_from_intent.py`
- `src/api/routes/presenter.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/consumers/definitions/aoi-canary.json`
- `tests/test_compose_from_intent.py`
- `tests/test_aoi_canary_contract.py`
- `tests/test_representative_composition_matrix.py`

Also inspect the current `aoi-canary` repo directly, especially:

- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts`
- `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-selection.json`
- `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts`
- `/home/evgeny/projects/aoi-canary/README.md`

Audit questions:

1. Is one live-proof closeout over the already-landed `aoi-canary` / AOI `source_selection` path the right next Phase E step, or should the replay proof already count as sufficient closure?
2. Is the memo honest about the current claim boundary:
   - code-complete and test-clean
   - deterministic replay proof exists
   - fresh browser/network live proof does not yet exist?
3. Is the memo correct to keep the exact same proof path fixed instead of widening to:
   - `source_profile`
   - non-AOI transient proof
   - broader consumer architecture?
4. Does the required live evidence set mechanically prove the thin-host claim, or are any key assertions still too narrative?
5. Is the blocker-handling rule bounded correctly, or does it risk turning closeout into broad engine-definition cleanup?
6. Does the memo keep the strategic claim calibrated:
   - live documentary closeout of an already-landed second-consumer path
   - not a new architecture proof
   - not broad consumer generality?

If useful, run non-destructive verification commands or focused tests in either repo.

Output requirements:

- Write the audit to:
  - `communications/REPORT_Codex_Phase_E_Transient_Second_Consumer_Live_Proof_Closeout_Scope_Audit_2026-03-30.md`
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
