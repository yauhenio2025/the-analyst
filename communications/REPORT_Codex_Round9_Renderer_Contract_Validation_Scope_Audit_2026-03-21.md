# Report: Codex Audit / Round 9 Renderer Contract Validation Scope

Date: 2026-03-21
Memo under audit: `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md`

## Verdict

Approve after revision.

## Findings

### 1. Highest severity: the proposed genealogy proof slice is not actually registry-backed clean

The memo says round 9 should prove fail-closed renderer-contract enforcement on a "bounded, registry-backed proof slice" and proposes reusing the round-8 genealogy control routes for that proof surface:

- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:131`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:146`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:160`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:216`

That claim does not hold for the genealogy route as it exists today.

The renderer registry only loads JSON definitions from `src/renderers/definitions/*.json` and currently fail-soft logs and skips bad files rather than failing loud:

- `src/renderers/registry.py:33`
- `src/renderers/registry.py:45`
- `src/renderers/registry.py:53`

The registered catalog is only:

- `accordion`
- `card_grid`
- `evidence_trail`
- `prose`
- `raw_json`
- `stat_summary`
- `tab`
- `table`
- `timeline`

I locally checked the actual round-8 genealogy proof manifests with:

- `build_presentation_manifest("proof-round4-adaptive-balance-final-1774012011", consumer_key="the-critic", slim=True)`
- `build_presentation_manifest("proof-round4-adaptive-matrix-final-1774012011", consumer_key="the-critic", slim=True)`

Both manifests still contain 8 active views whose `renderer_type` is not present in `src/renderers/definitions/`:

- `genealogy_per_work_scan -> card`
- `genealogy_cop_enabling_conditions -> enabling_conditions`
- `genealogy_cop_constraining_conditions -> constraining_conditions`
- `genealogy_cop_counterfactual -> prose_block`
- `genealogy_cop_synthesis -> prose_block`
- `genealogy_cop_path_dependencies -> timeline_strip`
- `genealogy_cop_unacknowledged_debts -> mini_card_list`
- `genealogy_cop_alternative_paths -> move_repertoire`

So the memo’s current statement that there are only two active views with no renderer registry definition is materially understated:

- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:115`

It found two obvious cases:

- `genealogy_per_work_scan -> card`
- `lines_of_attack_overview -> prose_narrative`

But on the actual genealogy proof route, the live surface is broader than that.

Implication: reusing the existing round-8 genealogy route as a strict renderer-contract proof surface is not honest unless round 9 explicitly does one of these:

- narrows the proof to a smaller genealogy route/view slice,
- adds the minimal renderer definitions needed for the participating genealogy views, or
- scopes the first fail-closed proof to AOI only and treats genealogy as a follow-on cleanup/gate.

### 2. High severity: the normal presenter path does not just run warn-only validation, it only validates renderer data and skips renderer config entirely

The memo is directionally correct that normal bridge/assembly validation is observational only:

- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:73`

That is true:

- `src/presenter/presentation_bridge.py:468`
- `src/presenter/presentation_bridge.py:475`
- `src/presenter/presentation_api.py:1479`
- `src/presenter/presentation_api.py:1487`

But the seam is slightly worse than the memo states. Both paths only call `validate_renderer_data(...)`:

- `src/presenter/presentation_bridge.py:481`
- `src/presenter/presentation_api.py:1494`

There is no corresponding normal-path `validate_renderer_config(...)` call in those bridge/assembly seams.

So round 9 is not merely:

- "turn existing normal-path warn-only validation into a hard gate"

It also requires:

- adding a serve-time renderer-config validation seam on the normal presenter path.

That should be named explicitly in the scope memo, because config enforcement is part of the stated round-9 claim:

- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:191`

### 3. Medium severity: the memo overstates how universal bounded-composition strictness currently is

The memo says strict renderer support/config/data enforcement already exists inside bounded composition rewrites:

- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:84`

That is mostly true for the proof-mode payloads that use known renderer definitions:

- `src/presenter/bounded_dynamic_composition.py:2867`
- `src/presenter/bounded_dynamic_composition.py:2917`
- `src/presenter/bounded_dynamic_composition.py:2929`

But the validator itself treats unknown renderers or missing schemas as valid with `schema_available=False`:

- `src/renderers/validator.py:102`
- `src/renderers/validator.py:105`
- `src/renderers/validator.py:112`
- `src/renderers/validator.py:171`
- `src/renderers/validator.py:174`
- `src/renderers/validator.py:181`

So the real current law is narrower:

- bounded composition fail-closes on consumer support,
- and on config/data schema violations for renderer types that actually exist in the renderer registry,
- but not on "renderer contract missing from registry" as a generic condition.

That nuance matters because round 9 is specifically about turning renderer contracts into platform law. The scope memo should say that the bounded-composition tranche already proves the enforcement pattern for known registry-backed renderers, not that it has already solved universal renderer-contract strictness.

### 4. Medium severity: the memo should call out route/trace exception plumbing as an explicit implementation seam

The memo correctly says route-level failures should become `409` and trace should stay inspectable:

- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:279`

But the concrete codepath is more specific than the memo currently acknowledges.

`results.py` and `presenter.py` only special-case `BoundedCompositionValidationError`:

- `src/api/routes/results.py:37`
- `src/api/routes/results.py:58`
- `src/api/routes/results.py:60`
- `src/api/routes/presenter.py:39`
- `src/api/routes/presenter.py:170`
- `src/api/routes/presenter.py:172`
- `src/api/routes/presenter.py:255`
- `src/api/routes/presenter.py:257`

And the trace route stays `200` with inspectable diagnostics only because `build_presentation_trace()` catches that same bounded-composition error internally:

- `src/presenter/decision_trace.py:81`
- `src/presenter/decision_trace.py:90`

If round 9 introduces a new renderer-contract exception type without either:

- reusing the existing bounded-composition error shape, or
- teaching these routes and `build_presentation_trace()` about the new error,

the current failure mode will degrade to route-level `500`s.

The memo should name that seam explicitly. Right now it freezes the principle but not the real codepath risk.

## What Looks Solid

The roadmap discipline is right. The round-8-and-beyond memo explicitly said the next serious tranche after the adaptive/declarative proof ladder should be renderer contract validation rather than another proof token:

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:161`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md:179`

The memo is also correct that normal presenter validation is presently observational only:

- `src/presenter/presentation_bridge.py:475`
- `src/presenter/presentation_api.py:1487`

It is correct that renderer-definition loading is still tolerant rather than fail-loud:

- `src/renderers/registry.py:45`
- `src/renderers/registry.py:53`

It is correct that the current curated view/template validator is not clean enough to become a hard gate in the same tranche. I re-ran `validate_registered_view_contracts()` locally and got exactly:

- `23 total`
- `16 valid`
- `7 invalid`
- `10 skipped`

That matches:

- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md:109`

This is especially important because `view_contract_validator.py` is already scoped as curated-template preflight, not universal runtime truth:

- `src/presenter/view_contract_validator.py:117`

And `view_behavior_validator.py` is narrower still: it is raw-registry `card_grid` policy checking only, with explicit residual risk around runtime overrides:

- `src/presenter/view_behavior_validator.py:1`
- `src/presenter/view_behavior_validator.py:7`
- `src/presenter/view_behavior_validator.py:11`

The AOI half of the proposed proof surface is good. I locally checked the two round-6 AOI proof manifests:

- `proof-round5-adaptive-aoi-dossier-final-1774100000`
- `proof-round5-adaptive-aoi-comparison-final-1774100000`

Both yielded zero active manifest views whose `renderer_type` was missing from `src/renderers/definitions/`.

So the memo is right that round 9 is a real platform-law step rather than another disguised proof-token branch. It is moving at the next serious boundary. The main issue is that the genealogy proof slice is not yet described honestly enough for that claim.

## Bottom Line

The direction is right: no new proof token, bounded renderer-contract validation next, and `view_contract_validator.py` treated as preflight context rather than the hard gate.

But the memo needs revision before it becomes an execution plan. The biggest correction is that the current round-8 genealogy control routes are not yet a clean registry-backed proof slice. AOI is. Genealogy is not. Tighten that proof-surface claim, explicitly name the missing normal-path config-validation seam, and spell out the route/trace error-plumbing dependency. After that, this is a credible round-9 scope.
