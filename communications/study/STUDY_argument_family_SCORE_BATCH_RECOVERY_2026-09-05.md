# Final independent-score syntax review

All 48 independent rating calls finished before this final adoption review. Collection produced 44 native scores, the previously adopted [single-brace recovery](STUDY_argument_family_SCORE_RECOVERY_2026-09-05.md), and three complete responses rejected by the strict JSON parser. No score was retried. Root read every response, all six reasons and the summary; the separate Sonnet and Sol readers also read their full responses. Numerical scores did not determine eligibility for repair.

The three pending cases contain complete judgments. The proposed changes insert only JSON punctuation at explicit offsets in the original UTF-8 bytes. They do not delete or replace bytes, change scores, add words, or infer missing reasoning. Corrected raw artifacts parse under the original strict eight-key score schema, including all six reasons. The original failed job records, raw responses, prompts, usage receipts, collection logs and pending queue are retained. These are historical parser failures even after an explicit derived score is accepted.

| Reading / rater | Exact insertions into original bytes | Raw SHA-256 | Corrected raw SHA-256 |
|---|---|---|---|
| DS original Castoriadis / Sol | `}` at byte 1888 | `a1333d1f5283041b17deb1b342e4eddabc8cdadba485a624346b586ae877e702` | `f3447a8f7b4c36b0c34bfb5c04bc496829a72e580f422f5fd3f878cf0b7e8fbc` |
| CF candidate Ganzinger / Sonnet | backslash at bytes 1055, 1076, 3312, 3322 | `4ebea8c863132426d401b0969f31c34065fa97ad1f54fe68ad4356afbf883ac0` | `48bb1de9a41a879458201e2b10e77d1c34a47c872ac1d052e511d2bdc9eaee46` |
| CF candidate Elling / Sonnet | `}` at byte 3236 | `67c4066c0f45ccb40bd5ea5a803100618db34df490a5f780bd1bfe1a30bcfb87` | `168889fec6b3654a71c980e022f840cb81c024412ac3ab5452aaa9f86de548c6` |

The Castoriadis and Elling insertions close the six-reason object before the top-level `one_line` member; Elling retains its original whitespace. Ganzinger escapes the existing quotation marks around “spinning in the void” and “otherwise.” Every other byte remains unchanged. The resulting score vectors in criterion order specificity, anchoring, non-obviousness, coherence, usefulness, hallucination risk are respectively `9/9/9/9/9/8`, `9/9/8/9/8/9`, and `8/9/7/8/7/9`.

The [batch adapter](../../scripts/study_argument_family_score_batch_recovery_2026_09_05.py) accepts an exact approval list with campaign, results, pending queue, code, corrected-artifact and review-file hashes. It requires all 24 generations and 48 one-call ratings, revalidates completed parents and every pending prompt/response/usage binding, and refuses any other failed record. Its only entry points are offline preview, explicit adoption and report. It uses the campaign lock, snapshots failures before publishing derived scores, and refuses to repeat an interrupted adoption. It cannot issue model calls. The original harness, prior recovery wrapper and collection adapters remain unchanged.

This review is a post-result handling amendment, following the [collection amendments](STUDY_argument_family_SCORING_COMPLETION_2026-09-05.md). It does not claim that native formatting succeeded. Final reporting separates 44 native and four syntax-derived scores and includes a sensitivity view excluding every affected comparison pair. The frozen source memos remain primary evidence.

Root reviewed the complete adapter and tests. **141 offline tests passed** in a fresh run: 44 batch cases plus 97 prior recovery/collection cases. Tests cover actual malformed responses, exact whitespace retention, invalid or ambiguous insertions, absent/extra score attempts, changed parents/prompts/receipts/reviews, post-adoption mutation, parser scoping, active locks, unplanned report keys and absence of a paid entry point. Adapter SHA-256 is `de01188636adc5f88d7a8fb63026bbfb78e3b9ce782d7aff1b2726eab0333a39`; test SHA-256 is `5a444e93cc19d77abe8acf3d9cd2efff73d30ec88a71b22c633a248f5e9ec7ca`. The actual-data preview additionally replays all completed records and validates the three pending cases before publication.

After adoption, validate the complete campaign with:

```bash
TMPDIR=/home/evgeny/projects/the-analyst-wt/study-tmp-2026-09-05 python scripts/study_argument_family_score_batch_recovery_2026_09_05.py --phase report --require-complete
```

The exact approval, immutable adoption manifest and all preserved inputs are under `data/study/argument_family_2026_09_05/530df62823ec1915/reader_notes/score_syntax_batch/`. The strict original harness does not silently accept these malformed responses; use the explicit adapter for the final derived-score report.
