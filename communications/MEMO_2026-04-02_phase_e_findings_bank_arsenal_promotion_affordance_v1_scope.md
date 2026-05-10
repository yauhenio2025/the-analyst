# Memo: Phase E Findings-Bank Arsenal Promotion Affordance V1 Scope

Subtitle: Add one output-specific first-hop affordance family on one analyzer-known findings surface

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
Most Recent Code Completion:
- `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_scope.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
Strategy Context:
- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`

## Purpose

Define the next bounded analyzer-side Phase E slice after the generic first-hop affordance family now survives on both transient and job-backed presentation surfaces.

The surface question is now answered.
The next honest variable is semantics.

This memo therefore scopes:

- one output-specific first-hop affordance family
- on one analyzer-known analytical surface only
- with host UX still downstream

It does **not** scope:

- a generic operation-family taxonomy
- destination lifecycle
- host-side implementation
- broad affordance differentiation across all findings-like outputs

## Strategic Decision

The next concrete move should be:

- one bounded findings-bank Arsenal-promotion affordance family on the AOI `aoi_by_sin_type` surface

not:

- broad findings semantics across every `aoi_sin_findings`-backed surface
- outline-routing
- research-answer routing
- another surface-propagation tranche
- full Close Read product scoping

The reason is straightforward:

- the generic first-hop seam is now proven on both presentation families
- the strongest runtime-real output-specific first-hop operation in the current evidence base is finding promotion to Arsenal
- `aoi_by_sin_type` is a curated analyzer-known surface with stable view identity, stable renderer shape, and a direct semantic fit with findings-bank behavior
- `aoi_by_theme` is backed by the same engine but is more nested and semantically mixed, so it is a weaker first target for specialized semantics

This keeps the next step small:

- fix the surface family
- vary semantics once
- keep host ownership intact

## Current Evidence Base

Three repo facts make this a credible next slice:

1. the generic `FirstHopAffordance` seam is now live on both transient and job-backed presentation lines
2. the Close Read operations/routing inventory confirms that finding promotion to Arsenal is runtime-real in Critic
3. the `aoi_by_sin_type` surface is already a curated analyzer-known view:
   - `view_key = "aoi_by_sin_type"`
   - `engine_key = "aoi_sin_findings"`
   - `renderer_type = "card_grid"`
   - grouped finding-card semantics are explicit in the view contract

There is also one concrete analyzer-side reason this slice can stay small:

- AOI normalization already computes stable `finding_id` values upstream
- the current `aoi_by_sin_type` card payload drops that handle before it reaches the served surface
- so the remaining gap is not "invent finding semantics from scratch"
- it is "carry one already-known finding handle plus one specialized semantic marker to one analyzer-known surface"

The inventory also makes the ordering clear:

- finding promotion to Arsenal is stronger and more runtime-real than outline-routing as a first analyzer-owned specialized family
- outline routing remains more comment-shaped and host-shaped

## Scope

### In scope

1. **One minimal specialized extension on `FirstHopAffordance`**

Keep the already-landed generic family intact:

- `capturable`
- `allowed_destinations`

Add one optional specialized marker to `FirstHopAffordance`:

- `specialized_family: Optional[str]`

This is intentionally small.
It is not a generalized operation schema.

For v1, the documented analyzer-owned vocabulary is:

- `"findings_bank_arsenal_promotion_v1"`

The type stays open because every later specialized family should not require a schema rewrite just to add one more documented string.

2. **Define what the specialized family actually guarantees**

The specialized family must mean more than:

- capture is possible
- the host may route to Arsenal

Those claims are already carried by the base affordance.

For this v1, the additional analyzer-side guarantee should be:

- the items on this surface are findings rather than arbitrary cards
- finding-level operations are semantically appropriate on those items
- each card exposes one minimal per-item promotion handle via `finding_id`
- the card preserves finding-level structured payload sufficient for host-side finding promotion logic without re-parsing prose

In other words:

- the base affordance says "generic capture is possible"
- the specialized family says "the items here are findings suitable for finding-level operations, with preserved structured payload and one stable per-item handle"

This still does **not** mean analyzer-v2 owns:

- Arsenal mutations
- button semantics
- destination lifecycle
- any host-side promotion workflow

3. **One analyzer-known surface only**

Emit the specialized marker only on the job-backed AOI `aoi_by_sin_type` surface.

The emission rule should be concrete:

- `workflow_key == AOI_WORKFLOW_KEY`
- `view_key == "aoi_by_sin_type"`
- `engine_key == "aoi_sin_findings"`
- renderer contract remains findings-card compatible on the analyzer side
- the base `FirstHopAffordance` already exists on that view

Do **not** emit the specialized marker on:

- `aoi_by_theme`
- transient compose views
- generic `aoi_sin_findings`-backed outputs by engine-key alone
- non-AOI findings-like surfaces

4. **Keep the generic family unchanged**

This slice adds specialized semantics on top of the existing generic seam.
It does not replace it.

So on `aoi_by_sin_type`, the completed affordance should still say:

- `capturable = true`
- `allowed_destinations = ["arsenal", "research_todo"]`

and additionally:

- `specialized_family = "findings_bank_arsenal_promotion_v1"`

The intent is:

- generic selection capture remains available as before
- the specialized marker tells hosts that this particular analyzer-known surface supports finding-level promotion semantics on top of generic capture semantics

