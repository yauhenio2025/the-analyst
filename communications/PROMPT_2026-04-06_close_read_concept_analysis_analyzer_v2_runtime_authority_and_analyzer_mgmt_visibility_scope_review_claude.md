Please review this scoping memo in full:

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

Also check the live deployed Render state directly. Do not rely only on local code.

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

What I need from you:

1. Test the robustness of the memo’s assumptions.
2. Examine them in light of the bigger `analyzer-v2 as the brain` objective and the broader Close Read roadmap.
3. Scrutinize the memo’s claims against the live deployed server, analyzer-mgmt on Render, and the actual codebase.
4. Evaluate whether this is the right next operational tranche after the recomposition scope.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Does the live Render evidence support the memo’s claim that the missing layer is deployment/authority/visibility rather than missing capability primitives?
- Is it right to insist on staying within existing analyzer-v2 types rather than inventing a new concept-runtime abstraction?
- Does the memo correctly assign authority to:
  - analyzer-v2 for execution, composition, provenance, and translated artifacts
  - analyzer-mgmt for visibility/editability
  - Critic for thin launch/poll/fetch/render behavior?
- Is the analyzer-mgmt visibility requirement concrete enough, or does it still leave too much hand-wavy about where a human operator would actually look and edit?
- Does the memo adequately account for the current live analyzer-mgmt failures on concept assets that do exist in analyzer-v2?
- Does the memo now make chain-backed workflow visibility and workflow-to-transformation linkage concrete enough to support the “canonical operator console” claim?
- Does the memo overstate how quickly Critic can be stripped back, given the current server and recomposition code?
- Does the memo correctly require commit/push/deploy of the local-only concept workflow/transformation/orchestrator files before treating local existence as live authority?
- Is “translated host-contract artifacts owned by analyzer-v2” the right next architectural move, or is there a more prior seam that still needs to be solved first?
- Is the Phase D Critic-thinning scope bounded tightly enough to the admitted `inferential` and `logical` seams, with cross-corpus concept analysis and broader legacy caches deferred?
- Does the memo stay correctly narrower than:
  - adding new concept submodes
  - general module-composition work
  - new Close Read UI work
  - standalone Close Read host work?
- Is there any place where the memo confuses local implementation evidence with live deployed authority?

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Analyzer_V2_Runtime_Authority_And_Analyzer_Mgmt_Visibility_Scope_Critique_2026-04-06.md`
