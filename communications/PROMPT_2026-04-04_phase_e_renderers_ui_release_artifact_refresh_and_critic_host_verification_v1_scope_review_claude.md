Please review this scope memo:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_scope.md`

Before you conclude, read all of these in full. Do not skip any of them:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_completion.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
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

What I need from you:

1. Test the robustness of the memo’s assumptions.
2. Examine them against the bigger picture and the analyzer-v2-as-brain objective.
3. Scrutinize the memo’s claims against the actual codebase, not just the memo text.
4. Pressure-test the proposed next step:
   - Is the package-source implementation genuinely complete already?
   - Is the stale packed-host consequence real on the current Critic path?
   - Is a version bump plus new tarball the right minimal handoff, given `release-pack.mjs` refuses overwriting an existing tarball?
   - Is this slice still bounded, or does it risk drifting into broader host-delivery posture work?
5. Evaluate the verification plan:
   - Is it honest about what package build / pack proves?
   - Does it require enough host-level proof on the two material nested genealogy surfaces?
   - Does it make `package-lock.json` part of the explicit dependency-refresh surface?
   - Does it require at least one proof per affected surface that goes through the actual installed package path rather than only mocked host tests?
   - If the current repo lacks exact proofs for those surfaces, is the proposed minimum test expansion still bounded?
6. Give a clear verdict:
   - approve
   - approve with corrections
   - reject
7. If you recommend corrections, make them concrete and implementation-relevant.

Check these points explicitly:

- The memo does not treat package-source implementation as still pending.
- The memo does not overclaim that refreshing the artifact settles broader host-delivery posture.
- The memo keeps `_firstHopAffordance`, workflow/job requiredness, `currentRendererCapture`, and destination-policy law out of this slice.
- The memo’s rationale for a new artifact/version is grounded in `release-pack.mjs`, not preference alone.
- The memo’s host consequence remains tied to the real nested genealogy surfaces that motivated the decision gate.
- The memo’s verification plan does not treat mocked host tests as sufficient proof of the installed-package fix.

At the top of your output, include a short section called `Context Check` listing every required memo and code file above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Phase_E_Renderers_UI_Release_Artifact_Refresh_And_Critic_Host_Verification_V1_Scope_Critique_2026-04-04.md`
