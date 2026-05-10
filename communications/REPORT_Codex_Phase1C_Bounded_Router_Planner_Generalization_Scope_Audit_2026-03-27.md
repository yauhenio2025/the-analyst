# Report: Phase 1C Bounded Router/Planner Generalization Scope Audit

Verdict: `Approve with revisions`

## Findings

### High: the memo is strategically correct, but it understates the presenter-contract follow-through required for a genuinely generic `direct_sections` planner outcome

The memo is right that the current remaining asymmetry is mostly at the router/planner layer, and it is also right that `compose-from-intent` now accepts `workflow_key=intellectual_genealogy` with `handoff_kind=direct_sections` (`src/presenter/compose_from_intent.py:141-154`, `tests/test_compose_from_intent.py:500-543`).

But the current public `compose-from-intent` contract is still much thinner than the memo’s proposed planner payload:

- `ComposeFromIntentRequest` only accepts `workflow_key`, `consumer_key`, `user_intent`, and bare `prose_sections[{engine_key,title,prose}]` (`src/presenter/schemas.py:605-621`)
- the richer planner metadata path in `compose_from_intent.py` is internal-only via `planning_sections`, not part of the public request shape (`src/presenter/compose_from_intent.py:612-637`)
- grouped mixed-content layouts still emit AOI-branded parent labels and descriptions (`"AOI Comparison"`, `"AOI Briefing"`) when both closeout and non-closeout sections are present (`src/presenter/compose_from_intent.py:640-672`)
- semantic-role assignment still depends on either AOI engine mappings or planner-style role hints/titles that the public `compose-from-intent` request cannot currently carry (`src/presenter/compose_from_intent.py:703-724`)

So the proposed generic handoff is only technically coherent if Phase 1C explicitly does one of these two things:

1. extend the public `compose-from-intent` boundary to accept planner-owned section metadata such as ordering / role hints / provenance, or
2. constrain the first genealogy proof so the returned `prose_sections` are already classifiable from bare `engine_key` and `title`, and avoid the AOI-branded grouped-parent branch.

Required revision:

- add one explicit presenter-boundary decision to the memo
- either authorize the bounded `compose-from-intent` request/schema follow-through needed for planner-owned metadata
- or explicitly constrain the first proof to the subset of `direct_sections` that the current bare request can consume honestly

### High: the analyzer and host planning contracts are still AOI-shaped, so “generic planner outcome” needs explicit schema/runtime follow-through in scope

The live code is still specialized around:

- `planning_outcome_kind = aoi_composition_handoff_plan` versus `genealogy_execution_plan` (`src/orchestrator/task_planning_schemas.py:26-40`)
- an AOI-only handoff payload model, `AoiCompositionHandoffPlan` (`src/orchestrator/task_planning_schemas.py:166-189`)
- AOI-only snapshot summary extraction in `planning_decision_store.py`, which pulls top-level metadata from `planning_decision.aoi_composition_handoff_plan` (`src/orchestrator/planning_decision_store.py:34-64`)
- AOI-shaped host typings in `taskLaunchRuntime.ts`, which only model `aoi_composition_handoff_plan` plus `genealogy_execution_plan` (`/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:8-18`, `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:92-163`)

The memo says the new outcome should be generic and should round-trip through immutable planning snapshots. That is correct directionally, but the current code means this is not just a router/planner `if` branch. It also requires bounded contract-shape work in:

- `src/orchestrator/task_planning_schemas.py`
- `src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`

Also note:

- Host Contract v2 already has a planner-advisory layer and `planning_decision_fetch`, but the genealogy result-backed surface currently only selects `task_route` and `task_plan`, not `planning_decision_fetch` (`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts:144-173`)

That does not mean the memo reopens Phase 1B. It does mean the memo should name the bounded contract/runtime follow-through explicitly, otherwise implementation planning will undercount the real work.

Required revision:

- add one explicit “must land” note that Phase 1C includes the bounded schema/runtime changes needed to represent, persist, and consume the new generic handoff outcome end to end

### Medium: the memo should make one executable adapter or harness mandatory, not merely permitted

The current non-AOI planner consumer is still execution-only:

