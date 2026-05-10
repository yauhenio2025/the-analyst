# Prompt For New Claude Session

Review the proposed next-stage memo:

- `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_scope.md`

Your job is to stress-test it hard, not to paraphrase it.

Please do all of the following:

1. test the robustness of the memo’s assumptions
2. examine the recommendation against the bigger-picture program objectives in:
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
   - any other recent strategic memo you think materially matters
3. scrutinize the memo’s claims against the live codebase in both:
   - `/home/evgeny/projects/analyzer-v2`
   - `/home/evgeny/projects/the-critic`
4. read the recent scope/completion trail from roughly the last 4 days, especially the Stage 8, 9, 10, 11, 12, and 13 memos and any relevant review reports
5. decide whether this is actually the right next phase, or whether the memo is missing a better next move

Questions you should answer explicitly:

- Is a bounded Stage 8/9 host-adoption slice really the next highest-leverage move after the Stage 13 second slice?
- Is the memo understating or overstating how ready the current host/runtime is for `route-task` / `plan-task` adoption?
- Is it correct to keep Host Contract v1 stable and layer a separate bounded task-launch contract on top?
- Does the revised memo now handle the risk of creating a third disconnected client/runtime layer in the-critic, or is the unification story still too weak?
- Is the proposed AOI proof seam honest, given that Stage 9 AOI planning still stops at allowed/blocked profiles rather than auto-selecting one?
- Is the AOI seam now framed honestly as contractual consolidation rather than a dramatic analytical-intelligence reduction?
- Is the proposed genealogy proof seam honest, given the current execution helpers and current host launch topology?
- Does the memo now treat genealogy `plan-task` honestly as advisory-for-dispatch but not read-only, and are the commit/idempotency implications scoped clearly enough?
- Does this recommendation actually reduce host-owned analytical intelligence, or just move it around?
- Is Stage 14 lifecycle still correctly deferred after the latest code and memo trail?
- If this memo is wrong, what should the next phase be instead?

Deliverable requirements:

- Put findings first, ordered by severity
- Prioritize real problems, mismatches, hidden scope creep, missing prerequisites, codebase contradictions, and proof-bar weakness
- Be explicit if some assumptions are good
- If you think the memo is directionally right but needs revision, say “Approve after revision”
- If you think it is ready, say “Approve”
- If you think it is the wrong next move, say so plainly

Save your final review to exactly:

- `communications/REPORT_Claude_STAGE8_9_Host_Adoption_Task_Launch_Scope_Critique_2026-03-24.md`

In that saved report, include:

- verdict
- key findings
- open assumptions
- whether the next phase should stay as proposed or be reframed
