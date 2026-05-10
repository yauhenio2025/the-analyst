# Prompt For Claude: Review Phase 0 AOI Exemplar Honesty Closeout Execution Memo

You are reviewing a bounded execution memo in `/home/evgeny/projects/analyzer-v2`.

Your job is not to implement the memo.
Your job is to pressure-test whether this is the right immediate Phase 0 memo, whether its assumptions are robust, and whether it stays honest relative to the larger program objective that analyzer-v2 becomes the intelligence layer and downstream apps become thin hosts.

## Primary document to review

- `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md`

## Required supporting material

Read and use these documents as active context:

- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md`
- `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`

Also inspect the relevant code and helpers, especially:

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts`
- `/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh`
- `/home/evgeny/projects/the-critic/test-stage5-aoi-landing-smoke.js`
- `src/api/routes/orchestrator.py`
- `src/orchestrator/task_router.py`
- `src/orchestrator/task_planner.py`
- `src/presenter/compose_from_intent.py`

You may inspect additional recent memos in `communications/` or relevant `docs/` if they materially bear on the memo’s assumptions or the larger objective.

## What to evaluate

Test the memo against these questions:

1. Is this the right immediate artifact for Phase 0, or is it still mixing immediate execution with future-phase planning?
2. Are the memo’s operational assumptions robust enough to make the fresh rerun and honest Stage 2 decision executable?
3. Does the memo preserve the bigger-picture goal, or does it still risk turning Phase 0 into another AOI-only sink?
4. Are its claims about the real Critic route, planner-primary browser path, artifact capture, and grading boundary accurate against the live codebase?
5. Is anything missing that would make the memo more likely to generate an honest Phase 0 outcome without widening scope?

## Things you should challenge aggressively

- whether the fixed project / thinker / task target is too rigid or correctly stabilizing
- whether the memo is over-relying on inherited Stage 5 scripts or artifacts
- whether “Phase 0 closes on the grade” is operationally real or still too easy to evade
- whether the memo is honest about what counts as a valid attempt versus a revision-triggering failed attempt
- whether the browser proof requirements are too weak, too strong, or mis-scoped for the real objective
- whether any of the memo’s future-facing assumptions are prematurely locking Phase 1 design choices

## Output requirements

Write your critique memo to:

- `communications/REPORT_Claude_Phase0_AOI_Exemplar_Honesty_Closeout_Execution_Memo_Critique_2026-03-26.md`

Your output should include:

- a verdict: `Approve`, `Approve after revision`, or `Reject`
- the strongest findings first
- explicit discussion of the bigger-picture objective, not just local operational details
- concrete file references where useful
- a short bottom-line judgment on whether this memo is the right immediate Phase 0 vehicle

Do not make code changes.
Do not update the memo yourself.
