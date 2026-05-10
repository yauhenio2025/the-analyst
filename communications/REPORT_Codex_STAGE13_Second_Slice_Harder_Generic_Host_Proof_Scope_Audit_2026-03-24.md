Approve

# Stage 13 Second-Slice Harder Generic Host Proof Scope Audit

Audited memo:
- `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`

## Findings

1. High: the memo is right that Stage 13 still has a real second slice before Stage 14.

The current codebase still does not satisfy the roadmap exit bar for Stage 13, which is `second consumer or generic host proof without rebuilding intelligence locally` in `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1061-1063`.

That remaining gap is not hypothetical. The transient host path is still deliberately isolated from the shared result-backed runtime:
- dedicated transient route: `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:256-261`
- dedicated transient client: `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts:121-178`
- dedicated transient page: `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:202-287`
- explicit isolation test forbidding transient files from importing `useBoundedV2Workspace` or `boundedV2Client`: `/home/evgeny/projects/the-critic/webapp/src/transientComposeIsolation.test.ts:4-29`

The first-slice proof record also says this directly rather than implying closure:
- `communications/PROOF_2026-03-24_stage13_minimal_generic_host_contract.md:48-61`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1233-1234`

So the memo is correct on the main sequencing claim: there is still meaningful Stage 13 work, and it is still more honest than jumping to Stage 14 lifecycle.

2. High: the cited host-surface-selection gap is real; the current contract is typed law plus readiness lookup, not a runtime surface resolver.

`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:267-309` defines `HOST_CONTRACT_V1_SURFACE_SELECTION_RULES`, but the app does not consume those rules to decide which host surface to run. The only live runtime use of the host contract inside the app is readiness-capability lookup:
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:107-112`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:158-162`

By contrast, the surface-selection rules are only exercised in the test/serialization path:
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.test.ts:70-81`

Actual host-surface choice still lives in page-local logic:
- generic workspace chooses behavior from URL/workflow/context in `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:190-195` and wires the shared workspace hook directly in `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:317-325`
- AOI transient launch decides readiness, warmup, and navigation locally in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:490-535`
- the transient page decides direct compose behavior locally in `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:202-287`

So the memo is accurate to say surface selection is still mostly documentary/page-local rather than executable law.

3. High: the first-slice proof is still weaker than the materially harder generic-host proof this memo proposes.

The first-slice proof established:
- typed Host Contract v1
- shared result-backed client and workspace hook
- bounded readiness adoption

That is what the saved proof artifacts claim:
- `communications/PROOF_2026-03-24_stage13_minimal_generic_host_contract.md:8-19`
- `communications/PROOF_stage13_shared_adapter_path_2026-03-24.md:8-31`

But it did not prove one contract-driven runtime across both result-backed and transient seams. The current code still shows:
- result-backed families centralized in `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:76-198`
- transient families centralized separately in `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts:121-178`
- analyzer-side transient compose still structurally bound to `the-critic` in `src/presenter/compose_from_intent.py:445-490`
- AOI source-backed launch still requiring host identity resolution plus host proxying in `/home/evgeny/projects/the-critic/api/server.py:18621-18705` and `/home/evgeny/projects/the-critic/api/server.py:20311-20365`

The current transient host itself still describes its role as a separate proof host rather than a generic workspace path:
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:298-301`

That makes the memo’s “harder proof” claim real rather than rhetorical.

4. Medium: the proposed next slice stays bounded if implemented literally; it does not quietly smuggle in lifecycle, second-consumer, or host-neutral compose work.

The roadmap already separates the two stages:
- Stage 13 exit bar: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1035-1063`
- Stage 14 lifecycle bar: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1065-1093`

The memo also matches current code truth by keeping AOI source-backed launch explicitly host-bounded rather than pretending it is consumer-neutral. That matches:
- host-contract ownership for `source_backed_transient_launch` in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:209-239`
- thinker/project-scoped identity resolution in `/home/evgeny/projects/the-critic/api/server.py:18621-18705`
- proxy forwarding to analyzer after host preparation in `/home/evgeny/projects/the-critic/api/server.py:20325-20340`

I do not see lifecycle, second-consumer, or `TRANSIENT_COMPOSE_CONSUMER_KEY` removal being smuggled into the proposed tranche. The only real scope risk is implementation drift: if the “surface resolver” expands beyond the current proof surfaces, it could become a disguised app/session framework.

5. Medium: the proof bar is strong enough to distinguish this slice from the first Stage 13 slice, but only if the implementation proves real runtime convergence rather than cosmetic wrapping.

The proposed bar is meaningfully stronger because it asks for:
- one shared contract-driven host runtime across one result-backed seam and one transient seam
- executable host-surface selection
- proof that analytical and renderer-law truth stays upstream

That is a genuine delta from the first slice, which only proved that result-backed seams mostly share a client/hook path and that bounded readiness adoption exists.

The important caveat is practical: the codebase could otherwise “pass” by adding a thin wrapper while leaving page-local branching intact. The current separation is deep enough that the second slice should only count if it changes actual call paths:
- transient route/client isolation is deliberate in `/home/evgeny/projects/the-critic/webapp/src/transientComposeIsolation.test.ts:12-29`
- compose endpoints stay separate public routes in `src/api/routes/presenter.py:380-430`

So the memo’s proof bar is adequate, but only if the saved evidence shows real runtime consolidation and not just renamed helper functions.

6. Low: the memo slightly understates how close the system already is to the narrower bespoke-UI vision, even though it is right that the thin-host proof is still partial.

The canonical roadmap already says the program is “in strong shape” against the narrower UI-composition vision:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:91-98`

That understatement matters because most of the remaining gap is no longer “can analyzer-v2 compose/render bespoke analytical UI?” Much of that downstream story is already real. The remaining problem is specifically:
- operational host-contract authority
- generic-host proof strength
- later lifecycle/governance decisions

At the same time, the narrower vision is not yet closed. The vision document still expects consumer apps to avoid domain-specific routes and workflow-specific pages:
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md:128-139`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md:276-288`

Current code still keeps dedicated AOI transient and AOI thematic surfaces:
- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:256-261`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:490-535`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:202-287`

So the memo slightly understates proximity to the narrow bespoke-UI vision, but it does not overstate Stage 13 closure.

## Open Questions / Residual Risks

- What is the smallest executable artifact for “host-surface selection law”? If it grows beyond the three current proof surfaces, the tranche will start drifting toward lifecycle or generic app-shell framework work.
- What concrete condition proves “one shared contract-driven host runtime”? The cleanest bar would be that transient launch/compose stops living behind the current isolation boundary in `/home/evgeny/projects/the-critic/webapp/src/transientComposeIsolation.test.ts:12-29`, rather than merely gaining another wrapper.
- How will the proof demonstrate that page code is no longer re-deriving analytical or renderer-law truth? That claim should be made testable, not left as prose.

## Verdict Rationale

Approve.

The memo matches live code truth, preserves the correct sequencing relative to Stage 14, and proposes a proof bar that is materially stronger than the first Stage 13 slice without quietly reopening lifecycle, consumer-neutrality, or second-consumer work.
