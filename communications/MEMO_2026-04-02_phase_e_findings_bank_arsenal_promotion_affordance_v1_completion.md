# Memo: Phase E Findings-Bank Arsenal Promotion Affordance V1 Completion

Subtitle: One pure AOI findings surface now carries bounded analyzer-owned findings-bank promotion semantics, fail-closed on real item handles

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
- `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_scope.md`
Most Recent Prior Code Completion:
- `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_completion.md`
Earlier Code Completions In This Line:
- `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`
- `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

## Purpose

Record what actually landed in the bounded findings-bank Arsenal-promotion affordance slice after the scope memo, the review corrections, and the closeout fix on missing per-card handles.

This memo is about what is now true on the analyzer side.
It is not a claim that generalized findings semantics are solved, that mixed surfaces now carry the same specialization, or that analyzer-v2 now owns host mutation behavior.

## What Landed

One bounded output-specific semantic family now exists on one pure analyzer-known findings surface:

- AOI `aoi_by_sin_type`

The generic first-hop contract remains intact:

- `capturable = true`
- `allowed_destinations = ["arsenal", "research_todo"]`

The landed specialized extension is:

- `FirstHopAffordance.specialized_family = "findings_bank_arsenal_promotion_v1"`

The supporting surface-level contract addition is:

- each `aoi_by_sin_type` card may now carry `finding_id`

That handle is:

- analyzer-owned
- opaque
- job-scoped

It is intentionally **not** the same thing as Critic's legacy numeric `db_id`, and it is not drop-in parity with Critic's current `/api/arsenal` mutation seam.

## The Final Emission Boundary

The completed specialization boundary is intentionally narrower than the first implementation attempt.

The specialized family now appears only when all of these are true:

- the view is on the job-backed line
- `workflow_key == AOI_WORKFLOW_KEY`
- `view_key == "aoi_by_sin_type"`
- `engine_key == "aoi_sin_findings"`
- the base `FirstHopAffordance` already exists
- the actual emitted payload proves complete per-card handles:
  - every emitted finding card has a non-empty `finding_id`

The specialization does **not** appear on:

- `aoi_by_theme`
- transient compose views
- genealogy views
- non-approved workflows
- older or malformed `aoi_by_sin_type` payloads that lack usable per-card handles

That last correction is important.
The specialized family is no longer inferred from workflow/view/engine identity alone.

## Closeout Correction

One review finding was real and had to be fixed before this slice could close honestly:

- existing AOI jobs could advertise `findings_bank_arsenal_promotion_v1` without actually exposing a usable per-card handle

The fix now fail-closes that case:

- specialization is attached only if the materialized `aoi_by_sin_type` payload proves complete `finding_id` coverage
- `_build_by_sin_type_payload(...)` no longer degrades missing ids to an empty string
- older persisted AOI payloads without handles remain generic-only instead of overclaiming finding-level promotion semantics

This means the analyzer contract is now stricter and more honest than the first pass:

- pure findings specialization only when item handles are genuinely present
- generic first-hop affordance otherwise

## What Else Changed

Two smaller but real contract consequences landed with the slice:

1. **Hash stability for generic views**

Both identity serializers now exclude unset specialized metadata:

- `src/presenter/compose_from_intent.py::_transient_identity_row(...)`
- `src/presenter/manifest_builder.py::_manifest_identity_row(...)`

That means generic affordance-bearing views do not churn hashes merely because `specialized_family` exists but is `None`.

2. **Saved AOI trace fixtures**

The saved Round 6 AOI trace fixtures were refreshed so their manifests reflect the stricter current truth:

- `communications/PROOF_round6_dossier_final_trace_2026-03-21.json`
- `communications/PROOF_round6_comparison_final_trace_2026-03-21.json`

Because those saved outputs do not prove complete `finding_id` coverage on `aoi_by_sin_type`, they now remain generic-only there.
That refresh is expected and desirable.

## Verification

Focused verification passed:

- `python -m compileall src/presenter/first_hop_affordance.py src/aoi/contract.py tests/test_presentation_api.py`
- `PYTHONPATH=. pytest -q tests/test_aoi_contract.py tests/test_presentation_api.py tests/test_manifest_trace.py tests/test_analysis_product_contract.py tests/test_compose_from_intent.py tests/test_representative_composition_matrix.py tests/test_transient_proof_harness_contract.py tests/test_compose_sessions.py`
  - `279 passed, 13 warnings`

No host code was changed in this slice.

## Calibrated Claim

The honest completed claim is now:

- analyzer-v2 can express one bounded findings-bank Arsenal-promotion semantic family on one pure analyzer-known AOI findings surface
- that specialization survives on the mainstream job-backed presentation line
- it remains layered on top of the generic first-hop affordance contract rather than replacing it
- it only appears when the actual emitted cards expose usable analyzer-owned per-item handles

It does **not** yet mean:

- findings semantics are generalized across all `aoi_sin_findings` surfaces
- mixed surfaces like `aoi_by_theme` now carry the same specialization
- analyzer-v2 owns a generic item-level operation schema
- analyzer handles are equivalent to Critic's current database ids
- host-side Arsenal mutations or lifecycle are now upstream-owned
- outline-routing or research-answer specialization is solved

## Why This Matters

This slice closes the first output-specific semantics question on the current first-hop line.

The analyzer now proves three layers in sequence:

- generic first-hop affordance on transient surfaces
- the same generic contract on job-backed surfaces
- one bounded specialized findings-bank semantic family on one pure analyzer-known findings surface

That is a real generality broadening step.
But it also exposes the next honest boundary:

- pure findings surfaces are easier than mixed surfaces

## Next Honest Step

The next bounded Phase E question should now be:

- can analyzer-v2 carry minimal finding-level handles on one mixed analyzer-known AOI surface without overclaiming whole-view findings semantics or inventing a generic item-level affordance subsystem?

The strongest current candidate is:

- AOI `aoi_by_theme`

That is the right next step because:

- it is backed by the same normalized AOI findings family
- the view definition already declares nested findings explicitly under each theme
- the Critic thematic UI already treats those nested findings as item-level entities keyed by `finding_id`
- the current analyzer contract still drops that handle on the mixed surface
- a whole-view findings-bank specialization would overclaim on `aoi_by_theme`, so the next honest question is mixed-surface handle carriage, not another easy pure-surface specialization
