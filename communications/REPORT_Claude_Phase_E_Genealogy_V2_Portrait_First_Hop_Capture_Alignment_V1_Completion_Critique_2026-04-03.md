# Report: Phase E Genealogy V2 Portrait First-Hop Capture Alignment V1 Completion Critique

Date: 2026-04-03
Reviewer: Claude Opus 4.6
Completion Memo: `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`

## Verdict: APPROVE WITH CORRECTIONS

The completion memo is well-calibrated and code-honest. The boundary claims are accurate. The "not" lists are genuinely protective rather than theatrical. Two corrections are needed: the memo overstates the truthfulness improvement on `source_type`, and it underreports a concrete UX regression in the `context_title` shape.

---

## 1. Strongest Parts of the Memo

### 1a. The Boundary Discipline Is Real

The memo's "What this does not mean" list (lines 79-83) is accurate and load-bearing:

- `entity_id` does not disambiguate sections: **verified**. `V2TabContent.tsx:595` sets `_captureEntityId: presentation.job_id || ''`. Every section from the same run shares the same `entity_id`. The memo explicitly says this (lines 123-135).
- no analyzer-v2 runtime changes: **verified**. `src/presenter/first_hop_affordance.py` is unchanged. `genealogy_final_synthesis` was already in `MIGRATED_COMPOSITION_ENGINE_FAMILIES` and `intellectual_genealogy` was already in `FIRST_HOP_AFFORDANCE_ELIGIBLE_WORKFLOW_KEYS`.
- no backend or persistence changes: **verified**. `CaptureContext.tsx` `submitCapture` is unchanged.
- not a generic custom-renderer law claim: **verified**. The implementation is entirely local to `SynthesisRenderer.tsx`. No shared renderer-package logic was touched.

### 1b. The Gating Logic Is Honest

`SynthesisRenderer.tsx:73-82` gates section capture on exactly the conjunction the scope memo required:

```
captureMode && onCapture && captureViewKey && captureViewName &&
captureSourceType && workflowKey && captureJobId &&
firstHopAffordance?.capturable === true
```

This is tighter than the prior unconditional `captureMode && onCapture` gating described in the scope memo's pre-state (evidence claim #4). The memo accurately calls this "consuming analyzer-owned generic first-hop truth."

### 1c. Section Coverage Narrowness Is Honest

Capture buttons render only on `exec_summary` (line 163), `portrait` (line 171), and `key_findings` (line 183). Author profile, methodological notes, and idea genealogy summaries do not have capture controls. The test at `SynthesisRenderer.test.tsx:101-103` asserts exactly 3 buttons. The memo accurately reports this.

### 1d. Test Evidence Matches Claims

- **Unit tests**: 10 `SynthesisRenderer` tests cover: passive mode, affordance-present/absent/false, missing config fields, correct selection emission for all three sections, entity_id fallback, config-derived source_type. These are thorough for the scope.
- **CaptureContext tests**: Verify `entity_id` and `source_workflow_key` forwarding to the create request payload.
- **Playwright**: One fixture-backed spec proves live genealogy page renders synthesis content, capture mode activates section buttons, clicking hands off to `CaptureActionBar` with config-derived title and preview text. The memo is honest that the dev overlay workaround is needed.

---

## 2. Weakest Assumptions and Overclaims

### 2a. `source_type` Truthfulness Is Overstated (Correction Required)

The memo says (lines 114-121):

> The renderer now consumes `_captureSourceType` rather than hardcoding `"genealogy"`.
> On this path, `V2TabContent` still resolves that value to the same downstream string: `"genealogy"`.
> So this slice improves truthfulness without breaking the current capture route expectation.

This is technically true but overstates the improvement. The renderer replaced a hardcoded `"genealogy"` with a config-read `_captureSourceType`. But `V2TabContent.tsx:594` computes that config value as:

```typescript
_captureSourceType: workflowKey?.includes('genealogy') ? 'genealogy' : 'analysis',
```

That is still a string-matching heuristic inside `V2TabContent`, not analyzer-emitted truth. The indirection moved from the renderer to the tab content component. The renderer is now more generic — it would work if `_captureSourceType` were set to `"analysis"` — but the system-level truthfulness of the `source_type` value has not changed. The analyzer does not emit `source_type`; the host still infers it.

