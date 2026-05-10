# Report: Phase 3 Bounded Lifecycle V1 Live Proof Closeout Scope Audit

Date: 2026-03-28
Audited memo: `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md`

## Verdict

Approve with revisions

The memo is strategically right and mostly code-backed. After the bounded Phase 3 implementation landed, the honest next step is one live `compose -> save -> reopen` closeout on the existing genealogy proof page, not a jump to Phase 4 governance/evaluation.

The live code supports the core claim that save/reopen now exists:

- file-backed analyzer-owned `compose_session` persistence in `src/presenter/compose_session_store.py:19-76`
- explicit presenter save/fetch routes in `src/api/routes/presenter.py:479-530`
- Host Contract v2 lifecycle families keyed by `session_id` in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts:147-173`
- client save/fetch helpers in `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts:85-167`
- proof-page reopen mode that clears prior transient/planner state and fetches only the saved session in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:60-98`

But the memo still needs tightening in three places:

1. it overstates the negative case by including missing `session_id`
2. its evidence shape is slightly under-specified for proving no recomputation on reopen
3. its preflight bar should be tied to captured run-detail fields because the current page does not enforce all of them automatically

## Findings

### 1. Medium: “missing `session_id`” is contradicted by the current proof page behavior

The memo says the closeout must record an explicit negative case for “invalid or missing `session_id`” and that reopen should fail closed with a visible error at `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md:157-169`.

That is only true for an invalid concrete `session_id`, not for a missing one.

Live code:

- when no `session_id` is present, the page exits reopen mode immediately and stays in normal compose mode in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:60-64`
- fail-closed behavior happens only when a concrete `session_id` is supplied and `getComposeSession(...)` fails in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:78-90`
- the fetch route itself can only fail on an actual path parameter, not a missing one, in `src/api/routes/presenter.py:507-530`
- the focused frontend test covers invalid-session failure and explicitly asserts no fallback recomputation in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.test.tsx:283-293`

Required revision:

- change the negative case from “invalid or missing `session_id`” to “invalid, unknown, or consumer-mismatched `session_id` in reopen mode”
- keep the acceptance bar on fail-closed invalid reopen, not on the normal no-query-param compose entry

### 2. Medium: the evidence shape is close, but still under-specifies how to prove “no recomputation on reopen”

The memo’s artifact set at `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md:210-226` is directionally right:

- trace JSON
- screenshot after reopen
- HAR
- saved-session payload artifact
- invalid-session artifact

That can prove the claim, but only if the reopen segment is isolated clearly enough.

Why this matters in code:

- saved lifecycle truth is the full `compose_request` plus full `compose_response`, not just hashes, in `src/presenter/schemas.py:737-759`
- the save store persists that exact payload and duplicates fidelity fields in `src/presenter/compose_session_store.py:44-60`
- reopen mode fetches that session by `session_id` and renders `savedSession.compose_response`, while clearing all prior routing/planning/compose state in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:67-90`, with the saved response taking precedence at `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:210` and rendering through the shell at `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:349`
- the frontend tests assert that reopen mode does not call `routeTask`, `planTask`, `getPlanningDecision`, `getPlanningDecisionComposeRequest`, or `composeFromIntent` in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.test.tsx:266-281`

A screenshot plus a generic HAR is not quite enough unless the reviewer can see which requests happened before save and which happened after reopen.

Required revision:

- require the successful trace JSON or a companion artifact to explicitly mark the reopen segment
- require the fetched saved-session payload from reopen, or an equivalent exact persisted-session record, not just the save response
- require either an annotated HAR extract or a short request table showing that after `?session_id=<id>` the browser made `GET /v1/presenter/compose-sessions/{session_id}` and did not make:
  - `route-task`
  - `plan-task`
  - `planning_decision_fetch`
  - `planning_decision_compose_request`
  - `POST /v1/presenter/compose-from-intent`

### 3. Low: the preflight bar is right, but the memo should state that the artifact must record those fields explicitly

The memo correctly requires preflight confirmation of:

- `workflow_key = intellectual_genealogy`
- `status = completed`
- `result_state = ready`
- `presentation_status = completed`
- `restore_available = true`

at `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md:121-137`.

The current page does not enforce that full set automatically:

- it checks `workflow_key` and `status === completed` before continuing in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:125-135`
- the run-detail client type does expose `result_state`, `restore_available`, and `presentation_status` in `/home/evgeny/projects/the-critic/webapp/src/types/boundedV2.ts:14-35`
- `getBoundedV2Run(...)` returns those fields from the analyzer run detail in `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:108-120`

