Please review this scoping memo in full:

- `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_deployment_and_cutover_scope.md`

Before concluding, read all of these in full. Do not skip any:

- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_runtime_authority_and_analyzer_mgmt_visibility_scope.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_local_visibility_and_operator_trail_completion.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_local_analyzer_v2_visibility_slice.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

Inspect these code files directly:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_by_ref.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/workflows/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/workflows/registry.py`
- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/concept_inferential_single_concept.json`
- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/concept_logical_single_concept.json`
- `/home/evgeny/projects/analyzer-v2/src/transformations/definitions/concept_inferential_host_contract_extraction.json`
- `/home/evgeny/projects/analyzer-v2/src/transformations/definitions/concept_logical_host_contract_extraction.json`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/lib/api.ts`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/implementations/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/workflows/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/jobs/[id].tsx`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py`

Also check the live deployed Render state directly. Do not rely only on local code.

Check these URLs explicitly:

- `https://analyzer-v2.onrender.com/v1/meta/definitions-version`
- `https://analyzer-v2.onrender.com/v1/workflows`
- `https://analyzer-v2.onrender.com/v1/transformations`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref`
- `https://analyzer-mgmt-frontend.onrender.com/implementations`
- `https://analyzer-mgmt-frontend.onrender.com/workflows`
- `https://analyzer-mgmt-frontend.onrender.com/transformations`
- `https://analyzer-mgmt-frontend.onrender.com/engines/inferential_commitment_mapper`
- `https://analyzer-mgmt-frontend.onrender.com/chains/concept_analysis_12_phase`

What I need from you:

1. Test the robustness of the memo’s assumptions.
2. Examine them in light of the bigger `analyzer-v2 as the brain` objective and the broader Close Read roadmap.
3. Scrutinize the memo’s claims against the live deployed server, analyzer-mgmt on Render, and the actual codebase.
4. Evaluate whether this is the right next operational tranche after the local visibility/operator-trail completion.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Is the memo right that the next gap is now deployment/live authority/cutover rather than more local concept-runtime design?
- Does the codebase support the claim that the local prerequisites are in place for a live deployment tranche?
- Does the memo make it explicit enough that several concept-runtime files are still untracked locally and must be `git add`ed before any commit/deploy claim is honest?
- Does the memo correctly keep the tranche inside existing analyzer-v2 types instead of reopening the substrate question?
- Is the operator-console law now concrete enough:
  - `implementations/[key]` as canonical composition page until `workflows/[key]` is sufficient
  - explicit workflow-to-transformation linkage
  - jobs/result-boundary linked back into the same operator trail?
- Does the memo make analyzer-mgmt live validation concrete enough to require actual browser rendering of engine/chain/transformation pages rather than just SPA-shell HTTP 200?
- Does the memo overstate readiness for Critic thinning, or is the bounded `inferential` / `logical` cutover now the right next host move?
- Is the Phase 4 Critic cutover broken down clearly enough into execution cutover, scrutiny cutover, and separate the-critic deployment dependency?
- Does the memo stay properly narrower than:
  - new concept submodes
  - broader composition-layer work
  - new Close Read UI work
  - standalone Close Read host work?
- Is there any place where the memo still confuses local proof with live deployed authority?
- Does the memo make deployment itself part of scope strongly enough, or does it still read like deploy is optional cleanup?
- Is the live browser-acceptance requirement concrete enough, especially for:
  - job/result-boundary/operator-link validation
  - logical scrutiny deriving only from translated data
  - `_analysis_provenance.execution_owner == "analyzer-v2"` on the persisted logical result?

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Live_Authority_Deployment_And_Cutover_Scope_Critique_2026-04-06.md`
