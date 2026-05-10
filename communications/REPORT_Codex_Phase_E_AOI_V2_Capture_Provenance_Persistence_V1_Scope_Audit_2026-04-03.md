# Report: Phase E AOI V2 Capture Provenance Persistence V1 Scope Audit

Date: 2026-04-03

## Verdict

`approve with corrections`

The direction is correct.
After the bounded `aoi_by_sin_type` selection-creation proof, the next real loss point is the Critic capture seam, not another analyzer-only AOI slice.

The corrections are about scope honesty:

- distinguish persisted provenance truth from workflow-neutral mutation semantics
- if research-todo stays in scope, include the real `ResearchFlagDialog` path, not only `capture_to_research_todo(...)`
- say explicitly that `source_workflow_key` fixes workflow truth, not exact source-run addressability

## The Memo's Strongest Code-Backed Points

### 1. The analyzer already emits the bounded AOI inputs this slice wants to preserve

This part is solid.

- `src/aoi/contract.py:333-356` assigns analyzer-owned string `finding_id`
- `src/aoi/contract.py:676-694` carries that handle onto `aoi_by_sin_type` cards
- `src/presenter/first_hop_affordance.py:87-96` attaches `specialized_family="findings_bank_arsenal_promotion_v1"` only on AOI `aoi_by_sin_type` when the payload proves complete handles
- `tests/test_presentation_api.py:1355-1394` and `tests/test_aoi_contract.py:291-332` verify that contract

So the memo is right that this slice does not need new analyzer semantics first.
The analyzer-side truth it depends on already exists.

### 2. The host already has the minimal workflow truth available at the exact AOI selection seam

The current host wiring supports the memo's basic direction.

- `webapp/src/components/V2TabContent.tsx:579-597` threads `_workflowKey`, `_captureJobId`, and `_firstHopAffordance` into renderer config
- `webapp/src/components/V2TabContent.test.tsx:378-444` verifies that AOI `aoi_by_sin_type` gets that config
- `webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:149-165` turns an eligible card click into a `CaptureSelection` with `entity_id`
- `webapp/src/components/renderers/AoiSinFindingsRenderer.test.tsx:100-146` verifies the emitted selection includes `entity_id: "find-B"`

That means `source_workflow_key` really is available without any analyzer change.
The host already knows it.

### 3. The current capture creation seam really does drop analyzer provenance

This is the memo's strongest implementation claim, and it is correct.

- `webapp/src/contexts/CaptureContext.tsx:17-35` defines optional `entity_id` on `CaptureSelection`
- `webapp/src/contexts/CaptureContext.tsx:103-122` omits `entity_id` and any workflow field from `POST /api/captures`
- `api/server.py:1284-1321` defines `CaptureCreateRequest` and `CaptureResponse` without `entity_id` or `source_workflow_key`
- `api/models_db.py:2666-2703` defines `GenealogyCaptureDB` without storage for either field

So yes: the current `/captures` seam drops analyzer provenance in practice.

### 4. Routed snapshots currently lose or overwrite workflow truth

This is also correct, and it matters to real product behavior.

- `api/server.py:22737-22747` hardcodes `workflow_key: "intellectual_genealogy"` in Arsenal `source_snapshot`
- `webapp/src/pages/ArsenalPage.tsx:192-207` consumes that `workflow_key` to build deep links back into analysis
- `api/server.py:22862-22878` builds a research-todo `source_snapshot` with only `selected_text`, `structured_data`, and `depth_level`

So preserving truthful workflow provenance has immediate user-facing value, not just internal neatness.

### 5. The memo is honest that analyzer `entity_id` is not Critic `db_id`

The distinction is code-backed.

- analyzer `finding_id` is a string handle in `src/aoi/contract.py:333-356`
- Arsenal items still point to numeric `critique_findings.id` in `api/models_db.py:152-167`

So the memo is right to frame analyzer `entity_id` as opaque analyzer provenance, not as direct mutation parity with Critic's legacy database ids.

### 6. Keeping `/captures/by-job/{job_id}` generalization out of scope for v1 is honest

The current status path is still plainly genealogy-shaped.

- `webapp/src/hooks/useCaptureStatus.ts:24-42` fetches `/captures/by-job/${jobId}`
- `api/server.py:22905-22923` still resolves that route with `GenealogyCaptureDB.genealogy_job_id == job_id`

That is a real separate problem, but it is not the smallest current truth-loss problem.

## The Memo's Weakest Or Overstated Assumptions

### 1. The research-todo part is under-scoped relative to the real AOI UI path

This is the biggest correction.

The current AOI "Research Question" path is not only `CaptureContext.submitCapture(...)`.
It also materially goes through:

- `webapp/src/components/ResearchFlagDialog.tsx:105-168`

That dialog:

- directly `POST`s `/api/captures`
- directly `POST`s `/api/research-todos`
- omits `entity_id` and workflow provenance in both request bodies
- then calls `/captures/{id}/to-research-todo` only as a non-critical follow-up

So a route-only fix for `capture_to_research_todo(...)` does not fully cover the current AOI proof surface.

