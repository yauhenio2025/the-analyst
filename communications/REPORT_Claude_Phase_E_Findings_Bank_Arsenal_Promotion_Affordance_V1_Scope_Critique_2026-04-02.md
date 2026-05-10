# Critique: Phase E Findings-Bank Arsenal Promotion Affordance V1 Scope

**Reviewer**: Claude (Opus 4.6)
**Date**: 2026-04-02
**Memo Under Review**: `MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_scope.md`

---

## Verdict: Approve With Corrections

The strategic decision is correct. The contract shape needs sharpening.

---

## 1. Strongest Parts Of The Memo

### 1a. Surface selection is well-reasoned

`aoi_by_sin_type` is the right first target. The code confirms:

- `renderer_type: "card_grid"` with flat item semantics (`title_field`, `description_field`, `badge_field`)
- `engine_key: "aoi_sin_findings"` with stable curated view identity
- `presentation_stance: "evidence"` (strongest fit for capture/promotion)
- No nested sub-renderers (unlike `aoi_by_theme` which has 7 sub-renderer types under accordion sections)

By contrast, `aoi_by_theme` uses `renderer_type: "accordion"` with deeply nested `section_renderers._default.sub_renderers` including `overview`, `engagement`, `key_claims`, `findings`, etc. Item-level semantics on that surface cross multiple renderer boundaries. The memo is correct to exclude it.

### 1b. Emission boundary is correctly narrow

The four-predicate gate (`workflow_key == AOI_WORKFLOW_KEY` AND `view_key == "aoi_by_sin_type"` AND `engine_key == "aoi_sin_findings"` AND existing base affordance) is tighter than needed but defensible. The code already proves this gating pattern works: `first_hop_affordance.py` gates on `FIRST_HOP_AFFORDANCE_ELIGIBLE_WORKFLOW_KEYS` and `MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS` with a leaf-only check. Adding a view_key predicate for specialized emission is consistent.

### 1c. Generic-on-top-of-specialized layering is the right architecture

The memo correctly keeps `capturable` + `allowed_destinations` unchanged and adds the specialized marker as optional metadata. This means:

- Hosts that don't understand specialized families keep working
- Hosts that do can offer richer UX
- No breaking change to any existing consumer

### 1d. Hash and trace specification is complete

The rules are explicit: contract hash changes, content hash does not, trace diffs surface the field. This matches exactly how the existing `first_hop_affordance` field already behaves in `manifest_builder.py:277-300` (included in `_manifest_identity_row`) and `decision_trace.py:540-553` (tracked in `_diff_snapshots`).

### 1e. Honest claim boundary

The memo does not overreach. "One specialized family on one surface" is accurate and appropriately modest.

---

## 2. Weakest Assumptions

### 2a. `specialized_family` is semantically thin (MAIN CONCERN)

The proposed field:

```python
specialized_family: Optional[Literal["findings_bank_arsenal_promotion_v1"]]
```

names a family but does not specify what the family means for host behavior.

Currently, the base affordance already says:
```json
{"capturable": true, "allowed_destinations": ["arsenal", "research_todo"]}
```

A host reading this already knows: "user can capture from this view and route to Arsenal." What does `specialized_family = "findings_bank_arsenal_promotion_v1"` add?

The implicit answer is: "the items on this surface are findings with structured data suitable for direct finding-to-Arsenal promotion, not just text-selection capture." This is the distinction between:

- **Generic capture**: text selection -> `CaptureActionBar` -> `submitCapture('arsenal', annotation)` with `selected_text` + basic `context_title`
- **Specialized promotion**: card-level action -> direct Arsenal creation preserving full finding `structured_data` (sin type, theme name, description, badge, etc.)

The Critic code confirms this distinction exists at runtime. `CaptureContext.tsx:87-166` shows the two-phase flow: create capture record with `structured_data`, then route to destination. The `structured_data` field preserves domain-specific finding shape. But the memo doesn't make this distinction explicit.

**Correction needed**: The memo should state what semantic guarantee the specialized family provides that the base affordance does not. Specifically: "findings on this surface carry stable structured_data shape suitable for finding-level (not text-selection-level) Arsenal promotion."

### 2b. No item-level identity specification

The `aoi_by_sin_type` card_grid groups items by `_category` with `group_style_map: "sin_type"`. Individual findings within a group are identified by position, not stable key.

In Critic, `CaptureSelection` uses `source_item_index: number` as the item identifier. This is fragile: if the engine re-runs and findings change order, previously-promoted items lose their provenance trail.

