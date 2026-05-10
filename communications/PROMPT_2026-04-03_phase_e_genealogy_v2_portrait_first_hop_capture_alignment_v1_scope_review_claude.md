# Prompt: Claude Review For Phase E Genealogy V2 Portrait First-Hop Capture Alignment V1 Scope

You are reviewing a new Phase E scope memo for analyzer-v2 / the-critic.

## Primary task

Read the scope memo:

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_scope.md`

Then test it hard.

Do not just summarize it.
Interrogate whether it is actually the right next step.

## What to examine

1. **Assumption robustness**
   - Is `genealogy_portrait` really the smallest honest non-AOI current-V2 step after the AOI mixed-surface proof?
   - Is host-side contract alignment a real matrix-broadening move, or just local cleanup?
   - Is section-level `entity_id = job_id` honest enough for this slice, or does that overclaim identity semantics?
   - Is the memo honest that this would prove non-AOI host alignment only, not generic custom-renderer law or non-AOI read-side truth?
   - Is the negative no-affordance browser proof now calibrated honestly, or does it still overclaim what can be shown on the untouched live genealogy page?

2. **Bigger-picture strategic fit**
   - Evaluate the memo against the broader roadmap and the analyzer-v2-as-brain objective.
   - Ask whether this step genuinely reduces host-owned workflow intelligence or merely rephrases existing host behavior.
   - Ask whether the memo is explicit enough that this slice is the prerequisite second workflow-family data point before generic custom-renderer law extraction becomes honest.
   - Ask whether a different next move would be more honest:
     - non-AOI read-side status truth
     - `IdeaEvolutionRenderer`
     - generic custom-renderer contract law
     - another analyzer-side slice

3. **Codebase truth**
   - Check the actual code, not just the memo's claims.
   - At minimum inspect:
     - `src/presenter/first_hop_affordance.py`
     - `src/views/definitions/genealogy_portrait.json`
     - `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
     - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx`
     - `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
     - `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
   - Verify whether the real current renderer gap is broader than affordance gating plus `source_workflow_key`, including:
     - hardcoded `source_type`
     - hardcoded title shape
     - omitted `entity_id`

4. **Recent memo context**
   - Read the most relevant recent memos in `communications/` and any relevant `docs/` material you need, especially:
     - `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_completion.md`
     - `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`
     - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
     - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
     - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
     - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Required output

Write your review to:

- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`

Your report should include:

- verdict: approve / approve with corrections / reject
- findings ordered by severity
- explicit discussion of whether this is genuinely the right next bounded step
- explicit discussion of what this slice would and would not prove for the broader analyzer-v2-as-brain objective
- concrete code references
- any missing tests, overclaims, or better alternative next moves

Be willing to say the step is too small, too host-local, or strategically out of order if that is where the code evidence leads.