If research-todo provenance stays in this memo's acceptance bar, `ResearchFlagDialog.tsx` needs to be added to:

- the scoped seams
- the host-side test plan
- the acceptance story

Otherwise the memo should narrow v1 to Arsenal-first provenance persistence.

### 2. `source_workflow_key` is the smallest defensible workflow-truth field, but it does not solve exact run addressability

The memo is directionally right here, but it should be more explicit.

`source_workflow_key` is the right minimal workflow-truth field because:

- analyzer `FirstHopAffordance` has no workflow slot in `src/presenter/schemas.py:695-700`
- the host already knows the workflow at `webapp/src/components/V2TabContent.tsx:579-580`
- Arsenal deep-linking currently only needs `workflow_key` plus the existing view/section data in `webapp/src/pages/ArsenalPage.tsx:192-207`

But the host also already has `presentation.job_id` at `webapp/src/components/V2TabContent.tsx:579-595`.
If the memo wants to claim job-scoped or output-scoped provenance truth, it should say more clearly that deferring a non-genealogy source job id means:

- v1 fixes workflow truth
- v1 does not yet fix exact source-run identity for non-genealogy captures

That stronger claim should stay deferred unless a later slice adds a neutral source-job field.

### 3. The memo should separate persisted provenance truth from routed mutation semantics more explicitly

The memo is correct to keep workflow-neutral Arsenal taxonomy out of scope.
But it should say more clearly what remains genealogy-shaped.

- `api/server.py:22691-22716` still tells the model it is transforming "genealogy analysis data"
- `api/server.py:22820-22850` still tells the model the capture came from "genealogy analysis data"
- `api/server.py:22729-22730` still writes `stream = f"genealogy_{...}"`

So if those prompts and stream names remain untouched, the honest v1 claim is:

- stored provenance metadata becomes truthful

not:

- the full routed mutation path becomes workflow-neutral

That distinction matters for roadmap honesty.

### 4. The reusable-substrate value is real, but it should be described modestly

This slice does teach something reusable:

- once a thin host receives analyzer-owned identity and workflow truth, capture persistence should preserve it rather than overwrite it with genealogy defaults

That is more reusable than another AOI-only analyzer semantic slice.

But the current storage/status substrate is still genealogy-branded:

- `GenealogyCaptureDB`
- `genealogy_job_id`
- `/captures/by-job/{job_id}`

So the memo should avoid implying that capture generalization itself is solved.

## Factual Discrepancies I Found

### 1. The memo's research-todo routing scope misses the actual current host path

`webapp/src/components/ResearchFlagDialog.tsx:105-168` is materially part of capture creation and research-todo persistence today.

If research-todo provenance is in scope, this file belongs in the required seams and tests.

### 2. The current hardcoded genealogy truth appears in more than `source_snapshot`

The memo calls out `source_snapshot.workflow_key` hardcoding, which is real.
But the same genealogy assumption also lives in:

- the Arsenal mutation prompt text at `api/server.py:22691-22716`
- the research-todo mutation prompt text at `api/server.py:22820-22850`
- Arsenal stream naming at `api/server.py:22729-22730`

That does not invalidate the memo.
It just means the memo should state more carefully that this v1 is about persisted provenance truth, not all routed workflow semantics.

### 3. The current Critic codebase appears to have no existing backend test coverage for the `/api/captures` seam

I found frontend tests for:

- AOI selection emission
- V2 config threading

I did not find existing Critic tests around:

- `create_capture(...)`
- `capture_to_arsenal(...)`
- `capture_to_research_todo(...)`

So the memo is right to demand focused new backend coverage here.

## What This Changes For The Larger Roadmap

This memo is still pointing at the right immediate next variable.

The analyzer-side question has already been answered on the bounded AOI line:

- the analyzer emits `finding_id`
- the presenter emits bounded first-hop affordance
- the current host can turn that into a valid `CaptureSelection`

The next honest gap is now host/backend truth preservation.

That is a better Phase E move than another AOI-local analyzer semantic refinement because it teaches a reusable thin-host rule:

- analyzer-owned identity and workflow provenance must survive capture creation and downstream frozen snapshots

But the roadmap implication should stay calibrated.
This v1 does not settle:

- status lookup generalization
- workflow-neutral Arsenal mutation taxonomy
- end-to-end Arsenal parity
- exact run-addressable provenance for non-genealogy captures

## The Most Defensible Next Move After This Memo

Approve the direction, but tighten the scope before implementation.

The smallest defensible v1 is:

- persist `entity_id` and `source_workflow_key` on the capture record and response
- use those persisted fields when building Arsenal `source_snapshot`
- keep `/captures/by-job`, `GenealogyCaptureDB` renaming, workflow-neutral stream taxonomy, and exact non-genealogy source-job identity deferred

If the slice insists on keeping research-todo parity in the same tranche, then the scope must explicitly add:

- `webapp/src/components/ResearchFlagDialog.tsx`
- the direct `/api/research-todos` `source_snapshot` path
- tests for that direct path, not only `capture_to_research_todo(...)`

Without that correction, the memo is directionally right but slightly overcommitted on what the current AOI host path would actually prove.
