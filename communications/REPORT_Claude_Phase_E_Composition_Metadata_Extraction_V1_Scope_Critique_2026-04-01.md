# Critique: Phase E Composition Metadata Extraction V1 Scope

Reviewer: Claude (Opus 4.6, fresh session)
Date: 2026-04-01
Subject Memo: `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`

---

## 1. Verdict

**Approve with corrections.**

This is the right next analyzer-side slice. The strategic sequencing is sound, the extraction target is correct, the scope is genuinely bounded, and the behavior-preserving discipline is the right operational constraint. But the memo has three honest gaps: it does not acknowledge that partial extraction already exists in two bridge files, it overstates how uniform the metadata situation is across AOI and genealogy engines, and it leaves the storage-location question too open for a scope memo that should be implementable by a fresh session.

---

## 2. Strongest Parts Of The Memo

### A. The extraction target is correct and code-backed

The three central maps are real, declarative, and the lowest-risk composition-law extraction target:

| Map | Location | Entries | Nature |
|-----|----------|---------|--------|
| `_ROLE_FROM_ENGINE_KEY` | `compose_from_intent.py:110-119` | 8 | engine -> semantic role |
| `_LEAF_PATTERN_BY_ROLE` | `compose_from_intent.py:82-88` | 5 | role -> view pattern |
| `_PRESENTATION_STANCE_BY_ROLE` | `compose_from_intent.py:89-95` | 5 | role -> stance |

These are already dictionaries, not procedural branching. Moving their authority from central code to metadata is genuinely low-risk refactoring, not architecture invention. The memo correctly identifies them as the first target.

### B. The explicitly-out-of-scope list is disciplined

The memo correctly defers:

- `_SUPPORTED_HANDOFF_KINDS` (workflow admission policy)
- `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` (consumer admission policy)
- `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER` (consumer-profile admission)

These encode operational policy, not composition metadata. The memo's instinct to separate composition-law extraction from admission-policy extraction is the right sequencing. All four prior reviews converge on this.

### C. The behavior-preserving constraint is the right discipline

The memo does not propose changing any routes, consumers, lifecycle, or renderer law. That is correct. Any slice that tries to combine extraction with runtime behavior changes would be a different, riskier tranche.

### D. The honest-claim section is accurately bounded

The memo explicitly names what completion would NOT mean (output-family taxonomy solved, composition law generalized, consumer admission generalized, lifecycle generalized). That honesty prevents scope creep and sets up the next decision correctly.

### E. Sequencing after the runtime-first inventory companion is correct

The completed operations/routing inventory sharpened the product-side picture but did not change the next code move. The memo correctly reads this: extraction first, affordance/routing attachment later. Both Claude and Codex prior reviews agreed independently.

---

## 3. Weakest Assumptions

### A. The memo does not acknowledge that partial extraction already exists

This is the most significant gap.

Two bridge files already carry `composition_role_hint` as structured metadata for the AOI and genealogy composition paths:

**AOI source bridge** (`src/presenter/composition_source_bridge.py:45-70`):

```python
_SOURCE_FAMILY_DEFINITIONS = {
    "thematic_synthesis": {"composition_role_hint": "synthesis_primary", ...},
    "engagement_mapping": {"composition_role_hint": "comparison_map", ...},
    "sin_findings": {"composition_role_hint": "findings_bank", ...},
    "thematic_report": {"composition_role_hint": "report_closeout", ...},
}
```

**Genealogy saved-result bridge** (`src/orchestrator/genealogy_saved_result_bridge.py:33-49`):

```python
_PREFERRED_GENEALOGY_SECTION_ORDER = (
    _PreferredGenealogySection(
        engine_keys=("genealogy_relationship_classification", "genealogy_pass1b_relationship_classification"),
        role_hint="comparison_map", ...
    ),
    _PreferredGenealogySection(
        engine_keys=("genealogy_final_synthesis", "genealogy_pass7_final_synthesis"),
        role_hint="report_closeout", ...
    ),
)
```

This means:

- For the `compose_from_source` and `compose_from_selection` handoff kinds, `_ROLE_FROM_ENGINE_KEY` is already NOT the authoritative source. The role hint flows through the bridge as structured metadata, and `_resolve_semantic_role()` at line 778 checks `context.composition_role_hint` FIRST before falling back to `_ROLE_FROM_ENGINE_KEY`.
- For the `direct_sections` handoff kind, `_ROLE_FROM_ENGINE_KEY` IS still the central authority for the AOI path, but the genealogy path already carries `role_hint` through the saved-result bridge.

