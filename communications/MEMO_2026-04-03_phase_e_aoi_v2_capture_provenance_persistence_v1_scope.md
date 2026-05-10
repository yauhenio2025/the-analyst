# Memo: Phase E AOI V2 Capture Provenance Persistence V1 Scope

Subtitle: Persist analyzer item identity and truthful analysis workflow provenance through the existing capture create-and-route seam on one live specialized V2 surface

Date: 2026-04-03
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
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
Immediate Prior Code Completion:
- `communications/MEMO_2026-04-02_phase_e_aoi_by_theme_nested_finding_handle_propagation_v1_completion.md`
Review Context:
- `communications/REPORT_Codex_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Audit_2026-04-03.md`
- `communications/REPORT_Claude_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Critique_2026-04-03.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Define the next bounded Phase E slice after the completed AOI V2 `aoi_by_sin_type` capture-selection consumer proof.

That proof answered one question cleanly:

- one live current host can already consume the analyzer contract on one specialized findings surface and create a well-formed `CaptureSelection`

The next honest question is one step deeper and still bounded:

- do the current capture-adjacent host paths preserve analyzer item identity and truthful analysis workflow provenance once that now-proven selection is submitted or saved?

This memo therefore scopes:

- one cross-repo host/backend persistence slice
- on the same AOI `aoi_by_sin_type` line first
- with no analyzer changes
- and with no claim that workflow-neutral mutation semantics or end-to-end Arsenal mutation parity are thereby solved

It does not scope:

- another analyzer-only semantic refinement
- generic renderer-package affordance consumption
- mixed-surface consumer work on `aoi_by_theme`
- generic capture-status generalization
- workflow-neutral Arsenal mutation taxonomy

## Strategic Decision

The next concrete move should be:

- one bounded capture-provenance persistence slice on the existing AOI V2 `aoi_by_sin_type` line, covering both the routed capture path and the current direct research-question save path

not:

- more analyzer-side specialization work
- immediate generic renderer-package consumption rules
- `aoi_by_theme` mixed-surface consumer work
- broader `/captures/by-job` generalization for analysis surfaces
- end-to-end `/api/arsenal` parity claims

The reason is straightforward:

- analyzer-side affordance and handle truth now exists
- one live current host now proves that truth is consumable at the selection-creation boundary
- the current concrete loss point is the capture/create-and-save seam after selection, not the surface contract itself
- fixing that seam teaches more reusable host/runtime law than another AOI-local analyzer shape

This is the smallest honest next step because it varies the proof boundary, not the analyzer semantics:

- keep the already-proven surface fixed
- keep the already-proven host selection rule fixed
- test whether the current capture pipeline can carry the truth it now receives

## Current Evidence Base

Seven repo facts make this the right next slice:

1. the bounded AOI V2 host proof already emits `entity_id` on the proven `aoi_by_sin_type` path
2. `CaptureSelection` in `webapp/src/contexts/CaptureContext.tsx` already has optional `entity_id`
3. `CaptureContext.submitCapture(...)` currently drops that field and does not send analysis workflow provenance in `POST /api/captures`
4. `CaptureCreateRequest`, `CaptureResponse`, and `GenealogyCaptureDB` currently do not persist those values
5. `capture_to_arsenal(...)` still hardcodes `workflow_key = "intellectual_genealogy"` in `source_snapshot`
6. the current AOI “Research Question” flow in `webapp/src/components/ResearchFlagDialog.tsx` creates both a capture and a research todo directly, and currently drops the same provenance on both request bodies
7. `_workflowKey` already exists on the bounded V2 path as a workflow-type identifier; the next truthful field is therefore workflow provenance metadata, not exact source-run identity

There is also one important smaller boundary to name explicitly:

- `GET /api/captures/by-job/{job_id}` still keys only off `genealogy_job_id`

That matters, but this memo treats it as a later capture-status generalization question, not part of the first provenance-persistence slice.

## Scope

### In scope

1. **One minimal host selection extension**

On the bounded AOI V2 proof line, extend the emitted `CaptureSelection` with:

- `source_workflow_key: str | None`

The existing analyzer/host evidence already gives the value:

- `V2TabContent.tsx` threads `_workflowKey`
- the local `aoi_by_sin_type` renderer already has the exact selection creation seam
- `_workflowKey` is already the relevant workflow-type identifier here, not a run-specific UUID

This keeps the host-side addition minimal:

- do not redesign capture UI
- do not add a second selection object
- do not infer workflow provenance downstream if the renderer already knows it

2. **Preserve the current genealogy fallback while widening provenance persistence**

The implementation must keep the current genealogy capture behavior intact:

- `CaptureContext.submitCapture(...)` currently uses `entity_id` as a `genealogy_job_id` fallback only for genealogy captures

That fallback should remain for existing genealogy callers while the same request body also begins forwarding:

- `entity_id`
- `source_workflow_key`

This slice should not “fix” genealogy behavior by breaking the fallback that current genealogy selections rely on.

3. **Persist analyzer item identity and workflow truth on the capture record**

Extend the current capture create/persist/response seam to carry:

- `entity_id`
- `source_workflow_key`

Expected seams:

- `webapp/src/contexts/CaptureContext.tsx`
- `api/server.py::CaptureCreateRequest`
- `api/server.py::CaptureResponse`
- `api/server.py::create_capture(...)`
- `api/server.py::_capture_to_response(...)`
- `api/models_db.py::GenealogyCaptureDB`

The contract should stay additive and optional:

- existing genealogy and research capture callers keep working
- older persisted capture rows may still have null values

4. **Cover both live research paths, not only the routed capture leg**

The current live research-question path is not only:

- `capture_to_research_todo(...)`

It is also:

- `ResearchFlagDialog` creating a capture directly with `POST /api/captures`
- `ResearchFlagDialog` creating a research todo directly with `POST /api/research-todos`

So this slice must preserve truthful provenance on both paths:

- the routed `/captures/{id}/to-research-todo` leg
- the direct `ResearchFlagDialog -> /api/research-todos` leg

Fixing only the routed capture leg would still leave the live AOI research-question path under-scoped.

5. **Route source snapshots from persisted truth rather than genealogy defaults**

On the existing routed capture line, use the persisted provenance fields when constructing downstream source snapshots.

That means:

- `capture_to_arsenal(...)` should stop hardcoding genealogy workflow truth in `source_snapshot`
- `capture_to_research_todo(...)` should also carry the same persisted provenance fields in `source_snapshot`
- `ResearchFlagDialog` direct `POST /api/research-todos` should also carry the same provenance fields in `source_snapshot`

The intended truth is:

- if the host submitted `entity_id`, the stored capture and routed snapshot preserve it
- if the host submitted `source_workflow_key`, the stored capture and routed snapshot preserve it

The surrounding snapshot shapes may remain different across Arsenal and research-todo flows.
What must be identical is the presence and meaning of the new provenance fields.

This slice is about truthful persisted provenance metadata.
It is not yet about making every downstream mutation taxonomy workflow-neutral.

6. **Keep the existing capture model naming and genealogy job lookup bounded**

Do not widen this into a naming or status-generalization cleanup.

That means:

- `GenealogyCaptureDB` may keep its current table/model name
- `genealogy_job_id` semantics stay unchanged
- `GET /api/captures/by-job/{job_id}` may remain genealogy-only in v1

The reason is scope discipline:

- the smallest current loss is dropped provenance fields
- generalized capture-status indexing is a separate later question

7. **Land the required DB migration explicitly**

Because this slice adds two new nullable persisted fields on `GenealogyCaptureDB`, it must include:

- one explicit database migration adding nullable `entity_id`
- one explicit database migration adding nullable `source_workflow_key`

This should be called out directly rather than left implicit in application-code changes.

8. **Keep analyzer item-handle semantics explicit**

The persisted `entity_id` here is:

- the opaque analyzer item handle emitted on the proven AOI V2 path
- not Critic's legacy numeric `db_id`
- not a host mutation contract by itself
- not a cross-run identity guarantee

The honest claim remains:

- job-scoped or output-scoped analyzer provenance truth is preserved once captured

### Explicitly out of scope

- any analyzer-v2 code changes
- `aoi_by_theme` mixed-surface consumer work
- generic renderer-package affordance consumption
- capture-status generalization beyond `genealogy_job_id`
- renaming `GenealogyCaptureDB`
- generic `source_job_id` redesign
- workflow-neutral Arsenal stream taxonomy
- end-to-end `/captures/...` to Arsenal success claims
- direct `/api/arsenal` mutation parity

## Population And Contract Shape

The implementation should stay minimal and source-of-truth-oriented.

Expected host-side shape:

- keep the current `aoi_by_sin_type` renderer proof logic
- add `source_workflow_key` at the same selection creation seam that already emits `entity_id`
- keep `CaptureActionBar` behavior unchanged
- keep `CaptureContext.submitCapture(...)` responsible for forwarding the additive fields while preserving the existing genealogy `entity_id -> genealogy_job_id` fallback
- update `ResearchFlagDialog` so its direct capture create and direct research-todo create requests also preserve the same provenance fields

Expected backend shape:

- extend `CaptureCreateRequest` and `CaptureResponse` with optional:
  - `entity_id`
  - `source_workflow_key`
- persist those fields on `GenealogyCaptureDB`
- return them from `_capture_to_response(...)`
- add one explicit DB migration for those nullable columns
- make routed source snapshots read from the persisted capture record, not inferred defaults
- keep the new provenance fields present in both Arsenal and research-todo source snapshots even if the surrounding snapshot structures remain asymmetric
- keep exact source-run identity deferred; `source_workflow_key` is workflow truth, not run identity

This slice should not redefine the existing genealogy-specific fallback behavior for old callers.
It should simply stop dropping truth when the bounded AOI V2 host proof already supplies it.

## Acceptance Bar

This slice should count as complete only if all of the following are true:

1. the bounded `aoi_by_sin_type` host proof path now submits `entity_id` and `source_workflow_key`
2. `POST /api/captures` persists those fields when present
3. `CaptureResponse` returns those fields when present
4. `ResearchFlagDialog` direct create flows also preserve the same provenance fields on both the capture and research-todo path
5. `capture_to_arsenal(...)` source snapshots use persisted workflow truth rather than hardcoded genealogy workflow truth
6. `capture_to_research_todo(...)` source snapshots also preserve the same provenance fields
7. research-todo direct-create snapshots also preserve the same provenance fields
8. older callers that do not provide the new fields keep working
9. the current genealogy `entity_id -> genealogy_job_id` fallback remains intact
10. `source_workflow_key` is treated as workflow-type truth, not exact source-run identity
11. an explicit DB migration lands for the two new nullable capture columns
12. `genealogy_job_id` semantics remain unchanged
13. `/api/captures/by-job/{job_id}` generalization remains explicitly deferred
14. the analyzer `entity_id` remains framed as opaque and non-equivalent to Critic `db_id`
15. no analyzer-v2 code changes are required
16. no claim is made that workflow-neutral Arsenal stream taxonomy or end-to-end Arsenal parity is now solved

## Test Plan

### Host-side verification

Add or extend focused tests for:

- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.test.tsx`
  - the bounded renderer emits `source_workflow_key` together with the already-proven `entity_id`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.test.tsx`
  - `_workflowKey` is still threaded correctly into the renderer-config seam used by the proof surface
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
  - add focused coverage for `submitCapture(...)` request bodies so `entity_id` and `source_workflow_key` are forwarded on create
  - prove the existing genealogy `entity_id -> genealogy_job_id` fallback remains intact
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
  - add focused coverage so the direct capture-create and direct research-todo-create requests both preserve the same provenance fields

### Backend verification

Add focused API coverage in `the-critic` for:

- capture creation persists and returns:
  - `entity_id`
  - `source_workflow_key`
- `capture_to_arsenal(...)` includes those values in the stored mutation source snapshot and no longer hardcodes genealogy workflow truth for the AOI proof line
- `capture_to_research_todo(...)` includes those values in the created todo source snapshot
- direct `POST /api/research-todos` also preserves those values in `source_snapshot`
- existing genealogy callers still pass without providing the new fields
- one migration check proves the new nullable capture columns exist after upgrade

If dedicated backend tests do not yet exist in `the-critic/api`, this slice may create the minimum focused test seam required to lock the new contract down.

### Browser proof

Add one focused browser/network proof on the existing AOI V2 `aoi_by_sin_type` page path:

- create the bounded capture selection through the existing capture UI and prove the routed capture path preserves the new provenance fields
- also exercise the current AOI “Research Question” save path and prove its direct create requests preserve the same provenance fields

The browser proof should remain bounded:

- it does not need to prove generic capture-status dots
- it does not need to prove end-to-end Arsenal parity

## Assumptions

- `source_workflow_key` is the smallest truthful workflow-type field for this slice; it does not solve exact source-run identity, and broader source-job indexing can remain deferred.
- The current genealogy-shaped capture model/table naming can stay in place while the contract broadens additively.
- The right v1 closeout is truthful persisted provenance metadata on the capture record and downstream snapshots, not a broader mutation-taxonomy redesign.
- The bounded AOI V2 `aoi_by_sin_type` proof line remains the right first target because it already proves selection-creation sufficiency and analyzer specialization there.
