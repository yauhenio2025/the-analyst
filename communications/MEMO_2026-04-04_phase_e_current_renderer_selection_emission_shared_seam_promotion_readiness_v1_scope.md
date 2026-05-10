# Memo: Phase E Current-Renderer Selection Emission Shared-Seam Promotion Readiness V1 Scope

Subtitle: One bounded calibration slice should decide whether the now-four-adopter Critic-local `currentRendererCapture` seam is honest enough for promotion beyond `the-critic`, or whether local ownership remains the right ceiling

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
Most Recent Code Completion:
- `communications/MEMO_2026-04-04_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_completion.md`
Relevant Prior Completions:
- `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`
Earlier Generalization Context:
- `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`
- `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Define the next honest question after the last materially broader current non-AOI renderer outlier is closed.

That question is no longer:

- can one more current renderer adopt `currentRendererCapture`

That is now complete.

The new question is:

- should `currentRendererCapture` remain a Critic-local helper
- or is the now-four-adopter seam honest enough for bounded promotion beyond `the-critic`

This is still a Phase E question because it is still about generality proof and host-thinning evidence.
But it should be treated as a promotion-readiness calibration step, not as an automatic shared-package extraction claim.

## Why This Is The Right Next Step

The evidence base changed materially on 2026-04-04.

The helper seam is no longer adopted by only three renderers.
It now spans:

- `AoiSinFindingsRenderer`
- `AoiThemeFindingsMiniCardList`
- `SynthesisRenderer`
- `IdeaEvolutionRenderer`

That means the current seam now covers:

- AOI pure findings
- AOI mixed nested findings
- non-AOI section capture
- non-AOI idea-card capture

It also now spans two workflow families and two capture-depth shapes:

- `L1_section`
- `L2_element`

So the next honest variable is no longer renderer-family breadth inside Critic.
The next variable is ownership and promotion:

- does this seam deserve broader ownership
- or is it still only a local host convenience

The strongest likely outcome should be treated as open, not assumed.
The current code suggests the most defensible forecast may be:

- ready only for a narrower extracted shell

rather than:

- promote `currentRendererCapture` unchanged

## Current State

The current Critic-local helper lives at:

- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`

The current helper is intentionally narrow:

- runtime resolution
- shared selection-shell assembly
- configurable `requireWorkflowKey`
- configurable `requireJobId`

It does **not** unify:

- `entity_id`
- preview text
- `parent_context`
- `genealogy_job_id`
- specialization or nested-handle gating
- destination semantics

One important reality must be named explicitly:

- the helper currently imports the Critic-local `CaptureSelection` type
- its runtime callback shape is also typed in Critic-local terms

So promotion beyond the host is not just a question of “copying the file somewhere else.”
There is real coupling to inspect first.

One second reality also matters:

- the shared renderer package source is already present in the active workspace at:
  - `/home/evgeny/projects/analyzer-v2/renderers-ui`
- Critic already consumes that package from a local analyzer-v2-owned tarball reference in:
  - `/home/evgeny/projects/the-critic/webapp/package.json`

So the destination for any promotion is real and already analyzer-v2-owned.
The question is therefore not:

- does a destination exist at all

It is:

- does the current helper shape fit that existing shared package honestly

One third reality must also be named:

- the shared package already contains its own generic capture assembly architecture
- that package-side architecture currently uses raw `config._onCapture` plus `Record<string, unknown>` selection payloads in generic renderers and sub-renderers

So promotion-readiness must inspect two existing architectures, not one:

1. the Critic-local `currentRendererCapture` seam and its four adopters
2. the shared-package raw capture assembly paths already living in `renderers-ui`

## What This Slice Should Answer

This slice should answer five bounded questions.

### 1. Is the seam materially stable across the four adopters?

Specifically:

- do the current two helper options remain sufficient:
  - `requireWorkflowKey`
  - `requireJobId`
- or would broader promotion immediately force new renderer-specific flags and branches

If new option flags or renderer-specific conditionals would be required just to keep current behavior, promotion is probably premature.

### 2. What is truly shared versus still renderer-local?

This slice should produce a clean separation between:

- genuinely shared runtime-resolution and selection-shell fields
- renderer-local identity rules
- renderer-local preview generation
- renderer-local coverage and gating
- renderer-local destination compatibility fields

### 3. Is the Critic-local type coupling still acceptable for promotion?

