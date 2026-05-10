# Prompt: Claude Review Of Round 8 Declarative Suite Scope

Read and critically review:

- `communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_scope.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_completion.md`
- `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_completion.md`
- `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

Then inspect the relevant code in both repos.

Minimum required code inspection:

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

Your task is not to be agreeable.
Your task is to pressure-test whether round 8 is actually the right next bounded move and whether this scope memo is implementation-safe.

I want you to examine five things at once:

1. **Codebase reality**
   - Is the proposed declarative suite lift actually aligned with the current seams in `bounded_dynamic_composition.py` and `decision_trace.py`?
   - What hidden implementation complexity is the memo missing?
   - Are there likely circularity, dispatch, validation, or equivalence-test problems not acknowledged in the memo?

2. **Structural scope discipline**
   - Is genealogy relationship + conditions actually the right first declarative suite pilot?
   - Is AOI being excluded for the right reasons, or is that just inertia?
   - Is the memo staying narrow enough to avoid drifting into a general adaptive registry?

3. **Trace / failure / validation fidelity**
   - Will the existing `adaptive_surface_suite_selection` grammar generalize cleanly to a declarative suite path?
   - Are the proposed 400 / 409 / trace-200 claims actually consistent with the current route and trace handlers?
   - Are there any suite-level invalid-spec or invalid-surface cases the memo is not treating honestly?

4. **Proof quality**
   - Is the proposed equivalence standard strong enough?
   - Is it too strong in places where the declarative path should intentionally differ from the hardcoded path?
   - Are the round-4 control fixtures and proof artifacts the right documentary control for round 8?

5. **Big-picture program alignment**
   - Is round 8 still a high-value proof, or are we now at the edge of doing locally elegant but strategically trivial work?
   - If round 8 lands, is the memo right that the next move should pivot to renderer contract validation and platform law rather than another proof branch?

Output requirements:

- Write the review to this exact file:
  - `communications/REPORT_Claude_Round8_Declarative_Adaptive_Suite_Scope_Critique_2026-03-21.md`
- Do not overwrite any other report file.
- Do not modify source code.

Required structure:

1. `Verdict`
   - one of:
     - `Approve`
     - `Approve after revision`
     - `Reject and rescope`

2. `Findings`
   - ordered by severity
   - include exact file references and line numbers where relevant
   - focus on bugs, hidden complexity, invalid assumptions, missing gates, proof-standard problems, and scope drift

3. `What The Memo Gets Right`
   - name the strongest parts, especially where the scope is disciplined or strategically aligned

4. `Big-Picture Assessment`
   - answer directly:
     - is round 8 coherent with the larger memo trail?
     - have we exceeded the useful proof ladder already?
     - if round 8 lands, should the next move really be renderer contracts / platform law?

5. `Concrete Revisions Required Before Planning`
   - only if needed
   - make them specific enough that the memo can be revised without guesswork

Be blunt.
If the memo is strategically right but technically under-specified, say so.
If the memo is overfitting the current proof ladder and missing the larger vision, say so.
