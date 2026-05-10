Please audit this scoping memo:

- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md`

Before concluding, read all of these in full. Do not skip any:

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

Inspect these code and capability files directly:

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json`

Audit goals:

1. Verify whether the memo correctly reframes the next phase as analyzer-v2 recomposition rather than “move/build the capabilities from scratch.”
2. Stress-test the claim that current Critic concept execution is still too locally owned to satisfy the analyzer-v2-as-brain objective.
3. Check whether the memo keeps the host/product boundary stable while shifting runtime ownership.
4. Evaluate whether parity audit + adapter/translation is the right bounded answer for inferential and logical, especially the chain-backed logical path.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Is the memo right that analyzer-v2 already has enough inferential/logical capability definition to justify rebasing rather than reinvention?
- Does the code support the memo’s claim that inferential and logical should be treated as two distinct rebasing problems?
- Does the memo correctly keep Close Read/native concept routes fixed in this tranche?
- Is the parity-audit requirement concrete enough, or does it still leave a more prior design ambiguity unresolved?
- Does the memo overstate the ease of translating analyzer-v2 outputs into current Critic rendering contracts?
- Is the logical scrutiny compatibility question scoped correctly, or does the memo leave too much unresolved there?
- Does this scope stay properly narrower than:
  - analyzer-v2-native migration of every concept submode
  - general module-composition work
  - standalone Close Read host work?
- Is there any place where the memo contradicts the larger default-families-plus-composable-modules roadmap?

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

If useful, you may rerun focused non-destructive inspections, but keep the audit primarily code-backed and roadmap-focused.

Save the audit to this exact file:

- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Analyzer_V2_Recomposition_Scope_Audit_2026-04-06.md`
