# Memo: Phase E Current-Renderer Selection Emission Parameterization V1 Completion

Subtitle: One bounded host-only shared seam now parameterizes repeated capture runtime resolution and shared `CaptureSelection` assembly across three live current custom renderers without overclaiming generic renderer law

Date: 2026-04-03
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Prior Code Completion:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
Strategic Trigger:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Record what actually landed after the bounded `genealogy_portrait` non-AOI proof closed:

- not another AOI consumer slice
- not backend or analyzer change
- not generic renderer-package law

The question here was narrower:

- is there now a smallest honest shared seam for the already-proved current custom-renderer capture consumers in Critic

## What Landed

One bounded host-only shared seam is now complete in Critic for three current custom-renderer capture consumers:

- `AoiSinFindingsRenderer`
- `AoiThemeFindingsMiniCardList`
- `SynthesisRenderer`

The landed shape is:

1. one new pure internal helper module now exists:
   - `webapp/src/lib/currentRendererCapture.ts`
2. that helper exposes two deliberately narrow functions:
   - `resolveCurrentRendererCaptureRuntime(...)`
   - `buildCurrentRendererCaptureSelection(...)`
3. the resolved runtime shape is explicit and shared:
   - `onCapture`
   - `sourceType`
   - `sourceViewKey`
   - `captureViewName`
   - optional `sourceWorkflowKey`
   - optional `captureJobId`
   - optional `captureEntityId`
4. the runtime resolver now centralizes the repeated always-shared gate:
   - capture mode on
   - handler present
   - view key present
   - view name present
   - source type present
   - `_firstHopAffordance?.capturable === true`
5. workflow and job requirements are now parameterized rather than forced globally:
   - `requireWorkflowKey`
   - `requireJobId`
6. the selection builder now centralizes only the truly shared shell:
   - `source_type`
   - `source_view_key`
   - `context_title = "<captureViewName>: <title>"`
   - optional `source_workflow_key`
7. renderer-local identity and shape logic intentionally stayed local:
   - `entity_id`
   - `genealogy_job_id`
   - `parent_context`
   - `source_renderer_type`
   - `content_type`
   - `depth_level`
   - preview text trimming
   - specialized-family or nested-handle guards
8. all three adopters now use the shared seam without intended behavior change

## The Final Boundary

The honest completed claim is:

- Critic now has one narrow shared current-renderer capture seam for runtime-resolution and shared selection-shell assembly across the three already-proved current custom renderers

What this does mean:

- the repeated `_firstHopAffordance?.capturable === true` gate is no longer duplicated three times
- the repeated `source_type` / `source_view_key` / `context_title` / `source_workflow_key` shell is no longer duplicated three times
- the seam is now explicit enough to test directly

What this does not mean:

- generic renderer-package law is now proven
- `IdeaEvolutionRenderer` is already aligned
- all current custom renderers now share one identity model
- `entity_id` semantics are unified
- preview generation is generic
- `allowed_destinations` policy is now consumed generically
- `source_type` system truth was redesigned
- analyzer or backend semantics changed

## Implementation Shape

The helper stayed deliberately narrow.

### Shared helper

`resolveCurrentRendererCaptureRuntime(...)` reads only the already-threaded runtime config:

- `_captureMode`
- `_onCapture`
- `_captureViewKey`
- `_captureViewName`
- `_captureSourceType`
- `_workflowKey`
- `_captureJobId`
- `_captureEntityId`
- `_firstHopAffordance`

It returns `null` unless the always-shared runtime is present and capturable is true.
Two bounded options preserve adopter-specific behavior:

- `requireWorkflowKey`
- `requireJobId`

`buildCurrentRendererCaptureSelection(...)` then composes only the shared selection shell and leaves the rest to the adopter.

### Adopters

The three adopters now consume that seam with intentionally different local rules:

1. `AoiSinFindingsRenderer`
   - keeps the stronger `isArsenalSpecialization(...)` gate local
   - keeps `entity_id = finding_id` local
   - keeps its current missing-`_workflowKey` behavior
   - still emits `source_workflow_key: undefined` when workflow is absent
2. `AoiThemeFindingsMiniCardList`
   - keeps the weaker mixed-surface gate local
   - keeps nested `finding_id` gating local
   - keeps `entity_id = finding_id` local
   - keeps parent-context logic local
3. `SynthesisRenderer`
   - keeps its narrow section coverage local
   - keeps `genealogy_job_id = _captureJobId` local
   - keeps `entity_id = _captureEntityId || _captureJobId` local
   - preserves the current portrait title artifact:
     - `Genealogical Portrait: Genealogical Portrait`

