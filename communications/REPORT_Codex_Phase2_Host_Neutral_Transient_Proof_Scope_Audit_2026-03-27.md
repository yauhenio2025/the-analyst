# Report: Phase 2 Host-Neutral Transient Proof Scope Audit

Verdict: `Approve with revisions`

## Findings

### High: the memo identifies the right remaining gap, but it understates that the only honest lowering path is still analyzer-side, not host-consumable runtime law

The memo is correct that Phase 1 bridge work is no longer the main missing seam. The current live code already has:

- bounded genealogy saved-result routing to `planner.direct_sections_compose_handoff` in `src/orchestrator/task_router.py:397-469`
- a real `direct_sections_composition_handoff_plan` in `src/orchestrator/task_planner.py:410-487`
- immutable planning snapshot round-trip in `src/orchestrator/planning_decision_store.py:26-120` and `src/api/routes/orchestrator.py:326-356`
- analyzer-side fail-closed lowering in `src/orchestrator/direct_sections_compose_harness.py:17-79`

But that last point is the important one: the only honest lowering helper currently lives in Python inside analyzer-v2. The current host runtime only:

- fetches the persisted planning snapshot in `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:264-279`
- types the new handoff shape in `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:140-196`

It does not have a shared browser/runtime lowering helper for `direct_sections_composition_handoff_plan`, and the planner followup contract still contains a placeholder rather than a dispatchable payload:

- `prose_sections: "<lower from direct_sections_composition_handoff_plan>"` in `src/orchestrator/task_planner.py:460-469`

That means a real transient proof harness cannot yet honestly perform:

1. fetch planning snapshot
2. lower
3. call `POST /v1/presenter/compose-from-intent`

without either:

- duplicating analyzer-side lowering logic in the host, or
- getting a new analyzer-owned lowering surface / materialized lowerable payload

Required revision:

- make the lowering boundary explicit in the memo
- choose one bounded implementation rule up front:
  - either add an analyzer-owned lowerable transient handoff surface
  - or add one shared host/runtime lowering helper whose logic is explicitly limited to lossless contract lowering and not workflow-specific reconstruction
- state that if the browser proof would require reimplementing analyzer semantic validation locally, stop and revise

### High: “minimal dedicated host-neutral transient proof harness” is directionally right, but the current code suggests the bounded default is a dedicated proof surface reusing the-critic runtime, not a new transient consumer by implication

The memo is right not to treat `aoi-canary` as already answering the transient question. The live canary code is still result-backed only:

- it calls only result discovery / manifest / presentation in `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts:45-99`
- its live fetch loop is discovery -> manifest -> presentation in `/home/evgeny/projects/aoi-canary/src/App.tsx:524-667`
- it contains no `route-task`, `plan-task`, `planning_decision_id`, or transient compose runtime at all

By contrast, the only mature host runtime for planner and transient consumption is still in `the-critic`:

- Host Contract v2 runtime law in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts:24-223`
- planner runtime in `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:214-279`
- transient compose dispatch in `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts:20-140`

There is also still a hard transient consumer binding today:

- `compose-from-intent` only accepts registered consumer adapters, and the registry currently contains only `the-critic` in `src/presenter/compose_from_intent.py:54-58` and `src/presenter/compose_from_intent.py:528-545`
- the host runtime treats transient families as `consumer_key='the-critic'` structural constants in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:186-229` and `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts:127-145`

So the memo should not leave readers with the impression that the bounded Phase 2 default is “new transient second consumer.” The code does not support that as the narrowest next move.

Required revision:

- clarify that the proof target is “outside the current AOI page/controller path,” not necessarily “new transient consumer identity”
- state explicitly that the bounded default may be a dedicated proof surface that reuses the existing Host Contract v2 / planner runtime already living in `the-critic`
- state explicitly that expanding transient consumer registration beyond `the-critic` is out of scope unless separately justified

### Medium: the genealogy saved-result target is the right first transient seam, and the memo is right to keep the proof off AOI proxy routes and `/v1/executor/jobs`

This part of the memo is supported by the live code.

Why genealogy saved-result is the right first target:

- it exercises the newly generalized non-AOI planner path in `src/orchestrator/task_router.py:397-469` and `src/orchestrator/task_planner.py:410-487`
- it uses the thin public presenter surface `ComposeFromIntentRequest` in `src/presenter/schemas.py:613-622`
- it avoids re-proving the AOI-only proxy/alias path in `/home/evgeny/projects/the-critic/api/server.py:19192-19280` and `/home/evgeny/projects/the-critic/api/server.py:21452-21575`

