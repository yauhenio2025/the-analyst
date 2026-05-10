# Critique: Phase E AOI V2 Mixed-Surface Nested Finding Consumer Proof V1 Scope

Date: 2026-04-03
Reviewer: Claude Opus 4.6 (1M context)
Memo Under Review:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`

## Verdict

**Approve with corrections**

The strategic sequencing is right. The calibration between what this slice proves and what it does not is mostly honest. But the memo underestimates one structural complexity and leaves three implementation details ambiguous enough that an implementor could make silent wrong choices.

---

## Strongest Points

### 1. Correct strategic sequencing

The memo is right that the pure-surface `aoi_by_sin_type` loop is now genuinely closed (selection, write-side provenance, read-side surfacing) and that another refinement on that same line would now teach less than broadening to a structurally different surface.

The four completion memos confirm this:
- selection creation proof: `AoiSinFindingsRenderer` creates well-formed `CaptureSelection` with `entity_id` and `source_workflow_key`
- write-side: both `CaptureContext.submitCapture` and `ResearchFlagDialog` now persist provenance
- read-side: `useAnalysisCaptureStatusByEntity` surfaces passive per-card truth after reload

Broadening the consumer proof to a structurally different surface is the right next variable to vary.

### 2. Honest whole-view calibration

The memo correctly refuses to treat `aoi_by_theme` as a findings-bank surface. This matches the codebase exactly:

- `first_hop_affordance.py` (lines 87-96) only assigns `specialized_family = "findings_bank_arsenal_promotion_v1"` when `view_key == "aoi_by_sin_type"` AND `engine_key == "aoi_sin_findings"` AND all findings have `finding_id`
- `aoi_by_theme` intentionally remains generic-only: `capturable=True`, `allowed_destinations=["arsenal","research_todo"]`, `specialized_family=None`

The memo's decision to rely on "generic capturable plus non-empty nested `finding_id`" as the guard condition is therefore the only honest option.

### 3. Correct host-state assessment

The memo's seven evidence-base claims are all codebase-verified:

1. `finding_id` on `aoi_by_theme` nested findings: confirmed at `contract.py:639-647`
2. `FirstHopAffordance` stays generic-only: confirmed by `first_hop_affordance.py` specialization guard
3. `hasViewRendererOverride('aoi_by_theme') === false`: confirmed by `renderers/index.ts` and `index.test.tsx` line 79
4. `V2TabContent` threads all needed metadata: confirmed (`_firstHopAffordance`, `_captureMode`, `_onCapture`, `_captureViewKey`, `_captureViewName`, `_captureSourceType`, `_workflowKey`)
5. Mixed surface structure (themes with nested findings): confirmed by payload shape in `_build_by_theme_payload()`
6. Legacy `ThemeSynthesisCard.tsx` evidences downstream value of theme-nested findings: confirmed
7. Read-side seam exists but does not answer mixed-surface question: confirmed

### 4. Correct handling of legacy payloads

The memo honestly acknowledges that older persisted `aoi_by_theme` payloads lack `finding_id` and requires silent degradation. This matches the implementation: `finding_id` is only added on rebuild via `contract.py:644-646`, and no repair-on-load compensation exists.

### 5. Correct read-side deferral

Keeping capture-status read-back out of scope for v1 is the right call. The `useAnalysisCaptureStatusByEntity` hook and `POST /api/captures/status/by-entity` route are `aoi_by_sin_type`-proven but not yet mixed-surface-proven. Bundling read-back into this slice would conflate two distinct proof questions.

---

## Weakest Assumptions and Calibration Problems

### 1. Structural complexity is materially understated

This is the memo's most significant calibration gap.

**`aoi_by_sin_type`** is structurally flat:
```
{ sin_type_key: [finding_card, finding_card, ...], ... }
```
Every card in every section is a finding. The `AoiSinFindingsRenderer` iterates sections and renders card grids with capture controls on all eligible cards.

**`aoi_by_theme`** is structurally nested:
```
{
  theme_key: {
    overview: str,
    engagement: str,
    key_claims: [{title, description}, ...],
    philosophical_commitments: [{title, description}, ...],
    argumentative_moves: [{title, description}, ...],
    source_documents: [str, ...],
    findings: [{finding_card_with_finding_id}, ...]
  },
  ...
}
```

Each theme section contains 7+ heterogeneous sub-sections, only ONE of which (`findings`) carries `finding_id` and should show capture controls. The others (overview, engagement, claims, commitments, moves, source_documents) must remain passive.

The memo says "one local `aoi_by_theme` view override or equivalently local bounded renderer seam" as if it were roughly analogous to the `aoi_by_sin_type` override. It is not. A view-level override for `aoi_by_theme` would need to either:

(a) **Reproduce** the entire theme accordion rendering (collapsible sections, section metadata, expand/collapse controls, sub-renderer dispatch) while injecting capture controls only in the `findings` sub-section, or

(b) **Compose** with the existing `NestedSectionsRenderer` by providing a targeted sub-renderer override for the findings sub-section only

Option (b) is smaller and more honest than (a), but the memo does not distinguish between them. An implementor reading this memo could choose (a) and produce a large, fragile renderer that duplicates substantial generic rendering logic.

**Correction needed**: The memo should explicitly recommend the composable sub-renderer seam over a full view-level override, or at minimum acknowledge the structural nesting makes a full override materially larger than the `aoi_by_sin_type` precedent.

### 2. Guard condition difference from `aoi_by_sin_type` is not called out

The existing `AoiSinFindingsRenderer` uses a five-condition guard:
```typescript
function isArsenalSpecialization(affordance): boolean {
  return Boolean(
    affordance
    && affordance.capturable
    && affordance.allowed_destinations.includes('arsenal')
    && affordance.specialized_family === 'findings_bank_arsenal_promotion_v1'
  );
}
```

Since `aoi_by_theme` intentionally has `specialized_family = null`, this guard will NEVER pass for `aoi_by_theme`. The new mixed-surface proof must use a materially different, weaker guard:

```typescript
// Hypothetical: generic capturable + non-empty finding_id per card
affordance?.capturable && card.finding_id
```

This is a deliberate design choice the memo makes (relying on generic capturable + item identity), but it never explicitly names the guard-shape difference from the pure-surface proof. An implementor might try to reuse or adapt `isArsenalSpecialization()` and be confused when it always returns false.

**Correction needed**: The memo should explicitly state that the `aoi_by_theme` capture guard is structurally different from `aoi_by_sin_type` and must NOT check `specialized_family`. It should name the exact guard: `affordance.capturable === true` AND `finding_id` is non-empty string on the individual card.

### 3. `renderer_type = "accordion"` needs verification

The memo states:
> `renderer_type = "accordion"`
> nested `findings` rendered as `mini_card_list`

The Critic codebase shows that `TYPE_RENDERER_OVERRIDES` maps `nested_sections` (not `accordion`) to `NestedSectionsRenderer`. The `aoi_by_theme` view may actually use `renderer_type = "nested_sections"` rather than `"accordion"`.

This is not a blocking issue — the rendered behavior may be accordion-like regardless of the type string — but the memo should use the actual `renderer_type` value from the view definition rather than the visual appearance name. If the actual type is `nested_sections`, then the implementation seam is `NestedSectionsRenderer` sub-renderer dispatch, not an accordion-specific override.

**Correction needed**: Verify the actual `renderer_type` for `aoi_by_theme` views and use the correct string. If it is `nested_sections`, update the scope accordingly.

### 4. Detection of findings-bearing vs non-findings-bearing family is unspecified

The memo correctly identifies adaptive family variation as an honesty boundary:

> If `aoi_by_theme` is currently rewritten to a non-findings-bearing family such as a comparison-review table, that variant should remain out of scope and render unchanged.

But it does not specify HOW the renderer detects whether the current payload is a findings-bearing family. The implementation needs a concrete detection mechanism. Options include:

- Check whether any theme section contains a non-empty `findings` array
- Check a metadata field on the view or section hint
- Check the `renderer_type` or `section_renderer_hints`

Without specifying this, an implementor might add a brittle detection heuristic or accidentally apply capture controls to a non-findings-bearing variant.

**Correction needed**: Specify the detection mechanism for findings-bearing family, even if it is as simple as "theme section contains a non-empty `findings` array with at least one item having non-empty `finding_id`."

### 5. `source_renderer_type = "mini_card_list"` is assumed, not verified

The memo freezes `source_renderer_type = "mini_card_list"` as part of the `CaptureSelection` shape. This value should match the actual renderer type used to render findings within theme sections. The current `NestedSectionsRenderer` delegates to sub-renderers based on section hints, and the actual sub-renderer type for findings may or may not be `mini_card_list`.

This matters for downstream capture provenance: if the persisted `source_renderer_type` does not match the actual rendering type, it creates a truthfulness gap in the capture record.

**Correction needed**: Verify the actual sub-renderer type used for findings within theme sections and use that verified value.

---

## Factual Mismatches with the Codebase

### Minor

1. **`renderer_type` string**: The memo says `accordion`. The Critic codebase maps `nested_sections` to `NestedSectionsRenderer` in `TYPE_RENDERER_OVERRIDES`. The actual `renderer_type` for `aoi_by_theme` views needs to be checked against the analyzer-v2 view definitions. This may be `nested_sections`, not `accordion`.

2. **`source_renderer_type`**: The memo asserts `mini_card_list` without citing which section_renderer_hint or sub-renderer dispatch produces that value at runtime.

### None critical

No factual claim in the memo is outright wrong. The evidence-base items are all codebase-verified. The issues above are matters of precision rather than factual error.

---

## What This Changes for the Broader Roadmap

### Positive

1. **Matrix broadening is real**: Moving from pure-surface to mixed-surface is a genuine structural variation, not just another same-family refinement. The `aoi_by_theme` payload shape (nested themes with heterogeneous sub-sections) is materially different from `aoi_by_sin_type` (flat sin-type to finding-card mapping).

2. **Generic guard condition is a substrate signal**: If the mixed-surface proof succeeds with `capturable + finding_id` alone (no `specialized_family`), it proves that the generic affordance contract is already sufficient for nested-item capture. That is more reusable than the specialized-family proof on `aoi_by_sin_type`.

3. **Non-AOI broadening becomes the next natural step**: After this slice, the honest next question is whether the same generic guard works on a non-AOI surface, not whether another AOI surface can be added.

### Neutral

4. **Still AOI-local**: This slice does not prove anything about non-AOI surfaces. The roadmap's Phase E exit signal requires a representative matrix across engine/output families. One more AOI surface, even a structurally different one, is necessary but not sufficient.

### Risk

5. **Implementation scope creep**: If the structural complexity concern is not addressed, the implementor may produce a large view-override renderer that reproduces `NestedSectionsRenderer` logic. That would be technically correct but architecturally wasteful, creating another local override that needs maintenance when the generic renderer-package rules eventually land.

---

## The Most Defensible Next Move After This Memo

Assuming this memo lands with the corrections above:

1. **Immediate next**: Implement the bounded `aoi_by_theme` mixed-surface consumer proof as scoped — capture-selection creation on nested thematic findings, using the composable sub-renderer seam rather than a full view override
2. **After that**: Non-AOI proof on one genealogy or standalone surface that tests the same generic `capturable + finding_id` guard on a different workflow family
3. **Not yet**: Generic renderer-package capture law, mixed-surface status read-back, or destination lifecycle semantics

The strongest reading of the roadmap is that this mixed-surface AOI slice is necessary but should be the LAST AOI-only consumer proof before the program broadens to non-AOI surfaces for Phase E exit credibility.

---

## Summary

The memo is strategically sound and its key claims are codebase-verified. The corrections needed are:

1. **Address structural nesting complexity explicitly** — the implementation shape is not analogous to the flat `aoi_by_sin_type` override
2. **Name the guard condition difference** — generic `capturable + finding_id` vs specialized-family five-condition guard
3. **Verify `renderer_type`** — may be `nested_sections`, not `accordion`
4. **Specify findings-bearing family detection** — how the renderer knows it is looking at a findings-bearing variant
5. **Verify `source_renderer_type`** — confirm actual sub-renderer type used for theme-nested findings

None of these corrections change the strategic direction. The slice is the right next move. The corrections ensure the implementor does the right thing at the seam level.
