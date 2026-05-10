# Prompt For Claude: Phase 3 Bounded Lifecycle V1 Scope Critique

Critique the newly drafted Phase 3 scope memo:

- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`

Your job is to test the robustness of the assumptions behind that memo against:

- the actual current codebase in `analyzer-v2`, `the-critic`, and any relevant current supporting surfaces
- the recent March 27-28 roadmap and memo trail
- the bigger program objective of making `analyzer-v2` the analytical brain while downstream apps become thin hosts

## Bigger-picture objective

Evaluate the memo in light of the real target:

- analyzer-v2 should own analytical understanding, routing, planning, composition law, presentation law, and now the saved truth of dynamic analytical surfaces where lifecycle is reopened
- downstream apps should be proving harnesses and thin hosts, not workflow-specific lifecycle controllers
- Phase 3 should follow verified Phase 2 host-neutral transient proof rather than reopening bridge work or drifting into publish/share productization

So judge the memo both as:

1. a bounded next implementation scope after verified Phase 2 completion
2. a sequencing decision about how to define lifecycle honestly without rebuilding consumer-local intelligence

## What to inspect first

Read these docs before writing your critique:

- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`
- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
- `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`
- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Then search `communications/` and `docs/` for any additional recent memos or reports that materially bear on:

- lifecycle
- session/draft/revisit semantics
- planning snapshots
- transient compose
- saved transient surfaces
- Host Contract v2
- older Stage 3 / Stage 14 direction memos that may now be obsolete or superseded

## Code paths to inspect

Analyzer:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/direct_sections_compose_harness.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`

Current consumer / proof surfaces:

- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`

Optional comparison if useful:

- `/home/evgeny/projects/analyzer-v2/src/api/routes/projects.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/project_manager.py`

## Questions to answer directly

1. Is lifecycle the right next phase now that Phase 2 transient proof is live and boundedly closed?
2. Is the memo right to target generic `direct_sections + compose-from-intent` lifecycle first rather than reopening AOI source-backed proxy lifecycle?
3. Is the memo correct that `planning_decision_id` is insufficient as a lifecycle object by itself?
4. Does the code support the memo’s claim that there is currently no real save/reopen lifecycle object for transient analytical surfaces?
5. Is the memo drawing the analyzer/host ownership line clearly enough for:
   - saved session truth
   - reopen payload truth
   - route/navigation semantics
   - `session_id` handling?
6. Is the bounded retention rule honest enough for a first lifecycle slice, or is it ducking a necessary lifecycle decision?
7. Does the memo stay properly bounded away from:
   - publish/share
   - automatic persistence
   - new transient consumer registration
   - AOI-specific productization
8. Is anything in the memo contradicted by the live code?
9. Is anything important missing that would make the scope under-specified or unsafe to implement?

## Output requirements

Write your critique to exactly this file:

- `communications/REPORT_Claude_Phase3_Bounded_Lifecycle_V1_Scope_Critique_2026-03-28.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether this is now the right next honest step.
5. A direct answer to whether the memo stays properly bounded.
6. Any concrete revisions needed before implementation planning.

Prioritize hidden assumptions, codebase mismatches, scope drift, and roadmap mis-sequencing over general summary.

Do not edit the memo.
Do not make code changes.
This is a documentation/code-path critique only.
