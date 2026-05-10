# Memo: Phase E Genealogy V2 Idea Evolution First-Hop Capture Alignment V1 Completion

Subtitle: One bounded host-only non-AOI current renderer now consumes the landed `currentRendererCapture` seam plus analyzer-owned generic first-hop capturability on idea cards without widening analyzer, backend, or read-side semantics

Date: 2026-04-04
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
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_scope.md`
Review Context:
- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Post_Eligibility_Scope_Critique_2026-04-03.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Record what actually landed after the bounded analyzer-side eligibility prerequisite removed the real upstream blocker on `genealogy_idea_evolution`.

This slice is about one last materially broader current non-AOI renderer consuming already-landed host and analyzer truth more honestly.
It is not a claim that:

- generic renderer-package law now exists
- current-renderer identity semantics are unified
- genealogy read-side capture truth now exists
- analyzer-v2 needed richer first-hop semantics
- backend or persistence behavior needed to change

## What Landed

One bounded host-only alignment slice is now complete on the live non-AOI `genealogy_idea_evolution` surface in Critic.

The landed behavior is:

1. `IdeaEvolutionRenderer` no longer relies on local `captureMode && onCapture` gating alone
2. idea-card capture now resolves through the already-landed `currentRendererCapture` seam with:
   - `requireWorkflowKey: true`
   - `requireJobId: true`
3. the renderer now consumes the additional helper-threaded inputs it previously ignored:
   - `_captureViewName`
   - `_captureSourceType`
   - `_workflowKey`
   - `_firstHopAffordance`
4. `_captureEntityId` is now part of the runtime contract on this path but remains intentionally unused for emitted item identity
5. emitted idea-card selections now include:
   - helper-built `context_title`
   - `source_workflow_key`
   - preserved `genealogy_job_id`
   - item-level `entity_id = idea.idea_id`
6. capture coverage stayed intentionally narrow:
   - capture remains available only on idea cards
   - hero, bifurcation, timeline, trace, summary, and other non-card regions remain passive
7. the proof boundary remains the existing `CaptureActionBar`
8. no analyzer-v2 runtime changes landed in this slice
9. no backend or persistence changes landed in this slice

## The Final Boundary

The honest completed claim is:

- the last materially broader current non-AOI renderer outlier now consumes the existing current-renderer capture seam plus analyzer-owned generic first-hop capturability on its bounded item surface

What this does mean:

- all four live current custom-renderer capture consumers now ride the same narrow helper seam
- `IdeaEvolutionRenderer` no longer hardcodes local genealogy selection provenance
- item-level identity is now emitted on this surface where it was previously omitted

What this does not mean:

- generic renderer-package law is now proven
- the helper is automatically ready for shared-package promotion
- `entity_id` is now cross-run canonical genealogy identity
- destination policy or read-side status semantics are now solved on this surface
- all genealogy renderers now share one common item model

## Implementation Shape

The implementation stayed local to Critic and local to `IdeaEvolutionRenderer`.

The landed shape is:

- `V2TabContent` continues to thread the capture/runtime metadata it already had:
  - `_captureMode`
  - `_onCapture`
  - `_captureViewKey`
  - `_captureViewName`
  - `_captureSourceType`
  - `_workflowKey`
  - `_captureJobId`
  - `_captureEntityId`
  - `_firstHopAffordance`
- `IdeaEvolutionRenderer` now resolves runtime through `resolveCurrentRendererCaptureRuntime(...)`
- the renderer uses an explicit post-resolution local assertion so `captureJobId` and `sourceWorkflowKey` are treated as truly present after runtime resolution rather than drifting back to `|| ''`
- idea-card clicks now call `buildCurrentRendererCaptureSelection(...)`
- the renderer passes `title = idea.idea_name` and lets the helper compose `context_title`
- emitted `entity_id` is pinned directly to `idea.idea_id`, not config fallback
- `stopPropagation()` stayed in place so capture clicks do not toggle card expansion accidentally

Three calibration details matter:

1. **`source_type` stayed behaviorally the same**

The renderer now consumes `_captureSourceType` from the threaded config rather than hardcoding `"genealogy"`.
On this path the runtime value still resolves to:

- `"genealogy"`

So this is a composability improvement, not a behavior change.

2. **`context_title` became more truthful and more human-readable**

The old local title shape was effectively:

- raw view-key / fallback driven
- `>`

The new helper-built title shape is:

- human-readable `view_name`
- `:`

So the visible delta is real but bounded:

- `Idea Evolution: Objectification`

3. **Fresh test scaffolding was part of the real work**

`IdeaEvolutionRenderer.test.tsx` no longer only proves normalization behavior.
This slice added actual component-test scaffolding for:

- positive helper-resolved capture
- fail-closed missing-config cases
- exact emitted selection shape
- click propagation safety

## Verification

Focused host unit verification passed:

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/components/renderers/IdeaEvolutionRenderer.test.tsx src/lib/currentRendererCapture.test.ts src/components/V2TabContent.test.tsx src/contexts/CaptureContext.test.tsx`
  - `26 passed`

