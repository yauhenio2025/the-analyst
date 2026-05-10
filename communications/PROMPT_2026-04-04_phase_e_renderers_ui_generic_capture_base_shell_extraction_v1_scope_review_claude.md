# Prompt For Claude: Phase E Renderers-UI Generic Capture-Base Shell Extraction V1 Scope Review

Please review the current next-step scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_scope.md`

Context you should also inspect before concluding:

- `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_completion.md`
- `communications/REPORT_Codex_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Audit_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Current_Renderer_Selection_Emission_Shared_Seam_Promotion_Readiness_V1_Scope_Critique_2026-04-04.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Code you should inspect directly:

- `renderers-ui/package.json`
- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `the-critic/webapp/src/lib/currentRendererCapture.ts`
- `the-critic/webapp/src/components/V2TabContent.tsx`
- `the-critic/webapp/src/contexts/CaptureContext.tsx`

What I want from you:

1. Test the robustness of the memo’s assumptions.
2. Examine them against the larger analyzer-v2-as-brain objective and the current roadmap.
3. Scrutinize the memo’s claims against the actual codebase, not just the memo text.
4. Pressure-test whether the proposed v1 extraction boundary is honest:
   - Is the top-level-renderer-only slice a valid partial first proof?
   - Is deferring `SubRenderers` still strategically honest given how much raw capture logic lives there?
   - Does the memo stay honest that this is a top-level package pilot only, not a representative package-wide proof?
   - Does it name the `SubRenderers` forwarding asymmetries clearly enough?
   - Is the proposed package-neutral shell actually the right candidate, or is it still too broad / too narrow?
5. State whether the current scope should be:
   - approved
   - approved with corrections
   - rejected
6. If you recommend corrections, make them concrete and implementation-relevant.

Important calibration points to check explicitly:

- The readiness memo now uses candidate-language, not “already proved extraction truth.”
- The next scope is explicitly a partial first extraction proof, not the whole package proof.
- The proposed shared shell stays below:
  - Critic `CaptureSelection`
  - `_firstHopAffordance`
  - `requireWorkflowKey`
  - `requireJobId`
  - `source_workflow_key`
  - `genealogy_job_id`
- The proposed utility still fits the existing package `Record<string, unknown>` capture style.
- The proposed utility preserves current package defaulting instead of drifting toward Critic fail-closed behavior.
- The scope is honest that `renderers-ui` does not currently have an established dedicated test harness for this extraction seam.
- The roadmap wording matches what the docs-first calibration actually established.

Please save your review to this exact file:

- `communications/REPORT_Claude_Phase_E_Renderers_UI_Generic_Capture_Base_Shell_Extraction_V1_Scope_Critique_2026-04-04.md`

Use a clear verdict near the top, then findings ordered by importance, then any strategic implications, then a bottom-line recommendation.
