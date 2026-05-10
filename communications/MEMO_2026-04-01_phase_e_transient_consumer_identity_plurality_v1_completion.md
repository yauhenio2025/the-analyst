# Memo: Phase E Transient Consumer Identity Plurality V1 Completion

Subtitle: Two proof-only consumer keys now admitted over the same standalone harness and same two transient seams

Date: 2026-04-01
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Implements:
- `communications/MEMO_2026-03-31_phase_e_transient_consumer_identity_generality_scope.md`
Relevant Prior Completion:
- `communications/MEMO_2026-03-31_phase_e_transient_proof_harness_v1_completion.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Transient_Consumer_Identity_Generality_Scope_Critique_2026-03-31.md`
- `communications/REPORT_Codex_Phase_E_Transient_Consumer_Identity_Generality_Scope_Audit_2026-03-31.md`
Proof Artifacts:
- `communications/PROOF_phase_e_transient_proof_probe_source_selection_2026-04-01.json`
- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_2026-04-01.json`
- `communications/PROOF_phase_e_transient_proof_probe_source_selection_live_closeout_2026-04-01.json`
- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_live_closeout_2026-04-01.json`
- `communications/PROOF_phase_e_transient_proof_probe_source_selection_live_closeout_2026-04-01.har`
- `communications/PROOF_phase_e_transient_proof_probe_source_selection_live_closeout_2026-04-01.png`
- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_live_closeout_2026-04-01.har`
- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_live_closeout_2026-04-01.png`

## Purpose

Record completion of the bounded Phase E slice that added one second proof-only consumer key to the already-proved standalone harness line.

This slice answered one specific question:

- is analyzer transient admission still effectively singular to one proof-only consumer key on the standalone harness line, or can a second proof-only consumer key ride the same harness and same two already-proved transient seams?

## Outcome

That bounded question is now answered in the affirmative.

The program now has live-proof that the hard-coded transient admission allowlist in `src/presenter/compose_from_intent.py` can carry two proof-only consumer keys over the same harness and same AOI + non-AOI transient seams.

The honest closed claim is narrow:

- bounded proof-only consumer-key plurality on the hard-coded transient admission line, plus end-to-end consumer_key propagation on the same harness surface

This does not mean:

- generic consumer admission (admission is still a manually curated code-level dict)
- renderer-adaptation generality (both consumers use the same renderer surface, so no adaptation fallback was exercised)
- lifecycle broadening
- source-profile broadening
- that consumer identity no longer matters in general

## What Landed

### 1. One additional proof-only consumer definition

- `src/consumers/definitions/transient-proof-probe.json`

Same renderer/sub-renderer surface as `transient-proof-harness`:
- supported renderers: `accordion`, `card_grid`, `tab`, `raw_json`
- supported sub-renderers: `annotated_prose`, `chip_grid`, `mini_card_list`, `rich_description_list`

### 2. Bounded admission in the hard-coded allowlist

- `src/presenter/compose_from_intent.py:179-184`: `transient-proof-probe` added to `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` with exactly `source_selection` and `direct_sections`
- `src/presenter/compose_from_intent.py:186-189`: `transient-proof-probe` is absent from `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`, keeping `source_profile` fail-closed

The admission gate function `get_transient_handoff_capability_error()` at `compose_from_intent.py:565-585` enforces both maps without code changes; it already gates generically by consumer key.

### 3. Harness consumer parameterization

The standalone harness at `/home/evgeny/projects/transient-proof-harness` now supports consumer selection:

- `App.tsx:25`: `ProofConsumerKey` union type (`'transient-proof-harness' | 'transient-proof-probe'`)
- `App.tsx:39`: default remains `transient-proof-harness`
- `App.tsx:48-57`: fixture matrix keyed by `[consumerKey][proofCase]`
- `App.tsx:64-68`: consumer selection from URL param `consumerKey`
- `App.tsx:104-108`: identity assertion now dynamically matches `activeFixture.request.consumer_key` (no longer hard-coded)
- `App.tsx:166-179`: consumer selector UI buttons

Non-identity analytical variables stay fixed when switching consumer:
- same `planning_decision_id` per case
- same `workflow_key` per case
- same `source_v2_job_id` (source_selection case)
- same compose route per case
- same expected root renderer per case
- same expected raw-json leaf set per case

### 4. Fresh probe-specific fixtures

- `/home/evgeny/projects/transient-proof-harness/src/fixtures/transient-source-selection-probe.json`
- `/home/evgeny/projects/transient-proof-harness/src/fixtures/transient-genealogy-direct-sections-probe.json`

These were generated from real analyzer behavior under `consumer_key=transient-proof-probe`, not hand-edited from prior harness bundles.

### 5. Fresh analyzer proof bundles

