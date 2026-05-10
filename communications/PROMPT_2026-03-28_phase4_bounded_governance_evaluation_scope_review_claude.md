# Prompt For Claude: Review Phase 4 Governance/Evaluation Scope

Please review this memo:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-28_phase4_bounded_governance_evaluation_scope.md`

Your job is to stress-test it before implementation planning.

## What to do

1. Test the robustness of the memo's assumptions.
2. Examine the scope in light of the bigger picture and the overall analyzer-v2-as-the-brain objectives.
3. Scrutinize the memo's codebase claims against the actual repositories.
4. Look through the most relevant recent memos in `communications/`, especially:
   - `MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
   - `MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_completion.md`
   - `MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
   - `MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
   - `MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
5. Pay special attention to whether the proposed first Phase 4 slice is genuinely the right next step, or whether it is silently skipping a more foundational need.

## Questions to answer

- Is a frozen two-case analyzer-owned evaluation pack the right first governance slice?
- Is the memo too optimistic about evaluating from durable truth plus saved artifacts without rerunning live proof?
- Should the first inspection seam be analyzer-only, or is some host/read surface required immediately?
- Is the memo correctly avoiding premature human approval UI and LLM-based subjective grading?
- Are there missing code-path constraints, data-shape constraints, or artifact dependencies that the memo needs to name explicitly?

## Output requirements

Write your review to this exact file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Phase4_Bounded_Governance_Evaluation_Scope_Critique_2026-03-28.md`

Use this structure:

1. `Verdict`
2. `Findings`
3. `Open Questions`
4. `Concrete Revisions`

Please keep the review direct, specific, and code-grounded.
