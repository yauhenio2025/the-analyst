# Claude Review: Round 8 / Declarative Adaptive Suite Scope

Date: 2026-03-21
Reviewer: Claude Opus 4.6 (1M context)
Documents reviewed:
- `communications/MEMO_2026-03-21_round8_declarative_adaptive_suite_scope.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_completion.md`
- `communications/MEMO_2026-03-21_round6_cross_workflow_adaptive_aoi_suite_completion.md`
- `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_completion.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

Code inspected:
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

---

## Verdict

**Approve after revision**

The memo identifies the right structural variable and the right proof target. The program logic is sound: round 8 is the correct next bounded move, and the decision to pivot after it toward renderer contracts is well-reasoned. But the memo is technically under-specified in several places where the codebase reveals real implementation complexity that the scope language glosses over. Those gaps are fixable in a revision pass before planning — none of them invalidate the claim.

---

## Findings

Ordered by severity.

### F1. The existing declarative spec schema is single-surface — there is no suite-level schema (HIGH)

The current `AdaptiveCompositionSpec` in `src/presenter/adaptive_specs/schemas.py:54-91` defines:

```python
class AdaptiveCompositionSpec(BaseModel):
    composition_mode: str
    workflow_key: str
    target_surface: str          # singular
    signal_extractor_key: str    # singular
    default_family: str          # singular
    families: list[AdaptiveFamilySpec]
    decision_rules: list[AdaptiveDecisionRule]
```

This is structurally single-surface. A suite spec needs to coordinate **two** target surfaces, each with its own signal extractor, family catalog, decision rules, and default family. The memo says "add one bounded suite spec that names both target surfaces" (line 233) but does not acknowledge that the existing schema cannot express this.

The implementation has three options:

1. **Two spec files** — one per surface, composed by a suite wrapper. Reuses the existing schema without modification but requires a new suite-level coordination layer.
2. **New suite schema** — e.g. `AdaptiveSuiteCompositionSpec` with a `target_surfaces` list of per-surface sub-specs. Clean but means a second schema class.
3. **Widen existing schema** — make `target_surface` optional and add `target_surfaces: Optional[list[...]]`. Ugly; breaks the single-surface contract that round 7 validated.

The memo should declare which approach it recommends before planning, because the choice affects schema validation, registry loading, and the equivalence proof.

### F2. Conditions signal extractor is not registered in the declarative dispatch (HIGH)

`_declarative_signal_extractors()` at `bounded_dynamic_composition.py:1460-1463` currently registers exactly one extractor:

```python
def _declarative_signal_extractors() -> dict[str, Any]:
    return {
        SIGNAL_EXTRACTOR_KEY_RELATIONSHIP_SURFACE_SIGNALS_V1: _extract_relationship_surface_signals,
    }
