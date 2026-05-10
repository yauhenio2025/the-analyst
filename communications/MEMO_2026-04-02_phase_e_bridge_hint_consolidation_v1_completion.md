# Memo: Phase E Bridge Hint Consolidation V1 Completion

Subtitle: AOI and genealogy bridge-emitted role hints now derive from canonical capability metadata on the migrated line

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
Implements:
- `communications/MEMO_2026-04-01_phase_e_bridge_hint_consolidation_v1_scope.md`
Most Recent Code Completion:
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
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

Record completion of the small post-extraction cleanup slice that removed the last migrated bridge-local semantic-role literals on the AOI source bridge and genealogy saved-result bridge.

This slice was meant to answer one bounded question:

- can the already-migrated AOI/genealogy bridge-backed paths keep emitting the same role hints as before, while deriving those hints from canonical capability metadata instead of bridge-local literals?

It was not meant to:

- start analyzer-side affordance/routing attachment
- widen lifecycle
- redesign bridge contracts broadly
- change compose precedence
- change host or harness behavior

## Outcome

That bounded cleanup question is now answered yes.

The landed code now establishes:

1. one thin validated bridge-role resolver in the engine layer, built directly on existing alias-aware capability discovery
2. AOI source-bridge hint emission derived from canonical capability metadata at candidate-construction time
3. genealogy saved-result hint emission derived from canonical capability metadata only after the concrete matched row is known
4. unchanged downstream compose precedence and fail-closed defense-in-depth on the migrated line

The honest closeout claim remains narrow:

- the migrated AOI and genealogy bridge-backed paths still emit the same semantic-role hints as before, but those hints no longer come from independent bridge-local literals

This does **not** yet mean:

- analyzer-v2 now emits first-hop affordance/routing annotations
- destination lifecycle is modeled upstream
- job-backed presentation surfaces carry the same analyzer-side semantic hints
- bridge files are generalized beyond the migrated line

## What Landed

### 1. Thin validated bridge-role resolver

The engine layer now carries one tiny bridge-facing convenience helper in:

- `src/engines/discovery.py`

That helper:

- accepts canonical or legacy engine keys
- resolves canonical capability metadata through the existing alias-aware discovery seam
- returns one validated `CompositionRole`
- raises a small local `CapabilityMetadataResolutionError` when metadata is missing or invalid

This keeps the bridge call sites explicit without inventing a new metadata subsystem.

### 2. AOI source bridge now derives hints before payload lookup

In:

- `src/presenter/composition_source_bridge.py`

the AOI bridge no longer stores bridge-local `composition_role_hint` literals in `_SOURCE_FAMILY_DEFINITIONS`.

Instead:

- role resolution now happens during candidate construction
- it happens before artifact or report payload lookup
- missing or invalid metadata converts the candidate into the bridge’s existing `invalid` state with:
  - empty `composition_role_hint`
  - explicit `resolution_note`
- required selections still fail through the existing `ComposeFromSourceResolutionError` path

This preserved the AOI bridge’s candidate-state semantics while removing the duplicated authority.

### 3. Genealogy saved-result bridge now derives hints from the matched row

In:

- `src/orchestrator/genealogy_saved_result_bridge.py`

`_PreferredGenealogySection` no longer stores `role_hint`.

That spec now stays responsible only for:

- engine-key ordering
- default title
- rationale

After `_first_matching_output(...)` determines the concrete matched row, the bridge now derives `role_hint` from the actual matched `engine_key`, including legacy-key matches like:

- `genealogy_pass1b_relationship_classification`
- `genealogy_pass7_final_synthesis`

If migrated metadata is missing or invalid for the matched row, the bridge now raises `GenealogySavedResultBridgeError` instead of emitting a stale hard-coded hint.

### 4. Downstream authority chain stayed intentionally unchanged

This slice did **not** change:

- `src/presenter/compose_from_intent.py`
- `src/presenter/dynamic_prompt.py`
- `src/views/generator.py`

So the post-close chain is now:

1. canonical capability metadata owns `composition_role`
2. bridges derive emitted hints from that metadata
3. the compose matcher still treats valid hints as highest precedence
4. the compose matcher remains the deeper migrated-family fail-closed backstop

## What Stayed Stable

The bridge consolidation was kept behavior-preserving:

- no host changes
- no harness changes
- no route changes
- no request/response schema changes
- no lifecycle changes
- no intended rendered-structure changes

The existing proof surfaces stayed stable through verification:

- AOI source bridge behavior
- genealogy `direct_sections`
- representative composition matrix
- proof-only harness contract
- compose-session line

## What Did Not Land Yet

This slice closes the remaining migrated bridge-local role-literal duplication, but it does **not** yet start the next semantic layer.

Not yet landed:

- analyzer-side first-hop affordance/routing annotations on composed outputs
- destination-lifecycle hints
- output-specific operation families like findings-to-Arsenal or outline upgrades
- job-backed page/manifest affordance propagation
- host UX changes for consuming analyzer-owned affordances

Those are still later questions.

## Strategic Implication

The near-term Phase E sequence is now cleaner:

1. composition metadata extraction
2. bridge-hint consolidation
3. bounded first-hop affordance/routing addendum

The product-side inventory already told us where to start:

- first-hop operations only
- runtime-real evidence first
- no destination-lifecycle absorption

After this closeout, the next honest analyzer-side step should now be:

- one bounded first-hop affordance/routing addendum over transient compose surfaces only

The right starting family is still the one already singled out by the inventory:

- capture/comment eligibility plus bounded allowed destinations on rendered analytical surfaces

## Honest Boundary

### What is now true

- migrated bridge-backed AOI and genealogy paths no longer carry independent bridge-local semantic-role literals
- emitted AOI `composition_role_hint` values now derive from canonical capability metadata before artifact/report lookup
- emitted genealogy `role_hint` values now derive from canonical capability metadata for the concrete matched row, including legacy-key matches
- missing or invalid migrated metadata now fails closed at the bridge in ways consistent with existing AOI and genealogy bridge semantics
- existing proof surfaces stayed behaviorally stable

### What is not yet true

- analyzer-v2 does not yet attach first-hop affordance/routing hints to transient composed views
- the `Close Read` flagship direction is not yet a build memo
- destination-internal lifecycle is not modeled upstream
- job-backed page and manifest surfaces do not yet carry the same semantic-affordance hints

## Verification

Implementation verification:

- `PYTHONPATH=. pytest -q tests/test_composition_source_bridge.py tests/test_genealogy_saved_result_bridge.py tests/test_compose_from_intent.py tests/test_representative_composition_matrix.py tests/test_transient_proof_harness_contract.py tests/test_compose_sessions.py`
  - `75 passed, 2 warnings`
- `python -m compileall src/engines/discovery.py src/presenter/composition_source_bridge.py src/orchestrator/genealogy_saved_result_bridge.py tests/test_composition_source_bridge.py tests/test_genealogy_saved_result_bridge.py tests/test_compose_from_intent.py`
  - passed

Docs pass note:

- no additional tests were run while writing this completion memo
