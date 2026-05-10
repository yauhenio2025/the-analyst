# Execution Plan: Round 7 / Declarative Adaptive Substrate Proof

Date: 2026-03-21
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md`

## Summary

Execute round 7 as a bounded declarative-substrate proof on the existing genealogy route.

Public proof contract:

- `/p/:projectId/analysis/intellectual_genealogy?composition_mode=declarative_relationship_surface_v1`

Bounded claim:

- analyzer-v2 can express one already-proven adaptive pattern through a repo-tracked JSON spec
- the runtime executor, validation path, and trace grammar remain code-owned
- the declarative mode matches the hardcoded adaptive relationship mode on dossier-like and comparison-like control signals
- the Critic host stays generic in substance

Round-7 proof boundary:

- target surface: `genealogy_relationship_landscape`
- declarative families in scope:
  - `relationship_profile_dossier`
  - `relationship_comparison_review`
- explicitly out of scope:
  - `relationship_field_map`

Hard stop conditions:

- if the adaptive-spec schema still requires freeform rule semantics, stop before implementation
- if builder/extractor dispatch cannot be expressed as a tiny code-owned registry, stop before implementation
- if the plan starts pulling rationale prose, trace-stage naming, or renderer JSON into the spec, stop and cut scope back

## Current Starting Point

### Already in code

The current relationship proof path in `src/presenter/bounded_dynamic_composition.py` already provides:

- `adaptive_relationship_surface_v1`
- deterministic extraction from `genealogy_relationship_landscape.items[*].structured_data`
- weighted relationship scoring
- three concrete runtime family builders:
  - dossier
  - comparison
  - field map
- `_validate_runtime_payload()` for consumer-capability and renderer/data validation
- `AdaptiveSurfaceSelection` with existing trace detail shape

The current trace path in `src/presenter/decision_trace.py` already provides:

- `adaptive_surface_selection` stage
- selected family / signal summary / rejected families / rationale details
- fail-closed invalid-mode handling with authored manifest retention

The presenter/result plumbing already threads `composition_mode` generically through:

- page assembly
- single-view loading
- manifest assembly
- result manifest
- result presentation
- refresh presentation

The repo already has a suitable pattern for JSON + Pydantic registries in:

- `src/views/registry.py`
- `src/transformations/registry.py`

The Critic host is already composition-mode-aware generically, but its proof-label mapping is explicit in:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`

The Critic client tests also explicitly enumerate current proof tokens in:

- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`

### What is still hardcoded and must widen

1. `src/presenter/bounded_dynamic_composition.py`
   - mode constants / supported-mode map
   - workflow authorization map
   - apply dispatch
   - inspect dispatch
   - trace-stage name dispatch
   - relationship family selection logic
   - relationship family -> builder routing

2. `src/presenter/decision_trace.py`
   - the inspected adaptive-mode allowlist only includes current hardcoded modes

3. There is no adaptive-spec schema, registry, or definitions directory yet.

4. There is no runtime dispatch layer for:
   - `signal_extractor_key`
   - `builder_template_key`

5. Route and contract tests still enumerate the currently known proof modes explicitly.

## Execution Strategy

Execute round 7 as a thin-registry equivalence tranche, not a generalized declarative platform rollout.

That means:

1. preserve the existing hardcoded relationship mode unchanged
2. introduce one new proof token only:
   - `declarative_relationship_surface_v1`
3. introduce one tiny adaptive-spec registry under `src/presenter/`
4. keep signal extraction, rationale generation, rejected-family reasons, validation, and trace grammar in code
5. prove automated equivalence with synthetic dossier/comparison controls
6. close with route-real documentary evidence on the existing round-3 proof jobs

## Work Packages

### WP0: Freeze The Adaptive-Spec Schema Before Runtime Wiring

Goal:

- lock the v1 declarative boundary before implementation fans out into dispatch code

New files:

- `src/presenter/adaptive_specs/__init__.py`
- `src/presenter/adaptive_specs/schemas.py`
- `src/presenter/adaptive_specs/registry.py`
- `src/presenter/adaptive_specs/definitions/declarative_relationship_surface_v1.json`

Schema requirements:

- `composition_mode`
- `workflow_key`
- `target_surface`
- `signal_extractor_key`
- `default_family`
- `families[]`
- `decision_rules[]`

Family entry requirements:

- `family_key`
- `builder_template_key`
- `view_name`

Spec exclusions:

- no trace stage names
- no rationale templates
- no rejected-family templates
- no renderer JSON
- no user-authored code

Rule grammar for v1:

- ordered first-match wins
- one positive dossier rule
- one explicit `default_family = relationship_comparison_review`
- bounded predicate operators only

Freeze legal operators in the schema:

- `eq`
- `gte`
- `lte`

Freeze legal rule structure in the schema:

- one rule contains one or more conjunctive predicate sets
- the rule matches if any predicate set matches
- no deeper nesting than that

Recommended concrete rule shape:

```json
{
  "family_key": "relationship_profile_dossier",
  "match_any": [
    [
      { "metric": "relationship_count", "operator": "eq", "value": 1 }
    ],
    [
      { "metric": "top_share", "operator": "gte", "value": 0.45 },
      { "metric": "score_gap", "operator": "gte", "value": 5 }
    ]
  ]
}
```

Recommended v1 spec skeleton:

```json
{
  "composition_mode": "declarative_relationship_surface_v1",
  "workflow_key": "intellectual_genealogy",
  "target_surface": "genealogy_relationship_landscape",
  "signal_extractor_key": "<freeze exact enum in WP0>",
  "default_family": "relationship_comparison_review",
  "families": [
    {
      "family_key": "relationship_profile_dossier",
      "builder_template_key": "<freeze exact enum in WP0>",
      "view_name": "Relationship Dossier"
    },
    {
      "family_key": "relationship_comparison_review",
      "builder_template_key": "<freeze exact enum in WP0>",
      "view_name": "Relationship Comparison Review"
    }
  ],
  "decision_rules": [
    {
      "family_key": "relationship_profile_dossier",
      "match_any": [
        [{ "metric": "relationship_count", "operator": "eq", "value": 1 }],
        [
          { "metric": "top_share", "operator": "gte", "value": 0.45 },
          { "metric": "score_gap", "operator": "gte", "value": 5 }
        ]
      ]
    }
  ]
}
```

Preflight validation must fail if:

- `default_family` is missing
- `default_family` is not declared in `families`
- an unknown operator is used
- `signal_extractor_key` is not in the legal enum
- `builder_template_key` is not in the legal enum
- duplicate `family_key` values exist
- a rule references an undeclared family

Important implementation rule:

- unlike `ViewRegistry` and `TransformationRegistry`, invalid adaptive specs must fail loudly for this proof tranche
- do not silently log-and-skip malformed specs

### WP1: Add A Thin Presenter-Side Adaptive-Spec Registry

Goal:

- load and validate the adaptive spec through one minimal registry, with no plugin system and no cross-module indirection maze

Files:

- `src/presenter/adaptive_specs/schemas.py`
- `src/presenter/adaptive_specs/registry.py`
- `src/presenter/adaptive_specs/definitions/declarative_relationship_surface_v1.json`

Implementation shape:

1. Use the same JSON-per-file + singleton registry pattern as:
   - `src/views/registry.py`
   - `src/transformations/registry.py`

2. Keep the registry tiny:
   - `get(composition_mode)`
   - `load()`
   - `reload()`
   - `list_keys()`

3. Make schema validation strict via Pydantic `model_validate`.

4. Make registry integrity validation explicit:
   - verify unique composition modes
   - verify the definitions directory exists
   - verify all loaded specs pass schema and enum checks

5. Add one small exception type for invalid adaptive-spec definitions if needed, but keep route-level handling explicit in presenter code.

No scope creep in WP1:

- no remote loading
- no user editing API
- no generalized registry CRUD
- no spec authoring UI

### WP2: Refactor The Relationship Path Into Shared Extraction + Two Family Choosers

Goal:

- avoid duplicating the existing relationship extractor/builders while enabling one declarative chooser alongside the current hardcoded chooser

Primary file:

- `src/presenter/bounded_dynamic_composition.py`

Required refactor:

Split the current relationship path into four conceptual pieces:

1. relationship signal extraction
   - extract cards
   - decorate cards
   - aggregate `signal_summary`

2. hardcoded family chooser
   - preserve current `adaptive_relationship_surface_v1` behavior exactly

3. declarative family chooser
   - evaluate the loaded spec against the extracted signals

4. code-owned rationale / rejected-family generation
   - keep this in Python
   - do not move this into JSON

Concrete target:

- the hardcoded mode should keep using the existing three-family chooser
- the declarative mode should use the shared extractor but only the two-family pilot chooser

This is the key architectural split for round 7.

### WP3: Implement The Declarative Relationship Mode In The Runtime Dispatcher

Goal:

- add the new proof-only mode and route it through the existing presenter/result plumbing

Files:

- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`

