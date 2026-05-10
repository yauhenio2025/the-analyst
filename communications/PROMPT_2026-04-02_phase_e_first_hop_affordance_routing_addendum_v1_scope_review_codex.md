# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the current codebase, the recent bridge-hint consolidation closeout, the Close Read operations/routing inventory, and the larger analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
3. Check the memo against the relevant analyzer code and tests:
   - `src/presenter/schemas.py`
   - `src/presenter/compose_from_intent.py`
   - `src/presenter/composition_role_registry.py`
   - `src/presenter/composition_source_bridge.py`
   - `src/orchestrator/genealogy_saved_result_bridge.py`
   - `src/engines/discovery.py`
   - `src/presenter/manifest_builder.py`
   - `src/presenter/presentation_api.py`
   - `tests/test_compose_from_intent.py`
   - `tests/test_representative_composition_matrix.py`
   - `tests/test_transient_proof_harness_contract.py`
   - `tests/test_compose_sessions.py`
4. Check the memo against the runtime/product evidence it depends on:
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/research/ResearchCard.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/research/ResearchAnswer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchComments.tsx`
   - nearby Critic files that materially govern capture, comment persistence, Arsenal routing, and research-todo routing
5. Read relevant recent roadmap/review context:
   - `communications/REPORT_Claude_Phase_E_Bridge_Hint_Consolidation_V1_Scope_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Phase_E_Bridge_Hint_Consolidation_V1_Scope_Audit_2026-04-01.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is a first-hop affordance/routing addendum the right immediate next analyzer-side slice after bridge-hint consolidation?
- Is `TransientIntentView` the right first attachment surface, or is there a smaller and stronger seam?
- Is `src/presenter/compose_from_intent.py::_to_transient_view(...)` the right shared population point for this v1 field?
- Does the memo correctly keep the v1 affordance family bounded to:
  - `capturable`
  - bounded `allowed_destinations`
- Are `arsenal` and `research_todo` the right only allowed destinations for this first slice?
- Is dropping `commentable` from v1 the right move for honesty on the current transient analytical line?
- Does the memo correctly frame this as a seam-establishment slice where eligible proved leaf views may initially carry uniform values?
- Does it clearly state that `allowed_destinations` is a deliberate subset of the broader inventory rather than the full first-hop surface?
- Does the memo correctly defer destination lifecycle, findings-specific flows, research-answer-specific routing, and host UX?
- Does it preserve thin-host architecture honestly, or does it smuggle host-local behavior upstream?
- Is the proposed leaf-surface / container-surface distinction concrete enough to implement and test?
- Is the migrated-family / non-proved-workflow emission boundary explicit and defensible enough?
- Does the memo preserve transient hash / fingerprint honesty for the new field strongly enough?
- Does the memo preserve output shapes and current proof surfaces honestly enough?
- Is there a smaller and stronger immediate slice than this one?
- What should change in the roadmap ordering after the bridge-hint consolidation closeout?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_First_Hop_Affordance_Routing_Addendum_V1_Scope_Audit_2026-04-02.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The memo's strongest code-backed points
3. The memo's weakest or overstated assumptions
4. Any factual discrepancies you found
5. What this changes for the larger roadmap
6. The most defensible next move after this memo

Be concrete. Use code-backed reasoning. Avoid fluff.