```

Round 8 must add a conditions signal extractor. That extractor must implement `_select_adaptive_conditions_surface` logic (lines 1011-1111), which reads from `structured_data` rather than per-item cards and produces `AdaptiveConditionsSelection` rather than `AdaptiveSurfaceSelection`.

These are different dataclass types with different fields:

- `AdaptiveSurfaceSelection`: has `ordered_cards: tuple[dict, ...]`
- `AdaptiveConditionsSelection`: has `source_payload: dict[str, Any]`

The memo says round 8 should "reuse the existing conditions signal seam already proved in round 4" (line 235). That is correct, but the declarative dispatch path currently only returns `AdaptiveSurfaceSelection`. Either:

- The conditions extractor returns a different type, which means `_select_declarative_relationship_surface_family` and `_hydrate_relationship_surface_selection` cannot be reused directly for the conditions surface. The suite spec needs per-surface type awareness.
- Or the conditions path gets forced into the `AdaptiveSurfaceSelection` shape, which may lose the `source_payload` field.

The memo should state explicitly how the conditions signal extractor maps into the declarative dispatch contract.

### F3. `ALLOWED_BUILDER_TEMPLATE_KEYS` and `ALLOWED_SIGNAL_EXTRACTOR_KEYS` need widening (MEDIUM)

`src/presenter/adaptive_specs/keys.py` defines:

```python
ALLOWED_SIGNAL_EXTRACTOR_KEYS = frozenset({
    SIGNAL_EXTRACTOR_KEY_RELATIONSHIP_SURFACE_SIGNALS_V1,
})
ALLOWED_BUILDER_TEMPLATE_KEYS = frozenset({
    BUILDER_TEMPLATE_KEY_RELATIONSHIP_PROFILE_DOSSIER,
    BUILDER_TEMPLATE_KEY_RELATIONSHIP_COMPARISON_REVIEW,
})
```

Round 8 must add:
- A conditions signal extractor key
- `conditions_balance_sheet` and `conditions_path_dependency_matrix` builder template keys

This is mechanical, but Pydantic validation in `AdaptiveFamilySpec._validate_builder_template_key` and `AdaptiveCompositionSpec._validate_signal_extractor_key` will reject any conditions spec file until these sets are widened. The memo does not mention this; it should, to avoid false confidence that the existing spec infrastructure is "ready for suite use without schema changes."

### F4. Trace integration has a hardcoded composition-mode set (MEDIUM)

`decision_trace.py:93-99` lists the modes that should produce `inspect_runtime_composition` diagnostics:

```python
if composition_mode in {
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
}:
```

Round 8 must add the new declarative suite mode here. That is trivial. But `decision_trace.py` also has branching logic at lines 225-270 that determines the `stage_reason` text based on `stage_name`. The suite stage (`adaptive_surface_suite_selection`) already has a branch, so the declarative suite mode should map to that same stage name.

The memo correctly says "suite trace stays `adaptive_surface_suite_selection`" — that is consistent with `get_runtime_composition_stage_name()` at lines 328-341, which maps suite modes to that stage name. The trace contract should hold. This finding is medium because the memo gets the answer right but does not acknowledge the trace-integration touchpoints explicitly enough for an implementor to find them.

### F5. The `inspect_runtime_composition` function needs a declarative suite branch (MEDIUM)

`inspect_runtime_composition()` at `bounded_dynamic_composition.py:344-374` has explicit branches for each composition mode. Round 8 must add a branch for the declarative suite mode that constructs an `AdaptiveSurfaceSuiteSelection` from two declarative per-surface selections.

Currently the only suite inspection paths are:
- `_select_adaptive_relationship_conditions_suite` → hardcoded (line 356)
- `_select_adaptive_aoi_theme_report_suite` → hardcoded (line 359)

A declarative suite inspection needs to compose two declarative per-surface selections — which means loading the suite spec, extracting per-surface specs, running each declarative signal extractor, running each declarative family selector, and assembling the results into an `AdaptiveSurfaceSuiteSelection`.

This is the main structural work of round 8. The memo describes it at a high level but should be clearer that this function is the primary integration point.

### F6. The Critic workspace page needs one more proof label, not zero (LOW)

`AnalysisWorkspacePage.tsx` at lines 77-105 maps each composition mode constant to a proof label. Round 8 requires adding:

```typescript
const DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1 =
  'declarative_genealogy_relationship_conditions_suite_v1';
