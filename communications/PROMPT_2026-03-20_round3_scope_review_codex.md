# Prompt: Codex Audit for Round 3 Adaptive Surface Family Scope

You are reviewing a proposed next-stage scope in:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-20_round3_adaptive_surface_family_scope.md`

Your job is to test whether the memo is technically grounded in the actual codebase and whether its assumptions are the right ones.

## What To Read First

Read these documents before forming a verdict:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-16_aoi_strategic_reassessment_after_parity_work.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_round2_bounded_dynamic_composition_scope.md`
- `/home/evgeny/projects/the-critic/communications/NEXT_SESSION_DYNAMIC_COMPOSITION_AUDIT.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`

Then inspect the actual code paths in at least:

- `src/presenter/presentation_api.py`
- `src/presenter/decision_trace.py`
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/variant_generator.py`
- `src/presenter/variant_store.py`
- `src/presenter/store.py`
- `src/presenter/presentation_bridge.py`
- `src/renderers/`
- `src/transformations/definitions/`
- `src/views/definitions/`
- `the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `the-critic/webapp/src/components/V2TabContent.tsx`
- `the-critic/api/server.py`

Also inspect recent repository history if it helps, but do not treat sparse commit history as authoritative if the memo trail is stronger.

## Questions You Must Answer

1. Is `genealogy_relationship_landscape` actually the best bounded proof target, or is there a smaller / stronger target in the real codebase?
2. Are the memo's proposed deterministic signals actually available from current structured outputs without a new inference pass?
3. Is a new deterministic selector really the right move, or does the codebase already contain dormant refinement / variant / template machinery that should be reused first?
4. Can the generic host truly stay unchanged for this proof, or are there hidden host assumptions that will break once surface-family contracts vary more strongly?
5. Is the proposed `composition_mode=adaptive_relationship_surface_v1` the right route contract, or is there a better narrower activation shape?
6. Are the proposed "surface families" concrete enough to implement and validate, or are they still too editorially vague?
7. What are the highest-risk assumptions in the memo?

## Output Requirements

Write your review to this file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_Round3_Adaptive_Surface_Family_Scope_Audit_2026-03-20.md`

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

- You are not implementing code.
- You are not writing a new plan from scratch unless the current memo is fundamentally wrong.
- Prefer identifying specific assumptions that need correction over giving broad generic advice.
- If you think the proposed target is wrong, name the exact better target and justify it concretely.
