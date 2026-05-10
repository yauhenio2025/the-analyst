# Memo: Stage 13 Tier A / AOI Canary Second-Consumer Completion

Date: 2026-03-24
Scope Memo: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_scope.md`
Program: Dynamic Bespoke Apps Platformization

## Summary

The bounded `aoi-canary` Tier A implementation is complete.

`aoi-canary` no longer depends on `presenter/page` as its primary live seam. It now uses analyzer-owned result contracts in this order:

1. `GET /v1/results/discovery`
2. `GET /v1/results/by-job/{job_id}`
3. `GET /v1/results/by-job/{job_id}/presentation`

This gives the program a real result-backed second-consumer implementation over analyzer-native result discovery, manifest truth, and presentation truth.

Tier A is now documentary-closed as well:

- the live proof artifact set against project-attached AOI data has been captured
- the ready-state seam is proved from the real canary session
- one stronger negative state (`discovery_empty`) is also proved

## What Landed

In `/home/evgeny/projects/aoi-canary`:

- `src/App.tsx`
  - live mode is now result-contract-first rather than presenter-page-first
  - live state is reducer-driven and explicit
  - manual `job_id` remains a debug-only bypass, not the proof path
  - no silent artifact fallback occurs when live result-contract fetches fail
- `src/lib/resultsClient.ts`
  - small typed client for:
    - discovery
    - manifest
    - presentation
- `src/types/results.ts`
  - bounded local types for the analyzer result-contract fields the canary actually consumes
- `src/test/App.test.tsx`
  - state-machine, discovery-scope, failure-state, and no-fallback coverage
- `src/test/resultsClient.test.ts`
  - request-shaping coverage for discovery, manifest, and presentation
- `README.md`
  - live-mode env and URL override documentation

## Behavioral Outcome

Live mode now behaves as follows:

- discovery-first mode:
  - resolves effective `project_id` and `workflow_key`
  - discovers the latest completed AOI result by analyzer ordering with `limit=1`
  - fetches standalone manifest first
  - only fetches presentation if manifest truth says the result is restorable and completed
- manual debug `job_id` mode:
  - bypasses discovery
  - still uses `manifest -> presentation`
  - does not require `project_id`
- debug presenter calls:
  - `trace/status` remain secondary and non-blocking
  - they no longer define live-mode success

State handling is now explicit rather than implicit:

- `config_missing`
- `discovering`
- `discovery_empty`
- `discovery_error`
- `loading_manifest`
- `manifest_error`
- `manifest_unavailable`
- `loading_presentation`
- `presentation_error`
- `ready`

The app also now preserves manifest truth when presentation fetch fails, including:

- resolved `job_id`
- effective discovery scope
- restore/result-state fields
- presentation error detail

## Post-Review Closeout

Two follow-up issues were found after the first implementation pass and then fixed:

1. stale live data could remain visible for a paint when switching into live mode or changing the debug `job_id`
2. the non-blocking `trace/status` behavior existed in code but did not yet have focused test coverage

Closeout changes:

- live reducer state is now cleared synchronously when:
  - entering discovery-first live mode
  - changing the manual debug `job_id`
- the reset path is mode-correct:
  - discovery-first goes directly to `discovering`
  - manual debug mode goes directly to `loading_manifest`
  - `config_missing` only applies to discovery mode without `project_id`
- `src/test/App.test.tsx` now covers:
  - non-blocking `trace/status` failures
  - immediate disappearance of the prior live page when the debug `job_id` changes

## Verification

Initial implementation verification:

- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
- `npm --prefix /home/evgeny/projects/aoi-canary run test`
- `PYTHONPATH=. pytest -q tests/test_aoi_canary_contract.py`

Result:

- canary type-check passed
- canary tests: `11` passed
- analyzer contract test: `1` passed

Post-review closeout verification:

- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
- `npm --prefix /home/evgeny/projects/aoi-canary run test`

Result:

- canary type-check passed
- canary tests: `13` passed

The analyzer-side canary contract test was not rerun in the post-review closeout because the follow-up changes were canary-only UI/state/test fixes.

## Live Proof Closeout

The documentary gap noted in the first completion pass is now closed.

Live proof artifacts:

- proof note:
  - `communications/PROOF_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout.md`
- proof summary:
  - `communications/PROOF_stage13_tier_a_aoi_canary_live_proof_summary_2026-03-24.json`
- ready-state browser/network artifacts:
  - `communications/PROOF_stage13_tier_a_aoi_canary_ready_session_2026-03-24.har`
  - `communications/PROOF_stage13_tier_a_aoi_canary_ready_requests_2026-03-24.json`
  - `communications/PROOF_stage13_tier_a_aoi_canary_ready_state_2026-03-24.png`
- negative-state browser/network artifacts:
  - `communications/PROOF_stage13_tier_a_aoi_canary_discovery_empty_session_2026-03-24.har`
  - `communications/PROOF_stage13_tier_a_aoi_canary_discovery_empty_requests_2026-03-24.json`
  - `communications/PROOF_stage13_tier_a_aoi_canary_discovery_empty_state_2026-03-24.png`

What the live proof demonstrates:

- `aoi-canary` issues the real acceptance chain itself:
  - `result_discovery`
  - `result_manifest`
  - `result_presentation`
- `consumer_key=aoi-canary` is carried through the second-consumer seam
- no `presenter/page` request appears on the ready-state success path
- `trace/status` remain secondary and non-blocking
- `discovery_empty` produces an explicit live error state without silent artifact fallback

The local proof target used for closeout was:

- analyzer:
  - `http://127.0.0.1:8001`
- canary preview:
  - `http://127.0.0.1:4174/`
- project:
  - `round5-proof-dossier-final-1774100000`
- workflow:
  - `anxiety_of_influence_thematic_single_thinker`
- resolved job:
  - `proof-round5-adaptive-aoi-dossier-final-1774100000`

`attach-project` was not needed.

Quality boundary:

- this closes the result-contract seam proof
- it does not claim stronger preparation/polish quality for the local round-5 fixture-backed proof target

## Boundaries

This tranche remains bounded:

- read-only only
- result-backed only
- AOI-only for acceptance
- no `result_refresh`
- no transient adoption in `aoi-canary`
- no Host Contract v1/runtime extraction into a shared cross-app package
- no lifecycle reopening

It also remains honest about what is still missing:

- Stage 13 Tier B remains completely open
- transient second-consumer proof remains open
- broader host-neutral proof remains open

## Status

The correct ledger is:

- `Stage 13 = Partial`
- Stage 13 Tier A implementation: landed
- Stage 13 Tier A documentary/live proof closeout: complete

So the main structural next step can now move on cleanly to the AOI exemplar-completion tranche while keeping Stage 13 overall partial until Tier B is earned.
