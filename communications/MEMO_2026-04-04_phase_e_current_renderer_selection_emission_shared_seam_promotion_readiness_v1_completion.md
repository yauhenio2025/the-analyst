# Memo: Phase E Current-Renderer Selection Emission Shared-Seam Promotion Readiness V1 Completion

Subtitle: The four-adopter Critic-local `currentRendererCapture` seam is not honest for shared-package promotion unchanged, and the strongest next honest candidate is one smaller package-neutral capture-base shell while first-hop, workflow/job, and typed-selection policy remain local

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
Immediate Prior Scope:
- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_scope.md`
Immediate Prior Completion:
- `communications/MEMO_2026-04-04_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_completion.md`
Review Inputs:
- `communications/REPORT_Codex_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Audit_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Critique_2026-04-04.md`
Codebases:
- `/home/evgeny/projects/the-critic`
- `/home/evgeny/projects/analyzer-v2/renderers-ui`

## Purpose

Close the bounded readiness-calibration question that became honest only after the fourth live Critic custom-renderer adopter landed.

That question was:

- should `currentRendererCapture` remain Critic-local
- should it be promoted unchanged into `@the-syllabus/analysis-renderers`
- or is only a smaller shared shell actually honest

This slice was deliberately docs-first.
It was not a code-move slice.
Its job was to compare the real local helper architecture against the real existing shared-package capture architecture and force an explicit verdict.

## What Was Inspected

The calibration inspected both capture architectures directly.

### Critic-local current-renderer seam

- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.test.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`

### Shared-package existing capture architecture

- `/home/evgeny/projects/analyzer-v2/renderers-ui/package.json`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardRenderer.tsx`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardGridRenderer.tsx`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `/home/evgeny/projects/the-critic/webapp/package.json`

## Headline Verdict

The readiness verdict is:

- **ready only for a narrower shell**

The honest completed conclusion is:

- `currentRendererCapture` is **not** ready for shared-package promotion unchanged
- the strongest next honest candidate for promotion is a smaller package-neutral capture-base utility shaped around the shared package's already-existing raw `config._onCapture` architecture
- Critic-local `CaptureSelection`, `_firstHopAffordance` fail-closed gating, workflow/job requirements, and renderer-specific identity/preview policy should remain local unless a separate shared contract is defined first

## Why Unchanged Promotion Failed

The blocker is not destination uncertainty.

The destination is real and already analyzer-v2-owned:

- `@the-syllabus/analysis-renderers`
- source tree:
  - `/home/evgeny/projects/analyzer-v2/renderers-ui`
- Critic dependency wiring:
  - `/home/evgeny/projects/the-critic/webapp/package.json`

The failure is architectural fit.

`currentRendererCapture` assumes semantics that the package's current generic capture builders do not share:

- Critic-local typed `CaptureSelection`
- helper-owned `_firstHopAffordance?.capturable === true` fail-closed gating
- helper-owned `requireWorkflowKey`
- helper-owned `requireJobId`
- helper-built `source_workflow_key`
- helper-built human-readable `view_name` + `:` title composition

The package-side builders already operate on a different baseline:

- raw `config._onCapture`
- `Record<string, unknown>` selection payloads
- no `CaptureSelection` import
- no `_firstHopAffordance` gate
- no required workflow/job checks
- `captureViewKey`-driven `>` title composition

Promoting the helper unchanged would therefore do one of two dishonest things:

1. force Critic-local first-hop/workflow policy into the package without a shared contract
2. create an incoherent two-tier capture architecture inside the same package

Neither is a valid promotion result.

## Comparison Matrix

| Dimension | Critic `currentRendererCapture` | Existing `renderers-ui` raw capture path | Readiness consequence |
| --- | --- | --- | --- |
| Typing | imports Critic `CaptureSelection` and returns that shape | uses `Record<string, unknown>` locally in package renderers/sub-renderers | unchanged helper is not package-neutral |
| Runtime inputs | `_captureMode`, `_onCapture`, `_captureViewKey`, `_captureViewName`, `_captureSourceType`, `_firstHopAffordance`, optional `_workflowKey`, optional `_captureJobId`, optional `_captureEntityId` | `_captureMode`, `_onCapture`, `_captureViewKey`, `_captureSourceType`, optional `_captureJobId`, optional `_captureEntityId` | helper expects stricter host-threaded inputs than package renderers currently use |
| Gating | fail-closed on `_firstHopAffordance?.capturable === true`; optional `requireWorkflowKey` and `requireJobId` | typically `captureMode && onCapture` only | `_firstHopAffordance` and workflow/job policy are not shared today |
| Title composition | helper builds `"<captureViewName>: <title>"` | package builders compose `"<captureViewKey> > ..."` chains | title law is divergent, not yet one shared policy |
| Workflow/job policy | explicit helper options; some adopters assert workflow/job presence post-resolution | no equivalent package abstraction | these requirements remain Critic-local current-renderer law |
| Identity fallback | left local to adopters | package renderers often default to `captureEntityId || captureJobId` | identity modeling is not currently shared |
| Fields emitted into selection | always injects `source_type`, `source_view_key`, `context_title`, optional `source_workflow_key`; rest from caller | injects raw shell fields directly inline per renderer | the next honest extraction candidate is only the smaller raw shell, not the full helper |

## What The Calibration Identified As The Smallest Honest Candidate

The strongest next candidate is:

- a package-neutral raw capture-base utility in `renderers-ui`

Its exact honest API should be something like:

