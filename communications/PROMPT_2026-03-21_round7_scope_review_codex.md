# Prompt For Codex: Round 7 Declarative Adaptive Substrate Scope Audit

You are auditing a scoping memo, not implementing it.

Your task is to do a deep, codebase-first audit of:

- `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md`

The purpose is to test whether this memo is truly the right next step after rounds 1 through 6, and whether its assumptions survive contact with the actual repository.

## Hard Rules

1. Do **not** implement anything.
2. Do **not** modify repo files except for writing your report.
3. Do **not** turn this into a coding spike.
4. Save your report only to:
   - `communications/REPORT_Codex_Round7_Declarative_Adaptive_Substrate_Scope_Audit_2026-03-21.md`

## Required Review Style

This should be an audit, not a summary.

You should actively test:

- hidden complexity
- stale assumptions
- under-specified contracts
- missing preconditions
- code seams the memo pretends are small but are actually wide
- risks that “declarative” turns into “new interpreter”

## Files To Inspect

Start with:

- `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md`
- `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_completion.md`
- `communications/PROOF_2026-03-21_round6_cross_workflow_adaptive_aoi_suite.md`
- `communications/MEMO_2026-03-20_round3_adaptive_surface_family_completion.md`
- `communications/PROOF_2026-03-20_round3_adaptive_surface_family.md`
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`
- `src/presenter/presentation_api.py`
- `src/presenter/schemas.py`
- `src/api/routes/presenter.py`
- `src/api/routes/results.py`

Then inspect any additional files you need to make the audit concrete.

## Questions You Must Answer

1. Is `declarative_relationship_surface_v1` the right first substrate token, or is there a better bounded pilot already hiding in the codebase?
2. What exact dispatch points and validation seams would need to widen?
3. Is the memo’s proposed declarative shape sufficiently bounded, or is it still one abstraction step away from a general-purpose interpreter?
4. Does “registered signal extractor + registered builder templates + declarative decision ladder” materially prove anything new, or does it just move constants into a file?
5. What exact pieces of the current `adaptive_relationship_surface_v1` path are actually safe to declarativize first?
6. What test/proof strategy would be needed to establish behavioral equivalence against the round-3 control fixtures?
7. What is the single most important revision needed before this memo should become an execution plan?

## Output Format

Write the report with these sections:

1. `Verdict`
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. `Findings`
   - ordered by severity
   - concrete and code-referenced
3. `What Is Actually Well-Scoped`
4. `What Is Under-Specified Or Risky`
5. `Recommended Revisions Before Execution Planning`
6. `Bottom Line`

## Preferred Standard

The most useful report will:

- challenge the memo where it is hand-wavy
- confirm repo facts where the memo is right
- expose hidden implementation width
- distinguish scope problems from execution problems

Do not be agreeable by default. Be accurate.