This matters for the scope memo because the extraction is EASIER than it appears for some paths (the bridge already carries the metadata) and HARDER for one specific path (AOI `direct_sections` coming from raw `compose_from_intent` with no bridge). The memo should name this asymmetry to avoid an implementor designing a uniform solution for a non-uniform problem.

### B. The memo overstates metadata uniformity across AOI and genealogy engines

The 8-engine migrated set is asymmetric in a way the memo does not acknowledge:

| Engine | Has capability definition (yaml)? | Has `output_contract` in capability def? | Has `output_mode: json`? | Has legacy JSON definition? | Legacy status |
|--------|----------------------------------|----------------------------------------|-------------------------|---------------------------|---------------|
| `aoi_thematic_synthesis` | Yes | Yes | Yes | No | N/A |
| `aoi_engagement_mapping` | Yes | Yes | Yes | No | N/A |
| `aoi_sin_findings` | Yes | Yes | Yes | No | N/A |
| `aoi_thematic_report` | Yes | Yes | Yes | No | N/A |
| `genealogy_relationship_classification` | Yes | **No** | **No** | No | N/A |
| `genealogy_pass1b_relationship_classification` | **No** (uses legacy JSON) | **No** | **No** | Yes | **deprecated** |
| `genealogy_final_synthesis` | Yes | **No** | **No** | No | N/A |
| `genealogy_pass7_final_synthesis` | **No** (uses legacy JSON) | **No** | **No** | Yes | **deprecated** |

This creates three concrete implementation questions the memo leaves unresolved:

1. **Where do composition metadata fields live for engines that have capability definitions?** The `composability` field already exists in capability definitions (via `schemas_v2.py:328-331`), but it describes engine-to-engine data sharing (`shares_with`, `consumes_from`), not renderer/UI composition law. Adding `composition_role`, `preferred_pattern_key`, `preferred_presentation_stance` as new top-level fields or as a new sub-block is a schema decision the scope memo should take a position on.

2. **Where does composition metadata live for deprecated legacy engines?** `genealogy_pass1b_relationship_classification.json` has `"status": "deprecated"` with `"deprecated_reason": "Built-in prompt in orchestrator; engine definition unused."` Yet it appears in `_ROLE_FROM_ENGINE_KEY`. If we are moving the metadata into engine definitions, which file carries it for a deprecated engine whose JSON definition is explicitly marked unused?

3. **Is the right storage location the capability definition layer or a separate composition-metadata layer?** The AOI engines already have rich capability definitions with `output_contract`. The genealogy engines do not. Adding composition metadata to capability definitions means the genealogy engines need either (a) new capability definitions with the composition fields, or (b) a separate metadata layer that works alongside both legacy JSON and capability-definition engines. The memo acknowledges this question in passing ("extension of current engine capability definitions or one adjacent registry-backed composition metadata definition layer") but should commit to one approach to avoid an implementor making an arbitrary choice.

### C. The memo does not account for `_ROLE_DESCRIPTION_PREFIX` and `_ROLE_RATIONALE_PREFIX`

The memo lists three maps to externalize (`_ROLE_FROM_ENGINE_KEY`, `_LEAF_PATTERN_BY_ROLE`, `_PRESENTATION_STANCE_BY_ROLE`). But there are two additional declarative maps of the same character at `compose_from_intent.py:96-109`:

- `_ROLE_DESCRIPTION_PREFIX` — 5 entries mapping role -> description prefix
- `_ROLE_RATIONALE_PREFIX` — 5 entries mapping role -> rationale prefix

These are consumed directly at lines 767-769 when building `_PlannerRow`:

```python
description=f"{_ROLE_DESCRIPTION_PREFIX[semantic_role]} for {title}.",
presentation_stance=_PRESENTATION_STANCE_BY_ROLE[semantic_role],
rationale=_ROLE_RATIONALE_PREFIX[semantic_role],
```

If `composition_role`, `preferred_pattern_key`, and `preferred_presentation_stance` are externalized but `_ROLE_DESCRIPTION_PREFIX` and `_ROLE_RATIONALE_PREFIX` remain hard-coded, the extraction is only partial. These are the same kind of composition law and should at minimum be acknowledged in scope.

