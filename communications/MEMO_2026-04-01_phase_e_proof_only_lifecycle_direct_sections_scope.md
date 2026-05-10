# Memo: Phase E Proof-Only Lifecycle Direct-Sections Scope

Subtitle: One standalone-harness save/reopen proof over the already-proved `direct_sections` lifecycle seam

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
Most Recent Completion:
- `communications/MEMO_2026-04-01_phase_e_transient_consumer_identity_plurality_v1_completion.md`
Relevant Prior Lifecycle Work:
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_implementation_completion.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_completion.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
Relevant Proof Artifacts:
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_genealogy_direct_sections_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_2026-04-01.json`
- `communications/PROOF_phase_e_transient_proof_probe_genealogy_direct_sections_live_closeout_2026-04-01.json`

## Purpose

Define the next bounded Phase E slice after proof-only consumer plurality is complete on the standalone harness line.

The missing seam is no longer:

- harness boundary
- second proof-only consumer identity
- AOI/non-AOI proof shape on the standalone harness

The missing seam is now:

- host-boundary generality for the already-proved analyzer-owned save/reopen lifecycle law on that same proof-only line

This memo scopes the smallest honest next step without drifting into:

- `source_selection` lifecycle widening
- `source_profile`
- broader consumer registration
- generic session-schema unions
- or productization of the standalone harness

## Current Code-Backed Boundary

### What already exists

The current codebase already has:

- a standalone proof-only harness repo:
  - `/home/evgeny/projects/transient-proof-harness`
- two proof-only consumer keys proved on that same harness line:
  - `transient-proof-harness`
  - `transient-proof-probe`
- two already-proved transient seams on that same harness line:
  - AOI `source_selection`
  - genealogy `direct_sections`
- analyzer-owned compose-session routes:
  - `POST /v1/presenter/compose-sessions`
  - `GET /v1/presenter/compose-sessions/{session_id}`
- analyzer-owned file-backed compose-session persistence:
  - `src/presenter/compose_session_store.py`
- one bounded lifecycle proof on the older current-consumer line:
  - March 28 Phase 3 over genealogy `direct_sections`

The key schema fact is:

- `ComposeSessionSaveRequest.compose_request` is still `ComposeFromIntentRequest`
- `PersistedComposeSession.compose_request` is still `ComposeFromIntentRequest`

That law currently lives in:

- `src/presenter/schemas.py`
- `src/presenter/compose_session_store.py`
- `src/api/routes/presenter.py`
- `tests/test_compose_sessions.py`

### What does not exist yet

On the standalone proof-only harness line, the codebase does not yet have:

- one bounded live `compose -> explicit save -> reopen by session_id` proof
- a proof-only harness UI flow for save/reopen
- harness-side compose-session client functions
- fresh proof artifacts showing reopen without recomputation

Important negative facts:

- `planning_decision_id` is still provenance, not lifecycle identity
- the standalone harness currently proves transient rendering only, not save/reopen lifecycle
- the public `compose-sessions` seam is still `ComposeFromIntentRequest`-shaped, so AOI `source_selection` does not fit that save/reopen seam as it exists today because its compose request shape is `ComposeFromSelectionRequest`, not `ComposeFromIntentRequest`
- the standalone harness currently shows `planning_decision_id` as its visible identity, so this slice must surface analyzer-generated `session_id` explicitly to keep lifecycle identity honest

## Strategic Decision

The next bounded Phase E slice should keep both the harness boundary and consumer identity fixed, and vary only host-boundary lifecycle proof.

Keep fixed:

- the standalone harness repo:
  - `/home/evgeny/projects/transient-proof-harness`
- one proof-only consumer key:
  - default `transient-proof-harness`
- one workflow seam:
  - genealogy `direct_sections`
- one compose route:
  - `POST /v1/presenter/compose-from-intent`
- the existing compose-session save/fetch routes
- the existing request/response schemas

Vary:

- whether the already-proved analyzer-owned lifecycle law can now survive the standalone proof-only harness boundary

Why `direct_sections` is the right first lifecycle target:

1. it already rides the exact `ComposeFromIntentRequest` / `ComposeFromIntentResponse` law used by the compose-session persistence seam
2. it avoids silently widening compose-session schema into unions just to make `source_selection` fit
3. it keeps the lifecycle question honest:
   - what exact object is saved?
   - what exact object is reopened?
   - what recomputation is forbidden on reopen?
4. it is materially stronger than the March 28 current-consumer lifecycle proof because the standalone harness currently has zero lifecycle infrastructure beyond what this slice would add
5. it is still smaller than reopening broader lifecycle or admission architecture

## Proposed Scope

### 1. Keep consumer identity fixed

Use one fixed proof-only consumer key for this slice:

- `transient-proof-harness`

Do not vary consumer identity inside this slice.

Plurality is already proved and should remain test-covered in parallel, but it is not the variable being tested here.

### 2. Add one bounded lifecycle flow to the standalone harness

The harness should gain one proof-only lifecycle flow for:

- `genealogy_direct_sections`

Required behavior:

1. compose the already-proved `direct_sections` case
2. expose one explicit save action
3. send the exact composed request/response pair to:
   - `POST /v1/presenter/compose-sessions`
4. receive analyzer-generated `session_id`
5. surface that `session_id` explicitly in the harness UI/state instead of continuing to present `planning_decision_id` as the visible identity
6. support reopen by that `session_id`
7. on reopen, fetch:
   - `GET /v1/presenter/compose-sessions/{session_id}`
8. render the saved compose-session truth without recomputing planner/composition work

The harness may use:

- query-param navigation
- a small saved-session route
- or another minimal local mechanism

But the law must remain:

- `session_id` is lifecycle identity
- `planning_decision_id` is provenance only

Two harness-side plumbing additions are required explicitly in this slice:

- one save-session client function
- one fetch-session client function

And reopen must pass the consumer key explicitly:

- `GET /v1/presenter/compose-sessions/{session_id}?consumer_key=transient-proof-harness`

Reason:

- the GET route still defaults `consumer_key` to `the-critic`, so failing to pass the proof-only consumer key would produce a truthful `409` mismatch rather than an honest reopen proof

### 3. Keep the slice `ComposeFromIntentRequest`-shaped

Do not widen the compose-session contract in this slice.

That means:

- target `direct_sections` first
- leave AOI `source_selection` lifecycle explicitly out of scope

Reason:

- current compose-session persistence is still `ComposeFromIntentRequest`-shaped in `src/presenter/schemas.py`
- the public save/fetch seam therefore fits `direct_sections` directly and does not fit `source_selection` directly
- broadening it to support `ComposeFromSelectionRequest` would be a materially larger step than the next honest bounded lifecycle proof

### 4. Prove reopen is served from saved session truth

The live proof must make the no-recomputation claim auditable.

On reopen, the captured success path must show no rerun of:

- `route-task`
- `plan-task`
- planning-decision fetch
- lowering
- `compose-from-intent`

Allowed reopen call:

- `GET /v1/presenter/compose-sessions/{session_id}`

Allowed supporting requests may appear, but they must be called out explicitly in the proof note.

### 5. Freeze a bounded proof artifact family

The lifecycle slice should freeze one bounded artifact family under the real execution date, including at minimum:

- saved-session JSON summary
- reopen-segment JSON summary
- full HAR for the save/reopen proof session
- rendered screenshot
- invalid-session JSON summary

Recommended naming family:

- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_saved_session_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_reopen_segment_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_session_2026-04-01.har`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_rendered_2026-04-01.png`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_invalid_session_2026-04-01.json`

