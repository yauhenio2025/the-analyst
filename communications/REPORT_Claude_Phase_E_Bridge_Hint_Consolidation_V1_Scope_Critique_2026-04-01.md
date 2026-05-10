# Critique: Phase E Bridge Hint Consolidation V1 Scope

Reviewer: Claude (Opus 4.6, fresh session)
Date: 2026-04-01
Subject Memo: `communications/MEMO_2026-04-01_phase_e_bridge_hint_consolidation_v1_scope.md`

---

## 1. Verdict

**Approve with corrections.**

This is the right next analyzer-side slice. The sequencing logic is sound: extraction landed, bridge-local duplication is the last obvious seam before affordance/routing work makes sense. The scope is genuinely bounded and the memo resists scope creep well. But it has three honest gaps: it understates the mechanical simplicity of the actual change, it does not specify how the shared helper should handle the genealogy bridge's multi-key lookup pattern, and it overspecifies the fail-closed requirement in a way that could create a live regression if the helper is not carefully aligned with the compose matcher's existing fail-closed logic.

---

## 2. Strongest Parts Of The Memo

### A. The sequencing argument is code-backed and correct

The memo correctly identifies that after the extraction tranche, bridge-local role hints are the single remaining duplicated authority for the migrated engine family. The evidence is concrete:

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
        role_hint="comparison_map", ...),
    _PreferredGenealogySection(
        engine_keys=("genealogy_final_synthesis", "genealogy_pass7_final_synthesis"),
        role_hint="report_closeout", ...),
)
```

Both still carry hard-coded role literals. The same values now exist as canonical capability metadata:

| Engine | YAML `composition_role` | Bridge-local literal |
|--------|------------------------|---------------------|
| `aoi_thematic_synthesis` | `synthesis_primary` | `synthesis_primary` |
| `aoi_engagement_mapping` | `comparison_map` | `comparison_map` |
| `aoi_sin_findings` | `findings_bank` | `findings_bank` |
| `aoi_thematic_report` | `report_closeout` | `report_closeout` |
| `genealogy_relationship_classification` | `comparison_map` | `comparison_map` |
| `genealogy_final_synthesis` | `report_closeout` | `report_closeout` |

All six values are currently identical across both sources. The duplication is real and the removal is low-risk.

### B. The scope boundaries are disciplined

The memo correctly defers:

- role-registry redesign
- output-family taxonomy
- affordance/routing annotation
- lifecycle broadening
- consumer admission extraction
- broader bridge redesign

That is the right list. None of those should be combined with this cleanup.

### C. The "what comes after" framing is correct

The memo correctly identifies the next step after this slice: one post-extraction affordance/routing addendum over first-hop operations only, drawing on the completed Close Read operations/routing inventory. That sequencing aligns with both the extraction completion memo and both prior reviews.

### D. The honest-claim section is accurately bounded

The memo explicitly names what completion would NOT mean. That honesty prevents the slice from being misread as broader composition-law generalization.

---

## 3. Weakest Assumptions

### A. The memo overspecifies the fail-closed requirement without aligning it with existing code

The memo says:

> bridge-backed paths should not silently emit stale hard-coded hints if canonical capability metadata cannot be resolved

This sounds right in principle. But the actual compose matcher in `compose_from_intent.py:759-797` already has its own fail-closed logic for the migrated engine family:

```python
def _resolve_semantic_role(context: _PlannerSectionContext) -> str:
    role_hint = (context.composition_role_hint or "").strip()
    if role_hint in COMPOSITION_ROLE_HINTS:
        return role_hint
    # ... capability metadata lookup ...
    # ... fail-closed for migrated keys if metadata absent/invalid ...
