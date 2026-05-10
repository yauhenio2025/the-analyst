# Memo: Phase E AOI Canary Source-Profile Second-Consumer Scope

Subtitle: Broaden the already-live-proved second consumer from AOI `source_selection` to the remaining AOI `compose-from-source` family

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
- `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`
Relevant Prior Completion:
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
Relevant Prior Scope:
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`

## Purpose

Define the next bounded Phase E step after the `aoi-canary` / AOI `source_selection` second-consumer path is fully live-proved.

The previous bounded Phase E questions are now answered:

- the current live transient compose substrate generalizes across the representative handoff-family matrix on the current consumer surface
- one real second consumer can consume one bounded AOI transient path without host-local analytical reconstruction
- that second-consumer path is now backed by real browser/network evidence, not only tests and replay artifacts

The next unresolved variable is narrower than “consumer generality” in the abstract:

- the same second consumer still does not cover the remaining AOI compose family
- `compose-from-source` and `source_backed_readiness` still retain explicit `the-critic` coupling for that path

So the next honest step is:

- broaden the already-live-proved `aoi-canary` consumer from AOI `source_selection` to AOI `source_profile`

not:

- a non-AOI second-consumer proof
- a third consumer
- generic consumer architecture
- or a broader productization tranche

## Current Code-Backed Boundary

### What is already true

Analyzer-v2 already has:

- live `the-critic` coverage for both AOI transient compose families:
  - `source_profile`
  - `source_selection`
- live `aoi-canary` coverage for:
  - AOI `source_selection` only
- a handoff-aware transient consumer gate in:
  - `src/presenter/compose_from_intent.py`
- a bounded second-consumer proof shell in:
  - `/home/evgeny/projects/aoi-canary/src/App.tsx`
  - `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts`
  - `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-selection.json`

The current canary proof shell is still selection-shaped end to end:

- `transientClient.ts` only exposes:
  - `composeFromSelection()`
- the current pinned fixture is:
  - `transient-aoi-source-selection.json`
- `App.tsx` currently loads that one fixture in `transient_proof` mode and posts only to:
  - `/v1/presenter/compose-from-selection`

So this next slice is still bounded, but it is not only:

- widen one analyzer-side allowlist entry
- remove one readiness blocker
- add one new fixture

It also includes one small but real canary-side route/client expansion for the `compose-from-source` path.

The current explicit coupling that remains is:

- `src/analysis_products/source_backed_readiness.py`
  - `compose-from-source only supports consumer_key='the-critic' in v1`
- `src/presenter/compose_from_intent.py`
  - `aoi-canary` is admitted only for `source_selection`

### Why `source_profile` is the right next step

This is the smallest honest next variable because:

1. `aoi-canary` is still explicitly an AOI canary surface, not a generic cross-workflow app.
2. `source_profile` is the remaining live AOI compose family already proven on the current consumer surface.
3. The current blocker is concrete and analyzer-owned:
   - consumer admission at `compose-from-source`
   - consumer coupling in `source_backed_readiness`
4. This broadens consumer proof without forcing a jump to non-AOI transient proof or broader consumer architecture.
5. `dossier` is the right narrower target because it is the smallest already-proved `source_profile` surface from the matrix bundle:
   - bounded synthesis plus closeout
   - not the broader comparison-style profile surface

## Strategic Decision

Keep the consumer fixed and vary only the remaining AOI compose family.

The proof target is:

- consumer:
  - `aoi-canary`
- workflow family:
  - AOI
- handoff family:
  - `source_profile`
- route:
  - `POST /v1/presenter/compose-from-source`
- default profile:
  - `dossier`
- default source identity:
  - `job-744edf255ad5`

This slice should prove a narrow claim:

- the same second consumer can consume both currently live AOI transient compose families without host-local analytical reconstruction

It should not claim:

- non-AOI second-consumer support
- `compose-from-intent` consumer generality
- broad multi-consumer architecture

## Scope Decisions

### Decision 1: Treat `compose-from-source` and readiness as one truthful path

The scope includes both:

- `POST /v1/presenter/compose-from-source`
- `GET /v1/results/by-job/{job_id}/source-backed-readiness`

Reason:

- `source_backed_readiness` currently tells the truth about the `compose-from-source` path
- if that truth remains `the-critic`-only while `compose-from-source` itself broadens, the analyzer contract story becomes internally inconsistent

So the next slice should remove the consumer-only blocker for `aoi-canary` on the AOI `source_profile` path rather than widening only the presenter route and leaving readiness stale.

### Decision 2: Keep the canary fixture-backed

Do not add planner integration, readiness-driven request synthesis, or source catalog logic inside `aoi-canary`.

Use one pinned analyzer-owned `ComposeFromSourceRequest` fixture in the canary repo, for example:

- `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-profile-dossier.json`

This fixture must live alongside the existing `source_selection` fixture.
It must not replace or overwrite the already-closed `source_selection` proof path.

The canary should replay that frozen request verbatim.
It must not derive profile or analytical input locally.

The canary-side bounded work here is explicit:

- add one thin `composeFromSource()` client function targeting:
  - `POST /v1/presenter/compose-from-source`
- keep the request schema faithful to `ComposeFromSourceRequest`
- do not try to coerce the `source_profile` path through the existing selection-shaped client surface

Before implementation starts in earnest, validate that the pinned default source job is actually usable on this path:

- `job-744edf255ad5`
- AOI `source_profile`
- profile `dossier`

If that job does not resolve a truthful dossier-capable source catalog for `compose-from-source`, choose a different pinned AOI source job and record the reason explicitly in the proof note and completion memo.

### Decision 3: Reuse the existing `transient_proof` mode

Do not build a second canary architecture path.

The preferred bounded shape is:

- keep `transient_proof`
- add one narrow fixture selector within `transient_proof`, not a new top-level app mode
- minimum proof-selector set:
  - AOI `source_selection`
  - AOI `source_profile:dossier`
- reuse the same thin response normalization and proof-surface validation discipline

This keeps the already-closed `source_selection` proof intact in parallel while adding the new `source_profile` path.

### Decision 4: Keep the proof bar live

This slice should close with:

- one real browser/network proof on `aoi-canary`
- one frozen observed `compose-from-source` POST body
- one HAR or equivalent full network capture
- one ready-state screenshot
- one proof note and JSON summary under `communications/`

The live proof should explicitly show:

- `consumer_key = aoi-canary`
- the exact pinned `ComposeFromSourceRequest` on the wire
- no hidden analytical upstream calls

Allowed supporting requests like style-token fetches should still be disclosed honestly.

## Must Not Widen

- do not add non-AOI second-consumer proof
- do not add `compose-from-intent` support for `aoi-canary`
- do not add a third consumer
- do not add generic consumer-discovery or plugin architecture
- do not add planner integration to `aoi-canary`
- do not make the canary derive source profiles or source identity locally
- do not widen readiness or presenter routes beyond the AOI `source_profile` path for `aoi-canary`

## Proposed Acceptance Bar

This slice should count only if all of the following are true:

1. `compose-from-source` accepts `consumer_key = aoi-canary` for AOI `source_profile`
2. the pinned `source_v2_job_id` is validated up front as truthful input for the `dossier` `source_profile` path on `compose-from-source`
3. AOI `source_backed_readiness` for the same job/profile no longer reports a blocker that is only:
   - `compose-from-source only supports consumer_key='the-critic' in v1`
4. AOI `source_backed_readiness` remains semantically truthful for the `source_profile` followup path rather than merely dropping the old blocker string
5. `aoi-canary` replays one pinned `ComposeFromSourceRequest` fixture rather than deriving profile truth locally
6. one real live `aoi-canary` browser session reaches ready state from that `compose-from-source` request
7. the observed wire request equals the pinned fixture request
8. no forbidden analytical upstream calls appear in the success-path network trace
9. the rendered page still satisfies the bounded degradation law already enforced for the canary transient path
10. the already-closed `aoi-canary` / AOI `source_selection` proof remains reproducible, fixture-backed, and test-covered in parallel
11. the proof record is frozen under `communications/`

If this slice lands, the honest new bounded claim becomes:

- `aoi-canary` can consume both live AOI transient compose families:
  - `source_selection`
  - `source_profile`

## Practical Constraints

This slice is still bounded, but it is not trivial:

- `source_profile` is not just another fixture replay
- the analyzer-side readiness truth currently encodes the old consumer coupling explicitly
- the canary still needs:
  - a second pinned request fixture
  - one thin `compose-from-source` client function
  - one narrow fixture selector inside `transient_proof`
  - one live closeout pass

If implementation starts requiring:

- broader consumer architecture redesign
- non-AOI host work
- planner integration in the canary
- or major route/schema redesign

then the right outcome is to stop and rescope.

## Decision

The next bounded Phase E step should be:

- one `aoi-canary` AOI `source_profile` second-consumer slice

The strategic reason is:

- it is the smallest remaining AOI consumer-generalization seam
- it closes the remaining explicit `the-critic` coupling on the live AOI compose-family surface
- it broadens the second-consumer proof honestly without pretending we have non-AOI or broad consumer generality yet
