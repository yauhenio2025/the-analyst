# Prompt: Codex Audit Of Round 8 Declarative Suite Scope

Audit the next-stage scope in:

- `communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_scope.md`

Use these as governing context:

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_completion.md`
- `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_completion.md`
- `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

Inspect the actual codebase before judging the memo.

Required code reading:

- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`
- `src/presenter/adaptive_specs/keys.py`
- `src/presenter/adaptive_specs/schemas.py`
- `src/presenter/adaptive_specs/registry.py`
- `src/presenter/adaptive_specs/definitions/declarative_relationship_surface_v1.json`
- `src/renderers/definitions/table.json`
- `tests/test_declarative_adaptive_specs.py`
- `tests/test_presentation_api.py`
- `tests/test_manifest_trace.py`
- `tests/test_analysis_product_contract.py`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`

What I want from you:

1. Determine whether the proposed round-8 memo is the right **next structural proof**.
2. Identify hidden engineering complexity that will matter during execution planning.
3. Check whether the memo’s suite assumptions are grounded in the current implementation seams.
4. Check whether the proposed proof standard is honest and adequate.
5. Check whether the round-8 move is still aligned with the larger “thin consumer platformization -> stronger presentation platform” arc, or whether it has become a low-value local optimization.

Specific questions to answer:

- Is the genealogy relationship + conditions suite the right first declarative suite pilot, or is another target cleaner?
- Does the current declarative substrate from round 7 actually generalize to a suite wrapper without major new machinery?
- What exact suite-specific seams are likely to need new abstraction?
- Will rejected-family semantics, trace details, and invalid-spec handling stay coherent under declarative suite selection?
- Are there likely spec/dispatch/registry drift seams the memo is not naming?
- Is the memo right that round 8 should probably be the end of the current proof ladder?
- If round 8 succeeds, is renderer contract validation really the next highest-leverage move?

Output requirements:

- Save the audit to this exact file:
  - `communications/REPORT_Codex_Round8_Declarative_Adaptive_Suite_Scope_Audit_2026-03-21.md`
- Do not overwrite any Claude report.
- Do not modify code.

Required output shape:

1. `Verdict`
   - `Approve`
   - `Approve after revision`
   - `Reject and rescope`

2. `Findings`
   - ordered by severity
   - use exact file/line references
   - focus on implementation blockers, hidden complexity, invalid assumptions, proof-standard weaknesses, and places where the memo quietly depends on code that does not exist yet

3. `What Is Strategically Right`
   - identify where the memo correctly follows the repo’s current proof arc

4. `Big-Picture Call`
   - answer directly:
     - Is round 8 coherent with the last five days of memos?
     - Are we still closing meaningful uncertainty, or are we now proving trivial variants?
     - If round 8 lands, should the program pivot away from proof-branch expansion?

5. `Required Memo Revisions`
   - only if needed
   - concrete, not vague

Do not be polite at the expense of accuracy.
If the memo is directionally right but execution-risky, say so.
If it quietly crosses the line from “bounded substrate proof” into “premature registry design,” say so explicitly.
