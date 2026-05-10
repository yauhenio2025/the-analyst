Audit the round-5 scope memo against the actual codebase and memo trail. Do not implement code. Do not edit repo files except for writing your report.

Write your audit to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_Round5_Cross_Workflow_Adaptive_AOI_Theme_Scope_Audit_2026-03-20.md`

Scope memo under review:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md`

Read at minimum:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md`
- `/home/evgeny/projects/analyzer-v2/src/aoi/contract.py`
- `/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_by_theme.json`
- `/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_by_sin_type.json`
- `/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_thematic_report.json`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`

Your job:

1. Verify that the memo really identifies the next meaningful program variable after round 4.
2. Verify that `aoi_by_theme` has the stable payload seam the memo assumes.
3. Test whether the proposed selector inputs are actually present and stable in the normalized AOI grouped payload.
4. Verify that the proposed runtime families are specific enough to validate cleanly.
5. Check whether any hidden host changes are still required despite the memo’s generic-host claim.
6. Check whether the route contract and thinker-scoped AOI assumptions are stable.
7. Flag missing tests, stale assumptions, or places where the scope is still too loose.

Please write the report with:

- `Findings`
- `Open questions`
- `What looks right`
- `Verdict`

Important constraints:

- Do not implement anything.
- Do not patch code.
- Do not “helpfully” turn this into an execution plan.
- Do not write a memo rewrite; write an audit.
- If you think the memo’s chosen AOI target is wrong, say what should replace it and why.
- Stay grounded in code and current memos, not generic design advice.
