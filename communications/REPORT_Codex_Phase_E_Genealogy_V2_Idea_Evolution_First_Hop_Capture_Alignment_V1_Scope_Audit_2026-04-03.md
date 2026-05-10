# Report: Phase E Genealogy V2 Idea Evolution First-Hop Capture Alignment V1 Scope Audit

Date: 2026-04-03

## Verdict

`reject`

The memo is right about the current host-local drift inside `IdeaEvolutionRenderer`, but wrong about the most important implementation precondition.

As written, this is **not** a host-only slice that can simply reuse the landed current-renderer helper plus generic first-hop capturability:

- `currentRendererCapture.ts` hard-requires `_firstHopAffordance?.capturable === true` before it returns runtime truth (`/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:26-63`)
- `V2TabContent` only threads whatever `payload.first_hop_affordance` the analyzer emitted (`/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:588-597`)
- analyzer-v2 only emits `first_hop_affordance` for migrated analytical leaf families, and `genealogy_idea_evolution` is still declared on `engine_key = "concept_synthesis"` (`src/presenter/first_hop_affordance.py:20-60`, `src/views/definitions/genealogy_idea_evolution.json:15-21`)

So the memo's proposed runtime gate would currently hide all capture buttons on this surface unless one of these happens first:

- analyzer-v2 broadens first-hop affordance eligibility to cover this view
- the helper grows a renderer-specific exception
- `IdeaEvolutionRenderer` bypasses the helper's gate

Only the first option is consistent with the stated analyzer-v2-as-brain direction and the memo's own decision rule.

## The Memo's Strongest Code-Backed Points

### 1. The current host gap is described accurately

The memo is correct that `IdeaEvolutionRenderer` is still on a host-local capture path.

- local gate is still just `captureMode && onCapture` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:380-386`, `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:555-556`)
- `source_type` is still hardcoded to `'genealogy'` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:568`)
- title is still renderer-local composition from `captureViewKey || 'Ideas'` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:567`)
- `source_workflow_key` is not emitted at all (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:560-570`)
- `entity_id` is not emitted at all (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:560-570`)

That part of the memo is solid.

### 2. Capture coverage is already narrow and the memo is right to keep it narrow

The only live capture control on this surface is the pin control in the idea-card footer.

- there is no comparable control in the hero / narrative structure block (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:441-480`)
- there is no capture control in the expanded timeline, indirect-enabler, or cross-cutting detail areas
- the existing control lives only inside each idea card footer (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:539-572`)

So "keep capture limited to existing idea-card buttons only" is the right scope boundary.

### 3. Reusing `currentRendererCapture.ts` is the right host seam if upstream truth exists

The landed helper is deliberately narrow:

- it resolves only shared runtime truth (`/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:26-63`)
- it builds only the shared selection shell (`/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:73-85`)
- it does not try to absorb renderer-local preview text, item payload shape, or identity modeling

That shape is already broad enough to cover:

- section-level genealogy capture in `SynthesisRenderer` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:62-114`)
- nested finding cards in `AoiThemeFindingsMiniCardList` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.tsx:47-139`)
- AOI finding cards with stronger local gating in `AoiSinFindingsRenderer` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:90-203`)

So the helper is not the problem. The missing upstream affordance on this specific view is the problem.

### 4. `requireWorkflowKey: true` and `requireJobId: true` are the right requirements if this surface is brought onto the helper honestly

Those requirements fit the actual downstream capture pipeline.

- `source_workflow_key` should be present if the selection is meant to be more truthful than the current local payload (`/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:109-115`)
- `genealogy_job_id` should also be present, because `CaptureContext` otherwise falls back genealogy captures to `entity_id` (`/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:97-113`)

That fallback matters here:

- if this renderer starts emitting `entity_id = idea.idea_id` without also requiring `_captureJobId`, the submission path could incorrectly treat an idea id as a genealogy job id

So the requirement pair is sound. It is just not enough on its own.

## The Memo's Weakest Or Overstated Assumptions

### 1. The memo's central "host-only" premise is overstated

The memo assumes `genealogy_idea_evolution` already has the same analyzer-owned generic first-hop truth that `genealogy_portrait` had.
The code does not support that.

- analyzer affordance emission is limited to migrated analytical leaf families (`src/presenter/first_hop_affordance.py:43-60`)
- `genealogy_idea_evolution` is still a `concept_synthesis` view, not one of the migrated family keys (`src/views/definitions/genealogy_idea_evolution.json:15-21`)

That means the memo's proposed gate on `_firstHopAffordance?.capturable === true` is not merely "one more helper adoption detail."
It is a blocking upstream dependency.

### 2. "Smallest honest next bounded step" is not true as written

