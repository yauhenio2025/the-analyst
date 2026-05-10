# Report: Phase 2 Consumer Contract Scope Audit

Date: 2026-03-19

## Findings

1. High: the duplicated bounded-v2 lifecycle logic is already large enough to justify extraction now, but the reusable seam is narrower than the memo currently states.

The common restore-first block is not incidental duplication. `AnalysisWorkspacePage` carries a 274-line run/result/restore/poll block at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:458`, `AoiV2ThematicPanel` carries a 357-line variant at `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:285`, and `GenealogyPage` carries a 292-line variant at `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:701`. The duplicated pieces are the exact ones the memo named: analyzer-v2 run/result fetches, saved-result restore, background freshness check, refresh-presentation, local snapshot fallback, and transition polling.

This is substantial enough to justify extraction now. The code is already paying the usual copy-paste tax: slightly different error behavior, slightly different cache behavior, slightly different completion follow-up, and page-local state mutations mixed directly into the shared restore decision tree.

2. High: `boundedV2Client.ts` should be limited to transport and contract parsing. The memo overstates what belongs there if it makes start/cancel/resume/import part of the required minimum.

The analyzer-v2-facing calls are stable and clearly shared:

- run detail fetch at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:468`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:295`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:711`
- result manifest/presentation/refresh fetches at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:458`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:497`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:541`
- discovery calls already repeated in page code at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:356`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:432`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:528`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:596`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:675`
- the shared manifest/run helpers are already centralized at `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:39`, `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:89`, `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:120`, `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:138`

By contrast, the host-side start paths are not one contract:

- generic workspace start: `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:762`
- AOI start: `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:721`
- genealogy start: `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1048`

Those payloads and endpoints are materially different. AOI uses thinker-scoped launch routes and thinker identity. Genealogy carries mode, selected works, optional target ideas, model overrides, and reuse-plan controls. The same problem exists for import and local result detail routes:

- generic workspace import/local detail: `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:572`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:864`
- genealogy import/local detail: `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:816`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1126`

Recommended boundary for `boundedV2Client.ts`:

- analyzer-v2 run discovery/detail wrappers
- analyzer-v2 result discovery/manifest/presentation/refresh wrappers
- a small Critic cache wrapper
- consistent `consumer_key` handling
- transport-level error normalization
- reuse of `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts` types instead of redefining them

Do not make generic start/cancel/resume/import wrappers part of the must-have Phase 2 minimum. Those can stay page-local for now, or become optional thin host-route helpers later.

3. High: `useBoundedV2Workspace.ts` should own the restore-first decision tree and polling transitions, but it should not own saved-result discovery, page hydration, tabs, or workflow-specific fallback state.

The reusable logic is the restore-first state machine:

- compare cached freshness before doing any destructive refresh at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:496`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:322`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:738`
- prefer upstream presentation when restorable, otherwise keep snapshot and set notice at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:513`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:341`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:757`
- fall back from upstream saved result to Critic-local saved result at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:632`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:462`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:889`
- continue polling after run completion while result restoration is still transitioning, using `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:120` and each page’s `shouldPollJob` wrapper at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:151`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:113`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:129`

The non-reusable parts are still real:

- generic workspace URL-backed tabs and deep-link handling at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:203`
- AOI tab selection and top-level view defaults at `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:124`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:196`
- genealogy URL tabs plus legacy/prose fallback state at `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:473`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:530`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:867`
- page-specific saved-result row shaping at `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:381`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:555`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:621`

Recommended boundary for `useBoundedV2Workspace.ts`:

- restore a selected saved result via upstream-first, local-snapshot-second logic
- background freshness refresh for a cached presentation
- manual refresh for a current presentation
- run-status polling through the completed/preparing/restorable transition
- notice selection through `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:138`

Keep page-local:

- saved-results list discovery/merge rules
- local result-detail fetch shape parsing
- active-tab state and default-tab selection
- view lazy-loading
- launch payload creation
- import/preview UX
- genealogy prose fallback and `viewingResult`
- AOI thinker filtering and AOI-specific saved-results refresh behavior

4. Medium: refresh/cache behavior is under-specified and is an implementation trap.

Current code does not call `cache-v2` inside `refreshStoredV2Presentation` after replacing a snapshot with a fresher server presentation. That is true in the generic workspace, AOI, and genealogy paths:

- refresh path without cache call: `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:486`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:312`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:728`
- cache happens elsewhere, mainly on direct upstream restore/poll/import paths: `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:603`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:649`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:710`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:443`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:479`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:617`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:850`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:906`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:969`

