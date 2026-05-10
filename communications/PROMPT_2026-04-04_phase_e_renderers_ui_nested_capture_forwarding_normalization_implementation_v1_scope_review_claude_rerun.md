Please review this scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_scope.md`

Before you conclude, read all of these in full. Do not skip any of them, even if some seem overlapping:

- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

Inspect these code files directly:

- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx`
- `renderers-ui/src/utils/captureBase.ts`
- `renderers-ui/scripts/check-capture-base.mjs`
- `src/views/definitions/genealogy_target_profile.json`
- `src/views/definitions/genealogy_per_work_scan.json`
- `/home/evgeny/projects/the-critic/webapp/package.json`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`

What I need from you:

1. Test the robustness of the memo’s assumptions.
2. Examine them against the bigger picture and the analyzer-v2-as-brain objective.
3. Scrutinize the memo’s claims against the actual codebase, not just the memo text.
4. Pressure-test the implementation plan:
   - Does the memo correctly identify the true fix surface in `AccordionRenderer`, `CardRenderer`, and `GenericSectionRenderer`?
   - Is the `AccordionRenderer` `nested_sections` gap real on current genealogy surfaces?
   - Does the `CardRenderer` plan really cover every subsection dispatch branch that currently drops capture runtime?
   - Is the `GenericSectionRenderer` extension truly pass-through only, or does it implicitly widen package law?
   - Are there any other forwarding paths in package renderers that this memo misses?
5. Verify the preservation rules against current `captureBase.ts` semantics.
6. Check the corrected provenance claim explicitly:
   - missing `_captureSourceType` definitely degrades genealogy nested captures today
   - missing `_captureEntityId` is only a conditional future-risk on the current host path because `V2TabContent` currently threads `_captureJobId` and `_captureEntityId` from the same `presentation.job_id`
7. Evaluate whether this still qualifies as one bounded forwarding-normalization patch rather than a broader renderer refactor.
8. Give a clear verdict:
   - approve
   - approve with corrections
   - reject
9. If you recommend corrections, make them concrete and implementation-relevant.

Check these points explicitly:

- The memo does not promote any Critic-local capture law into the package.
- The memo does not change `captureBase.ts` itself.
- The memo’s `GenericSectionRenderer` extension is pass-through only, not gating or normalization.
- The memo correctly names which near-term genealogy surfaces are affected by each gap.
- The memo is honest that even a clean patch only clears the package-source gate, not host-delivery posture or app-layer first-hop policy.
- The memo’s file-touch set matches the actual fix shapes described in the text.

At the top of your output, include a short section called `Context Check` listing every required memo and code file above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Critique_Rerun_2026-04-04.md`