- `communications/PROOF_phase_e_transient_proof_probe_source_selection_2026-04-01.json`
- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_2026-04-01.json`

Both contain full `request_json`, `response_json`, and `consumer_adaptation_truth` sections under the probe consumer key.

### 6. Two live closeouts under the new consumer key

AOI `source_selection` live closeout:

- `communications/PROOF_phase_e_transient_proof_probe_source_selection_live_closeout_2026-04-01.json`
- `consumer_key = transient-proof-probe`
- `response_status = 200`
- `response_presentation_consumer_key = transient-proof-probe`
- `observed_request_json_equals_pinned_fixture_request = true`
- `observed_root_renderer = tab`
- `raw_json_leaf_keys = ["compose_intent_04_aoi_thematic_report"]`
- `root_renderer_matches = true`
- `raw_json_set_matches = true`
- `forbidden_analytical_requests_observed = []`

Genealogy `direct_sections` live closeout:

- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_live_closeout_2026-04-01.json`
- `consumer_key = transient-proof-probe`
- `response_status = 200`
- `response_presentation_consumer_key = transient-proof-probe`
- `observed_request_json_equals_pinned_fixture_request = true`
- `observed_root_renderer = card_grid`
- `raw_json_leaf_keys = []`
- `root_renderer_matches = true`
- `raw_json_set_matches = true`
- `forbidden_analytical_requests_observed = []`

## Verification

Analyzer verification:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_source_backed_readiness.py tests/test_transient_proof_harness_contract.py tests/test_transient_proof_probe_contract.py tests/test_compose_sessions.py tests/test_representative_composition_matrix.py`
- result: `70 passed, 2 warnings`

Key test coverage for the new consumer:

- `tests/test_compose_from_intent.py:957-965`: admission shape assertion (only `source_selection` and `direct_sections`, `source_profile` excluded, absent from source profiles map)
- `tests/test_compose_from_intent.py:1029-1084`: compose-from-selection acceptance under probe key
- `tests/test_compose_from_intent.py:1284-1291`: compose-from-source explicit rejection for probe
- `tests/test_compose_from_intent.py:1346-1389`: compose-from-intent acceptance under probe key for genealogy
- `tests/test_source_backed_readiness.py:322-343`: readiness blocked for probe on AOI `source_profile`
- `tests/test_transient_proof_probe_contract.py:27-52`: AOI proof bundle contract truth
- `tests/test_transient_proof_probe_contract.py:55-76`: genealogy proof bundle contract truth

Harness verification:

- `npm --prefix /home/evgeny/projects/transient-proof-harness run type-check` -> passed
- `npm --prefix /home/evgeny/projects/transient-proof-harness run test -- --run` -> `10 passed`

Prior harness consumer (`transient-proof-harness`) remains unchanged and still passes.

## Worktree Notes

At live-capture time:

- `analyzer_v2_repo_state = dirty`
- `analyzer_v2_commit_sha = 01427880e1c4c5ddb896b8b0c7fb8c74f6b228c9`
- `transient_proof_harness_repo_state = dirty`
- `transient_proof_harness_commit_sha = c11fa0f0297d0c62135fbbbaf45bc325d4ceb8ff`

The analyzer-v2 worktree had a large set of pre-existing unrelated tracked and untracked changes. Only the files named in this memo were changed by this slice.

## Honest Boundary

### What is now true

- analyzer-v2 admits two proof-only consumer keys on the standalone harness line:
  - `transient-proof-harness`
  - `transient-proof-probe`
- both are admitted only on:
  - `source_selection`
  - `direct_sections`
- both are blocked on:
  - `source_profile`
- the standalone harness can exercise both consumer keys over the same proof cases without code branching beyond consumer/fixture selection
- all non-identity analytical variables remain identical across consumer keys
- end-to-end consumer_key propagation works correctly for both keys (request → response → harness assertion)

### What is not yet true

- admission is not generic or data-driven; it remains a hard-coded dict in `compose_from_intent.py`
- renderer adaptation was not materially tested (both consumers use the same renderer surface)
- lifecycle law was not broadened
- source-profile law was not broadened
- broad consumer registration architecture does not exist
- consumer identity is not irrelevant in general

### What this slice actually proved

The substance of this slice is narrow and honest:

1. The hard-coded transient allowlist accepts more than one proof-only consumer key
2. Consumer_key propagates correctly end-to-end under a second proof-only key
3. The harness can parameterize over consumer identity while keeping all analytical variables fixed
4. The fail-closed gate on `source_profile` and readiness blocks correctly for the new key

This is the smallest useful Phase E step, not a strong generality proof.

## Decision

This bounded Phase E slice is complete on its intended bar.

The program now has proof-only consumer-key plurality on the standalone harness line. The honest documentary claim is:

- the hard-coded transient admission allowlist is not singular to one proof-only consumer key; two proof-only consumer keys can ride the same minimal harness over the same AOI and non-AOI transient seams while source_profile remains fail-closed

The next honest Phase E question is no longer consumer-key plurality on the proof-only line.

The next bounded step should be:

- one standalone-harness lifecycle proof over the already-proved `direct_sections` lifecycle seam
- one fixed proof-only consumer key

Why this is the next honest slice:

- compose-session persistence is still `ComposeFromIntentRequest`-shaped in `src/presenter/schemas.py`
- genealogy `direct_sections` already runs through that exact request/response law
- the standalone harness and proof-only consumer plurality line are now both already proved
- March 28 already proved the lifecycle law on `direct_sections` in the older current-consumer shell, so the remaining honest variable is whether that same law survives the standalone harness boundary
- broadening lifecycle first on AOI `source_selection` would run into the current public save seam as it exists today and would likely require session-schema widening, which is materially larger than this next bounded step

So the clean next question is:

- can the standalone proof-only harness now prove one bounded explicit save/reopen lifecycle on the already-proved `direct_sections` seam, with explicit `session_id` identity, without recomputation on reopen and without reopening source-profile or generic consumer-architecture questions?
