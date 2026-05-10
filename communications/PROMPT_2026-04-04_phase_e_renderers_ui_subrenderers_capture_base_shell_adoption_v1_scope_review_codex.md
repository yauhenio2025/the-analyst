# Prompt For Codex: Phase E Renderers-UI SubRenderers Capture-Base Shell Adoption V1 Scope Audit

Please audit the current next-step scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md`

Before concluding, also read:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_completion.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Audit_Rerun_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Critique_Rerun_2026-04-04.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Inspect the code directly:

- `renderers-ui/package.json`
- `renderers-ui/src/utils/captureBase.ts`
- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `renderers-ui/scripts/check-capture-base.mjs`
- `the-critic/webapp/package.json`

Audit goals:

1. Verify whether the scope matches the real remaining package capture architecture.
2. Stress-test the assumptions behind making `SubRenderers` the next bounded surface.
3. Check whether direct utility adoption is honest without bundled forwarding normalization.
4. Check whether the memo stays honest about what the top-level pilot did and did not prove.
5. Evaluate the scope in light of the larger roadmap and analyzer-v2-as-brain objective.
6. Say clearly whether the scope is:
   - approve
   - approve with corrections
   - reject

Please check these questions explicitly:

- Is `SubRenderers` now the right dominant deferred surface, or is the next honest step actually forwarding normalization first?
- Does the memo preserve current forwarded defaults rather than accidentally promising runtime-threading fixes?
- Is the proposed adopter set precise and complete for the current inline `SubRenderers` capture builders?
- Does the scope stay below package-wide convergence claims?
- Is the verification plan honest enough given there is still no dedicated `renderers-ui` test runner?
- What exact concerns still need to remain outside this tranche?
- Does the next roadmap recommendation still hold after inspecting the code?

If useful, you may rerun a focused non-destructive verification command, but keep the audit primarily code-backed and scope-focused.

Save your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Renderers_UI_SubRenderers_Capture_Base_Shell_Adoption_V1_Scope_Audit_2026-04-04.md`

Please put the verdict near the top and keep the output concrete, code-backed, and calibration-focused.
