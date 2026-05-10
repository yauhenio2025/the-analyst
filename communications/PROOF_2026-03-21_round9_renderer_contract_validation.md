# Round 9 Proof: AOI Serve-Time Renderer Contract Enforcement

Date: 2026-03-21

## Scope

Round 9 closes one bounded platform-law claim:

- the shared presenter surface can enforce renderer contracts at **serve time** for the AOI proof mode
- failures surface through the existing bounded-composition envelope:
  - page / manifest / result presentation / refresh / single-view -> `409`
  - trace -> `200` with `composition_issues`

This round does **not** introduce a new composition token.

The enforced proof mode is:

- `adaptive_aoi_theme_report_suite_v1`

The blocked secondary surface remains:

- `declarative_genealogy_relationship_conditions_suite_v1`

## What Was Enforced

Round 9 validates the **effective serve-time renderer contract** after composition resolution and consumer adaptation:

- final `renderer_type`
- final `renderer_config`
- final `structured_data` when the payload actually serves structured data

This enforcement lives at the shared manifest-builder seam plus one explicit composition-mode single-view seam.

It does **not** broaden normal-path consumer-capability enforcement.

It does **not** move validation into the preparation pipeline.

## Automated Verification

Backend focused regression:

- `PYTHONPATH=. pytest tests/test_declarative_adaptive_specs.py tests/test_manifest_trace.py tests/test_presentation_api.py tests/test_analysis_product_contract.py -q`
- result:
  - `200 passed, 12 warnings`

Dedicated renderer preflight command:

- `python scripts/check_renderer_contracts.py`
- result:
  - exit code `0`
  - repo-tracked renderer registry artifacts validated cleanly
  - schema health reported no invalid renderer schemas

Focused frontend regression:

- `CI=true npm test -- --watch=false src/lib/boundedV2Client.test.ts src/hooks/useBoundedV2Workspace.test.tsx src/pages/AnalysisWorkspacePage.test.tsx src/pages/AnalysisWorkspacePage.integration.test.tsx`
- result:
  - `4 suites passed`
  - `99 tests passed`

The frontend run still emits the existing non-blocking React `act(...)` warnings from `useBoundedV2Workspace`.

Python compile check:

- `python -m py_compile src/presenter/renderer_contract_enforcement.py src/presenter/manifest_builder.py src/presenter/presentation_api.py src/renderers/validator.py`

## AOI Proof Controls

Round 9 reused the existing round-6 AOI documentary controls directly:

- `proof-round5-adaptive-aoi-dossier-final-1774100000`
- `proof-round5-adaptive-aoi-comparison-final-1774100000`

Closure was executed against the local presenter surface using:

- `build_presentation_manifest(...)`
- `assemble_page(...)`
- `build_presentation_trace(...)`

This is sufficient for round 9 because the tranche is backend-only:

- no Critic code changed
- no new browser proof label was needed
- the route/trace HTTP contract is already covered by the focused route tests

Saved artifacts:

- `communications/PROOF_round9_dossier_final_trace_2026-03-21.json`
- `communications/PROOF_round9_comparison_final_trace_2026-03-21.json`
- `communications/PROOF_round9_renderer_contract_verification_2026-03-21.json`

### Dossier Control

- job:
  - `proof-round5-adaptive-aoi-dossier-final-1774100000`
- result:
  - `composition_status = applied`
  - `composition_issue_count = 0`
- selected families:
  - `aoi_by_theme -> aoi_theme_dossier`
  - `aoi_thematic_report -> aoi_report_briefing`
- round-6 parity:
  - selected families match saved round-6 proof
  - rationale strings match saved round-6 proof
  - normalized served manifest matches the saved round-6 final manifest when ignoring:
    - `presentation_hash`
    - `presentation_content_hash`
    - `prepared_at`
  - normalized served page payload is identical with enforcement on vs enforcement helper patched to no-op

### Comparison Control

- job:
  - `proof-round5-adaptive-aoi-comparison-final-1774100000`
- result:
  - `composition_status = applied`
  - `composition_issue_count = 0`
- selected families:
  - `aoi_by_theme -> aoi_theme_comparison_review`
  - `aoi_thematic_report -> aoi_report_evidence_review`
- round-6 parity:
  - selected families match saved round-6 proof
  - rationale strings match saved round-6 proof
  - normalized served manifest matches the saved round-6 final manifest when ignoring:
    - `presentation_hash`
    - `presentation_content_hash`
    - `prepared_at`
  - normalized served page payload is identical with enforcement on vs enforcement helper patched to no-op

## Genealogy Block

Round 9 explicitly did **not** lift the genealogy surface into strict serve-time enforcement.

That blocked state was rechecked against the existing round-8 proof jobs:

- `proof-round4-adaptive-balance-final-1774012011`
- `proof-round4-adaptive-matrix-final-1774012011`

Both still carry the same non-registry renderer types on the served page surface:

- `card`
- `constraining_conditions`
- `enabling_conditions`
- `mini_card_list`
- `move_repertoire`
- `prose_block`
- `timeline_strip`

This confirms the genealogy blocker is still architectural, not hypothetical:

- the current genealogy proof surface still mixes top-level renderer law with existing sub-renderer law
- round 9 correctly leaves that for a separate tranche instead of smuggling it into AOI enforcement

## Proof Conclusion

Round 9 is closed on its actual bounded claim.

What is now proved:

1. strict serve-time renderer contract enforcement can be added to the shared presenter path without inventing a new HTTP/error dialect
2. the AOI proof surface survives that enforcement cleanly on the existing control jobs
3. trace remains inspectable with the existing `composition_issues` fallback path
4. single-view now validates the requested composed subtree against the final served contract instead of bypassing the final manifest seam
5. genealogy remains honestly blocked and was not hand-waved into closure

What round 9 did **not** prove:

1. strict serve-time enforcement for genealogy
2. top-level renderer law for current supported sub-renderers
3. renderer-catalog cleanup across the whole repo
4. broadened consumer-capability enforcement outside bounded composition
5. item-driven surface enforcement beyond the AOI slice
