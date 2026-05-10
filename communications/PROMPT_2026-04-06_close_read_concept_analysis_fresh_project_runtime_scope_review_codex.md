Please audit this implementation scope memo:

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

Audit goals:

1. Verify whether this memo correctly identifies the next real blocker after the concept-family host tranche.
2. Stress-test the proposed project-aware runtime seam for `inferential` / `logical` against the current codebase.
3. Check whether the persistence-normalization proposal is honest about the current SQLite/Postgres split in the API.
4. Evaluate whether the scope stays properly bounded or drifts into analyzer-v2-native migration, UI redesign, or broader composition-layer work.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Is the memo right that the current `Close Read` concept family host shell is live enough, and that the missing piece is fresh-project runtime?
- Does the code support the memo’s claim that `inferential` and `logical` are still fixed-corpus analyzers while the generic concept path is already project-aware?
- Is using the API’s current database abstraction the right persistence fix, or is there a stronger bounded alternative?
- Does the memo correctly distinguish product/runtime repair from local-environment workaround?
- Is passing project-loaded documents into the core analyzers the right seam, or should the fix happen elsewhere?
- Does the memo need to freeze more about prompt genericization, especially the deeper Benanav/NLR/Response hardcodings inside the 12-phase logical pipeline?
- Should scrutiny persistence/readback be explicitly in scope together with concept detection / concept analysis persistence?
- Does the memo correctly identify `get_sync_session()` / `sync_session_maker` from `database.py` as the intended reuse seam for normalization?
- Is the fresh-project acceptance path concrete and testable enough to justify implementation?
- Does the fresh-project acceptance path verify the already-admitted logical scrutiny feature strongly enough?
- Does the memo preserve the right bigger-picture ordering relative to:
  - current default-family work
  - later analyzer-v2-native migration
  - later composition-layer work
  - later standalone Close Read host work

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

If useful, you may rerun focused non-destructive inspections, but keep the audit primarily code-backed and roadmap-focused.

Save the audit to this exact file:

- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Fresh_Project_Runtime_Scope_Audit_2026-04-06.md`
