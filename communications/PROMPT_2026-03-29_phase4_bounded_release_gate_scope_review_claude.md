# Prompt For Claude: Review Phase 4 Bounded Release Gate Scope

Please review this memo:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-29_phase4_bounded_release_gate_scope.md`

Your job is to stress-test it before implementation planning.

## What to do

1. Test the robustness of the memo's assumptions.
2. Examine the scope in light of the bigger picture and the overall analyzer-v2-as-the-brain objectives.
3. Scrutinize the memo's codebase claims against the actual repositories.
4. Look through the most relevant recent memos in `communications/`, especially:
   - `MEMO_2026-03-29_phase4_bounded_governance_evaluation_v1_completion.md`
   - `MEMO_2026-03-28_phase4_bounded_governance_evaluation_scope.md`
   - `MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
   - `MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
   - `MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
5. Pay special attention to whether a bounded pack-level gate is genuinely the right next Stage 15 slice, or whether the memo is skipping a more foundational need such as review tooling, override law, or a different enforcement boundary.

## Questions to answer

- Is a bounded analyzer-owned gate decision over persisted evaluation reports the right next slice now that report generation exists?
- Should the first gate run materialize fresh reports itself, or should it consume explicit existing report ids instead?
- Is the memo honest enough about frozen retrospective semantics, or does it risk overstating what a gate over frozen reports means?
- Is a read-only analyzer inspection seam for gate decisions enough for this slice, or is some review/override surface already required?
- Are there missing report-shape, rule-table, or evidence-linkage constraints that the memo needs to name explicitly?

## Output requirements

Write your review to this exact file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Phase4_Bounded_Release_Gate_Scope_Critique_2026-03-29.md`

Use this structure:

1. `Verdict`
2. `Findings`
3. `Open Questions`
4. `Concrete Revisions`

Please keep the review direct, specific, and code-grounded.
