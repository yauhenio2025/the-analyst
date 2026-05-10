Please review this implementation scope memo in full:

- `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`

Before concluding, read all of these in full. Do not skip any:

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
- `/home/evgeny/projects/the-critic/api/database.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py`
- `/home/evgeny/projects/the-critic/analyzer/extract.py`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/closeReadConceptRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CloseReadFamilySwitcher.tsx`

What I need from you:

1. Test the robustness of the scope memo’s assumptions.
2. Examine them in light of the bigger Close Read vision and the analyzer-v2-as-brain roadmap.
3. Scrutinize the memo’s claims against the actual codebase, not just the memo text.
4. Evaluate whether this is the right next implementation tranche, or whether it still leaves a more prior blocker unresolved.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Is the memo right that the current blocker is runtime enablement rather than more Close Read concept UI work?
- Does the memo correctly identify two separate seams:
- Does the memo correctly identify the full runtime seam set:
  - project-awareness of `inferential` / `logical`
  - backend-neutral persistence for detected concepts, concept analyses, and logical scrutiny
- Is it correct to keep the current Close Read concept route contract fixed in this tranche?
- Does the memo correctly reject “just switch local development to Postgres” as a sufficient product/runtime fix?
- Is the proposed reuse seam correct:
  - load documents in the API via `load_documents(project_id)`
  - inject them into the core analyzers
  - avoid teaching the analyzers to query the database directly
- Does the memo overstate how easy it is to genericize the current inferential/logical prompts away from the Benanav/Morozov corpus?
- Does the memo adequately acknowledge the deeper hardcodings inside the 12-phase logical pipeline, not just the top-level inferential prompt?
- Is the memo right to keep this tranche narrower than a full analyzer-v2-native migration?
- Is the memo right to bring scrutiny persistence/readback into the same runtime-normalization pass?
- Does the memo name `get_sync_session()` / `sync_session_maker` from `database.py` as the right reuse target for persistence normalization?
- Is the fresh-project acceptance path concrete enough?
- Does the fresh-project acceptance path include enough verification for the admitted logical scrutiny feature?
- Does this scope preserve the roadmap distinction between:
  - default family completion
  - later composition-layer work
  - later standalone-host work

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Fresh_Project_Runtime_Scope_Critique_2026-04-06.md`
