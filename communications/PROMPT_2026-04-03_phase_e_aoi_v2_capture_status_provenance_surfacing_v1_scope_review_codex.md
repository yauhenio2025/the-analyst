# Prompt For Fresh Codex Session

Please audit this memo critically:

- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_scope.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the current codebase, the just-completed AOI V2 capture-provenance persistence slice, and the larger analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_scope.md`
   - `communications/REPORT_Codex_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Audit_2026-04-03.md`
   - `communications/REPORT_Claude_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Critique_2026-04-03.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
3. Check the memo against the relevant Critic code and tests:
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/hooks/useCaptureStatus.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
   - `/home/evgeny/projects/the-critic/api/server.py`
   - `/home/evgeny/projects/the-critic/api/models_db.py`
   - `/home/evgeny/projects/the-critic/tests/test_capture_provenance.py`
   - nearby Critic files that materially govern capture lookups, research answer state, and AOI page rendering
4. Check the memo against the analyzer-side context it depends on:
   - `src/presenter/first_hop_affordance.py`
   - `src/aoi/contract.py`
   - nearby analyzer files that materially govern the specialized `aoi_by_sin_type` contract
5. Read relevant roadmap/review context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Is AOI V2 capture-status/provenance surfacing the right immediate next slice after persisted provenance truth landed?
- Is the memo correct that the current shared read seam is still genealogy-job keyed and section-level, and therefore cannot honestly surface AOI card-level truth on `aoi_by_sin_type`?
- Is the memo now explicit enough that the current shared route is worse than that:
  - AOI analysis captures persist with `genealogy_job_id = null`
  - `/api/captures/by-job/{job_id}` therefore cannot match them at all
  - and the route is not project-scoped?
- Is a separate AOI-compatible lookup seam the smallest honest choice, or should the existing `/api/captures/by-job/{job_id}` route be widened instead?
- Is the memo correct to keep the existing genealogy status seam untouched in v1?
- Does passive per-card state on `aoi_by_sin_type` define the right proof boundary, or is the memo undercommitting / overcommitting?
- Is reload/revisit truth the right required browser proof boundary?
- Is the memo honest to defer:
  - same-session optimistic invalidation
  - generic renderer-package capture-status behavior
  - `aoi_by_theme`
  - non-AOI proof
  - deep-link UX
  - capture deduplication rules
- Does the proposed lookup seam teach reusable substrate value, or is it too local to one AOI renderer?
- Is the memo calibrated enough that the reusable-substrate value is still modest rather than a generic capture-status closeout?
- Does the memo handle older captures with null provenance fields honestly enough?
- Is there a stronger next move than this one, given the broader roadmap?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_AOI_V2_Capture_Status_Provenance_Surfacing_V1_Scope_Audit_2026-04-03.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The memo's strongest code-backed points
3. The memo's weakest or overstated assumptions
4. Any factual discrepancies you found
5. What this changes for the larger roadmap
6. The most defensible next move after this memo

Be concrete. Use code-backed reasoning. Avoid fluff.
