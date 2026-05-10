# Prompt: Codex Review For Phase E Genealogy V2 Portrait First-Hop Capture Alignment V1 Scope

Audit the proposed next Phase E slice for analyzer-v2 / the-critic.

## Subject memo

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_scope.md`

## Your job

Do a code-and-doc audit, not a paraphrase.

You should test whether the memo is:

- technically correct against the current codebase
- strategically aligned with the broader roadmap
- honestly scoped
- actually the smallest defensible next step after the completed AOI mixed-surface consumer proof

## Required inspection targets

At minimum inspect:

- `src/presenter/first_hop_affordance.py`
- `src/views/definitions/genealogy_portrait.json`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`

Also inspect relevant recent memos in `communications/` and `docs/` as needed, especially:

- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Questions to answer

1. Does `genealogy_portrait` actually receive generic `FirstHopAffordance` under the current analyzer rules?
2. Is this slice genuinely matrix-broadening, or just host cleanup on an already-capturable surface?
3. Is the proposed use of `entity_id` on this non-AOI slice honest, or does it overclaim per-item identity semantics?
4. Is the memo honest that this would prove non-AOI host alignment only, not generic custom-renderer law or non-AOI read-side truth?
5. Is `genealogy_portrait` really smaller and cleaner than `IdeaEvolutionRenderer` for the next proof?
6. Does the memo correctly identify the real current host gap:
   - `SynthesisRenderer` still gates on host-local capture assumptions
   - still hardcodes `source_type`
   - still hardcodes the current title shape
   - still omits `entity_id`
   - and still omits `source_workflow_key`?
7. Is a host-only alignment slice the right next move, or should the roadmap jump somewhere else first?
8. Is the negative no-affordance browser proof now calibrated honestly, or does it still overclaim what can be shown on the untouched live genealogy page?
9. Does the memo now say clearly enough that this slice is the prerequisite second workflow-family data point before generic custom-renderer law extraction becomes honest?

## Required output

Write the audit to:

- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`

Your audit should include:

- verdict: approve / approve with corrections / reject
- findings ordered by severity
- concrete file/line references
- explicit comment on whether this is the right next bounded step in the bigger program
- explicit comment on what this slice would and would not prove for the analyzer-v2-as-brain objective
- explicit comment on whether the browser-proof plan is calibrated correctly between live-page positive proof and mocked/unit negative proof
- verification notes if you run focused tests or checks

If you think another next step is cleaner or more honest, say so directly and explain why.
