Please review this implementation scope memo in full:

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

What I need from you:

1. Test the robustness of the scope memo’s assumptions.
2. Examine them in light of the bigger Close Read vision and overall analyzer-v2-as-brain objectives.
3. Scrutinize the memo’s claims against the actual codebase, not just the memo text.
4. Evaluate whether the scope is implementation-ready rather than drifting back into product-boundary ambiguity.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Is the route model for the concept family under Close Read concrete and coherent?
- Does the scope correctly preserve the result-backed-only posture and keep launch/detection on native concept-analysis routes?
- Is the landing/index inclusion law correct and sufficiently explicit for:
  - both-core-result concepts
  - one-core-result concepts
  - deferred-only concepts
  - zero-core-result concepts
- Does the scope correctly require case-insensitive concept grouping and slug resolution through the summary list before detail fetch?
- Is the detail-page submode/tab fallback law concrete enough to implement safely?
- Does the scope reuse the right runtime seams from existing Critic code, or does it overstate how reusable the current `ConceptsPanel` detail layer is?
- Does the scope correctly treat `AnalysisDetail` as the wrong extraction seam and `InferentialDetail` / `LogicalDetail` as the real lower extraction boundary?
- Is the logical-only scrutiny cut honest and well-bounded?
- Does the scope overreach on provenance/capture assumptions for concept analysis, given that the old concept estate is not currently V2TabContent-based?
- Does the scope correctly state that concept-family capture is net-new bounded plumbing rather than inherited reuse from genealogy/AOI?
- Does the scope keep the right separation between:
  - current default-family work
  - later composition-layer work
  - standalone-host deferral

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Family_Implementation_Scope_Critique_2026-04-05.md`
