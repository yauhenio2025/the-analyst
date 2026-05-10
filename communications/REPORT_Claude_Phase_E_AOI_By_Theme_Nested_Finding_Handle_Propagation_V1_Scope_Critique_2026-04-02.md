# Critique: Phase E AOI By-Theme Nested Finding Handle Propagation V1 Scope

**Reviewer**: Claude (Opus 4.6)
**Date**: 2026-04-02
**Memo Under Review**: `MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_scope.md`

---

## Verdict: Approve With Corrections

The strategic decision is correct. The implementation seam recommendation needs correction. One scope-discipline choice is counterproductive.

---

## 1. Strongest Parts Of The Memo

### 1a. `aoi_by_theme` really is a mixed surface, not a second findings bank

The code confirms this directly. `aoi_by_theme.json` declares an accordion with 7 sub-renderer types under `section_renderers._default.sub_renderers`:

- `overview` (annotated_prose)
- `engagement` (annotated_prose)
- `key_claims` (rich_description_list)
- `philosophical_commitments` (rich_description_list)
- `argumentative_moves` (rich_description_list)
- `source_documents` (chip_grid)
- `findings` (mini_card_list)

Only the last one is findings-shaped. The rest are thematic overview, engagement narrative, and structured claim lists. Calling this a findings bank would overclaim.

By contrast, `aoi_by_sin_type.json` is a flat `card_grid` grouped by `_category` with `group_style_map: "sin_type"`. Every item on that surface is a finding. The distinction is real.

### 1b. The decision to NOT add `specialized_family` on `aoi_by_theme` is correct

This follows directly from 1a. A whole-view specialized family marker says "the items on this surface are findings suitable for finding-level operations." That claim is honest on `aoi_by_sin_type` but dishonest on `aoi_by_theme` where 6 of 7 sub-sections are not findings.

### 1c. The gap is precisely identified

The existing test at `tests/test_aoi_contract.py:324` explicitly asserts:

```python
assert "finding_id" not in theme_payload["findings"][0]
```

Meanwhile the normalized findings DO carry `finding_id` — generated at `src/aoi/contract.py:333` via hash fingerprint or upstream LLM value. And `_build_by_sin_type_payload()` already carries `finding_id` through at lines 683-685. So the gap is not "invent identity" — it is "stop dropping one already-known handle at one call site."

### 1d. Analyzer handle semantics are well-calibrated

