Please review this scoping memo in full:

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

What I need from you:

1. Test the robustness of the memo’s assumptions.
2. Examine them in light of the bigger Close Read roadmap and the analyzer-v2-as-brain objective.
3. Scrutinize the memo’s claims against the actual codebase and capability definitions, not just the memo text.
4. Evaluate whether this is the right next architectural phase after the fresh-project runtime tranche.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Is the memo right that the next move should be framed as recomposition/rebinding rather than capability invention?
- Does the code actually support the claim that analyzer-v2 already has the decisive building blocks for this family:
  - inferential engine definition
  - inferential operationalization/pass structure
  - concept-analysis chain/suite
- Does the memo correctly distinguish the two rebasing problems:
  - inferential as an engine/operationalization rebinding problem
  - logical as a chain-level recomposition problem?
- Is it right to keep the current Close Read and native Critic host contracts fixed during this tranche?
- Does the memo correctly preserve the roadmap distinction between:
  - fresh-project runtime truth
  - analyzer-v2 recomposition
  - later composition-layer work
  - later standalone-host work?
- Does the memo overstate how close analyzer-v2 outputs already are to the current Critic host/result contracts?
- Is the proposed parity-audit-plus-adapter approach the right bounded answer, or does the code suggest a more prior blocker still exists?
- Does the memo correctly keep scrutiny narrower than the broader ammunition/send-to-outline estate while still requiring compatibility with rebased logical outputs?
- Is the memo honest about the likely remaining dependence on host-local translation or normalization for the logical path?
- Is there any place where the memo quietly slips back into treating Critic-local analyzers as canonical instead of transitional?

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Analyzer_V2_Recomposition_Scope_Critique_2026-04-06.md`