Required backend changes:

1. Add new mode constant:
   - `COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1 = "declarative_relationship_surface_v1"`

2. Add it to:
   - `_SUPPORTED_COMPOSITION_MODES`
   - `_MODE_WORKFLOW_MAP`

3. Add runtime apply branch:
   - `_apply_declarative_relationship_surface(payloads, consumer_key)`

4. Add inspect branch:
   - the declarative mode must still emit `AdaptiveSurfaceSelection.as_trace_details()`

5. Keep the same trace-stage grammar:
   - `get_runtime_composition_stage_name()` should return `adaptive_surface_selection`

6. Add one extractor dispatch map keyed by `signal_extractor_key`.

7. Add one builder dispatch map keyed by `builder_template_key`.

8. Keep both maps code-owned and tiny for v1:
   - exactly one legal extractor key
   - exactly two legal builder keys

9. Build the declarative selection path as:
   - load spec by `composition_mode`
   - verify target surface and workflow match request
   - run code-owned extractor
   - evaluate ordered rules
   - fall back to explicit `default_family`
   - generate rationale/rejected-family prose in code
   - resolve family -> builder template key
   - build payload using the existing relationship builders
   - validate payload with `_validate_runtime_payload()`

10. Keep route-level validation behavior hardcoded:
   - invalid mode/workflow -> 400
   - invalid spec / invalid runtime payload -> 409

Important round-7 constraint:

- `relationship_field_map` stays untouched in the hardcoded mode
- the declarative pilot does not register or select it
- do not delete, rework, or weaken the field-map code path

### WP4: Wire Declarative Inspection Into Decision Trace Without Inventing A New Grammar

Goal:

- keep round 7 inside the existing trace contract

Files:

- `src/presenter/decision_trace.py`
- `tests/test_manifest_trace.py`

Required changes:

1. Import the new declarative mode constant.

2. Add it to the inspected adaptive-mode set in `build_presentation_trace()`.

3. Ensure trace output remains shaped like existing adaptive single-surface traces:
   - `target_surface`
   - `selected_family`
   - `signal_summary`
   - `rejected_families`
   - `rationale`

4. Keep the stage name:
   - `adaptive_surface_selection`

5. Ensure invalid declarative spec/runtime cases still produce:
   - `composition_status = invalid`
   - composed stage diagnostics
   - authored final manifest retained

This is a proof of declarative selection, not a proof of a new trace language.

### WP5: Backend Equivalence And Invalid-Path Test Coverage

Goal:

- make round-7 proof coverage explicit and synthetic-control-based

Files:

- `tests/test_presentation_api.py`
- `tests/test_manifest_trace.py`
- `tests/test_analysis_product_contract.py`
- new file:
  - `tests/test_adaptive_spec_registry.py`
    or
  - `tests/test_declarative_adaptive_specs.py`

Required tests:

#### A. Adaptive-spec schema / registry tests

1. valid round-7 spec loads successfully
2. missing `default_family` fails
3. unknown operator fails
4. unknown `signal_extractor_key` fails
5. unknown `builder_template_key` fails
6. duplicate family keys fail
7. undeclared-family rule target fails

#### B. Synthetic equivalence controls

Build two synthetic payload maps that reproduce the round-3 control shapes:

1. dossier-like signal distribution
   - one clear dominant relationship
   - expect `relationship_profile_dossier`

2. comparison-like signal distribution
   - multiple materially comparable relationships
   - expect `relationship_comparison_review`

For each control:

1. apply `adaptive_relationship_surface_v1`
2. apply `declarative_relationship_surface_v1`
3. normalize outputs by removing mode-specific metadata
4. assert equivalence for:
   - selected family
   - renderer type
   - normalized renderer_config
   - normalized structured_data
   - `derivation_kind`
   - `source_parent_view_key`
   - trace detail shape

