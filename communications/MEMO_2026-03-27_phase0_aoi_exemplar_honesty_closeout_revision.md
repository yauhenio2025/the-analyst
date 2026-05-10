# Memo: Phase 0 AOI Exemplar Honesty Closeout Revision

Date: 2026-03-27
Status: Closeout C; no truthful Phase 0 grade exists yet
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md`
- `communications/PROOF_phase0_aoi_execution_backed_corpus_inventory_2026-03-27.json`
- `communications/PROOF_phase0_aoi_execution_backed_launch_2026-03-27.json`
- `communications/PROOF_phase0_aoi_execution_backed_active_boundary_2026-03-27.json`
- `src/analysis_products/run_contract.py`
- `src/analysis_products/result_contract.py`

## Summary

This Phase 0 execution attempt does not produce a truthful Stage 2 grade.

The preflight passed and the fresh Otto Neurath AOI rerun really launched:

- project: `round5-proof-dossier-final-1774100000`
- thinker: `otto_neurath`
- workflow: `anxiety_of_influence_thematic_single_thinker`
- fresh job: `job-8c366372e0ef`

But the required active-run boundary proof failed immediately:

- the fresh job existed
- the fresh job was visible in analyzer active discovery without the thinker filter
- the fresh job did **not** appear in analyzer active discovery when the required `selected_source_thinker_id=otto_neurath` filter was applied

That means the required active-boundary artifact could not be produced honestly on the contracted path.

So this is `Closeout C`: invalid attempt because truthful grading was impossible.

## What Passed

- local analyzer-v2 started on `http://127.0.0.1:8002`
- local Critic backend started on `http://127.0.0.1:5555`
- local Critic webapp started on `http://127.0.0.1:3456`
- `ANTHROPIC_API_KEY` was present
- analyzer meta responded
- Critic backend/docs responded
- the AOI proof surface loaded
- the Otto corpus inventory was already the exact intended four-document set with stable `source_document_id` values
- the real Critic AOI launch route returned a fresh job envelope for `job-8c366372e0ef`

## Why The Attempt Is Invalid

The failure is not that the run id was fake or that the operator launched the wrong route.

The failure is narrower and more structural:

1. The fresh job was real.
   - `POST /api/influence/thinkers/otto_neurath/run-thematic-analysis-v2` returned `job-8c366372e0ef`
   - Critic job detail preserved the expected project, workflow, and thinker context
   - analyzer `GET /v1/runs/discovery?...scope=active` without the thinker filter returned the fresh job

2. The required thinker-scoped active discovery proof failed.
   - `GET /v1/runs/discovery?...scope=active&selected_source_thinker_id=otto_neurath` returned `[]`
   - the Stage 5 direct-poll smoke therefore failed immediately on the required active-boundary contract

3. The likely cause is visible in the current analyzer contract code.
   - `src/analysis_products/run_contract.py` filters active discovery by `selected_source_thinker_id` through `_extract_thinker_fields(...)`
   - `src/analysis_products/result_contract.py` only unwraps thinker fields for `_type == "request_snapshot"`
   - the fresh executor job row for `job-8c366372e0ef` was stored as `_type = "by_ref_request_snapshot"`
   - while the job remains in the generating / pending window, run detail therefore surfaces:
     - `selected_source_thinker_id = null`
     - `selected_source_thinker_name = null`

So the active AOI run can exist and still be filtered out of the required thinker-scoped run discovery path.

That breaks the contracted active-boundary proof.

## Additional Execution State

After launch, the fresh job remained in:

- `status = pending`
- `phase_name = Generating Analysis Plan`
- `detail = Planning from registered documents...`

through the observed polling window ending at `2026-03-26T16:09:46Z`.

No truthful completed-boundary proof, counted browser proof, or Stage 2 grading memo was produced from this attempt.

That restraint is deliberate.
Once the required active-boundary proof failed, continuing to a final grade would have turned the memo into a softened workaround instead of an honest gate.

## Next Honest Step

Do one bounded repair on the active discovery seam, then rerun Phase 0 fresh.

The repair target is:

- make active run discovery preserve thinker identity for fresh AOI by-ref jobs during the generating / pending window
- specifically, ensure the thinker-scoped active discovery path can surface jobs whose stored request snapshot type is `by_ref_request_snapshot`

After that repair lands, rerun the same Phase 0 execution memo from the beginning on a new fresh Otto run.

Do not reuse `job-8c366372e0ef` as the authoritative execution-backed exemplar.
