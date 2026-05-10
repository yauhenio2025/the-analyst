Please review this scope memo in full:

- `communications/MEMO_2026-04-04_close_read_v1_scope.md`

Before you conclude, read all of these in full. Do not skip any of them, even if some seem overlapping:

- `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_completion.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Inspect these code files directly:

- `src/views/definitions/genealogy_target_profile.json`
- `src/views/definitions/genealogy_per_work_scan.json`
- `src/views/definitions/genealogy_portrait.json`
- `src/views/definitions/genealogy_idea_evolution.json`
- `/home/evgeny/projects/the-critic/webapp/package.json`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/InstalledPackageNestedCapture.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`

What I need from you:

1. Test the robustness of the memo's assumptions.
2. Examine them in light of the bigger picture and the analyzer-v2-as-brain objective.
3. Scrutinize the memo's claims against the actual codebase, not just the memo text.
4. Pressure-test the proposed `Close Read V1` boundary:
   - Is genealogy really the strongest honest center of gravity for V1?
   - Is a bounded Critic-hosted pilot the right default posture, or does the code reality point elsewhere?
   - Is the memo honest about what current runtime evidence supports for first-hop operations and destinations?
   - Does the memo resolve app-layer eligibility at the right layer, or is it still smuggling in substrate assumptions?
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject
6. If you recommend corrections, make them concrete and implementation-relevant.

Check these points explicitly:

- The memo does not treat renderer-substrate work as still blocking product scoping.
- The memo does not overclaim full product readiness.
- The memo keeps V1 below:
  - Book Modeler
  - destination-internal lifecycle unification
  - workflow-neutral destination taxonomy
  - generic renderer-package capture law
  - multi-user / multi-project architecture
- The memo grounds V1 in current real destinations only:
  - Arsenal
  - Research todo
- The memo names host-delivery posture and app-layer first-hop eligibility as explicit product questions rather than pretending they are already solved by the substrate.

At the top of your output, include one short section called `Context Check` listing every required memo above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Close_Read_V1_Scope_Critique_2026-04-04.md`
