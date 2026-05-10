# Proof: Phase E AOI Canary Source-Profile Comparison Live Closeout

Date: 2026-03-31

## Claim Closed

This proof closes the live documentary bar for the bounded second-consumer AOI `source_profile` comparison path on:

- consumer:
  - `aoi-canary`
- profile:
  - `comparison`
- pinned source job:
  - `job-744edf255ad5`
- route:
  - `POST /v1/presenter/compose-from-source`
- host mode:
  - `transient_proof`

The earlier frozen analyzer proof at:

- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_profile_comparison_2026-03-31.json`

proved the widened contract on the direct analyzer seam.

This proof is different:

- it is a real browser/network capture of the canary consuming that same path live

## Environment

- analyzer base URL:
  - `http://127.0.0.1:8011`
- canary URL:
  - `http://127.0.0.1:4174/`
- canary serve mode:
  - `vite preview` over a production-built bundle
- canary app mode:
  - `transient_proof`
- capture boundary:
  - `from source_profile:comparison selector click through ready rendered state`

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

- `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-profile-comparison.json`

Fixture identity:

- `proof_fixture_key = phase_e_aoi_canary_source_profile_comparison_v1`
- `proof_bundle_identity = communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_profile_comparison_2026-03-31.json`
- `consumer_key = aoi-canary`
- `profile = comparison`
- `source_v2_job_id = job-744edf255ad5`

## Result

The live closeout passed.

Recorded outcome from the frozen JSON summary:

- `response_status = 200`
- `resolver_version = compose-from-source-v3`
- `observed_request_json_equals_pinned_fixture_request = true`
- `compose_request_count_in_session = 1`
- `root_renderer_type = tab`
- `raw_json_leaf_keys = ["compose_intent_03_aoi_thematic_report"]`
- `workflow_key = anxiety_of_influence_thematic_single_thinker`
- `consumer_key = aoi-canary`
- `style_school = explanatory_narrative`
- `view_count = 4`

This means the live browser session preserved the exact bounded adaptation-quality law pinned for the comparison preset:

- root renderer stayed `tab`
- no root `raw_json`
- exactly one `raw_json` leaf
- that leaf was the exact comparison closeout view:
  - `compose_intent_03_aoi_thematic_report`

## Thin-Host Audit

The live proof makes the thin-host claim auditable for the `source_profile:comparison` selector switch.

Observed analytical request seam:

- one real `POST /v1/presenter/compose-from-source`

Observed forbidden analytical seams:

- `[]`

Specifically not observed in the captured success path:

- `route-task`
- `plan-task`
- planning-snapshot fetch
- `compose-from-selection`
- `compose-from-intent`

Observed non-analytical supporting requests:

- [
  {
    "method": "GET",
    "url": "http://localhost:8001/v1/styles/tokens/explanatory_narrative",
    "status": 0
  }
]

That supporting request does not weaken the thin-host claim. It is a presentation-support fetch and is disclosed here explicitly rather than silently omitted.

## Capture Notes

The canary intentionally preserves `source_selection` as the default transient proof case. To keep that earlier proof intact while isolating this new `source_profile:comparison` closeout, the browser/network capture starts at the explicit selector switch into `source_profile:comparison` rather than from full page load.

That means this artifact proves exactly the new broadened comparison seam without weakening either of the already-closed paths:

- `source_selection`
- `source_profile:dossier`

## Frozen Artifact Set

- analyzer proof bundle:
  - `/home/evgeny/projects/analyzer-v2/communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_profile_comparison_2026-03-31.json`
- JSON summary:
  - `/home/evgeny/projects/analyzer-v2/communications/PROOF_phase_e_aoi_canary_source_profile_comparison_live_closeout_2026-03-31.json`
- screenshot:
  - `/home/evgeny/projects/analyzer-v2/communications/PROOF_phase_e_aoi_canary_source_profile_comparison_live_closeout_2026-03-31.png`
- HAR-equivalent network capture:
  - `/home/evgeny/projects/analyzer-v2/communications/PROOF_phase_e_aoi_canary_source_profile_comparison_live_closeout_2026-03-31.har`

## Conclusion

The bounded `aoi-canary` second-consumer surface now live-proves the full currently supported AOI transient compose family set:

- AOI `source_selection`
- AOI `source_profile` with `profile = dossier`
- AOI `source_profile` with `profile = comparison`

The honest closed claim for this slice is:

- analyzer-v2 can serve the live AOI `source_profile:comparison` transient compose path to `aoi-canary`
- the canary consumes that response through the same thin field-only host adapter discipline
- the exact wire request matches the pinned analyzer-owned `ComposeFromSourceRequest` comparison fixture
- no hidden analytical upstream calls are needed beyond the intended `compose-from-source` seam during the captured proof window
