# Proof: Phase E Transient Second-Consumer AOI Canary Source-Selection Live Closeout

Date: 2026-03-31

## Claim Closed

This proof closes the live documentary bar for the already-landed bounded second-consumer transient path:

- consumer:
  - `aoi-canary`
- path:
  - AOI `source_selection`
- route:
  - `POST /v1/presenter/compose-from-selection`
- host mode:
  - `transient_proof`

The earlier artifact at:

- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json`

was an honest deterministic replay surface.

This proof is different:

- it is a real browser/network capture over the landed path

## Environment

- analyzer base URL:
  - `http://127.0.0.1:8011`
- canary URL:
  - `http://127.0.0.1:4174/`
- canary serve mode:
  - `vite preview` over a production-built bundle
- canary app mode:
  - `transient_proof`
- fresh-session HAR definition:
  - full page load into `transient_proof` through the rendered ready state

Repo state at capture time:

- analyzer-v2 commit:
  - `01427880e1c4c5ddb896b8b0c7fb8c74f6b228c9`
- analyzer-v2 repo state:
  - `DIRTY`
- aoi-canary commit:
  - `c356e360814b2acd8f0177ffd9e96ebe17009f1c`
- aoi-canary repo state:
  - `DIRTY`

## Pinned Input

The live session replayed the committed analyzer-owned request fixture:

- `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-selection.json`

Fixture identity:

- `proof_fixture_key = phase_e_transient_second_consumer_aoi_source_selection_v1`
- `proof_bundle_identity = communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json`
- `planning_decision_id = planning-decision-d6b6bb0cd7ac`

## Result

The live closeout passed.

Recorded outcome from the frozen JSON summary:

- `response_status = 200`
- `resolver_version = compose-from-selection-v1`
- `observed_request_json_equals_pinned_fixture_request = true`
- `compose_request_count_in_session = 1`
- `root_renderer_type = tab`
- `raw_json_leaf_keys = ["compose_intent_04_aoi_thematic_report"]`
- `workflow_key = anxiety_of_influence_thematic_single_thinker`
- `consumer_key = aoi-canary`
- `style_school = explanatory_narrative`
- `view_count = 5`

This means the live browser session preserved the same bounded adaptation-quality law already enforced in tests:

- root renderer stayed `tab`
- no root `raw_json`
- exactly one `raw_json` leaf
- that leaf was the closeout/report view only

## Thin-Host Audit

The live proof makes the thin-host claim auditable.

Observed analytical request seam:

- one real `POST /v1/presenter/compose-from-selection`

Observed forbidden analytical seams:

- none

Specifically not observed in the captured success path:

- `route-task`
- `plan-task`
- planning-snapshot fetch
- `compose-from-source`
- `compose-from-intent`

Observed non-analytical supporting request:

- one style-token fetch:
  - `GET http://localhost:8001/v1/styles/tokens/explanatory_narrative`

That request is presentation/support traffic, not analytical reconstruction traffic.
It does not weaken the bounded thin-host claim.

## Capture Notes

One earlier live-browser attempt on the Vite dev server was intentionally not used as the closeout artifact because React development behavior caused duplicate compose requests on page load.

To keep the closeout on the exact same code path while removing development-only duplication noise, the final proof was captured from:

- the same canary code
- the same pinned fixture
- the same analyzer route
- but served through `vite preview` on a production-built bundle

That preserved the proof target while yielding one clean browser session with one real compose POST.

## Frozen Artifact Set

- JSON summary:
  - `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-31.json`
- screenshot:
  - `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-31.png`
- HAR:
  - `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-31.har`

## Conclusion

The bounded second-consumer transient path is now live-proved, not only test-proved.

The honest closed claim is:

- analyzer-v2 can serve one bounded AOI `source_selection` transient compose path to `aoi-canary`
- the canary consumes that response through a thin field-only host adapter
- the exact wire request matches the pinned analyzer-owned fixture
- no hidden analytical upstream calls are needed beyond the intended compose seam

This closes the documentary/live-proof gap left open by the March 30 implementation completion memo.
