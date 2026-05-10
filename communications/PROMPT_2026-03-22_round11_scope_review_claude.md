# Prompt: Claude Review For Round 11 Scope Memo

Read and critique this memo as an external reviewer:

- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_scope.md`

Your task is to stress-test it against:

1. the actual roadmap direction
2. the bigger analyzer-v2 vision
3. the current codebase
4. the most relevant recent memos and completion notes

Do **not** implement anything.
Do **not** just summarize the memo.
Treat this as a scoped architecture review.

## What To Examine

First, read the key roadmap and completion docs:

- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md`
- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_scope.md`

Then inspect the relevant code seams:

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

Also check whether any relevant Perspective docs folder exists in or near this repo.
If none exists, say so explicitly instead of pretending you reviewed one.

## Questions You Must Answer

1. Is round 11 as “bounded compose-from-intent” actually the right next move after rounds 9 and 10, or is the memo skipping a more necessary platform step?
2. Is the memo honest about the current codebase, especially:
   - `POST /v1/presenter/compose` already existing with a different meaning
   - `PagePresentation` being job-bound
   - the lack of a transient presenter contract
   - the narrow pattern catalog
3. Is AOI the correct required proof slice, or is that just habit from rounds 9 and 10?
4. Is the memo underestimating any missing seam needed to make compose-from-intent real?
5. Is the transient-contract choice the right one, or should the scope take a different route?
6. Does the memo stay aligned with the big-picture “thin shell + analyzer-v2 as brain” direction, or does it drift into a toy API round?

## Output Requirements

Write your review to this exact file:

- `communications/REPORT_Claude_Round11_Bounded_Compose_From_Intent_Scope_Critique_2026-03-22.md`

Your review should include:

- a one-line verdict: `Approve`, `Approve after revision`, or `Reject`
- the strongest reasons the direction is right
- concrete findings, ordered by severity
- explicit references to files and line ranges where useful
- a short bottom-line recommendation on whether the memo is ready to turn into an execution plan

Be direct. Prefer precision over encouragement.