```

The compose matcher checks `context.composition_role_hint` first (line 760-762). If the bridge still emits a valid hint from canonical metadata, the compose matcher will accept it immediately and never reach its own metadata lookup. If the bridge fails closed by raising an error or emitting an empty hint, the compose matcher will then perform its own metadata lookup and its own fail-closed enforcement.

The risk is: if the new bridge helper fails closed *differently* from the compose matcher's existing fail-closed behavior (e.g., different error type, different error message, different conditions), this creates a confusing double-enforcement where the system may raise from the bridge on some edge cases and from the compose matcher on others.

**Correction needed**: The memo should specify whether bridge-level fail-closed should raise immediately (preventing the section from reaching compose at all) or whether it should emit an empty/absent hint and let the compose matcher's existing fail-closed logic handle enforcement. The cleaner design is probably the latter: the bridge emits the derived value or emits nothing, and the compose matcher remains the single fail-closed enforcement point for the migrated family. This avoids introducing a second enforcement layer.

### B. The memo does not specify how the shared helper handles the genealogy bridge's multi-key lookup

The AOI source bridge is mechanically simple: each `_SOURCE_FAMILY_DEFINITIONS` entry maps to exactly one canonical engine key. The helper just calls `resolve_capability_definition(registry, engine_key)` and reads `.composition_role`.

The genealogy bridge is different. Each `_PreferredGenealogySection` carries a *tuple* of engine keys:

```python
engine_keys=("genealogy_relationship_classification", "genealogy_pass1b_relationship_classification")
```

The bridge iterates through this tuple to find matching phase outputs. The engine key that actually appears in the phase output could be either the canonical key or the legacy alias. The helper must be specified clearly on this point:

- Does it accept the engine key from the *matched phase output* (which could be a legacy key)?
- Or does it accept the canonical key from the section spec?

The existing `resolve_capability_definition` in `src/engines/discovery.py:59-71` already handles both: it first tries a direct lookup, then scans all capability definitions for a `legacy_engine_key` match. So the helper can accept either key. But the memo should state this explicitly rather than leaving it as an implementation detail.

### C. The memo overstates how much consolidation is mechanically needed

The actual code change is quite small:

1. **AOI source bridge**: Replace the 4 hard-coded `composition_role_hint` values in `_SOURCE_FAMILY_DEFINITIONS` with a lookup into canonical capability metadata via the shared helper. The `engine_key` for each entry is already known.

2. **Genealogy bridge**: Replace the 2 hard-coded `role_hint` values in `_PREFERRED_GENEALOGY_SECTION_ORDER` with a lookup into canonical capability metadata for the matched engine key.

This is 6 literal string replacements backed by one small helper function. The memo frames this as if it requires a "shared bridge-facing composition-role resolution helper" (scope item 1), which is a correct but slightly heavier framing than necessary. The helper is essentially: call `resolve_capability_definition`, read `.composition_role`, validate it.

This is not a criticism of the scope -- if anything, the smallness of the change strengthens the case for doing it. But the memo should be honest that this is a ~50-line change with a small test update, not a multi-day effort.

---

## 4. Code-Backed Findings

### Finding 1: The compose matcher already treats bridge hints as highest precedence -- this is correct and important

`compose_from_intent.py:759-762`:
```python
def _resolve_semantic_role(context: _PlannerSectionContext) -> str:
    role_hint = (context.composition_role_hint or "").strip()
    if role_hint in COMPOSITION_ROLE_HINTS:
        return role_hint
