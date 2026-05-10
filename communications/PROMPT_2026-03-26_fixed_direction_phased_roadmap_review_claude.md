# Prompt For Claude: Review Fixed-Direction Phased Roadmap

You are reviewing a strategic roadmap memo in `/home/evgeny/projects/analyzer-v2`.

Your job is not to implement anything.
Your job is to pressure-test whether this roadmap actually keeps the program moving toward the stated goal that analyzer-v2 becomes the intelligence layer and downstream apps become thin hosts.

## Primary document to review

- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`

## Required supporting material

Read and use the following as active context:

- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md`
- `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md`

Also inspect the relevant code, especially:

- `src/api/routes/orchestrator.py`
- `src/orchestrator/task_router.py`
- `src/orchestrator/task_planner.py`
- `src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

## What to evaluate

Test the memo against five questions:

1. Is the phase ordering strategically correct?
2. Does the memo correctly distinguish:
   - what genuinely moved upstream
   - what is still host-owned
   - what is accidental AOI / `the-critic` coupling
3. Are the anti-drift rules strong enough to stop the program from wasting time on app-local polish that will not matter in the target architecture?
4. Does the roadmap preserve honest sequencing around the still-open AOI exemplar gate without allowing AOI proof maintenance to consume the whole roadmap?
5. If followed literally, would this roadmap materially increase the chance that analyzer-v2 becomes the brain rather than just a better downstream presenter?

## Things you should challenge aggressively

- whether Phase 0 is still too much AOI gravity
- whether Phase 1 is specific enough, or still hides too many unrelated generalization tasks
- whether current apps are being treated honestly as proving harnesses rather than future end-state products
- whether Stage 13 Tier B / second-consumer / non-AOI proof is placed in the right phase
- whether lifecycle or governance should move earlier
- whether the memo understates any code reality that would make the roadmap harder than it sounds

## Output requirements

Write a critique memo to:

- `communications/REPORT_Claude_Fixed_Direction_Phased_Roadmap_Critique_2026-03-26.md`

Your output should include:

- a verdict: `Approve`, `Approve after revision`, or `Reject`
- the strongest findings first
- explicit discussion of the bigger-picture objective, not just local code facts
- concrete file references where useful
- a short bottom-line judgment on whether this roadmap is the best available direction right now

Do not make code changes.
Do not update the roadmap memo yourself.

