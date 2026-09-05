# Post-study citation and empty-ledger corrections

The [argument-family study](STUDY_argument_family_RESULTS_2026-09-05.md) completed and passed its required-complete report before these changes were applied. Runtime `af5861a`, its model prompts, every archived response and all ratings retain their historical behavior. The candidate YAMLs remain unchanged and unregistered.

## Checked prose citations

Counterfactual/Harris kept prose references to F4/F5/F7/F11 after the critic rejected those findings. The frozen oneshot wall reported `missing_cited: []` because that path never ran the prose citation check. An empty list could therefore be mistaken for successful verification.

[WallReport](../../src/executor/ledger_walls.py) now explicitly distinguishes `not_checked` from `checked`. Checked oneshot assembly reuses the existing bracketed-ID membership check against retained findings, distinguishing absent rejected IDs from other absent IDs. The receipt lists unresolved references when present. It does not rewrite the original prose or treat an addition's lineage as an alias for a rejected ID. Scope diagnostics also distinguish an empty declared-reference list from loss of one or more declared references; the conservative any-loss policy is unchanged.

Deep synthesis retains its existing allowance for final and earlier ledger IDs, including earlier rejected rows, and records that broader scope explicitly. The check examines preceding prose only. It does not certify quotation accuracy, interpretation, or IDs embedded in every other response field.

The saved Harris two-call replay preserves exact prompts, routes, labels and raw responses and now reports the four missing rejected IDs. Its derived output changes only the visible citation receipt and clarified scope wording. This is a diagnostic correction, not a new model reading.

## Exact empty-ledger marker

The Dialectical mixed-control critic returned `## Ledger` followed by the literal `(empty)` and five valid inventory scope reviews. The scope parser treated that exact marker as non-row material, making all five reviewed negatives inconclusive even though the reader and critic correctly found no organizing opposition in the inventory.

[The scope handoff](../../src/executor/process_runner.py) now accepts that exact trimmed literal as an empty ledger body. Arbitrary prose, other marker spellings, malformed scope records, missing source access and failed invocations remain subject to the existing checks. The marker itself establishes neither absence nor a completed review.

The saved 22-call mixed-control replay checks the original baseline exactly. With only the marker correction applied, the 21 pre-synthesis prompts/routes/labels remain identical; the synthesis input changes only the five inventory scope outcomes from inconclusive to supported negative. Its source text, findings ledger and system prompt remain unchanged. No new synthesis was requested, and the old final response was not reused as a response to that changed prompt. This validates the handoff correction, not how a model will respond to it.

## Verification and evidence

**294 tests passed** on the current main tree after applying both patches, including 68 unchanged production prompt hashes, the saved Harris regression, desk/corpus dispatch, quote/ruling/scope behavior, and the concurrent dossier boot-recovery/SIGTERM-drain changes. The separate 22-call mixed-control replay also passed; it is recorded in its own evidence bundle rather than counted in those 294 tests. The separate study recovery/collection suite passed **141 tests**. Tests used no provider calls. The runtime suite emitted 131 warnings and no failures.

Prepared patch hashes are `7bd7896e3fb0f500928a5f0da8c7a81c07dac4ec89b1a7cef47db239ce3ae7d8` (citation/scope diagnostics) and `d2cdbc8dd32e2408b4e4948781e5dd1fb0a6a3a431d02725e7933f93f5986b29` (exact marker). The evidence bundles are [citation replay](../../data/study/quote_scope_diagnostics_2026_09_05/manifest.json), [empty-marker replay](../../data/study/scope_empty_marker_2026_09_05/replay_manifest.json), and [fresh main test log](../../data/study/argument_family_preparation_2026_09_05/post_trial_runtime_tests.log). These local ignored artifacts retain the reviewed patches and replay details independently of a temporary worktree.

The remaining [consolidation plan](MAINTENANCE_quote_scope_CONSOLIDATION_2026-09-05.md) targets shared pure mechanics, section boundaries and lineage handling. These two corrections add no fuzzy quote matching, silent ID remapping or semantic absence certification. Engine corrections and any live application corpus exposure still require fresh validation.
