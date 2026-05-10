# Audit: Round 7 / Declarative Adaptive Substrate Scope

Date: 2026-03-21
Memo under review: `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md`

## Verdict

Approve after revision.

The program direction is right: after rounds 1 through 6, the next meaningful variable is no longer "can adaptive selection work?" but "can one proven adaptive mode be lifted into a bounded static substrate without losing determinism, fail-closed validation, and trace inspectability." The memo is correct to keep round 7 single-surface, proof-only, and explicitly non-interpreter (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:117-131`, `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:194-223`).

But the memo is not execution-plan ready as written. The biggest issue is that it declares a three-family substrate while its own control standard only reuses the two round-3 route fixtures. That leaves `relationship_field_map` outside the stated equivalence proof even though it is inside the proposed declarative catalog (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:242-246`, `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:314-325`, `communications/PROOF_2026-03-20_round3_adaptive_surface_family.md:36-58`).

## Findings

### 1. The memo’s equivalence control does not cover all three families it wants to declarativize

The memo scopes `relationship_profile_dossier`, `relationship_comparison_review`, and `relationship_field_map` into the proposed family catalog (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:242-246`). But its required control pair is only the two round-3 proof fixtures (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:314-325`), and the round-3 proof record itself only contains route-real dossier and comparison cases (`communications/PROOF_2026-03-20_round3_adaptive_surface_family.md:36-58`, `communications/MEMO_2026-03-20_round3_adaptive_surface_family_completion.md:83-111`).

`relationship_field_map` is real code, but its strongest evidence in this repo is unit-level adaptation coverage, not route-real control coverage (`src/presenter/bounded_dynamic_composition.py:1391-1471`, `tests/test_presentation_api.py:673-698`). That means the memo currently asks round 7 to prove declarative equivalence for one family that the stated control strategy does not actually control.

This is the most important revision needed before execution planning. Either:

- cut round 7 to a two-family dossier/comparison pilot, or
- add a third route-real field-map control fixture before turning the memo into a plan.

### 2. The memo understates how many dispatch points and validation seams would have to widen

Today the substrate is not registry-driven. It is hardcoded in one module plus all the shared composition-mode plumbing around it.

- Mode authorization is a hardcoded token set and workflow map in `src/presenter/bounded_dynamic_composition.py:15-50` and `src/presenter/bounded_dynamic_composition.py:236-260`.
- Runtime apply dispatch is a hardcoded `if` ladder in `src/presenter/bounded_dynamic_composition.py:263-301`.
- Trace-stage mapping and inspect dispatch are hardcoded in `src/presenter/bounded_dynamic_composition.py:304-342`.
- The composed payload path is invoked from `_prepare_page_payloads_for_recommendations()` in `src/presenter/presentation_api.py:679-787`.
- Manifest, page, and single-view assembly all thread `composition_mode` through that path in `src/presenter/presentation_api.py:837-1009`.
- Result manifest, result presentation, and refresh also thread the token and depend on the same validation behavior in `src/analysis_products/result_contract.py:273-450`.
- HTTP-level 400/409 mapping is duplicated across presenter and results routes in `src/api/routes/presenter.py:142-287` and `src/api/routes/results.py:44-116`.
- Route tests enumerate the currently supported proof modes explicitly in `tests/test_analysis_product_contract.py:1430-1510`.

The memo’s language about a new declarative mode being "independent" is directionally right (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:176-192`), but execution is not "one new token." It is a multi-file widening of authorization, dispatch, inspection, trace, result-contract threading, route mapping, and tests.

### 3. The proposed spec shape includes fields that are not grounded in the current relationship path and pull the design toward a new interpreter

The memo wants the spec to declare `trace_stage_name`, `description_template`, and `trace_rationale_template` (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:230-254`). Those fields do not match how the live relationship path works.

- Trace stage naming is code-owned by `get_runtime_composition_stage_name()` and currently collapses adaptive single-surface modes onto the existing `adaptive_surface_selection` grammar (`src/presenter/bounded_dynamic_composition.py:304-316`, `src/presenter/decision_trace.py:220-279`).
- Relationship rationales are produced in selector code, not builder metadata, by `_choose_relationship_surface_family()` (`src/presenter/bounded_dynamic_composition.py:1020-1081`).
- Builders then reuse `selection.rationale` as the view description instead of deriving new prose from templates (`src/presenter/bounded_dynamic_composition.py:1329-1345`, `src/presenter/bounded_dynamic_composition.py:1365-1388`, `src/presenter/bounded_dynamic_composition.py:1455-1471`).

