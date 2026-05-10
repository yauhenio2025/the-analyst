# Memo: Phase E Job-Backed First-Hop Affordance Propagation V1 Scope

Subtitle: Propagate the existing bounded first-hop capture/routing hint family from transient compose onto job-backed presentation surfaces

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
- `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`
Earlier Code Completions In This Line:
- `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
Strategy Context:
- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Critique_2026-04-02.md`
- `communications/REPORT_Codex_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Audit_2026-04-02.md`

## Purpose

Define the next bounded analyzer-side Phase E slice after the transient first-hop affordance/routing addendum landed cleanly.

The transient line now proves one thing:

- analyzer-v2 can attach one bounded first-hop semantic-affordance object to public presentation views while preserving thin-host ownership and hash honesty

The next question should vary the **surface contract**, not the semantics.

This memo therefore scopes:

- propagation of the already-landed first-hop affordance family onto the job-backed presentation line

It does **not** scope:

- richer output-specific affordance semantics
- new destinations
- destination lifecycle
- host UX changes

## Strategic Decision

The next concrete move should be:

- one bounded job-backed propagation slice for the already-landed first-hop affordance object

not:

- a findings-specific or research-answer-specific affordance family yet
- a broader operation-family taxonomy
- destination-lifecycle propagation
- `Close Read` product build-out

The reason is simple:

- the transient line already proved the analyzer-owned attachment seam
- the current affordance values are still intentionally uniform
- the smallest honest new variable is whether the same bounded hint family can survive the mainstream job-backed presenter contracts

This keeps the semantics fixed and varies only the presentation surface.
That is smaller and stronger than inventing richer semantics on the next move.

## Current Evidence Base

Three things are now true in the repo:

1. the transient compose line already carries a bounded first-hop affordance object on the approved migrated analytical leaf surfaces
2. the job-backed line already has mature public view contracts and hash law:
   - `ViewPayload`
   - `EffectiveManifestView`
   - `PagePresentation`
3. the current hosts already consume the job-backed presentation line as the mainstream long-lived rendering surface

The host-facing surface priority on that line should be stated honestly:

- `PagePresentation.views` is the real host-facing rendering surface today
- `EffectivePresentationManifest.views` matters in this slice mainly because it is the contract/hash surface and the source used by adjacent trace/reuse seams

The current transient closeout also established the key discipline this slice should keep:

- the new field belongs to contract identity
- it does not pretend to change analytical content

That same contract/content distinction already exists on the job-backed line through:

- `presentation_hash`
- `presentation_content_hash`

So the current repo already has the right substrate for this propagation slice.

## Scope

### In scope

1. **One shared first-hop affordance model across transient and job-backed surfaces**

The current transient-only naming is now slightly too narrow for the next step.
This slice should normalize the model into one shared presenter-side type:

- `FirstHopAffordance`

usable by:

- `TransientIntentView`
- `ViewPayload`
- `EffectiveManifestView`

The semantic payload stays unchanged:

- `capturable: bool`
- `allowed_destinations: ["arsenal", "research_todo"]`

2. **Job-backed surface propagation only**

This slice should add the same optional affordance object to:

- `ViewPayload`
- `EffectiveManifestView`

and therefore expose it through:

- `PagePresentation.views`
- `EffectivePresentationManifest.views`

The order of importance should remain explicit:

- primary public surface: `PagePresentation.views`
- secondary contract/hash surface: `EffectivePresentationManifest.views`

3. **Keep the same narrow emission boundary**

The emission rule should remain as conservative as the transient closeout:

- approved workflow families only, using `workflow_key` from the job-backed presenter path
- migrated-family analytical leaf views only
- parent/container views unannotated
- non-migrated / non-proved workflows unannotated

This slice should not broaden the semantic boundary while broadening the surface boundary.

Because the job-backed line has no transient `handoff_kind`, the rule must be framed concretely:

- first resolve `workflow_key` from the prepared job-backed page inputs
- then emit only when both are true:
  - `workflow_key` is one of the currently approved proved families:
    - AOI
    - genealogy
  - the view is a migrated-family analytical leaf:
    - real `engine_key`
    - no active children

This should be treated as the job-backed analogue of the transient route-aware gate, not as a heuristic guess from renderer shape alone.

4. **Prefer one shared job-backed population seam**

The preferred shared analyzer seam should be a small helper applied on the job-backed presenter path after `_prepare_page_payloads(...)` returns and before manifest/page hashes are finalized.

The best bounded implementation target appears to be:

- one shared helper on the prepared job-backed `ViewPayload` tree, invoked where `workflow_key` is already available on the `presentation_api.py` path

because:

- `_prepare_page_payloads(...)` already resolves the job-backed payload tree plus `workflow_key`
- `build_presentation_manifest(...)` and `assemble_page(...)` already converge immediately after that seam
- `EffectivePresentationManifest` is derived there directly
- `PagePresentation.views` already reuses the same `ViewPayload` tree

The slice should avoid duplicating affordance population separately in:

- manifest assembly
- page assembly

The memo should be explicit about what this means in practice:

- do not hide workflow-gated affordance emission down inside `build_effective_manifest(...)` alone, because that function does not own workflow resolution as its primary seam
- instead, annotate the prepared payload tree once, then let both manifest and page assembly inherit the same field

5. **Carry hash/fingerprint honesty across the job-backed line**

The propagated field must be treated explicitly in:

- effective manifest hash identity
- page hash identity

The same honesty line as transient should hold:

- contract hash includes the affordance object
- content hash does not treat it as analytical content

That means the implementation must explicitly name the contract-hash seam:

- `src/presenter/manifest_builder.py::_manifest_identity_row(...)`

and not rely on the new field being picked up accidentally.

