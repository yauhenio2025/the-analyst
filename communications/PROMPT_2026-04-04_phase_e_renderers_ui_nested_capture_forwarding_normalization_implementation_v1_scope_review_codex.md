Please audit this scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_scope.md`

Before you conclude, read all of these in full. Do not skip any of them:

- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md`
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Decision_V1_Scope_Critique_2026-04-04.md`
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Decision_V1_Scope_Audit_2026-04-04.md`
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
- `the-critic/webapp/package.json` (at `/home/evgeny/projects/the-critic/webapp/package.json`)
- `the-critic/webapp/src/components/V2TabContent.tsx` (at `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`)
- `the-critic/webapp/src/lib/currentRendererCapture.ts` (at `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`)
- `the-critic/webapp/src/components/CaptureActionBar.tsx` (at `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`)
- `the-critic/webapp/src/contexts/CaptureContext.tsx` (at `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`)

What I need from you:

1. Verify every code-level claim in the memo against the actual codebase. Do not trust the memo text alone.
2. Confirm or refute:
   - AccordionRenderer `captureForward` at lines 516-523 omits `_captureSourceType` and `_captureEntityId` — check the actual code
   - AccordionRenderer `nested_sections` path at line 555 passes no capture config to GenericSectionRenderer — check the actual code
   - AccordionRenderer fallback path at line 569 passes no capture config — check the actual code
   - CardRenderer subsection dispatch at lines 339-378 has zero capture forwarding on all four branches — check the actual code
   - GenericSectionRenderer at line 197 passes `subHint.config || {}` to resolved sub-renderers with no capture fields — check the actual code
   - `genealogy_target_profile.json` uses `nested_sections` in its section_renderers — check the actual JSON
   - `genealogy_per_work_scan.json` uses `renderer_type: "card"` with subsections that use `nested_sections` — check the actual JSON
   - `CaptureContext.tsx` uses `source_type === 'genealogy'` for `genealogy_job_id` fallback — check the actual code
3. Check if there are any OTHER forwarding gaps the memo misses. Specifically:
   - Does CardGridRenderer have any nested dispatch that needs normalization? (The memo claims it does not.)
   - Are there other callers of GenericSectionRenderer that would need the captureConfig prop?
   - Do any other view definitions use `nested_sections` in ways that would expose the gap?
4. Evaluate whether the proposed GenericSectionRenderer extension is minimal enough. Specifically:
   - Does adding `captureConfig` prop introduce any new behavior beyond pass-through?
   - Does spreading captureConfig into sub-renderer configs risk overwriting any existing config fields?
   - Are the recursive GenericSectionRenderer calls correctly identified?
5. Examine the scope against the bigger picture:
   - Is this still appropriate Phase E substrate work, or has it drifted into product design?
   - Does the anti-drift Rule 1 from the fixed-direction roadmap support this slice?
   - Is the deferred list complete?
6. Run the following verification if possible:
   - `cd renderers-ui && npm run build`
   - `cd renderers-ui && node scripts/check-capture-base.mjs`
7. Give a clear verdict:
   - approve
   - approve with corrections
   - reject
8. If you recommend corrections, make them concrete with exact file paths and line numbers.

At the top of your output, include a short section called `Context Check` listing every required memo and code file above and confirming you read it.

Save the audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Audit_2026-04-04.md`
