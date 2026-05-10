# Report: Phase E Current-Renderer Selection Emission Shared-Seam Promotion-Readiness V1 Scope Audit

Date: 2026-04-04
Reviewer: Codex
Scope Under Review:
- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_scope.md`

## Verdict

**Approve with corrections.**

The memo is asking the right next bounded Phase E question. The four-adopter question is closed in code, and the remaining honest variable is now ownership and promotion ceiling. But one premise is materially wrong: the active workspace does contain a first-class local source tree for `@the-syllabus/analysis-renderers` at `/home/evgeny/projects/analyzer-v2/renderers-ui`, not just the installed copy under `the-critic/webapp/node_modules`. That correction matters because the real readiness question is less "is there any visible destination?" and more "does the current Critic-local helper fit the already-existing shared package capture substrate without importing Critic-local semantics into it?"

Focused verification I ran before writing this audit:

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/lib/currentRendererCapture.test.ts src/components/renderers/AoiSinFindingsRenderer.test.tsx src/components/renderers/AoiThemeFindingsMiniCardList.test.tsx src/components/renderers/SynthesisRenderer.test.tsx src/components/renderers/IdeaEvolutionRenderer.test.tsx src/components/V2TabContent.test.tsx src/contexts/CaptureContext.test.tsx`
- Result: 7 suites passed, 45 tests passed
- Existing repo note still present: Jest open-handle warning after completion

## The Memo's Strongest Code-Backed Points

- The seam is real and exactly four-adopter wide. `currentRendererCapture.ts` is used only by `AoiSinFindingsRenderer`, `AoiThemeFindingsMiniCardList`, `SynthesisRenderer`, and `IdeaEvolutionRenderer`, which matches the memo's matrix exactly.
- The helper is genuinely narrow. In `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:26-85` it only:
  - resolves runtime from already-threaded config
  - fail-closes on missing capture mode / handler / view key / view name / source type / `first_hop_affordance.capturable`
  - optionally requires workflow key and/or job id
  - builds only the shared selection shell (`source_type`, `source_view_key`, `context_title`, `source_workflow_key`)
- The two current options are still honest for the current four adopters. The live matrix is:
  - `AoiSinFindingsRenderer`: `requireWorkflowKey: false`
  - `AoiThemeFindingsMiniCardList`: `requireWorkflowKey: true`
  - `SynthesisRenderer`: `requireWorkflowKey: true`, `requireJobId: true`
  - `IdeaEvolutionRenderer`: `requireWorkflowKey: true`, `requireJobId: true`
  I found no evidence in code or tests that the current four adopters need a third helper option.
- The memo is right that the divergences still live outside the helper:
  - `AoiSinFindingsRenderer` keeps specialized-family gating and persisted-status readback local in `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:51-57` and `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:94-113`
  - `AoiThemeFindingsMiniCardList` keeps nested `finding_id` gating, fallback-to-package rendering, and parent-context assembly local in `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.tsx:47-66` and `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.tsx:129-145`
  - `SynthesisRenderer` keeps section whitelist, genealogy compatibility fields, and run-level entity fallback local in `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:99-114`
  - `IdeaEvolutionRenderer` keeps idea-card-only coverage, item-level `entity_id = idea.idea_id`, and a local stricter runtime wrapper in `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:375-394` and `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:577-592`
- The memo is also right to treat this as a readiness calibration slice instead of immediate extraction. The helper still depends on Critic-threaded private config from `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:588-597`, and the actual selection contract is still Critic-local in `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:17-35`.

## The Memo's Weakest Or Overstated Assumptions

