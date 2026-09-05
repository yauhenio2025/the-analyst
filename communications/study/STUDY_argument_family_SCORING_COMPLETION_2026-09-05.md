# Completing independent ratings while preserving syntax failures

After the [first explicit offline recovery](STUDY_argument_family_SCORE_RECOVERY_2026-09-05.md), collection stopped on a second Sol JSON response with the same omitted closing brace before `one_line`. At that point 18 rating calls existed: 16 natively valid scores, one adopted syntax recovery, and one newly failed parse. All 24 generation products remained unchanged. Total saved-response cost was USD 4.248038 across 144 logical calls.

The second response is **Sol / original Dialectical Structure / Castoriadis**, attempt `916e19e78a5c`. Its raw SHA-256 is `a1333d1f5283041b17deb1b342e4eddabc8cdadba485a624346b586ae877e702`. Inserting one `}` at zero-based UTF-8 byte offset **1888** yields `f3447a8f7b4c36b0c34bfb5c04bc496829a72e580f422f5fd3f878cf0b7e8fbc`. Root read the full raw reasons; an independent reviewer confirmed that only this insertion gives the complete frozen schema. The six values remain 9, 9, 9, 9, 9, 8, and all reason text remains unchanged. Its complete call receipt records USD 0.109606, the requested Sol model, 52,308 input tokens, 499 output tokens and zero retries. This syntax review alone does not publish a valid score.

## Collection rule, recorded before remaining calls

The ratings are independent: every job depends only on its generated reading and source, with no other rating as input. Root therefore separates collection from acceptance of a format repair. The separate collection wrapper may defer a failed judge parse only when all of the following hold:

- The original job is preserved as failed, with one complete saved invocation and its exact raw response, error and parent/source/prompt/model/usage bindings.
- The failure is a JSON decoding error. The unique insertion of one closing brace immediately before the single `,"one_line":` delimiter yields the exact original eight-key object, six valid scores and six nonempty reasons.
- No score, reason or summary content is supplied or changed. Missing content, other schema failures, partial/error responses and unknown cost remain fatal.
- An immutable pending entry binds the failed job, original and proposed corrected hashes, insertion offset and collection code. No derived score is accepted or marked complete.

The wrapper then continues the remaining original independent jobs through the unchanged execution, budget, campaign lock and source-review gate. It does not retry the failed call, change its prompt or open another spend window. Resuming collection checks the preserved failed entry before skipping it. The first recovery and its original wrapper remain unchanged.

After all 48 rating calls have been collected, root must review every pending raw response and bind an exact acceptance list before any batch adoption. That later offline step must preserve the failed state and all invocation bytes, validate previous native and recovered products, and report native versus recovered scores separately. The required-complete report must use the explicit recovery adapter; an unmodified strict-parser report cannot certify malformed raw strings. Exclusion of recovered pairs will be reported as a sensitivity check.

This is a recorded amendment to the study's collection procedure, made after two observed serialization failures. The fixed matrix, independent rubric, source memos, prompts, model routes, generation runtime and USD 16 authorization remain unchanged. The rule does not use the score values or preferred treatment to decide which failures to defer. These tools are study utilities; no application parser behavior changes here.

## Collection implementation checks

The [collector](../../scripts/study_argument_family_collect_scores_2026_09_05.py), SHA-256 `2e4a345e5a4e33e1e32d474382dcf70d39fc3f012cef11a6356afe9626560970`, leaves the first recovery wrapper and original harness unchanged. Root reviewed its full code and tests and required a check of every existing pending entry at the original source-review gate, before the next paid call. Unknown keys, changed failed records or snapshots, and inconsistent response bindings stop continuation.

**75 offline tests passed**: 35 collector cases and the 40 unchanged first-recovery cases. These cover the exact second raw response, preservation of failed state and raw bytes, no repeated calls, continued independent success, incomplete/fallback/unknown-response refusal, the original budget and source-review barriers, and tampered pending records stopping before another call. The test file SHA-256 is `f9c320c709050bcc84ba97522ae8f6f547a1297dd2d905ea4cf6872559891063`.

The actual offline preflight reproduces 24 generation products and 17 valid scores, with the second failure still unaccepted. Root separately validates that failure's complete call and proposed syntax correction through the same collector helper, without writing a pending entry or derived score. The [deferral review](../../data/study/argument_family_2026_09_05/530df62823ec1915/reader_notes/score_recovery/root_second_deferral_review.json) binds the exact response and collector. Collection may now continue under the original USD 16 authorization; final acceptance of pending scores remains a separate offline review.

