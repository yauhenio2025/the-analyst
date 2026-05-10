# Memo: Phase E AOI Canary Source-Profile Comparison Second-Consumer Scope

Subtitle: Broaden the already-live-proved `aoi-canary` AOI `source_profile:dossier` path to the remaining `source_profile:comparison` surface

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
Immediate Prior Completion:
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_dossier_second_consumer_v1_completion.md`
Relevant Prior Completion:
- `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
Relevant Prior Scope:
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_second_consumer_scope.md`

## Purpose

Define the next bounded Phase E step after the `aoi-canary` second consumer is now live-proved on:

- AOI `source_selection`
- AOI `source_profile` with `profile = dossier`

The next unresolved variable is no longer:

- whether `aoi-canary` can consume the `source_profile` route family at all

That question is now answered in bounded dossier-only form.

The next unresolved variable is narrower:

- whether the same second consumer can broaden from the smaller `source_profile:dossier` surface to the remaining `source_profile:comparison` surface without reopening broader consumer architecture

So the next honest step is:

- keep the same consumer
- keep the same route family
- keep the same AOI workflow family
- broaden only the remaining `comparison` preset surface

not:

- a non-AOI second-consumer proof
- a third consumer
- generic consumer architecture
- or a broader host-neutral platformization tranche

## Current Code-Backed Boundary

### What is already true

Analyzer-v2 now has:

- live `the-critic` coverage for both AOI `source_profile` presets:
  - `dossier`
  - `comparison`
- live `aoi-canary` coverage for:
  - AOI `source_selection`
  - AOI `source_profile:dossier`
- explicit fail-closed analyzer policy for:
  - AOI `source_profile:comparison` on `aoi-canary`
- matching readiness truth for that same bounded policy

`aoi-canary` already has the bounded host substrate needed for the next step:

- `transient_proof`
- one separate `composeFromSource()` client
- one separate `ComposeFromSourceRequest` fixture type
- one proof selector that preserves:
  - `source_selection` as the default case
  - `source_profile:dossier` as the second case

So this next slice is smaller than the dossier slice was.

But it is not zero-work on the canary side.

The current proof shell still bakes dossier-specific branching into:

- `buildTransientStatusLabel(...)`
- `buildTransientSurfaceMessage(...)`

and the case model still only names:

- `source_selection`
- `source_profile_dossier`

So the comparison slice still needs explicit canary-side plumbing:

- widen the proof-case union and case map
- add one third fixture-backed proof case
- make status/surface copy profile-aware rather than binary dossier-vs-selection branching

It does not need:

- a new top-level canary mode
- a new client architecture
- or a new readiness concept

### What is still missing

The current explicit gap is:

- `src/presenter/compose_from_intent.py`
  - `aoi-canary` still rejects `profile='comparison'`
- `src/analysis_products/source_backed_readiness.py`
  - `allowed_selectors` for `consumer_key=aoi-canary` currently stop at:
    - `['dossier']`
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
  - no third proof selector case exists yet for:
    - `source_profile:comparison`
- `/home/evgeny/projects/aoi-canary/src/fixtures/`
  - no pinned `comparison` fixture exists yet

### Why `comparison` is the right next step

This is the smallest honest next variable because:

1. it stays on the exact same second consumer:
   - `aoi-canary`
2. it stays on the exact same route family:
   - `compose-from-source`
3. it uses the same bounded canary proof shell that now already works for:
   - `source_selection`
   - `source_profile:dossier`
4. it closes the remaining preset-level gap inside the current AOI `source_profile` route family
5. it is broader than dossier because it exercises the remaining AOI source-profile surface:
   - comparison map
   - findings bank
   - report closeout
6. it is still more honest as a next step than forcing a non-AOI consumer proof through an AOI-named host before the current AOI route family itself is closed

## Strategic Decision

Keep the second consumer fixed and vary only the remaining AOI `source_profile` preset surface.

The proof target is:

- consumer:
  - `aoi-canary`
- workflow family:
  - AOI
- route family:
  - `source_profile`
- exact profile:
  - `comparison`
- route:
  - `POST /v1/presenter/compose-from-source`
- matching readiness seam:
  - `GET /v1/results/by-job/{job_id}/source-backed-readiness`
- default pinned source identity:
  - `job-744edf255ad5`

This slice should prove a narrow claim:

- the same second consumer can now consume the full currently supported AOI `source_profile` preset set, not only the smaller dossier surface

It should not claim:

- non-AOI second-consumer support
- `compose-from-intent` support on `aoi-canary`
- broad consumer generality

## Scope Decisions

### Decision 1: Broaden both presenter and readiness together

The scope includes both:

- `POST /v1/presenter/compose-from-source`
- `GET /v1/results/by-job/{job_id}/source-backed-readiness`

Reason:

- the dossier slice proved that route truth and readiness truth have to move together
- if presenter admits `comparison` but readiness still advertises only `dossier`, the analyzer contract story becomes stale again

So the comparison slice must broaden:

- the route gate
- the readiness truth

together.

### Decision 2: Keep readiness naming stable in v1

Do not widen this slice into a schema-label cleanup.

Keep:

- `selector_lifecycle_phase = "source_selection"`

Reason:

- this is still bounded preset-based source selection over the source-backed catalog
- reopening naming/schema cleanup here would turn a narrow profile-surface slice into a broader contract-edit tranche

This is an intentional compromise, not an accidental leftover.
The implementation should test it explicitly:

- `selector_lifecycle_phase` stays `source_selection`
- readiness truth still broadens to include `profile = comparison` for the same pinned triplet when feasible

### Decision 3: Reuse the existing canary proof shell

Keep:

- `transient_proof`
- `source_selection` as the default proof case

Add one third selectable proof case:

- AOI `source_profile:comparison`

Keep all three cases in parallel:

- AOI `source_selection`
- AOI `source_profile:dossier`
- AOI `source_profile:comparison`

Do not replace the current default.
Preserving the already-closed `source_selection` path as the default remains the cleanest way to keep the earlier proof mechanically intact.

### Decision 4: Keep fixture contracts distinct

Do not collapse the selection and source-profile proof inputs into one loose canary shape.

Keep:

- one fixture type for `ComposeFromSelectionRequest`
- one fixture type for `ComposeFromSourceRequest`

Add one new pinned source-profile comparison fixture, for example:

- `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-profile-comparison.json`

The canary must replay that request verbatim.
It must not derive profile truth, source catalogs, or planner truth locally.

### Decision 5: Validate the pinned AOI source job up front

Before implementation starts in earnest, validate that the default pinned source job is truthful for:

- `job-744edf255ad5`
- AOI `source_profile`
- `profile = comparison`

This is more important than it was for dossier, because comparison depends on a broader feasible source surface.

Current repo validation already shows:

- `job-744edf255ad5`
- `allowed_profiles = ['dossier', 'comparison']`

So the default assumption is now stronger than it was for the dossier memo:

- the live blocker is consumer policy, not source feasibility

If that job does not support a truthful comparison-capable source-backed path, choose a replacement AOI source job and record the reason explicitly in:

- the proof note
- the completion memo

### Decision 6: Keep the proof bar live

This slice should close with:

- one frozen analyzer proof bundle
- one real browser/network proof on `aoi-canary`
- one frozen observed `compose-from-source` POST body
- one HAR or equivalent full network capture
- one ready-state screenshot
- one proof note and JSON summary under `communications/`

The live proof should explicitly show:

- `consumer_key = aoi-canary`
- `profile = comparison`
- the pinned `source_v2_job_id` used for proof
- the exact pinned `ComposeFromSourceRequest` on the wire
- no hidden analytical upstream calls

Allowed supporting requests like style-token fetches should still be disclosed honestly.

Be explicit about proof shape, not just proof existence.

The frozen analyzer proof bundle should include at minimum:

- `consumer_key = aoi-canary`
- `route_family = source_profile`
- `profile = comparison`
- `source_v2_job_id`
- `compose_call`
- `request_json`
- `response_json`
- a bounded `consumer_adaptation_truth` summary

The live closeout summary should include at minimum:

- `response_status`
- `resolver_version`
- exact `observed_request_json`
- `observed_request_json_equals_pinned_fixture_request`
- `raw_json_leaf_keys`
- `forbidden_analytical_requests_observed`
- any allowed non-analytical supporting requests

## Must Not Widen

- do not add non-AOI second-consumer proof
- do not add `compose-from-intent` support for `aoi-canary`
- do not add a third consumer
- do not add generic consumer-discovery or plugin architecture
- do not add planner or readiness-driven request synthesis to `aoi-canary`
- do not make the canary derive profile truth or source identity locally
- do not replace the already-closed `source_selection` or `source_profile:dossier` proof paths

## Proposed Acceptance Bar

This slice should count only if all of the following are true:

1. `compose-from-source` accepts:
   - `consumer_key = aoi-canary`
   - `profile = comparison`
   - the pinned `source_v2_job_id` used for proof
2. the pinned job is validated up front as truthful input for the `comparison` path
3. `source_backed_readiness` for that same triplet is semantically truthful:
   - same consumer
   - same profile
   - same pinned job
4. `aoi-canary` replays one pinned `ComposeFromSourceRequest` comparison fixture rather than deriving analytical truth locally
5. `transient_proof` still defaults to `source_selection`
6. one real live `aoi-canary` browser session reaches ready state from the `compose-from-source` request for `profile = comparison`
7. the observed wire request equals the pinned comparison fixture request
8. no forbidden analytical upstream calls appear in the success-path network trace
9. the rendered page still satisfies the bounded degradation law:
   - no root `raw_json`
   - at most one `raw_json` leaf
   - if present, that leaf is the closeout/report leaf only
10. the earlier `source_selection` and `source_profile:dossier` proof paths remain intact, fixture-backed, and test-covered in parallel
11. the proof record is frozen under `communications/`

Test acceptance only, not live-closeout proof by itself:

- unsupported combinations still fail closed, including:
  - `aoi-canary` on `direct_sections`
  - non-AOI widening
  - any remaining unsupported source-profile values outside the now-declared set

Explicit regression coverage should include:

- analyzer:
  - `aoi-canary` succeeds on `source_profile:comparison`
  - `aoi-canary` still succeeds on `source_profile:dossier`
  - `aoi-canary` still succeeds on `source_selection`
  - `aoi-canary` still fails on `direct_sections`
  - non-AOI widening still fails closed
  - readiness for `profile = comparison` is now truthful for the pinned triplet
  - readiness naming remains intentionally stable at `selector_lifecycle_phase="source_selection"`
- canary:
  - the third proof case is selectable
  - status/surface labels are profile-aware
  - the new comparison fixture is replayed verbatim
  - the earlier `source_selection` and `source_profile:dossier` cases remain intact

## Practical Constraints

This slice is narrower than the dossier slice, but it is not free:

- comparison may depend on broader source-family feasibility than dossier
- readiness truth must remain aligned with the widened route policy
- the canary still needs:
  - one new fixture
  - one third proof selector case
  - one new live closeout pass

If implementation starts requiring:

- broader consumer architecture redesign
- non-AOI host work
- planner integration in the canary
- or major route/schema redesign

then the right outcome is to stop and rescope.

## Decision

The next bounded Phase E step should be:

- one `aoi-canary` AOI `source_profile:comparison` second-consumer slice

The strategic reason is:

- it is the smallest remaining AOI second-consumer surface gap
- it strengthens the current claim from dossier-only route-family coverage toward full current AOI `source_profile` preset coverage
- it broadens the second-consumer proof honestly without pretending we have non-AOI or broad consumer generality yet

If this slice closes, the next honest unresolved variable is no longer inside AOI `source_profile`.
At that point the program should revisit the next broader Phase E question explicitly, rather than silently continuing AOI-local preset work by inertia.
