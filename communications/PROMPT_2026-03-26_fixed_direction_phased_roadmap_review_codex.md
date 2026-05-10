# Prompt For Codex: Audit Fixed-Direction Phased Roadmap

Audit the strategic roadmap in `/home/evgeny/projects/analyzer-v2` and decide whether it is the right fixed direction for getting the program to the stated “analyzer-v2 is the brain” goal without wasting time on app-local dead ends.

## Primary document

- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`

## Required context

Read and use these documents:

- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md`
- `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md`

Inspect the actual codebase claims against at least these files:

- `src/api/routes/orchestrator.py`
- `src/orchestrator/task_router.py`
- `src/orchestrator/task_planner.py`
- `src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

You may inspect additional recent memos in `communications/` or relevant `docs/` if they materially bear on the roadmap.

## Questions to answer

1. Is the memo’s phase ordering the best available sequencing from the current state?
2. Does it correctly separate:
   - immediate exemplar honesty work
   - architectural generalization work
   - later lifecycle/governance work
3. Are the anti-drift rules strong enough to keep the program from overinvesting in `the-critic` or AOI-specific behavior that is not part of the intended end state?
4. Does the memo overstate how close the current codebase is to host-neutral planner-to-presentation behavior?
5. What, if anything, is missing from the roadmap that would make it more likely to reach the actual platform goal?

## Deliverable

Write your audit to:

- `communications/REPORT_Codex_Fixed_Direction_Phased_Roadmap_Audit_2026-03-26.md`

Include:

- a verdict: `Approve`, `Approve with revisions`, or `Reject`
- findings ordered by severity
- explicit codebase-backed reasoning
- discussion of the bigger-picture goal, not just local implementation state
- a concise bottom line on whether this roadmap is the right fixed direction

Do not modify code or update the roadmap memo yourself.