The memo doesn't need to solve this (it's correctly out-of-scope for host UX), but it should acknowledge that the specialized family implicitly assumes finding-level identity stability from the engine output. If `aoi_sin_findings` reorders findings across runs, the specialized promotion semantics degrade. This should be named as a known constraint, not a scope item.

### 2c. The Literal string carries zero machine-readable semantics

`"findings_bank_arsenal_promotion_v1"` is an opaque label. A host must hard-code knowledge of what this string means. Compare with the base affordance where `capturable` and `allowed_destinations` are directly actionable without external knowledge.

An alternative contract shape that carries more information:

```python
class SpecializedAffordanceHint(BaseModel):
    family: Literal["findings_bank_arsenal_promotion_v1"]
    item_semantic_type: Literal["finding"]
    structured_data_preserved: bool = True
```

This is more explicit about what the family guarantees. However, this may be premature generalization for v1. The memo should state that the opaque label is intentionally minimal for v1 and that richer item-level semantic hints are a known follow-on.

---

## 3. Code-Backed Findings

### 3a. Population seam is straightforward

The specialized marker should be populated in `first_hop_affordance.py`, specifically by extending `derive_first_hop_affordance()`. The function already receives the full `ViewPayload` (which carries `view_key` and `engine_key`). Adding a view_key check is one conditional:

```python
# In first_hop_affordance.py
def derive_first_hop_affordance(payload, *, enabled):
    if not enabled or not is_migrated_analytical_leaf_payload(payload):
        return None
    affordance = FirstHopAffordance(
        capturable=True,
        allowed_destinations=list(FIRST_HOP_ALLOWED_DESTINATIONS),
    )
    # Specialized family annotation
    if payload.view_key == "aoi_by_sin_type" and payload.engine_key == "aoi_sin_findings":
        affordance.specialized_family = "findings_bank_arsenal_promotion_v1"
    return affordance
```

No new population seam is needed. The existing `attach_first_hop_affordances()` recursive walk already calls `derive_first_hop_affordance()` on every payload.

### 3b. Workflow gating is already handled

The existing `workflow_supports_first_hop_affordance(workflow_key)` check runs before any derivation. Since `aoi_by_sin_type` is only reachable under `AOI_WORKFLOW_KEY` (confirmed by `data_source.workflow_key` in the view definition JSON), the four-predicate gate reduces to two novel checks: `view_key` and `engine_key`. The workflow and leaf predicates are already enforced.

### 3c. Schema extension is minimal

Adding one optional field to `FirstHopAffordance` in `schemas.py:695-702`:

```python
class FirstHopAffordance(BaseModel):
    capturable: bool
    allowed_destinations: list[FirstHopDestination] = Field(default_factory=list)
    specialized_family: Optional[str] = None  # or Literal[...]
```

This is backward-compatible. Existing serialized affordances without the field will deserialize with `None`.

### 3d. `_manifest_identity_row` already handles the field correctly

`manifest_builder.py:293-297` already serializes `first_hop_affordance` via `.model_dump(mode="json")`. Adding a new field to `FirstHopAffordance` will automatically appear in the identity row and affect `presentation_hash`. No manifest builder changes needed.

### 3e. `_diff_snapshots` already tracks the field

`decision_trace.py:544` already includes `"first_hop_affordance"` in the tracked fields tuple. Since the diff compares the entire field value (not sub-fields), a change from `{capturable: true, allowed_destinations: [...]}` to `{capturable: true, allowed_destinations: [...], specialized_family: "..."}` will be surfaced as a change. No trace changes needed.

### 3f. Content hash correctly excludes affordance

`manifest_builder.py:309-311` builds the content manifest from `structured_data`, `items`, `reading_scaffold`, and `output_hashes`. The `first_hop_affordance` field is not included. Adding `specialized_family` to the affordance model will not affect content hash. Correct by construction.

### 3g. `aoi_by_theme` uses the same engine but gets no specialized marker

Both views use `engine_key: "aoi_sin_findings"`. The specialized marker gates on `view_key == "aoi_by_sin_type"`, not on engine_key alone. This means `aoi_by_theme` (view_key = "aoi_by_theme") will correctly remain generic-only. The negative test should verify this explicitly.

### 3h. Transient compose is unaffected

Transient compose goes through `_handoff_supports_first_hop_affordance()` which checks `(workflow_key, handoff_kind)` pairs from `_FIRST_HOP_AFFORDANCE_ELIGIBLE_HANDOFFS`. The specialized marker logic should only activate in `derive_first_hop_affordance()`, which is shared. But transient compose views don't carry stable `view_key` from curated definitions — they carry engine-derived keys. The view_key gate naturally excludes transient surfaces.

