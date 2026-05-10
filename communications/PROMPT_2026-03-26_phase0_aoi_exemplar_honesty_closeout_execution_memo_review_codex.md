# Prompt For Codex: Audit Phase 0 AOI Exemplar Honesty Closeout Execution Memo

Audit the immediate Phase 0 execution memo in `/home/evgeny/projects/analyzer-v2` and decide whether it is the right bounded memo for generating the evidence the program actually needs now.

Your task is not to execute the proof.
Your task is to verify whether the memo’s assumptions, boundaries, and codebase claims are solid enough to support an honest fresh rerun and explicit Stage 2 decision without widening back into AOI-specific drift.

## Primary document

- `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md`

## Required context

Read and use these documents:

- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md`
- `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`

Inspect the actual codebase claims against at least these files:

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

You may inspect additional recent memos in `communications/` or relevant `docs/` if they materially bear on the memo.

## Questions to answer

1. Is this memo the right immediate Phase 0 artifact, or should it still be narrower or differently shaped?
2. Are the operational assumptions strong enough to make the fresh rerun executable and honestly gradable?
3. Does the memo correctly separate:
   - valid preconditions
   - valid proof steps
   - valid closeout outcomes
   - out-of-scope widening
4. Are the codebase-backed claims about the real Critic route, planner-primary browser path, and existing helper scripts accurate?
5. What, if anything, is missing or prematurely fixed in the memo that would make Phase 0 execution more honest and more robust?

## Deliverable

Write your audit to:

- `communications/REPORT_Codex_Phase0_AOI_Exemplar_Honesty_Closeout_Execution_Memo_Audit_2026-03-26.md`

Include:

- a verdict: `Approve`, `Approve with revisions`, or `Reject`
- findings ordered by severity
- explicit codebase-backed reasoning
- discussion of the bigger-picture goal, not just local execution mechanics
- a concise bottom line on whether this memo is the right immediate Phase 0 vehicle

Do not modify code or update the memo yourself.