Phase 2 needs an explicit call on whether to preserve that behavior or tighten it. If this is silently changed during extraction, restore behavior will look "mostly the same" in-session while persisted snapshots evolve differently.

5. Medium: polling transitions are easy to regress if the hook is simplified too aggressively.

The pages are not polling only for active jobs. They are also polling for the post-completion transition where analyzer-v2 is done executing but presentation restore is still preparing:

- `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:120`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:151`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:113`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:129`

If `useBoundedV2Workspace.ts` reduces this to `pending || running`, completed runs with `presentation_status === "running"` or `result_state === "preparing"` will stop resolving into a presentation.

6. Medium: AOI-specific state is a real boundary and should not be smuggled into the generic hook.

AOI is not only another renderer. It filters both discovery and local saved-result data by thinker identity:

- thinker matcher: `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:137`
- result discovery filter: `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:528`
- local filtering and merged row shaping: `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:545`

It also refreshes the saved-results list after completion and after manual refresh:

- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:629`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:802`

That behavior belongs to the AOI host surface, not the generic bounded-v2 hook.

7. Medium: `GenealogyPage` should stay out of the first adoption set.

`GenealogyPage` is not just "another consumer". It is a mixed-mode page with:

- legacy/prose fallback state at `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:473`
- prose metadata injection when v2 is unavailable at `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:867`
- a much heavier launch payload and reuse-plan logic at `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1033`
- genealogy-specific routes for start/cancel/import at `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1079`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1112`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1133`
- hardcoded tab selection for restored/imported results at `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1121`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1150`

It is a good regression reference and likely a good second-wave adopter after the contract stabilizes on `AnalysisWorkspacePage` and `AoiV2ThematicPanel`. Pulling it into the first edit set would blur Deliverable B into a broader genealogy modernization pass.

8. Medium: the verification surface is thinner than the memo assumes, so Phase 2 should budget new tests around the extracted hook/client.

Current direct frontend coverage is minimal:

- freshness helper tests exist at `/home/evgeny/projects/the-critic/webapp/src/utils/presentationFreshness.test.ts:1`
- no direct tests exist for `resultContract.ts`, `AnalysisWorkspacePage`, `GenealogyPage`, or `AoiV2ThematicPanel` restore orchestration

I ran:

- `CI=true npm test -- --watch=false --runTestsByPath src/utils/presentationFreshness.test.ts` in `the-critic/webapp`: passed
- `pytest -q tests/test_aoi_v2_routes.py -k 'get_analysis_job_reads_v2_detail_from_durable_reference_without_in_memory_authority or cancel_analysis_job_uses_durable_reference_without_in_memory_authority or resume_analysis_job_preserves_imported_local_alias_without_mapping'` in `the-critic`: 3 passed

Those passing route tests do support the memo’s assumption that the underlying durable-reference/run-detail contract is already present on the host side:

- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:205`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:361`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py:396`

But they do not cover the frontend restore-first decision tree that Phase 2 will actually move.

## Implementability Without Analyzer-v2 Changes

Yes, this is implementable without analyzer-v2 changes if the scope is tightened to the real duplication seam.

Reason:

- the frontend already consumes the needed analyzer-v2 run/result endpoints from all three surfaces
- the required manifest/run fields already exist in `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:39` and `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:89`
- freshness metadata is already available and exercised through `/home/evgeny/projects/the-critic/webapp/src/utils/presentationFreshness.ts:1`
- the backend durable-reference path is already covered by the passing route tests above

The blockers are not upstream analyzer-v2 contract gaps. The risks are entirely in how much host-side behavior gets pulled into the first abstraction.

## Recommended Scope Adjustment

Phase 2 should still use the proving pair named in the memo:

- `AnalysisWorkspacePage`
- `AoiV2ThematicPanel`

But the contract boundary should be tightened:

- `boundedV2Client.ts`: analyzer-v2 transport wrappers, discovery wrappers, result-manifest/presentation/refresh wrappers, optional Critic cache wrapper, shared error normalization
- `useBoundedV2Workspace.ts`: restore-first orchestration, transition polling, refresh logic, notice selection, and callback-based integration points for page-owned state
- page-local: launch/cancel/resume/import UX, saved-results list merge rules, local result-detail parsing, tab state, view lazy-loading, AOI thinker semantics, genealogy prose fallback

## Adoption Call

`GenealogyPage` should stay out of the first adoption set.

Use it as a comparison and regression surface during the first extraction. Only pull it in after the shared contract is proven stable in `AnalysisWorkspacePage` and `AoiV2ThematicPanel`.

## Verdict

Proceed with scope changes.
