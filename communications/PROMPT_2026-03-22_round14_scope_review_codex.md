Review this memo in a brand-new session:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`

Treat this as an external architecture/code audit, not a rewrite exercise.

Please do all of the following:

1. test the robustness of the memo’s assumptions against the live code
2. evaluate whether this is truly the right next move in light of:
   - `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
   - `/home/evgeny/projects/analyzer-v2/communications/DYNAMIC_BESPOKE_APPS_VISION.md`
   - `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
   - `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md`
   - `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_completion.md`
   - `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md`
   - `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`
   - `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`
3. inspect the real code seams, especially:
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
   - `/home/evgeny/projects/the-critic/api/server.py`
   - `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
4. inspect any other recent docs or memos that materially bear on the decision
5. state explicitly if no relevant “Perspective” docs folder exists in this workspace context

Questions to answer:

1. Is hot-path transient launch adoption the right next bounded move, or is the stronger next tranche actually transient-to-authored promotion or something else?
2. Does the memo put the launch seam in the right place?
3. Is `source_analysis_id` the right normal UI handoff key, with raw `source_v2_job_id` kept out of the normal product path?
4. Does the memo correctly preserve the lifecycle boundary between job-backed AOI workspace law and transient compose law?
5. What assumptions are too loose, too optimistic, or contradicted by the code?
6. What should the execution plan lock down explicitly if the scope is directionally right?

Output requirements:

- Save your audit to:
  - `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_Round14_AOI_Transient_Hot_Path_Launch_Scope_Audit_2026-03-22.md`
- Give a clear verdict:
  - Approve
  - Approve after revision
  - Reject
- Findings first, ordered by severity.
- Be specific about code paths, route/lifecycle seams, and any hidden widening risk.
- If you think the memo picks the wrong next move, name the better alternative and justify it.
