# Critique: Phase E Current-Renderer Selection Emission Shared-Seam Promotion Readiness V1 Scope

Date: 2026-04-04
Reviewer: Claude (Opus 4.6)

Scope Under Review:
- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_scope.md`

Prior Context Reviewed:
- `communications/MEMO_2026-04-04_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`
- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Post_Eligibility_Scope_Critique_2026-04-03.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`

Codebase Files Inspected:
- `the-critic/webapp/src/lib/currentRendererCapture.ts`
- `the-critic/webapp/src/lib/currentRendererCapture.test.ts`
- `the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
- `the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.tsx`
- `the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx`
- `the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
- `the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.test.tsx`
- `the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.test.tsx`
- `the-critic/webapp/src/components/renderers/SynthesisRenderer.test.tsx`
- `the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.test.tsx`
- `the-critic/webapp/src/components/V2TabContent.tsx`
- `the-critic/webapp/src/contexts/CaptureContext.tsx`
- `the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/package.json`
- `the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/src/types/index.ts`
- `the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/src/index.ts`
- `the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/src/sub-renderers/SubRenderers.tsx`
- `the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/src/renderers/CardGridRenderer.tsx`
- `the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/src/renderers/AccordionRenderer.tsx`
- `the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/src/renderers/CardRenderer.tsx`
- `analyzer-v2/renderers-ui/package.json`
- `analyzer-v2/renderers-ui/src/index.ts`
- `the-critic/webapp/package.json` (dependency line)

## Verdict

**Approve with corrections.**

The memo asks the right next question. The framing as a readiness-calibration step rather than an automatic extraction is honest and defensible. But it contains one factual error that materially changes the calibration, and it under-specifies the scope of what the calibration must inspect.

## The Memo's Strongest Points

### 1. The question is correctly timed

All four custom-renderer capture consumers now ride the same `currentRendererCapture` seam. The breadth covers two workflow families (AOI and genealogy), two capture depths (`L1_section` and `L2_element`), and three distinct identity models. The memo is right that the next honest variable is no longer renderer breadth — it is ownership.

### 2. The calibration-first posture is correct

Framing this as a readiness assessment rather than an automatic extraction prevents premature code movement. The five calibration questions (stability, shared-vs-local separation, type coupling, destination reality, verdict) are well-chosen.

### 3. The type coupling honesty is real

The memo correctly identifies that `currentRendererCapture.ts` imports Critic-local `CaptureSelection` and that its callback is typed in Critic-local terms. This is the genuine coupling that makes promotion non-trivial.

### 4. The trichotomy verdict is well-calibrated

The three possible outcomes — promotion-ready, not ready, narrower shell — are the right set. They prevent the calibration from being a rubber-stamp exercise.

### 5. The negative-scope list is thorough

The memo is explicit about what this slice is not: no package extraction, no type redesign, no backend changes, no destination policy, no generic renderer law. This prevents scope creep during calibration.

## The Weakest Assumptions or Overclaims

### 1. FACTUAL ERROR: The package source IS known and available

The memo states at lines 108-111:

> in the active workspace, the only clearly visible shared-renderer package boundary is the installed dependency copy under:
> `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers`
> there is no clearly established first-class source repo for that package in the current working set

This is wrong. The source repository for `@the-syllabus/analysis-renderers` is:

- `/home/evgeny/projects/analyzer-v2/renderers-ui/`

The Critic's `package.json` line 10 explicitly references it:

```
"@the-syllabus/analysis-renderers": "file:../../analyzer-v2/renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.5.tgz"
```

The `renderers-ui/` directory contains the full TypeScript source, build scripts, and release tooling. It ships at version 0.6.5. It is a first-class part of the analyzer-v2 workspace.

This error matters because it misframes the calibration. If the source is known and owned inside analyzer-v2, then "is there a real destination for promotion?" (question 4) has a partially pre-answered basis. The calibration should still run — but its starting position is less uncertain than the memo claims.

### 2. The memo omits the existing shared-package capture architecture

The memo treats `currentRendererCapture` and its four Critic-local adopters as the entire capture surface. It is not.

The shared `@the-syllabus/analysis-renderers` package already contains substantial capture code in a different architecture:

