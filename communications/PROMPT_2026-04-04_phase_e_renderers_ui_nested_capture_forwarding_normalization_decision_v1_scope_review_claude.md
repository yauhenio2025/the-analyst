Please review this scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md`

Before you conclude, read all of these in full. Do not skip any of them:

- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md`
- `communications/REPORT_Claude_Close_Read_Roadmap_Recalibration_Critique_Rerun_2026-04-04.md`
- `communications/REPORT_Codex_Close_Read_Roadmap_Recalibration_Audit_Rerun_2026-04-04.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

Inspect these code files directly:

- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `renderers-ui/src/utils/captureBase.ts`
- `renderers-ui/scripts/check-capture-base.mjs`
- `the-critic/webapp/package.json`
- `the-critic/webapp/src/components/V2TabContent.tsx`
- `the-critic/webapp/src/lib/currentRendererCapture.ts`
- `the-critic/webapp/src/components/CaptureActionBar.tsx`

What I need from you:

1. Test the robustness of the memo’s assumptions.
2. Examine them against the bigger picture and the analyzer-v2-as-brain objective.
3. Scrutinize the memo’s claims against the actual codebase, not just the memo text.
4. Pressure-test the decision boundary:
   - Is forwarding-normalization really the last clear package-internal capture-runtime gate?
   - Are the `AccordionRenderer` and `CardRenderer` asymmetries correctly differentiated?
   - Is the memo honest that clearing this gate would still leave packed-host integration readiness, host-delivery posture, and app-layer first-hop eligibility for the subsequent `Close Read V1` memo?
5. Evaluate whether the scope is tight enough to stay docs-first and decision-only unless evidence forces a real patch.
6. Give a clear verdict:
   - approve
   - approve with corrections
   - reject
7. If you recommend corrections, make them concrete and implementation-relevant.

Check these points explicitly:

- The memo does not frame this slice as automatic forwarding normalization.
- The memo does not overclaim package-wide nested runtime convergence.
- The memo treats `AccordionRenderer` as a metadata/defaulting precision issue.
- The memo treats `CardRenderer` as a functional nested capture-availability issue across every subsection dispatch branch, not just one path.
- The memo keeps `_firstHopAffordance`, workflow/job requiredness, host `CaptureSelection`, and destination-policy law out of the package slice.
- The memo says clearly that even a “clean” verdict only clears the package-source gate and does not settle packed-host integration readiness, host-delivery posture, or app-level first-hop policy.
- The memo does not treat `renderers-ui/scripts/check-capture-base.mjs` as forwarding-correctness proof; only utility-behavior evidence.

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Decision_V1_Scope_Critique_2026-04-04.md`
