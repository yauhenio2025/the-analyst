# Review: Phase 4 / Deliverable D — Cross-Workflow Generic Workspace Scope

Date: 2026-03-19
Reviewer: Claude Opus 4.6

---

## 1. Verdict

**The scope is correct and tight. The tranche is implementable as written with no analyzer-v2 changes.**

The gap between the current generic workspace and a working AOI proof is smaller than it looks — roughly 4 concrete changes to `AnalysisWorkspacePage.tsx`, zero changes to the shared hook or client library, and one small handoff link from the AOI bespoke surface. The scope memo correctly identifies the seam and correctly identifies the risk boundaries.

I have two real corrections (one narrowing, one missing acceptance step) and several confirmed assumptions below.

---

## 2. Findings

### Finding 1: The plumbing is already complete below the generic page

The entire thinker-scoped contract is already wired end-to-end **except** at the `AnalysisWorkspacePage` level:

| Layer | Thinker context? | Evidence |
|---|---|---|
| `boundedV2Client.discoverBoundedV2Runs` | YES — passes `selected_source_thinker_id` | `boundedV2Client.ts:87` |
| `boundedV2Client.discoverBoundedV2Results` | YES — passes `selected_source_thinker_id` | `boundedV2Client.ts:102` |
| `useBoundedV2Workspace` options | YES — accepts `selectedSourceThinkerId` | `useBoundedV2Workspace.ts:28` |
| `useBoundedV2Workspace.discoverActiveRun` | YES — passes `selectedSourceThinkerId` to `discoverBoundedV2Runs` | `useBoundedV2Workspace.ts:313` |
| `AoiV2ThematicPanel` (bespoke surface) | YES — wires everything through | `AoiV2ThematicPanel.tsx:145, 271` |
| **`AnalysisWorkspacePage`** | **NO** — does not read thinker from URL, does not pass to hook or launch body | `AnalysisWorkspacePage.tsx:219-225, 474-478` |
| Critic backend `POST /api/analysis/{wf}/analyze` | YES — delegates to `start_genealogy_analysis`, validates thinker for AOI | `server.py:20091-20099, 19068` |
| `GenealogyAnalysisRequest` model | YES — `selected_source_thinker_id`, `selected_source_thinker_name` | `models_genealogy.py:41-42` |
| analyzer-v2 run/result discovery | YES — query param `selected_source_thinker_id` | Already live |

**Bottom line**: The gap is purely in `AnalysisWorkspacePage` reading query parameters and threading them through to the places that already accept them.

### Finding 2: handleRunAnalysis does not pass thinker context

`AnalysisWorkspacePage.handleRunAnalysis()` (line 468-509) constructs the launch body as:

```typescript
const body: Record<string, unknown> = {
  project_id: projectId,
  execution_backend: 'v2',
  workflow_key: workflowKey,
};
```

This will fail the backend validation at `server.py:19068`:

```python
if workflow_key == AOI_THEMATIC_WORKFLOW_KEY and not request.selected_source_thinker_id:
    raise HTTPException(status_code=400, detail="selected_source_thinker_id is required...")
```

The fix is straightforward: read `selected_source_thinker_id` and `selected_source_thinker_name` from `URLSearchParams` and include them in the body. This is a 5-line change.

### Finding 3: Local saved result filtering requires no model changes

The scope memo hedges on whether "local AOI result payloads carry thinker identity." They do.

`GenealogyResultSummary` (the backend model returned by `/api/analysis/{wf}/results/{project_id}`) already includes `selected_source_thinker_id` and `selected_source_thinker_name` (`models_genealogy.py:100-101`). The backend populates these via `_build_saved_result_summary` → `_extract_result_thinker_identity` (`server.py:18394-18411`).

The `LocalSavedResultSummary` type inside `AnalysisWorkspacePage` (lines 58-66) does not declare these fields yet, but that is a 2-line TypeScript type addition, not a schema or backend change. `AoiV2ThematicPanel` already has the correct type (lines 42-52) and the `matchesThinker` filter (lines 77-86) that can be lifted directly.

### Finding 4: Upstream discovery is already thinker-scoped — but the generic page doesn't use it

`AnalysisWorkspacePage.loadSavedResults()` calls `discoverBoundedV2Results({ projectId, workflowKey })` without `selectedSourceThinkerId` (line 359-361). When the workflow is `anxiety_of_influence_thematic_single_thinker`, this will return results for ALL thinkers in the project — violating acceptance criterion #3.

Fix: pass `selectedSourceThinkerId` (read from URL) to `discoverBoundedV2Results`. The function already accepts it.

### Finding 5: ArsenalPage already proves query-param deep-linking into the generic workspace

`ArsenalPage.tsx:207` constructs URLs like `/p/${projectId}/analysis/${wfKey}?view=X&section=Y`. This proves that the generic workspace already serves as a query-param-driven target. Adding `selected_source_thinker_id` and `selected_source_thinker_name` as additional query params is entirely consistent with existing patterns.

