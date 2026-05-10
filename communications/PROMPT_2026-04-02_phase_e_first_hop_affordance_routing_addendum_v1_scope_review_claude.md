# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_scope.md`

Do not assume the memo is correct.
Test whether it is now the right immediate next analyzer-side tranche after the completed bridge-hint consolidation closeout and the completed Close Read operations/routing inventory companion.

## What to do

1. Read the scope memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
3. Scrutinize the memo against the actual codebase, especially:
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
   - nearby presenter / schemas / transient compose files that materially govern where optional view metadata can be attached without changing host behavior
4. Check the memo against the strongest product/runtime evidence:
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/research/ResearchCard.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/research/ResearchAnswer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchComments.tsx`
5. Read relevant recent memos and reviews in `communications/`, especially:
   - `communications/REPORT_Claude_Phase_E_Bridge_Hint_Consolidation_V1_Scope_Critique_2026-04-01.md`
   - `communications/REPORT_Codex_Phase_E_Bridge_Hint_Consolidation_V1_Scope_Audit_2026-04-01.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Is a first-hop affordance/routing addendum really the right immediate next analyzer-side slice after bridge-hint consolidation?
- Is `TransientIntentView` the right first attachment surface, or is there a smaller and stronger seam?
- Is `src/presenter/compose_from_intent.py::_to_transient_view(...)` the right explicit population point for this v1 field?
- Is the proposed v1 field family:
  - `capturable`
  - bounded `allowed_destinations`
  actually the right smallest honest starting set?
- Is dropping `commentable` from v1 the right call, given the current transient analytical compose line and the stronger product-side evidence?
- Does the memo correctly frame this as a seam-establishment exercise where eligible proved leaf views may initially carry uniform values?
- Is the memo honest enough about `allowed_destinations` being a deliberate subset of the inventory rather than the whole inventory surface?
- Does the memo correctly keep destination lifecycle, findings-specific flows, research-answer-specific routing, and host UX out of scope?
- Does the memo preserve the right ownership split:
  - analyzer-v2 annotates semantic affordances and destination eligibility
  - hosts operationalize the actual UX and post-click behavior
- Is the migrated-family / leaf-only / non-proved-workflow boundary explicit and defensible enough?
- Is the memo too optimistic about how much can be inferred analyzer-side from current transient analytical surfaces?
- Does the memo name the necessary transient hash / fingerprint coverage for the new field clearly enough?
- Does the memo keep output shapes and proof surfaces stable enough?
- Is there a smaller or stronger immediate slice than this one?
- Does the memo frame the relationship between this addendum, the Close Read flagship direction, and the broader analyzer-v2-as-brain objective correctly?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_First_Hop_Affordance_Routing_Addendum_V1_Scope_Critique_2026-04-02.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The strongest parts of the memo
3. The weakest assumptions
4. Code-backed findings
5. Strategic implications for the roadmap
6. Concrete corrections or reframing you recommend

Keep the critique specific and unsentimental.
Do not produce fluff.
