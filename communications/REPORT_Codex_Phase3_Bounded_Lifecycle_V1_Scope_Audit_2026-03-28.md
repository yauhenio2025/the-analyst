# Report: Phase 3 Bounded Lifecycle V1 Scope Audit

Date: 2026-03-28
Audited memo: `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`

## Verdict

Approve with revisions

The memo identifies the correct next gap after the verified March 28 Phase 2 closeout: the program now lacks explicit lifecycle law for transient analytical surfaces, not more proof widening on the same transient bridge.

The main direction is sound:

- lifecycle is now the right next seam
- the generic direct-sections transient path is the right first substrate
- `planning_decision_id` is not sufficient lifecycle identity for truthful reopen
- the analyzer/host ownership split is aligned with current doctrine

But the memo should be tightened in a few places so the scope does not blur:

- transient lifecycle vs existing job/result restore
- planner snapshot identity vs lifecycle identity
- exact saved payload fidelity required for reopen-without-recomputation

## Findings

No high-severity contradictions found.

### 1. Medium: the memo overstates the negative claim about existing save/reopen objects

The live code does not contain any transient `session_id` object, transient compose save route, or reopen-by-session route. A repo-wide search across `analyzer-v2/src`, `the-critic/api`, and `the-critic/webapp/src` found no such transient lifecycle object.

But the broader codebase does already have reopenable saved-result surfaces:

- analyzer result restore by `job_id` through `GET /v1/results/by-job/{job_id}/presentation` with `restore_available` and `restore_reason` in `src/analysis_products/result_contract.py:246-271`, `src/analysis_products/result_contract.py:382-419`, and `src/api/routes/results.py:75-138`
- host-local saved AOI/genealogy snapshot rows keyed by `analysis_id`, with `_presentation` persisted into local DB records in `/home/evgeny/projects/the-critic/api/server.py:19528-19616` and warmed from analyzer-v2 through `/api/genealogy/cache-v2/{v2_job_id}` in `/home/evgeny/projects/the-critic/api/server.py:20892-20953`

So the memo is correct only if narrowed to:

- no existing first-class save/reopen object for transient compose surfaces

Without that revision, the memo reads more absolute than the code supports.

### 2. Medium: `planning_decision_id` is not enough for lifecycle identity, but it is not merely “internal”

The memo is right that `planning_decision_id` is not truthful lifecycle identity for a saved transient surface.

Why:

- `PersistedTaskPlanningDecision` stores planner truth, not saved presentation truth, in `src/orchestrator/task_planning_schemas.py:246-258`
- the lowering route only reconstructs a thin compose request from the planning snapshot in `src/api/routes/orchestrator.py:364-394` and `src/orchestrator/direct_sections_compose_harness.py:65-79`
- the genealogy proof page then calls `POST /v1/presenter/compose-from-intent` again after fetch/lower in `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:91-119`
- the AOI page likewise reloads the planning snapshot and then recomposes through the source-backed path in `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:381-395` and `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:534-574`

But the memo should not call `planning_decision_id` purely internal. It is already a host-visible canonical identity inside Host Contract v2 and URL/query semantics:

- `planning_decision_fetch` and `planning_decision_compose_request` both declare canonical identity `planning_decision_id` in `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts:116-143`
- the runtime fetch helpers use that id directly in `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:273-305`
- the AOI route carries `planning_decision_id` in query params in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:690-707`

Revision needed:

- describe `planning_decision_id` as planner snapshot identity or reload identity, not lifecycle identity

### 3. Medium: the memo should make saved-payload fidelity explicit, not just “enough provenance”

The memo is directionally honest that reopen without recomputation requires storing the final transient presentation payload, not just `planning_decision_id`.

That is supported by code:

- transient compose returns a non-job-backed payload only in memory in `src/presenter/compose_from_intent.py:503-518`
- `TransientIntentPagePresentation` contains hashes, resolver version, style school, and views, but no session identity or persistence fields in `src/presenter/schemas.py:708-734`
- view defs are marked `status="draft"` in `src/presenter/compose_from_intent.py:884-893` and `src/presenter/compose_from_intent.py:1183-1191`, which is presenter metadata, not a saved lifecycle object

The memo should therefore state explicitly that the saved lifecycle object must persist:

- the exact final transient response or exact final presentation snapshot
- its `presentation_hash`, `presentation_content_hash`, and `resolver_version`
- the original save-time request snapshot
- save timestamp and provenance links

Otherwise implementors could still fake “reopen” by replaying lower/compose off planning truth.

### 4. Low: retention is explicit enough for v1, but durability level should be named

The proposed rule:

- retain saved compose sessions indefinitely in v1

is sufficiently explicit for a bounded first slice.

But the memo should also say that indefinite retention means analyzer-persisted durable storage, not browser-only state and not host-local cache truth. That follows from the memo’s own ownership rule, but naming it would make implementation planning safer.

## Concrete Code-Path Verification

### Main claim: the next gap is lifecycle law, not more transient proof widening

Verified.

The roadmap trail now consistently places lifecycle after the bridge-proof work:

- the fixed roadmap says Phase 3 corresponds to Stage 14 lifecycle after Phase 2 bridge proof
- the Phase 2 completion memo explicitly names Phase 3 bounded lifecycle v1 as the next honest step
- the older Stage 14 draft in `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:330-358` deferred lifecycle until the bridge was stronger; Phase 1A/1B/1C plus March 28 Phase 2 now satisfy that prerequisite

The older March 16-17 lifecycle documents do not contradict this. They were about bounded run/result lifecycle authority and consumer simplification, not transient analytical surface sessions:

- `communications/PLAN_Stage3_Lifecycle_Authority.md`
- `communications/REPORT_Claude_Stage4_Run_Lifecycle_Authority_Critique.md`

### Main claim: the generic direct-sections path is the right first lifecycle substrate

Verified.

The generic genealogy proof path is materially thinner and more generalized:

- planner snapshot fetch and lowering are analyzer-direct in `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:273-305`
- generic direct transient compose goes straight to analyzer `POST /v1/presenter/compose-from-intent` in `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts:20-55`
- the proof route is a dedicated generic proof surface in `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:255-263` and `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:47-119`

The AOI source-backed path is still more host-shaped and proxy-shaped:

- AOI planner-backed launch still warms a host-local snapshot alias `analysis_id` in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:546-571`
- it navigates with host route/query semantics in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:690-707`
- the final compose call is still host-proxied `compose-from-selection`, not generic analyzer-direct `compose-from-intent`, in `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts:108-139`
- the host backend still resolves `source_analysis_id` alias to canonical `source_v2_job_id` in `/home/evgeny/projects/the-critic/api/server.py:19192-19260`

So the memo’s substrate choice is correct.

### Main claim: `planning_decision_id` is not enough to serve as truthful lifecycle identity

Verified.

It identifies immutable planner truth only:

- file-backed planning snapshot persistence in `src/orchestrator/planning_decision_store.py:26-58`
- persisted schema contains routing/planning/task truth but no saved compose response in `src/orchestrator/task_planning_schemas.py:246-258`

Current reopen behavior still recomputes:

- direct-sections “recovery” lowers snapshot into a fresh compose request and then recomposes
- AOI “recovery” fetches planner truth and then recomposes through selection/source-backed routes

So `planning_decision_id` can remain a provenance link, but not the saved surface identity.

### Main claim: there is no current transient save/reopen object

Substantively verified, with wording revision needed.

There is no transient `session_id`, no transient save route, no reopen-by-session route, and no transient compose persistence store in the inspected code paths. The transient response schema itself has no session field in `src/presenter/schemas.py:708-734`.

But existing job/result restore and local snapshot objects do exist, so the memo should name the narrower absence precisely.

### Main claim: the proposed ownership split matches Phase 1B doctrine

Verified.

Phase 1B doctrine says:

- analyzer owns routing/planning truth and followup-contract semantics
- host owns continuity aliasing, surface selection, navigation, URL law, and browser execution

The live AOI path still reflects that:

- host resolves/warms `source_analysis_id` continuity state in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:546-571`
- host owns route/query navigation in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:696-707`
- analyzer owns persisted planning truth and direct lowering in `src/api/routes/orchestrator.py:351-394`

So the memo’s split is consistent with current doctrine as long as the new lifecycle object is analyzer-owned truth and the host does not reconstruct it by replaying planning law.

### Main claim: the memo is honest about what must be stored to reopen without recomputation

Mostly verified.

The minimum honest requirement is indeed:

- save request snapshot
- save exact final response or presentation snapshot
- save provenance links

Because current recomposition depends on lower/compose replay, and there is no existing saved transient payload object.

## Judgment On Larger Program Sequence

This is the right next step in the larger sequence.

Why:

- Phase 1B locked the ownership doctrine
- Phase 1A/1C removed the AOI-only structural constraint and persisted planner truth
- March 28 Phase 2 proved the generalized transient substrate on a non-AOI browser surface
- the remaining gap is now what a kept dynamic surface is, not whether the bridge can produce another transient proof

Trying to widen transient proof again before lifecycle would mostly re-prove an already-proven seam.

The memo is also right not to start lifecycle on the AOI proxy path, because that would entangle first-pass lifecycle law with:

- host-local continuity aliasing
- source identity proxy resolution
- AOI-specific source-backed compose behavior

The generic direct-sections path is the cleaner place to define the first truthful save/reopen law.

## Required Revisions

1. Replace broad “no existing save/reopen object” wording with:
   - no existing first-class save/reopen object for transient compose surfaces
   - existing job-backed result restore and host-local snapshot objects remain separate and should not be conflated with the new lifecycle object

2. Replace “`planning_decision_id` is internal” with:
   - `planning_decision_id` is existing planner snapshot identity used for reload/deep-link recovery
   - it is not sufficient lifecycle identity for a saved transient surface

3. Make saved fidelity non-negotiable:
   - reopen must serve the exact saved transient response or exact saved presentation snapshot
   - not a replay from planning snapshot
   - not a fresh compose result that merely happens to be similar

4. Name the minimum saved fields more concretely:
   - `session_id`
   - `saved_at`
   - `workflow_key`
   - `consumer_key`
   - saved compose request snapshot
   - saved final response or saved final presentation snapshot including hashes and resolver version
   - provenance link fields such as `planning_decision_id` and `source_v2_job_id` where present

5. Add one explicit durability sentence:
   - v1 saved sessions must live in analyzer-owned durable storage
   - browser state and host-local cache do not count as lifecycle truth

## Bottom Line

The memo is strategically correct and code-backed enough to move forward.

After the March 28 Phase 2 proof, the next honest seam is lifecycle law for transient analytical surfaces. The chosen first substrate is right. The main revisions needed are precision revisions, not a change of direction.
