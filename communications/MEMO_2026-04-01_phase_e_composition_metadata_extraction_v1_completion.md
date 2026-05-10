# Memo: Phase E Composition Metadata Extraction V1 Completion

Subtitle: Metadata-first semantic-role resolution for the proved engine family, with bridge-role duplication still intentionally deferred

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
Implements:
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`
Most Recent Product Companion Completion:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
Strategy Context:
- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Composition_Metadata_Extraction_V1_Scope_Critique_2026-04-01.md`
- `communications/REPORT_Codex_Phase_E_Composition_Metadata_Extraction_V1_Scope_Audit_2026-04-01.md`

## Purpose

Record completion of the first analyzer-side, behavior-preserving extraction tranche that moved the lowest-risk workflow-shaped composition law out of central presenter code and into metadata for the currently proved engine family.

This slice was meant to answer one bounded question:

- can analyzer-v2 make canonical capability metadata authoritative for semantic role on the current proved AOI/genealogy line, while moving role-level composition law into a presenter registry and preserving current proof behavior?

It was not meant to:

- solve output-family taxonomy
- generalize admission policy
- broaden lifecycle
- attach analyzer-side affordance/routing hints yet
- consolidate every remaining duplicated role seam in one pass

## Outcome

That bounded extraction question is now answered yes.

The landed code now establishes:

1. a shared `CompositionRole` type at the engine layer
2. canonical capability-definition ownership of `composition_role` for the proved AOI/genealogy engine family
3. presenter-owned role-level composition law for:
   - pattern
   - stance
   - description prefix
   - rationale prefix
4. hint-first, metadata-first semantic-role resolution in `compose_from_intent.py`
5. fail-closed enforcement for migrated canonical-or-legacy engine-family keys when `composition_role` metadata is missing or invalid
6. alias-aware capability-metadata preference on adjacent compose/view-generation seams

The honest closeout claim remains narrower than “composition law is generalized”:

- the first workflow-shaped composition maps are now externalized from `compose_from_intent.py` for the currently proved engine family, and migrated semantic-role resolution is metadata-first rather than fallback-map-first

This does not yet mean:

- one authoritative source exists everywhere bridge-backed role hints are emitted
- analyzer-side affordance/routing attachment has begun
- taxonomy is solved
- lifecycle or admission policy are any more general than before

## What Landed

### 1. Shared role type and canonical capability metadata

The engine layer now carries one shared `CompositionRole` type:

- `src/engines/composition_roles.py`

And the capability-definition schema now carries:

- `composition_role`

through:

- `src/engines/schemas_v2.py`

That metadata is populated on the canonical capability YAMLs for the currently proved family:

- `aoi_thematic_synthesis`
- `aoi_engagement_mapping`
- `aoi_sin_findings`
- `aoi_thematic_report`
- `genealogy_relationship_classification`
- `genealogy_final_synthesis`

### 2. Presenter-owned role registry

The role-level composition-law maps no longer live in `compose_from_intent.py`.

They now live in:

- `src/presenter/composition_role_registry.py`

This registry is now authoritative for:

- pattern key
- presentation stance
- description prefix
- rationale prefix

### 3. Metadata-first semantic-role resolution

`src/presenter/compose_from_intent.py` now resolves semantic role in the intended order:

1. valid bridge-emitted role hint
2. canonical capability metadata returned for canonical or legacy keys
3. heuristics only for engines outside the migrated family

Two audit-found hardening points are now explicitly closed:

- if a migrated canonical-or-legacy engine-family key has no capability metadata at all, the matcher now fails closed instead of falling through to title/token heuristics
- if a migrated engine-family key resolves capability metadata but that metadata has no valid `composition_role`, the matcher also fails closed

The regression bar is explicit:

- neutral section titles are used in tests so positive cases do not accidentally rely on title-token hints

### 4. Alias-aware compose-adjacent hardening

The legacy genealogy alias story is now materially cleaner.

Alias-aware capability metadata is now preferred not only on the compose matcher, but also in adjacent seams:

- `src/presenter/dynamic_prompt.py`
- `src/views/generator.py`

For legacy alias keys like:

- `genealogy_pass1b_relationship_classification`
- `genealogy_pass7_final_synthesis`

canonical capability metadata now wins where this tranche touched resolution logic.

### 5. Existing proof surfaces stayed stable

The extraction was kept analyzer-side and behavior-preserving.

There were:

- no host or harness changes
- no route changes
- no request/response schema changes
- no lifecycle changes

The representative composition matrix, proof-only harness line, and compose-session line stayed valid through verification rather than through expectation rewriting.

## What Did Not Land Yet

One deliberate duplication remains:

- `src/presenter/composition_source_bridge.py` still carries bridge-local `composition_role_hint` literals
- `src/orchestrator/genealogy_saved_result_bridge.py` still carries bridge-local `role_hint` literals

That means the current proved engine family still has duplicate role values in:

1. canonical capability metadata
2. AOI source-bridge definitions
3. genealogy saved-result bridge definitions

The extraction tranche made canonical capability metadata authoritative on the compose matcher and adjacent alias-aware resolution seams, but it did **not** yet eliminate those bridge-local duplicates.

That remaining duplication is now the smallest honest next code gap.

## Strategic Implication

The strategy stack is now materially stronger.

The reviews were right about the order:

- extraction first
- product-side operations/routing inventory as companion evidence
- only later analyzer-side affordance/routing attachment

But after this closeout, the next immediate analyzer-side step should no longer be phrased as “start affordance attachment.”

The next bounded step should be:

- one bridge-hint consolidation tranche

That step is smaller and stronger than jumping directly into affordance/routing annotation, because it removes the last obvious duplicated role source on the already-migrated line before new analyzer-owned semantics are attached to composed outputs.

So the honest near-term order is now:

1. composition metadata extraction
2. bridge-hint consolidation against canonical capability metadata
3. post-extraction analyzer-side affordance/routing addendum over first-hop operations only

## Honest Boundary

### What is now true

- semantic role for the currently proved engine family is now metadata-first in the compose matcher
- role-level pattern/stance/description/rationale no longer live in `compose_from_intent.py`
- migrated canonical-or-legacy engine-family keys now fail closed if metadata is absent or invalid
- neutral-title regressions prove that migrated positive and negative cases are not accidentally riding title-token heuristics
- alias-aware capability preference now reaches dynamic prompt and view generation hardening on the touched seams

### What is not yet true

- bridge-emitted role hints are not yet consolidated to the canonical metadata source
- analyzer-side affordance/routing annotations are not yet attached to outputs
- output-family taxonomy is not yet formalized
- admission and lifecycle seams are not more general than they were before this slice
- the broader `Close Read` product direction is not yet a build memo

## Verification

Implementation verification:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_genealogy_saved_result_bridge.py tests/test_representative_composition_matrix.py tests/test_served_renderer_contract_policy.py`
  - `70 passed, 2 warnings`
- `PYTHONPATH=. pytest -q tests/test_transient_proof_harness_contract.py tests/test_compose_sessions.py`
  - `8 passed`

Docs pass note:

- no additional tests were run while writing this completion memo