- `AccordionRenderer.tsx`: raw `config._onCapture` at line 107, emits at line 370
- `CardGridRenderer.tsx`: local `CaptureSelection = Record<string, unknown>` at line 29, raw capture at line 530
- `CardRenderer.tsx`: raw `config._onCapture` at line 151, emits at line 281
- `SubRenderers.tsx`: local `CaptureSelection = Record<string, unknown>` at line 36, then 8+ sub-renderers each independently reading `config._onCapture`

These shared-package renderers already use a type-agnostic capture pattern: `CaptureSelection = Record<string, unknown>`. They do NOT import Critic-local types. They do NOT use `currentRendererCapture`.

So the calibration must inspect TWO capture architectures, not one:

1. **Critic-local custom renderers**: 4 adopters using the structured `currentRendererCapture` helper with typed `CaptureSelection`
2. **Shared-package generic renderers**: 10+ renderers using raw `config._onCapture` with `Record<string, unknown>`

The promotion-readiness question must answer: should these converge? Can they? Or is the two-tier architecture actually correct (generic renderers stay untyped, custom renderers use a helper)?

### 3. The CaptureSelection coupling is real but narrower than implied

The memo frames the Critic-local `CaptureSelection` import as a potential blocker for promotion. But inspecting the actual types:

`CaptureContext.tsx` defines `CaptureSelection` with ~15 fields. The `currentRendererCapture.ts` helper actually uses `CaptureSelection` in three places:

1. `import type { CaptureSelection }` (line 1)
2. `onCapture: (selection: CaptureSelection) => void` in the runtime interface (line 4)
3. `sourceType: CaptureSelection['source_type']` — a type-level index (line 5)
4. `buildCurrentRendererCaptureSelection(...)` returns `CaptureSelection` (line 76)

The builder function's `CaptureSelectionSharedParams` (line 66-71) is defined as `Omit<CaptureSelection, 'source_type' | 'source_view_key' | 'context_title' | 'source_workflow_key'> & { title: string }`.

This means the helper is structurally dependent on the `CaptureSelection` shape, not just nominally. But the shared package already has a working escape hatch: `Record<string, unknown>`. A promoted version could use a generic type or a minimal interface rather than importing the full Critic-local type.

The coupling is real but not insurmountable. The calibration should characterize it precisely rather than treating it as a binary blocker.

## Code-Backed Findings

### Finding 1: IdeaEvolutionRenderer already wraps the helper with a local type assertion

`IdeaEvolutionRenderer.tsx:375-395` defines:

```typescript
type IdeaEvolutionCaptureRuntime = CurrentRendererCaptureRuntime & {
  captureJobId: string;
  sourceWorkflowKey: string;
};
```

Then `resolveIdeaEvolutionCaptureRuntime()` calls the shared helper and asserts that the optional fields are actually present. This is evidence that the shared helper's optionality model is correct — adopters that need tighter guarantees wrap it locally. This pattern would survive promotion.

### Finding 2: The helper's option set is empirically stable

Across all four adopters:

| Adopter | `requireWorkflowKey` | `requireJobId` |
|---------|---------------------|----------------|
| AoiSinFindingsRenderer | `false` | (default false) |
| AoiThemeFindingsMiniCardList | `true` | (default false) |
| SynthesisRenderer | `true` | `true` |
| IdeaEvolutionRenderer | `true` | `true` |

No adopter requires additional option flags. The two-option model has held across four materially different surfaces. This is positive evidence for stability.

### Finding 3: The shared package renderers already solve the type problem differently

`renderers-ui/src/sub-renderers/SubRenderers.tsx:35-36`:
```typescript
// CaptureSelection is passed via config._onCapture — no direct type import needed
type CaptureSelection = Record<string, unknown>;
```

The shared package deliberately avoids importing any host-local type. If the helper were promoted into the package, it could follow the same pattern: define a minimal interface locally rather than importing from any host.

### Finding 4: The `buildCurrentRendererCaptureSelection` return type is the real coupling point

The builder function at `currentRendererCapture.ts:73-85` explicitly returns `CaptureSelection`. In a promoted version, this would either need to:

- return a generic `Record<string, unknown>` (losing type safety)
- define a minimal `CaptureSelectionBase` interface in the package
- export the builder as generic (`<T extends CaptureSelectionBase>`)

This is the design decision the calibration must make. It is not a blocker — it is a trade-off.

### Finding 5: `_firstHopAffordance` gating is NOT in the shared package

The critical `_firstHopAffordance?.capturable === true` gate that `currentRendererCapture.ts` enforces (line 45-46) is entirely absent from the shared package's renderers. The package renderers gate on `captureMode && onCapture` only.

This means the helper introduces a stricter contract than what generic renderers currently use. If promoted, should the package renderers adopt this stricter gate too? Or should the helper coexist alongside the legacy pattern? The calibration should address this.

## Strategic Implications for the Roadmap

### Positive

The promotion-readiness question is correctly positioned on the Phase E line. It strengthens the analyzer-v2-as-brain direction because:

- if the helper is promotable, it moves capture runtime resolution out of host-local code and into analyzer-owned shared substrate
- the `renderers-ui` package being inside analyzer-v2 means promotion would literally move code into the brain's jurisdiction

### Risk: moving Critic assumptions into the package

The distilled roadmap's anti-drift Rule 1 says: "Prefer upstream intelligence over downstream convenience." If the helper is promoted with its current `CaptureSelection` dependency intact, that would move a Critic-local assumption into the package rather than moving upstream intelligence down. The calibration must distinguish between these.

### Sequencing consideration

The distilled roadmap's Rule 4 says: "Prefer representative matrices over exhaustive workflow theater." This calibration slice is a matrix-broadening move (from Critic-local → package-available) rather than another narrow proof. That is strategically correct.

## Concrete Corrections or Reframing

### Correction 1 (Required): Fix the package-source factual error

Replace lines 108-111 with an honest statement:

> The source repository for `@the-syllabus/analysis-renderers` is `/home/evgeny/projects/analyzer-v2/renderers-ui/`. The Critic consumes it via a file-local tarball reference. So there is a real, known, analyzer-v2-owned destination for promoted code. The calibration should assess whether the helper's current shape is honest enough for that destination — not whether a destination exists at all.

### Correction 2 (Required): Add the two-architecture inspection to the calibration scope

The calibration must inspect not just the four Critic-local custom-renderer adopters, but also the existing capture architecture in the shared package. Specifically:

- How do `AccordionRenderer`, `CardGridRenderer`, `CardRenderer`, and the 8+ SubRenderers currently handle `config._onCapture`?
- Is the `currentRendererCapture` helper's strict `_firstHopAffordance` gate compatible with the package's existing looser gate?
- Should promotion replace the package's existing raw pattern, coexist alongside it, or provide a migration path?

### Correction 3 (Recommended): Reframe question 4

Question 4 ("Is there a real destination for promotion?") should be reframed from:

> This slice should not assume the answer is automatically `@the-syllabus/analysis-renderers`

to:

> The destination exists (`renderers-ui/` in analyzer-v2). The question is whether the helper's current shape, including its type dependencies and gating strictness, is compatible with the package's existing capture architecture — or whether promotion would create an incoherent two-tier capture model inside the same package.

### Correction 4 (Recommended): Add a sixth calibration question

Add:

> 6. If promoted, should the helper replace or supplement the package's existing raw `config._onCapture` pattern in generic renderers?

This question matters because the answer determines whether promotion is a ~20-line file move or a package-wide refactor. The calibration should size this honestly.

### Correction 5 (Minor): The "four adopters" framing understates the evidence base

The memo counts four Critic-local custom renderers. But the shared package already has 10+ renderers with capture code. If the calibration considers both, the total adopter base is ~14 renderers. The memo should be honest about both populations.

## Summary

The memo asks the right question at the right time. Its calibration-first posture prevents premature extraction. Its negative scope is well-defined. The five questions it proposes to answer are mostly sound.

But it contains one factual error (the package source is known and available in analyzer-v2) and omits a material architectural consideration (the shared package already has its own distinct capture architecture that the calibration must account for). These corrections change the calibration's starting position but do not change its fundamental shape. With corrections, this is executable and strategically valuable.
