# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_scope.md`

Do not assume the memo is correct.
Test whether this is now the right immediate next analyzer-side tranche after the completed transient first-hop affordance addendum closeout.

## What to do

1. Read the scope memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`
   - `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_scope.md`
   - `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`
   - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
   - `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
   - `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
   - `communications/REPORT_Codex_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Audit_2026-04-02.md`
3. Scrutinize the memo against the actual codebase, especially:
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
   - nearby presenter / schemas files that materially govern how job-backed view metadata propagates into `EffectivePresentationManifest` and `PagePresentation`
4. Check the memo against the strongest host/runtime evidence:
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
5. Read relevant recent memos and reviews in `communications/`, especially:
   - `communications/REPORT_Claude_Phase_E_First_Hop_Affordance_Routing_Addendum_V1_Scope_Critique_2026-04-02.md`
   - `communications/REPORT_Codex_Phase_E_First_Hop_Affordance_Routing_Addendum_V1_Scope_Audit_2026-04-02.md`
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Is job-backed first-hop affordance propagation really the right immediate next analyzer-side slice after the transient closeout?
- Is it smaller and stronger than jumping straight to one output-specific affordance family?
- Is the memo right to keep the semantics fixed and vary only the surface contract?
- Is a shared affordance model across transient and job-backed surfaces the right move, or does that widen the change too early?
- Are `ViewPayload` and `EffectiveManifestView` the right attachment surfaces?
- Is the memo now precise enough that population should happen after `_prepare_page_payloads(...)` returns and before `build_effective_manifest(...)` finalizes hashes?
- Is the job-backed eligibility rule concrete enough, given that there is no transient `handoff_kind` on this line and the gate must use `workflow_key` plus migrated analytical leaf shape?
- Does the memo correctly preserve the same narrow emission boundary:
  - migrated-family analytical leaf views only
  - parent/container views unannotated
  - non-migrated / non-proved workflows unannotated
- Is keeping `capturable + allowed_destinations=["arsenal","research_todo"]` fixed the right discipline for this slice?
- Does the memo correctly defer:
  - `commentable`
  - findings-specific promotion semantics
  - research-answer specific routing
  - outline routing
  - destination lifecycle
- Does the memo preserve thin-host architecture honestly, or does it start smuggling host-local workflow law into the presenter?
- Does the memo name the necessary job-backed hash / fingerprint consequences clearly enough?
- Does the memo now handle the `PagePresentation` vs `EffectivePresentationManifest` distinction honestly enough:
  - `PagePresentation.views` as the real host-facing surface
  - `EffectivePresentationManifest.views` as mainly a contract/hash and adjacent trace/reuse surface today?
- Does the memo underestimate any knock-on effects on:
  - `presentation_hash`
  - `presentation_content_hash`
  - `build_presentation_manifest`
  - `assemble_page`
  - `_manifest_identity_row(...)`
  - decision-trace snapshots and `_diff_snapshots(...)`
- Is there a smaller or stronger next slice than this one?
- Does the memo correctly frame the relationship between this propagation slice, the Close Read flagship direction, and the broader analyzer-v2-as-brain objective?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_Job_Backed_First_Hop_Affordance_Propagation_V1_Scope_Critique_2026-04-02.md`

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
