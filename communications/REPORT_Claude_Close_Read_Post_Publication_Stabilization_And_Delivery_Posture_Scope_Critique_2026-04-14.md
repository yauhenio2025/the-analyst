# Critique Report: Close Read Post-Publication Stabilization And Delivery Posture Scope

Date: 2026-04-14
Reviewer: Claude (Opus 4.6)
Memo Under Review:
- `communications/MEMO_2026-04-14_close_read_post_publication_stabilization_and_delivery_posture_scope.md`

## Verdict: APPROVE WITH CORRECTIONS

The memo is structurally sound, strategically honest, and well-sequenced relative to the prior Close Read chain. It correctly identifies the next honest corridor as stabilization rather than expansion or extraction. Three corrections are needed before execution.

---

## Key Findings

### 1. The genealogy ERR_CONNECTION_REFUSED is likely cross-repo, not the-critic-local

**Finding**: Code-level investigation of the deployed genealogy runtime reveals the probable origin of the ERR_CONNECTION_REFUSED residual.

The deployed `closeReadGenealogyRuntime.ts` calls **both**:

- `API_BASE` (the-critic backend at `https://the-critic.onrender.com/api`) for local saved result snapshots
- `ANALYZER_V2_URL` (analyzer-v2 at `https://analyzer-v2.onrender.com`) via `dispatchAnalyzerDirectRequest` for upstream discovery and presentation fetch

The `discoverCloseReadGenealogySavedResults` function makes a parallel call to `discoverBoundedV2Results` which dispatches to analyzer-v2. On Render, `ERR_CONNECTION_REFUSED` is the specific error a browser emits when the TCP connection itself is rejected, which is consistent with Render service cold-start behavior.

**Impact on scope**: The memo treats this as a the-critic-local defect to investigate and fix in Phases 1 and 3. That framing is too narrow. Phase 1's reproduction may discover that the error is an analyzer-v2 availability seam, not a the-critic code defect. If so, the "fix" would be improving how the-critic handles transient analyzer-v2 unavailability (e.g., retry, graceful fallback, error suppression) rather than eliminating the error at its source.

This does not break the scope, but Phase 1 should be prepared for the possibility that the residual is cross-repo in origin even if the fix remains the-critic-local in implementation.

### 2. The public surface is confirmed real

**Live verification** (2026-04-14):

- Frontend host `https://the-critic-1.onrender.com`: serving, returns 200
- Current deployed bundle: `main.1d26cf69.js` (matches the April 13 completion evidence)
- Backend host `https://the-critic.onrender.com/api/health`: 200

All six admitted routes exist in the deployed `origin/master` routes file at `webapp/src/routes.tsx:261-292`:

- `/p/:projectId/close-read` -> `CloseReadLandingPage`
- `/p/:projectId/close-read/genealogy` -> `CloseReadPage`
- `/p/:projectId/close-read/aoi` -> `CloseReadAoiIndexPage`
- `/p/:projectId/close-read/aoi/:thinkerId` -> `CloseReadAoiThinkerPage`
- `/p/:projectId/close-read/concepts` -> `CloseReadConceptIndexPage`
- `/p/:projectId/close-read/concepts/:conceptSlug` -> `CloseReadConceptDetailPage`

All page components and supporting runtime modules exist in deployed source.

The memo's claim that "the public Close Read surface is already real and the next question is stabilization/posture rather than publication" is **confirmed by both live evidence and deployed source**.

### 3. Analyzer-v2 and analyzer-mgmt are correctly out of scope

**analyzer-v2**: Live and healthy (engines endpoint returns 200). The uncommitted local changes (new `/v1/results/*` and `/v1/runs/*` endpoints, analysis_products module) are development work, not deployed blockers. The deployed state on `origin/master` is stable and does not block Close Read stabilization.

**analyzer-mgmt**: The local checkout is extremely dirty (1,684-line job page deletion, 2,840 lines net deleted vs origin/master). However, the **deployed** state on `origin/master` (commit `0ce31a9` "Harden concept artifact operator state on job pages") is the April 13 normalization deploy and is stable. The local deletions appear to be uncommitted refactoring work that is irrelevant to the deployed product surface.

The scope memo's instruction to put both repos out of scope is correct. There is no deployed blocker in either repo that this tranche needs to address.

**One caveat**: If the ERR_CONNECTION_REFUSED investigation (Finding 1) reveals that the fix requires changing how the-critic calls analyzer-v2, the implementation should still keep that change local to the-critic (e.g., improving the fetch error handling or retry behavior). It should not become a reason to pull analyzer-v2 into scope.

### 4. The delivery-posture decision is framed honestly enough, with one soft weakness

The memo defaults to "stay on the current Critic host pair" and says extraction should only be escalated if "the stabilization audit proves that current-host entanglement is the actual blocker."

