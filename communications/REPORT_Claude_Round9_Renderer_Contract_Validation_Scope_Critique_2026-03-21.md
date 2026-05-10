# Claude Review: Round 9 / Renderer Contract Validation Scope

Date: 2026-03-21
Reviewer: Claude Opus 4.6 (1M context)

Documents reviewed:
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_completion.md`
- `communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

Code inspected:
- `src/renderers/registry.py`
- `src/renderers/validator.py`
- `src/renderers/definitions/*.json` (all 9 renderer definitions)
- `src/presenter/presentation_api.py` (`_validate_payload_data`)
- `src/presenter/presentation_bridge.py` (`_validate_transform_output`)
- `src/presenter/bounded_dynamic_composition.py` (`_validate_runtime_payload`)
- `src/presenter/view_contract_validator.py`
- `src/presenter/view_behavior_validator.py`
- `src/presenter/decision_trace.py`
- `src/api/routes/results.py`
- `src/api/routes/presenter.py`

---

## Verdict

**Approve after revision**

Renderer contract validation is the right next move. The memo correctly identifies the strategic position and the three-layer distinction. But the memo under-specifies the actual enforcement mechanism and over-states one gap that the codebase has already closed. Those issues are fixable in a revision pass.

---

## Findings

### F1. The memo's premise about unpopulated `input_data_schema` is out of date (HIGH)

The Dynamic Bespoke Apps vision document (Section 9.3) and the round-8 roadmap memo both cite unpopulated `input_data_schema` as a major gap. The round-9 memo inherits this framing implicitly.

But the actual renderer catalog tells a different story:

| Renderer | input_data_schema | Quality |
|----------|------------------|---------|
| accordion | populated | Full — oneOf with minProperties |
| card_grid | populated | Full — oneOf array/keyed object |
| evidence_trail | populated | Minimal — permissive additionalProperties:true |
| prose | populated | Full — oneOf string/object |
| raw_json | populated | Empty `{}` — intentional for diagnostic use |
| stat_summary | populated | Full — oneOf value types |
| tab | populated | Full — oneOf with minProperties |
| table | populated | Full — multi-table/flat/keyed |
| timeline | populated | Full — array of objects with required fields |

**All 9 renderers have `input_data_schema` defined.** 7 of 9 have substantive schemas capable of rejecting malformed data. The remaining 2 (evidence_trail, raw_json) are intentionally permissive.

This means the round-9 claim should not be framed as "populate missing renderer schemas." The schemas are already there. The round-9 claim should be framed as "make the existing schemas enforceable on the serve path."

The memo should acknowledge this explicitly. The gap is not schema authoring — it is enforcement policy.

### F2. The memo does not specify what "fail-closed on the serving path" actually means mechanically (HIGH)

The memo says round 9 should make "renderer config/data validation real on the shared presenter-serving path" (line 191). But it does not specify the enforcement mechanism.

The codebase already has the exact code seam where this would happen:

- `src/presenter/presentation_api.py:_validate_payload_data()` — currently calls `validate_renderer_data(..., mode=ValidationMode.WARN)`. Making this STRICT is literally changing one enum value.
- `src/presenter/presentation_bridge.py:_validate_transform_output()` — same pattern, currently WARN.

But switching to STRICT has consequences the memo does not address:

1. **What happens when `schema_available=False`?** Currently, `validate_renderer_data()` at `src/renderers/validator.py:105-110` returns `valid=True` when the renderer is not in the registry or has no schema. Under strict mode, should "no schema" mean "pass" or "fail"? The memo must state a policy.

2. **The two active views with unregistered renderer types** (`genealogy_per_work_scan -> card`, `lines_of_attack_overview -> prose_narrative`) would pass validation under the current "no schema = pass" rule. But if round 9 tightens the policy to "unregistered renderer = fail," those views break on the serve path. The memo acknowledges these views exist (line 116-117) but does not state whether round 9 should fix, exempt, or ignore them.

3. **Should enforcement happen at assembly time (all views) or serve time (per request)?** If at assembly time, every page build that includes a view with malformed data would fail. If at serve time, only the specific requested view would fail. The memo should pick one.

### F3. `_validate_runtime_payload` validates consumer support, not renderer schemas — the memo conflates these (MEDIUM)

The memo says at line 86-91 that `_validate_runtime_payload()` "already fail-closes renderer support by consumer, renderer config schema, renderer data schema."

This is partially incorrect. Inspecting `bounded_dynamic_composition.py:2867-2945`, `_validate_runtime_payload` validates:

- Whether the renderer type is in the consumer's supported renderers list
- Whether section renderer types are supported
- Whether sub-renderer types are supported

