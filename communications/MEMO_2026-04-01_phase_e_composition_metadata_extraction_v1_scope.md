# Memo: Phase E Composition Metadata Extraction V1 Scope

Subtitle: First behavior-preserving extraction of workflow-shaped composition law out of `compose_from_intent.py`

Date: 2026-04-01
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Product Companion Completion:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
Most Recent Code Completion:
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_v1_completion.md`
Strategy Context:
- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
Companion Product Discovery:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
Review Context:
- `communications/REPORT_Claude_Interface_First_Renderer_Output_Family_Strategy_Critique_2026-04-01.md`
- `communications/REPORT_Codex_Interface_First_Renderer_Output_Family_Strategy_Audit_2026-04-01.md`

## Purpose

Define the next bounded analyzer-side Phase E slice after:

- the proof-only lifecycle `source_selection` closeout
- the interface-first strategy review
- the completed runtime-first Close Read operations/routing inventory companion

The reviews converge on one next move:

- do not jump straight to output-family taxonomy design
- do not jump straight to `source_profile` lifecycle broadening
- first extract the lowest-risk workflow-shaped composition law out of `src/presenter/compose_from_intent.py`

This memo therefore scopes one behavior-preserving extraction tranche.

The completed product-side inventory sharpened this choice rather than replacing it:

- real downstream first-hop operations are now better evidenced
- but analyzer-side affordance/routing attachment work should still wait until after this extraction tranche lands

One more code-backed clarification now matters:

- this slice is not inventing a brand-new composition-resolution path from scratch
- partial extraction already exists through role hints emitted by the current source/result bridges
- the goal is to make composition metadata authoritative and uniform across the currently proved engine set

## Strategic Decision

The next concrete move should be:

- analyzer-side composition metadata extraction

not:

- another consumer shell
- another live proof shell exercise
- immediate source-backed lifecycle broadening
- a large taxonomy-design exercise before the current coupling is extracted

The reason is now code-backed and review-backed:

- renderer boundedness is real
- output-family taxonomy does not yet exist
- the hardest current blocker is still centrally encoded workflow-shaped composition law

The lowest-risk way forward is:

- extract the first hard-coded composition maps into metadata for the currently proved engines
- preserve current behavior exactly
- keep host apps and proof harnesses unchanged

## Current Coupling Target

The first extraction target is the central composition metadata currently hard-coded in:

- `src/presenter/compose_from_intent.py`

Specifically:

- `_ROLE_FROM_ENGINE_KEY`
- `_LEAF_PATTERN_BY_ROLE`
- `_PRESENTATION_STANCE_BY_ROLE`
- `_ROLE_DESCRIPTION_PREFIX`
- `_ROLE_RATIONALE_PREFIX`

But the current code is not a total blank slate.
Two partial upstream metadata seams already exist:

- `src/presenter/composition_source_bridge.py` already emits `composition_role_hint`
- `src/orchestrator/genealogy_saved_result_bridge.py` already emits `role_hint`

And the current resolver already prefers those hints:

- `_resolve_semantic_role(...)` checks role hints before falling back to `_ROLE_FROM_ENGINE_KEY`

Those seams currently determine, for the already-proved engines:

- semantic role
- leaf pattern / view family choice
- presentation stance
- description text prefix
- rationale prefix

They are the clearest current examples of composition-law data that should stop living as central hard-coded presenter maps.

So the extraction goal is more precise than “add metadata somewhere”:

- keep the existing hint-first resolution shape
- make canonical upstream metadata authoritative for the currently proved engine set
- stop relying on central hard-coded fallback maps as the primary source for migrated engines

This slice does **not** attempt to solve all current hard-coded policy seams.

In particular, this slice does **not** directly target:

- `_SUPPORTED_HANDOFF_KINDS`
- `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS`
- `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`

Those remain real later candidates, but they are operational/admission policy, not the best first extraction target.

## Scope

### In scope

1. Add one metadata-bearing seam for the currently composed engine set only.

The migrated engine set should be limited to the engines already on the proved transient/lifecycle line:

- `aoi_thematic_synthesis`
- `aoi_engagement_mapping`
- `aoi_sin_findings`
- `aoi_thematic_report`
- `genealogy_relationship_classification`
- `genealogy_pass1b_relationship_classification`
- `genealogy_final_synthesis`
- `genealogy_pass7_final_synthesis`

2. Commit the storage location.

For this slice, the authoritative per-engine metadata location should be:

- extension of the current engine capability definitions

This slice should therefore treat the existing capability-definition layer as the canonical home for:

- `composition_role`

This memo no longer leaves storage location open between multiple alternatives.

3. Represent, in metadata, at least:

- per canonical engine capability definition:
  - `composition_role`
- per extracted composition-role metadata seam:
  - `preferred_pattern_key`
  - `preferred_presentation_stance`
  - `description_prefix`
  - `rationale_prefix`

The important code-backed distinction is:

- `composition_role` is the real existing upstream seam already hinted by current bridges
- pattern/stance/description/rationale still behave like role-level composition law keyed by that role

But the acceptance bar is the same:

- migrated engines must no longer rely on the central hard-coded maps as the authoritative source for:
  - semantic role
  - pattern choice
  - stance choice
  - description/rationale prefixes

4. Handle legacy genealogy aliases explicitly.

Two of the migrated genealogy engine keys are still legacy aliases in compose-adjacent paths:

- `genealogy_pass1b_relationship_classification`
- `genealogy_pass7_final_synthesis`

This slice should not leave their metadata story implicit.

The scope should require one explicit analyzer-side resolution rule so those legacy keys resolve to the canonical capability-definition metadata for:

- `genealogy_relationship_classification`
- `genealogy_final_synthesis`

This avoids pretending the compose-adjacent path is already alias-aware when it is not.

5. Teach `compose_from_intent.py` to read metadata first.

Expected behavior:

- migrated engines resolve role from capability-definition metadata
- migrated engines resolve pattern/stance/description/rationale from extracted role metadata keyed by that resolved role
- unmigrated engines may still fall back to the existing hard-coded maps temporarily

6. Preserve runtime behavior.

This is a behavior-preserving tranche.

That means:

- same routes
- same consumers
- same lifecycle behavior
- same resolver versions
- same rendered structure law
- same proof bundles / proof assertions unless explicitly updated for metadata provenance only

### Explicitly out of scope

- formal output-family taxonomy design as the main deliverable
- new renderer families
- new sub-renderer families
- source-backed `source_profile` lifecycle broadening
- consumer admission generalization
- removal of all hard-coded composition policy in one pass
- host or harness UX changes
- analyzer-side affordance/routing-hint field design or attachment-point design
- broad capability-schema redesign outside the fields needed for `composition_role`
- generic save-schema widening

## Why This Slice Is Next

The strategy reviews were explicit:

- taxonomy will emerge more honestly from extraction than from top-down naming first

This slice is the right next step because it:

1. attacks real analyzer-side coupling instead of adding more shell proof
2. moves the system toward analyzer-v2-as-brain more directly than another host exercise
3. reduces future engine onboarding cost if successful
4. creates a cleaner foundation for any later output-family taxonomy

## Proposed Design Shape

### 1. Metadata first, fallback second

The implementation should be staged:

- capability-definition metadata path for canonical migrated engines
- explicit alias-resolution path for legacy genealogy keys
- role-metadata path for pattern/stance/description/rationale
- fallback path to old maps for everything else

This keeps the tranche bounded and lowers regression risk.

### 2. Keep the extraction local to the current composition seam

The first pass should stay close to `compose_from_intent.py`.

Do not widen this into:

- engine-registry redesign everywhere
- planner redesign
- taxonomy debate about every possible future engine

The goal is smaller:

- prove that current central composition maps can be externalized for the current proved engine set without breaking behavior

### 3. Preserve proof surfaces

This slice should keep existing proof surfaces stable:

- representative composition matrix
- `aoi-canary` proof lines
- standalone harness proof lines
- lifecycle proof lines

If those begin changing materially, the slice is no longer bounded enough.

## Acceptance Bar

This slice should count as complete only if all of the following are true:

1. the currently proved engine set resolves `composition_role`, `preferred_pattern_key`, and `preferred_presentation_stance` from metadata rather than the central hard-coded maps
   - and the equivalent description/rationale prefixes also no longer come from the central hard-coded maps for migrated engines

2. `compose_from_intent.py` still preserves behavior for unmigrated engines through bounded fallback

3. focused analyzer tests prove that migrated engines no longer depend on the old maps for authoritative role/pattern/stance/description/rationale resolution
   - and that legacy genealogy aliases resolve through the explicit analyzer-side alias rule rather than by accidental fallback

4. representative composition behavior remains unchanged on the already-proved matrix:
- AOI `source_profile`
- AOI `source_selection`
- genealogy `direct_sections`

5. current proof-only harness and second-consumer proof lines do not require code changes to stay valid

6. no route shapes, request/response schemas, or lifecycle contracts change in this slice

7. the extraction path is documented clearly enough that a later tranche can decide whether to:
- broaden the metadata layer further
- formalize output families
- or extract more composition-law seams next

## Test Plan

### Analyzer

Add focused tests for:

- migrated engines resolve role/pattern/stance from metadata
- fallback remains intact for unmigrated engines
- representative composition matrix stays unchanged
- served renderer contract tests remain unchanged
- transient proof consumer contract tests remain unchanged

Recommended verification surface:

- `tests/test_compose_from_intent.py`
- `tests/test_representative_composition_matrix.py`
- `tests/test_served_renderer_contract_policy.py`

### No host-side tranche

This slice should require:

- no harness changes
- no `aoi-canary` changes
- no new live browser proof closeout as the primary acceptance bar

If the tranche starts needing host changes to validate the extraction, it is drifting.

## Honest Claim If Completed

If this slice closes honestly, the claim should remain narrow:

- the first layer of current workflow-shaped composition metadata has been extracted out of central presenter code for the currently proved engine set, without changing runtime behavior
- and the existing hint-first resolution path is now backed by authoritative metadata rather than mostly by central fallback maps

It would **not** yet mean:

- output-family taxonomy is solved
- composition law is generalized across all engines
- consumer admission law is generalized
- lifecycle is generalized any further

## What Comes After This

If this slice succeeds, the next honest decision will be better informed.

At that point the program can decide among:

1. broaden metadata extraction further
2. formalize a true output-family taxonomy over the extracted metadata
3. tackle another deeper composition-law seam
4. revisit whether source-backed `source_profile` lifecycle should broaden at all on the current save contract
5. use the completed operations/routing inventory to scope one post-extraction addendum over first-hop semantic-affordance and routing-hint hypotheses only

The important thing is:

- do not skip the extraction step
- do not pretend taxonomy alone solves current coupling