Confirm this by checking: transient compose views get view_keys like `"source_profile"`, `"source_selection"`, `"direct_sections"` — none of which match `"aoi_by_sin_type"`. So the specialized marker is inherently job-backed-only without needing a separate gate.

---

## 4. Strategic Implications For The Roadmap

### 4a. This slice validates the operation-family layer as a real abstraction

The interface-first renderer/output family strategy memo (`MEMO_2026-04-01`) identified three distinct problems: renderer-family boundedness, output-family taxonomy, and composition-law generalization. This slice is the first concrete probe into the second problem. If it lands cleanly, it proves that the analyzer can own output-specific semantic declarations without absorbing host UX.

### 4b. The v1 opaque-label approach creates a naming precedent

Whatever string goes into `specialized_family` becomes the first entry in what will eventually be an operation-family vocabulary. The choice of `"findings_bank_arsenal_promotion_v1"` is Critic-shaped: it names a specific host destination ("Arsenal") in an analyzer-owned field. This is slightly awkward — the analyzer should ideally declare the semantic capability ("finding-level structured promotion") rather than the host destination ("Arsenal promotion"). But for a v1 with one known consumer this is tolerable.

### 4c. Outline-routing is correctly deferred

The operations inventory confirms that outline-routing is more comment-shaped and host-shaped than finding promotion. Outline talking points require text anchor context and section-level provenance that are harder to express as a flat affordance marker. Finding promotion has a cleaner item-level semantic boundary. The ordering is correct.

### 4d. Close Read productization is not advanced by this slice

This slice advances the analyzer contract, not the product. Close Read needs: multi-input selection, engine-dependent follow-up paths, Arsenal/research-todo lifecycle, outline management. This slice provides one small building block. The memo is honest about this.

---

## 5. Concrete Corrections

### Correction 1: Define what the specialized family guarantees (REQUIRED)

Add a section explaining:

> The `specialized_family` marker on `aoi_by_sin_type` declares that:
> - items on this surface are individual findings with stable structured_data shape
> - finding-level (not text-selection-level) operations are semantically appropriate
> - the finding data shape includes sin type, theme association, and diagnostic description
> - hosts MAY offer direct finding-level promotion UX beyond generic text capture
>
> The base affordance says "capture is possible." The specialized family says "the items here are findings suitable for finding-level operations."

Without this, the field is a label without a contract.

### Correction 2: Acknowledge item identity as a known constraint (RECOMMENDED)

Add under "Population And Contract Shape":

> The specialized family implicitly assumes finding-level identity stability from the `aoi_sin_findings` engine output within a single job execution. Item identity across re-executions of the same workflow is not guaranteed by this contract. Hosts that implement finding-level promotion should use job-scoped item references, not cross-job item identity.

### Correction 3: Clarify the Literal type vs open string decision (RECOMMENDED)

The memo says `Optional[Literal["findings_bank_arsenal_promotion_v1"]]`. This should be:

```python
specialized_family: Optional[str] = None
```

with a documented vocabulary, not a Literal. Reason: Literal types force a schema change for every new family. An open string with a documented vocabulary is more extensible while still being validatable. The v1 vocabulary is `{"findings_bank_arsenal_promotion_v1"}`. Future slices add entries without schema changes.

### Correction 4: Specify that no new test file is needed (MINOR)

The memo mentions `tests/test_analysis_product_contract.py` as a recommended verification surface. This file does not exist. The memo should either commit to creating it (adds scope) or drop it from the recommendation and extend existing `test_presentation_api.py` and `test_manifest_trace.py` instead.

### Correction 5: Name the negative test cases explicitly (RECOMMENDED)

The memo says "negative coverage proving no specialized emission on aoi_by_theme, non-AOI surfaces, transient compose views." Make these concrete:

- `aoi_by_theme` (same engine, different view_key) -> no specialized_family
- `aoi_thematic_analysis` (parent view) -> no first_hop_affordance at all (existing behavior)
- genealogy views (different workflow, different engine) -> no specialized_family
- transient compose views (no stable curated view_key) -> no specialized_family
- non-approved workflow -> no first_hop_affordance at all (existing behavior)

---

## 6. Bottom Line

The strategic ordering is correct: generic first-hop seam is proven, Arsenal promotion is the strongest runtime-real specialized operation, `aoi_by_sin_type` is the right surface. The implementation is small (one optional field, one conditional in `derive_first_hop_affordance`, a handful of tests).

The main gap is that the `specialized_family` field names a family without specifying what semantic guarantee the family provides. Correction 1 above fixes this with two sentences. The remaining corrections are minor tightening.

This is the right next slice. It should proceed after the corrections are applied.
