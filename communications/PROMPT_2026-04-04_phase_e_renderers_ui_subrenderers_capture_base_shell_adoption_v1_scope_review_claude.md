# Prompt For Claude: Phase E Renderers-UI SubRenderers Capture-Base Shell Adoption V1 Scope Review

Please review the current next-step scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_scope.md`

Context you should also inspect before concluding:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_completion.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Audit_Rerun_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Critique_Rerun_2026-04-04.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Code you should inspect directly:

- `renderers-ui/package.json`
- `renderers-ui/src/utils/captureBase.ts`
- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `renderers-ui/scripts/check-capture-base.mjs`
- `the-critic/webapp/package.json`

What I want from you:

1. Test the robustness of the memo’s assumptions.
2. Examine them against the larger analyzer-v2-as-brain objective and the current roadmap.
3. Scrutinize the memo’s claims against the actual codebase, not just the memo text.
4. Pressure-test whether the proposed next slice is honest:
   - Is `SubRenderers` now the real next dominant deferred surface?
   - Is direct adoption of the existing `captureBase` utility the right next step, or should forwarding normalization come first?
   - Does the memo stay honest that current forwarding asymmetries remain untouched?
   - Is the adopter set precise enough and still bounded enough?
   - Does the verification plan stay honest given that `renderers-ui` still has no dedicated test runner?
5. State whether the current scope should be:
   - approved
   - approved with corrections
   - rejected
6. If you recommend corrections, make them concrete and implementation-relevant.

Important calibration points to check explicitly:

- The top-level extraction completion memo does **not** overclaim package-wide proof.
- The next scope is about the dominant deferred `SubRenderers` surface, not generic package convergence.
- The proposed adoption still stays below:
  - Critic `CaptureSelection`
  - `_firstHopAffordance`
  - `requireWorkflowKey`
  - `requireJobId`
  - `source_workflow_key`
  - `genealogy_job_id`
- The scope is explicit that forwarded defaults stay as they are today.
- The scope is explicit that forwarding normalization is not part of this tranche.
- The proposed utility reuse still fits the package’s `Record<string, unknown>` capture style.
- The roadmap wording matches what the top-level pilot actually established.

Please save your review to this exact file:

- `communications/REPORT_Claude_Phase_E_Renderers_UI_SubRenderers_Capture_Base_Shell_Adoption_V1_Scope_Critique_2026-04-04.md`

Use a clear verdict near the top, then findings ordered by importance, then any strategic implications, then a bottom-line recommendation.