**Correction**: The memo should say "the renderer now reads source_type from the threaded config rather than hardcoding it, which improves renderer generality, but the host-level inference of source_type from workflow_key is unchanged." Replace "improves truthfulness" with "improves renderer composability."

### 2b. `context_title` Produces a Redundant Label on the Portrait Section (Underreported)

The new `context_title` formula is `${captureViewName}: ${title}`. On the portrait section, this produces:

```
"Genealogical Portrait: Genealogical Portrait"
```

This is confirmed by `SynthesisRenderer.test.tsx:218`. The test asserts this value, meaning it's intentional — but the memo does not acknowledge this UX regression. The prior format `"Synthesis > Genealogical Portrait"` was arguably less redundant.

This is not a blocker, but the memo should note it as a known presentation artifact of the truthful formula, not silently accept it as a feature.

### 2c. "More Truthful CaptureSelection" Is Mostly Fair But Imprecise

The memo repeatedly calls the result "more truthful." Let me itemize what actually changed:

| Field | Before | After | Truthfulness Gain |
|-------|--------|-------|-------------------|
| `source_workflow_key` | absent | `workflowKey` | **Real** — new field, carries genuine provenance |
| `entity_id` | absent | `captureEntityId \|\| captureJobId` | **Real** — new field, bounded but useful |
| `source_type` | `"genealogy"` (hardcoded) | `_captureSourceType` (resolves to `"genealogy"`) | **Minimal** — same value, different plumbing |
| `context_title` | `"Synthesis > ..."` | `"${captureViewName}: ${title}"` | **Presentation** — more descriptive but see 2b |
| Gating | `captureMode && onCapture` | + `firstHopAffordance?.capturable === true` | **Real** — analyzer-governed rather than unconditional |

Two of five changes are genuinely new truthfulness (`source_workflow_key`, `entity_id`). One is genuinely better gating (first-hop). One is cosmetic same-value indirection (`source_type`). One is a presentation change with a known regression (`context_title`).

**Correction**: The memo should be more precise about which fields represent new truth versus which represent unchanged values through different plumbing.

---

## 3. Code-Backed Findings

### 3a. The First-Hop Contract Consumed Is Extremely Simple

The entire first-hop consumption is `firstHopAffordance?.capturable === true` — a single boolean check. The memo frames this as "consuming analyzer-owned generic first-hop truth," which is accurate but potentially misleading about the depth of contract consumption. The renderer does not inspect `allowed_destinations` or `specialized_family`. The AOI surfaces consume the same boolean plus specialized family semantics plus per-item `finding_id`.

This matters for the "proof matrix" framing. The memo says the matrix now includes three structurally different surfaces. But the contract consumption depth differs:

- `aoi_by_sin_type`: `capturable` + `specialized_family` + `finding_id`
- `aoi_by_theme`: `capturable` + nested `finding_id` (no specialized_family)
- `genealogy_portrait`: `capturable` only

The genealogy proof is the shallowest contract consumer. That doesn't invalidate the proof — the scope memo explicitly said no item-level or specialized_family requirements — but the memo should acknowledge that the structural diversity of contract consumption is modest.

### 3b. `genealogy_job_id` Backward Compatibility Is Properly Maintained

`SynthesisRenderer.tsx:129`: `genealogy_job_id: captureJobId || ''` preserves the existing capture route expectation. `CaptureContext.tsx:97-102` correctly resolves `genealogy_job_id` from the selection, including the fallback for genealogy source types. The backward-compatibility claim is verified.

### 3c. `CaptureContext.submitCapture` Already Forwards All New Fields

`CaptureContext.tsx:113-114`:
```typescript
entity_id: currentSelection.entity_id || null,
source_workflow_key: currentSelection.source_workflow_key || null,
```

These were already landed in the prior AOI capture-provenance persistence slice. The genealogy renderer now fills them, but the pipe was already ready. The memo is accurate that no persistence changes were needed.

### 3d. No View-Key Override Needed