### Finding 6: The AOI entry handoff is trivially implementable

The AOI thinker detail page (`AnxietyOfInfluencePages.tsx`) already has a tabbed view per thinker at `/p/:projectId/anxiety-of-influence/:thinkerId/v2-thematic`. The handoff link into the generic workspace would be:

```
/p/{projectId}/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id={thinkerId}&selected_source_thinker_name={thinkerName}
```

This can be a single `<Link>` or button in either the `AoiV2ThematicPanel` header or the thinker detail tab bar. No route reorganization needed.

---

## 3. Assumptions Tested

| Assumption from scope memo | Tested? | Result |
|---|---|---|
| "Generic route already accepts AOI bounded parameters" | YES | **TRUE** — `GenealogyAnalysisRequest` has `selected_source_thinker_id/name`, generic route delegates to same handler that validates them |
| "boundedV2Client already supports selectedSourceThinkerId" | YES | **TRUE** — both `discoverBoundedV2Runs` and `discoverBoundedV2Results` accept it |
| "useBoundedV2Workspace already supports selectedSourceThinkerId" | YES | **TRUE** — option field exists and is threaded to `discoverActiveRun` |
| "Explicit query params are the right seam" | YES | **TRUE** — consistent with existing ArsenalPage deep-link pattern; alternatives (React Router state, context) would be non-bookmarkable and hide the contract |
| "No analyzer-v2 changes needed" | YES | **TRUE** — all upstream APIs already accept thinker context as query parameters |
| "Local saved results may not carry thinker identity" | YES | **FALSE** — backend already populates `selected_source_thinker_id/name` on `GenealogyResultSummary`; only the TS type on the generic page is missing the declaration |
| "The scope stays critic-first" | YES | **TRUE** — all changes are in `the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx` plus one link from the AOI surface |

---

## 4. Scope Corrections

### 4a. NARROW: Remove the "small Critic-side field pass-through" hedge

The scope memo says:

> If local AOI result payloads do **not** currently carry thinker identity, the only acceptable widening in this tranche is a small Critic-side field pass-through.

They already carry it. The `GenealogyResultSummary` model includes `selected_source_thinker_id` and `selected_source_thinker_name` and the backend populates them. The "widening" hedge can be struck.

What IS needed is a 2-line TypeScript type expansion on the generic page's `LocalSavedResultSummary` interface to declare the fields that the backend already returns.

### 4b. ADD: Explicit `handleRunAnalysis` thinker injection step

The scope memo talks about "one explicit bounded thinker context" and "AOI start request body" but does not call out that `handleRunAnalysis` currently sends no thinker fields at all. This is the single most important code change in the tranche and should be named explicitly as a scope item:

> When the workflow is AOI and thinker context is present in query params, `handleRunAnalysis` must include `selected_source_thinker_id` and `selected_source_thinker_name` in the launch body.

Without this, the AOI launch will 400.

---

## 5. Suggested Acceptance Criteria Changes

Current criteria are sound. Suggested additions:

**Add criterion 2a (between existing 2 and 3):**

> `AnalysisWorkspacePage.handleRunAnalysis` includes `selected_source_thinker_id` and `selected_source_thinker_name` from URL query parameters in the AOI launch body. The backend validates these and the launch succeeds.

**Strengthen criterion 3:**

> AOI active-run and result discovery in the generic workspace are thinker-scoped **for both upstream discovery (via `selected_source_thinker_id` query param to analyzer-v2) and local saved-result listing (via client-side filtering on the `selected_source_thinker_id` field already present in backend responses).**

**Add verification criterion:**

> Manual test: navigate to `/p/{projectId}/analysis/anxiety_of_influence_thematic_single_thinker?selected_source_thinker_id={id}&selected_source_thinker_name={name}`, confirm that: (a) "Run Analysis" starts an AOI job scoped to that thinker, (b) saved results show only that thinker's runs, (c) active-run discovery is thinker-scoped.

---

## 6. Recommended Next Move

**Proceed with implementation.** The scope is correct and the codebase is ready.

The concrete implementation order should be:

1. **Read query params** — add `useSearchParams` to `AnalysisWorkspacePage`, extract `selected_source_thinker_id` and `selected_source_thinker_name`
2. **Wire to hook** — pass `selectedSourceThinkerId` to `useBoundedV2Workspace`
3. **Wire to launch** — include thinker fields in `handleRunAnalysis` body when present
4. **Wire to discovery** — pass `selectedSourceThinkerId` to `discoverBoundedV2Results` in `loadSavedResults`, add `matchesThinker` filter for local results, expand `LocalSavedResultSummary` type
5. **Add handoff link** — one link/button from the AOI thinker detail page to the generic workspace with query params prefilled
6. **Manual proof** — exercise both workflows through the generic route

Estimated change surface: ~60 lines in `AnalysisWorkspacePage.tsx`, ~5 lines for the handoff link, zero changes elsewhere.

No analyzer-v2 work. No backend changes. No route reorganization. The tranche stays `the-critic`-first as the scope memo recommends.
