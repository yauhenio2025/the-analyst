Audit the proposed round-6 scoping memo and save your output to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_Round6_Cross_Workflow_Adaptive_AOI_Suite_Scope_Audit_2026-03-21.md`

Do not implement code. Do not edit source files. Write only the audit report.

Primary file to audit:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_scope.md`

Required context:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round5_cross_workflow_adaptive_aoi_theme_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_scope.md`
- `/home/evgeny/projects/analyzer-v2/communications/PLAN_2026-03-20_round5_cross_workflow_adaptive_aoi_theme_execution.md`

Code and renderer surfaces to inspect:

- `/home/evgeny/projects/analyzer-v2/src/presenter/bounded_dynamic_composition.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/decision_trace.py`
- `/home/evgeny/projects/analyzer-v2/src/aoi/contract.py`
- `/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_by_theme.json`
- `/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_thematic_report.json`
- `/home/evgeny/projects/analyzer-v2/src/views/definitions/aoi_by_sin_type.json`
- `/home/evgeny/projects/analyzer-v2/src/renderers/definitions/table.json`
- `/home/evgeny/projects/analyzer-v2/src/renderers/definitions/accordion.json`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

Audit questions:

1. Is `adaptive_aoi_theme_report_suite_v1` the right bounded next proof token and shape?
2. Is `aoi_thematic_report` really the right second AOI surface, or is `aoi_by_sin_type` more grounded for the next suite proof?
3. Are the proposed `aoi_report_briefing` and `aoi_report_evidence_review` contracts concrete enough to validate with the existing renderer schemas?
4. Does the memo hide meaningful complexity in single-view, trace, or in-place child replacement under `aoi_thematic_analysis`?
5. Is the gate status right, given that round 5 lacks route-real proof fixtures and proof docs?
6. Are there any places where the memo says “generic host” but the current Critic code would still need explicit AOI-specific work?

Please write the report with:

- `Verdict`
- `Findings`
- `Checks Performed`
- `What Seems Correct`
- `Risks / Open Questions`

Be concrete. Cite exact files and behavior. If the memo should be narrowed, say exactly how. If a fallback to `aoi_by_sin_type` should become the primary target, say that directly.
