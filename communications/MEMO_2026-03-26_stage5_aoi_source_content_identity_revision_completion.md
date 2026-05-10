# Memo: Stage 5 AOI Source-Content Identity Revision Completion

Date: 2026-03-26
Status: Repair landed; recovered run traced; fresh post-fix execution-backed rerun required
Program: Dynamic Bespoke Apps Platformization
Supersedes: N/A (this is the repair completion, not the follow-on rerun)
Depends on:
- `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_scope.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_preflight_identity_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_requests_2026-03-26.json`
- `communications/PROOF_stage5_aoi_source_content_identity_trace_2026-03-26.json`

## Summary

The bounded analyzer-side AOI source-content identity repair is now landed.

What is now true:

- the confirmed contamination vector in `aoi_thematic_synthesis` has been removed from both the live capability definition and the capability-history snapshot
- the AOI contract now suppresses contradictory structured provenance instead of silently persisting it as valid
- the AOI contract now records explicit identity-integrity status for contaminated outputs instead of quietly masking the contradiction at the top level
- focused AOI contract / presentation / compose verification now passes

What is also now true:

- the recovered execution-backed run `job-6ee8b0621177` is still not honest enough for Stage 2 closure
- the recovered run is not `display-safe`, not `artifact-safe`, and not `closure-grade`
- the next honest step is a fresh post-fix execution-backed rerun on the same Otto Neurath documents, not another browser rerun and not another host-side repair pass

## What Landed

### 1. The thinker-specific contamination vector was removed

The AOI thematic-synthesis capability no longer embeds thinker-specific `selected_source_thinker` example content.

This landed in:

- `/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/aoi_thematic_synthesis.yaml`
- `/home/evgeny/projects/analyzer-v2/src/engines/capability_history/aoi_thematic_synthesis_snapshot.json`

This is a bounded repair:

- it fixes the confirmed AOI-specific prompt contamination vector
- it does not redesign the general capability composer or cross-workflow prompting substrate

### 2. AOI normalization now fails more honestly on source-identity contradiction

The AOI contract now treats selected-source identity contamination as an explicit integrity condition rather than silently papering it over.

Landed behavior:

- contradictory top-level `selected_source_thinker` is no longer allowed to pass through as if valid
- off-corpus theme/source provenance is suppressed instead of being normalized into misleading persisted truth
- off-corpus representative-quote provenance is suppressed instead of silently remaining valid-looking
- downstream AOI report normalization now records residual contradictory identity rather than pretending closure-grade cleanliness

This landed in:

- `/home/evgeny/projects/analyzer-v2/src/aoi/contract.py`

### 3. The recovered run is now traced honestly across the whole identity chain

The saved trace artifact shows the real seam shape for `job-6ee8b0621177`:

- plan truth stays fixed on `otto_neurath`
- raw Phase `1.0` output is the first real contradiction layer
- the raw Phase `1.0` contradiction is not singular:
  - `john_oneill` appears in `21` raw thematic-synthesis outputs
  - `aaron_benanav` appears in `3` raw thematic-synthesis outputs
- structured AOI artifacts partially mask the contradiction at the top level but still carry polluted downstream evidence
- downstream engagement/report prose still inherits O'Neill-centered language
- the composed presentation still exposes that contradiction in Phase `1.0` preview and report summary

That trace is saved in:

- `communications/PROOF_stage5_aoi_source_content_identity_trace_2026-03-26.json`

## What The Trace Proved

### 1. The first real contradiction is raw Phase `1.0`, not the browser shell

The recovered run's plan-selected source thinker is Otto Neurath.

But raw Phase `1.0` AOI thematic synthesis already contradicts that truth:

- `phase_results["1.0"].final_output_preview` names `john_oneill`
- raw `aoi_thematic_synthesis` outputs for the same job also contain `aaron_benanav`

So the browser was not inventing the seam. It was showing a contradiction that already existed upstream.

### 2. Structured provenance is improved by the repair, but the recovered stored run is still not clean

Current code, when re-run over the saved thematic-synthesis source output, now does the right bounded thing:

- `identity_integrity.status = explicit_identity_contradiction_suppressed`
- top-level selected thinker resolves to Otto Neurath
- first-theme source-document refs are suppressed
- first-theme representative quotes are suppressed

So the repair is real for future normalization behavior.

However, the already stored recovered run is still not artifact-safe:

- the saved source-thematic artifact still carries `8` representative quotes with `source_document_id = unknown`
- the recovered report/engagement path still carries contradictory O'Neill-centered prose

### 3. Downstream prose contamination still survives and blocks closure-grade use

Current code, when re-run over the stored Phase `4.0` thematic-report output, now records the contradiction honestly:

- `identity_integrity.status = explicit_identity_contradiction_detected`
- contamination source is `upstream_thematic_synthesis`
- observed contradictory thinker set includes both `john_oneill` and `aaron_benanav`
- `residual_fields` includes `report_sections.summary`

That is the right integrity read.

But it also proves the recovered run is still not closure-grade:

- the engagement map still says Benanav acts as the institutional engineer to O'Neill's philosophical architect
- the report summary still frames Benanav as operationalizing John O'Neill's reconstruction of Otto Neurath
- the saved-result / presentation path still exposes `john_oneill` in Phase `1.0` preview and O'Neill-centered report summary prose

## Regression Coverage

Focused regression coverage now proves the repaired seam that was actually scoped.

At minimum, the coverage now proves:

- the AOI thematic-synthesis live definition no longer embeds thinker-specific selected-source identity
- the capability-history snapshot no longer embeds thinker-specific selected-source identity
- contradictory raw selected-source identity cannot survive into AOI normalization silently
- report-path identity contradiction is flagged rather than silently normalized away
- compose/presentation seams continue to verify under the tightened AOI contract

Files changed:

- `/home/evgeny/projects/analyzer-v2/tests/test_aoi_contract.py`

## Verification

Run result:

- `PYTHONPATH=. pytest -q /home/evgeny/projects/analyzer-v2/tests/test_aoi_contract.py /home/evgeny/projects/analyzer-v2/tests/test_registered_corpus_launch.py /home/evgeny/projects/analyzer-v2/tests/test_presentation_api.py /home/evgeny/projects/analyzer-v2/tests/test_compose_from_intent.py`
  - `111 passed`

Residual warnings are unchanged:

- existing Pydantic deprecation warnings
- existing datetime deprecation warnings

## Status Implications

- the Stage 5 structural host/browser seam remains closed
- the bounded analyzer-side source-content identity repair is now landed
- the recovered run `job-6ee8b0621177` still is not `display-safe`
- the recovered run still is not `artifact-safe`
- the recovered run still is not `closure-grade`
- Stage 2 remains open
- Tranche 3 remains blocked

## Next Honest Step

The next step is not another browser rerun and not another host-side repair.

The next step is one fresh post-fix `execution_backed` AOI rerun on the same Otto Neurath documents.

That rerun should answer the only question that still matters for Stage 2:

- after the contamination vector removal and AOI contract tightening, does a fresh execution-backed AOI run stay source-content-clean enough to support honest closure-grade `selection_fit` / `rendered_usefulness`?

If that fresh rerun is clean, the Stage 2 decision can be written honestly.
If it is not, stop again and write a new bounded revision memo rather than widening into cross-workflow redesign.