So the memo is not contradicted, but the proof remains under-specified unless the trace/preflight artifact explicitly records those three additional fields.

Required revision:

- say that the preflight artifact must capture and retain the run-detail values for `result_state`, `presentation_status`, and `restore_available`, because the current proof page does not itself block on them

## Code-Path Verification

### Q1. Is a bounded Phase 3 live proof closeout now the right next step instead of Phase 4 governance/evaluation?

Yes.

The sequencing is consistent across the active roadmap trail:

- the fixed roadmap says Phase 3 is not closed until one bounded lifecycle path is live-proved, and Phase 4 governance comes after that in `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:291-326` and `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:361-420`
- the Phase 3 implementation completion memo says the next honest step is still inside Phase 3 and explicitly says not to jump to governance yet in `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_implementation_completion.md:33-45` and `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_implementation_completion.md:172-203`
- repo search under `communications/` found the scope memo and review prompts for this Phase 3 closeout, but no actual Phase 3 proof artifact set yet

Older documents do not override this:

- `communications/PLAN_Stage3_Lifecycle_Authority.md` is about result-restore authority and Critic snapshot simplification, not transient compose sessions
- `communications/MEMO_2026-03-19_phase4_cross_workflow_workspace_scope.md` is an older superseded governance/workspace line that the current memo already labels as non-active

### Q2. Is the memo right to keep the closeout on the existing genealogy proof page and generic direct-sections transient substrate?

Yes.

This is where the lifecycle slice was actually implemented:

- the proof page owns the save/reopen UX in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:100-207`
- the page’s active compose chain is still the generic direct-sections path:
  - `routeTask(...)`
  - `planTask(...persist_decision: true)`
  - `getPlanningDecision(...)`
  - `getPlanningDecisionComposeRequest(...)`
  - `composeFromIntent(...)`
  in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:137-179`
- the lifecycle helpers are analyzer-direct and generic in `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts:85-167`
- Host Contract v2 attaches the lifecycle families to `genealogy_result_backed_workspace_experience` in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts:213-225`

That is a cleaner first lifecycle substrate than the AOI proxy stack because the closeout stays on `compose-from-intent` plus persisted session truth, not on host aliasing or source-backed compose proxies.

### Q3. Does the code support the claim that save/reopen is implemented but not yet live-proved?

Yes.

Implemented in code:

- analyzer-generated `session_id` in `src/presenter/compose_session_store.py:26-27`
- file-backed persistence of exact request/response truth in `src/presenter/compose_session_store.py:30-62`
- save/fetch routes in `src/api/routes/presenter.py:479-530`
- persisted session schema in `src/presenter/schemas.py:746-759`
- proof-page reopen mode in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:60-98`

Focused verification exists:

- `tests/test_compose_sessions.py:54-176`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.test.tsx:237-293`

I also ran the focused test slices:

- `PYTHONPATH=. pytest -q tests/test_compose_sessions.py -q` -> `5 passed`
- `CI=true npm test -- --runInBand --watchAll=false src/lib/composeFromIntentClient.test.ts src/pages/GenealogyTransientProofPage.test.tsx` -> `8 passed`

But there is still no Phase 3 live proof artifact set in `communications/`, so “implemented but not yet live-proved” is the honest current state.

### Q4. Is the memo right that `session_id`, not `planning_decision_id`, is the truthful lifecycle identity?

Yes.

`planning_decision_id` is persisted planner truth, not saved presentation truth:

- planning snapshot ids are generated in `src/orchestrator/planning_decision_store.py:22-57`
- the persisted planning snapshot schema stores task/routing/planning data, not compose-session payloads, in `src/orchestrator/task_planning_schemas.py:246-258`
- the planning-decision compose-request route only lowers that snapshot back into a thin `ComposeFromIntentRequest` in `src/api/routes/orchestrator.py:364-394`

By contrast, `session_id` identifies the saved lifecycle object that includes the final compose response:

- `PersistedComposeSession` carries `session_id`, fidelity fields, `compose_request`, and `compose_response` in `src/presenter/schemas.py:746-759`
- the fetch route is keyed by `session_id` in `src/api/routes/presenter.py:507-530`
- Host Contract v2 names `session_id` as the canonical identity for `transient_compose_session_fetch` in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts:160-173`

So `planning_decision_id` remains provenance and reload identity for planner snapshots, but it cannot truthfully substitute for saved lifecycle identity.

### Q5. Does the memo’s required evidence shape prove “no recomputation on reopen”?

Mostly, but not quite as written.

The proposed evidence shape is pointed in the right direction, but it needs one more explicit requirement:

- the reopen segment must be isolated clearly enough to show which requests happened after `?session_id=<id>`
- the fetched saved-session payload, or equivalent exact saved-session record used on reopen, must be captured

Without that, the reviewer can inspect the HAR, but the proof remains too dependent on manual inference.

### Q6. Is the memo honest about what remains out of scope?

Yes.

The live code still reflects those boundaries:

- no publish/share semantics in the saved-session schema or routes
- no auto-save, because save is an explicit user action on the proof page in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:187-207`
- no new transient consumer registration; the transient consumer registry is still only `the-critic` in `src/presenter/compose_from_intent.py:158`
- host runtime still preserves the existing transient consumer constraint in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts:127-145`

So the memo is honest that governance/evaluation, new consumer registration, publish/share, and AOI lifecycle widening are still out of scope.

### Q7. Is anything in the memo contradicted by the code?

Yes, one point:

- “missing `session_id`” is not a fail-closed negative reopen case on the existing page

Everything else material is directionally supported by the code.

### Q8. Is anything important missing that would make the closeout under-specified or unsafe?

Yes, two practical clarifications are still needed:

1. the negative case should be defined around an invalid concrete reopen identity, not a missing query param
2. the evidence instructions should require an explicit reopen network/fetch proof, not just a generic HAR plus screenshot

Those are revision-level issues, not reasons to reject the slice.

## Judgment On Program Sequence

This is the correct immediate next step.

The live program state now reads cleanly:

- Phase 1 bridge and ownership work is closed
- Phase 2 host-neutral transient proof is closed
- Phase 3 lifecycle implementation is landed but not documentary-closed
- therefore the next active slice is still one bounded Phase 3 live proof closeout, not Phase 4 governance

That sequence is supported by:

- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:316-326`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_implementation_completion.md:172-203`

Moving to governance/evaluation before this closeout would build review machinery on top of an unproved lifecycle claim.

## Required Revisions

1. Replace “invalid or missing `session_id`” with:
   - invalid, unknown, or consumer-mismatched `session_id` in reopen mode

2. Tighten the evidence shape so it explicitly requires:
   - the reopen fetch request by `session_id`
   - the fetched saved-session payload, or equivalent exact persisted-session record used on reopen
   - an annotated absence proof that no planner/composition endpoints ran after reopen

3. Add one sentence tying the preflight bar to captured artifact fields:
   - the recorded preflight artifact must include `result_state`, `presentation_status`, and `restore_available`, because the current page only hard-blocks on `workflow_key` and `status`

## Bottom Line

The memo is the right next-step memo for the current codebase. The implementation exists, the sequencing is correct, and the chosen proof surface is the right one.

The needed changes are precision revisions, not a change of direction. After those revisions, the memo is solid enough to execute as the Phase 3 closeout slice.