- the backend genealogy proof path is hard-limited to task-planned `registered_corpus` execution and rejects any planning outcome other than `genealogy_execution_plan` (`/home/evgeny/projects/the-critic/api/server.py:18062-18080`, `/home/evgeny/projects/the-critic/api/server.py:18311-18386`)
- the Genealogy page exposes that same execution proof path as “Registered-corpus proof path: route-task, plan-task, then executor/jobs” (`/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1039-1050`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1465-1505`)

So there is no existing host-side genealogy consumer that can already execute a composition-facing planner result.

The memo’s acceptance criteria correctly require an executable non-AOI planner-to-presentation proof. But the “one thin executable adapter or harness may be added” wording is too soft. Without a named adapter/harness deliverable, this scope could still stop at:

- router accepts `saved_result`
- planner returns JSON
- no real consumer executes that JSON into `compose-from-intent`

Required revision:

- upgrade the thin adapter/harness from “may” to “must”
- name the execution boundary explicitly:
- either a focused analyzer integration harness
- or one thin current-host adapter
- but in either case it must execute the returned handoff contract into `compose-from-intent`

### Medium: targeting genealogy `saved_result` is the right seam, but the memo should make the data-thickness gate and section-budget limit more explicit

On strategy, the memo is right not to overload the existing `registered_corpus` launch path:

- current router and planner code treat genealogy `registered_corpus` / `inline_documents` as execution planning only (`src/orchestrator/task_router.py:172-224`, `src/orchestrator/task_planner.py:384-469`)
- the current host backend enforces that task-planned genealogy must terminate in `/v1/executor/jobs` (`/home/evgeny/projects/the-critic/api/server.py:18369-18375`)
- the Stage 8/9 completion memo records that seam as a bounded execution proof, not a composition path (`communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md:9-15`, `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md:26-39`, `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md:49-53`)

The saved-result target is also technically aligned with current identity law:

- saved-result summaries already carry canonical `v2_job_id` for genealogy results (`/home/evgeny/projects/the-critic/api/server.py:18693-18711`)

But the memo should sharpen two bounded constraints that matter in current code:

- `compose-from-intent` hard-caps `prose_sections` at 4 (`src/presenter/compose_from_intent.py:542-547`)
- the current codebase does not yet show a genealogy-specific saved-result section-materialization bridge analogous to AOI’s source bridge

The memo already gestures at “stop and write a revision memo instead” if saved-result truth is too thin. That is the right safety valve. It should be made more operational.

Required revision:

- state explicitly that the first genealogy saved-result proof must succeed with analyzer-owned result truth that can materialize at most 4 direct sections without re-running analysis and without host-local semantic reconstruction

## Explicit Answers

1. Is the memo correct that the remaining Phase 1 gap is now at the router/planner layer rather than another host-contract or AOI-local seam?

Mostly yes.

The roadmap trail and Phase 1A completion memo are aligned that the main remaining asymmetry is now router/planner-side, not another host-contract decision (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:221-239`, `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md:157-179`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1205-1208`).

But not literally yes in the narrowest sense:

- the shared presenter executor still has AOI-branded grouped-parent behavior and a public request shape that is thinner than the memo’s proposed generic planner payload (`src/presenter/compose_from_intent.py:612-724`)

So the right reading is:

- router/planner asymmetry is the main remaining Phase 1 gap
- Phase 1C still needs small shared-presenter/schema follow-through to make that new planner outcome executable

2. Does the code support the memo’s claim that the planner is still asymmetric?

Yes.

AOI saved-result path:

- router accepts `saved_result` and routes to `planner.aoi_compose_handoff` (`src/orchestrator/task_router.py:172-199`, `tests/test_task_router.py:45-87`)
- planner returns `aoi_composition_handoff_plan` and followup to `/v1/presenter/compose-from-selection` (`src/orchestrator/task_planner.py:472-640`, `tests/test_task_planner.py:403-445`)
- persisted planning snapshots are tested for this AOI handoff path (`tests/test_task_planner.py:448-527`)

Genealogy task-planned path:

- router only accepts `registered_corpus` / `inline_documents` for genealogy (`src/orchestrator/task_router.py:203-224`)
- planner only accepts `registered_corpus` / `inline_documents` context for genealogy and returns `genealogy_execution_plan` plus `/v1/executor/jobs` (`src/orchestrator/task_planner.py:384-469`)
- the-critic backend enforces that exact followup contract (`/home/evgeny/projects/the-critic/api/server.py:18356-18375`)

3. Is the memo right to target `saved_result` genealogy composition planning rather than extending the existing `registered_corpus` task-planned launch path?

Yes.

That is the cleaner bounded target because:

- `registered_corpus` is already an execution-launch seam with explicit fail-closed `/v1/executor/jobs` semantics, not a composition seam (`/home/evgeny/projects/the-critic/api/server.py:18369-18375`)
- the Stage 8/9 completion memo explicitly frames genealogy task-planned launch as `registered_corpus` execution proof only (`communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md:26-39`, `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md:49-53`)
- saved-result planning matches the Phase 1B canonical identity doctrine around `source_v2_job_id` and the existing AOI planning-snapshot law

The memo’s own safety clause is also correct:

- if genealogy saved-result truth cannot honestly materialize bounded sections, the slice should stop and revise rather than silently mutating the registered-corpus execution proof into a mixed execution/compose adapter

4. Is the proposed generic `direct_sections` planner outcome technically coherent with the existing shared transient handoff executor?

Partly.

Mechanically coherent:

- genealogy is registered for `direct_sections` (`src/presenter/compose_from_intent.py:141-154`)
- a bounded genealogy `compose-from-intent` call works today (`tests/test_compose_from_intent.py:500-543`)

Not fully coherent yet at the public contract level:

- `compose-from-intent` only accepts bare prose sections (`src/presenter/schemas.py:605-621`)
- the richer role/order metadata path exists only internally (`src/presenter/compose_from_intent.py:612-637`)
- grouped layouts still emit AOI-branded parent labels (`src/presenter/compose_from_intent.py:653-669`)

So the memo’s target is viable, but only with the revisions above.

5. Would the proposed scope actually produce a non-AOI planner-to-presentation path, or only another analyzer-only proof that still bypasses the planner?

It would produce a real non-AOI planner-to-presentation path if implemented with the required thin adapter/harness.

Without that explicit requirement, it could degrade into another analyzer-only proof that stops at planner JSON.

So the memo’s acceptance tests point in the right direction, but the executable adapter/harness should be made mandatory.

6. Is anything in the memo contradicted by the code?

No material claim is flatly contradicted.

The main issue is overstatement, not contradiction:

- the shared executor is reusable in a bounded sense, but not yet cleanly generic at every semantic/UI detail

7. Is anything important missing that would make the scope under-specified or unsafe to implement?

Yes.

Missing items:

- one explicit presenter-boundary decision for how planner-owned direct-section metadata reaches `compose-from-intent`
- one explicit bounded schema/runtime follow-through note for analyzer snapshot types and host typings
- one mandatory executable adapter/harness
- one explicit section-budget / data-thickness gate for the first genealogy saved-result proof

8. Is this scope narrow enough to stay Phase 1C, rather than drifting into browser productization, lifecycle work, or Phase 2 proof?

Yes, with the revisions above.

The memo stays inside the Phase 1 sequence established by the fixed-direction roadmap and Phase 1A completion memo:

- one bounded non-AOI composition-facing planner path
- no lifecycle/session reopening
- no browser polish mandate
- no second-consumer or host-neutral proof claim

## Concrete Code-Path Verification

- The router still structurally excludes genealogy `saved_result`: `task_router.py` only treats AOI as `saved_result`-compatible and rejects genealogy `saved_result` outright (`src/orchestrator/task_router.py:172-224`).
- The routing schema itself still has no generic composition-facing genealogy outcome; the launch contract kinds are AOI compose handoff or genealogy analyze/analyze-by-ref (`src/orchestrator/task_routing_schemas.py:61-69`).
- The planner still has exactly two positive planning branches:
  - genealogy execution plan to `/v1/executor/jobs` (`src/orchestrator/task_planner.py:436-456`)
  - AOI composition handoff to `/v1/presenter/compose-from-selection` (`src/orchestrator/task_planner.py:597-624`)
- The planning schema remains AOI-specialized for saved-result composition:
  - `SavedResultPlanningContext` is described as bounded AOI handoff planning (`src/orchestrator/task_planning_schemas.py:128-133`)
  - `AoiCompositionHandoffPlan` is the only composition-facing handoff payload model (`src/orchestrator/task_planning_schemas.py:166-189`)
- Planning snapshot persistence exists and is real, but its summary extraction is AOI-shaped today (`src/orchestrator/planning_decision_store.py:34-64`; `src/api/routes/orchestrator.py:326-356`; `tests/test_task_planner.py:448-527`).
- Host Contract v2 is already layered as Phase 1B required, so the memo is correct not to reopen that decision (`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts:56-127`, `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts:196-221`).
- The current host-side genealogy task-planned consumer is still explicitly execution-only and registered-corpus-only (`/home/evgeny/projects/the-critic/api/server.py:18062-18386`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1039-1050`, `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx:1465-1505`).
- The shared `direct_sections` executor is boundedly reusable, but the current proof only covers a one-section genealogy happy path (`tests/test_compose_from_intent.py:500-543`), and grouped multi-section behavior still uses AOI-branded parent titles (`src/presenter/compose_from_intent.py:653-669`).