After the current-renderer helper landed, the next honest gap is **not** yet "host-only idea evolution alignment."

There is one smaller precondition first:

- make `genealogy_idea_evolution` actually receive analyzer first-hop affordance truth

Without that, the slice either stops being host-only or stops being an analyzer-v2-as-brain proof.

### 3. `entity_id = idea.idea_id` is only honest under a very narrow reading

This is acceptable only if the memo states clearly that the claim is run-local / renderer-local identity, not canonical identity.

Why:

- analyzer genealogy pass 1 treats `idea_id` as a cross-pass identifier inside the genealogy pipeline (`src/engines/definitions/genealogy_pass1_idea_extraction.json:147-154`)
- but the newer extraction contract for idea evolution already allows a different shape, "snake_case identifier" (`src/transformations/definitions/idea_evolution_extraction.json:16-24`)
- the current renderer test fixture also uses that drifted snake_case style (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.test.tsx:10-40`)

So `idea.idea_id` is good enough for emitted item identity on this rendered surface.
It is not good enough to imply solved non-AOI canonical identity semantics.

### 4. The test plan is premature on the positive path

The memo asks for a positive live browser proof after helper adoption.
That only makes sense if the analyzer first-hop field is actually present on the live page.

Under the current analyzer code, helper adoption would remove the existing buttons rather than prove them.

## Factual Discrepancies I Found

### 1. The biggest discrepancy: `genealogy_idea_evolution` is not first-hop-affordance eligible today

This is the main blocker.

- `first_hop_affordance` is emitted only for migrated analytical leaf payloads (`src/presenter/first_hop_affordance.py:43-60`)
- `genealogy_idea_evolution` is backed by `engine_key = "concept_synthesis"` (`src/views/definitions/genealogy_idea_evolution.json:15-21`)
- `concept_synthesis` is not in `MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS` (`src/presenter/first_hop_affordance.py:20-35`)

So the memo's proposed use of `resolveCurrentRendererCaptureRuntime(...)` with first-hop gating cannot work on the live view as claimed.

### 2. The memo's description of the current host-local gap is otherwise mostly accurate

I did **not** find a major contradiction in these narrower claims:

- local `captureMode && onCapture`
- hardcoded `source_type`
- hardcoded title composition
- missing `source_workflow_key`
- missing `entity_id`

Those are all real.

### 3. The memo should be more explicit that helper reuse would be correct only after the affordance gap is fixed

If the memo said:

- first land a tiny analyzer-side affordance eligibility slice
- then align `IdeaEvolutionRenderer` to the helper

it would be defensible.

As written, it skips that prerequisite.

## What This Would Change For The Larger Roadmap

The roadmap direction is still broadly right:

- `genealogy_idea_evolution` is the last materially broader current non-AOI renderer outside the shared helper seam

But the roadmap sequencing in the recent memos is slightly off.

The honest statement now is:

- the next important renderer-family proof is still `genealogy_idea_evolution`
- but the next **code** move cannot honestly be host-only helper adoption unless analyzer-v2 first emits affordance truth on that view

That changes the analyzer-v2-as-brain interpretation in one specific way:

- a host-only `IdeaEvolutionRenderer` slice would no longer prove "the host consumed analyzer-owned generic first-hop truth" unless analyzer-v2 first makes that truth available
- otherwise the host would either be preserving a local exception path or forcing a fake helper exception

So the roadmap should insert one prerequisite calibration step before claiming this is the next bounded host-only proof.

## The Most Defensible Next Move After This Memo

The most defensible next move is:

1. a **small analyzer-side affordance eligibility slice** for `genealogy_idea_evolution`
2. then the bounded host-side `IdeaEvolutionRenderer` helper adoption slice

The first slice should be extremely narrow:

- decide whether `concept_synthesis` on `genealogy_idea_evolution` is now an approved analytical leaf for first-hop affordance
- if yes, extend the migrated/eligible family logic just enough for this view
- add focused analyzer tests proving `first_hop_affordance` now appears on this view and does not broaden more than intended

Only after that should the host slice land:

- reuse `resolveCurrentRendererCaptureRuntime(...)`
- reuse `buildCurrentRendererCaptureSelection(...)`
- keep capture coverage limited to existing idea-card buttons
- require both `_workflowKey` and `_captureJobId`
- emit `entity_id = idea.idea_id` with explicit run-local identity language
- add the renderer/unit/browser proof the memo already describes

If the program is not willing to broaden analyzer affordance eligibility for `concept_synthesis`, then the honest next move is not this memo at all.
It is a revised scope memo that explicitly says `genealogy_idea_evolution` remains outside the generic first-hop proof line for now and only a narrower provenance/helper cleanup is in scope.
