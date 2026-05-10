Please audit this scoping memo:

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

Also verify the live deployed Render state directly. Do not rely only on local code.

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

Audit goals:

1. Verify whether the memo correctly identifies the next gap as live deployment/authority/cutover rather than more local design work.
2. Stress-test whether the local code and docs really justify moving to a deployment tranche now.
3. Check whether the memo correctly preserves the analyzer-v2 type discipline:
   - engines
   - operationalizations
   - chains
   - workflows
   - transformations
4. Examine whether the memo is concrete enough about the operator-console law in analyzer-mgmt.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Does the codebase support the claim that the missing work is now live deployment and cutover, not more local concept-runtime invention?
- Is the memo right to treat deployment of analyzer-v2 and analyzer-mgmt as scope, not follow-up cleanup?
- Does the memo now make `git add` / commit / push / deploy a hard enough gate given that some concept-runtime files are still untracked locally?
- Does the memo correctly preserve `implementations/[key]` as the canonical composition page until workflow detail is fully sufficient?
- Does it make workflow-to-transformation linkage concrete enough?
- Does it correctly fold jobs/result-boundary into the operator trail requirement?
- Does it make live analyzer-mgmt validation concrete enough to require real browser rendering of engine/chain/transformation pages rather than only HTTP availability?
- Is the bounded Critic cutover scoped tightly enough to `inferential` and `logical`, with cross-corpus and broader cache cleanup deferred?
- Does the memo correctly break out the-critic deployment as a separate dependency from analyzer-v2/analyzer-mgmt deployment?
- Does the memo stay properly narrower than broader Close Read composition-layer work and UI expansion?
- Is there any place where the memo quietly assumes the Render deployment has already happened?
- Is the live browser-acceptance path concrete enough to prove analyzer-v2 is truly the authority for the admitted concept submodes, including:
  - job/result-boundary/operator-link checks
  - logical scrutiny derived only from translated analyzer-v2-backed data
  - `_analysis_provenance.execution_owner == "analyzer-v2"` on the persisted logical result?

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the audit to this exact file:

- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Live_Authority_Deployment_And_Cutover_Scope_Audit_2026-04-06.md`