```

Bridge-emitted hints bypass the capability metadata lookup entirely. So if bridge hints stay hard-coded, canonical metadata is functionally irrelevant for bridge-backed paths. The memo correctly identifies this as the problem.

### Finding 2: The AOI bridge threads `composition_role_hint` through multiple dataclasses

The hard-coded hint travels through:
- `_SOURCE_FAMILY_DEFINITIONS` (line 46-70) -> `CompositionSourceCandidate.composition_role_hint` (line 117) -> `CompositionMaterializedSection.composition_role_hint` (line 230) -> `_PlannerSectionContext.composition_role_hint` in compose_from_intent

This is a pass-through chain, not a transformation chain. The hint is never modified after initial assignment. So replacing the source (the dict literal) with a metadata lookup is safe. The downstream dataclass fields remain unchanged.

### Finding 3: The genealogy bridge threads `role_hint` through `DirectSectionsSectionTrace`

`genealogy_saved_result_bridge.py:127-141`:
```python
trace_rows.append(
    DirectSectionsSectionTrace(
        ...
        role_hint=spec.role_hint,
        ...
    )
)
```

Similarly a direct pass-through. Replacing `spec.role_hint` with a metadata-derived value is safe as long as the value is the same string.

### Finding 4: Both `dynamic_prompt.py` and `views/generator.py` already use alias-aware resolution

Both files import and call `resolve_capability_definition` from `src/engines/discovery.py`, which handles legacy alias keys. So the alias-aware resolution pattern already exists and is tested in adjacent code. The new bridge helper should reuse this same function.

### Finding 5: All 6 canonical capability YAMLs already carry `composition_role`

Verified by direct inspection:
- `aoi_thematic_synthesis.yaml:90` -> `composition_role: synthesis_primary`
- `aoi_engagement_mapping.yaml:80` -> `composition_role: comparison_map`
- `aoi_sin_findings.yaml:89` -> `composition_role: findings_bank`
- `aoi_thematic_report.yaml:72` -> `composition_role: report_closeout`
- `genealogy_relationship_classification.yaml:540` -> `composition_role: comparison_map`
- `genealogy_final_synthesis.yaml:689` -> `composition_role: report_closeout`

The metadata is present, typed correctly (all are valid `CompositionRole` literals), and matches the bridge-local hard-coded values exactly.

### Finding 6: Existing tests verify bridge-emitted role hints by value

`tests/test_genealogy_saved_result_bridge.py:58-60`:
```python
assert [trace.role_hint for trace in handoff.section_trace] == [
    "comparison_map",
    "report_closeout",
]
```

These tests assert the exact string values. After consolidation, the same values should emerge from canonical metadata. The tests should not need rewriting -- they should pass unchanged, which is a natural behavioral equivalence check.

---

## 5. Strategic Implications For The Roadmap

### A. This slice removes the last obvious prerequisite for honest affordance/routing work

The sequencing rule in the extraction completion memo is correct:

> do not attach new analyzer-owned affordances while the migrated composition-role line still has duplicated bridge-local authority

After this slice, the migrated engine family will have one canonical source of `composition_role` truth (the YAML metadata), consumed through one resolution path (the shared helper / `resolve_capability_definition`), with no bridge-local overrides. That makes the subsequent affordance/routing addendum cleaner to scope.

### B. The slice is small enough that it should not delay affordance/routing work significantly

Given the mechanical simplicity (6 literal replacements + 1 small helper + test verification), this should be a fraction of a session. It should not be padded into a multi-day effort.

### C. The Close Read inventory remains the right product-side companion for the next code move

The operations/routing inventory (`communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`) provides runtime-first evidence for what affordance/routing hints to attach. That evidence base is not consumed by this cleanup slice -- it waits for the follow-on.

---

## 6. Concrete Corrections Or Reframing

### Correction 1: Clarify fail-closed enforcement ownership

The memo should specify that bridge-level fail-closed means: if canonical metadata cannot be resolved for a migrated engine-family key, the bridge should raise or return an error that prevents the section from being constructed at all. It should NOT mean: the bridge silently emits an empty hint and hopes the downstream compose matcher catches it. The existing compose matcher fail-closed logic should remain as a defense-in-depth backup, not as the primary enforcement point for bridge-backed paths.

Alternatively, the simpler design: bridges emit the resolved value or raise before constructing the candidate/section. This keeps enforcement at the point of origin.

### Correction 2: Specify how the helper handles the genealogy multi-key pattern

The memo should add one sentence: "The helper must accept any key from the genealogy bridge's engine-key tuple (canonical or legacy) and resolve to the canonical capability definition through the existing `resolve_capability_definition` alias bridge."

### Correction 3: Be honest about the size of this slice

The memo should acknowledge that this is a small, focused cleanup, not a multi-file refactoring effort. Framing it as larger than it is risks inflating the effort estimate and delaying the more important affordance/routing follow-on.

### Correction 4: Do not introduce the shared helper as a new authority layer

The memo proposes "one shared bridge-facing composition-role resolution helper." That is fine mechanically, but the memo should be clear that this helper is a convenience wrapper around `resolve_capability_definition` + `.composition_role`, not a new authority layer. Canonical capability metadata remains the authority. The helper is syntactic sugar for bridge callsites.

---

## Bottom Line

Approve the memo after the four corrections above. The sequencing is right: extraction landed, bridge duplication is the one remaining obvious seam, and removing it before starting affordance/routing work is the correct order. The scope is genuinely bounded. The mechanical change is small and low-risk. The main improvement needed is more precision about fail-closed enforcement ownership and the genealogy multi-key pattern, plus honesty about the slice's small size.

This is the most defensible immediate next analyzer-side code move.

**Verification Note**

This was a docs-and-code audit tranche. No tests were run.