```

and a corresponding label entry like `"declarative suite proof"`. This is trivial but the memo says "no new host logic beyond one generic proof label if needed" — it should just say "one new proof label is needed."

### F7. Round-4 documentary control fixtures may need re-seeding (LOW)

The memo says the round-4 balance and matrix fixtures should serve as the documentary control for round 8. The round-4 completion memo notes these fixtures were stored as:

- `proof-round4-adaptive-balance-final-1774012011`
- `proof-round4-adaptive-matrix-final-1774012011`

The memo correctly acknowledges (lines 99-104) that if those fixtures are no longer present locally, equivalent controls can be re-seeded. This is honest. But it means the proof plan should include a fixture verification step before proof execution, not just hope they are there.

### F8. The `_apply_declarative_relationship_surface` function hardcodes `ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY` inside `_load_adaptive_spec_or_raise_validation` (LOW)

At `bounded_dynamic_composition.py:879`, the spec-loading error handler hardcodes the view key:

```python
CompositionIssue(
    view_key=ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    ...
)
```

For the conditions surface, this should reference the conditions view key, not the relationship one. The existing code does this because round 7 only had one surface. A suite lift should parameterize this. Minor, but a real bug if copied unchanged.

---

## What The Memo Gets Right

### Strong scope discipline

The memo consistently separates what is in scope from what should remain blocked. The "out of scope" list (lines 148-158) is well-chosen: excluding AOI, multi-workflow registries, spec-owned rationale prose, and general expression interpreters are all the right calls. These are the exact temptations that would turn round 8 from a proof into a product.

### Correct proof target

Genealogy relationship + conditions is the right first declarative suite target. It is already the most documented suite in the repo, the two surfaces have genuinely different selection shapes (per-item cards vs. top-level structured data), and the round-4 proof artifacts provide a documentary control that would be expensive to replicate elsewhere.

### Honest equivalence standard

The equivalence standard (lines 218-226) is well-calibrated. It asks for same selected family, same signal summary, same rationale text, same renderer shape — but does not demand byte-level trace identity. That is the right grain. The declarative path may legitimately differ in rejected-family lists (since the hardcoded path knows about `relationship_field_map` while the declarative path does not), and the memo implicitly allows for this via "where surfaces/families overlap." The round-7 tests already demonstrate this pattern at `test_declarative_adaptive_specs.py:366-369` with `issubset` rather than strict equality.

### Hard stops are real

The hard-stop list (lines 254-261) is not decorative. Each item names a specific failure mode that would indicate the work has drifted from bounded proof toward premature registry design. That list is the kind of thing that actually prevents scope creep in practice.

### Post-round-8 pivot is strategically right

The roadmap vision memo makes a compelling case that round 8 should be the last proof-ladder round. The proof family has now climbed from "can the host stay thin?" through "can adaptive behavior generalize across workflows?" to "can declarative specs drive it?" The remaining structural variable — declarative suite coordination — is the natural capstone. After that, more proofs would be repetitive; the program should move to renderer contracts and consumer consolidation.

---

## Big-Picture Assessment

### Is round 8 coherent with the larger memo trail?

Yes. The memo trail from March 16 through March 21 traces a clear arc: thin host → shared consumer contract → artifact seam → adaptive family → adaptive suite → cross-workflow → declarative single-surface → (proposed) declarative suite. Each round answered the smallest remaining structural question. Round 8 continues that pattern.

### Have we exceeded the useful proof ladder already?

Not quite, but we are at the edge. Round 7 proved declarative single-surface. The step from single-surface to suite is genuinely different — it requires coordinating two declarative per-surface selections under one composition-mode token with one trace grammar. That is not a trivial lift; it tests composition at a level the single-surface pilot did not. But round 9 (e.g., declarative AOI suite) would almost certainly be repetitive after round 8, because the structural variable it would test (declarative suite on a different workflow) is the same kind of variable that round 6 already exhausted for hardcoded suites.

The memo is right: round 8 is probably the last high-value proof round.

### If round 8 lands, should the next move really be renderer contracts / platform law?

Yes. The dynamic bespoke apps vision document (Section 9.3) makes the case clearly: `input_data_schema` exists in `RendererDefinition` but is unpopulated across all renderer JSONs. The table renderer definition at `src/renderers/definitions/table.json` is the exception — it already has a populated `input_data_schema` (lines 7-42). This is the only renderer with real contracts. The other six have empty or absent schemas.

Until renderer contracts are real, the composition substrate is building on trust. The adaptive and declarative proof work proves that family selection mechanics are sound, but it does not prove that the composed payloads are structurally valid for the target renderer. The next move should close that gap.

Renderer contracts before consumer consolidation also makes operational sense: consolidation will require the-critic to consume renderers from a shared package, and those renderers should validate their inputs before that migration surfaces silent shape mismatches at scale.

---

## Concrete Revisions Required Before Planning

### R1. Declare the suite spec schema approach

The memo must state whether round 8 will:

(a) use a **new suite-level spec schema** (e.g., `AdaptiveSuiteCompositionSpec` with per-surface sub-specs), or
(b) use **two separate single-surface spec files** coordinated by a bounded suite wrapper function, or
(c) **widen the existing schema** with optional plural fields.

Recommendation: option (a) is cleanest. A small `AdaptiveSuiteCompositionSpec` with a `surfaces: list[AdaptiveSurfaceSpec]` field would express the suite contract without polluting the single-surface schema. The memo should say this or explain why it chooses differently.

### R2. Acknowledge the conditions signal extractor dispatch gap

The memo should explicitly state that:

- A new conditions signal extractor key must be registered in `keys.py` and `_declarative_signal_extractors()`
- The conditions extractor returns `AdaptiveConditionsSelection`, not `AdaptiveSurfaceSelection`
- The declarative suite path must handle both types
- The conditions family ladder (`conditions_balance_sheet`, `conditions_path_dependency_matrix`) must be registered in `ALLOWED_BUILDER_TEMPLATE_KEYS`

One sentence noting these four touch-points is enough. Without it, an implementor will encounter Pydantic validation failures on the first conditions spec attempt and may not understand why.

### R3. Add `inspect_runtime_composition` and `decision_trace.py` to the integration-point list

The memo should name these two functions as explicit integration touch-points. `inspect_runtime_composition` needs a new branch for the declarative suite mode. `decision_trace.py` needs the new mode constant in its conditional set. Both are straightforward, but if the planning step does not identify them, the implementation risks missing them until test time.

### R4. Include a fixture verification step in the proof plan

The memo should require a fixture verification step:

- Before executing the declarative suite proof, confirm that the round-4 balance and matrix control fixtures are present in the local executor database
- If they are absent, re-seed from the documented fixture construction pattern before running the proof
- Document the fixture verification outcome in the proof note

This prevents a situation where the proof attempt fails not because of a code problem but because the control fixtures were lost between sessions.

### R5. Fix the hardcoded view key in `_load_adaptive_spec_or_raise_validation`

This is a minor code bug, not a memo revision. But the planning step should flag it: at `bounded_dynamic_composition.py:879`, the error-handler `CompositionIssue` hardcodes `ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY`. For conditions-surface errors, this should use the actual target surface key from the spec. The round-8 implementation should fix this as part of the suite lift.
