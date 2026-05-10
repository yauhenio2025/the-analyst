# Prompt For New Codex Session

Audit the proposed next-stage memo:

- `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_scope.md`

This is not a summarization task. Treat it as a codebase-and-strategy audit.

Required work:

1. inspect the live analyzer-v2 and the-critic code to verify or falsify the memo’s claims
2. inspect the recent memo trail from the last 4 days, especially Stage 8, 9, 10, 11, 12, and 13 scope/completion memos and any recent review reports
3. compare the recommendation against the canonical roadmap and broader vision in:
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
4. judge whether this is actually the next honest phase, or whether the memo is skipping a more important prerequisite

Please be especially concrete about:

- whether the-critic currently uses `route-task` or `plan-task` anywhere
- what exact launch/execution helpers already exist for:
  - `orchestrator/analyze`
  - `orchestrator/analyze-by-ref`
  - `executor/jobs`
  - `compose-from-source`
- whether the proposed AOI seam and genealogy seam are both feasible without analyzer API changes
- whether a separate bounded task-launch contract is cleaner than widening Host Contract v1
- whether the revised memo actually avoids creating a third disconnected client/runtime layer, or still risks adding one beside `boundedV2Client.ts` and `composeFromIntentClient.ts`
- whether the memo accidentally blurs advisory planning with lifecycle or automatic dispatch
- whether the memo now describes genealogy `plan-task` precisely enough as advisory-for-dispatch but not read-only
- whether the AOI seam is still thinner than the genealogy seam and is now framed honestly
- whether the roadmap now really points upstream, or whether another Stage 13 / Stage 14 move would be more honest

Output expectations:

- findings first, ordered by severity
- cite specific files and code paths where relevant
- call out both accurate claims and weak assumptions
- give a plain verdict:
  - Approve
  - Approve after revision
  - Reject / wrong next move

Save your final audit to exactly:

- `communications/REPORT_Codex_STAGE8_9_Host_Adoption_Task_Launch_Scope_Audit_2026-03-24.md`

The saved audit should include:

- verdict
- findings
- open assumptions
- whether the memo’s recommendation should stand, be revised, or be replaced
