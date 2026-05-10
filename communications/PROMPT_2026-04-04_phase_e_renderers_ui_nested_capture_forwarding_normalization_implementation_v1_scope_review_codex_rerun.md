Please audit this scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_scope.md`

Before you conclude, read all of these in full. Do not skip any:

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

Audit goals:

1. Verify every code-level claim in the memo against the actual codebase. Do not trust the memo text alone.
2. Confirm or refute:
   - `AccordionRenderer` configured/auto-detect forwarding still omits `_captureSourceType` and `_captureEntityId`
   - `AccordionRenderer` `nested_sections` and fallback paths pass no capture config to `GenericSectionRenderer`
   - `CardRenderer` subsection dispatch forwards no capture runtime on all relevant branches
   - `GenericSectionRenderer` currently lacks any generic capture-config forwarding prop
   - `genealogy_target_profile.json` and `genealogy_per_work_scan.json` actually exercise the named gaps
   - `CaptureContext.tsx` and `ResearchFlagDialog.tsx` make the `source_type === 'genealogy'` consequence materially real
3. Check the corrected provenance claim explicitly:
   - is `source_type` degradation definitely current on the live host path?
   - is `entity_id` degradation only conditional today because `V2TabContent` currently threads `_captureJobId` and `_captureEntityId` from the same `presentation.job_id`?
4. Check whether there are any other forwarding gaps the memo misses:
   - Does `CardGridRenderer` have any nested dispatch that needs normalization?
   - Are there other callers of `GenericSectionRenderer` that would need `captureConfig`?
   - Do other current view definitions use `nested_sections` in ways that materially affect the verdict?
5. Evaluate whether the proposed `GenericSectionRenderer` extension is minimal enough:
   - pass-through only
   - no package-law widening
   - no hidden merge-order or config-overwrite problem beyond the intended forwarding behavior
6. Examine the scope against the bigger picture:
   - Is this still appropriate Phase E substrate work, or has it drifted into product design?
   - Does the deferred list remain honest?
   - Does the next-step recommendation still hold after inspecting both code and roadmap context?
7. If useful, rerun focused non-destructive verification:
   - `cd renderers-ui && npm run build`
   - `cd renderers-ui && node scripts/check-capture-base.mjs`
8. Give a clear verdict:
   - approve
   - approve with corrections
   - reject
9. If you recommend corrections, make them concrete with exact file paths and line references where possible.

At the top of your output, include a short section called `Context Check` listing every required memo and code file above and confirming you read it.

Save the audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Audit_Rerun_2026-04-04.md`