If round 7 adds templated rationale/description fields, it is no longer only "config choosing among registered builders." It is introducing a new interpolation layer for user-facing trace and description prose. That is exactly the kind of extra runtime the memo says it does not want.

### 4. “Registered signal extractor + registered builder templates + declarative decision ladder” only proves something new if the generic substrate actually owns the mode

As implemented today, the proof modes are still token-specific code paths:

- relationship selection is `_select_adaptive_relationship_surface()` plus `_choose_relationship_surface_family()` (`src/presenter/bounded_dynamic_composition.py:605-670`, `src/presenter/bounded_dynamic_composition.py:1020-1081`)
- relationship family application is direct builder dispatch in `_apply_adaptive_relationship_surface()` (`src/presenter/bounded_dynamic_composition.py:455-484`)
- builder implementations are concrete runtime payload constructors, not registry entries (`src/presenter/bounded_dynamic_composition.py:1227-1471`)

I also did not find any existing runtime composition registry for `signal_extractor_key` or `builder_template_key` in `src/`; those names only appear in the memo/prompt during this audit. So unless round 7 introduces:

- a real spec schema,
- a real spec loader,
- a real generic rule evaluator, and
- a real generic builder-key-to-function resolver,

the change mostly moves thresholds and family metadata out of Python and into a file.

That is not worthless, but it is weaker than the memo’s framing. The proof value is not "declarative substrate exists" unless the generic substrate is actually what reads and executes the mode.

### 5. `declarative_relationship_surface_v1` is still the right route-facing pilot, but not for the reason the memo gives

The memo says `genealogy_relationship_landscape` is best because it is the simplest mature seam and simpler than AOI (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:141-168`). The maturity part is right; the raw seam-simplicity part is overstated.

The relationship surface still depends on:

- a `per_item` authored view contract, not a top-level structured object (`src/views/definitions/genealogy_relationship_landscape.json:36-42`)
- reconstruction from `payload.items[*].structured_data` (`src/presenter/bounded_dynamic_composition.py:1999-2018`)
- weighted scoring over relationship-type and relationship-strength enums (`src/presenter/bounded_dynamic_composition.py:52-64`, `src/presenter/bounded_dynamic_composition.py:2247-2271`)

By comparison, the AOI theme selector reads one top-level structured payload and already preserves authored order metadata after the round-5 seam repair (`src/views/definitions/aoi_by_theme.json:52-90`, `src/presenter/bounded_dynamic_composition.py:798-948`, `src/presenter/bounded_dynamic_composition.py:2036-2070`, `communications/PROOF_2026-03-21_round5_cross_workflow_adaptive_aoi_theme.md:191-206`).

So the real reason to prefer the relationship pilot is not "simplest code path." It is:

- best existing control record,
- earliest and most mature proof seam,
- single-surface route,
- no child-surface parent contract,
- no late documentary bug in the current proof memo set.

That is enough. The memo should just say that plainly.

### 6. The test/proof strategy needs a canonicalized equivalence method because raw manifest hashes are designed to differ across modes

The memo says the declarative mode should be behaviorally equivalent to `adaptive_relationship_surface_v1` (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:319-327`). But raw manifest equality is not the right compare method because `composition_mode` is part of both the contract and content fingerprints in `build_effective_manifest()` (`src/presenter/manifest_builder.py:223-250`), and the test suite explicitly asserts that hashes change when `composition_mode` changes (`tests/test_manifest_trace.py:398-429`).

So a real equivalence proof cannot be:

- "same presentation hash"
- "same presentation_content_hash"

It has to compare normalized outputs after removing mode-specific metadata. The memo currently says "equivalent in substance" but does not define that substance.

## What Is Actually Well-Scoped

- One existing route, one existing authored surface, and one proof-only token is the right scale. The memo is correct not to bundle suite coordination into round 7 (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:151-158`).
- Keeping signal extraction, builder implementations, validation calls, trace schema, and route error mapping in code is the right boundary (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:288-306`).
- Reusing the existing `adaptive_surface_selection` trace grammar is the right target. The current single-surface adaptive path already has a stable trace shape for selected family, signal summary, rejected families, and rationale (`src/presenter/bounded_dynamic_composition.py:73-95`, `src/presenter/decision_trace.py:220-279`).
- Reusing the round-3 control route is strategically correct for dossier/comparison. Those fixtures are still the cleanest relationship-surface controls in the repo (`communications/PROOF_2026-03-20_round3_adaptive_surface_family.md:36-167`).
- The safest first declarativization boundary is the decision ladder plus family-key-to-builder mapping for the relationship surface. That is the piece of the current path that can move into a spec without reopening signal extraction or payload construction.