```bash
python scripts/study_argument_family_collect_scores_2026_09_05.py --run --phase judge --budget-usd 16 --review-record /absolute/path/to/reader_notes/pre_score/judge_review.json
```

## Manual-review queue after a second syntax form

At 27 rating calls, a Sonnet response for candidate Counterfactual/Ganzinger contains unescaped ASCII quotation marks inside two reason strings. The one-brace rule correctly stops rather than changing or accepting it. Its raw SHA-256 is `4ebea8c863132426d401b0969f31c34065fa97ad1f54fe68ad4356afbf883ac0`. Root and an independent reviewer confirm that four inserted backslashes at original byte offsets 1055, 1076, 3312 and 3322 produce `48bb1de9a41a879458201e2b10e77d1c34a47c872ac1d052e511d2bdc9eaee46`, preserving every other byte and all scores/reason wording. The six values remain 9, 9, 8, 9, 8, 9. This is still only a reviewed proposal, pending final adoption.

Root now broadens **collection deferral, not score acceptance**, to any native `JSONDecodeError` following the same complete, fully bound call. The [manual collection adapter](../../scripts/study_argument_family_collect_manual_scores_2026_09_05.py) preserves old one-brace entries exactly and gives other syntax failures a manual-review entry with no proposed corrected hash or insertion offset. It does not interpret missing or malformed judgment content as valid. A complete call receipt is distinct from a complete judgment; any missing judgment content remains unresolved and cannot enter the final score matrix without a valid separately reviewed result. Explicit partial/backend errors, unknown usage/cost, and non-JSON schema failures still stop collection.

This amendment allows the remaining independent ratings to be collected while failed parses await review. The exact same matrix, prompts, budget and source gate remain in force; no failed call is retried. The manual adapter SHA-256 is `b6ae90a9bb203e7980ecd55ad49c1eefbfd5e3a1d55bcb709b545c46c2ea3078`. **97 offline tests passed** (22 new manual-queue cases plus the previous 75), and actual-data preflight preserves 24 generations, 25 accepted scores and both current failed parses. Root's [manual-queue acceptance record](../../data/study/argument_family_2026_09_05/530df62823ec1915/reader_notes/score_recovery/root_manual_collection_review.json) verifies the old pending entry and the new complete Sonnet call without correction or publication. Independent review found no further defect.

```bash
python scripts/study_argument_family_collect_manual_scores_2026_09_05.py --run --phase judge --budget-usd 16 --review-record /absolute/path/to/reader_notes/pre_score/judge_review.json
```

## Completed collection and offline adoption

All 48 planned score calls completed under the original approval. Collection ended with 44 native scores, the first adopted recovery and three failed parses, with no unqueued failure. The [final syntax review](STUDY_argument_family_SCORE_BATCH_RECOVERY_2026-09-05.md) binds each complete pending response and its exact insertion list. The final missing-brace case is Sonnet / candidate Counterfactual / Elling, with whitespace before `one_line`; its original raw bytes remain unchanged.

Root's exact approval was created only after all 48 response contents had been read. The offline preview passed and explicit adoption published the three derived scores without a paid call. Batch manifest SHA-256 is `a5c067e804b5586b6ee657aab2022ced6557ae69a7fda9e3c89853bbc0bd89eb`; the prior first-recovery manifest remains unchanged. The final required-complete report validates **24 generations and 48 scores, zero errors**, separating **44 native and four syntax-derived scores**. Report SHA-256 is `ff0875ceae47a6953bf35e4f6856920f1bcc8795212211c928c71f4bee900fc5`.

Total saved-response cost is **USD 6.173507 for 174 logical calls**. Scores account for USD 3.025237. The earlier generation retry's empty attempt has unknown usage/charge, so these receipt totals are not a provider invoice. There were no paid score retries. The [results](STUDY_argument_family_RESULTS_2026-09-05.md) include source findings and a sensitivity view excluding all four affected pairs.

The collection commands above are historical. To verify the completed derived-score campaign, use only the explicit final offline adapter:

```bash
TMPDIR=/home/evgeny/projects/the-analyst-wt/study-tmp-2026-09-05 python scripts/study_argument_family_score_batch_recovery_2026_09_05.py --phase report --require-complete
```

The original harness and all adopted recovery/collection code are hash-pinned evidence. Do not edit them or rerun the collection/adoption commands for this completed campaign.
