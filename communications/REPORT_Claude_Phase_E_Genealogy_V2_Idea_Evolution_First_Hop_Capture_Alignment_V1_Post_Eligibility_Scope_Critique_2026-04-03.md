# Critique: Phase E Genealogy V2 Idea Evolution First-Hop Capture Alignment V1 Scope (Post-Eligibility Re-Evaluation)

Date: 2026-04-03
Reviewer: Claude (Opus 4.6)

Scope Under Review:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_scope.md`

Prior Reviews:
- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md` (verdict: reject)
- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md` (verdict: approve with corrections)

Eligibility Prerequisite Completion:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`

## Verdict

**Approve with minor corrections.**

The original Codex rejection was based on a single blocking fact: `genealogy_idea_evolution` did not receive analyzer-side `first_hop_affordance`, so the helper's hard gate on `_firstHopAffordance?.capturable === true` would suppress all capture buttons. That blocker is now removed. The scope is now executable as written, with six minor corrections carried forward from the earlier Claude critique plus one new finding.

## Status of the Original Rejection Reason

The Codex audit's rejection was entirely correct at the time it was written. The central finding was:

> `currentRendererCapture.ts` hard-requires `_firstHopAffordance?.capturable === true` before it returns runtime truth ... analyzer-v2 only emits `first_hop_affordance` for migrated analytical leaf families, and `genealogy_idea_evolution` is still declared on `engine_key = "concept_synthesis"` ... So the memo's proposed runtime gate would currently hide all capture buttons on this surface.

This is no longer true. The eligibility completion confirms:

- `first_hop_affordance.py:52-57` now contains `is_genealogy_idea_evolution_first_hop_eligible_leaf()` which checks `view_key == "genealogy_idea_evolution"` and `engine_key == "concept_synthesis"` and `children == []`
- `derive_first_hop_affordance()` at line 67 calls this as a second eligibility branch alongside the migrated-family check
- the emitted affordance is generic: `capturable=True`, `allowed_destinations=["arsenal", "research_todo"]`, no `specialized_family`
- both presenter paths (job-backed and transient compose) inherit this rule through the shared derivation function

The blocker is resolved. The scope's "host-only" premise is now honest.

## What Is Now Validated

### 1. The helper reuse claim is now sound

The scope says to reuse `resolveCurrentRendererCaptureRuntime(...)` and `buildCurrentRendererCaptureSelection(...)` without helper changes. This is confirmed:

- `resolveCurrentRendererCaptureRuntime` at `currentRendererCapture.ts:26-64` gates on `_firstHopAffordance?.capturable === true` (line 45) — that field will now be present on `genealogy_idea_evolution` payloads
- `buildCurrentRendererCaptureSelection` at `currentRendererCapture.ts:73-85` composes the shared shell with `context_title: "${runtime.captureViewName}: ${title}"` — no renderer-specific branching needed
- `V2TabContent.tsx:597` threads `payload.first_hop_affordance ?? null` to `_firstHopAffordance` — the analyzer-emitted affordance flows through without host invention

The helper does not need to change. This confirms the scope's assumption.

### 2. The SynthesisRenderer adoption pattern is the right model

`SynthesisRenderer.tsx:62-66` shows the exact adoption pattern this scope proposes:

```typescript
const captureRuntime = resolveCurrentRendererCaptureRuntime(config, {
  requireWorkflowKey: true,
  requireJobId: true,
});
```

And selection emission at lines 104-114 uses `buildCurrentRendererCaptureSelection(captureRuntime, {...})` with renderer-local fields passed as params. `IdeaEvolutionRenderer` should follow this same pattern.

### 3. The `requireWorkflowKey: true` and `requireJobId: true` options are correct

The scope names these requirements. They are confirmed as the right options for this surface:

- `_workflowKey` is needed for `source_workflow_key` emission, which the current inline path omits entirely
- `_captureJobId` is needed for `genealogy_job_id` emission, which the current inline path falls back to empty string

Both `SynthesisRenderer` (the other genealogy adopter) uses both requirements.

### 4. The "host-only" boundary is now genuinely host-only

No analyzer files need to change. No backend persistence changes. No new API endpoints. The scope touches exactly one renderer file in the Critic codebase, plus its test file. This is a clean host-only slice.

