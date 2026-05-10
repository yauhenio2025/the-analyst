# Audit: Round 8 / Declarative Adaptive Suite Scope

Date: 2026-03-21
Memo under review: `communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_scope.md`

## Verdict

Approve after revision.

The memo is strategically pointed at the right remaining proof question. Round 7 explicitly left declarative suites unproved, and the larger roadmap is correct that one bounded declarative suite pilot is the last non-trivial variable before the program should stop extending the proof ladder (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_completion.md:155-187`, `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:84-126`, `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:169-206`).

But the memo is not execution-honest yet. The current declarative substrate is still single-surface, single-extractor, relationship-only machinery. Round 8 is not a tiny wrapper over that substrate. It needs one new suite schema shape, one new per-surface execution path, one explicit answer for conditions-rule expressivity, and a more honest proof claim around the hardcoded suite control.

## Findings

### 1. The current declarative substrate does not generalize to suites via a small wrapper; it is single-surface and relationship-specific.

The round-7 schema is structurally one-surface-only: one `target_surface`, one `signal_extractor_key`, one `default_family`, and one `decision_rules[]` list (`src/presenter/adaptive_specs/schemas.py:54-91`). The only repo-tracked spec is a single relationship-surface file with that exact shape (`src/presenter/adaptive_specs/definitions/declarative_relationship_surface_v1.json:1-45`). Runtime dispatch is also hardcoded around that one shape: `apply_bounded_dynamic_composition()` and `inspect_runtime_composition()` have explicit `if composition_mode == ...` branches for the declarative relationship token, while suite handling remains entirely separate hardcoded branches (`src/presenter/bounded_dynamic_composition.py:280-325`, `src/presenter/bounded_dynamic_composition.py:344-374`).

The actual declarative executor is also relationship-only. `_apply_declarative_relationship_surface()` loads one spec, resolves one target payload, runs one extractor, selects one family, and calls the relationship builder map (`src/presenter/bounded_dynamic_composition.py:508-538`). `_select_declarative_relationship_surface()` hardcodes the same assumptions (`src/presenter/bounded_dynamic_composition.py:676-704`). `_declarative_signal_extractors()` exposes only `relationship_surface_signals_v1`, and `_relationship_surface_builders()` only resolves relationship families (`src/presenter/bounded_dynamic_composition.py:1460-1473`). The schema key whitelist mirrors that limitation: there is one allowed extractor key and two allowed builder template keys, both relationship-specific (`src/presenter/adaptive_specs/keys.py:5-21`).

So the answer to “does the round-7 declarative substrate actually generalize to a suite wrapper without major new machinery?” is no. It generalizes only if round 8 adds bounded new machinery:

- a suite spec shape
- per-surface spec entries
- per-surface extractor/builder registries
- a suite-aware executor/inspector

That is still bounded. It is not “just add one more JSON file.”

### 2. The memo overstates equivalence to the hardcoded suite control while explicitly excluding one family the hardcoded suite can still select.

The memo says round 8 should prove declarative equivalence against the hardcoded round-4 control, but it also marks declarative `relationship_field_map` out of scope (`communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_scope.md:127-157`). The hardcoded genealogy suite does not share that limitation. `_apply_adaptive_relationship_conditions_suite()` will build `relationship_field_map` when the relationship selector chooses it (`src/presenter/bounded_dynamic_composition.py:541-586`), and `_choose_relationship_surface_family_key()` still selects `relationship_field_map` for diffuse fields (`src/presenter/bounded_dynamic_composition.py:769-786`).

That means the memo is not currently describing full semantic equivalence to `adaptive_genealogy_relationship_conditions_v1`. It is describing a bounded pilot that proves:

- dossier + balance
- comparison + matrix

against the hardcoded control’s corresponding cases (`communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_scope.md:227-250`, `communications/PROOF_2026-03-20_round4_adaptive_surface_suite.md:52-80`).

That is still a worthwhile proof. It just is not full control replacement. The memo needs to say that explicitly, or else widen the declarative relationship family set and proof controls to include the field-map branch.

### 3. The current declarative rule grammar cannot express the conditions selector as written without new code-owned derived metrics.

Round-7 declarative predicates are deliberately tiny: only `eq` and `gte`, and only against literal values (`src/presenter/adaptive_specs/keys.py:10-21`, `src/presenter/adaptive_specs/schemas.py:16-39`). That was enough for the relationship pilot because the hardcoded relationship selector already reduces to fixed threshold checks over scalar metrics like `relationship_count`, `top_share`, and `score_gap` (`src/presenter/bounded_dynamic_composition.py:769-786`).

The conditions selector is different. Its hardcoded decision depends on:

- `path_count >= 2`
- `path_signal >= balance_signal`

where `path_signal` and `balance_signal` are sums derived from multiple metrics, not raw fields already present in the current predicate grammar (`src/presenter/bounded_dynamic_composition.py:1076-1085`, `src/presenter/bounded_dynamic_composition.py:1317-1360`).

So the memo is missing the exact bounded abstraction it needs for conditions. If round 8 wants to stay non-interpreter, it should not widen the predicate language. It should say plainly that the code-owned conditions extractor must emit derived metrics such as `path_signal` and `balance_signal`, after which declarative rules can stay in the current constant-threshold form. Without that revision, the memo quietly depends on rule expressivity that does not exist.

### 4. The suite-specific drift surface is broader than the memo names: authorization, dispatch, trace staging, result threading, tests, and Critic labeling all widen manually.

Adding a new suite token is not just a spec file. Backend authorization is hardcoded in `_SUPPORTED_COMPOSITION_MODES` and `_MODE_WORKFLOW_MAP` (`src/presenter/bounded_dynamic_composition.py:53-68`). Runtime application and inspection are hardcoded in `apply_bounded_dynamic_composition()` and `inspect_runtime_composition()` (`src/presenter/bounded_dynamic_composition.py:280-325`, `src/presenter/bounded_dynamic_composition.py:344-374`). Trace stage naming is hardcoded in `get_runtime_composition_stage_name()` (`src/presenter/bounded_dynamic_composition.py:328-341`). The trace builder also has an explicit list of composition modes whose details it will inspect (`src/presenter/decision_trace.py:80-113`).

That token then threads through presenter payload assembly, manifest assembly, page assembly, single-view assembly, result manifests, result presentation, refresh, and the HTTP route layers (`src/presenter/presentation_api.py:657-1010`, `src/analysis_products/result_contract.py:273-440`, `src/api/routes/presenter.py:142-287`, `src/api/routes/results.py:44-116`).

The test surface matches that widening. Result-contract tests enumerate supported proof modes directly (`tests/test_analysis_product_contract.py:1070-1585`). The Critic workspace also hardcodes every proof label, including the current declarative single-surface token and the hardcoded genealogy suite token (`/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:77-105`).

The memo is directionally right that the host remains generic. But “one generic proof label if needed” understates the real drift surface. Round 8 needs an explicit checklist for all manual token enumerations, or the suite will land with backend/frontend/test skew.

### 5. Fail-closed invalid-spec handling can stay coherent, but the current error model assumes one target surface and needs a suite-level ownership decision.

The existing declarative loader normalizes registry failures into `BoundedCompositionValidationError`, which is good (`src/presenter/bounded_dynamic_composition.py:868-916`). But it is still written around a single target surface. The first registry failure path always blames `genealogy_relationship_landscape` (`src/presenter/bounded_dynamic_composition.py:876-885`), and the workflow-mismatch path assumes one `spec.target_surface` (`src/presenter/bounded_dynamic_composition.py:887-915`). That fits round 7. It does not fit a suite spec with multiple targets.

Trace behavior is also only partly solved. `build_presentation_trace()` already preserves the route-level discipline the memo wants:

- invalid requested mode -> route-level `400`
- accepted mode with runtime/spec failure -> trace stays `200` with `composition_status="invalid"`
- suite traces reuse `adaptive_surface_suite_selection` when `surface_decisions` are present (`src/presenter/decision_trace.py:67-113`, `src/presenter/decision_trace.py:222-292`)

That means the trace grammar can stay coherent. But round 8 still needs to define where a suite-spec failure attaches:

- one suite-level pseudo-surface
- the first failing target surface
- one issue per affected target surface

If the memo does not choose that explicitly, invalid-spec handling will drift into ad hoc issue attribution.

## What Is Strategically Right

The genealogy relationship + conditions suite is still the right first declarative suite pilot. It stays inside one workflow, already has route-real documentary controls, and avoids AOI’s parent-surface coupling. The AOI adaptive builders still have to preserve `source_parent_view_key="aoi_thematic_analysis"` on rewritten child surfaces (`src/presenter/bounded_dynamic_composition.py:1981-2041`, `src/presenter/bounded_dynamic_composition.py:2061-2087`), while the genealogy relationship and conditions builders do not have that extra parent-contract seam (`src/presenter/bounded_dynamic_composition.py:1601-1618`, `src/presenter/bounded_dynamic_composition.py:1839-1856`, `src/presenter/bounded_dynamic_composition.py:1887-1928`). The memo is right to avoid AOI widening here (`communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_scope.md:106-121`).

The memo is also right to keep rationale prose, rejected-family prose, trace grammar, workflow authorization, extractors, and builders code-owned (`communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_scope.md:159-187`). The current suite trace model already supports per-surface decisions under one stage through `AdaptiveSurfaceSuiteSelection` (`src/presenter/bounded_dynamic_composition.py:140-150`), and `build_presentation_trace()` already renders that as `adaptive_surface_suite_selection` without inventing a second trace dialect (`src/presenter/decision_trace.py:224-275`).

Strategically, the memo is aligned with the actual program arc. Round 7 closed declarative single-surface proof and explicitly left declarative suites open (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_completion.md:155-187`, `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_completion.md:226-243`). The round-8 roadmap memo is therefore right that one bounded declarative suite pilot is the last meaningful proof question before the work should pivot (`communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:84-126`, `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:137-206`).