1. `resolvePackageCaptureBaseRuntime(config)`
2. `buildPackageCaptureSelectionBase(runtime, params)`

The bounded shared responsibility of that shell would be:

- read only package-common raw capture config:
  - `_captureMode`
  - `_onCapture`
  - `_captureViewKey`
  - `_captureSourceType`
  - optional `_captureJobId`
  - optional `_captureEntityId`
- return a package-neutral runtime shaped around:
  - `onCapture: (sel: Record<string, unknown>) => void`
  - `sourceViewKey: string`
  - `sourceType: string`
  - `captureJobId?: string`
  - `captureEntityId?: string`
- build only the package-generic selection base:
  - `source_view_key`
  - `source_type`
  - `context_title` from caller-supplied title segments using existing package `>` composition
  - optional raw identity fallback when the caller does not supply a more specific `entity_id`

That is the smallest candidate the calibration identified as plausibly matching the package's current architecture.
This slice did not prove that extraction through package implementation and package-side verification yet.

## What Must Remain Critic-Local

The following concerns should remain Critic-local unless a separate shared contract is defined first:

- Critic `CaptureSelection` typing
- `CurrentRendererCaptureRuntime` as a typed host helper contract
- `_firstHopAffordance` fail-closed gating
- `requireWorkflowKey`
- `requireJobId`
- `source_workflow_key`
- human-readable `view_name` + `:` title composition
- `genealogy_job_id`
- renderer-specific `entity_id` policy
- renderer-specific preview-text generation
- renderer-specific `parent_context`
- specialization and nested-handle gating
- renderer-local status/readback behavior

This is the hard boundary that keeps the narrower-shell verdict honest.

## What The Slice Answered

### 1. Are the two current helper options still sufficient across the four adopters?

Yes.
The evidence remains:

- `AoiSinFindingsRenderer`: `requireWorkflowKey: false`
- `AoiThemeFindingsMiniCardList`: `requireWorkflowKey: true`
- `SynthesisRenderer`: `requireWorkflowKey: true`, `requireJobId: true`
- `IdeaEvolutionRenderer`: `requireWorkflowKey: true`, `requireJobId: true`

No third helper option is required today.

### 2. What is truly shared versus renderer-local?

The local helper already drew the right boundary for Critic:

- shared:
  - runtime resolution
  - shared selection-shell fields
- local:
  - identity
  - preview text
  - coverage
  - specialization/nested-handle gates
  - compatibility fields like `genealogy_job_id`

But that Critic-local shared subset is still broader than the package's actual common denominator.

### 3. Is the Critic-local type coupling acceptable for promotion?

Not unchanged.

The coupling is not fatal in principle.
But it is strong enough that unchanged helper promotion would mostly export Critic assumptions into the package.

### 4. Does a real destination exist?

Yes.
That question is now closed.

The real question was destination fit, and the answer is:

- not for unchanged helper promotion
- yes to advancing one smaller package-neutral capture-base shell as the next honest extraction candidate

### 5. Should promotion replace or supplement the package's existing raw capture pattern?

If the narrower shell is pursued, it should **supplement-then-converge** rather than immediately replace everything.

Why:

- the package already has multiple inline raw capture builders
- those builders are not yet uniformly equivalent
- the first honest move is to extract the raw shared base they already mostly share

This is not yet an argument for replacing Critic-local `currentRendererCapture`.

## Verification

Focused Critic stability verification passed:

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/lib/currentRendererCapture.test.ts src/components/renderers/AoiSinFindingsRenderer.test.tsx src/components/renderers/AoiThemeFindingsMiniCardList.test.tsx src/components/renderers/SynthesisRenderer.test.tsx src/components/renderers/IdeaEvolutionRenderer.test.tsx src/components/V2TabContent.test.tsx src/contexts/CaptureContext.test.tsx`
  - `7 suites passed`
  - `45 tests passed`

This verification was used only as a behavior lock for the readiness analysis.
No runtime extraction or package move was attempted in this slice.

Environment honesty note:

- Jest still prints the existing open-handle warning after the passing batch

## What Changed Strategically

Before this slice, the strongest honest next-step statement was:

- evaluate whether the four-adopter helper seam is promotion-ready

After this slice, the stronger honest statement is:

- the current helper seam is **not** promotion-ready unchanged
- the honest shared candidate is a smaller package-neutral capture-base shell aligned to `renderers-ui`'s existing raw capture architecture

That is useful Phase E evidence.
It prevents fake genericity and narrows the real reusable substrate more precisely than the earlier helper-level hope.

## Next Honest Step

The next honest step is **not**:

- promote `currentRendererCapture` into `renderers-ui`

The next honest step is:

- scope one bounded `renderers-ui` generic capture-base shell extraction slice

That next slice should target only the narrower candidate shell named above and should stay below:

- Critic `CaptureSelection` typing
- first-hop policy
- workflow/job requiredness
- `source_workflow_key`
- `genealogy_job_id`
- host-specific identity and preview law
- generic renderer-package law claims

If that narrower shell cannot be extracted cleanly against the package's existing raw builders, the fallback remains respectable:

- keep the current helper local and stop there

## Final Completed Claim

This readiness slice is now complete.

Its finished claim is:

- the four-adopter Critic-local `currentRendererCapture` seam is not honest for shared-package promotion unchanged
- one smaller package-neutral capture-base shell has been identified as the next honest extraction candidate
- and the exact policy/type/identity concerns that must remain Critic-local are now explicit