The five-point characterization (opaque, analyzer-owned, job-scoped, not Critic's `db_id`, no cross-run identity guarantee) is exactly right. The Critic `FindingsPage.tsx:641` loads Arsenal status as `Set<number>` keyed by numeric `finding_id`. The analyzer produces string-valued `finding_id` via SHA-1. These are different identity systems. The memo does not confuse them.

### 1e. The ordering decision is defensible

After closing the pure-surface findings-bank specialization on `aoi_by_sin_type`, the next honest variable is surface-shape difficulty (mixed vs. pure), not semantic broadening. This keeps the proof progression legible: generic first-hop → pure-surface specialization → mixed-surface handle carriage.

---

## 2. Weakest Assumptions

### 2a. "Keep `_finding_card()` unchanged" is the wrong scope-discipline choice (MAIN CORRECTION)

The memo frames this as scope discipline: "do not widen the shared card helper globally." But the code evidence argues against it.

`_finding_card()` has exactly **two** callers:

1. `_build_by_theme_payload()` — line 663
2. `_build_by_sin_type_payload()` — line 682

Both callers receive full normalized finding dicts that already contain `finding_id`. The current pattern in `_build_by_sin_type_payload` is:

```python
card = _finding_card(item)
finding_id = item.get("finding_id")
if isinstance(finding_id, str) and finding_id.strip():
    card["finding_id"] = finding_id
```

The memo proposes replicating this exact pattern inside `_build_by_theme_payload`. That creates identical code duplication at both call sites.

The simpler, smaller change is to add `finding_id` to `_finding_card()` itself:

```python
def _finding_card(finding: dict[str, Any]) -> dict[str, Any]:
    sin_type = finding.get("sin_type") or ""
    card = {
        "title": ...,
        ...
    }
    finding_id = finding.get("finding_id")
    if isinstance(finding_id, str) and finding_id.strip():
        card["finding_id"] = finding_id
    return card
```

This is:

- fewer lines changed total (3 lines added in `_finding_card`, 3 lines removed from `_build_by_sin_type_payload`, 0 lines added in `_build_by_theme_payload`)
- zero code duplication
- no risk of the two call sites drifting apart in how they handle `finding_id`
- no "global widening" concern because `_finding_card()` is a private function with exactly two callers, both of which need the same behavior

The scope discipline of leaving `_finding_card()` unchanged is a false economy. The memo frames it as protecting other surfaces, but there are no other surfaces. The function is private and fully enumerable.

**Recommendation**: Add `finding_id` to `_finding_card()` and remove the separate handling from `_build_by_sin_type_payload()`. This makes the slice both smaller and more honest.

### 2b. Host evidence is from the legacy path, not the V2 presentation path

The memo says: "the Critic thematic UI already treats those nested findings as item-level entities keyed by `finding_id`."

This is true for `ThemeSynthesisCard.tsx` (lines 287, 292, 297), which uses `finding.finding_id` for React keys and expand/collapse state. But ThemeSynthesisCard is the **legacy Critic UI path** where findings come from the Critic backend's own data model — `ThematicFinding` with `finding_id: string` at `types.ts:3095`.

The V2 presentation path routes through `V2TabContent` → GenericSectionRenderer → `mini_card_list` sub-renderer, which renders items based on the view definition's `renderer_config.config` fields (`title_field`, `subtitle_field`, `description_field`, `badge_field`). That path does NOT use `finding_id` for anything.

So the host evidence shows that the legacy path needs finding identity, not that the V2 path already consumes it. This doesn't invalidate the slice — it's still correct to carry the handle upstream so it's AVAILABLE when the V2 path needs it. But the memo should be honest that no existing V2 host code will immediately use this field.

### 2c. Legacy payload behavior should be more precise

The memo says: "If legacy repair is not naturally available at the chosen seam, this memo prefers honesty over hidden compensation logic."

This is the right instinct but should be more concrete. `_build_by_theme_payload()` runs during `build_aoi_output_metadata()` at line 85-89, which runs at **output persistence time** during engine execution. Already-persisted AOI payloads will not be re-normalized. The only way legacy payloads get the new `finding_id` is if the job is re-executed or the user triggers a presentation refresh that re-builds structured payloads.

The memo should state explicitly: "New executions will carry the handle. Existing persisted `structured_payloads.aoi_by_theme` blobs in the output store will not be repaired."

---

## 3. Code-Backed Findings

### 3a. The implementation is genuinely small

With the `_finding_card()` correction above, the implementation is:

- Add 3 lines to `_finding_card()` in `src/aoi/contract.py:730`
- Remove 3 lines from `_build_by_sin_type_payload()` at lines 683-685
- Update the test assertion at `tests/test_aoi_contract.py:324` from `assert "finding_id" not in ...` to `assert ... == first_finding["finding_id"]`
- Update `test_build_by_theme_payload_uses_theme_ids_as_stable_keys_even_when_names_collide` (line 335) to expect `finding_id` in theme findings
- Update any affected manifest/hash proof fixtures

That is 4-5 files, ~10 lines of net change. Genuinely bounded.

### 3b. `findings_by_theme` carries `finding_id` upstream

Confirmed at `src/aoi/contract.py:359-362`:

```python
findings_by_theme = {}
for finding in findings:
    findings_by_theme.setdefault(finding["theme_id"], []).append(finding)
```

Each `finding` in this dict is the full normalized finding including `finding_id` (line 336). The handle is not lost until `_finding_card()` drops it at line 730-744.

### 3c. No presenter changes needed

The change is entirely in the AOI contract layer. `_build_by_theme_payload()` produces `structured_payloads["aoi_by_theme"]` which flows into the presentation system as `structured_data`. The presenter doesn't inspect individual finding fields — it passes `structured_data` through to the consumer. So no changes to `first_hop_affordance.py`, `manifest_builder.py`, or `presentation_api.py` are required.

### 3d. The `FirstHopAffordance` on `aoi_by_theme` is already correct

From `first_hop_affordance.py:87-96`, the specialization gate requires `view_key == AOI_FINDINGS_BANK_SPECIALIZATION_VIEW_KEY` which is `"aoi_by_sin_type"`. `aoi_by_theme` will get the generic affordance (if it's a leaf with a migrated engine key) but NOT the specialized family. No changes needed.

---

## 4. Strategic Implications For The Roadmap

### 4a. This is a legitimate next step, but it's approaching the boundary of AOI-specific work

The distilled roadmap's Rule 2 says: "A bounded proof is useful only if it teaches or ratifies a reusable substrate."

This slice teaches: "mixed surfaces can carry nested item handles without whole-view specialization." That is a reusable pattern. But the proof is exclusively on AOI surfaces with AOI-specific normalization code.

The question is whether the NEXT slice after this should stay AOI-local or pivot to proving the same pattern on a non-AOI surface (e.g., genealogy). The memo's "What Comes After" section correctly identifies this tension but doesn't resolve it.

### 4b. The slice does not conflict with the Close Read direction

The Close Read direction change (`MEMO_2026-04-01_close_read_direction_change_and_implications.md`) shifts emphasis toward analyzer-owned routing and operation contracts. Carrying `finding_id` on `aoi_by_theme` is additive to that direction — it makes one more surface's items identifiable, which is prerequisite for any future routing/operation behavior.

### 4c. The proof progression is now:

1. Generic first-hop affordance on transient surfaces ✓
2. Same generic affordance on job-backed surfaces ✓
3. One specialized findings-bank family on one pure surface ✓
4. **[This slice]** Nested finding handles on one mixed surface
5. *[Future]* Mixed-surface specialized family? Or pivot to outline-routing?

This is a legible progression. Step 4 is correctly positioned.

---

## 5. Is There A More Defensible Next Step?

The memo considers three alternatives and rejects them. All three rejections are correct:

**Broadening findings-bank specialization to `aoi_by_theme`**: Would overclaim. The whole-view marker is dishonest on a mixed surface. Rejected correctly.

**Pivoting immediately to outline-routing**: The operations/routing inventory (`APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`) shows outline-routing is more comment-shaped and host-shaped than finding promotion. It depends on host mutation endpoints that don't exist in analyzer-v2 yet. The memo is right that this is a harder, less analyzer-owned operation.

**Inventing a generic item-level affordance schema**: Premature. We have exactly two surfaces that need item handles. A generic schema needs at least 3-4 examples to avoid overfitting.

The memo's proposed slice is the smallest honest next step. No stronger alternative is apparent.

---

## 6. Concrete Corrections

### Correction 1 (Required): Add `finding_id` to `_finding_card()` instead of duplicating in `_build_by_theme_payload()`

Move the conditional `finding_id` inclusion into `_finding_card()` and remove the separate handling from `_build_by_sin_type_payload()`. This is fewer lines, zero duplication, and serves both callers. Update the memo's "Expected implementation seam" accordingly.

### Correction 2 (Required): Be precise about legacy payloads

Replace "If legacy repair is not naturally available at the chosen seam, this memo prefers honesty over hidden compensation logic" with: "New AOI job executions will carry `finding_id` on `aoi_by_theme` findings. Already-persisted `structured_payloads.aoi_by_theme` blobs in the output store will not be repaired. Legacy payloads that lack the field should be treated honestly — the host should not assume the field is always present."

### Correction 3 (Informational): Qualify the host evidence

The ThemeSynthesisCard evidence is from the legacy Critic UI path, not the V2 presentation rendering path. The V2 `mini_card_list` sub-renderer does not currently use `finding_id`. The handle is being carried upstream so it is available for future V2 host consumption, not because existing V2 host code already depends on it.

### Correction 4 (Informational): Note that `_build_by_sin_type_payload` will simplify

If `_finding_card()` gains the `finding_id` field, the separate handling at `_build_by_sin_type_payload()` lines 683-685 becomes dead code. The implementor should clean it up rather than leaving both paths.