This slice must inspect whether a shared seam can exist honestly while the helper currently depends on:

- Critic-local `CaptureSelection`
- Critic-local `onCapture` callback shape

The calibration should name this precisely:

- the coupling is real
- but the shared package already uses a different solution:
  - `Record<string, unknown>`

So the question is not only whether the coupling exists.
It is also whether a promoted seam should:

- stay typed through a smaller package-owned base contract
- become package-generic through a looser `Record<string, unknown>` shape
- or remain local because either move would be dishonest right now

If that coupling cannot be removed or redefined without widening semantics or inventing a fake package-generic type, the honest result may be:

- keep the helper local

### 4. Is there a real destination for promotion?

The destination exists:

- `@the-syllabus/analysis-renderers`
- source tree:
  - `/home/evgeny/projects/analyzer-v2/renderers-ui`

So this slice should test not destination existence but destination fit:

- is the current helper shape actually compatible with the package's existing capture architecture
- or would promotion create an incoherent two-tier capture model inside the same package

### 5. What verdict should the roadmap take?

The slice should end with one explicit readiness verdict:

- promotion-ready
- not ready; keep Critic-local
- ready only for a narrower extracted shell than the current helper

### 6. If promoted, should it replace or supplement the package's existing raw capture pattern?

This slice should answer explicitly whether a promoted seam would:

- replace the existing package-side raw `config._onCapture` capture builders
- supplement them as a second stricter path
- or remain separate because convergence would currently be dishonest

## Proposed Implementation Boundary

This should be a bounded calibration / readiness slice first, not an immediate shared-package refactor.

The slice should:

- inspect the helper and its four adopters directly
- inspect the shared renderer package source and its existing generic capture assembly paths
- define the smallest honest promoted API if one exists
- stop short of package code movement if the promotion case is not clean

The slice should **not**:

- move code into a shared package yet
- redesign `CaptureSelection`
- invent host-neutral identity semantics
- widen analyzer semantics
- add backend or persistence changes
- add destination-policy law
- claim generic renderer-package capture law

## Proof Inputs

The calibration should inspect the following code directly:

- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.test.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/package.json`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/package.json`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardRenderer.tsx`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardGridRenderer.tsx`
- `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx`

The calibration should also inspect the recent documentary context:

- `communications/MEMO_2026-04-04_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`
- the current roadmap stack

## Acceptance Criteria

This slice is successful only if it ends with an honest, code-backed answer to all of these:

1. Is promotion beyond Critic-local ownership actually warranted now?
2. If yes, what exact API is promotable without new semantic branches?
3. If no, what exact coupling or divergence still blocks promotion?
4. Is the current helper the right ceiling for now, or is a narrower extracted shell the better answer?
5. Does the answer strengthen host-thinning evidence rather than just moving local complexity around?
6. If promotion is attempted later, should it replace or supplement the package's existing raw capture pattern?

## Verification Standard

For this calibration slice, the key standard is code-backed reasoning rather than implementation volume.

If the slice later turns into an actual code move, the acceptance bar for that later extraction should replay the already-proved surface set:

- `currentRendererCapture.test.ts`
- `AoiSinFindingsRenderer.test.tsx`
- `AoiThemeFindingsMiniCardList.test.tsx`
- `SynthesisRenderer.test.tsx`
- `IdeaEvolutionRenderer.test.tsx`
- `tests/aoi-v2-sin-capture.spec.ts`
- `tests/aoi-v2-theme-capture.spec.ts`
- `tests/genealogy-v2-portrait-capture.spec.ts`
- `tests/genealogy-v2-idea-evolution-capture.spec.ts`

But those reruns are not themselves the purpose of this readiness memo.

## What This Slice Is Not

This is not:

- immediate shared-package extraction
- generic renderer-package capture law
- a new host consumer proof
- a new analyzer-side semantics slice
- genealogy read-side truth surfacing
- destination lifecycle or mutation taxonomy work

## Assumptions And Defaults

- The four-adopter current helper matrix is now complete enough that promotion-readiness is the honest next variable.
- The strongest honest outcome may still be:
  - keep the helper local
- A narrower promoted shell may be more honest than promoting the entire current helper unchanged.
- The existing shared-package raw capture architecture is part of the proof surface and cannot be ignored.
- If the calibration finds that shared ownership would merely move Critic-local `CaptureSelection` assumptions into a package, the correct result is to stop and say so.
