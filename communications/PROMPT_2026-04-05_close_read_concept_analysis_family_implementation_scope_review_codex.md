Please audit this implementation scope memo:

- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`

Before concluding, read all of these in full. Do not skip any:

- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

Inspect these code files directly:

- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CloseReadFamilySwitcher.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadAoiPages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/types.ts`
- `/home/evgeny/projects/the-critic/api/server.py`

Audit goals:

1. Verify whether the scope correctly translates the concept-family boundary memo into an implementation-ready tranche.
2. Stress-test the route model, landing/detail behavior, and the result-backed-only posture against the current Critic codebase.
3. Check whether the scope honestly handles the reuse vs extraction seam around `ConceptsPanel`.
4. Evaluate whether the scope keeps the logical-only scrutiny cut bounded while keeping ammunition/send-to-outline/cross-concept/big-picture deferred.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Is the scope right to place the concept family under `/close-read/concepts` and `/close-read/concepts/:conceptSlug`, or does the current route architecture suggest a better bounded choice?
- Does the landing/index behavior correctly filter to admitted core submodes using the existing `/api/concept/analyses` summary endpoint?
- Does the scope correctly require case-insensitive concept grouping and slug resolution through the summary list before detail fetch?
- Is the detail-page availability and submode fallback law concrete enough?
- Does the scope overstate the feasibility of inheriting the Close Read baseline, especially provenance/capture, given the current non-V2 concept detail runtime?
- Is extracting `InferentialDetail` / `LogicalDetail` and a logical-scrutiny helper the right seam, and does the scope correctly reject `AnalysisDetail` as the extraction boundary?
- Does the scope correctly constrain scrutiny to the logical surface and trim the broader ammunition workflow?
- Does the scope correctly state that concept-family capture is net-new bounded plumbing rather than inherited reuse?
- Does the scope keep the right order of work, or does it drift prematurely into composition-layer or standalone-host concerns?

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

If useful, you may rerun focused non-destructive inspections, but keep the audit primarily code-backed and roadmap-focused.

Save the audit to this exact file:

- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Family_Implementation_Scope_Audit_2026-04-05.md`
