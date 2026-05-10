# Report: Phase 1B Host Ownership And Contract Unification Scope Audit

Verdict: `Approve with revisions`

## Findings

### High: the memo under-inventories the live task-launch contract story

The memo is correct that the current story is split across Host Contract v1/runtime, `taskLaunchRuntime`, page-local AOI launch code, and host proxy identity resolution (`communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_scope.md:50-140`).

But the live code also has a backend task-launch consumer that the memo does not name:

- `the-critic/api/server.py` already implements task-planned genealogy by calling `route-task`, syncing registered-corpus documents, calling `plan-task`, validating the returned followup contract, and only then launching `/v1/executor/jobs` (`/home/evgeny/projects/the-critic/api/server.py:18311-18386`)
- the Stage 8/9 completion memo explicitly records that backend seam as landed current-consumer behavior (`communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md:26-39`)

So the current contract story is not only:

- frontend `taskLaunchRuntime`
- AOI page-local launch code

It is also:

- backend host interpretation of planner contracts for genealogy launch

Required revision:

- add the task-planned genealogy server path to the Phase 1B current-state inventory
- make the ownership decision on task-launch contract interpretation cover both frontend and backend host consumers

### High: the memo is right to reject `taskLaunchRuntime` as a floating sidecar, but “absorb route-task/plan-task as first-class Host Contract v2 families” risks collapsing distinct layers

The memo’s direction is correct:

- `route-task` and `plan-task` should not remain an unbounded parallel contract (`communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_scope.md:257-268`)

But the code shows these seams are not ordinary delivery families today:

- `taskLaunchRuntime.ts` is only the typed client for `POST /v1/orchestrator/route-task` and `POST /v1/orchestrator/plan-task` (`/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:154-189`)
- `task_router.py` returns advisory launch contracts that still point the host at planning or execution endpoints rather than directly delivering results (`src/orchestrator/task_router.py:398-458`)
- `task_planner.py` then returns `downstream_followup_contract` that maps onto `/v1/presenter/compose-from-selection` or `/v1/executor/jobs` (`src/orchestrator/task_planner.py:392-409`, `src/orchestrator/task_planner.py:553-577`)

The earlier Stage 8/9 scope was clearer here:

- keep Host Contract v1 stable
- layer one bounded task-launch contract on top
- chain that layer into existing host/runtime families (`communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_scope.md:203-235`)

Required revision:

- keep the “one authoritative analyzer-to-host contract story” idea
- but define at least two explicit layers inside it:
- planner-advisory / task-launch law
- delivery / run-result-readiness / transient launch law

The memo’s “planner-advisory subcluster” option is technically sound.
The “just absorb them as ordinary families” option is too blurry unless the memo explicitly preserves layer distinction.

### Medium: navigation and launch handoff are correctly identified, but the memo should explicitly include reload and persistence semantics

The memo is right that navigation and launch handoff remain host-owned (`communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_scope.md:237-255`).

The live AOI path shows why this is more than URL construction:

- `AoiV2ThematicPanel` passes planner-selected sources, blocked profiles, and resolved intent seed through `navigate(..., { state })` (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:701-717`)
- `AoiComposeFromIntentPage` decides planner-backed versus profile-backed behavior from `location.state` plus URL params (`/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:229-260`, `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:414-449`)
- the profile autostart path is URL-driven and deliberately drops `source_v2_job_id` on autostart (`/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:452-484`)

That means reload/deep-link behavior is already semantically important:

- planner-backed selection state is ephemeral
- legacy profile-backed autostart is durable in the URL

Required revision:

- Phase 1B should explicitly decide what must survive reload, deep-link, or share
- and what is allowed to remain ephemeral browser navigation state

### Medium: the memo’s canonical identity versus continuity-alias framing is technically coherent, but the doctrine should be stated more firmly

The live code already supports the memo’s basic framing:

- `source_backed_transient_launch` records `canonical_identity = upstream_v2_job_id` and treats `source_analysis_id` / `source_v2_job_id` as optional continuity selectors (`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:215-230`)
- `_resolve_source_backed_compose_identity(...)` resolves alias to canonical upstream identity, validates project + thinker scope, and can return the local continuity alias for reuse (`/home/evgeny/projects/the-critic/api/server.py:19192-19298`)
- analyzer-facing compose requests only accept `source_v2_job_id`, not `source_analysis_id` (`src/presenter/schemas.py:658-679`; `src/presenter/compose_from_intent.py:533-562`)

So the technically coherent reading is:

- analyzer boundary: canonical-id-first now
- host boundary: dual threading exists operationally
- `source_analysis_id` is continuity support, not equal upstream truth

Required revision:

- state explicitly that `source_v2_job_id` is already the canonical analyzer boundary
- treat the open question as whether the product boundary should continue to thread both ids for host continuity, not whether analyzer-v2 should accept equal dual truth

## Explicit Answers

1. Is the memo correct that the current contract story is split across:
   - Host Contract v1 / hostContractRuntime
   - `taskLaunchRuntime`
   - page-local launch and navigation code
   - host proxy identity resolution?

Yes, mostly.

Verified code paths:

- Host Contract v1 families, readiness capabilities, and host-surface rules live in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:6-18` and `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:87-314`
- runtime dispatch checks, input validation, consumer-key handling, readiness lookup, and surface-family lookup live in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts:53-190` and `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts:213-233`
- `taskLaunchRuntime` is the typed frontend client for `route-task` and `plan-task` in `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:154-189`
- AOI page-local launch/navigation law lives in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:573-810` and `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:229-484`
- host proxy identity resolution lives in `/home/evgeny/projects/the-critic/api/server.py:19192-19298`

Revision needed:

- add the backend task-planned genealogy path as another live task-launch contract consumer (`/home/evgeny/projects/the-critic/api/server.py:18311-18386`)

2. Does the memo correctly identify the four ownership decisions that Phase 1B must settle?

Yes.

Those four decisions align with the fixed-direction roadmap’s own definition of Phase 1B:

- source identity translation
- warm-snapshot / continuity-alias behavior
- surface selection
- navigation / launch-handoff semantics
- plus the separate decision on the relation of `taskLaunchRuntime` to the host contract story (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:206-220`)

3. Is the memo’s treatment of canonical identity versus host continuity alias technically coherent?

Yes, with the clarification above.

The current code supports:

- canonical upstream identity at the analyzer boundary
- host-local continuity alias at the product boundary

The memo becomes fully coherent if it names that asymmetry explicitly instead of leaving “alias-first / canonical-id-first / permanently dual-identity” equally open.

4. Is the proposed relation between `taskLaunchRuntime` and Host Contract v2 sound, or does it blur distinct layers incorrectly?

Partly sound.

It is sound to bring `route-task` and `plan-task` inside one authoritative contract story.
It is not sound to flatten them into ordinary delivery families without preserving their advisory and followup-contract role.

Best technical reading:

- one authoritative contract suite
- distinct planner-advisory subcluster
- explicit mapping from planner followup contracts onto delivery/runtime families

5. Is anything in the memo contradicted by the code?

No material claim is flatly contradicted.

The main issues are:

- omission of the backend genealogy task-launch consumer
- ambiguity about contract layering

6. Is anything important missing that would make the Phase 1B decision under-specified?

Yes.

Missing items:

- the already-live backend genealogy task-planned consumer
- explicit reload / deep-link / share semantics for planner-backed AOI handoff state
- explicit ownership of who interprets `downstream_followup_contract` and maps it to host navigation or executor launch

7. Is this scope narrow enough to be executable as a decision slice, rather than turning back into a broad roadmap?

Yes.

The memo is decision-only, explicitly forbids widening, and matches the approved phase order after Phase 0 closure (`communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md:150-170`; `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:164-220`).

With the revisions above, it remains a real decision slice rather than another broad strategy memo.

## Concrete Code-Path Verification

- The memo is correct that Host Contract v1 is a real typed artifact with 11 families, ownership labels, canonical identity fields, readiness capability tables, and host-surface selection rules (`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:6-18`, `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:87-314`).
- The memo is correct that `hostContractRuntime.ts` uses that artifact for dispatch checks, required-input validation, consumer-key threading, readiness lookup, and surface-family lookup (`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts:53-190`).
- The memo is correct that `taskLaunchRuntime.ts` dispatches via `dispatchAnalyzerApiRequest(...)` instead of through host-contract family definitions (`/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:1`, `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:154-189`).
- The memo is correct that the AOI planner-primary path still mixes host-owned and analyzer-owned law. The AOI panel owns row pinning, readiness timing, warmup timing, routing/planning submission, navigation, and planner metadata threading (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:546-571`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:573-810`).
- The memo is correct that `AoiComposeFromIntentPage.tsx` owns URL/search-param parsing, planner-vs-profile branching, and the call into `composeFromSource(...)` or `composeFromSelection(...)` (`/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:229-260`, `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:368-449`).
- The memo is correct that source identity and continuity alias behavior are materially host-owned today through `_resolve_source_backed_compose_identity(...)` (`/home/evgeny/projects/the-critic/api/server.py:19192-19298`).
- The memo is correct that analyzer transient compose remains AOI-bound and `the-critic`-bound. `compose_from_intent.py` hard-validates both `workflow_key` and `consumer_key` across transient entrypoints (`src/presenter/compose_from_intent.py:496-562`).

## Judgment On Program Sequence

This is the right next step in the larger sequence.

Why:

- the Phase 0 closeout explicitly says the main line should now move to Phase 1 beginning with Phase 1B (`communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md:167-170`)
- the fixed-direction roadmap defines Phase 1B exactly as host ownership decisions and contract unification before Phase 1A generalization (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:206-220`)
- the master roadmap still targets thin hosts with minimal stable obligations, not workflow-specific analytical controllers (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:43-68`)

So the memo is solving the correct next problem:

- not more AOI-local repair
- not premature lifecycle work
- not fake genericization by simply weakening validators

## Required Revisions

1. Add the backend task-planned genealogy path to the Phase 1B current-state inventory and ownership matrix.
2. Reframe the `taskLaunchRuntime` question as a layered contract question:
   - planner-advisory contract
   - delivery/runtime contract
3. Add one explicit decision or invariant on reload/deep-link/share durability for planner-backed AOI handoff state.
4. Tighten the identity doctrine so `source_v2_job_id` is named as canonical analyzer truth now, while `source_analysis_id` is framed as host continuity support unless the product boundary deliberately preserves dual threading.
5. In the deliverable shape, add either:
   - one backend task-launch call graph
   - or one explicit statement explaining why that already-live consumer is excluded

With those revisions, the memo is solid enough to guide later Phase 1A implementation planning without re-opening the boundary questions mid-implementation.
