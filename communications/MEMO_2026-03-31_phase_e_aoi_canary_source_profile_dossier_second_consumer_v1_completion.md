# Memo: Phase E AOI Canary Source-Profile Dossier Second-Consumer V1 Completion

Subtitle: The bounded `aoi-canary` AOI `source_profile` path is now live-proved on `profile=dossier`, with readiness truth aligned and `comparison` fail-closed

Date: 2026-03-31
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
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_second_consumer_scope.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`
Relevant Prior Completion:
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_AOI_Canary_Source_Profile_Second_Consumer_Scope_Critique_2026-03-31.md`
- `communications/REPORT_Codex_Phase_E_AOI_Canary_Source_Profile_Second_Consumer_Scope_Audit_2026-03-31.md`

## Purpose

Record the completion of the bounded second-consumer broadening slice from:

- `aoi-canary` / AOI `source_selection`

to:

- `aoi-canary` / AOI `source_profile`
- `profile = dossier`

This memo also records the final scope-tightening hardening that made the v1 claim fully honest:

- analyzer-side `source_profile` support for `aoi-canary` is now dossier-only
- `comparison` remains fail-closed
- `source_backed_readiness` now tells that same dossier-only truth rather than advertising both profiles

## Outcome

The bounded `aoi-canary` AOI `source_profile` second-consumer slice is complete on its intended v1 bar.

The closed path is:

- consumer:
  - `aoi-canary`
- workflow family:
  - AOI
- handoff family:
  - `source_profile`
- profile:
  - `dossier`
- pinned source job:
  - `job-744edf255ad5`
- route:
  - `POST /v1/presenter/compose-from-source`
- matching readiness seam:
  - `GET /v1/results/by-job/{job_id}/source-backed-readiness`
- canary mode:
  - `transient_proof`

This means the second consumer is now live-proved on:

- AOI `source_selection`
- AOI `source_profile` with `profile = dossier`

It does not mean:

- full `source_profile` support on `aoi-canary`
- non-AOI second-consumer proof
- broad consumer generality

## What Landed

### 1. Analyzer-side `source_profile` dossier support

Analyzer-v2 now admits `aoi-canary` on the bounded `source_profile` path through:

- `POST /v1/presenter/compose-from-source`

with the truthful v1 restriction:

- `consumer_key = aoi-canary`
- `profile = dossier`

This landed in:

- `src/presenter/compose_from_intent.py`

The final gate shape is two-level:

- consumer -> supported handoff kinds
- consumer -> supported `source_profile` values

So the final analyzer-side truth is:

- `aoi-canary` supports:
  - AOI `source_selection`
  - AOI `source_profile:dossier`
- `aoi-canary` still fails closed for:
  - AOI `source_profile:comparison`
  - `direct_sections`

### 2. Readiness truth now matches the route

`source_backed_readiness` no longer carries stale `the-critic`-only truth for this path.

Instead it now computes consumer-aware `allowed_selectors` and `blocked_selectors`, so the readiness output matches the real admitted path for:

- `consumer_key = aoi-canary`
- `profile = dossier`
- `source_v2_job_id = job-744edf255ad5`

The important stable v1 naming decision remains:

- `selector_lifecycle_phase = "source_selection"`

That was preserved intentionally as bounded preset-based source selection, not reopened into a schema rename tranche.

### 3. Canary-side bounded broadening

`aoi-canary` now keeps the already-closed `source_selection` proof intact while adding one parallel `source_profile:dossier` transient proof case.

What landed in the canary repo:

- one thin `composeFromSource()` client
- one separate `ComposeFromSourceRequest` fixture
- one narrow selector inside `transient_proof`
- distinct fixture typing for:
  - `ComposeFromSelectionRequest`
  - `ComposeFromSourceRequest`

The canary still does not derive analytical truth locally.
It still replays pinned analyzer-owned request fixtures.

### 4. Frozen proof artifacts

The analyzer-side deterministic proof bundle is frozen at:

- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_profile_dossier_2026-03-31.json`

The live closeout artifact set is frozen at:

- `communications/PROOF_phase_e_aoi_canary_source_profile_dossier_live_closeout_2026-03-31.md`
- `communications/PROOF_phase_e_aoi_canary_source_profile_dossier_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_aoi_canary_source_profile_dossier_live_closeout_2026-03-31.png`
- `communications/PROOF_phase_e_aoi_canary_source_profile_dossier_live_closeout_2026-03-31.har`

The live closeout records:

- `response_status = 200`
- `resolver_version = compose-from-source-v3`
- `observed_request_json_equals_pinned_fixture_request = true`
- `compose_request_count_in_session = 1`
- `raw_json_leaf_keys = ["compose_intent_02_aoi_thematic_report"]`
- `forbidden_analytical_requests_observed = []`

### 5. Scope-tightening hardening after implementation review

One follow-up hardening pass was required before this slice could be claimed honestly as dossier-only:

- the initial analyzer-side broadening admitted all `source_profile` values for `aoi-canary`
- the final implementation now blocks `comparison` explicitly at both:
  - the presenter gate
  - the readiness layer

That hardening was not a rescope.
It was the final correction needed to make the v1 claim match the actual implementation boundary.

## Verification

Final focused analyzer verification:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_source_backed_readiness.py tests/test_aoi_canary_contract.py tests/test_representative_composition_matrix.py`
- result:
  - `55 passed, 2 warnings`

Canary verification from the implementation slice:

- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
  - passed
- `npm --prefix /home/evgeny/projects/aoi-canary run test -- --run`
  - `21 passed`

The final real readiness behavior on the pinned AOI source job is now:

- `profile='dossier'`
  - `requested_selector_status=ready`
  - `allowed_selectors=['dossier']`
  - `readiness_status=ready`
- `profile='comparison'`
  - `requested_selector_status=blocked`
  - `allowed_selectors=['dossier']`
  - `blocked_selectors['comparison']=["compose-from-source does not support consumer_key='aoi-canary' for profile='comparison'"]`
  - `readiness_status=partially_ready`

## Honest Boundary

### What is now true

- one real second consumer now live-proves both AOI transient route families in bounded form:
  - `source_selection`
  - `source_profile` with `profile = dossier`
- the canary still consumes analyzer-owned transient truth through the same thin field-only host adapter discipline
- the `source_profile:dossier` live proof is now backed by:
  - tests
  - deterministic frozen proof
  - browser/network closeout
- readiness truth and route truth now agree on the same dossier-only boundary

### What is not yet true

- `aoi-canary` does not yet support `profile = comparison`
- this does not prove full AOI `source_profile` preset coverage on the second consumer
- this does not prove non-AOI second-consumer transient support
- this does not prove `compose-from-intent` support on `aoi-canary`
- this does not prove broad multi-consumer or arbitrary engine/pass composition generality

## Decision

This bounded Phase E slice is now closed on its honest v1 terms:

- implementation landed
- readiness truth landed
- live proof landed
- dossier-only hardening landed

The next honest Phase E step is no longer:

- broadening `aoi-canary` to AOI `source_profile` in the abstract

That question is now answered in bounded dossier-only form.

The next bounded unresolved seam is narrower:

- the remaining `source_profile` preset on the same second consumer:
  - `profile = comparison`

So the next honest slice should ask:

- can the already-live-proved `aoi-canary` AOI `source_profile:dossier` path be broadened to the remaining `source_profile:comparison` surface while preserving the same thin-host and truthful-readiness law?
