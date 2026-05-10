# Critique: Phase E Genealogy V2 Idea Evolution First-Hop Capture Alignment V1 Scope

Date: 2026-04-03
Reviewer: Claude (Opus 4.6)

Scope Under Review:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_scope.md`

## Verdict

**Approve with corrections.**

The scope is honest about what it is and what it is not. The sequencing is defensible. But the memo has several calibration gaps between what it claims the current code does and what the code actually does, plus one structural assumption about the helper that needs explicit correction.

## Strongest Parts

1. **The sequencing is right.** After the shared helper landed across three adopters (AoiSinFindingsRenderer, AoiThemeFindingsMiniCardList, SynthesisRenderer), testing it on the last materially different current non-AOI renderer is the smallest honest next step. The memo names this correctly and does not skip ahead to generic-law claims.

2. **The scope of capture coverage is honest.** The memo explicitly says capture stays on idea cards only and does not extend to the hero, bifurcations, timeline nodes, foundational patterns, or cross-domain transfers. This matches the current code at `IdeaEvolutionRenderer.tsx:555` where the capture button exists only inside the idea card footer loop.

3. **The "what this is not" section is accurate and important.** No backend change, no analyzer change, no generic renderer-package law, no read-side truth surfacing. This is a real boundary that prevents scope creep.

4. **The decision rule is valuable.** "If the implementation requires widening the helper with renderer-specific branches beyond configurable workflow/job requirements, then stop and recalibrate" — this is the right guardrail.

5. **The `entity_id` calibration language is appropriately cautious.** The memo says `idea.idea_id` is "current rendered idea identity, not cross-run stable canonical identity" — this is honest and correct.

## Weakest Assumptions / Overclaims

### 1. The memo mischaracterizes the current capture config threading

The scope says (Section 2) the renderer should gate on:
- `_workflowKey` present
- `_captureJobId` present
- `_firstHopAffordance?.capturable === true`

But the current `IdeaEvolutionRenderer` (lines 381-386) only reads **four** config fields:
- `_captureMode`
- `_onCapture`
- `_captureJobId`
- `_captureViewKey`

It does **not** currently read:
- `_captureViewName`
- `_captureSourceType`
- `_workflowKey`
- `_captureEntityId`
- `_firstHopAffordance`

The memo says the renderer uses "local `captureMode && onCapture` gating" and lists "no `source_workflow_key`" and "no `entity_id`" as gaps. This is true. But it does not acknowledge that the renderer also does not currently consume `_captureViewName`, `_captureSourceType`, or `_firstHopAffordance` at all. This matters because the implementation is not just replacing one gate — it is adding five new config reads. The memo should name this honestly as the actual delta, not imply the renderer is close to the helper and just needs minor tweaks.

### 2. `source_type` is not "hardcoded" in the renderer — it is a literal

The memo says the renderer has "hardcoded `source_type = "genealogy"`" (line ~48). This is true at line 568:
```
source_type: 'genealogy' as const,
```

But the important nuance is that `V2TabContent` (line 594) also derives `_captureSourceType` as `'genealogy'` for this path via:
```
workflowKey?.includes('genealogy') ? 'genealogy' : 'analysis'
```

So the proposed change from literal `'genealogy'` to config-derived `_captureSourceType` will produce the same runtime value. The memo should say this explicitly — the improvement is composability, not a behavior change.

### 3. The `context_title` change is slightly mischaracterized

The memo says the current shape is `Ideas > <idea name>` from `captureViewKey || "Ideas"`. The actual code at line 567 is:
```
context_title: `${captureViewKey || 'Ideas'} > ${idea.idea_name}`,
```

The proposed shape is `"<_captureViewName>: <idea name>"`. The memo correctly names this as a visible UX delta. But it is worth noting that the current separator is `>` and the proposed separator is `:` (matching the helper convention). The functional difference is:
- Before: `genealogy_idea_evolution > Objectification` (using view key, not view name)
- After: `Idea Evolution: Objectification` (using view name)

That is actually a **better** title, but the memo should note that the current title uses the raw **view_key** (slug), not a human-readable name. The delta is therefore both separator and source, not just separator.

### 4. The test plan is ambitious but the existing test file is minimal

The memo proposes expanding `IdeaEvolutionRenderer.test.tsx` with 8 test categories. But the existing test file has exactly **one** test that only validates `normalizeIdeaEvolutionV2Data`. It does not render the component at all — it does not even import `React` or use `@testing-library`. The actual implementation will need to:

- Set up render infrastructure for the component (mock DesignTokenContext, mock fetch for V1 prose mode, mock CaptureContext)
- Deal with the component's `useEffect` for functional analysis fetching
- Mock or provide `RendererProps` shape

This is a materially larger test-authoring lift than "expand tests." The memo should name this as new test infrastructure, not an expansion of existing tests.

### 5. Browser proof boundary is honest but has a practical gap

The memo says the browser proof should verify the positive path only: "idea-card capture control appears in capture mode → clicking reaches CaptureActionBar → action bar shows title, preview, depth badge, action buttons."

This is fine as a boundary. But the memo says to "cover the no-affordance negative only in unit tests or mocked / fixture-backed browser proof." In practice, the negative path (no `_firstHopAffordance`) cannot be easily proved in a live browser proof because `V2TabContent` threads whatever the analyzer returns. The only way to see the negative in a live browser is to navigate to a genealogy result that lacks an affordance — which would require either a specific test fixture or the absence of the feature on a real run. The memo should acknowledge this and confirm that mocked unit tests are sufficient for the negative path.

## Code-Backed Findings

### Finding 1: Current capture emission is shallow

At `IdeaEvolutionRenderer.tsx:560-571`, the current capture emission is:
```typescript
onCapture({
  source_view_key: captureViewKey || '',
  source_section_key: idea.idea_id,
  source_renderer_type: 'idea_evolution',
  content_type: 'item',
  selected_text: `${idea.idea_name}: ${idea.description || ''}`.slice(0, 500),
  structured_data: { idea, synthesis, traces: tracesAcrossWorks.length },
  context_title: `${captureViewKey || 'Ideas'} > ${idea.idea_name}`,
  source_type: 'genealogy' as const,
  genealogy_job_id: captureJobId || '',
  depth_level: 'L2_element',
});
```

Missing fields compared to the helper convention:
- No `source_workflow_key`
- No `entity_id`
- `genealogy_job_id` uses fallback to empty string rather than config truth
- `source_type` is literal
- `context_title` uses view key, not view name

The scope's proposed emission at Section 4 is well-calibrated to this gap.

### Finding 2: The helper shape is compatible without modification

`resolveCurrentRendererCaptureRuntime` at `currentRendererCapture.ts:26-64` already accepts:
- `requireWorkflowKey: true`
- `requireJobId: true`

And `buildCurrentRendererCaptureSelection` already composes the shared shell (`source_type`, `source_view_key`, `context_title`, `source_workflow_key`) and lets the caller supply the rest via spread.

The renderer-local fields (`entity_id`, `genealogy_job_id`, `source_renderer_type`, `content_type`, `depth_level`) are exactly the kind of local payload the helper was designed to not absorb. **The helper does not need to change for this adoption.** This confirms the scope's assumption.

### Finding 3: `stopPropagation` is already present

The current capture button at line 559 already uses `e.stopPropagation()` on the click handler. The scope correctly names this as something to preserve, and the code confirms it already exists.

### Finding 4: V2TabContent threads all needed config

`V2TabContent.tsx:589-597` already threads all eight fields the helper reads. The renderer just does not consume most of them yet. No V2TabContent changes are needed.

## Strategic Implications

1. **This is genuinely the last current non-AOI renderer.** After `SynthesisRenderer` adopted the helper for `genealogy_portrait`, `IdeaEvolutionRenderer` is the only remaining current non-AOI custom renderer that has capture behavior but sits outside the shared seam. Completing this closes the current renderer set.

2. **This does not prove generic law.** The scope is explicit about this. After this slice, four current custom renderers will share one helper — but that is still a small, known, host-internal set. The value is family-completion evidence, not architecture.

3. **The sequencing prevents premature extraction.** Aligning the last outlier first, then evaluating whether the helper is generic enough, is the right order. Extracting to a package before all current adopters are aligned would be premature.

4. **The `idea_id` as `entity_id` question is calibrated.** Unlike the synthesis renderer where `entity_id` falls back to `_captureJobId` (run-level identity), this renderer can supply genuine item-level identity. That is stronger evidence for the eventual identity model, but the memo correctly avoids overclaiming it as solved.

## Concrete Corrections

1. **Add an honest delta inventory.** The memo should list all five new config fields the renderer will start consuming (not just the two it does not emit). This makes the implementation scope honest.

2. **Clarify that `source_type` will not change at runtime.** State explicitly: "On this path, `_captureSourceType` resolves to `'genealogy'` via `V2TabContent`'s existing heuristic. The change improves composability, not runtime behavior."

3. **Clarify the `context_title` transition.** The current title uses the raw view_key slug, not a human-readable name. The proposed title uses `_captureViewName` which is the human-readable `view_name` from the `ViewPayload`. Name this as a genuine improvement, not just a separator change.

4. **Acknowledge the test-authoring lift honestly.** The current test file has no component rendering infrastructure. The memo's test plan requires building render harness scaffolding from scratch. Name this as new test infrastructure work, not an expansion.

5. **Confirm the negative browser proof boundary.** State explicitly: "The no-affordance negative path will be verified in unit tests only. No live browser proof for the negative case is required or claimed, because the negative path depends on analyzer-side affordance absence which is not controllable from the browser test."

6. **Minor: fix the proposed emission field list.** The scope says `context_title = "<_captureViewName>: <idea.idea_name>"` but the helper builds this internally from `runtime.captureViewName` and the `title` parameter. The implementation will pass `title = idea.idea_name` to `buildCurrentRendererCaptureSelection`, not compose the full title locally. Make this explicit so the implementor does not duplicate the helper's work.
