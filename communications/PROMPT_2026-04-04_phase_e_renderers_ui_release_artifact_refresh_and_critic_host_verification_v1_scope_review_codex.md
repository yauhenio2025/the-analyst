Please audit this scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_scope.md`

Before you conclude, read all of these in full. Do not skip any:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_completion.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md`
- `communications/REPORT_Codex_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Audit_Rerun_2026-04-04.md`
- `communications/REPORT_Claude_Phase_E_Renderers_UI_Nested_Capture_Forwarding_Normalization_Implementation_V1_Scope_Critique_Rerun_2026-04-04.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

Inspect these code files directly:

- `renderers-ui/package.json`
- `renderers-ui/scripts/release-pack.mjs`
- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/dispatch/SubRendererDispatch.tsx`
- `renderers-ui/src/utils/captureBase.ts`
- `renderers-ui/release-artifacts/the-syllabus-analysis-renderers-0.6.5.tgz`
- `/home/evgeny/projects/the-critic/webapp/package.json`
- `/home/evgeny/projects/the-critic/webapp/package-lock.json`
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/package.json`
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/AccordionRenderer.js`
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/renderers/CardRenderer.js`
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/dist/dispatch/SubRendererDispatch.js`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
- `src/views/definitions/genealogy_target_profile.json`
- `src/views/definitions/genealogy_per_work_scan.json`

Audit goals:

1. Verify every code-level claim in the memo against the actual codebase and installed host package.
2. Confirm or refute:
   - the forwarding patch is already present in local `renderers-ui` source
   - the Critic consumer still points at a stale `0.6.5` tarball
   - the installed `node_modules` dist still reflects the old omission paths
   - `release-pack.mjs` really forces a new version / tarball rather than overwrite
3. Check whether the scope names the right next step:
   - traceable artifact refresh
   - Critic dependency refresh
   - focused host verification
   - not broader host-delivery redesign
4. Stress-test the verification plan:
   - is it sufficient to prove the two material nested genealogy consequences are cleared?
   - does it explicitly include `package-lock.json` in the dependency-refresh surface?
   - does it require at least one proof per affected genealogy surface that exercises the actual installed package path rather than only mocked host tests?
   - does it remain bounded if new host tests are needed?
5. Evaluate the memo against the bigger roadmap:
   - does this still fit the short corridor toward lean `Close Read V1` honestly?
   - does any part still overclaim package or host convergence?
6. If useful, rerun focused non-destructive verification:
   - `cd renderers-ui && npm run build`
   - `cd renderers-ui && node scripts/check-capture-base.mjs`
   - any spot-check needed on the installed Critic package files
7. Give a clear verdict:
   - approve
   - approve with corrections
   - reject
8. If you recommend corrections, make them concrete with exact file paths and line references where possible.

At the top of your output, include a short section called `Context Check` listing every required memo and code file above and confirming you read it.

Save the audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Renderers_UI_Release_Artifact_Refresh_And_Critic_Host_Verification_V1_Scope_Audit_2026-04-04.md`
