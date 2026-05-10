# Prompt: Codex Review For Round 11 Scope Memo

Audit this scope memo against the live repo:

- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_scope.md`

Your job is to test whether the memo is:

- technically grounded
- coherent with the roadmap
- honest about the current code seams
- scoped tightly enough to be implementable

Do **not** implement the round.
Do **not** rewrite the memo unless needed for your report.

## Review Inputs

Read these docs first:

- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md`
- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_scope.md`

Then inspect the actual code paths the memo depends on:

- `src/api/routes/presenter.py`
- `src/api/routes/views.py`
- `src/api/routes/view_patterns.py`
- `src/api/routes/renderers.py`
- `src/api/routes/transformations.py`
- `src/presenter/schemas.py`
- `src/presenter/presentation_api.py`
- `src/presenter/manifest_builder.py`
- `src/views/generator.py`
- `src/views/pattern_schemas.py`
- `src/views/patterns/*.json`
- `renderers-ui/src/index.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`

Also look for any relevant Perspective docs directory.
If there is none, state that explicitly.

## What To Audit

Focus on these questions:

1. Is compose-from-intent actually the right next round after round 10, or would that skip a still-blocking platform seam?
2. Does the memo correctly describe the existing primitives:
   - stateless transformations
   - ephemeral `views/generate`
   - renderer recommendation
   - current manifest enforcement
   - current consumer consolidation state
3. Is the memo right to reject reusing the existing job-bound `PagePresentation` contract?
4. What missing implementation seam is most likely to bite first:
   - transient page contract
   - transient page assembly helper
   - pattern-selection weakness
   - renderer/pattern validation gap
   - trace/diagnostics shape
5. Is the AOI-only proof slice a real bounded move, or is it too narrow / too disconnected from the broader vision?
6. Is the memo accidentally underscoping any place where current code is more job-bound than it admits?
7. Is there any place where the memo’s “glue over existing pieces” claim is too optimistic?

## Output Requirements

Write your audit to this exact file:

- `communications/REPORT_Codex_Round11_Bounded_Compose_From_Intent_Scope_Audit_2026-03-22.md`

Your output should contain:

- a one-line verdict: `Approve`, `Approve after revision`, or `Reject`
- the best parts of the memo
- specific findings, ordered by severity
- file references for the key facts you verified
- a short conclusion on whether this is execution-plan ready

Be skeptical and concrete.