Why the other obvious seams are worse:

- AOI proxy-backed transient proof would mostly re-prove the already-browser-exercisable AOI route that still depends on host proxy identity resolution and `the-critic`-specific transient dispatch
- genealogy `registered_corpus` task planning is still explicitly execution-only and hard-fails unless planning ends at `/v1/executor/jobs` in `/home/evgeny/projects/the-critic/api/server.py:18356-18375`

This supports the memo’s claim that the proof can and should stay off:

- `the-critic` AOI proxy routes
- `/v1/executor/jobs`
- host-local section extraction

The remaining caveat is the lowering point described above, not the choice of genealogy as the target.

### Medium: the memo is honest about `aoi-canary`, and should stay stricter about optional token/session borrow

The memo’s `aoi-canary` claim is accurate:

- `aoi-canary` is a real second-consumer proof for result-backed analyzer-native result contracts
- it is not a transient planner-to-presentation consumer
- the Stage 13 Tier A completion memo says exactly that in `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md:181-197`

The optional ephemeral token / session borrow is also correctly framed as dangerous. The current code paths give no evidence that such a token is needed for the target chain:

- route-task / plan-task / planning-decision-fetch are identity-based, not session-based
- the current direct-sections proof chain is keyed by `planning_decision_id` and `source_v2_job_id`, not transient session state

Required revision:

- strengthen the memo from “may be introduced early here” to “only after proving that `planning_decision_id` + current request identity are insufficient for the chosen proof surface”
- state explicitly that no token/session construct should be introduced to compensate for an unclear lowering boundary

## Explicit Answers

1. Is the memo correct that the remaining program gap is now stronger host-neutral transient proof rather than more Phase 1 bridge work?

Yes, mostly.

The live code and Phase 1 completion trail support that the core bridge substrate now exists:

- shared transient handoff executor in `src/presenter/compose_from_intent.py:145-157`
- non-AOI planner outcome in `src/orchestrator/task_planning_schemas.py:30-46` and `src/orchestrator/task_planner.py:448-487`
- immutable planning snapshots in `src/orchestrator/planning_decision_store.py:26-120`

The main remaining gap is now proof consumption beyond the current AOI page/controller path, not more router/planner widening. The one important caveat is that host-consumable lowering is not yet solved as runtime law.

2. Is a minimal dedicated proof harness really the right default vehicle, or does the current codebase suggest a better bounded option?

Yes, a dedicated proof harness is the right category.

But the current code suggests the best bounded implementation is a dedicated proof surface that reuses the existing runtime already in `the-critic`, not extension of `aoi-canary` and not a brand-new transient app by default.

Reason:

- `aoi-canary` has no planner/transient runtime at all
- `the-critic` already has Host Contract v2, `taskLaunchRuntime`, transient compose dispatch, and generic rendering
- transient consumer registration is still structurally tied to `the-critic`

3. Is the memo right to target genealogy `saved_result` transient proof first rather than AOI proxy-backed transient proof or another execution-oriented genealogy seam?

Yes.

That is the cleanest bounded seam because it proves the new non-AOI planner path directly, avoids AOI proxy-specific identity semantics, and avoids the executor-oriented genealogy branch that still terminates at `/v1/executor/jobs`.

4. Does the current code support the memo’s claim that the proof can stay off:

- `the-critic` AOI proxy routes
- `/v1/executor/jobs`
- host-local section synthesis?

Yes for the first two, and mostly yes for the third.

Supported:

- direct analyzer planner chain exists for genealogy saved-result in `src/orchestrator/task_router.py:397-469`, `src/orchestrator/task_planner.py:410-487`, and `src/api/routes/orchestrator.py:326-356`
- analyzer-side section extraction is upstream in `src/orchestrator/genealogy_saved_result_bridge.py:53-148`
- genealogy task-planned executor launch remains separate and execution-only in `/home/evgeny/projects/the-critic/api/server.py:18356-18375`

Caveat:

- host-local section extraction is not required
- but host/browser-side honest lowering is not yet provided as shared runtime law

5. Is the memo honest about what `aoi-canary` already proves and what it does not?

Yes.

Both the canary code and its completion memo show result-backed second-consumer proof only, not transient planner-backed proof.

6. Is anything in the memo contradicted by the code?