## What Is Under-Specified Or Risky

- There is no proposed schema or lifecycle for the new composition spec itself. The memo says "repo-tracked static configuration" but does not say how it is loaded, validated, or versioned before routes call into it (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:206-238`).
- There is no bounded predicate grammar yet. `decision_rules[]` needs a fixed operator set and a required default/fallthrough rule; otherwise round 7 becomes a rule-engine implementation disguised as config (`communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md:265-286`).
- `signal_extractor_key` and `builder_template_key` imply registries that do not currently exist in the runtime composition path. Without explicit referential-integrity validation, bad specs will fail as 500s or ad hoc exceptions rather than the current 400/409 contract.
- `trace_stage_name` should not be data-driven in round 7. The memo says trace emission and schema stay hardcoded, and that should include stage naming.
- `description_template` and `trace_rationale_template` are not safe first declarativizations. They require a new text-template layer and are not needed to prove bounded declarative selection.
- The current tests prove direct adaptation and trace detail for the relationship surface, but they do not prove cross-mode equivalence against route-real round-3 controls (`tests/test_presentation_api.py:616-698`, `tests/test_manifest_trace.py:1056-1169`).

## Recommended Revisions Before Execution Planning

1. Narrow the family catalog or widen the control set.
Either make round 7 a two-family dossier/comparison pilot, or add a third route-real field-map control fixture. Do not keep a three-family declarative catalog with a two-fixture equivalence standard.

2. Strip non-essential templating fields out of the v1 spec.
Remove `trace_stage_name`, `description_template`, and `trace_rationale_template` from round 7. Keep stage naming and rationale prose in code.

3. Define the actual declarative boundary explicitly.
Round 7 should only declarativize:
`composition_mode`, `workflow_key`, `target_surface`, `signal_extractor_key`, `families[]`, and an ordered decision ladder over fixed numeric predicates.
Round 7 should keep hardcoded:
signal extraction, scoring weights, builder implementations, payload mutation defaults, trace prose, validation calls, and route error mapping.

4. Specify the generic executor seam in code terms.
The execution plan should say exactly which code path becomes generic:
- validate mode against loaded spec
- resolve one hardcoded extractor by key
- compute `signal_summary`
- evaluate ordered rules
- resolve one hardcoded builder by family key
- run `_validate_runtime_payload()`
- emit existing `adaptive_surface_selection` trace details

5. Add a real spec-validation layer before runtime payload validation.
The plan should include startup/load-time checks for:
- unknown `workflow_key`
- unknown `target_surface`
- unknown extractor key
- unknown family key / builder key
- duplicate family keys
- missing default rule
- unreachable or ambiguous rules

6. Define equivalence as a normalized compare, not hash equality.
For each control fixture, compare:
- selected family
- trace stage name
- renderer type
- normalized renderer-config shape
- normalized structured-data keys/rows
- `derivation_kind`
- `source_parent_view_key`
- fail-closed behavior for invalid mode/spec/payload

Ignore:
- `composition_mode`
- `presentation_hash`
- `presentation_content_hash`
- timestamps

7. Enumerate the code seams up front in the execution plan.
At minimum the plan will touch:
- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`
- `src/presenter/presentation_api.py`
- `src/analysis_products/result_contract.py`
- `src/api/routes/presenter.py`
- `src/api/routes/results.py`
- the proof-token test matrices in `tests/test_presentation_api.py`, `tests/test_manifest_trace.py`, and `tests/test_analysis_product_contract.py`

## Bottom Line

Round 7 is the right next category of proof. Another hardcoded workflow branch would be lower value than a bounded declarative substrate experiment.

But the memo needs one major tightening before it should become an execution plan: align the declarative scope with real controls. Right now the cleanest repo-grounded round-7 pilot is not "all three relationship families in config." It is "the relationship surface, narrowed to the families that already have route-real control fixtures, executed by a tiny validated rule spec on top of the current hardcoded extractor and builders."

If the memo makes that revision, the rest of the plan becomes coherent. If it does not, round 7 risks proving only that a partly imagined registry can move constants into a file while leaving its hardest family outside the actual equivalence standard.
