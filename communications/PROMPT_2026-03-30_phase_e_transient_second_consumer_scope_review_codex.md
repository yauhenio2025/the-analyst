# Prompt: Codex Audit Of Phase E Transient Second-Consumer Scope

Audit this scope memo against the live codebase, the broader program direction, and the current Phase E boundary:

- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`

Also read enough surrounding material to test whether the memo is strategically honest and codebase-accurate:

- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- relevant recent Phase E and Stage 13 review/completion memos in `communications/`

Inspect the analyzer-v2 codebase directly, especially:

- `src/presenter/compose_from_intent.py`
- `src/presenter/manifest_builder.py`
- `src/consumers/definitions/aoi-canary.json`
- `src/consumers/registry.py`
- `src/api/routes/presenter.py`
- `tests/test_compose_from_intent.py`
- `tests/test_representative_composition_matrix.py`

Also inspect the current `aoi-canary` repo directly, especially:

- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts`
- `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/resultsClient.test.ts`
- `/home/evgeny/projects/aoi-canary/README.md`

Audit questions:

1. Is a bounded transient second-consumer proof the right next Phase E slice after the representative composition matrix landed?
2. Is `aoi-canary` the right second-consumer target, or is the memo ignoring a better existing consumer surface?
3. Is AOI `source_selection` the right default proof path, or should the scope prefer `source_profile`, both, or something else?
4. Does the memo stay honest about the real analyzer-side work required:
   - expanding the transient consumer allowlist/registration surface
   - not pretending current transient compose is already consumer-neutral?
5. Is analyzer-side fallback such as `prose -> raw_json` an acceptable bounded proof for this slice, or does it weaken the claim too much?
6. Does the memo keep the strategic claim calibrated:
   - bounded transient second-consumer proof
   - not full consumer generality
   - not arbitrary engine/pass composition

If useful, run non-destructive verification commands or focused tests in either repo.

Output requirements:

- Write the audit to:
  - `communications/REPORT_Codex_Phase_E_Transient_Second_Consumer_Scope_Audit_2026-03-30.md`
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
