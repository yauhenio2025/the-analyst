# Prompt For Codex: Phase E Renderers-UI Generic Capture-Base Shell Extraction V1 Scope Audit

Please audit the current next-step scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`

Before concluding, also read:

- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_completion.md`
- `communications/REPORT_Codex_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Audit_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Critique_2026-04-04.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Inspect the code directly:

- `renderers-ui/package.json`
- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `the-critic/webapp/src/lib/currentRendererCapture.ts`
- `the-critic/webapp/src/components/V2TabContent.tsx`
- `the-critic/webapp/src/contexts/CaptureContext.tsx`

Audit goals:

1. Verify whether the scope matches the real package capture architecture.
2. Stress-test the assumptions behind the partial first-extraction boundary.
3. Compare the proposed extracted shell against the actual inline package builders.
4. Check whether the memo stays honest about what was established in the prior readiness slice.
5. Evaluate the scope in light of the larger roadmap and analyzer-v2-as-brain objective.
6. Say clearly whether the scope is:
   - approve
   - approve with corrections
   - reject

Please check these questions explicitly:

- Is the new candidate-language calibrated correctly, or does any part still overclaim package-side proof?
- Is top-level-only adoption a genuinely honest first subset, or does the weight of `SubRenderers` make that framing misleading?
- Is the memo explicit enough that v1 is a top-level package pilot only, not a representative package-wide proof?
- Does it account honestly for the existing `SubRenderers` forwarding asymmetries?
- Is the proposed utility/API actually the smallest reusable package-neutral shell?
- Does the proposed shell preserve current package defaulting rather than importing Critic fail-closed behavior?
- What exact concerns still need to stay Critic-local?
- Does the next roadmap recommendation still hold after inspecting the code?

If useful, you may rerun a focused non-destructive verification batch, but keep the audit primarily code-backed and scope-focused.

Save your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Audit_2026-04-04.md`

Please put the verdict near the top and keep the output concrete, code-backed, and calibration-focused.
