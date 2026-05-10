# Memo: Round 9 / Renderer Contract Validation Completion

Date: 2026-03-21
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-21_round9_renderer_contract_validation_scope.md`
Proof Note: `communications/PROOF_2026-03-21_round9_renderer_contract_validation.md`

## Purpose

Record the actual outcome of round 9.

This note closes the gap between:

- the round-9 scope memo
- the implemented backend enforcement boundary
- the saved AOI proof evidence
- the explicit genealogy block that remained out of scope

## Bounded Claim Closed In Round 9

Round 9 proved one bounded thing:

- renderer contracts can become a **serve-time fail-closed presenter boundary** on a real shared proof route without adding a new composition token, without changing the Critic host, and without breaking the existing bounded-composition trace/error dialect

The enforced proof mode is:

- `adaptive_aoi_theme_report_suite_v1`

The blocked surface remained:

- `declarative_genealogy_relationship_conditions_suite_v1`

## What Landed

### Shared Enforcement Boundary

Round 9 added a dedicated presenter-side serve-time enforcement helper:

- `src/presenter/renderer_contract_enforcement.py`

That helper:

- only runs on the allowlisted AOI proof mode
- validates final served `renderer_config`
- validates final served `structured_data` when the payload actually serves structured data
- treats missing renderer definitions/contracts as hard failures on the enforced slice
- raises `BoundedCompositionValidationError` populated with `CompositionIssue`s

Failure reasons are now explicit:

- `renderer_definition_missing`
- `renderer_config_validation_failed`
- `renderer_data_validation_failed`

### Integration Seams

Round 9 wired the enforcement boundary into the actual serve path instead of the older warn-only observational hooks.

The shared multi-view enforcement seam is now:

- `src/presenter/manifest_builder.py::build_effective_manifest()`

This means:

- manifest
- page
- result presentation
- refresh
- trace fallback

all hit the same final served contract boundary after consumer adaptation.

Round 9 also closed the single-view seam explicitly:

- `src/presenter/presentation_api.py::assemble_single_view()`

In composition mode, single-view now:

- collects the requested payload subtree
- runs that subtree through the effective manifest seam
- returns the adapted payload only after the final served contract has been checked

That prevents composition-mode single-view from bypassing the new enforcement layer.

### Preflight / CI Validation

Round 9 did **not** make the runtime renderer registry crash on bad JSON.

It kept request-time loading tolerant in:

- `src/renderers/registry.py`

But it added a fail-loud preflight helper in:

- `src/renderers/validator.py::validate_renderer_registry_artifacts()`

That gives CI a real way to fail hard on broken repo-tracked renderer artifacts while leaving request-time registry loading tolerant.

Round 9 follow-up also added a dedicated executable check command:

- `python scripts/check_renderer_contracts.py`

That command now serves as the stable preflight entrypoint rather than leaving renderer-contract preflight as a test-only helper.

### Scope Discipline

Round 9 stayed bounded.

It did **not**:

- add a new proof token
- broaden normal-path consumer-capability enforcement
- lift genealogy sub-renderers into top-level renderer law
- turn into a renderer-catalog cleanup tranche
- add Critic-side workflow logic

## Important Mid-Implementation Correction

Round 9 found one real serve-time seam during closure:

- pure container hosts such as `aoi_thematic_analysis` can serve children without serving their own `structured_data`

The first enforcement pass incorrectly validated `structured_data=None` against the container renderer schema and caused the live AOI proof jobs to fail.

The implementation was corrected to validate served structured data only when the payload actually claims structured data:

- `payload.structured_data is not None`, or
- `payload.has_structured_data`

This keeps the boundary honest:

- leaf/data-serving views are enforced
- pure container/navigation hosts are not falsely treated as malformed data payloads

That correction is now covered by tests and by the successful AOI proof closure.

## Verification

Backend focused regression:

- `PYTHONPATH=. pytest tests/test_declarative_adaptive_specs.py tests/test_manifest_trace.py tests/test_presentation_api.py tests/test_analysis_product_contract.py -q`
- result:
  - `200 passed, 12 warnings`

Focused frontend regression:

- `CI=true npm test -- --watch=false src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx`
- result:
  - `4 suites passed`
  - `99 tests passed`

Python compile check:

- `python -m py_compile src/presenter/renderer_contract_enforcement.py src/presenter/manifest_builder.py src/presenter/presentation_api.py src/renderers/validator.py`

Renderer preflight check:

- `python scripts/check_renderer_contracts.py`
- result:
  - exit code `0`
  - no broken repo-tracked renderer definitions
  - no invalid registered renderer schemas

Remaining noise is unchanged:

- existing backend deprecation warnings
- existing frontend React `act(...)` warnings

## AOI Proof Outcome

Round 9 reused the existing round-6 AOI documentary controls:

- `proof-round5-adaptive-aoi-dossier-final-1774100000`
- `proof-round5-adaptive-aoi-comparison-final-1774100000`

Observed outcome on both:

- `composition_status = applied`
- `composition_issue_count = 0`
- selected families matched the saved round-6 proof
- rationale strings matched the saved round-6 proof
- normalized served manifests matched the saved round-6 final manifests when ignoring:
  - `presentation_hash`
  - `presentation_content_hash`
  - `prepared_at`
- normalized served page payloads were identical with enforcement on vs enforcement helper patched to no-op

Saved artifacts:

- `communications/PROOF_round9_dossier_final_trace_2026-03-21.json`
- `communications/PROOF_round9_comparison_final_trace_2026-03-21.json`
- `communications/PROOF_round9_renderer_contract_verification_2026-03-21.json`

## Genealogy Outcome

Genealogy remained intentionally blocked in round 9.

That blocked state was rechecked against the existing round-8 proof jobs and still shows the same missing renderer keys on the served page surface:

- `card`
- `constraining_conditions`
- `enabling_conditions`
- `mini_card_list`
- `move_repertoire`
- `prose_block`
- `timeline_strip`

This confirms the scope decision was correct:

- round 9 should close AOI serve-time enforcement
- genealogy needs a separate architectural decision about lifting current sub-renderer law into top-level renderer law

## What Round 9 Now Proves

Round 9 now proves:

1. the presenter can enforce final served renderer contracts at a shared backend boundary instead of only logging warn-only validation failures
2. the existing bounded-composition error envelope is sufficient for renderer-contract failures
3. trace remains inspectable at `200` with `composition_issues`
4. AOI survives strict serve-time renderer validation on the real control jobs
5. AOI served outputs remain payload-equivalent before vs after enforcement on the documented control jobs
6. single-view no longer bypasses the final served contract boundary in composition mode

## What Round 9 Did Not Prove

Round 9 did not prove:

1. strict serve-time genealogy enforcement
2. full renderer-catalog cleanliness
3. top-level law for current supported sub-renderers
4. global strict renderer enforcement across every route and workflow
5. item-driven surface enforcement outside the allowlisted AOI slice

The `items` boundary is intentionally deferred.

Round 9 enforcement validates served `structured_data` on the AOI proof slice because that is the contract exercised by the allowlisted mode. If strict serve-time enforcement expands to item-driven surfaces later, item-level contract law should be handled in that widening tranche instead of being smuggled into round 9.

## Program Position After Round 9

The proof ladder is now paying off at the platform boundary rather than only inside new composition variants.

That means the next serious move should stay on the platform path:

- consumer consolidation
- stronger renderer/sub-renderer law
- or the next bounded compose-from-intent platform seam

It should **not** revert to adding another proof token as the primary round objective.
