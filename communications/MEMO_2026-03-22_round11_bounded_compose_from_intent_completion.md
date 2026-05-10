# Memo: Round 11 / Bounded Compose-From-Intent Completion

Date: 2026-03-22
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_scope.md`

## Purpose

Record the actual outcome of round 11.

This note closes the gap between:

- the round-11 scope memo
- the implemented transient compose-from-intent route
- the focused verification and documentary proof that now exist in the repo

## Bounded Claim Closed In Round 11

Round 11 proved one bounded thing:

- analyzer-v2 can accept a bounded AOI intent + prose envelope and return a transient render-ready page through a new presenter route without creating a job, without persisting generated views, and without requiring new consumer-specific runtime UI logic

The required proof surface remained:

- AOI only
- `consumer_key = the-critic`

The blocked / deferred surface remained:

- genealogy compose-from-intent
- `tab` / hierarchy planning
- persisted draft creation
- product-level frontend adoption of the transient page contract

## What Landed

### New Route And Transient Contract

Round 11 added a new presenter route:

- `POST /v1/presenter/compose-from-intent`

It also added a new transient non-job-backed contract in `src/presenter/schemas.py`:

- `ComposeFromIntentRequest`
- `ComposeFromIntentSectionInput`
- `TransientIntentView`
- `TransientIntentPagePresentation`
- `ComposeFromIntentTrace`
- `ComposeFromIntentResponse`

The route now returns:

- `presentation`
- `generated_view_definitions`
- `trace`

without exposing job-bound fields like:

- `job_id`
- `plan_id`
- `phase_number`
- `prepared_at`
- `raw_prose`

### New Orchestration Seam

Round 11 added the primary new implementation seam in:

- `src/presenter/compose_from_intent.py`

That module now owns the whole bounded v1 flow:

1. request validation
2. page-structure planning
3. sequential section generation + transformation
4. transient assembly
5. consumer adaptation
6. final renderer-contract validation

It also introduced the route’s dedicated resolver/version token:

- `compose-from-intent-v1`

and its dedicated dependency-unavailable path:

- `503` for missing/unavailable LLM dependency

### Deterministic Normalization

Round 11 made generated views deterministic after generation.

The route now overwrites:

- `view_key`
- `position`
- `parent_view_key`
- `target_app`
- `target_page`
- `renderer_type`
- `status`
- `visibility`

using the bounded transient format:

- `compose_intent_{index:02d}_{engine_key_slug}`

This means the generative planner/generator layer can vary while the transient page structure stays stable and auditable.

### Capability-Definition Engine Fallback

The first live proof exposed a real AOI seam:

- the round-11 request uses real AOI proof engines such as `aoi_thematic_synthesis`, `aoi_sin_findings`, and `aoi_thematic_report`
- those are available through capability definitions, not only through the standard engine registry JSONs

Round 11 therefore widened the engine fallback used by the transient route:

- `src/presenter/compose_from_intent.py`
- `src/views/generator.py`
- `src/presenter/dynamic_prompt.py`

That fallback now provides enough engine metadata for:

- request validation
- dynamic prompt composition
- view-generation prompt construction

without widening into a general engine-registry redesign.

### Card-Grid Contract Normalization

The second live proof exposed another real seam:

- `card_grid_grouped` can legitimately use `items_path` to consume grouped arrays from a nested object
- strict renderer-law validation was checking the pre-extraction mixed object instead of the actual served grouped-array shape

Round 11 fixed that in the transient path only:

- `src/presenter/compose_from_intent.py`

The route now normalizes grouped card-grid transient data into the effective served contract shape before final validation.

That keeps round-11 strict contract validation honest without widening round-9 renderer law globally.

## Verification

Focused backend regression:

- `PYTHONPATH=. pytest tests/test_compose_from_intent.py tests/test_presentation_api.py tests/test_manifest_trace.py tests/test_analysis_product_contract.py -q`
- result:
  - `182 passed, 13 warnings`

Focused route-boundary hardening:

- `PYTHONPATH=. pytest tests/test_compose_from_intent.py -q`
- result:
  - `13 passed, 2 warnings`

That focused round-11 file now includes the route-level boundary cases for:

- generic wrapped terminal model failure -> `502`
- wrapped transport / dependency failure -> `503`

Python compile check:

- `python -m py_compile src/presenter/compose_from_intent.py src/presenter/dynamic_prompt.py src/views/generator.py src/presenter/schemas.py src/presenter/renderer_contract_enforcement.py src/api/routes/presenter.py tests/test_compose_from_intent.py`
- result:
  - clean

Focused frontend compatibility verification:

- `cd /home/evgeny/projects/the-critic/webapp && CI=true npm test -- --watch=false src/components/ViewRenderer.test.tsx`
- result:
  - `1 suite passed`
  - `5 tests passed`

Known non-blocking noise remained:

- existing pydantic deprecation warnings
- existing `datetime.utcnow()` deprecation warnings from older executor/result-contract code
- the existing engine-registry load log for an unrelated invalid genealogy engine definition during live proof runs

None blocked the bounded round-11 claim.

## Documentary Proof Closure

Round 11 reused the existing AOI proof jobs as the prose source:

- `proof-round5-adaptive-aoi-dossier-final-1774100000`
- `proof-round5-adaptive-aoi-comparison-final-1774100000`

Saved artifacts:

- `communications/PROOF_round11_dossier_request_2026-03-22.json`
- `communications/PROOF_round11_dossier_response_2026-03-22.json`
- `communications/PROOF_round11_dossier_trace_2026-03-22.json`
- `communications/PROOF_round11_dossier_generated_views_2026-03-22.json`
- `communications/PROOF_round11_comparison_request_2026-03-22.json`
- `communications/PROOF_round11_comparison_response_2026-03-22.json`
- `communications/PROOF_round11_comparison_trace_2026-03-22.json`
- `communications/PROOF_round11_comparison_generated_views_2026-03-22.json`
- `communications/PROOF_round11_compose_from_intent_verification_2026-03-22.json`
- `communications/PROOF_2026-03-22_round11_bounded_compose_from_intent.md`

The saved verification summary confirms for both closure runs:

- `style_school = explanatory_narrative`
- `resolver_version = compose-from-intent-v1`
- final served order matches normalized generated definition order
- final trace stages are:
  - `page_plan`
  - `view_generation`
  - `transformation_execution`
  - `consumer_adaptation`
  - `contract_validation`
- `contract_issue_count = 0`

Important closure note:

- the exact pattern mix is generative and may vary across independent reruns
- the proof claim is therefore bounded to the saved closure runs and the route invariants, not to a fixed canonical renderer sequence

## What Round 11 Now Proves

Round 11 now proves:

1. analyzer-v2 has a real bounded `compose-from-intent` entrypoint rather than only a roadmap placeholder
2. the route can orchestrate planner, generator, transformer, consumer adaptation, and final renderer-law validation without persisting drafts
3. the external response can stay explicitly transient and non-job-backed
4. AOI proof prose can be re-composed into a bounded transient page through the shared generic consumer path
5. final route failures now distinguish:
   - `400` request errors
   - `502` malformed/upstream orchestration failures
   - `503` dependency unavailability
   - `409` final renderer-contract failures

6. the route-level `502` / `503` boundary is now tightened so generic wrapped model failures do not get misclassified as dependency outages

## What Round 11 Did Not Prove

Round 11 did not prove:

1. production frontend adoption of the transient page contract
2. direct drop-in `PagePresentation` compatibility for `V2TabContent`
3. genealogy compose-from-intent
4. child-view planning or `tab` layout
5. persisted draft / job creation from transient pages

## Residual Notes

Two residual limits remain explicit:

1. section work is intentionally sequential in v1; no real thread/offloop fan-out was introduced
2. `llm_extraction_schema` is prompt guidance only in the transient dynamic extraction path; final renderer-law validation remains the authoritative enforcement boundary

Neither blocks the bounded round-11 claim.

## Program Position After Round 11

The roadmap sequence is now materially realized in code:

- round 9: renderer contract enforcement
- round 10: consumer consolidation
- round 11: bounded compose-from-intent

That means the next serious move should no longer be another proof-token ladder step.

The natural next questions are now product and platform questions:

- whether to adopt the transient contract in a real consumer surface
- whether to widen beyond AOI
- whether to add bounded draft persistence or promote transient pages into first-class authored artifacts

But round 11 itself is closed on its actual bounded claim.
