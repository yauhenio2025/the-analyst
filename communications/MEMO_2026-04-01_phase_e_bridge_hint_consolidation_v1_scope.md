# Memo: Phase E Bridge Hint Consolidation V1 Scope

Subtitle: Remove the remaining bridge-local role-hint duplication for the migrated engine family by deriving emitted hints from canonical capability metadata

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

## Purpose

Define the next bounded analyzer-side step after the completed composition metadata extraction tranche.

That extraction moved semantic-role authority into canonical capability metadata and role-level presentation law into a presenter registry, but it intentionally left one duplicated seam in place:

- bridge-emitted role hints in the AOI source bridge and genealogy saved-result bridge are still hard-coded locally

This memo scopes the smallest honest follow-on:

- consolidate those bridge-emitted hints so they derive from canonical capability metadata instead of from bridge-local literals

This is a cleanup-and-authority tranche, not a new taxonomy tranche and not analyzer-side affordance/routing attachment yet.

## Strategic Decision

The next bounded code step should be:

- bridge-hint consolidation against canonical capability metadata for the already-migrated engine family

not:

- immediate analyzer-side affordance/routing attachment
- lifecycle broadening
- admission-policy extraction
- output-family taxonomy work
- broader engine-schema redesign

The reason is straightforward:

- the extraction tranche answered the metadata-first compose question
- the completed operations/routing inventory gives later affordance work a runtime-first evidence base
- but there is still one obvious duplicated role source on the already-proved line

That duplicated seam should be removed before new analyzer-owned semantic affordances are attached to outputs.

## Current Remaining Duplication

After the extraction closeout, the migrated engine family still carries duplicated role values in bridge-backed paths.

Today the same semantic role can still live in:

1. canonical capability metadata
2. `src/presenter/composition_source_bridge.py`
3. `src/orchestrator/genealogy_saved_result_bridge.py`

The affected bridge-local fields are:

- `composition_role_hint` in the AOI source bridge definitions
- `role_hint` in the genealogy saved-result bridge section specs / emitted traces

The compose matcher already treats bridge hints as highest precedence.
So if those bridge hints stay hard-coded forever, canonical metadata is not yet the only authoritative source on the migrated line.

## Scope

### In scope

1. Add one shared bridge-facing composition-role resolution helper.

That helper should:

- accept a canonical or legacy engine key
- return canonical capability metadata for both canonical and legacy keys
- return one validated `composition_role`
- fail closed for migrated engine-family keys if canonical capability metadata is absent or invalid

This helper should reuse the post-extraction metadata path rather than inventing a second composition-authority mechanism.

2. Consolidate AOI source-bridge role hints.

In:

- `src/presenter/composition_source_bridge.py`

remove bridge-local role authority for the migrated AOI family.

The bridge may still emit `composition_role_hint` in its outputs, but that emitted value should now be derived from canonical capability metadata, not hard-coded in `_SOURCE_FAMILY_DEFINITIONS`.

Keep these AOI bridge concerns unchanged:

- source-family ordering
- titles
- source-backend kind
- profile selection behavior
- output shapes / trace shapes

3. Consolidate genealogy saved-result bridge role hints.

In:

- `src/orchestrator/genealogy_saved_result_bridge.py`

remove bridge-local role authority for the migrated genealogy family.

The bridge may still emit `role_hint` in `DirectSectionsSectionTrace`, but that value should now be derived from canonical capability metadata for the matched engine key, including legacy aliases:

- `genealogy_pass1b_relationship_classification`
- `genealogy_pass7_final_synthesis`

Keep these genealogy bridge concerns unchanged:

- preferred section order
- default titles
- rationales
- output shapes / trace shapes

4. Keep fail-closed semantics aligned with the extraction tranche.

For the migrated engine family, bridge-backed paths should not silently emit stale hard-coded hints if:

- canonical capability metadata cannot be resolved
- `composition_role` is missing
- `composition_role` is invalid

Those cases should fail closed instead of falling back to bridge-local literals.

5. Preserve current behavior and proof surfaces.

This remains a behavior-preserving analyzer-side tranche.

That means:

- no host or harness changes
- no route changes
- no request/response schema changes
- no lifecycle changes
- no admission changes
- no intended rendered-structure changes

### Explicitly out of scope

- role-registry redesign
- output-family taxonomy work
- analyzer-side affordance/routing annotation
- host or harness UX changes
- source-profile lifecycle broadening
- consumer admission extraction
- broader bridge redesign beyond role-hint authority

## Why This Slice Is Next

This is the smallest honest post-extraction step because it does one thing only:

- remove the remaining bridge-local duplication of semantic-role authority on the migrated engine family

It is stronger than jumping directly to affordance/routing attachment because it first makes the already-landed composition metadata story cleaner:

- canonical capability metadata becomes authoritative not only in the compose matcher, but also in the bridge emitters that feed that matcher

It is smaller than broader composition-law work because it does not widen role families, pattern law, or route families.

## Acceptance Bar

This slice should count as complete only if all of the following are true:

1. bridge-local role literals are no longer authoritative for the migrated engine family in:
   - `src/presenter/composition_source_bridge.py`
   - `src/orchestrator/genealogy_saved_result_bridge.py`

2. the AOI source bridge still emits `composition_role_hint`, but that value is now derived from canonical capability metadata for the canonical engine key

3. the genealogy saved-result bridge still emits `role_hint`, but that value is now derived from canonical capability metadata for both canonical and legacy matched engine keys

4. missing or invalid `composition_role` metadata on a migrated bridge-backed engine-family key fails closed rather than being masked by bridge-local literals

5. current bridge output shapes and trace shapes remain unchanged

6. representative proof behavior remains unchanged for:
   - AOI `source_selection`
   - AOI `source_profile`
   - genealogy `direct_sections`

7. no host or harness code changes are required

8. the next analyzer-side step after this slice becomes cleaner to scope:
   - one bounded affordance/routing addendum over first-hop operations only

## Test Plan

### Primary analyzer verification

Add or extend focused tests for:

- AOI source-bridge role hints derive from canonical capability metadata
- genealogy saved-result bridge role hints derive from canonical capability metadata for:
  - canonical keys
  - legacy alias keys
- missing metadata on migrated bridge-backed keys fails closed
- bridge outputs preserve existing field shapes and ordering

Recommended primary verification surface:

- `tests/test_composition_source_bridge.py`
- `tests/test_genealogy_saved_result_bridge.py`
- `tests/test_compose_from_intent.py`

### Stability / regression

Keep the broader proof surfaces unchanged through verification:

- `tests/test_representative_composition_matrix.py`
- `tests/test_transient_proof_harness_contract.py`
- `tests/test_compose_sessions.py`

No new host-side browser proof is the primary acceptance bar here.

## Honest Claim If Completed

If this slice closes honestly, the claim should remain narrow:

- bridge-backed AOI and genealogy composition paths no longer carry their own independent hard-coded semantic-role authority for the migrated engine family; they emit the same role hints as before, but those hints now derive from canonical capability metadata

It would **not** yet mean:

- analyzer-side affordance/routing attachment has begun
- output-family taxonomy is solved
- bridge files are fully generalized
- lifecycle or admission policy are more generic

## What Comes After This

If this slice lands cleanly, the next honest analyzer-side follow-on should be:

- one post-extraction affordance/routing addendum over **first-hop** operations only

That later slice should draw on:

- the completed Close Read operations/routing inventory
- the cleaner post-consolidation composition metadata line

The important sequencing rule remains:

- do not attach new analyzer-owned affordances while the migrated composition-role line still has duplicated bridge-local authority