It does **not** validate renderer config or data against JSON schemas. That validation happens separately via `validate_renderer_data()` and `validate_renderer_config()` in `src/renderers/validator.py`, which is called from the warn-only paths in `presentation_bridge.py` and `presentation_api.py`.

The memo should distinguish between:

- **Consumer capability validation** (already strict, in bounded composition)
- **Renderer schema validation** (currently warn-only, in bridge/assembly)

These are different enforcement surfaces. Round 9 is about the second one, not the first.

### F4. The memo does not address the "what to do with invalid payloads" question (MEDIUM)

If renderer schema enforcement becomes fail-closed, the memo needs to answer: what happens to the response?

Options:

(a) **Strip the failing view from the page presentation.** The page still renders, minus the invalid view. Diagnostic trace shows what was removed and why.

(b) **Fail the entire page request with 409.** The whole page is rejected if any view fails validation. This is the bounded composition pattern.

(c) **Downgrade the failing view to raw_json or a diagnostic renderer.** The page still renders, but the failing view shows its raw data instead of a broken renderer.

The memo says "renderer contract failures are platform-law violations, not warning-only log lines" (line 291). That rules out the current warn-only behavior. But it does not pick between strip, reject, or downgrade. The execution plan needs this decision.

### F5. Renderer registry load tolerance should stay tolerant at runtime (LOW)

The memo says the renderer registry "should stop silently degrading when a repo-tracked definition is broken" (line 187). That is correct for CI/startup validation. But at runtime, the registry is a read-heavy cache — a single malformed renderer definition should not crash the entire API server.

The recommended approach is:

- **CI/load tests**: fail-loud (test that `load()` succeeds without errors)
- **Runtime**: keep the current tolerant loading but add a health endpoint or startup check

The memo should clarify that "fail-loud" means "fail in CI," not "crash the server at import time."

### F6. The proof standard is appropriate but under-specified (LOW)

Reusing the round-8 genealogy and round-6 AOI control routes is the right call — no new tokens, no new proof branches. But the memo should specify what "survive strict renderer-contract enforcement" means in practice:

- Does it mean the control routes still return 200 with valid page presentations under strict mode?
- Does it mean the trace diagnostics show zero renderer-contract violations?
- Does it mean the existing proof screenshots still match after enforcement is enabled?

The proof standard should be: "existing control routes produce identical page presentations under strict enforcement, with zero renderer-contract issues in the trace."

---

## What The Memo Gets Right

### Strategic positioning is correct

Renderer contract validation is genuinely the right next move after the proof ladder. The adaptive/declarative work proved that family selection mechanics are sound. The missing layer is whether the composed payloads are structurally valid for the target renderer. This is exactly what the Dynamic Bespoke Apps vision (Section 9.3, Priority 1) and the round-8 roadmap memo both identify as the next platform gap.

### The three-layer distinction is real and useful

The separation of renderer schema health, runtime payload contract validity, and curated view/template contract fidelity (lines 244-277) maps cleanly to the actual codebase:

1. **Schema health** = `src/renderers/validator.py:validate_all_schemas()` — already works, all 9 pass
2. **Runtime payload validity** = `validate_renderer_data()` + `validate_renderer_config()` — infrastructure exists, mode needs switching
3. **Curated contract fidelity** = `src/presenter/view_contract_validator.py` — shows 7/23 invalid, not yet ready for hard-gating

The memo is right that round 9 should focus on layer 2 and treat layer 3 as context.

### Bounded scope discipline is maintained

The out-of-scope list (lines 228-239) correctly blocks: global strictness flip, full legacy cleanup, new composition tokens, and renderer redesign. The memo resists the temptation to turn round 9 into a diffuse catalog-cleanup project.

### No new composition tokens

Not inventing a new proof token is the right discipline. The proof ladder is closed. Round 9 should prove that the existing platform contracts become enforceable, not that another composition variant works.

---

## Bottom Line

Renderer contract validation is the correct next move. The infrastructure is more ready than the memo acknowledges — all 9 renderer schemas are populated, the validator already supports strict mode, and the enforcement seam is a one-line mode change. The real work is deciding the failure policy (strip vs. reject vs. downgrade), handling unregistered renderer types, and building the test/proof envelope.

Revise the memo to:
1. Acknowledge that `input_data_schema` is already populated across all 9 renderers
2. Distinguish consumer capability validation (already strict) from renderer schema validation (currently warn-only)
3. State the failure policy for invalid payloads on the serve path
4. State the policy for views whose renderer type has no registry entry
5. Clarify that "fail-loud" for registry loading means CI/test failure, not runtime crash
6. Tighten the proof standard to "identical page presentations under strict enforcement with zero renderer-contract issues in trace"