- The memo understates how concrete the shared package destination already is. There is a local package source tree at `/home/evgeny/projects/analyzer-v2/renderers-ui/package.json:2-3`, with the same package identity as the installed dependency. The issue is not lack of visible source.
- The memo understates how much existing package capture law already exists independently of `currentRendererCapture`. In `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:35-36` and `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx:108-114`, the package already uses generic `Record<string, unknown>` selection callbacks and reads capture config directly. Promotion therefore means reconciling with an existing package substrate, not just relocating one helper file.
- The Critic-local `CaptureSelection` import is not just a small coupling note. `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:1-5` makes the helper's callback and `sourceType` unions depend directly on Critic context types, while the shared package explicitly avoids such a type import and uses `Record<string, unknown>` instead in `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:35-36`. That makes the current helper shape not promotion-ready unchanged.
- Promotion beyond Critic would not only test the four adopters. The shared package's current capture builders do not consume `_captureViewName`, do not gate on `_firstHopAffordance`, and still compose titles from `captureViewKey` with `>` chains, for example in:
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx:675-689`
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx:364-380`
  So "promotion" is not merely ownership transfer. It is an API-fit question against a divergent existing package capture convention.

## Factual Discrepancies

- The memo says the only clearly visible shared-renderer package boundary in the workspace is the installed copy under `the-critic/webapp/node_modules`, and that no clearly established first-class source repo is visible. That is false. `/home/evgeny/projects/analyzer-v2/renderers-ui/package.json:2-3` is a first-class local source tree for `@the-syllabus/analysis-renderers`.
- Because of that, "source-ownership uncertainty" is weaker than the memo claims, but "promotion-fit uncertainty" is stronger than the memo claims. The visible source exists; it simply does not yet match the helper's current semantics.

## What This Would Change For The Larger Roadmap

- The memo still passes the roadmap filter. It is asking whether current-app work now encodes reusable host/runtime law or should stop at the local ceiling. That is legitimate Phase E work under the anti-drift rules.
- But a positive verdict on unchanged helper promotion would not, by itself, strengthen the analyzer-v2-as-brain claim very much. If the move merely lifts Critic-local `CaptureSelection`, Critic-local first-hop gating, and Critic-local workflow/job assumptions into the shared renderer package, that is code movement more than host-thinning.
- The roadmap implication should therefore be phrased more tightly:
  - this slice is valuable because it can identify the honest ceiling
  - the strongest honest outcome may be "keep local" or "extract a narrower shell"
  - that is still useful Phase E evidence because it prevents fake genericity
- In other words, this slice strengthens the roadmap most if it refuses over-promotion. That is aligned with:
  - "prefer upstream intelligence over downstream convenience"
  - "do not confuse bounded proof with generalized architecture"

## Most Defensible Next Move

- Keep this as a calibration slice, but correct the proof target. The comparison set should explicitly include the existing shared-package capture builders in `renderers-ui`, not just `package.json`.
- If forced to choose today among the memo's readiness outcomes, the most defensible forecast is:
  - **ready only for a narrower extracted shell**
  not:
  - promotion-ready unchanged
- The narrower shell, if it exists, should be package-neutral and avoid Critic-local `CaptureSelection` typing. Candidates would be small utilities around generic capture config reading and title/context composition. The following should stay local unless a separate contract is defined first:
  - Critic `CaptureSelection` typing
  - `_firstHopAffordance` fail-closed policy
  - `requireWorkflowKey` / `requireJobId` policy as current-renderer law
  - `genealogy_job_id` emission
  - renderer-specific identity, preview, status, and specialization logic
- If the next slice is implementation-oriented rather than purely documentary, the smallest honest move is not to promote `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts` unchanged. It is to first audit and compare these shared-package capture paths:
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/AccordionRenderer.tsx`
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardRenderer.tsx`
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/renderers/CardGridRenderer.tsx`
  - `/home/evgeny/projects/analyzer-v2/renderers-ui/src/sub-renderers/SubRenderers.tsx`
  Then decide whether the promotable unit is:
  - no shared extraction
  - a narrower generic capture utility
  - or, only after that, a broader shared seam

## Bottom Line

The memo is directionally correct about what question comes next. The seam is real, narrow, and four-adopter-wide. The memo is not yet precise enough about the actual shared-package landscape. After correcting that, the strongest code-backed conclusion is:

- the next slice should calibrate promotion readiness
- the current helper is not ready for shared-package promotion unchanged
- a narrower shell may be promotable
- and "keep it local" remains a fully respectable outcome if the calibration shows that shared ownership would mostly export Critic-local assumptions