### 5. V2TabContent already threads all needed fields

`V2TabContent.tsx:588-597` already threads all eight config fields the helper reads:

- `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, `_captureViewName`, `_captureSourceType`, `_captureEntityId`, `_captureStatusMap`, `_firstHopAffordance`

No `V2TabContent` changes are needed. The renderer just needs to start consuming the fields it currently ignores.

## Corrections Still Needed (Carried Forward + New)

### 1. Add an honest delta inventory of new config field reads

The scope says the renderer should gate on `_workflowKey`, `_captureJobId`, and `_firstHopAffordance`. But the actual implementation delta is larger. The renderer currently reads only four config fields (`_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`). After alignment it will read nine:

**New reads:**
- `_captureViewName` (for helper-built `context_title`)
- `_captureSourceType` (replacing hardcoded `'genealogy'`)
- `_workflowKey` (for `source_workflow_key` emission)
- `_captureEntityId` (for fallback `entity_id`)
- `_firstHopAffordance` (for capturable gate)

The scope should name all five new reads explicitly so the implementor understands this is not a minor tweak — it is bringing the renderer onto a substantially richer config contract.

### 2. Clarify that `source_type` will not change at runtime

The scope proposes replacing hardcoded `source_type: 'genealogy' as const` with config-derived `_captureSourceType`. On this path, `V2TabContent.tsx:594` sets `_captureSourceType` to `'genealogy'` via `workflowKey?.includes('genealogy') ? 'genealogy' : 'analysis'`. The runtime value will be identical. The improvement is composability and contract truthfulness, not behavior change. The scope should state this explicitly so reviewers do not expect a visible difference.

### 3. Clarify the `context_title` transition accurately

The scope says the current shape is `"${captureViewKey || 'Ideas'} > ${idea.idea_name}"`. The actual code at `IdeaEvolutionRenderer.tsx:567` confirms this. But the scope should note:

- The current title uses the raw **view_key slug** (e.g., `genealogy_idea_evolution`), not a human-readable name
- The proposed title uses `_captureViewName` which carries the human-readable `view_name` from the view definition (e.g., `"Idea Evolution"`)
- The separator changes from `>` to `:` (matching the helper convention at `currentRendererCapture.ts:80`)
- This is a genuine UX improvement: `"Idea Evolution: Objectification"` is better than `"genealogy_idea_evolution > Objectification"`

Name it as a dual improvement (human-readable name + consistent separator), not just a separator change.

### 4. Acknowledge the test infrastructure lift honestly

The scope says to expand `IdeaEvolutionRenderer.test.tsx` with 8 test categories. But the existing test file has exactly one test that validates `normalizeIdeaEvolutionV2Data` — a pure function test. It does not render the component, does not import React or `@testing-library`, and has no mock infrastructure for `DesignTokenContext`, `CaptureContext`, or `RendererProps`.

The scope's test plan requires building component render infrastructure from scratch. This is new test scaffolding work, not an expansion of existing tests. The scope should name it as such and estimate it as a material portion of the implementation effort.

### 5. Confirm the negative browser proof boundary

The scope says to "cover the no-affordance negative only in unit tests or mocked / fixture-backed browser proof." This is correct and should be stated more firmly: the no-affordance negative path cannot be proved in a live browser without controlling the analyzer-side affordance emission, which would require either a test fixture or a separate analyzer-side test mode. Unit/mock tests are the right boundary for the negative path.

### 6. Clarify that `buildCurrentRendererCaptureSelection` builds `context_title` internally

The scope's proposed emission (Section 4) lists `context_title = "<_captureViewName>: <idea.idea_name>"`. But the helper builds this internally at `currentRendererCapture.ts:80`:

```typescript
context_title: `${runtime.captureViewName}: ${title}`,
```

The implementor should pass `title: idea.idea_name` as a param to `buildCurrentRendererCaptureSelection`, not compose the full `context_title` locally. If the scope leaves this ambiguous, the implementor may duplicate the helper's work. State explicitly: "Pass `title: idea.idea_name` to the builder; the helper composes the full `context_title` from `_captureViewName` + `title`."

### 7. (New) Pin the `entity_id` fallback pattern from SynthesisRenderer

`SynthesisRenderer.tsx:113` uses `entity_id: captureRuntime.captureEntityId || captureRuntime.captureJobId || ''` — a two-level fallback. The scope proposes `entity_id = idea.idea_id`, which is stronger because it provides genuine item-level identity rather than run-level fallback.

But the scope should decide: does `IdeaEvolutionRenderer` use `idea.idea_id` directly (bypassing the `_captureEntityId` config field), or does it prefer `idea.idea_id` over `_captureEntityId` as a renderer-local override?

The honest answer is: use `idea.idea_id` directly. The `_captureEntityId` field from `V2TabContent` is set to `presentation.job_id` (line 595), which is run-level identity. For item-level capture, the renderer's own `idea.idea_id` is more specific and should take precedence. The scope should say this explicitly: "`entity_id` uses `idea.idea_id` directly, not the config-derived `_captureEntityId`, because item-level identity is available and more specific than run-level fallback."

## Code-Backed Confidence Assessment

### The implementation path is clean

The change touches one file with a well-understood pattern. The SynthesisRenderer adoption (lines 62-131) is a direct template. The required steps are:

1. Import `resolveCurrentRendererCaptureRuntime` and `buildCurrentRendererCaptureSelection`
2. Replace the four-field inline config extraction with a single `resolveCurrentRendererCaptureRuntime(config, { requireWorkflowKey: true, requireJobId: true })` call
3. Replace the `captureMode && onCapture` gate with `Boolean(captureRuntime)`
4. Replace the inline `onCapture({...})` call with `captureRuntime.onCapture(buildCurrentRendererCaptureSelection(captureRuntime, {...}))`
5. Keep `stopPropagation()` on the button click handler
6. Keep capture coverage limited to idea cards only

No helper changes. No V2TabContent changes. No analyzer changes.

### The affordance will be present on live pages

After the eligibility completion:
- `derive_first_hop_affordance` returns `FirstHopAffordance(capturable=True, ...)` for `genealogy_idea_evolution` leaves
- This flows through `attach_first_hop_affordances` on the job-backed path
- `V2TabContent` threads it to `_firstHopAffordance`
- The helper gate `_firstHopAffordance?.capturable === true` will pass

So the positive browser proof is now achievable on a live genealogy result page.

### No specialized_family contamination

The eligibility completion confirmed: no `specialized_family` is set on this surface. The specialized-family logic only fires for `aoi_by_sin_type` / `aoi_sin_findings` combinations gated by `workflow_key == "aoi_v2"`. The genealogy path produces a plain generic affordance.

## Strategic Assessment

### 1. This is the right next step

The program now has:
- Analyzer-side eligibility for `genealogy_idea_evolution` (just completed)
- A shared helper with three adopters (`AoiSinFindingsRenderer`, `AoiThemeFindingsMiniCardList`, `SynthesisRenderer`)
- One remaining current non-AOI renderer outlier (`IdeaEvolutionRenderer`)

Closing this outlier completes the current renderer set. After this, the helper will have been adopted by all four current custom renderers with capture behavior. That is family-completion evidence.

### 2. This does not prove generic law

The scope is explicit: this is one more bounded data point, not architecture. Four current adopters on one shared helper is evidence for eventual extraction, not proof that the helper is generic enough. The scope does not overclaim.

### 3. The two-step sequencing is now validated

The Codex audit's rejection forced a correct two-step sequence:
1. Analyzer-side eligibility (done)
2. Host-side helper adoption (this scope)

That sequencing proved the program's willingness to fix upstream blockers rather than work around them downstream. This is a good precedent for the analyzer-v2-as-brain direction.

### 4. After this lands, the next question changes

Once all four current renderers share the helper, the next honest question is no longer "can one more renderer adopt?" but "is the helper stable enough across its adopter set to consider extraction into a shared package?" That is a Phase F question, not a Phase E question. The scope correctly stays within Phase E boundaries.

## Final Assessment

The scope is now executable. The original rejection reason is resolved. The scope's core claims — host-only, helper reuse without changes, narrow capture coverage, honest identity language — are all code-backed and sound. Apply the seven corrections above (six carried forward, one new) to tighten the implementation guidance, then proceed.
