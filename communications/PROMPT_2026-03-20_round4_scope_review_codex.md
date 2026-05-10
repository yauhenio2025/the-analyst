# Prompt: Codex Audit for Round 4 Adaptive Surface Suite Scope

You are reviewing a proposed next-stage scope in:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round4_adaptive_surface_suite_scope.md`

Your job is to test whether the memo is technically grounded in the actual codebase and whether its assumptions are the right ones.

This task is documentation-only.

Your entire deliverable is one report file. Do not implement anything. Do not edit source code. Do not "helpfully" build the proof. If you feel tempted to patch code, stop and write the audit instead.

## What To Read First

Read these documents before forming a verdict:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-16_aoi_strategic_reassessment_after_parity_work.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round2_bounded_dynamic_composition_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-20_round3_adaptive_surface_family.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round3_adaptive_surface_family_completion.md`
- `/home/evgeny/projects/the-critic/communications/NEXT_SESSION_DYNAMIC_COMPOSITION_AUDIT.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`

Then inspect the actual code paths in at least:

- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`
- `src/presenter/presentation_api.py`
- `src/analysis_products/result_contract.py`
- `src/api/routes/results.py`
- `src/api/routes/presenter.py`
- `src/views/definitions/genealogy_conditions.json`
- `src/views/definitions/genealogy_cop_enabling_conditions.json`
- `src/views/definitions/genealogy_cop_constraining_conditions.json`
- `src/views/definitions/genealogy_cop_path_dependencies.json`
- `src/views/definitions/genealogy_cop_alternative_paths.json`
- `src/views/definitions/genealogy_cop_counterfactual.json`
- `src/views/definitions/genealogy_cop_synthesis.json`
- `src/views/definitions/genealogy_cop_unacknowledged_debts.json`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
- `/home/evgeny/projects/the-critic/api/server.py`

Also inspect recent repository history if it helps, but do not treat sparse commits as more authoritative than the memo trail.

## Questions You Must Answer

1. Are the signals needed for `genealogy_conditions` actually available from current structured payloads without a new inference pass?
2. Is `genealogy_conditions` the best second adaptive target in the real codebase, or is there a smaller / stronger target?
3. Are the proposed conditions families concrete enough to implement and validate, or are they still too editorially vague?
4. Can the generic host truly stay unchanged once both `genealogy_relationship_landscape` and `genealogy_conditions` start varying under the same proof mode?
5. Is `composition_mode=adaptive_genealogy_surface_suite_v1` the right route contract, or is there a narrower activation shape that fits the existing code better?
6. Is a suite-level trace stage the right inspectability shape, or would separate per-surface stages be cleaner and less risky?
7. What are the highest-risk assumptions in the memo?

## Output Requirements

Write your review to this file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_Round4_Adaptive_Surface_Suite_Scope_Audit_2026-03-20.md`

If the file does not exist, create it. Do not create any other new files.

Structure the review like this:

1. `Findings`
   - ordered by severity
   - each finding should cite concrete file paths and line numbers where possible
2. `Open Questions / Weak Assumptions`
3. `What The Memo Gets Right`
4. `Verdict`
   - one short paragraph saying whether the memo is execution-ready as written, needs tightening, or is pointed in the wrong direction

Keep the review grounded in the actual codebase.
Do not just restate the memo.

## Important Constraints

- Do not implement code.
- Do not modify any repository file except the report file above.
- Do not write a new plan from scratch unless the current memo is fundamentally wrong.
- Prefer identifying specific assumptions that need correction over giving broad generic advice.
- If you think the proposed second target is wrong, name the exact better target and justify it concretely.
