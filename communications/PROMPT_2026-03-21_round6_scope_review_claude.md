Review the proposed round-6 scoping memo critically and save your output to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Round6_Cross_Workflow_Adaptive_AOI_Suite_Scope_Critique_2026-03-21.md`

Do not implement code. Do not edit source files. Write only the report.

Primary file to review:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md`

Context you should examine before writing the report:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md`
- `/home/evgeny/projects/analyzer-v2/communications/PLAN_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_execution.md`

Code and contract surfaces you should inspect:

- `/home/evgeny/projects/analyzer-v2/src/presenter/bounded_dynamic_composition.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/decision_trace.py`
- `/home/evgeny/projects/analyzer-v2/src/aoi/contract.py`
- `/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_by_theme.json`
- `/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_thematic_report.json`
- `/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_by_sin_type.json`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

What I want from you:

1. Judge whether `aoi_thematic_report` is actually the right second AOI surface, or whether `aoi_by_sin_type` is the better bounded next target.
2. Look for hidden complexity in coordinating two AOI child surfaces under `aoi_thematic_analysis`.
3. Stress-test the claim that round 6 should remain generic-host-only.
4. Check whether the proposed report-family contracts are concrete enough to validate cleanly.
5. Check whether the proposed suite trace shape is the right reuse of round-4 suite tracing.
6. Check whether the documentary gate is framed correctly given that round 5 is code/test complete but not route-proof complete.

Please structure the report with:

- `Verdict`
- `Findings`
- `What Looks Right`
- `What Needs Tightening`
- `Recommended Revision`

Prioritize:

- incorrect assumptions
- hidden implementation complexity
- under-specified contracts
- places where the memo overclaims what the current codebase can support

Do not be polite at the expense of precision. If the memo should change direction, say so explicitly.