## Big-Picture Call

Yes, round 8 is coherent with the last five days of memos. It follows directly from the round-4 suite proof, the round-6 cross-workflow suite proof, and the round-7 declarative single-surface proof. It is still closing meaningful uncertainty, but only if it proves a real suite substrate shape. If round 8 is reduced to “two single-surface specs happen to be invoked under one token,” it becomes a trivial variant. If it lands as a bounded suite schema plus per-surface declarative execution with unchanged fail-closed and trace discipline, it closes the last real structural gap in this ladder.

The memo is also right that round 8 should probably end the current proof ladder. After that point the next major risk is no longer “can we select the right family?” It is “can we trust and scale the composed payload contract?” That matches the larger vision record, which already says renderer contracts should come first once the proof ladder is sufficient (`communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:190-206`, `communications/DYNAMIC_BESPOKE_APPS_VISION.md:610-623`).

If round 8 succeeds, renderer contract validation is the next highest-leverage move. The repo already has the validation hook points in `_validate_runtime_payload()` and renderer definitions such as `table.json` (`src/presenter/bounded_dynamic_composition.py:2569-2647`, `src/renderers/definitions/table.json:1-83`). The remaining leverage is in making those contracts more complete and more upstream-authoritative, not in proving yet another composition token.

## Required Memo Revisions