Unlike the AOI surfaces which required local dispatcher overrides in `renderers/index.ts`, this slice only modified the existing `SynthesisRenderer` that was already registered by view_key `genealogy_portrait`. No new routing logic was added. The memo doesn't highlight this, but it's a meaningful simplicity signal: the existing renderer structure was already correct, only its internal capture behavior needed alignment.

---

## 4. Strategic Implications for the Roadmap

### 4a. The Proof Matrix Is Broader But the Contract Depth Is Not

The memo claims the proof matrix is now "AOI pure findings, AOI mixed surface nested findings, non-AOI current section renderer." This is accurate as a surface-family claim. But the contract depth consumed on the genealogy surface is minimal (`capturable: true`). The AOI surfaces exercise richer contract facets (specialized_family, finding_id, per-item handles, read-back).

This means the "two structurally different data points for generic law extraction" framing (from the prior scope critique) is partially deflated. The two data points share the `capturable: true` boolean, but their selection-emission shapes differ significantly (card with finding_id vs section with section_key). The real extraction target is the selection-shape taxonomy, not the affordance check itself.

### 4b. The Next Step Framing Is Sound But Should Be More Specific

The memo's next-step framing (lines 219-245) is honest: either a generic extraction memo or one more `IdeaEvolutionRenderer` proof. But it should be more specific about what "generic custom-renderer first-hop seam" means in practice:

- The affordance check is already trivially generic: `firstHopAffordance?.capturable === true`.
- The non-generic part is selection emission: each renderer builds a different `CaptureSelection` shape (card_grid emits `finding_id` + `parent_context`; synthesis emits `section_key` + `depth_level`; accordion shim emits `source_item_index` + `parent_context`).
- The honest extraction question is therefore: can selection-shape emission be parameterized by renderer metadata rather than per-renderer local code?

The memo should reframe "generic custom-renderer first-hop seam" as "generic selection-emission parameterization" to avoid conflating the trivially-generic affordance check with the actually-hard selection-shape diversity.

### 4c. IdeaEvolutionRenderer Is Not Just "Another Proof" — It Would Test Multi-Depth

The completion memo mentions `IdeaEvolutionRenderer` as an alternative next step. The prior scope critique noted it is 944 lines with V1/V2 format detection and both L1_section and L2_element depth levels. That makes it structurally more demanding than SynthesisRenderer (which is L1_section only). If the goal is to test whether generic law can emerge, IdeaEvolutionRenderer would exercise a dimension (multi-depth capture) that the current matrix doesn't cover. The memo should note this as a factor in the next-step decision.

---

## 5. Concrete Corrections and Reframing Recommended

1. **Replace "improves truthfulness" with "improves renderer composability"** for the `source_type` discussion (section "Implementation Shape", calibration detail #1). The system-level inference logic is unchanged; only the renderer's coupling to it improved.

2. **Acknowledge the `"Genealogical Portrait: Genealogical Portrait"` redundancy** in the `context_title` UX delta section. Note it as a known artifact that may warrant a deduplication check in future context_title formatting, without blocking this slice.

3. **Be more precise in the "Calibrated Claim"** about which fields represent new truth vs same-value-through-different-plumbing. The current phrasing "more truthful CaptureSelection" is mostly fair but could be stronger with: "adds `source_workflow_key` and `entity_id` provenance fields and gates on analyzer-owned capturability, while preserving the same downstream `source_type` value through config-derived indirection."

4. **In the "Why This Matters" section**, note that the contract depth consumed on the genealogy surface is shallower than the AOI surfaces (no specialized_family, no per-item handles). The proof value is in surface-family breadth, not contract-depth coverage.

5. **In "Next Honest Step"**, reframe "generic custom-renderer first-hop seam" as "generic selection-emission parameterization." The affordance check is already trivially generic. The hard part is the selection shape.

---

## Summary

The completion memo is honest, well-bounded, and code-accurate on all material claims. The implementation matches what was scoped. Tests verify the landed behavior. The memo does not overclaim strategic significance beyond what the evidence supports. The two required corrections (source_type truthfulness precision, context_title redundancy acknowledgment) are minor and do not change the overall verdict.