### Explicitly out of scope

- changing the affordance family beyond:
  - `capturable`
  - bounded `allowed_destinations`
- adding `commentable`
- adding `outline_talking_point`
- findings-specific promotion semantics
- research-answer specific routing semantics
- destination lifecycle
- trace-only affordance propagation
- host UX work
- result-manifest / product-manifest redesign
- non-migrated heuristic affordance inference

The slice also does **not** treat decision trace as a primary new surface.
But because the decision trace snapshots and diffs `EffectiveManifestView`, the implementation must update those supporting seams so affordance changes do not become invisible in trace diffs.

## Why This Slice Is Next

The transient line already established the analyzer-owned affordance seam.

The next honest question is no longer:

- can analyzer-v2 emit first-hop affordance metadata at all?

It is:

- can the mainstream job-backed presentation line carry the same bounded hint family without semantic drift or contract dishonesty?

That is a smaller move than jumping immediately to:

- findings-specific affordances
- research-answer routing semantics
- outline routing

Those richer families are probably where non-uniform semantics begin, but they are also more host-shaped and more output-specific.
The job-backed propagation slice is a cleaner surface-generalization step first.

## Proposed Design Shape

### 1. Reuse one shared affordance contract

Do not fork the same semantics into:

- one transient-only nested model
- one separate job-backed nested model

Use one shared presenter schema type for first-hop affordances across both surface families:

- `FirstHopAffordance`

Keep this generalization minimal.
This is a naming/placement cleanup for one already-landed bounded model, not a new affordance subsystem.
The transient-specific model should therefore be renamed to:

- `FirstHopAffordance`

and that rename should happen only because the model is now genuinely shared, not because the slice is widening semantics.

### 2. Propagate on views, not on page-level metadata

Keep this view-local, not page-global.

The affordance belongs on:

- the specific analytical view a host may capture from

It should not be represented as:

- one page-level list of destinations
- one trace-only annotation
- one renderer-config override

### 3. Keep output semantics frozen in v1

This is not the slice where `aoi_sin_findings` becomes special.
If a view qualifies, it should receive the same landed bounded values as the transient line.

That means the value of this slice is:

- surface propagation
- contract unification
- hash honesty

not richer semantic discrimination.

## Acceptance Bar

This slice should count as complete only if all of the following are true:

1. one shared first-hop affordance model is usable on both transient and job-backed presentation surfaces
2. `ViewPayload` can carry the optional first-hop affordance object
3. `EffectiveManifestView` can carry the optional first-hop affordance object
4. `PagePresentation.views` and `EffectivePresentationManifest.views` expose the field without host-side patching
5. the job-backed presenter path populates the field through one shared analyzer-owned helper rather than duplicated local logic
6. the emission boundary remains explicit and narrow:
   - approved workflow-key families only
   - migrated-family analytical leaf views only
   - parent/container views unannotated
   - non-migrated / non-proved workflows unannotated
7. the affordance family remains fixed to:
   - `capturable`
   - `allowed_destinations = ["arsenal", "research_todo"]`
8. job-backed `presentation_hash` changes when the affordance contract changes
9. job-backed `presentation_content_hash` does not change when only the affordance contract changes
10. `PagePresentation` remains the primary host-facing surface for this slice; `EffectivePresentationManifest` is updated because it owns contract/hash identity and adjacent trace/reuse seams
11. decision-trace support stays honest:
   - `build_presentation_trace(...)` does not become a new primary surface
   - but affordance changes are not silently omitted from `EffectiveManifestView` snapshot diffs
12. existing transient affordance behavior remains unchanged
13. no host code changes are required for correctness

## Test Plan

### Primary analyzer verification

Add or extend focused tests for:

- shared affordance schema availability on:
  - transient view
  - `ViewPayload`
  - `EffectiveManifestView`
- job-backed workflow-key eligibility rule on the prepared payload path
- job-backed affordance population on the current migrated analytical leaf surfaces
- parent/container views staying unannotated on the job-backed line
- non-migrated / non-proved workflows staying unannotated
- manifest/page hash behavior covering the new field explicitly
- page/manifest parity:
  - the same eligible view carries the same affordance object on both surfaces
- decision-trace diff coverage:
  - affordance field changes are visible in `EffectiveManifestView` snapshot diffs rather than silently ignored
- transient test/schema import updates as needed if the shared-model rename from `TransientFirstHopAffordance` to `FirstHopAffordance` lands, with behavioral assertions otherwise unchanged

Recommended primary verification surface:

- `tests/test_manifest_trace.py`
- `tests/test_presentation_api.py`
- `tests/test_analysis_product_contract.py`

### Stability / regression

Keep the following lines unchanged except for the new additive metadata:

- `tests/test_compose_from_intent.py`
- `tests/test_representative_composition_matrix.py`
- `tests/test_transient_proof_harness_contract.py`
- `tests/test_compose_sessions.py`

## Honest Claim If Completed

If this slice closes honestly, the claim should remain narrow:

- analyzer-v2 can now carry the same bounded first-hop capture/routing affordance object on both the transient compose line and the mainstream job-backed presentation line, while keeping the semantics fixed, the hosts thin, and destination lifecycle out of scope

It would **not** yet mean:

- richer output-specific affordances are solved
- findings or research-answer routing semantics are generalized
- hosts automatically expose or honor the new field
- `Close Read` is product-ready

## What Comes After This

If this slice lands cleanly, the next honest follow-on should be:

- one output-specific first-hop affordance family on a single analyzer-known analytical surface

The most plausible candidates are:

- findings-bank promotion semantics
- one bounded outline-routing hint family

What should **not** happen next:

- jumping straight to destination lifecycle
- broadening destinations again
- reopening composition-authority cleanup
