# Memo: Phase E First-Hop Affordance Routing Addendum V1 Scope

Subtitle: Attach bounded analyzer-owned first-hop capture/routing hints on transient compose surfaces

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
- `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`
Most Recent Product Companion Completion:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
Strategy Context:
- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Bridge_Hint_Consolidation_V1_Scope_Critique_2026-04-01.md`
- `communications/REPORT_Codex_Phase_E_Bridge_Hint_Consolidation_V1_Scope_Audit_2026-04-01.md`

## Purpose

Define the next bounded analyzer-side Phase E slice after:

- composition metadata extraction
- bridge-hint consolidation
- the completed runtime-first Close Read operations/routing inventory

The cleaned post-extraction authority line now makes one smaller semantic step possible:

- attach analyzer-owned first-hop affordance/routing hints to the transient compose response itself

This memo scopes that step narrowly.

It is not:

- a `Close Read V1` build memo
- destination-lifecycle modeling
- research-queue or outline-lifecycle modeling
- affordance attachment across every presentation surface at once

## Strategic Decision

The next concrete move should be:

- one bounded first-hop affordance/routing addendum on the transient compose line

not:

- more composition-authority cleanup
- destination-lifecycle annotation
- job-backed page/manifest affordance propagation
- findings-specific or research-answer-specific operation families
- a full analyzer-owned routing/product law for every downstream destination

The reason is now cleaner than before:

- the product-side inventory already identified the strongest runtime-real first-hop operations
- the composition-role line is now metadata-first end to end on the migrated AOI/genealogy bridge-backed path
- the next smallest honest semantic layer is surface-level capture/routing eligibility

## Current Evidence Base

The completed Close Read operations/routing inventory already isolated the strongest runtime-real first-hop seams in `the-critic`.

The best bounded starting family is still the one the inventory explicitly recommended:

- capture/routing eligibility on rendered analytical surfaces

The runtime-real first-hop matrix shows three facts that matter here:

1. generic selection capture to `Arsenal` and `Research Todo` is already real
2. outline talking-point routing is also runtime-real, but it is less generic and more output-shaped than the capture routes
3. destination-internal lifecycle is real too, but it must stay out of this tranche

That means the first analyzer-side affordance addendum should begin with a deliberately small field family:

- `capturable`
- bounded `allowed_destinations`

This is a seam-establishment slice, not a semantically discriminating one.
On the current proved transient analytical line, the honest v1 expectation is:

- the eligible leaf analytical views will likely receive the same values
- the main point is to establish analyzer-owned first-hop hint carriage on the transient compose line itself

`commentable` is intentionally deferred.
The current codebase shows comment persistence in product surfaces, but not a similarly clean analyzer-knowable rule for generic commentability on the current transient analytical compose line.

and it should defer:

- findings-star promotion
- generic `commentable`
- outline talking-point routing
- research-answer specific routing
- async research lifecycle
- premise-scrutiny / logic-gap families

## Scope

### In scope

1. Choose one bounded attachment surface.

For this v1 slice, the attachment surface should be:

- `TransientIntentView` inside `ComposeFromIntentResponse.presentation.views`

The concrete shared population seam should be named explicitly:

- `src/presenter/compose_from_intent.py::_to_transient_view(...)`

That function is the single conversion point shared by:

- `compose-from-intent`
- `compose-from-source`
- `compose-from-selection`

This keeps the addendum on the current proved transient compose line:

- `compose-from-intent`
- `compose-from-source`
- `compose-from-selection`

It does **not** broaden to:

- job-backed `PagePresentation`
- `EffectivePresentationManifest`
- trace-only metadata

2. Add one bounded affordance object.

The transient view payload should gain one optional affordance object for first-hop semantics only.

This v1 object should stay limited to:

- `capturable: bool`
- `allowed_destinations: list[...]`

The allowed destinations should stay bounded to this deliberate v1 subset of the runtime-real first-hop destinations already evidenced in the inventory:

- `arsenal`
- `research_todo`

This memo is intentionally **not** taking the full inventory set in one pass.
The inventory also evidences outline talking-point routing, but that remains out of scope here because this first slice is trying to establish the most generic first-hop capture/routing seam first.

3. Limit emission to the current proved analytical surfaces.

This slice should stay on the currently proved transient compose line only:

- AOI `source_selection`
- AOI `source_profile`
- genealogy `direct_sections`

And it should begin with the user-visible analytical views on that line, not with every possible downstream surface family.

For honesty, the emission boundary should be stated even more tightly:

- emit hints only for views on the migrated proved AOI/genealogy analytical family
- non-migrated or non-proved workflow views should remain unannotated in this v1 slice rather than being guessed by heuristic

The safe initial distinction is:

- analytical leaf views may carry first-hop affordance hints
- parent/container views should remain unannotated or empty by default unless there is concrete evidence that they are a real first-hop interaction surface themselves

This leaf-vs-container split should be treated as an explicit rule, not as an implementation afterthought.

4. Keep analyzer ownership narrow.

For this slice, analyzer-v2 should own only:

- semantic affordance hints
- bounded destination eligibility hints

Hosts should still own:

- actual selection models
- comment/capture UI
- button placement
- local workflows after a user chooses an allowed destination

5. Keep derivation analyzer-owned and explicit.

The affordance mapping should be analyzer-owned and explicit on the transient compose line.

It should not depend on:

- host heuristics
- consumer-local guesses
- renderer-local ad hoc inference

But this slice does **not** require a full taxonomy of every future operation family.

The minimal requirement is:

- the current proved analytical surfaces can emit bounded first-hop hints from analyzer-owned logic on the compose path

### Explicitly out of scope

- job-backed page/manifest affordance propagation
- destination-internal lifecycle hints
- research queue / lookup / refresh annotations
- outline upgrade / extract lifecycle hints
- findings-specific Arsenal promotion semantics
- research-answer specific routing semantics
- premise-scrutiny / logic-gap affordances
- NotebookLM or Book Modeler routing
- host UX changes
- Close Read product scoping

## Why This Slice Is Next

This is the smallest honest semantic addendum after bridge-hint consolidation.

It is stronger than immediately jumping to findings/research-specific operation families because it starts with the generic first-hop layer the inventory already showed is real.

It is smaller than destination-lifecycle work because it stays on:

- first-hop only
- transient compose only
- analytical surfaces only

It is more strategically useful than another cleanup slice because it is the first post-extraction step that actually begins the analyzer-owned semantic-affordance line implied by the `Close Read` direction, while still preserving thin-host ownership.

## Proposed Design Shape

### 1. Transient-view field, not renderer-config overloading

Do not bury first-hop affordances inside:

- `renderer_config`
- `structured_data`
- consumer-specific adaptation notes

Keep them as explicit transient-view metadata.

That makes the ownership boundary clearer:

- analyzer owns the hint
- host chooses how or whether to operationalize it

### 2. Start with one tiny shared affordance family

Do not design a broad vocabulary yet.

This v1 field family should stay bounded to:

- capture eligibility
- bounded allowed first-hop destinations

That is enough to start the analyzer-owned line honestly without pretending commentability, findings, research answers, outline flows, and destination lifecycle are already unified.

### 3. Prefer analytical leaf surfaces first

The initial emission rule should be conservative:

- leaf analytical views on the current transient compose line are the intended candidates
- parent containers, tab shells, and similar structural views should not automatically inherit the same hints

This keeps the first slice from overstating what the analyzer really knows.

### 4. Carry the new field through transient hashes honestly

Because this slice adds optional transient-view metadata, the contract/content fingerprinting story must remain honest too.

So the implementation should explicitly decide and test:

- whether the new affordance object belongs in the transient contract hash
- whether it belongs in the transient content hash

The important bar is not any one specific choice.
The important bar is:

- the new field must not silently bypass `presentation_hash` / `presentation_content_hash` expectations
- hash behavior must be covered by direct regression tests

## Acceptance Bar

This slice should count as complete only if all of the following are true:

1. `ComposeFromIntentResponse.presentation.views` can carry one optional first-hop affordance object without changing existing route or lifecycle contracts
2. the affordance object is bounded to:
   - `capturable`
   - `allowed_destinations`
3. allowed destinations are bounded to:
   - `arsenal`
   - `research_todo`
4. the affordance object is populated through `src/presenter/compose_from_intent.py::_to_transient_view(...)`, not through host-side or renderer-side patching
5. the current proved transient analytical surfaces can emit analyzer-owned first-hop hints on that field
6. the v1 emission boundary is explicit:
   - migrated-family analytical leaf views only
   - parent/container views unannotated or empty by default
   - non-proved / non-migrated workflows unannotated
7. destination-lifecycle and output-specific operation families remain out of the emitted contract
8. transient hash behavior is covered explicitly so the new field does not silently bypass `presentation_hash` / `presentation_content_hash`
9. representative composition behavior and proof surfaces remain unchanged except for the new optional metadata
10. no host or harness code changes are required for correctness

## Test Plan

### Primary analyzer verification

Add or extend focused tests for:

- `TransientIntentView` schema carrying the new optional affordance object
- `_to_transient_view(...)` as the population seam for the new field
- emitted affordance hints on the current proved transient compose line:
  - AOI `source_selection`
  - AOI `source_profile`
  - genealogy `direct_sections`
- all eligible proved leaf analytical views carrying the same bounded v1 values where appropriate
- container/parent views staying unannotated or empty by default
- non-proved / non-migrated workflows staying unannotated
- destinations staying bounded to:
  - `arsenal`
  - `research_todo`
- transient `presentation_hash` / `presentation_content_hash` behavior covering the new field explicitly

Recommended primary verification surface:

- `tests/test_compose_from_intent.py`
- `tests/test_representative_composition_matrix.py`

### Stability / regression

Keep the broader proof surfaces unchanged through verification:

- `tests/test_transient_proof_harness_contract.py`
- `tests/test_compose_sessions.py`

No host-side browser proof is the primary bar for this slice.

## Honest Claim If Completed

If this slice closes honestly, the claim should remain narrow:

- analyzer-v2 can now annotate the current transient compose surfaces with one bounded first-hop semantic-affordance/routing hint family for capture eligibility and allowed destinations, while leaving hosts responsible for actual UX and leaving destination lifecycle out of scope

It would **not** yet mean:

- analyzer-v2 owns full downstream operation-family law
- analyzer-v2 has solved generic commentability
- findings, research-answer routing, and outline flows are generalized
- job-backed page/manifest surfaces now carry the same hints
- `Close Read` is ready to build

## What Comes After This

If this slice lands cleanly, the next honest follow-on should be one of two things:

1. broaden first-hop affordance/routing attachment to one output-specific operation family
   - for example findings-specific or research-answer specific routing

or

2. decide whether the same bounded first-hop hints should propagate onto job-backed presentation surfaces

What should **not** happen next:

- jumping straight into destination lifecycle
- pretending the `Close Read` product is now fully scoped
- reopening composition-authority cleanup instead of using the cleaned line
