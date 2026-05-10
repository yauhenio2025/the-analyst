# Memo: Phase E Job-Backed First-Hop Affordance Propagation V1 Completion

Subtitle: The bounded first-hop affordance contract now survives on the mainstream job-backed presentation line

Date: 2026-04-02
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Immediate Scope Memo:
- `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_scope.md`
Most Recent Prior Code Completion:
- `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`
Earlier Code Completions In This Line:
- `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

## Purpose

Record what actually landed in the bounded job-backed first-hop affordance propagation slice after the transient addendum closeout and the review corrections on helper placement, leaf gating, and trace/hash honesty.

This memo is about what is now true on the analyzer side.
It is not a claim that richer output-specific operation families are already solved, that hosts expose the new field automatically, or that destination lifecycle is now modeled upstream.

## What Landed

The already-landed bounded first-hop affordance contract now exists on both presenter surface families:

- transient compose surfaces
- job-backed presentation surfaces

The shared contract is now:

- `FirstHopAffordance`
- `FirstHopDestination`

The bounded v1 payload stays unchanged:

- `capturable`
- `allowed_destinations = ["arsenal", "research_todo"]`

The shared model now appears on:

- `TransientIntentView`
- `ViewPayload`
- `EffectiveManifestView`

and therefore survives through:

- transient compose responses
- `PagePresentation.views`
- `EffectivePresentationManifest.views`

## The Final Job-Backed Emission Boundary

The completed job-backed emission boundary is intentionally narrow and matches the approved discipline:

- approved workflow families only:
  - AOI
  - genealogy
- approved views only:
  - migrated-family analytical leaves
  - real `engine_key`
  - `not payload.children`
- parent/container views remain unannotated
- non-migrated / non-proved workflow views remain unannotated

This slice did **not** broaden the semantic family while broadening the surface family.

## The Actual Population Seam

The main implementation correction from the review landed as intended:

- the job-backed helper now runs in the shared `_prepare_page_payloads(...)` flow

That means the prepared payload tree is annotated once at the shared presenter seam and then reused by:

- `build_presentation_manifest(...)`
- `assemble_page(...)`
- `get_presentation_status(...)`
- trace flows that build manifests from `_prepare_page_payloads(...)`

One additional explicit carry-forward was required:

- the non-`composition_mode` branch of `assemble_single_view(...)` bypasses `_prepare_page_payloads(...)`
- that branch now calls the same helper directly so eligible lazy-loaded leaves keep parity with full-page surfaces

## Hash And Trace Honesty

The new job-backed field is now contract-honest rather than a ghost annotation.

On the job-backed line:

- `presentation_hash` changes when `first_hop_affordance` changes
- `presentation_content_hash` does **not** change when only `first_hop_affordance` changes

The explicit contract-hash seam was updated at:

- `src/presenter/manifest_builder.py::_manifest_identity_row(...)`

The trace line also stays honest:

- `EffectiveManifestView` now carries the same field
- `_diff_snapshots(...)` now includes `first_hop_affordance`
- no separate trace-only population path was introduced

## What Else Changed

Two additional cleanup points landed as part of the slice:

1. **Shared model naming**

The transient-only names were generalized because the model is now genuinely shared:

- `TransientFirstHopAffordance` -> `FirstHopAffordance`
- `TransientFirstHopDestination` -> `FirstHopDestination`

Transient behavior itself stayed unchanged apart from the shared naming/import update.

2. **Saved AOI trace fixtures**

Two saved AOI trace fixtures had to be refreshed because the job-backed final manifests now correctly carry the new field:

- `communications/PROOF_round6_dossier_final_trace_2026-03-21.json`
- `communications/PROOF_round6_comparison_final_trace_2026-03-21.json`

That refresh is expected and desirable.
The old snapshots were missing the now-real contract field.

## Verification

Focused presenter verification passed:

- `python -m compileall src/presenter/schemas.py src/presenter/first_hop_affordance.py src/presenter/compose_from_intent.py src/presenter/presentation_api.py src/presenter/manifest_builder.py src/presenter/decision_trace.py tests/test_compose_from_intent.py tests/test_presentation_api.py tests/test_manifest_trace.py`
- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_presentation_api.py tests/test_manifest_trace.py`
  - `164 passed, 2 warnings`

Broader regression verification also passed:

- `PYTHONPATH=. pytest -q tests/test_analysis_product_contract.py tests/test_representative_composition_matrix.py tests/test_transient_proof_harness_contract.py tests/test_compose_sessions.py`
  - `91 passed, 13 warnings`

## Calibrated Claim

The honest completed claim is now:

- analyzer-v2 can carry the same bounded first-hop capture/routing affordance object on both the transient compose line and the mainstream job-backed presentation line
- the contract remains analyzer-owned, view-local, leaf-gated, and hash-honest
- `PagePresentation.views` is now covered as the real host-facing surface
- `EffectivePresentationManifest.views` carries the same field for contract/hash and adjacent trace/reuse truth

It does **not** yet mean:

- richer output-specific affordance families are solved
- findings-specific promotion semantics are generalized
- research-answer routing semantics are generalized
- outline routing is generalized
- hosts automatically expose or honor the new field
- destination lifecycle belongs to analyzer-v2
- `Close Read` is product-ready

## Why This Matters

This slice closes an important surface-generalization question cleanly.

The analyzer now owns one bounded first-hop affordance seam across both current presentation families:

- transient compose
- job-backed page/manifest

That means the next honest variable is no longer the surface contract.
It is semantics.

## Next Honest Step

The next bounded question should now be:

- can analyzer-v2 carry one output-specific first-hop affordance family on one analyzer-known analytical surface without jumping to full operation-family taxonomy or destination lifecycle?

The strongest current candidate is:

- one findings-bank Arsenal-promotion affordance family on the AOI `aoi_by_sin_type` surface

That is the best next move because:

- it has strong runtime evidence in Critic
- it is more analyzer-known than outline-routing
- it is narrower than broadening destinations or lifecycle
- it varies semantics while keeping the already-proved surface propagation line fixed
