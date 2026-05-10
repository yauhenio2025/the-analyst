# Memo: Phase E Proof-Only Lifecycle Source-Selection Scope

Subtitle: One standalone-harness save/reopen proof over AOI `source_selection` via one analyzer-owned persistable lowered intent-request field

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
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_v1_completion.md`
Relevant Prior Scope:
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_scope.md`
Relevant Proof Artifacts:
- `communications/PROOF_phase_e_transient_proof_harness_source_selection_2026-03-31.json`
- `communications/PROOF_phase_e_transient_proof_harness_source_selection_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_saved_session_2026-04-01.json`
- `communications/PROOF_phase_e_proof_only_lifecycle_direct_sections_reopen_segment_2026-04-01.json`

## Purpose

Define the next bounded Phase E slice after standalone-harness lifecycle proof is complete on genealogy `direct_sections`.

The missing seam is no longer:

- whether the standalone harness can carry any save/reopen lifecycle seam
- whether `session_id` identity can survive that thinner host boundary
- whether the proof-only consumer/harness line is only transient

The missing seam is now:

- whether that same proof-only harness can broaden lifecycle from intent-shaped genealogy `direct_sections` to AOI `source_selection` honestly, without host-local reconstruction and without distorting the current save contract by default

This memo scopes the smallest honest next step and keeps the remaining boundary narrow.

## Current Code-Backed Boundary

### What already exists

The codebase now already has:

- standalone-harness transient proof on AOI `source_selection`
- standalone-harness transient proof on genealogy `direct_sections`
- standalone-harness save/reopen lifecycle proof on genealogy `direct_sections`
- one fixed proof-only consumer lifecycle proof on:
  - `consumer_key = transient-proof-harness`
  - `proofCase = genealogy_direct_sections`

The relevant code facts are:

- `compose_from_selection()` already lowers a `ComposeFromSelectionRequest` into an internal `ComposeFromIntentRequest` before composing:
  - `src/presenter/compose_from_intent.py`
- `ComposeSessionSaveRequest.compose_request` is still `ComposeFromIntentRequest`
- `PersistedComposeSession.compose_request` is still `ComposeFromIntentRequest`
- the standalone harness currently saves lifecycle only by sending exact intent-shaped request plus exact raw compose response

### What does not exist yet

What still does not exist is:

- a truthful way for the standalone harness to save AOI `source_selection` through that same analyzer-owned save seam

The important contractual gap is specific:

- the public save seam persists `ComposeFromIntentRequest`
- AOI `source_selection` composes through `POST /v1/presenter/compose-from-selection`
- the current source-selection response trace exposes selection and section-materialization provenance, but not the exact lowered `prose_sections` bodies that were used inside the analyzer-owned compose call
- so the harness cannot honestly reconstruct the exact lowered request locally from current public response truth

One nearby analyzer seam already exists, but it does not solve this AOI problem:

- the current planning-decision lowering fetch is direct-sections-only
- it does not expose analyzer-owned lowered request truth for AOI `source_selection`
- so it is not a current escape hatch for this slice

That means the remaining problem is not simply “schema unions versus no schema unions.”

The real problem is:

- where does the exact analyzer-owned lowered request come from for truthful save?

## Strategic Decision

The next bounded slice should keep the harness, consumer identity, and public save/fetch lifecycle law as stable as possible, and vary only one thing:

- whether analyzer-owned source-selection lifecycle truth can be carried across the standalone harness boundary without local reconstruction

Keep fixed:

- harness repo:
  - `/home/evgeny/projects/transient-proof-harness`
- consumer key:
  - `transient-proof-harness`
- existing save/fetch routes:
  - `POST /v1/presenter/compose-sessions`
  - `GET /v1/presenter/compose-sessions/{session_id}`
- existing `direct_sections` lifecycle proof in parallel

Vary only:

- AOI `source_selection` lifecycle persistence truth

## Proposed Scope

### 1. Expose one analyzer-owned persistable lowered intent request for `source_selection`

The slice should surface the exact lowered `ComposeFromIntentRequest` used inside `compose_from_selection()` as analyzer-owned truth.

Preferred concrete mechanism for this bounded slice:

- add one optional response field to `ComposeFromIntentResponse`, for example:
  - `persistable_intent_request: Optional[ComposeFromIntentRequest]`
- populate it for `compose-from-selection`
- leave it absent / `null` for plain `compose-from-intent`

This is intentionally narrow:

- no new route family
- no new wrapper response type unless implementation review proves it smaller
- no separate save endpoint by default

What must be true:

- the lowered request must come from analyzer-owned compose truth
- it must contain the exact prose sections actually used for composition
- it must preserve the exact values needed for persistence:
  - `workflow_key`
  - `consumer_key`
  - `user_intent`
  - `style_school`
  - full lowered `prose_sections`

What must not happen:

- the harness must not synthesize the lowered request from trace metadata
- the harness must not rebuild prose sections from selection lineage
- the harness must not infer the lowered request from view output

What is explicitly not the default choice for this slice:

- broadening `ComposeSessionSaveRequest` into a generic union over every compose request family

Important wording discipline:

- a generic save-schema union is deferred for this slice, not disproved forever
- if later saved-session architecture needs generic original-request-family preservation, that remains an open broader design question

### 2. Keep lifecycle identity law unchanged

The lifecycle identity law should stay exactly the same as the completed `direct_sections` lifecycle slice:

- `session_id` is lifecycle identity
- `planning_decision_id` is provenance
- `source_v2_job_id` is provenance when real

For AOI `source_selection`, provenance should include:

- `planning_decision_id`
- `source_v2_job_id`

The harness must surface:

- `session_id` as the primary visible identity after save and on reopen
- `planning_decision_id` and `source_v2_job_id` only as provenance

### 3. Keep the standalone harness fixed

Use the same standalone harness and same proof-only consumer:

- `/home/evgeny/projects/transient-proof-harness`
- `consumer_key = transient-proof-harness`

Do not vary consumer identity again in this slice.

Do not create another shell.

Do not add planner fetch, lowering fetch, result discovery, or host-local save helpers.

The current harness lifecycle gate must broaden explicitly from:

- `consumerKey === "transient-proof-harness" && proofCase === "genealogy_direct_sections"`

to a bounded two-case lifecycle gate:

- `consumerKey === "transient-proof-harness"`
- `proofCase === "genealogy_direct_sections" || proofCase === "source_selection"`

### 4. Add one bounded AOI lifecycle flow

The harness should gain one save/reopen lifecycle flow for:

- AOI `source_selection`

Required behavior:

1. compose the pinned AOI `source_selection` fixture through `POST /v1/presenter/compose-from-selection`
2. receive analyzer-owned lowered persistence truth for that exact composed response
3. explicitly save through `POST /v1/presenter/compose-sessions`
4. receive analyzer-generated `session_id`
5. fresh-navigate to a `sessionId` URL
6. reopen through:
   - `GET /v1/presenter/compose-sessions/{session_id}?consumer_key=transient-proof-harness`
7. render from saved session truth only

Reopen must show:

- zero second `POST /v1/presenter/compose-from-selection`
- zero `POST /v1/presenter/compose-from-intent`
- zero hidden in-memory fallback
- one saved-session fetch path

Save-call discipline must be explicit:

- the harness must send the analyzer-owned `persistable_intent_request` from the response
- it must not send the original `ComposeFromSelectionRequest` fixture to the save seam
- it must include truthful provenance:
  - `planning_decision_id`
  - `source_v2_job_id`

### 5. Freeze a bounded proof family

Freeze one AOI source-selection lifecycle proof family under the real execution date, at minimum:

- saved-session JSON summary
- reopen-segment JSON summary
- full HAR
- rendered screenshot
- invalid-session JSON summary

That proof family should record:

- exact original `ComposeFromSelectionRequest`
- exact analyzer-owned lowered request used for save
- whether saved `compose_request` equals that analyzer-owned lowered request exactly
- `planning_decision_id`
- `source_v2_job_id`
- analyzer-generated `session_id`
- reopened `presentation_hash`
- reopened `presentation_content_hash`
- reopened `resolver_version`
- zero second compose calls on reopen

## Acceptance Bar

This slice should count as complete only if all of the following are true:

1. the standalone harness can compose the pinned AOI `source_selection` case under `consumer_key=transient-proof-harness`

2. the analyzer exposes exact analyzer-owned lowered request truth for that composed source-selection response

3. the harness saves that exact lowered request plus exact raw compose response through the existing analyzer-owned save seam

4. save includes truthful provenance:
- `planning_decision_id`
- `source_v2_job_id`

5. the analyzer returns analyzer-generated `session_id`

6. the harness surfaces `session_id` as lifecycle identity and keeps planning/job ids as provenance only

7. fresh-navigation reopen succeeds through:
- `GET /v1/presenter/compose-sessions/{session_id}?consumer_key=transient-proof-harness`

8. reopen shows:
- zero second `POST /v1/presenter/compose-from-selection`
- zero `POST /v1/presenter/compose-from-intent`
- zero hidden in-memory fallback

9. the reopened payload preserves saved truth exactly enough to verify:
- `consumer_key`
- `workflow_key`
- `presentation_hash`
- `presentation_content_hash`
- `resolver_version`

10. invalid `session_id` fails closed

11. existing `direct_sections` lifecycle proof remains intact in parallel

12. this slice does not widen:
- `source_profile`
- proof-only consumer identity again
- generic save-schema unions by default
- host-local lowered-request synthesis

## Out Of Scope

This slice should not:

- broaden lifecycle to `source_profile`
- broaden lifecycle to `transient-proof-probe`
- create a generic request-family union over all save shapes unless review proves no smaller honest bridge exists
- turn the harness into a productized saved-session browser
- reopen AOI/non-AOI consumer generality questions

## Honest Claim If Completed

If this slice closes honestly, the claim should remain narrow:

- the standalone proof-only harness can now carry one fixed AOI `source_selection` lifecycle proof by relying on one analyzer-owned persistable lowered intent-request field plus the existing analyzer-owned save/reopen seam, without host-local reconstruction

It would not yet mean:

- lifecycle is generalized across all compose request families
- source-profile lifecycle is solved
- generic saved-session architecture now exists
- the public save seam is fully abstracted from request-family shape

## Why This Is The Next Honest Step

After direct-sections lifecycle closes on the proof-only harness, the remaining open transient family on that same harness is AOI `source_selection`.

That makes this the next honest question:

- not because AOI deserves priority by itself
- but because it is the smallest remaining lifecycle broadening step on the exact same host line

It is also the right contractual next step:

- the current save seam is still intent-shaped
- `compose_from_selection()` already creates the lowered request internally
- the remaining missing law is how that exact analyzer-owned lowered request becomes persistable truth for lifecycle, without making the harness fake it

If this slice closes honestly, the next broader question after it would be:

- whether source-backed `source_profile` lifecycle should be attempted at all on the proof-only line, or whether lifecycle broadening should stop until a cleaner generalized save contract exists
