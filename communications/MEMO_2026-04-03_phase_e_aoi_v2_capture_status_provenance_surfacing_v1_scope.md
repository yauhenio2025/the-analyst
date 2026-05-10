# Memo: Phase E AOI V2 Capture Status/Provenance Surfacing V1 Scope

Subtitle: Read persisted capture truth back onto the same bounded AOI `aoi_by_sin_type` V2 findings surface after reload, using stored entity/workflow provenance rather than genealogy-job assumptions

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
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`
Immediate Prior Code Completion:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
Immediate Prior Scope And Reviews:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_scope.md`
- `communications/REPORT_Codex_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Audit_2026-04-03.md`
- `communications/REPORT_Claude_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Critique_2026-04-03.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Define the next bounded Phase E slice after the completed AOI V2 capture-provenance persistence closeout.

That closeout answered the write-side question cleanly:

- one bounded Critic pipeline can now preserve analyzer `entity_id` and truthful workflow-type provenance after submission/save on the AOI `aoi_by_sin_type` line

The next honest question is the read-side counterpart:

- can the current Critic runtime read that persisted truth back onto the same bounded AOI `aoi_by_sin_type` surface after reload or revisit?

This memo therefore scopes:

- one host/backend read-side proof in Critic
- on the same AOI `aoi_by_sin_type` line first
- with no analyzer changes
- and with no claim that generic capture-status law, workflow-neutral routed semantics, or mixed-surface consumer behavior are thereby solved

## Strategic Decision

The next concrete move should be:

- one bounded AOI V2 capture-status/provenance surfacing slice on `aoi_by_sin_type`

not:

- another analyzer-only semantic refinement
- immediate `aoi_by_theme` consumer work
- generic renderer-package capture-status behavior
- generic `/api/captures/by-job/{job_id}` generalization
- workflow-neutral capture taxonomy redesign
- a new non-AOI consumer proof before the current AOI line is closed on the read side

The reason is straightforward:

- the analyzer contract is already emitted
- one live host already creates correct selections from it
- persisted capture truth now survives write-side submission/save
- the remaining concrete loss is read-side visibility of that truth back on the AOI page
- the current shared read seam is not merely too coarse for AOI card truth; AOI analysis captures persist with `genealogy_job_id = null`, so that route cannot match them at all

This still varies the proof boundary rather than the analyzer semantics:

- keep the same bounded specialized AOI surface
- keep the same capture pipeline
- test whether persisted truth can now be consumed back on the page

## Current Evidence Base

Seven concrete repo facts make this the right next slice:

1. `AoiSinFindingsRenderer.tsx` already emits:
   - `entity_id`
   - `source_workflow_key`
2. capture creation and direct research-question save now persist those fields truthfully on the capture record
3. routed Arsenal and routed research-todo snapshots now also carry:
   - `workflow_key`
   - `source_workflow_key`
   - `entity_id`
4. `V2TabContent.tsx` already threads `_captureStatusMap` into renderer config
5. `useCaptureStatus.ts` already exists, but only calls `GET /api/captures/by-job/{job_id}`
6. `GET /api/captures/by-job/{job_id}` is still genealogy-job keyed, section-level, and not project-scoped, so it is not merely coarse for AOI card truth; AOI analysis captures with `genealogy_job_id = null` cannot match it at all
7. the bounded AOI consumer surface already has exactly the right per-card handle for read-back:
   - `finding_id`

One additional boundary matters for honesty:

- older captures may still have null `entity_id` and null `source_workflow_key`

That means a truthful v1 must degrade silently for those rows rather than pretending universal historical coverage now exists.

## Scope

### In scope

1. **One bounded analysis-compatible capture-status lookup seam**

Do not stretch `GET /api/captures/by-job/{job_id}` into analysis semantics in v1.

The current route is the wrong contract for this slice, not just an incomplete one:

- it filters only on `genealogy_job_id`
- AOI analysis captures intentionally persist with `genealogy_job_id = null`
- it is not project-scoped
- it returns no `entity_id`
- it returns no `source_workflow_key`

Instead add one separate bounded read seam in Critic keyed by persisted analysis truth:

- `source_workflow_key`
- `source_view_key`
- `entity_id[]`

Project truth should still come from the existing project header.

The lookup should return raw persisted capture rows for those entity ids, not a new workflow-neutral status taxonomy.

At minimum each returned row should preserve:

- `capture_id`
- `entity_id`
- `destination`
- `research_status`
- `has_answer`

The new seam must be project-scoped from the existing project header.

`source_view_key` and `source_workflow_key` may also be echoed for clarity, but the critical point is:

- the backend lookup key must now be analysis-compatible and item-compatible
- the response may stay close to the existing capture-status vocabulary rather than inventing new status law

2. **One bounded local host read-side proof on `aoi_by_sin_type`**

Keep this read-side proof local to the existing bounded AOI renderer path.

That means:

- no generic renderer-package capture-status rule
- no mixed-surface consumer work
- no changes to `aoi_by_theme`

The host should use the new lookup seam only on `aoi_by_sin_type`, where:

- specialization already exists
- `finding_id` already exists
- whole-view shape is already proven

3. **Surface passive per-card truth, not new mutation law**

The UI proof should stay passive-first.

The smallest honest surface is:

- show bounded per-card state derived from persisted captures

For example:

- Arsenal already captured
- Research todo exists
- Research answer exists

This should be treated as read-back visibility only.
It should not yet broaden into:

- capture deduplication rules
- repeat-capture blocking rules
- automatic deep-linking to destination items
- workflow-neutral destination semantics

4. **Use persisted truth, not local heuristics**

The host read path should rely on persisted capture truth, not reconstruct capture state from:

- current local selection state
- current `lastResult`
- card text matching
- section-key-only heuristics

That is the real point of the slice:

- prove that the newly persisted `entity_id` plus `source_workflow_key` are already sufficient for one bounded read-side host proof

5. **Keep the existing genealogy status seam untouched**

Do not repurpose or rename the existing genealogy path in v1:

- `GET /api/captures/by-job/{job_id}`
- `useCaptureStatus.ts`

They may remain genealogy-job keyed and section-level.

This slice should add one bounded AOI-compatible read seam rather than pretending the generic status problem is solved.
That is smaller and more honest than widening the current route, because the current route would need a new filter model, new response truth, and new frontend grouping behavior before it even became AOI-compatible.

6. **Handle older captures honestly**

Rows lacking:

- `entity_id`
- or `source_workflow_key`

should simply not match the bounded AOI lookup.

That is acceptable and honest for v1.
The read-side proof is about truthful surfacing of persisted capture truth where it exists, not retroactive repair of historical rows.

7. **Keep fresh-load truth primary**

The required proof boundary is:

- reload, revisit, or fresh fetch of the AOI V2 page/surface shows persisted capture truth on the matching cards

Immediate in-session optimistic synchronization after a new capture may be added only if it falls out trivially from the same bounded hook.
It is not the thing this slice must prove.

### Explicitly out of scope

- any analyzer-v2 code changes
- `aoi_by_theme` mixed-surface consumer work
- generic renderer-package capture-status rules
- generic `/api/captures/by-job/{job_id}` redesign
- workflow-neutral destination/status taxonomy
- exact source-run identity
- end-to-end Arsenal or research-todo lifecycle semantics
- destination deep-link UX
- capture deduplication or repeat-capture policy

## Acceptance Bar

This slice is successful only if all of the following are true:

1. persisted AOI `aoi_by_sin_type` captures can be looked up by:
   - `source_workflow_key`
   - `source_view_key`
   - `entity_id`
   - and existing project scope
2. a fresh load or revisit of the bounded AOI V2 `aoi_by_sin_type` surface surfaces passive card-level capture truth using that lookup
3. the host proof works for both persisted destinations already proven on this line:
   - Arsenal
   - research todo
4. research-answer truth can also surface when present, using the existing `research_status` / `has_answer` vocabulary rather than a new status law
5. older captures with null provenance fields do not error and do not produce false-positive card states
6. the existing genealogy `/api/captures/by-job/{job_id}` seam remains intact and un-reinterpreted
7. the proof stays host/backend only in Critic
8. no analyzer changes are required

## Test Plan

### Backend/API tests

Add focused backend coverage for the new AOI-compatible read seam:

- lookup by:
  - `source_workflow_key`
  - `source_view_key`
  - `entity_id[]`
- request remains project-scoped through the existing header
- matching AOI capture rows return truthful persisted:
  - `entity_id`
  - `destination`
  - `research_status`
  - `has_answer`
- rows with null `entity_id` or null `source_workflow_key` do not match
- older genealogy `/captures/by-job/{job_id}` behavior remains unchanged

### Host unit tests

Add focused host coverage on the bounded AOI renderer path:

- the local `aoi_by_sin_type` renderer or local hook fetches read-back truth for card `finding_id` values
- passive per-card state appears only when matching persisted capture rows exist
- cards without matching persisted truth remain visually passive
- older or handle-less payloads remain readable and unbroken
- no generic renderer-package behavior changes are required

### Browser proof

Extend the bounded AOI V2 browser proof to cover fresh-load/read-back truth:

- create or seed a persisted AOI capture with truthful provenance
- load or reload the AOI `aoi_by_sin_type` page
- verify the matching card surfaces the expected passive state
- verify non-matching cards remain unaffected

The browser proof target is:

- persisted truth is visible after reload/revisit

It is not:

- end-to-end destination lifecycle
- repeat-capture policy
- deep-link navigation

## Assumptions

- `aoi_by_sin_type` remains the right first read-side proof because it is still the only current surface with:
  - specialized affordance
  - per-card `finding_id`
  - bounded host proof already in place
- a separate AOI-compatible read seam is cleaner for v1 than overloading the genealogy `/captures/by-job/{job_id}` route
- more strongly: the current genealogy route cannot match AOI analysis captures at all, so a separate AOI-compatible seam is not just cleaner but materially smaller and more honest
- passive per-card surfacing is the smallest honest read-side proof; active recapture rules and destination deep-link UX can remain later questions
- reusable-substrate value in this slice is real but still modest: it proves analyzer-identity read-back on one bounded surface, not generic capture-status law
- after this read-side slice, the case for further AOI-only work becomes weaker unless the next move broadens substrate value beyond the same bounded surface family
