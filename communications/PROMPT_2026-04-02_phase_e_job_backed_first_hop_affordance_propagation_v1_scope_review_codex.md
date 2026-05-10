# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the current codebase, the completed transient first-hop affordance closeout, the Close Read operations/routing inventory, and the larger analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_scope.md`
   - `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
   - `communications/REPORT_Claude_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Critique_2026-04-02.md`
3. Check the memo against the relevant analyzer code and tests:
   - `src/presenter/schemas.py`
   - `src/presenter/compose_from_intent.py`
   - `src/presenter/manifest_builder.py`
   - `src/presenter/presentation_api.py`
   - `src/presenter/decision_trace.py`
   - `tests/test_compose_from_intent.py`
   - `tests/test_representative_composition_matrix.py`
   - `tests/test_manifest_trace.py`
   - `tests/test_presentation_api.py`
   - `tests/test_analysis_product_contract.py`
4. Check the memo against the runtime/product evidence it depends on:
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - nearby Critic files that materially govern job-backed rendering plus capture/routing actions
5. Read relevant recent roadmap/review context:
   - `communications/REPORT_Claude_Phase_E_First_Hop_Affordance_Routing_Addendum_V1_Scope_Critique_2026-04-02.md`
   - `communications/REPORT_Codex_Phase_E_First_Hop_Affordance_Routing_Addendum_V1_Scope_Audit_2026-04-02.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is job-backed first-hop affordance propagation the right immediate next analyzer-side slice after the transient closeout?
- Is it genuinely smaller and stronger than jumping to one output-specific affordance family?
- Is the memo right to keep the semantics fixed and vary only the surface contract?
- Should the shared affordance model be generalized now, or is that a premature rename/extraction?
- Are `ViewPayload` and `EffectiveManifestView` the right attachment surfaces?
- Is the memo now precise enough that the shared helper should run after `_prepare_page_payloads(...)` returns and before `build_effective_manifest(...)` processes payloads?
- Is the job-backed eligibility rule concrete enough, given that there is no transient `handoff_kind` here and the gate must use `workflow_key` plus migrated analytical leaf shape?
- Does the memo correctly preserve the narrow emission boundary:
  - approved workflow-key families only
  - migrated-family analytical leaf views only
  - parent/container views unannotated
  - non-migrated / non-proved workflows unannotated
- Does the memo correctly keep the bounded field family fixed to:
  - `capturable`
  - `allowed_destinations=["arsenal","research_todo"]`
- Does it correctly defer:
  - `commentable`
  - findings-specific promotion
  - research-answer routing
  - outline routing
  - destination lifecycle
- Does the memo preserve thin-host architecture honestly, or does it smuggle host-local behavior upstream?
- Does the memo correctly handle the contract-identity consequences for:
  - `presentation_hash`
  - `presentation_content_hash`
  - `_manifest_identity_row(...)`
  - `build_effective_manifest`
  - `assemble_page`
  - `build_presentation_manifest`
  - `build_presentation_trace`
- Does the memo now treat `PagePresentation` vs `EffectivePresentationManifest` honestly enough:
  - `PagePresentation.views` as the real host-facing surface
  - `EffectivePresentationManifest.views` as mainly a contract/hash and adjacent trace/reuse surface?
- Does the memo correctly treat decision trace as a supporting obligation rather than a primary new surface, while still requiring `_diff_snapshots(...)` coverage for the new field?
- Is there a smaller and stronger immediate slice than this one?
- What should change in the roadmap ordering after the transient first-hop affordance closeout?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Audit_2026-04-02.md`

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
