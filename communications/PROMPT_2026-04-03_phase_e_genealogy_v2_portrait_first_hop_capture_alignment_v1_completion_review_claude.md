# Prompt For Fresh Claude Session

Please review this completion memo critically:

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`

Do not assume the memo is correct.
Test whether its claims are properly calibrated against the landed Critic code, the broader roadmap, and the larger analyzer-v2-as-brain objective.

## What to do

1. Read the completion memo in full.
2. Read the immediate current context:
   - `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_scope.md`
   - `communications/REPORT_Codex_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
   - `communications/REPORT_Claude_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`
   - `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
3. Scrutinize the memo against the actual codebase, especially:
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.test.tsx`
   - `/home/evgeny/projects/the-critic/webapp/tests/genealogy-v2-portrait-capture.spec.ts`
4. Verify the upstream analyzer-side premise:
   - `src/presenter/first_hop_affordance.py`
   - nearby analyzer files needed to check whether the generic first-hop contract on the genealogy line was already sufficient
5. Read relevant roadmap context:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## What to focus on

- Does the completion memo describe the landed boundary honestly?
- Is it correct that this slice is host-only and local to `SynthesisRenderer`?
- Is the memo accurate that section capture now depends on generic first-hop capturability rather than purely local assumptions?
- Is the memo honest about what stayed narrow:
  - only `exec_summary`, `portrait`, and `key_findings`
  - no backend changes
  - no read-side truth surfacing
  - no generic custom-renderer law extraction
- Is the memo calibrated enough about `entity_id` not disambiguating sections within a run?
- Does it overstate the strategic meaning of this non-AOI proof?
- Is its framing of the next honest step sound, or is there a smaller or more defensible follow-on?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Completion_Critique_2026-04-03.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The strongest parts of the memo
3. The weakest assumptions or overclaims
4. Code-backed findings
5. Strategic implications for the roadmap
6. Concrete corrections or reframing you recommend

Keep the critique specific and unsentimental.
Do not produce fluff.
