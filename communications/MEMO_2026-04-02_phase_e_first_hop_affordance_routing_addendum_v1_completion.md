# Memo: Phase E First-Hop Affordance Routing Addendum V1 Completion

Subtitle: Bounded analyzer-owned first-hop capture/routing hints now exist on the transient compose line

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
- `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_scope.md`
Most Recent Prior Code Completion:
- `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

## Purpose

Record what actually landed in the bounded first-hop affordance/routing addendum after the scope memo and the follow-up review corrections.

This memo is about what is now true on the analyzer side.
It is not a claim that downstream operation-family law is solved, that job-backed surfaces already carry the same hints, or that hosts now expose the corresponding UX automatically.

## What Landed

The transient compose response now carries one bounded analyzer-owned first-hop affordance object on the approved analytical leaf surfaces.

The landed field family is exactly:

- `capturable`
- `allowed_destinations`

The nested contract is implemented as:

- `TransientFirstHopAffordance`

on:

- `TransientIntentView`

The emitted v1 values are deliberately small and uniform where present:

- `capturable = true`
- `allowed_destinations = ["arsenal", "research_todo"]`

No `commentable` field landed in this slice.

## The Final Emission Boundary

The completed implementation is narrower than the early draft and now matches the approved boundary:

- emit only on migrated-family analytical leaf views
- emit only on these transient compose handoff families:
  - AOI `source_profile`
  - AOI `source_selection`
  - genealogy `direct_sections`
- do not emit on AOI `direct_sections`
- do not emit on synthetic parent/container views
- do not emit on non-migrated / non-proved workflow views

The key implementation detail is that emission is no longer derived from leaf shape plus engine family alone.
It is now gated by the actual `(workflow_key, handoff_kind)` pair before `_to_transient_view(...)` builds the public transient tree.

## What Changed During Closeout

Two review-detected gaps were real and were fixed before closeout:

1. **Scope mismatch on AOI `direct_sections`**

The first implementation version annotated AOI `direct_sections` because the affordance gate only checked:

- migrated-family engine key
- leaf status

That was broader than the approved scope.
The fix now gates first-hop affordance emission by the approved route family itself, not just by the leaf engine family.

2. **Representative matrix coverage gap**

The initial implementation tests proved the field on the compose path but did not make the representative frozen matrix bundles assert it.
That gap is now closed.

The representative matrix tests now assert first-hop affordance presence/absence on the three approved frozen proof bundles, and the frozen response JSON plus `presentation_hash` values were refreshed accordingly.

## Verification

Focused closeout verification passed:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_representative_composition_matrix.py`
  - `70 passed, 2 warnings`

Broader regression verification also passed:

- `PYTHONPATH=. pytest -q tests/test_composition_source_bridge.py tests/test_genealogy_saved_result_bridge.py tests/test_compose_from_intent.py tests/test_representative_composition_matrix.py tests/test_transient_proof_harness_contract.py tests/test_compose_sessions.py`
  - `91 passed, 2 warnings`

## Proof And Contract Effects

The additive field is now contract-honest on the transient line:

- it participates in transient `presentation_hash`
- it does **not** participate in transient `presentation_content_hash`

That means the analyzer now treats first-hop affordance as:

- a contract-level annotation
- not a change to rendered analytical content

The representative frozen proof bundles were updated to reflect that contract truth:

- `communications/PROOF_phase_e_matrix_aoi_source_profile_dossier_2026-03-30.json`
- `communications/PROOF_phase_e_matrix_aoi_source_selection_2026-03-30.json`
- `communications/PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json`

## Calibrated Claim

The honest completed claim is now:

- analyzer-v2 can annotate the current approved transient compose surfaces with one bounded first-hop semantic-affordance/routing hint family for capture eligibility and allowed destinations
- the hint is analyzer-owned, route-aware, leaf-only, and hash-honest
- hosts remain responsible for actual UX and post-click behavior

It does **not** yet mean:

- analyzer-v2 owns full downstream operation-family law
- commentability is generalized
- findings-specific or research-answer-specific routing is generalized
- job-backed `PagePresentation` or `EffectivePresentationManifest` surfaces carry the same hints
- `Close Read` is now product-ready

## Why This Matters

This slice is strategically small but important.

It proves one more layer of analyzer ownership beyond composition and rendering:

- analyzer-owned semantic first-hop hints can now travel on a public presentation contract
- the host does not need to infer them ad hoc
- the contract can evolve without pretending downstream lifecycle is already solved

That is the first concrete analyzer-owned semantic-affordance seam on the presentation side.

## Next Honest Step

The next honest bounded question is no longer whether transient compose can carry a first-hop affordance seam at all.
That is now answered.

The next bounded question should be:

- can the same already-landed bounded first-hop affordance family propagate onto the mainstream job-backed presentation line without changing the semantics, widening destinations, or pulling host UX upstream?

That means the next scoped slice should target:

- job-backed `ViewPayload`
- `EffectivePresentationManifest`
- `PagePresentation`

while keeping:

- the field family fixed to `capturable + allowed_destinations`
- the destination set fixed to `arsenal + research_todo`
- output-specific operation families deferred
- destination lifecycle deferred

That is the cleanest next variable after this transient-only seam closeout.
