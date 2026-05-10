# Memo: Stage 5 AOI Selection-Compose Contract Revision — Completion

Date: 2026-03-25
Status: Repair landed; diagnostic rerun required
Program: Dynamic Bespoke Apps Platformization
Supersedes: N/A (this is the repair completion, not the diagnostic rerun)
Depends on:
- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_diagnosis.md`

## Summary

The bounded analyzer repair for selection-backed transient compose contract alignment has landed. The fix stays inside `analyzer-v2` as scoped and does not reopen host snapshot durability, identity continuity, selector/provider behavior, AOI planning law, or the frozen Stage 5 pack.

## Root Cause

The `409 bounded_dynamic_composition_validation_failed` error was caused by `_transform_section_prose` running lossy LLM extraction on source-family-backed AOI sections whose `section.prose` was already structured JSON (serialized normalized artifact payloads from the composition source bridge).

The LLM extraction transformed the structured JSON into differently-keyed `structured_data`, losing the original keys (`themes`, `source_documents`, `selected_source_thinker` for thematic_synthesis; `findings_overview`, `severity_classification`, `target_provenance`, `source_provenance`, `discrepancy_and_consequence` for sin_findings). Contract enforcement then correctly flagged these as `section_renderer_missing_structured_data_key`.

## Fix Applied

### 1. Source-family preservation in `_transform_section_prose`

When `planner_row.source_family_key is not None` and the renderer is not `prose`, the transform now attempts to parse `section.prose` as JSON. If it parses to a dict, it is used directly as `structured_data` without running LLM extraction. The trace metadata records `extraction_source: "source_family_preserved"`.

Falls through to normal LLM extraction if the prose is not valid JSON, ensuring backward compatibility for non-source-family sections.

### 2. `_reconcile_renderer_config_with_data` safety net

After preserving the structured data, the generated `renderer_config.section_renderers` is reconciled against the actual data keys. Section_renderers entries that reference keys absent from `structured_data` are removed, and the `sections` list is pruned to match. This handles cases where the view generator creates section_renderers for keys the artifact doesn't have.

### Files Changed

- `src/presenter/compose_from_intent.py` — Added `_try_preserve_source_family_data`, `_reconcile_renderer_config_with_data`, and source-family shortcut in `_transform_section_prose`
- `tests/test_compose_from_intent.py` — 4 new regression tests

## Regression Coverage

| Test | Assertion |
|------|-----------|
| `test_source_family_preservation_skips_llm_extraction_for_accordion` | Thematic synthesis artifact parsed directly; extraction_source = source_family_preserved; all artifact keys present in structured_data |
| `test_source_family_preservation_reconciles_stale_section_renderers` | Section_renderers keys not in structured_data are removed; sections list pruned |
| `test_source_family_preservation_sin_findings_contract_valid` | Sin-findings preserved artifact produces zero `section_renderer_missing_structured_data_key` issues |
| `test_compose_from_selection_four_family_evolution_ready_contract_valid` | Full four-family compose-from-selection passes contract enforcement; thematic_synthesis and sin_findings both source_family_preserved; thematic_report passthrough; contract_validation issues = 0 |

All 27 `compose-from-intent` tests pass (23 existing + 4 new). Adjacent focused analyzer suites also pass: `tests/test_composition_source_bridge.py` (4) and `tests/test_served_renderer_contract_policy.py` (10).

A full repo `PYTHONPATH=. pytest -q` run in this workspace is not clean: `430 passed, 3 failed`. The failures appear outside this slice in `tests/test_manifest_trace.py` (missing proof jobs) and `tests/test_variant_generator.py` (`test_empty_existing_hints`).

## Preserved Constraints

- Planner-backed launch stays on `compose-from-selection` ✓
- Canonical `source_v2_job_id` stays preserved ✓
- `compose-from-source` remains excluded from the counted path ✓
- No legacy/debug fallback is allowed ✓
- Host warm snapshot durability not reopened ✓
- Selector/provider behavior not touched ✓
- AOI planning law/prompts not touched ✓
- Frozen Stage 5 pack not consumed ✓

## What Still Needs To Happen

Per the scope memo decision 6:

1. Rerun the same live `evolution_ready` diagnostic
2. Only if that succeeds end to end, rerun the same frozen four-case Stage 5 pack

If the diagnostic still fails on a new downstream seam, stop again and write a new revision memo.

## Status Implications

- Stage 5 remains `In progress` until the diagnostic rerun succeeds
- The frozen rerun is not yet earned
- Stage 2 remains open
- Tranche 3 remains blocked
