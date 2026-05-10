# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_scope.md`

Do not assume the memo is correct.
Test whether this is now the right immediate next bounded Phase E slice after the completed AOI V2 capture-provenance persistence closeout.

## What to do

1. Read the scope memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_scope.md`
   - `communications/REPORT_Codex_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Audit_2026-04-03.md`
   - `communications/REPORT_Claude_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Critique_2026-04-03.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
   - `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
   - `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
3. Scrutinize the memo against the actual Critic codebase, especially:
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/hooks/useCaptureStatus.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
   - `/home/evgeny/projects/the-critic/api/server.py`
   - `/home/evgeny/projects/the-critic/api/models_db.py`
   - nearby Critic files that materially govern capture status lookup, research status joins, and AOI V2 page rendering
4. Check the memo against the analyzer-side context it depends on:
   - `src/presenter/first_hop_affordance.py`
   - `src/aoi/contract.py`
   - nearby analyzer files that materially govern the already-landed `aoi_by_sin_type` specialization and handle truth
5. Read relevant roadmap context in `communications/`, especially:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Is read-side AOI V2 capture-status/provenance surfacing really the smallest honest next move after write-side provenance truth?
- Is the memo correct that the current concrete read-side gap is:
  - genealogy-job keyed
  - section-level
  - while the AOI proof line is workflow/entity keyed and card-level?
- Is the memo now explicit enough that the current shared route is worse than merely coarse:
  - AOI analysis captures persist with `genealogy_job_id = null`
  - `/api/captures/by-job/{job_id}` therefore cannot match them at all
  - and the route is not project-scoped today?
- Is a separate AOI-compatible lookup seam actually better than widening `GET /api/captures/by-job/{job_id}`?
- Is the memo correct to keep the existing genealogy status seam untouched in v1?
- Is passive per-card status surfacing the right proof boundary, or is the memo under-scoping or over-scoping what should happen on the host?
- Is reload/revisit truth the right required boundary, or should same-session refetch/invalidation be in scope too?
- Does the memo stay honest that this is not yet:
  - generic capture-status law
  - generic renderer-package capture behavior
  - mixed-surface AOI consumer work
  - non-AOI proof
  - end-to-end destination lifecycle
- Is `aoi_by_sin_type` still the right next consumer line, or is the roadmap now at risk of AOI-local drift?
- Does the proposed read seam teach reusable substrate value, or is it too local to one renderer?
- Is the memo calibrated enough that the reusable-substrate value here is still modest rather than a generic capture-status closeout?
- Are older captures with null `entity_id` / `source_workflow_key` handled honestly enough?
- Is there a more defensible next move than this one?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_AOI_V2_Capture_Status_Provenance_Surfacing_V1_Scope_Critique_2026-04-03.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The memo's strongest parts
3. The weakest assumptions
4. Code-backed findings
5. Strategic implications for the roadmap
6. Concrete corrections or reframing you recommend

Keep the critique specific and unsentimental.
Do not produce fluff.