Two calibration details matter:

1. **This is selection-emission parameterization, not generic law**

The shared part now exists and is real.
But the helper is still intentionally small enough that it does not try to absorb:

- item identity modeling
- preview construction
- destination semantics
- read-side capture truth

2. **`source_type` is still host-derived upstream**

The helper now consumes `sourceType` from config rather than each renderer hardcoding it.
That improves composability and reduces renderer-local drift.
But it does **not** mean the host-wide source-type inference changed:

- `V2TabContent` still resolves `_captureSourceType`

3. **The helper places `entity_id`; it does not invent it**

That is important because the three adopters do not share one identity model:

- AOI pure findings: `finding_id`
- AOI mixed findings: `finding_id`
- genealogy portrait: job/run fallback

The helper is therefore honest precisely because it stopped short of false unification.

## Verification

Focused helper + adopter unit verification passed:

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/lib/currentRendererCapture.test.ts src/components/renderers/AoiSinFindingsRenderer.test.tsx src/components/renderers/AoiThemeFindingsMiniCardList.test.tsx src/components/renderers/SynthesisRenderer.test.tsx src/components/V2TabContent.test.tsx src/contexts/CaptureContext.test.tsx`
  - `35 passed`

Focused live browser verification on the three touched adopter lines also passed:

- `npx playwright test tests/genealogy-v2-portrait-capture.spec.ts tests/aoi-v2-sin-capture.spec.ts tests/aoi-v2-theme-capture.spec.ts --project=chromium`
  - `7 passed`

One small non-goal regression was also kept closed during the extraction:

- AOI `aoi_by_sin_type` read-side status lookup remains independent of capture-mode gating after the helper adoption

Environment honesty notes:

- Jest still prints the repo's existing open-handle warning after the passing frontend batch
- Playwright still required the frontend to run with compile-on-error flags because of unrelated existing TypeScript warnings elsewhere in the app

## Calibrated Claim

Before this slice, the program had three real current-renderer proofs but no explicit shared seam for the repeated runtime-resolution and shared selection-shell logic across them.

After this slice, the stronger honest claim is:

- the current evidence base is now strong enough for one narrow internal current-renderer selection-emission parameterization seam across three live consumers, without forcing shared identity semantics or generic renderer law

That is stronger than the prior state, but still bounded.

The completed seam is:

- internal
- host-only
- helper-scale
- current-renderer-specific

not:

- package-generic
- analyzer-owned
- destination-complete
- identity-unifying

## Why This Matters

This slice matters because it reduces renderer-local duplication without pretending the duplication was the whole problem.

It gives the program:

- one directly testable helper seam
- one honest place where current-renderer capture runtime requirements now live
- one honest place where the shared selection shell now lives

That is useful because the proof matrix is no longer just a set of unrelated local wins.
There is now one explicit shared substrate across:

- AOI pure findings
- AOI mixed thematic findings
- non-AOI synthesis sections

But the reusable-substrate value is still modest because one structurally broader current renderer still sits outside the seam.

## Next Honest Step

The next honest question is no longer whether the three already-proved current renderers can share any seam at all.
That is now answered.

But the first review pass on the candidate `IdeaEvolutionRenderer` follow-on surfaced one real blocker:

- the helper correctly requires `_firstHopAffordance?.capturable === true`
- `V2TabContent` only threads what analyzer-v2 emitted
- `genealogy_idea_evolution` does **not** currently receive `first_hop_affordance`

So the next code move should not be the host-side renderer adoption first.

The next honest scoped question should be:

- should analyzer-v2 broaden generic first-hop affordance eligibility just enough for the `genealogy_idea_evolution` analytical leaf, without globally blessing `concept_synthesis` or widening semantics

Only after that lands does the host-side follow-on become honest:

- can `IdeaEvolutionRenderer` then consume the already-landed current-renderer capture seam plus generic first-hop capturability without forcing helper exceptions or generic renderer-package claims

What should **not** happen next:

- another AOI-only current-consumer slice
- a premature claim that current-renderer parameterization is now “done”
- generic package extraction
- read-side genealogy capture truth surfacing
- backend or persistence expansion

So the roadmap posture changes in one specific way:

- the shared selection-emission seam is now real inside the current-renderer set
- but the immediate next move is one small analyzer-side affordance-eligibility prerequisite for `genealogy_idea_evolution`, not the host adoption itself