Do not compare:

- `composition_mode`
- `presentation_hash`
- `presentation_content_hash`
- timestamps

#### C. Declarative invalid-path tests

1. invalid spec produces route-level `409`
2. invalid runtime payload still produces route-level `409`
3. trace returns `composition_status = invalid` with authored manifest retained
4. missing adaptive target surface still fails closed

#### D. Result/presenter threading tests

Backfill the same route/contract coverage currently used for other proof modes:

1. result manifest preserves the declarative mode
2. result presentation threads the mode to page assembly
3. refresh presentation threads the mode
4. single-view route threads the mode
5. presenter page route maps proof validation failure to `409`

### WP6: Critic Host — One Label Mapping Plus Minimal Regressions

Goal:

- keep the host generic while making the new proof token visible and tested

Files:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`

Required changes:

1. Add one proof-label mapping:
   - `declarative_relationship_surface_v1 -> declarative adaptive substrate proof`
   or similarly short generic proof text

2. Add one page-level regression:
   - generic restore shows the proof label
   - no workflow-specific host logic is added

3. Add one integration regression:
   - generic restore threads the declarative token end-to-end
   - lazy single-view load preserves the token
   - skip-cache behavior remains generic

4. Extend the explicit `compositionMode` arrays in `boundedV2Client.test.ts` to include the new token.

No host-surface work in WP6:

- no workflow-specific rendering
- no substrate-specific UI
- no alternate execution path

### WP7: Manual Route Proof And Round-7 Closure Note

Goal:

- close the stage with route-real evidence, while keeping the automated equivalence proof synthetic and deterministic

Manual routes:

- hardcoded control:
  - `/p/:projectId/analysis/intellectual_genealogy?composition_mode=adaptive_relationship_surface_v1`
- declarative candidate:
  - `/p/:projectId/analysis/intellectual_genealogy?composition_mode=declarative_relationship_surface_v1`

Use the existing round-3 documentary controls:

- `proof-round3-adaptive-dossier-final-1774002300`
- `proof-round3-adaptive-comparison-final-1774002300`

Required checks:

1. open the hardcoded adaptive route on the dossier control
2. open the declarative route on the dossier control
3. confirm the same visible family title renders
4. repeat for the comparison control
5. inspect trace for both declarative runs
6. confirm `adaptive_surface_selection` grammar and selected-family parity on both controls

Record artifacts:

- screenshots
- extracted page text
- trace JSON

Write one short closure/proof note after execution, recording:

1. route used
2. proof token
3. control jobs used
4. selected family per control
5. focused test results
6. route-real comparison result
7. the exact bounded claim closed

## Acceptance Checklist

Treat round 7 as complete only if all of the following are true:

1. the adaptive-spec schema is frozen and validated by tests
2. the presenter-side adaptive-spec registry exists and fails loudly on bad definitions
3. the hardcoded relationship mode remains behaviorally unchanged on existing tests
4. the declarative mode is wired through supported-mode validation, runtime dispatch, result contracts, and trace inspection
5. dossier-like and comparison-like synthetic controls normalize equal between hardcoded and declarative modes
6. invalid declarative spec/runtime cases fail closed with `409`, not `500`
7. the Critic generic host shows the new proof label and forwards the token generically
8. a round-7 closure note records route-real declarative proof against the two round-3 documentary controls
9. no claim is made that round 7 proves field-map parity or generalized declarative substrate rollout

## What Not To Do During Execution

Do not:

- declarativize `relationship_field_map` in round 7
- widen to suite-mode substrate work
- move rationale prose or rejected-family prose into JSON
- introduce plugin loading, remote loading, or runtime code evaluation
- add workflow-specific Critic behavior
- compare raw manifest hashes across modes as the equivalence standard
- claim universal parity for all relationship-surface signal shapes

## Bottom Line

Round 7 should be implemented as a minimal declarative executor sitting on top of the existing relationship extractor, existing builders, existing validation, and existing trace grammar.

If execution stays inside that boundary, the tranche proves something real. If it expands into freeform rule evaluation, templated prose, or three-family parity claims, it stops being the bounded substrate proof the revised memo now correctly scopes.