Focused browser verification also passed:

- `npx playwright test tests/genealogy-v2-idea-evolution-capture.spec.ts --project=chromium`
  - `1 passed`

The browser proof stayed at the intended boundary:

- live `genealogy_idea_evolution` content renders
- entering capture mode exposes the bounded idea-card capture control
- clicking it reaches the existing `CaptureActionBar`
- the action bar shows:
  - title
  - preview text
  - depth badge
  - action buttons

Environment honesty notes:

- Jest still prints the repo's existing post-run open-handle warning after the passing frontend batch
- Playwright still required the frontend to run with `TSC_COMPILE_ON_ERROR=true DISABLE_ESLINT_PLUGIN=true` because the repo has unrelated existing TypeScript warnings outside this slice

## Calibrated Claim

Before this slice, the strongest honest `genealogy_idea_evolution` claim was:

- the analyzer-side affordance blocker was removed
- but the host renderer still assembled capture selections locally and omitted key provenance fields

After this slice, the stronger honest claim is:

- the full current custom-renderer capture set in Critic now uses one shared runtime-resolution / selection-shell seam across:
  - AOI pure findings
  - AOI mixed thematic findings
  - non-AOI genealogy sections
  - non-AOI genealogy idea cards

That is materially stronger than the prior state.
But it is still bounded:

- one local helper
- one host app
- one renderer family set
- no package promotion yet

## Why This Matters

This slice matters because it closes the last obvious current-renderer outlier without inventing new substrate.

It strengthens the analyzer-v2-as-brain direction in a specific, defensible way:

- the host no longer keeps a separate local capture-assembly pattern on `genealogy_idea_evolution`
- the current helper seam is no longer just a three-renderer convenience
- the seam now spans both AOI and non-AOI current renderers, and both section-level and item-level capture shapes

That is enough to change the next question.

## Next Honest Step

The next honest question is no longer:

- can one more current renderer adopt the local helper seam

That is now answered.

The next question is:

- is the now-four-adopter `currentRendererCapture` seam honest enough for promotion beyond Critic-local ownership
- or is Critic-local ownership still the right ceiling for this helper

That question should be treated as a bounded readiness / promotion-calibration step, not an automatic extraction claim.

Why the calibration step is necessary:

- the helper still imports the Critic-local `CaptureSelection` type
- the four adopters still have materially different local identity and shape rules
- the shared renderers package boundary is not yet a proven destination in the active workspace

So the next memo should scope:

- one bounded current-renderer shared-seam promotion-readiness slice

What should **not** happen next:

- another current-renderer proof just to accumulate more local evidence
- a reflexive shared-package extraction claim
- a generic renderer-law claim
- destination-policy, read-side status, or backend/analyzer widening
