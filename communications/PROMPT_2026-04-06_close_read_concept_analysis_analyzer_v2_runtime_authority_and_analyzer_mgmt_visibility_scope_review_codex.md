Please audit this scoping memo:

- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_runtime_authority_and_analyzer_mgmt_visibility_scope.md`

Before concluding, read all of these in full. Do not skip any:

- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

Inspect these code files directly:

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py`
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/`
- `/home/evgeny/projects/analyzer-v2/src/transformations/definitions/`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/engines/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/workflows/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/implementations/index.tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/implementations/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/transformations/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/jobs/[id].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/lib/api.ts`

Also verify the live deployed Render state directly. Do not rely only on local code.

Check these URLs explicitly:

- `https://analyzer-v2.onrender.com/v1/meta/definitions-version`
- `https://analyzer-v2.onrender.com/v1/engines`
- `https://analyzer-v2.onrender.com/v1/chains`
- `https://analyzer-v2.onrender.com/v1/operationalizations`
- `https://analyzer-v2.onrender.com/v1/workflows`
- `https://analyzer-v2.onrender.com/v1/transformations`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref`
- `https://analyzer-mgmt-frontend.onrender.com/engines/inferential_commitment_mapper`
- `https://analyzer-mgmt-frontend.onrender.com/chains/concept_analysis_12_phase`
- `https://analyzer-mgmt-frontend.onrender.com/operationalizations/inferential_commitment_mapper`
- `https://analyzer-mgmt-frontend.onrender.com/workflows`
- `https://analyzer-mgmt-frontend.onrender.com/implementations`
- `https://analyzer-mgmt-frontend.onrender.com/transformations`

Audit goals:

1. Verify whether the memo correctly identifies the live gap as workflow/transformation/orchestrator deployment rather than missing concept-analysis capability primitives.
2. Stress-test the claim that we can and should stay inside existing analyzer-v2 types:
   - engines
   - operationalizations / passes / stances / depths
   - chains
   - workflows
   - transformations
3. Check whether the memo correctly turns analyzer-mgmt into the canonical visibility/editability console rather than inventing a new admin layer.
4. Examine whether the memo is honest about what Critic must stop owning if analyzer-v2 is to become the real runtime authority.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Does the live Render server already prove that the core concept-analysis primitives exist?
- Is the memo right that the missing live layer is:
  - concept workflows
  - concept host-contract transformations
  - bounded concept orchestrator route
  rather than missing engines/chains?
- Does the memo correctly avoid inventing new substrate types?
- Is the proposed analyzer-mgmt visibility law concrete enough, or does it still leave an ambiguous operator surface?
- Does the memo adequately account for the fact that analyzer-mgmt already fails to render some concept assets that are live in the analyzer-v2 API?
- Does the memo require a concrete chain-aware workflow visibility rule and explicit workflow-to-transformation linkage, or is that still too implicit?
- Does the memo correctly identify what Critic should still own versus stop owning?
- Does the memo correctly require commit/push/deploy of the local-only concept workflow/transformation/orchestrator files before calling analyzer-v2 the live authority?
- Is the “analyzer-v2 produces translated host-contract artifacts” move the right next step, or does the code suggest a more prior blocker?
- Is the Phase D Critic-thinning story bounded tightly enough to the two admitted submodes, with cross-corpus concept analysis and broader legacy cache cleanup explicitly deferred?
- Does the memo stay properly narrower than:
  - broader module-composition work
  - new Close Read UI work
  - standalone Close Read host work?
- Is there any place where the memo quietly treats local code existence as equivalent to deployed analyzer authority?

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the audit to this exact file:

- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Analyzer_V2_Runtime_Authority_And_Analyzer_Mgmt_Visibility_Scope_Audit_2026-04-06.md`