## Acceptance Bar

This slice should count as complete only if all of the following are true:

1. the standalone harness can compose the pinned `genealogy_direct_sections` case under one fixed proof-only consumer key

2. the harness can explicitly save that exact composed response through:
- `POST /v1/presenter/compose-sessions`

3. the analyzer returns an analyzer-generated `session_id`

4. the harness surfaces that `session_id` explicitly as lifecycle identity

5. the harness can reopen by that `session_id` and render the saved surface through:
- `GET /v1/presenter/compose-sessions/{session_id}?consumer_key=transient-proof-harness`

6. the reopened surface is served from saved compose-session truth with zero recomputation of:
- `route-task`
- `plan-task`
- planning-decision fetch
- lowering
- `compose-from-intent`

7. the reopened payload preserves the saved response truth exactly enough to verify:
- `consumer_key`
- `workflow_key`
- `presentation_hash`
- `presentation_content_hash`
- `resolver_version`

8. invalid `session_id` fails closed

9. existing plurality proof remains intact in parallel:
- `transient-proof-harness`
- `transient-proof-probe`
- both transient-only proof cases

10. this slice does not widen:
- `source_selection` lifecycle
- `source_profile`
- readiness behavior
- generic session-schema unions

## Out Of Scope

This slice should not:

- add lifecycle support for AOI `source_selection`
- add lifecycle support for `source_profile`
- vary consumer identity again
- reopen renderer-surface questions
- introduce a generic saved-session browser app
- replace the existing bounded compose-session schema with a union over every compose request type

## Honest Claim If Completed

If this slice closes honestly, the claim should remain narrow:

- one fixed proof-only consumer on the standalone harness can now carry the already-proved analyzer-owned `direct_sections` lifecycle law across a thinner host boundary, with explicit `session_id` identity and no recomputation on reopen

It would not yet mean:

- lifecycle law is generalized across all transient request families
- AOI `source_selection` save/reopen is solved
- consumer identity no longer matters for lifecycle
- generic reusable app/session lifecycle architecture now exists

## Why This Is The Next Honest Step

After proof-only plurality, this is the smallest stronger question available:

- stronger than another consumer-identity variation
- smaller than source-selection lifecycle
- smaller than session-schema widening
- smaller than contract-driven admission refactors

It is also the cleanest step that uses the codebase as it actually exists:

- compose-session persistence is already real
- but it is still `ComposeFromIntentRequest`-shaped
- so `direct_sections` is the correct next proof seam

If this slice closes honestly, the next broader question after it would be:

- whether proof-only lifecycle can broaden beyond `ComposeFromIntentRequest`-shaped `direct_sections` to AOI `source_selection` without distorting the compose-session contract