1. Rewrite the implementation claim from “lift the round-7 substrate into a suite wrapper” to “add one bounded suite schema and one suite-aware executor on top of round-7 primitives.” The current code does not support suites by simple wrapper reuse (`src/presenter/adaptive_specs/schemas.py:54-91`, `src/presenter/bounded_dynamic_composition.py:508-538`, `src/presenter/bounded_dynamic_composition.py:676-704`).

2. Make the proof claim honest about scope. Either:
   - state that round 8 is a bounded two-relationship-family declarative suite pilot and not full semantic replacement for `adaptive_genealogy_relationship_conditions_v1`, or
   - widen the declarative relationship family set and route-real controls to cover `relationship_field_map` too (`src/presenter/bounded_dynamic_composition.py:541-586`, `src/presenter/bounded_dynamic_composition.py:769-786`).

3. Name the conditions-rule seam explicitly. The memo should require code-owned derived metrics such as `path_signal` and `balance_signal` in the conditions extractor so the rule grammar can remain fixed and non-interpreter (`src/presenter/adaptive_specs/schemas.py:16-39`, `src/presenter/bounded_dynamic_composition.py:1076-1085`, `src/presenter/bounded_dynamic_composition.py:1317-1360`).

4. Enumerate the manual drift checklist up front:
   - `_SUPPORTED_COMPOSITION_MODES`
   - `_MODE_WORKFLOW_MAP`
   - apply/inspect/stage-name switches
   - result/presenter threading
   - route tests
   - Critic proof label mapping

5. Define suite-spec failure ownership before execution planning. The memo should say how a bad suite spec maps to `CompositionIssue.view_key` and how trace details behave when suite inspection cannot resolve per-surface decisions (`src/presenter/bounded_dynamic_composition.py:868-916`, `src/presenter/decision_trace.py:80-113`, `src/presenter/decision_trace.py:222-292`).

6. Keep the post-round-8 pivot explicit. If round 8 lands, the program should freeze bounded declarative substrate v1 and move to renderer contracts, not continue expanding proof tokens (`communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:169-206`, `communications/DYNAMIC_BESPOKE_APPS_VISION.md:616-623`).