This is honest but **slightly under-specified about what evidence would trigger escalation**. The acceptance criteria focus on route-level and surface-level correctness (no 404, clean replay, etc.) but don't define what "current-host entanglement is the actual blocker" looks like concretely.

Examples of evidence that should trigger escalation:
- if the ERR_CONNECTION_REFUSED is caused by Critic-host-specific network topology and would not occur on a standalone host
- if fixing residual defects requires changes to shared Critic code that risk regression on non-Close-Read surfaces
- if the browser-proof harness reveals that Close Read routes are fragile because they share state/context with unrelated Critic features

The memo would be more honest if Phase 4 included explicit escalation triggers rather than leaving them entirely to judgment.

### 5. The browser-proof harness should capture console errors, not just route results

Phase 2 specifies that the harness should "capture route result plus screenshot/trace evidence." This is necessary but insufficient for diagnosing the known residual.

The ERR_CONNECTION_REFUSED is a **console/network error**, not a route-level failure. A Playwright harness that only checks HTTP status and takes screenshots will report the genealogy route as passing while the residual continues to exist.

The harness should explicitly capture:
- browser console errors (via `page.on('console')` or `page.on('pageerror')`)
- network request failures (via `page.on('requestfailed')`)
- classify each route by the four-tier scheme in Phase 1, not just by screenshot

### 6. The-critic local checkout divergence is significant but properly addressed

The local `the-critic` checkout is **24 commits behind origin/master**. This means the local tree does not contain the April 13 Close Read publication commits (232c368 through 938c09f).

Phase 0 of the scope memo explicitly requires "source-align the-critic to deployed origin/master" before changing code. This is correct and critical. Without this step, any implementation work would be based on stale code that predates the public Close Read surface.

### 7. The admitted family set claim is accurate

The memo claims the admitted set is:
- genealogy
- AOI thematic single-thinker
- concept analysis: inferential, logical

The deployed routes and the April 13 browser matrix confirm exactly three families with exactly these modes. No extra concept submodes or additional families were observed in the deployed source.

---

## Corrections Required

### Correction 1: Phase 1 should anticipate cross-repo origin of ERR_CONNECTION_REFUSED

The current Phase 1 framing assumes the genealogy console errors are the-critic-local. Rewrite the Phase 1 scope to:

> Reproduce the known live genealogy ERR_CONNECTION_REFUSED residual. Classify whether the error originates from:
> - a the-critic frontend code defect
> - a the-critic backend endpoint failure
> - a transient analyzer-v2 network/availability seam
>
> If the origin is analyzer-v2 availability, the fix should remain the-critic-local (improved error handling, graceful fallback, or error suppression) rather than pulling analyzer-v2 into scope.

### Correction 2: Phase 2 browser-proof harness must capture console and network errors

Add to Phase 2 requirements:

> The harness must capture browser console errors and network request failures per route, not only route-level HTTP status and screenshots. The known residual is a console-level error, not a route-level failure, and a harness that ignores console/network diagnostics will miss it.

### Correction 3: Phase 4 should name concrete escalation triggers

Add to Phase 4:

> The delivery-posture freeze should answer not only "is the surface clean enough" but should explicitly document whether any of the following escalation triggers were encountered:
> - residual defects caused by shared Critic host infrastructure rather than Close Read code
> - fixes that required changes to non-Close-Read Critic code paths
> - browser-proof failures caused by shared Critic state/context contamination
> - network-topology issues that would not exist on a standalone host
>
> If none were encountered, the posture should remain current-host. If any were encountered, document them as the explicit rationale for a future extraction corridor.

---

## Secondary Observations (Not Blocking)

1. **Bundle fingerprint is stable**: The live bundle `main.1d26cf69.js` matches the April 13 completion evidence. No subsequent deploys have changed the frontend since the publication tranche.

2. **The April 5 V1 product memo is now historically interesting, not governing**: The V1 memo froze a genealogy-only boundary. The V1.5 coexistence scope added AOI. The April 13 publication completed the three-family umbrella including concepts. The current scope memo correctly treats the three-family umbrella as the active surface rather than referencing V1 boundaries.

3. **The April 11 operator-surface scope was completed on April 13**: The operator-surface and thin-host normalization tranche closed successfully. The scope memo correctly references that completion and does not reopen it.

4. **Render deployment model**: The memo correctly notes that `render.yaml` is documentary, not blueprint-managed. The live services are dashboard-managed with auto-deploy from master.

---

## Is This Ready To Execute?

**Yes, with the three corrections applied.**

The memo's strategic reading is correct: this is the smallest honest question before extraction or expansion. The evidence chain from the prior 10 days supports the claim that the public surface is real and the next move is stabilization. The scope boundaries are appropriately narrow.

The three corrections do not change the scope's direction or boundaries. They improve the diagnostic precision of Phases 1, 2, and 4 so the tranche produces trustworthy evidence for the delivery-posture decision rather than potentially misclassifying the known residual.
