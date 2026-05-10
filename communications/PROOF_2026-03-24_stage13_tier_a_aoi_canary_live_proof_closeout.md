# Proof: Stage 13 Tier A / AOI Canary Live Proof Closeout

Date: 2026-03-24
Program: Dynamic Bespoke Apps Platformization
Scope memo: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`
Completion memo: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`

## Summary

Stage 13 Tier A is now documentary-closed.

`aoi-canary` was run live as a second consumer against the local analyzer instance in discovery-first mode, and the proof artifacts show the bounded acceptance seam:

1. `GET /v1/results/discovery`
2. `GET /v1/results/by-job/{job_id}`
3. `GET /v1/results/by-job/{job_id}/presentation`

The ready-state capture shows the canary rendering the AOI dossier surface without unsupported-renderer fallback, and the negative-state capture shows `discovery_empty` with no silent artifact fallback and no hidden `presenter/page` substitution.

This closes the Tier A result-contract seam proof.

It does **not** close Stage 13 overall.

## Proof Environment

- Analyzer URL:
  - `http://127.0.0.1:8001`
- Canary URL:
  - `http://127.0.0.1:4174/`
- Canary mode:
  - production `vite build` + `vite preview`
  - `VITE_AOI_MODE=live`
- Acceptance scope:
  - `project_id=round5-proof-dossier-final-1774100000`
  - `workflow_key=anxiety_of_influence_thematic_single_thinker`
  - `consumer_key=aoi-canary`
  - no `selected_source_thinker_id`
- Negative proof scope:
  - `project_id=round5-proof-dossier-final-1774100000-empty`
  - same AOI workflow and consumer key

`attach-project` was **not** needed.

The local proof job was already discoverable:

- `proof-round5-adaptive-aoi-dossier-final-1774100000`

## Ready-State Evidence

Artifacts:

- browser-network artifact:
  - `communications/PROOF_stage13_tier_a_aoi_canary_ready_session_2026-03-24.har`
- extracted request/response summary:
  - `communications/PROOF_stage13_tier_a_aoi_canary_ready_requests_2026-03-24.json`
- UI screenshot:
  - `communications/PROOF_stage13_tier_a_aoi_canary_ready_state_2026-03-24.png`

Observed acceptance request chain from the actual canary session:

1. `GET /v1/results/discovery?project_id=round5-proof-dossier-final-1774100000&workflow_key=anxiety_of_influence_thematic_single_thinker&consumer_key=aoi-canary&limit=1`
2. `GET /v1/results/by-job/proof-round5-adaptive-aoi-dossier-final-1774100000?consumer_key=aoi-canary`
3. `GET /v1/results/by-job/proof-round5-adaptive-aoi-dossier-final-1774100000/presentation?consumer_key=aoi-canary`

Observed non-blocking secondary debug requests:

- `GET /v1/presenter/trace/proof-round5-adaptive-aoi-dossier-final-1774100000?consumer_key=aoi-canary`
- `GET /v1/presenter/status/proof-round5-adaptive-aoi-dossier-final-1774100000?consumer_key=aoi-canary`

Observed absence:

- no `GET /v1/presenter/page/*` request on the ready-state success path

Rendered ready-state facts from the capture:

- state:
  - `Live result loaded`
- project:
  - `round5-proof-dossier-final-1774100000`
- workflow:
  - `anxiety_of_influence_thematic_single_thinker`
- resolved job:
  - `proof-round5-adaptive-aoi-dossier-final-1774100000`
- result:
  - `ready`
- restore:
  - `available`
- views:
  - `5`

## Negative-State Evidence

Artifacts:

- browser-network artifact:
  - `communications/PROOF_stage13_tier_a_aoi_canary_discovery_empty_session_2026-03-24.har`
- extracted request/response summary:
  - `communications/PROOF_stage13_tier_a_aoi_canary_discovery_empty_requests_2026-03-24.json`
- UI screenshot:
  - `communications/PROOF_stage13_tier_a_aoi_canary_discovery_empty_state_2026-03-24.png`

Observed negative-state request:

1. `GET /v1/results/discovery?project_id=round5-proof-dossier-final-1774100000-empty&workflow_key=anxiety_of_influence_thematic_single_thinker&consumer_key=aoi-canary&limit=1`

Observed response:

- `200 OK`
- empty JSON array

Observed UI state:

- state:
  - `No discoverable AOI result found`
- strategy summary:
  - `No completed AOI result is discoverable for project round5-proof-dossier-final-1774100000-empty and workflow anxiety_of_influence_thematic_single_thinker.`
- resolved job:
  - `pending`
- no artifact-backed AOI page rendered
- no `presenter/page` request issued

This is the stronger negative proof path the scope memo preferred:

- `discovery_empty`

not merely:

- `config_missing`

## Quality Boundary

This proof closes the result-contract seam, not a stronger preparation-quality or polish-quality claim.

The local round-5 dossier proof target is a proof-fixture-backed result:

- `presentation_runs.status = completed`
- `presentation_runs.stats = {"proof_fixture": true, "round": 5}`
- `presentation_artifacts` count for the round-5 AOI proof jobs: `0`
- `polish_cache` count for the round-5 AOI proof jobs: `0`

So the correct reading is:

- the second-consumer contract seam is proved
- analyzer discovery/manifest/presentation truth is proved
- bounded AOI rendering in the second consumer is proved
- stronger preparation/polish quality is **not** what this proof demonstrates

## Verification

Reran after live proof capture:

- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
- `npm --prefix /home/evgeny/projects/aoi-canary run test`
- `PYTHONPATH=. pytest -q tests/test_aoi_canary_contract.py`

Result:

- canary type-check passed
- canary tests: `13` passed
- analyzer canary contract test: `1` passed

Residual warning:

- existing Pydantic deprecation warning in the analyzer-side test run

## Strategic Result

The cheap honest second-consumer bar is now actually closed for the bounded Tier A slice:

- a separate consumer
- discovery-first
- analyzer-owned result contracts
- no workflow-specific analytical reconstruction in the consumer
- explicit negative-state behavior instead of silent artifact fallback

The honest remaining ledger is:

- Stage 13 Tier A: closed
- Stage 13 overall: still partial
- Tier B transient/stronger host-neutral proof: still open

So the main structural next phase can now move on to:

- AOI exemplar completion