---

## 4. Code-Backed Findings

### Finding 1: `_resolve_semantic_role()` already prioritizes metadata over the central map

The existing resolution chain at `compose_from_intent.py:778-800`:

```python
def _resolve_semantic_role(context: _PlannerSectionContext) -> str:
    role_hint = (context.composition_role_hint or "").strip()
    if role_hint in _ROLE_HINTS:
        return role_hint

    engine_role = _ROLE_FROM_ENGINE_KEY.get(context.engine_key)
    if engine_role is not None:
        return engine_role

    # ... title-token heuristic fallback
```

This means:

- If a `composition_role_hint` is provided and valid, the central map is already bypassed
- The bridge-backed paths (`compose_from_source`, `compose_from_selection`, genealogy `direct_sections`) already flow through this and already carry hints
- The extraction target is narrower than it appears: the main gap is that raw `compose_from_intent` with the `direct_sections` AOI handoff does not carry bridge-provided hints, so those fall through to `_ROLE_FROM_ENGINE_KEY`

This is good news for the tranche: the resolver architecture already supports metadata-first resolution. The work is about making the metadata authoritative for all paths, not about inventing a new resolver.

### Finding 2: Only 4 of ~28 capability definitions have `output_contract`

A grep across `src/engines/capability_definitions/` shows `output_contract` only in:

- `aoi_thematic_synthesis.yaml`
- `aoi_engagement_mapping.yaml`
- `aoi_sin_findings.yaml`
- `aoi_thematic_report.yaml`

No genealogy capability definition has `output_contract` or `output_mode: json`. This confirms the asymmetry finding above.

### Finding 3: The `composability` field in capability definitions is about engine-to-engine sharing, not UI composition

Inspecting `src/engines/schemas_v2.py:328-331` and the actual `composability` blocks in yaml files:

```yaml
composability:
  shares_with:
    themes: Stable theme inventory with theme names and claims.
    source_documents: Explicit list of source documents used...
  consumes_from: {}
  synergy_engines:
    - aoi_engagement_mapping
```

This describes data handoff between engines in a pipeline, NOT composition role, preferred renderer, or presentation stance. Adding the new composition metadata fields alongside `composability` would be semantically clean (both are about how engines relate to the broader system), but an implementor should not confuse the two.

### Finding 4: The three composition entry paths use role hints differently

| Entry path | How role hint arrives | Central map authority? |
|---|---|---|
| `compose_from_intent` (AOI direct_sections) | Raw prose sections, no bridge | Yes — `_ROLE_FROM_ENGINE_KEY` is authoritative |
| `compose_from_source` (AOI source_profile) | Bridge provides `composition_role_hint` from `_SOURCE_FAMILY_DEFINITIONS` | No — bridge metadata takes priority |
| `compose_from_selection` (AOI source_selection) | Bridge provides `composition_role_hint` from source candidates | No — bridge metadata takes priority |
| Genealogy direct_sections | Saved-result bridge provides `role_hint` from `_PREFERRED_GENEALOGY_SECTION_ORDER` | No — bridge metadata takes priority |

So the central map `_ROLE_FROM_ENGINE_KEY` is actually authoritative only for one specific path: AOI `direct_sections` via raw `compose_from_intent`. For the other three proved paths, partial extraction has already happened through the bridge metadata.

### Finding 5: Existing tests cover the right surfaces

- `tests/test_compose_from_intent.py` — 38+ tests covering request validation, section matching, planner row generation, consumer adaptation, all three entry points
- `tests/test_representative_composition_matrix.py` — 3 matrix cases (AOI source_profile, AOI source_selection, genealogy direct_sections) with proof bundles
- `tests/test_served_renderer_contract_policy.py` — strict/shadow/warn policy resolution

These are the right verification surfaces. The extraction tranche should add tests that prove metadata-first resolution for migrated engines and fallback for unmigrated engines, without changing the existing test expectations.

---

## 5. Strategic Implications For The Roadmap

### 5.1 This is the right next slice, but the implementation should be informed by the partial-extraction asymmetry

The scope is correct. But the implementation plan should explicitly account for:

- Bridge-backed paths already resolve from metadata — the extraction only needs to make that authoritative and add the missing composition fields to engine definitions
- The raw `compose_from_intent` AOI `direct_sections` path is the one where the extraction requires new metadata to flow

### 5.2 The storage-location decision should be settled in the scope, not left to the implementor

The memo offers two options: extend capability definitions or create a separate composition-metadata layer. The code evidence points clearly toward extending capability definitions:

- The `composability` field already exists as a natural neighbor
- 4 AOI engines already have `output_contract` — composition metadata is a natural extension
- The genealogy capability definitions need composition fields regardless of where they live
- A separate registry would add load-time complexity for minimal benefit at this scale (8 engines)

The recommendation: the scope should commit to capability-definition extension and not leave this open.

### 5.3 The deprecated-engine question is real but bounded

For `genealogy_pass1b_relationship_classification` and `genealogy_pass7_final_synthesis`, the simplest solution is to put composition metadata on their capability-definition counterparts (`genealogy_relationship_classification` and `genealogy_final_synthesis`) and add a `legacy_engine_key` mapping (which already exists in `genealogy_relationship_classification.yaml:535`). The deprecated JSON definitions should not be the metadata authority.

### 5.4 This slice does not block the operations/routing inventory follow-on

The completed inventory companion correctly deferred affordance/routing attachment until after this extraction lands. That sequencing remains correct. Nothing in this scope requires or blocks the later affordance work.

---

## 6. Concrete Corrections And Reframing

### Correction 1: Acknowledge existing partial extraction

Add a subsection under "Current Coupling Target" that names:

- `composition_source_bridge.py:45-70` already carries `composition_role_hint` for AOI source-backed paths
- `genealogy_saved_result_bridge.py:33-49` already carries `role_hint` for genealogy direct-sections
- `_resolve_semantic_role()` already checks `composition_role_hint` first
- The extraction is therefore about making metadata universally authoritative and filling gaps, not about inventing a new resolution path

### Correction 2: Name the AOI-genealogy metadata asymmetry

Add to the scope:

- AOI capability definitions already have `output_contract` and `output_mode: json` — these are metadata-rich
- Genealogy capability definitions have `composability.shares_with` but no `output_contract` — they are metadata-poorer
- Deprecated legacy JSON definitions should not become the new metadata authority
- The capability-definition layer should be the single metadata storage location

### Correction 3: Commit to capability-definition extension as the storage location

Replace:

> "The exact storage location may be: extension of current engine capability definitions or one adjacent registry-backed composition metadata definition layer"

With:

> "Composition metadata should be added as new fields in engine capability definitions. The `composability` block already provides a natural neighbor. For engines that only have legacy JSON definitions, either add capability definitions or add a `composition_metadata` section to the legacy JSON."

### Correction 4: Include `_ROLE_DESCRIPTION_PREFIX` and `_ROLE_RATIONALE_PREFIX` in the extraction target

These two maps are the same kind of composition law as the three already identified. If composition_role is externalized, the description and rationale for that role should travel with it. Add them to the "at least" metadata list, or explicitly note them as deferred-to-next-tranche.

### Correction 5: Clarify the scope of "migrated engines no longer rely on central maps"

The acceptance bar says:

> "migrated engines must no longer rely on the central hard-coded maps as the authoritative source"

This should be clarified to mean:

- For bridge-backed paths (source_profile, source_selection, genealogy direct_sections): verify that composition metadata in capability definitions is the single source of truth, and bridge definitions reference it rather than duplicating it
- For raw compose_from_intent (AOI direct_sections): verify that metadata-first resolution works and falls back only for unmigrated engines
- The central maps may remain in code as a fallback but should no longer be the authority for any migrated engine on any path

---

## Summary

The memo scopes the right slice at the right time. The extraction target is code-backed, the sequencing is review-validated, the behavior-preserving constraint is disciplined, and the out-of-scope boundaries are correct.

The corrections are about implementability, not direction:

1. Name the partial extraction that already exists in two bridge files
2. Name the AOI-genealogy metadata asymmetry honestly
3. Commit to capability-definition extension as the storage location
4. Include `_ROLE_DESCRIPTION_PREFIX` and `_ROLE_RATIONALE_PREFIX` or explicitly defer them
5. Clarify what "no longer rely on central maps" means across the four proved composition paths

With these corrections, the scope is ready for implementation.
