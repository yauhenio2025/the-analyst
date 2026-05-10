# Prompt For Fresh Codex Session

Please audit this completion memo critically:

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`

Do not treat the memo as presumptively correct.
Test its assumptions against the actual landed Critic code, the recent Phase E current-consumer line, the broader roadmap, and the analyzer-v2-as-brain objective.

## Required tasks

1. Read the memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_scope.md`
   - `communications/REPORT_Codex_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
   - `communications/REPORT_Claude_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
3. Check the memo against the relevant host/runtime code and tests:
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/tests/genealogy-v2-portrait-capture.spec.ts`
4. Check the memo against the relevant analyzer contract source:
   - `src/presenter/first_hop_affordance.py`
   - any nearby analyzer files needed to verify the genealogy generic first-hop claim
5. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

- Does the completion memo accurately describe the landed code boundary?
- Is it correct that `SynthesisRenderer` now consumes analyzer-owned generic first-hop truth rather than relying only on host-local unconditional capture assumptions?
- Is the memo honest about the intentionally narrow section coverage:
  - `exec_summary`
  - `portrait`
  - `key_findings`
- Is it correct that:
  - `source_type` now comes from config
  - `source_workflow_key` is emitted
  - `entity_id = _captureEntityId || _captureJobId`
  - `genealogy_job_id` remains present
- Is the memo calibrated enough about `entity_id`:
  - useful run/job identity
  - not section-disambiguating identity
- Does the memo overstate how much this advances generic custom-renderer law readiness?
- Is the memo's suggested next honest step defensible, or is there a smaller or cleaner follow-on?
- What is the strongest roadmap interpretation after this completion?

## Output requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Completion_Audit_2026-04-03.md`

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

Be concrete.
Use code-backed reasoning.
Avoid fluff.
