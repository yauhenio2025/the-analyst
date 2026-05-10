# Memo: Phase 3 Bounded Lifecycle V1 Live Proof Closeout Scope

Subtitle: Close the implemented lifecycle slice with one real save/reopen proof before Phase 4

Date: 2026-03-28
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion: `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_implementation_completion.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`
- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
- `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`
- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-19_phase4_cross_workflow_workspace_scope.md` as an older superseded governance/workspace line, not the active next step

## Purpose

Define the immediate next bounded slice after the Phase 3 lifecycle implementation landed in code.

This memo is not another lifecycle-design memo.
The save/reopen law is now implemented tightly enough for the current roadmap line.

The missing seam is now evidentiary:

- Phase 3 has code
- Phase 3 has focused tests
- Phase 3 does not yet have one recorded live proof that the lifecycle law works end to end on the intended substrate

So the next honest step is:

- one bounded Phase 3 live proof closeout

not:

- Phase 4 governance/evaluation
- another lifecycle schema redesign
- AOI lifecycle productization
- new transient consumer registration

## Current code-backed boundary

### What now exists

The current codebase already has all of the following:

- analyzer-owned file-backed `compose_session` persistence
- analyzer-generated `session_id`
- presenter save/fetch routes:
  - `POST /v1/presenter/compose-sessions`
  - `GET /v1/presenter/compose-sessions/{session_id}`
- Host Contract v2 delivery/runtime families for:
  - `transient_compose_session_save`
  - `transient_compose_session_fetch`
- an existing non-AOI proof page that can now:
  - compose
  - explicitly save
  - reopen by `session_id`
- reopen code that clears prior planning/compose state and fetches only the saved session truth

Primary files carrying that reality:

- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_session_store.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/presenter.py`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx`

### What is still not proved

The program still does not have one recorded live Phase 3 proof that shows:

- one real compose success
- one explicit save success that returns analyzer-generated `session_id`
- one deep-link or reload reopen success by that same `session_id`
- one fail-closed invalid-session negative case

Important current law that this closeout must preserve:

- `planning_decision_id` is planning provenance, not lifecycle identity
- saved lifecycle truth is the persisted compose session, not the planning snapshot
- reopen must not rerun:
  - `route-task`
  - `plan-task`
  - `planning_decision_fetch`
  - lowering
  - `compose-from-intent`

## Strategic decision

Do not jump to Phase 4 yet.

The right next step is to close Phase 3 on the substrate that Phase 3 actually implemented:

- the existing genealogy saved-result transient proof page
- the current registered transient consumer identity:
  - `consumer_key=the-critic`
- the generic direct-sections path, not the AOI source-backed proxy stack

Why this is the right closeout target:

1. It sits on the thinnest generalized transient substrate already proved in Phase 2.
2. It tests the new lifecycle law where it was actually implemented.
3. It avoids reopening AOI-specific proxy identity/continuity semantics as the first lifecycle closeout burden.
4. It keeps Phase 4 governance/evaluation from being built on unproved lifecycle claims.

## Scope decision

The next slice should be a live-proof closeout, not more implementation by default.

Use the existing proof page:

- `/p/:projectId/proof/transient/genealogy-saved-result`

Do not add a sibling lifecycle proof page unless implementation proves the current page cannot honestly carry the closeout.

## Must land

### 1. One completed genealogy saved-result preflight

The closeout must start from one already-completed genealogy saved result.

The closeout does not earn credit by:

- starting fresh genealogy execution
- proving `/v1/executor/jobs`
- quietly shifting away from the saved-result transient substrate

Preflight must confirm at least:

- `workflow_key = intellectual_genealogy`
- `status = completed`
- `result_state = ready`
- `presentation_status = completed`
- `restore_available = true`

The preflight artifact must explicitly capture those run-detail fields.
Do not leave `result_state`, `presentation_status`, or `restore_available` implicit just because the current page exposes them in its trace UI.

### 2. One real `compose -> save -> reopen` chain on the existing proof page

The required live chain is:

1. open the existing genealogy proof page with a completed saved-result target
2. run the existing Phase 2 compose chain
3. explicitly save the transient surface
4. capture the returned analyzer-generated `session_id`
5. reopen the same page by `?session_id=<saved id>`
6. verify the saved session renders without planner/composition replay

Behavior that must be visible in the closeout:

- save is deliberate, not automatic
- the URL changes to `?session_id=<id>`
- reopen mode clears prior planning/compose state
- reopened rendering comes from saved compose-session truth

### 3. One fail-closed invalid-session proof

The closeout must also record one explicit negative case:

- invalid, unknown, or consumer-mismatched `session_id` in reopen mode

Acceptance bar:

- reopen fails closed with a visible error
- the page does not silently fall back to:
  - prior in-memory compose state
  - recomputing planning/composition
  - any AOI proxy or executor path

### 4. One auditable no-recomputation proof

The artifact set must make the lifecycle law auditable.

The closeout must make it obvious that reopen did not call:

- `route-task`
- `plan-task`
- `planning_decision_fetch`
- `planning_decision_compose_request`
- `POST /v1/presenter/compose-from-intent`

This is the main proof burden of Phase 3.

The successful trace artifact must explicitly isolate the reopen segment.
Do not make the reviewer infer reopen behavior from one undifferentiated session trace.

### 5. One exact saved-payload fidelity check

The closeout must verify that reopen is serving the exact saved lifecycle truth.

At minimum, the proof should compare or record:

- `session_id`
- `workflow_key`
- `consumer_key`
- `presentation_hash`
- `presentation_content_hash`
- `resolver_version`

The reopened surface should match the saved compose session record, not merely “look similar.”

## Must not widen

- do not jump to Phase 4 governance/evaluation in this slice
- do not reopen lifecycle schema design unless the live proof exposes a real blocker
- do not add publish/share semantics
- do not add auto-save
- do not add new transient consumer registration
- do not turn `planning_decision_id` into fake lifecycle identity
- do not move the closeout burden onto the AOI source-backed proxy path by default

## Required evidence shape

Minimum artifact set for honest closeout:

- one trace JSON for the successful live chain
- one rendered screenshot or equivalent rendered-state artifact after reopen
- one HAR for the browser session
- one saved-session payload artifact showing returned `session_id` and fidelity fields
- one invalid-session negative proof artifact
- one explicit reopen-segment request table or equivalent HAR extract that covers only the `?session_id=<id>` portion of the run

The evidence must make these points inspectable:

- save happened explicitly
- `session_id` was analyzer-generated and returned by save
- reopen used `session_id`
- reopen rendered saved truth
- reopen did not replay planner/composition calls

The reopen-segment artifact must show:

- one `GET /v1/presenter/compose-sessions/{session_id}` on reopen
- zero reopen-segment calls to:
  - `route-task`
  - `plan-task`
  - `planning_decision_fetch`
  - `planning_decision_compose_request`
  - `POST /v1/presenter/compose-from-intent`

## Acceptance bar

Phase 3 can close honestly only if the closeout shows all of the following:

1. one real non-AOI transient surface was composed on the existing proof page
2. that surface was explicitly saved into analyzer-owned lifecycle truth
3. the page successfully reopened by `session_id`
4. reopen rendered the saved surface without planner/composition replay
5. invalid `session_id` failed closed

If any one of those is missing, do not mark Phase 3 closed.
Write a bounded revision memo instead.

## Next step after successful closeout

Only after this closeout exists should the main line move to Phase 4:

- governance, review, and evaluation infrastructure

At that point the platform will have, in order:

- a bounded AOI exemplar closeout
- a generalized planner-to-presentation bridge
- a stronger host-neutral transient proof
- one explicit save/reopen lifecycle path

That is the minimum honest substrate for Phase 4 governance work.
