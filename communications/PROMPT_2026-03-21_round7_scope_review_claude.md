# Prompt For Claude: Round 7 Declarative Adaptive Substrate Scope Critique

You are reviewing a scoping memo, not implementing it.

Your task is to perform an in-depth architectural and code-grounded critique of:

- `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md`

## Goal

Test whether the memo is actually the right next move after rounds 1 through 6, and whether its assumptions hold up against the real codebase.

You should examine:

- the memo itself
- the round-6 completion/proof notes
- the current adaptive runtime code
- trace code
- route/error-mapping code
- any renderer/validation contracts needed to assess the memo’s feasibility

This is not a request for a summary. It is a request for a critical, code-grounded review that tries to break the memo.

## Important Constraints

1. Do **not** implement anything.
2. Do **not** edit source files.
3. Do **not** “improve by coding.”
4. Save your output only to:
   - `communications/REPORT_Claude_Round7_Declarative_Adaptive_Substrate_Scope_Critique_2026-03-21.md`

## What To Examine

At minimum, inspect:

- `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md`
- `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_completion.md`
- `communications/PROOF_2026-03-21_round6_cross_workflow_adaptive_aoi_suite.md`
- `communications/MEMO_2026-03-20_round3_adaptive_surface_family_completion.md`
- `communications/PROOF_2026-03-20_round3_adaptive_surface_family.md`
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`
- `src/presenter/presentation_api.py`
- `src/api/routes/presenter.py`
- `src/api/routes/results.py`

Read other files only if they are necessary to validate or challenge the memo.

## Specific Questions To Answer

1. Is `genealogy_relationship_landscape` actually the right first declarative substrate pilot, or is the memo underestimating hidden dependencies in that path?
2. Is the proposed substrate boundary tight enough, or is it already drifting toward a registry/interpreter?
3. Is “signal extractor stays hardcoded, builder templates stay hardcoded, decision ladder becomes declarative” a real proof, or just configuration theater?
4. What exact code seams would have to widen to support `declarative_relationship_surface_v1`?
5. Are there hidden assumptions around trace equivalence, validation behavior, or workflow authorization that the memo is glossing over?
6. Is the equivalence standard realistic and testable with the existing round-3 fixtures?
7. Does the memo accidentally skip an important preflight gate or documentary gate?

## Output Format

Write a serious critique with:

1. `Verdict`
   - one of:
     - `Approve`
     - `Approve after revision`
     - `Do not approve`
2. `Findings`
   - ordered by severity
   - cite concrete file paths and, when useful, line references
   - focus on hidden complexity, over-claiming, architectural mismatch, missing gates, or incorrect assumptions
3. `What The Memo Gets Right`
4. `What Must Be Revised Before Execution Planning`
5. `Bottom Line`

Be direct. Prefer specific criticism over polite vagueness.

## Standard

The best response is not “this sounds reasonable.”

The best response is:

- specific about where the memo matches the code
- specific about where the memo is too loose
- specific about what would turn it into an execution-ready scope
