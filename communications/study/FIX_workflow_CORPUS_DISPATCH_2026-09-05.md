# Corpus dispatch through the application

Implemented after the ideas study and Fable's review. The application now passes selected raw documents to process engines as an explicit keyed map, so a real collection reaches corpus extraction. The legacy combined text remains available to stance engines. This closes the dispatch defect identified in the [ideas synthesis](STUDY_ideas_SYNTHESIS_2026-09-05.md); it is offline application-path validation, not a new paid corpus study or an observed production deployment.

## Source identity and scope

The dossier stores `corpus:<original document key>` bindings alongside its legacy flattened target. Those bindings survive executor job serialization, normalization and resume; the process sees the original keys used by the dossier's desks. Existing stored source documents are reused. Historical jobs without those bindings retain their previous single-source input; headers are not parsed to invent document boundaries.

Phase dispatch preserves the existing source selection:

- AOI phase 1 receives only the selected thinker's sources; phase 3 receives the target plus those sources. Other standard phases receive the target, expanded into original dossier documents where bindings exist.
- Independent per-work profiling receives only the prior work. An explicit empty dependency list overrides template dependencies. A comparison using distilled target analysis receives the prior raw text as its source and the target analysis as context. A raw comparison receives both texts.
- Chapter execution receives only the selected chapter text. Whole-book summaries and previous engine output remain context and cannot supply source anchors.
- Supplementary chains receive the same selected source map as the primary chain.

Stored document identities distinguish titles that collapse to the same sanitized spelling; aliases for the same stored document are deduplicated. A missing or empty explicitly selected source fails before a process model call and names the missing key. It cannot silently reduce the collection.

## Final output ownership

Pass numbers restart for each engine. Dossier collection therefore orders a phase's outputs by their complete creation timestamps, then keeps the final text, engine identity and wall metadata together. This matters for corpus ancestry: Conditions' `P6` and Commitment's `X6` require the appropriate engine's checks. Historical phases with incomplete timestamps keep their previous ordering rather than receiving an invented chronology.

## Validation and limits

Two fresh offline pytest runs cover **189 distinct tests**: 171 passed across the new dispatch regressions, process shape, corpus ledger, anchor repairs and adaptive target normalization; an independent run passed 46 across dispatch, AOI contract/canary and the four-engine shape test, with the 28 dispatch cases overlapping. No provider calls were allowed. The new cases exercise both single-engine and chain dispatch through real process code at surface, standard and deep depths, two-source walls, persisted metadata, dossier resume, source selection, chapter isolation, missing sources and final-engine desk ancestry. `git diff --check` is clean. Existing deprecation warnings remain.

Four tests in `test_phase3_prompt_budget.py` already fail on clean `d9cfc6e`: three expect phase 3 to exclude the raw source corpus, contrary to its current implementation, and one imports missing `_estimate_pass_budget`. The separate auto-presentation suite also has a pre-existing missing-helper import error. These were not rewritten to make this patch pass.

Two existing issues remain outside this fix: per-work **result** keys still use sanitized titles, and the global `get_latest_output_for_phase` helper still orders by pass number. The new raw-source map does not share the first collision, and dossier collection no longer uses the latter ordering to choose its final engine. Neither limitation is certified resolved by these tests.