No major strategic claim is contradicted.

The main issue is under-specification:

- the memo talks as if a real proof harness can simply fetch, lower, and compose
- the code shows that lowering is still analyzer-side only, and transient consumer identity is still structurally `the-critic`

7. Is anything important missing that would make the scope under-specified or unsafe to implement?

Yes.

Missing items:

- one explicit decision on where honest lowering lives for a real consumer proof
- one explicit rule that Phase 2 does not imply new transient consumer registration
- one explicit statement that the bounded default proof surface may reuse `the-critic` runtime law instead of creating a new app/runtime stack
- one stronger precondition on optional token/session borrow

8. Is the optional ephemeral token/session borrow properly bounded, or is it likely to blur Phase 2 into Phase 3 lifecycle work?

As written, it is directionally bounded, but still too permissive.

The current code does not show a need for such a token. So the memo should bias more strongly against introducing one unless a concrete proof blocker is demonstrated first.

9. Is this scope narrow enough to stay Phase 2 rather than drifting into productization, another contract rewrite, or lifecycle design?

Yes, with the revisions above.

The memo stays properly away from:

- reopening Phase 1 router/planner generalization
- reopening Phase 1B ownership doctrine
- executor/jobs genealogy launch work
- polished app productization
- full lifecycle/session design

## Concrete Code-Path Verification

- Phase 1C non-AOI planner path is real:
  - `src/orchestrator/task_router.py:397-469`
  - `src/orchestrator/task_planner.py:410-487`
  - `src/orchestrator/task_planning_schemas.py:198-258`
- Persisted planning snapshot support is real:
  - `src/orchestrator/planning_decision_store.py:26-120`
  - `src/api/routes/orchestrator.py:346-356`
- The current honest genealogy proof is still analyzer-side:
  - `src/orchestrator/direct_sections_compose_harness.py:17-79`
  - `tests/test_phase1c_genealogy_direct_sections.py:50-173`
- The shared transient presenter path is reusable for genealogy `direct_sections`, but still enforces registered transient consumer adapters:
  - `src/presenter/compose_from_intent.py:145-158`
  - `src/presenter/compose_from_intent.py:521-545`
- Host Contract v2 and planner runtime already exist in the current consumer:
  - `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts:24-223`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:214-279`
- The current browser-exercisable transient path is still AOI-proxy-bound:
  - `/home/evgeny/projects/the-critic/api/server.py:19192-19280`
  - `/home/evgeny/projects/the-critic/api/server.py:21452-21575`
- The current host-side genealogy task-planned path is still execution-only:
  - `/home/evgeny/projects/the-critic/api/server.py:18356-18375`
- `aoi-canary` remains result-backed only:
  - `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts:45-99`
  - `/home/evgeny/projects/aoi-canary/src/App.tsx:524-667`

## Judgment On Program Sequence

This is the right next step in the larger program sequence.

The roadmap and completion trail now line up cleanly:

- Phase 0 closed the AOI exemplar honestly
- Phase 1B locked ownership and Host Contract v2 doctrine
- Phase 1A unified the planner/runtime story and durable AOI recovery
- Phase 1C added one bounded non-AOI planner-to-presentation path

So the next honest question is no longer “can the bridge exist?” It is “can a non-current-AOI proof surface consume it without rebuilding analytical intelligence locally?”

That is exactly the Phase 2 question the memo is trying to frame.

## Required Revisions

1. Add one explicit lowering-boundary decision.
   - State where the real consumer proof gets its honest lowered `ComposeFromIntentRequest`.
   - Fail closed if that would require duplicating analyzer semantic validation locally.

2. Clarify the proof vehicle.
   - Say that the bounded default is a dedicated proof surface outside the current AOI page/controller path.
   - Explicitly allow that surface to reuse the existing Host Contract v2 / planner runtime already living in `the-critic`.
   - Explicitly say that a new transient consumer identity is not required by default.

3. Tighten the transient-consumer boundary.
   - Note that transient presenter consumption is still registered only for `the-critic`.
   - If changing that becomes necessary, treat it as separate scope rather than hidden Phase 2 glue.

4. Tighten the optional token/session clause.
   - Require proof that `planning_decision_id` plus current request identity are insufficient before introducing any ephemeral token or session identifier.
   - State that such a token may not be used to mask an unresolved lowering or host-runtime boundary.

With those revisions, the memo is solid and in the right sequence position.
