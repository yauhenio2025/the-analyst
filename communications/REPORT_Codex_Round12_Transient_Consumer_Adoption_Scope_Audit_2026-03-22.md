Approve after revision

# Round 12 Scope Audit

Perspective docs: no materially relevant recent Perspective docs were found for this analyzer-v2 round. The only local hit I found was `/home/evgeny/projects/visualizer/docs/STRATEGIC_AUDIT_CIA_PERSPECTIVE.md`, which is a December 17, 2025 Visualizer intelligence-tradecraft audit and does not materially inform AOI transient consumer adoption.

## Findings

1. `High`: The memo is correct that round 12 should not try to make the current workspace "job-optional"; it must explicitly define a separate frontend transient contract instead of trying to coerce the round-11 response into `PagePresentation`.
   - The backend route already returns a different contract: `TransientIntentPagePresentation` / `TransientIntentView`, with `workflow_key`, `consumer_key`, hashes, `resolver_version`, `style_school`, and `views`, but no `job_id` or `plan_id` (`src/presenter/schemas.py:631-676`).
   - The route implementation builds that non-job presentation directly and hashes it as its own contract (`src/presenter/compose_from_intent.py:740-770`).
   - Round 11 tests assert that `job_id` is absent from the returned presentation (`tests/test_compose_from_intent.py:159-183`).
   - By contrast, the-critic’s current shared presentation type requires `job_id` and `plan_id` at the type level (`/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:85-104`), and `useBoundedV2Workspace` is built entirely around job polling, restore, refresh, and cached result manifests (`/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:23-48`, `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:128-225`, `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:320-417`).
   - The scope memo should therefore say plainly: round 12 introduces a new frontend transient contract and does not widen `PagePresentation`.

2. `High`: The dedicated transient shell is the right boundary, but the memo over-specifies "one dedicated AOI transient page" as if route placement were the architecture. The architectural boundary is the shell and contract, not necessarily a brand-new permanent route.
   - The large vision says the consumer app should provide routing and a generic workspace, not accumulate new domain-specific pages (`communications/DYNAMIC_BESPOKE_APPS_VISION.md:128-139`).
   - The round-12 memo proposes a dedicated AOI route and page (`communications/MEMO_2026-03-22_round12_transient_consumer_adoption_scope.md:107-128`).
   - The-critic already has an AOI-specific host surface in `AnxietyOfInfluencePages.tsx`, with a dedicated thinker page and a `V2 Thematic` panel (`/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx:787-854`).
   - The repo also already has the generic job-backed workspace route at `/p/:projectId/analysis/:workflowKey` (`/home/evgeny/projects/the-critic/webapp/src/routes.tsx:253-257`).
   - Revision needed: say that shell isolation is mandatory, but route placement is an implementation choice. A dedicated page is acceptable as a proof host, but it should be described as a bounded host choice, not a new standing frontend doctrine.

3. `Medium-High`: The memo understates how much of the current frontend is job-bound, and it should block more than just "retrofitting `AnalysisWorkspacePage`."
   - `V2TabContent` is not merely "a bit job-aware"; it keys polish cache and section-polish cache by `presentation.job_id`, calls `/v1/presenter/polish` and `/v1/presenter/polish-section` with `job_id`, pulls capture status by `job_id`, threads `_jobId` / `_captureJobId` / `_captureEntityId`, and passes `jobId` straight into `ViewRenderer` (`/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:293-356`, `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:395-485`, `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:558-594`, `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:979-994`).
   - `AnalysisWorkspacePage` is built around run creation, cancel/resume, import, refresh, export, saved results, provenance, capture, and a two-row parent/child tab model (`/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:601-770`, `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:907-1129`).
   - Round 11 explicitly did not prove `PagePresentation` compatibility or child-view / tab layout (`communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md:240-248`).
   - The transient planner is explicitly flat: one top-level view per section, no parents, no children, no tabs (`src/presenter/compose_from_intent.py:297-307`).
   - Revision needed: the memo should explicitly block tab synthesis, single-view lazy loading by job ID, provenance, capture, polish, refresh, export, and saved-result restore from round 12 scope.

4. `Medium`: The memo is directionally right about `ViewRenderer`, but it understates how much of the AOI leaf renderer path is already transient-ready.
   - `ViewRenderer` only requires a `view`, `data`, and optionally `jobId`; it conditionally injects `_jobId` only when present, then resolves package defaults, explicit local overrides, sub-renderers, and prose fallback (`/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx:93-160`, `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx:165-250`).
   - The remaining top-level override seam in the-critic is genealogy-specific plus `nested_sections`; there is no AOI-specific view-key override (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts:18-25`).
   - The remaining sub-renderer overrides are compatibility aliases and `nested_sections`, not AOI-specific transient debt (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SubRenderers.tsx:19-24`).
   - Round 10 already proved the AOI generic workspace path uses shared package-backed renderer defaults rather than consumer-owned runtime registration (`communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md:17-30`, `communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md:60-107`).
   - Revision needed: the memo should force maximal reuse of `ViewRenderer` and current shared renderer resolution, and explicitly forbid new AOI-specific renderer overrides in round 12.