To make that honest, the slice should also include one minimal surface-shape change on `aoi_by_sin_type`:

- each emitted finding card should carry `finding_id`

This is not a generalized per-renderer item schema.
It is one minimal handle added on one analyzer-known findings surface whose upstream AOI normalization already produces stable `finding_id` values.

5. **Keep host ownership explicit**

The analyzer should only declare the specialized semantic family.
It should **not** own:

- finding-card button behavior
- mutation endpoints
- optimistic UI state
- Arsenal page behavior

Hosts remain responsible for operationalizing the UX.

### Explicitly out of scope

- any new destination beyond current `arsenal` / `research_todo`
- destination lifecycle
- direct research-todo specialization on findings
- `outline_talking_point`
- `aoi_by_theme`
- transient compose parity for this specialized family
- generalized item-level analyzer schema for every renderer
- broad findings-bank semantics across all workflows
- cross-job identity guarantees for findings

## Population And Contract Shape

The implementation should stay in the existing shared affordance path, not create a second subsystem.

The expected analyzer-side shape is:

- reuse the existing `FirstHopAffordance`
- extend it minimally with `specialized_family`
- extend `aoi_by_sin_type` card items minimally with `finding_id`
- populate that field in the same affordance helper line that already governs job-backed first-hop annotation

The contract should be described precisely:

- `specialized_family = "findings_bank_arsenal_promotion_v1"` means the host may treat `aoi_by_sin_type` items as findings suitable for finding-level operations
- those items carry a minimal per-item handle via `finding_id`
- those items preserve finding-level structured payload rather than forcing host reconstruction from prose alone

Known constraint:

- `finding_id` stability is only being claimed within the analyzer-produced findings contract for a given job execution
- hosts should not assume cross-job identity stability if the same workflow is re-run and findings reorder or materially change

The supporting contract consequences should stay explicit:

- `PagePresentation.views` is the real host-facing surface
- `EffectiveManifestView` carries the same field because it owns contract/hash and adjacent trace/reuse truth
- `_manifest_identity_row(...)` must include the specialized field
- `presentation_content_hash` must continue to ignore it as non-content metadata
- `_diff_snapshots(...)` must surface specialized-family changes rather than silently ignore them

## Acceptance Bar

This slice should count as complete only if all of the following are true:

1. `FirstHopAffordance` gains one optional specialized marker and nothing broader
2. the generic first-hop payload remains unchanged everywhere else
3. only job-backed AOI `aoi_by_sin_type` emits the specialized marker
4. `aoi_by_theme` remains generic-only
5. transient compose surfaces remain unchanged
6. `PagePresentation.views` exposes the specialized marker on the eligible surface
7. `EffectiveManifestView` exposes the same specialized marker on the eligible surface
8. `presentation_hash` changes when the specialized marker changes
9. `presentation_content_hash` does not change when only the specialized marker changes
10. trace snapshot diffs surface the specialized marker honestly
11. `aoi_by_sin_type` card items expose `finding_id` as the minimal per-item promotion handle
12. the specialized family contract is documented as finding-level, not generic selection-level
13. no host code changes are required for correctness of the analyzer-side contract

## Test Plan

### Primary analyzer verification

Add or extend focused tests for:

- shared schema support for the new optional `specialized_family`
- shared schema support for the open-string vocabulary approach
- job-backed `aoi_by_sin_type` emission on:
  - `ViewPayload`
  - `EffectiveManifestView`
  - `PagePresentation.views`
- `aoi_by_sin_type` card-shape verification:
  - emitted card items carry `finding_id`
  - finding-level structured payload remains available to hosts
- negative coverage proving no specialized emission on:
  - `aoi_by_theme`
  - genealogy views
  - transient compose views
  - non-approved workflows
  - non-AOI surfaces generally
- hash behavior:
  - contract hash changes
  - content hash does not
- trace diff behavior:
  - specialized-family changes are visible in manifest snapshot diffs

Recommended primary verification surface:

- `tests/test_presentation_api.py`
- `tests/test_manifest_trace.py`
- `tests/test_analysis_product_contract.py`
- `tests/test_aoi_contract.py`

### Stability / regression

Keep these lines unchanged except for the new additive specialized metadata where applicable:

- `tests/test_compose_from_intent.py`
- `tests/test_representative_composition_matrix.py`
- `tests/test_transient_proof_harness_contract.py`
- `tests/test_compose_sessions.py`

## Honest Claim If Completed

If this slice closes honestly, the claim should remain narrow:

- analyzer-v2 can now express one specialized findings-bank Arsenal-promotion semantic family on one analyzer-known AOI findings surface, with one minimal per-item handle and preserved finding-level payload, while preserving the generic first-hop affordance seam, keeping hosts thin, and leaving destination lifecycle out of scope

It would **not** yet mean:

- findings semantics are generalized across all `aoi_sin_findings` outputs
- item-level operation schemas are solved generically
- research-answer or outline-routing semantics are solved
- Close Read is product-ready

## What Comes After This

If this slice lands cleanly, the next honest follow-on should be one of these:

- broaden the same findings-bank semantics to one second analyzer-known findings surface only if the evidence remains clean
- or scope one separate bounded outline-routing family

What should **not** happen next:

- broadening destinations again
- jumping to destination lifecycle
- pretending this one surface proves a full operation-family taxonomy
