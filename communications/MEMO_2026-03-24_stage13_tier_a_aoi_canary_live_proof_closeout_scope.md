# Memo: Stage 13 Tier A / AOI Canary Live Proof Closeout Scope

Date: 2026-03-24
Status: Draft scope memo
Program: Dynamic Bespoke Apps Platformization
Prior scope: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_scope.md`
Prior completion: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Summary

The `aoi-canary` Tier A implementation is now landed, but Tier A is not yet fully closed.

The remaining gap is narrower than architecture and narrower than a new platform tranche:

- obtain or prepare one discoverable AOI proof result under a real `project_id`
- run the canary live against analyzer-v2 in discovery-first mode
- capture the bounded evidence that a second consumer really uses:
  - `result_discovery`
  - `result_manifest`
  - `result_presentation`
- capture at least one honest negative state showing that live-mode failure does not silently fall back to artifact content

This is a proof-closeout step, not a new architecture stage.

One important boundary should stay explicit during closeout:

- this proof is meant to demonstrate the second-consumer result-contract seam
- it is not meant to prove full upstream preparation/polish quality unless the chosen proof job actually carries that quality signal

## Why This Is The Next Honest Step

The code is in place:

- `aoi-canary` now uses a result-contract-first live path
- the live state machine is explicit
- canary tests and analyzer-side contract coverage pass

But the roadmap bar for Tier A was never “local tests only.”

Tier A was supposed to prove that a second consumer can discover and render a real AOI result through analyzer-owned result contracts without rebuilding analytical truth locally.

That requires live evidence, not only implementation and local verification.

So the next step should be:

- close the live proof tail cleanly

not:

- reopen architecture
- jump to transient second-consumer work
- or move the main line fully to AOI exemplar completion as if Tier A were already documentary-closed

## Bounded Claim

The bounded claim for this closeout step is:

- `aoi-canary` can operate as a second consumer over the analyzer result contract seam for one real AOI proof path, and when that proof path is missing or blocked it fails explicitly rather than silently masking the failure with artifact content

This step does **not** claim:

- transient second-consumer support
- Host Contract v1/runtime reuse across apps
- task-launch adoption in `aoi-canary`
- lifecycle law
- a general second-consumer platform proof beyond the bounded AOI result-backed seam

## Scope Decisions

### Decision 1: This is evidence capture, not new architecture

Do not widen this step into:

- another `aoi-canary` refactor
- shared package extraction
- transient route work
- task-launch work

Code changes should be limited to small compatibility or proof-surface fixes only if the live run exposes a real mismatch.

### Decision 2: Proof path is discovery-first

The acceptance path is:

1. resolve effective `project_id` and AOI `workflow_key`
2. call `GET /v1/results/discovery?project_id=...&workflow_key=...&consumer_key=aoi-canary&limit=1`
3. use the selected job from analyzer ordering
4. call `GET /v1/results/by-job/{job_id}`
5. if manifest truth allows it, call `GET /v1/results/by-job/{job_id}/presentation`
6. render the returned AOI surface in `aoi-canary`

Manual `job_id` may remain available for debugging, but it does not count as Tier A proof closure.

### Decision 3: Negative proof is required

At least one explicit negative path should be captured as part of closeout.

Acceptable bounded options:

- `config_missing` with discovery-first mode and no `project_id`
- `discovery_empty` using a debug `project_id` / `workflow_key` combination that returns no rows
- `manifest_unavailable` if the selected result is legitimately non-restorable
- `presentation_error` if a real compatible failure case exists

The point is to prove the state model honestly:

- no silent artifact fallback
- no hidden presenter-page substitution

### Decision 4: Proof data prep is out-of-band but explicit

If the intended AOI proof result is not discoverable under the chosen `project_id`, the allowed data-prep move is:

- `POST /v1/results/by-job/{job_id}/attach-project`

This should be treated as bounded one-time pre-proof setup only:

- not part of the acceptance seam
- not part of `aoi-canary` product logic
- not repeated as part of the proof itself unless the memo explains why the proof data had to be attached first

### Decision 5: Thinker-scoped proof is optional but must be explicit if used

Tier A acceptance does not require a thinker-scoped discovery path.

But if the proof is intended to reproduce a specific pinned thinker experience, then the closeout must record that explicitly and keep the scope honest:

- record the effective `selected_source_thinker_id`
- show it in the discovery request artifact
- make clear that the proof is still AOI result-backed Tier A, just with one extra bounded discovery filter

If no thinker filter is used, the closeout should say so explicitly.

### Decision 6: Keep the AOI acceptance path narrow

Tier A closure should still count only the bounded AOI workflow proof path:

- `consumer_key=aoi-canary`
- AOI workflow key
- discovery-first
- read-only
- result-backed

Debug overrides are fine for diagnosis, but they do not expand what Tier A means.

## Proposed Deliverables

### 1. Real proof data and scope record

Record the exact live proof inputs used:

- analyzer base URL
- `project_id`
- effective `workflow_key`
- effective `selected_source_thinker_id`, if any
- chosen proof job after discovery
- whether `attach-project` was needed
- whether the chosen proof job represents raw phase-output restore or a more fully prepared/polished result path

### 2. Saved discovery/manifest/presentation evidence

Save bounded evidence showing:

- discovery response for the proof path
- standalone manifest response for the chosen job
- presentation response metadata for the chosen job
- request-level artifacts for all three calls:
  - actual request URLs or curl commands
  - consumer key used
  - any discovery filters used
  - timestamps or equivalent traceable capture context

This can be saved as:

- curl output
- JSON snippets
- screenshots of the debug panel plus browser state

as long as the seam is clear and reproducible.

### 3. Saved UI proof for the ready state

Capture a live `aoi-canary` screenshot or equivalent evidence showing:

- effective scope
- resolved `job_id`
- result-backed render path is active
- AOI surface rendered without unsupported-renderer fallback

### 4. Saved UI proof for one negative state

Capture one live negative state that proves:

- the app did not silently fall back to artifact content
- the result-contract-first state machine is actually visible in product behavior

The negative proof should also include the triggering request context, not only the screenshot, so future review can tell whether the failure came from:

- missing config
- empty discovery
- manifest-unavailable truth
- or a real presentation error

### 5. Closeout memo/proof note

Save one proof note or closeout memo that links:

- the live inputs
- the captured outputs
- the bounded claim being closed
- the exact request-level evidence set
- whether `attach-project` was needed as one-time setup
- whether the proof demonstrates contract-seam correctness only or also stronger preparation quality
- any residual gap that still keeps Stage 13 itself partial

## Verification Expectations

This closeout step should rerun only the bounded checks relevant to proof confidence:

- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
- `npm --prefix /home/evgeny/projects/aoi-canary run test`
- `PYTHONPATH=. pytest -q tests/test_aoi_canary_contract.py`

If a small compatibility fix is required during proof closeout, rerun those checks after the fix.

## Non-Goals

- no transient second-consumer work
- no `result_refresh`
- no `route-task` / `plan-task` adoption in `aoi-canary`
- no Host Contract runtime extraction into a shared package
- no AOI exemplar-loop work yet
- no lifecycle reopening

## Draft Judgment

The immediate next step is a bounded Tier A live proof closeout, not a broader architecture tranche.

Once that closeout exists, the main structural next phase can move cleanly to:

- AOI exemplar completion

But skipping the live proof step would leave Tier A only code-complete, not actually proved.
