# Round 11 Proof: AOI Bounded Compose-From-Intent

Date: 2026-03-22

## Scope

Round 11 closes one bounded claim:

- analyzer-v2 can accept a small AOI intent + prose envelope and return a valid transient render-ready page
- the route is stateless:
  - no job creation
  - no plan creation
  - no view-registry writes
  - no `presentation_cache` writes
- the route reuses the existing presenter / transformation / consumer-adaptation seams instead of introducing consumer-specific UI logic

The new endpoint is:

- `POST /v1/presenter/compose-from-intent`

The bounded v1 scope remains:

- AOI-only:
  - `workflow_key = anxiety_of_influence_thematic_single_thinker`
- consumer-only:
  - `consumer_key = the-critic`
- flat-page only:
  - one generated top-level view per input prose section
  - no generated children
  - no `tab` renderer

## What Was Built

Round 11 added:

- a new transient orchestration module:
  - `src/presenter/compose_from_intent.py`
- new transient presenter schemas:
  - `ComposeFromIntentRequest`
  - `TransientIntentView`
  - `TransientIntentPagePresentation`
  - `ComposeFromIntentResponse`
- a new presenter route:
  - `POST /v1/presenter/compose-from-intent`

The route now performs five bounded stages:

1. request validation
2. page planning
3. sequential per-section generation + transformation
4. consumer adaptation
5. final renderer-contract validation

The route also now has its own explicit resolver version:

- `compose-from-intent-v1`

and its own dependency-unavailable path:

- `503` for LLM dependency unavailability

## Automated Verification

Focused backend regression:

- `PYTHONPATH=. pytest tests/test_compose_from_intent.py tests/test_presentation_api.py tests/test_manifest_trace.py tests/test_analysis_product_contract.py -q`
- result:
  - `182 passed, 13 warnings`

Python compile check:

- `python -m py_compile src/presenter/compose_from_intent.py src/presenter/dynamic_prompt.py src/views/generator.py src/presenter/schemas.py src/presenter/renderer_contract_enforcement.py src/api/routes/presenter.py tests/test_compose_from_intent.py`
- result:
  - clean

Focused frontend compatibility verification:

- `cd /home/evgeny/projects/the-critic/webapp && CI=true npm test -- --watch=false src/components/ViewRenderer.test.tsx`
- result:
  - `1 suite passed`
  - `5 tests passed`

That frontend run is intentionally narrow:

- round 11 does not ship runtime product integration in the-critic
- it only proves that transient returned views can render through the existing generic `ViewRenderer` path without new runtime overrides

## Proof Inputs

Round 11 reused the documentary AOI proof jobs already used in rounds 9 and 10:

- `proof-round5-adaptive-aoi-dossier-final-1774100000`
- `proof-round5-adaptive-aoi-comparison-final-1774100000`

The prose inputs for closure were loaded directly from `phase_outputs` via:

- `load_all_job_outputs(job_id, include_content=True)`

Closure then invoked the public presenter route function directly:

- `asyncio.run(compose_from_intent_endpoint(request_payload))`

This is sufficient for round 11 because the tranche is backend-first:

- there is no browser/UI runtime integration in scope
- the route contract itself is what is being proved

Saved proof artifacts:

- `communications/PROOF_round11_dossier_request_2026-03-22.json`
- `communications/PROOF_round11_dossier_response_2026-03-22.json`
- `communications/PROOF_round11_dossier_trace_2026-03-22.json`
- `communications/PROOF_round11_dossier_generated_views_2026-03-22.json`
- `communications/PROOF_round11_comparison_request_2026-03-22.json`
- `communications/PROOF_round11_comparison_response_2026-03-22.json`
- `communications/PROOF_round11_comparison_trace_2026-03-22.json`
- `communications/PROOF_round11_comparison_generated_views_2026-03-22.json`
- `communications/PROOF_round11_compose_from_intent_verification_2026-03-22.json`

## Dossier-Like Closure Run

- source job:
  - `proof-round5-adaptive-aoi-dossier-final-1774100000`
- request shape:
  - 2 prose sections
  - `aoi_thematic_synthesis`
  - `aoi_thematic_report`
- result:
  - `200`
  - `view_count = 2`
  - `style_school = explanatory_narrative`
  - `resolver_version = compose-from-intent-v1`
- saved served order:
  - `compose_intent_01_aoi_thematic_synthesis`
  - `compose_intent_02_aoi_thematic_report`
- saved served renderer types:
  - `accordion`
  - `accordion`
- saved trace stages:
  - `page_plan`
  - `view_generation`
  - `transformation_execution`
  - `consumer_adaptation`
  - `contract_validation`
- proof checks:
  - served order matches normalized generated definition order
  - final route response is contract-valid
  - no `409` issues were emitted

## Comparison-Like Closure Run

- source job:
  - `proof-round5-adaptive-aoi-comparison-final-1774100000`
- request shape:
  - 3 prose sections
  - `aoi_engagement_mapping`
  - `aoi_sin_findings`
  - `aoi_thematic_report`
- result:
  - `200`
  - `view_count = 3`
  - `style_school = explanatory_narrative`
  - `resolver_version = compose-from-intent-v1`
- saved served order:
  - `compose_intent_01_aoi_engagement_mapping`
  - `compose_intent_02_aoi_sin_findings`
  - `compose_intent_03_aoi_thematic_report`
- saved served renderer types:
  - `card_grid`
  - `accordion`
  - `prose`
- saved trace stages:
  - `page_plan`
  - `view_generation`
  - `transformation_execution`
  - `consumer_adaptation`
  - `contract_validation`
- proof checks:
  - served order matches normalized generated definition order
  - final route response is contract-valid
  - no `409` issues were emitted

## Important Proof Note

Round 11 is generative.

That means the exact pattern mix is not the proof claim, and it is not guaranteed to be stable across independent reruns.

What is fixed and proved on the saved closure runs is:

1. the route accepts the bounded AOI request shape
2. planner output is normalized into deterministic transient keys and positions
3. final served order matches planner order after normalization
4. final served views remain inside the bounded generic renderer family
5. final served payloads pass renderer-contract validation
6. the route returns the narrowed transient non-job-backed response shape

The saved artifacts above are therefore the authoritative documentary closure for round 11.

## Proof Conclusion

Round 11 is closed on its actual bounded claim.

What is now proved:

1. analyzer-v2 can compose a transient AOI page directly from intent + prose without creating a job
2. the route can orchestrate existing planner, generation, transformation, consumer-adaptation, and renderer-law seams without route-to-route HTTP
3. the external response can stay honest and non-job-backed
4. final contract failures reuse the existing bounded-composition issue envelope instead of inventing a new dialect
5. the generated-view layer is normalized deterministically even though the planning/generation path is generative

What round 11 did not prove:

1. browser/UI product integration of the transient page contract
2. genealogy compose-from-intent
3. `tab` or child-view planning
4. persisted draft creation
5. deterministic repeatability of exact pattern choice across reruns