5. `Medium`: The memo is right to demand honest `400 / 409 / 502 / 503` behavior, but it should name the existing client-law mismatch as an explicit scope item.
   - The backend route already distinguishes those outcomes (`src/api/routes/presenter.py:367-394`), and round-11 tests cover the `502` / `503` mapping (`tests/test_compose_from_intent.py:376-439`).
   - The current bounded-v2 client path cannot preserve that contract cleanly. Its shared `parseJson()` helper throws generic `Error` instances and does not preserve structured status information (`/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:27-39`).
   - The rest of `boundedV2Client` is entirely framed as runs/results/by-job APIs (`/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:42-179`).
   - Revision needed: round 12 should define a dedicated transient client and typed error surface instead of piggybacking on the bounded-v2 run/result client.

6. `Medium`: AOI-only remains the right proof surface; the memo is correct to keep genealogy and broader widening blocked.
   - Round 9 enforcement was allowlisted to the AOI proof mode, with genealogy explicitly blocked (`communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md:19-31`, `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md:41-47`, `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md:107-115`).
   - Round 11 hard-validates AOI-only and `consumer_key = the-critic` in request validation (`src/presenter/compose_from_intent.py:217-225`).
   - Round 11 completion explicitly lists genealogy widening, tab layout, and persistence as not yet proved (`communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md:240-248`).
   - So the AOI-only proof surface is right; widening now would be scope fraud.

## Direct Answers

1. Does the roadmap really point to transient consumer adoption next?
   - Yes, with one qualification. The original round-8 roadmap pivoted toward renderer contracts, consumer consolidation, and bounded compose-from-intent (`communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:169-249`, `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:280-282`). Round 11 completion then made "adopt the transient contract in a real consumer surface" an explicit natural next question (`communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md:261-273`). So round 12 is not skipping a hidden unfinished platform-law seam. The unfinished seam is the transient consumer contract itself.

2. Is the dedicated transient shell the right architectural boundary?
   - Yes. Shell separation is the right boundary. Workspace unification is not.
   - But the memo should not hard-code "new dedicated AOI route" as the architectural truth. The shell boundary is essential; route placement is secondary.

3. Which parts of the-critic are closer to transient-ready than the memo admits, and which are more job-bound than the memo admits?
   - Closer than admitted: `ViewRenderer`, package-backed default renderer resolution, and the absence of AOI-specific renderer overrides (`/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx:102-160`, `/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts:18-25`).
   - More job-bound than admitted: `V2TabContent`, `AnalysisWorkspacePage`, `useBoundedV2Workspace`, and `boundedV2Client`, plus the compile-time `PagePresentation` type that spreads job semantics across the consumer (`/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:85-104`, `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:51-417`, `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:42-179`).

4. Is the proposed AOI-only proof surface the right one?
   - Yes. AOI is the only surface where round 9 renderer-law, round 10 consumer consolidation, and round 11 transient orchestration all line up.
   - The proof surface should stay flat and transient. It should not quietly grow tab planning, genealogy support, or persistence.

5. What exact assumptions should be forced into the scope memo before planning?
   - The frontend will introduce new transient TypeScript types for the compose-from-intent response; it will not widen `PagePresentation`.
   - The new shell will render `presentation.views` as a flat ordered list and will not synthesize tab trees.
   - The new shell may reuse `ViewRenderer` and current shared renderer resolution only; no new AOI-specific renderer overrides.
   - The new client will be dedicated to `/v1/presenter/compose-from-intent` and preserve `400 / 409 / 502 / 503` distinctly.
   - The proof host may be a dedicated AOI route or an isolated AOI page/tab host, but it may not inherit `AnalysisWorkspacePage` or `useBoundedV2Workspace`.
   - Proof inputs stay pinned to the saved round-11 dossier and comparison requests.

6. What should remain explicitly blocked?
   - Any attempt to make `AnalysisWorkspacePage`, `V2TabContent`, or `useBoundedV2Workspace` "dual mode."
   - Any synthetic `job_id` / `plan_id` placeholders.
   - Any use of run polling, result restore, export, provenance, capture, page polish, section polish, or refresh APIs on the transient path.
   - Any tab/child-view planning or lazy single-view fetches by job ID.
   - Any saved-result persistence, draft promotion, import-to-DB, or cache-warming work.
   - Any widening beyond AOI or any genealogy transient adoption.

## Recommended Memo Revisions Before Execution Planning

- Replace "one dedicated AOI transient page" with language that distinguishes the required shell boundary from optional route placement.
- Add an explicit sentence that round 12 introduces a separate transient consumer contract and does not make `PagePresentation` optional.
- Add an explicit prohibition on tabs, child-view planning, provenance, capture, polish, export, refresh, saved-result restore, and job-ID-based lazy loading.
- Add an explicit requirement for a dedicated transient client with typed `400 / 409 / 502 / 503` handling.
- Add an explicit reuse clause: `ViewRenderer` and existing shared renderer resolution are reused as-is; no new workflow-specific renderer logic is allowed.

## Bottom Line

The memo has the right next move and the right instinct about shell isolation. It needs revision because it currently treats route placement as architecture, does not force a separate frontend transient contract strongly enough, and does not block enough of the existing workspace law. Tighten those points and the round-12 scope is credible.