## Judgment On Program Sequence

This is the right next step in the larger sequence.

The recent roadmap and memo trail all converge on the same state judgment:

- Phase 0 closed honestly
- Phase 1B locked contract/ownership decisions
- Phase 1A landed shared bridge substrate and durable AOI planner recovery
- the remaining honest gap is one non-AOI composition-facing planner path, not another host-contract memo and not premature lifecycle or Phase 2 proof (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:221-239`, `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md:157-179`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1205-1238`)

So the memo is aimed at the correct problem.

## Required Revisions

1. Add one explicit presenter-boundary decision:
   - either extend `compose-from-intent` to accept planner-owned section metadata
   - or constrain the first genealogy proof so bare `prose_sections` are sufficient and AOI-branded grouped-parent behavior is avoided or generalized
2. Add one explicit bounded schema/runtime work item covering:
   - `src/orchestrator/task_planning_schemas.py`
   - `src/orchestrator/planning_decision_store.py`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
   - and any minimal Host Contract v2 surface-selection/runtime updates needed for `planning_decision_fetch`
3. Change the thin adapter/harness from optional to required, and name which boundary executes the new handoff contract into `compose-from-intent`.
4. Add one operational preflight rule:
   - if genealogy saved-result truth cannot honestly materialize at most 4 direct sections from analyzer-owned result/view/artifact truth, stop and write a revision memo instead of widening the slice.

With those revisions, the memo is solid enough to drive Phase 1C implementation planning.
