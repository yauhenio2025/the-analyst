# Ideas study: final baseline results, 2026-09-05

The baseline finished with **52/52 valid jobs: 28 generation outputs and 24 Sonnet judgments**. Across twelve single-paper pairs, six favor the checked production reading in both orders and six split; none agree on the old reading or a tie. Estimated original invocation cost is **$6.735188 across 175 calls**. These baseline totals include the recovery-dependent judgments and preserve the two original postprocessing failures.

All six excluded splits select **A in both orders**: old when presented first, checked when presented first. Across individual decisions, A wins 18/24 and B wins 6/24. This observed order sensitivity supplies no agreed winner for those six pairs. It does not by itself identify the cause of the variation. Conditions, Argument and Epistemology each have two checked agreements and one split; Commitment has three splits.

This is a whole-treatment comparison: original questions and one Sol reading versus redesigned questions, method cards, a synthesis brief, one Sol reading and a DeepSeek check. A/B order counterbalancing does not hide visible ledgers, check receipts, formatting or length. The judgments therefore do not isolate question quality or the critic's contribution, and they do not replace the independent source assessments in the four reading memos.

Two checked parents—Argument/Chen and Epistemology/Harris—were adopted from saved complete read/critic responses after the frozen parser mistook requested `Must keep` references for duplicate rulings. The accepted recovery changes only that auxiliary-section boundary; original attempts, prompts, responses and failure history remain preserved. It makes no new model calls and applies none of the broader proposed anchor or rewrite repairs. See the [recovery manifest](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/auxiliary_recovery/20260905T045321.120955Z/manifest.json) and [adoption manifest](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/auxiliary_recovery/adoptions/20260905T064226.572337Z/manifest.json). Their judgments are included and their costs counted once.

The committed [aggregation script](../../scripts/summarize_ideas_study_2026_09_05.py) passed `--require-complete` for both the [validated Markdown](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/final_aggregate_2026_09_05.md) and [full JSON](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/final_aggregate_2026_09_05.json), with a shared [manifest](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/final_aggregate_2026_09_05.manifest.json). The [independent mapping audit](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/judge_mapping_audit/20260905T064408.523174Z/audit.json) validates all actual source/A/B prompts, raw letter verdicts and mapped outcomes against the [plan](../../data/study/ideas_2026_09_05/374325c24e6b10a1/plan.json) and [results](../../data/study/ideas_2026_09_05/374325c24e6b10a1/results.json). In the pair table, decision links open the mapped verdict; adjacent raw links open the original Sonnet response.

Identity: `374325c24e6b10a15663e9cbe9fd3520818964bc05f8f46b2d88944e0b7cbfca`. Snapshot: `017fe532055d03e725734e321b62b56e68c5321591c3283b1899d16606f218a6`.
Aggregator: `8425d127d6f7b72774aadd7a4cd8528ff0d328df30aff6b4eb642509da846a53`.

Valid outputs: 28/28 generations; 24/24 judgments. Recovered parents: 2.

## Both-order agreements

| Engine | Old | Checked | Tie | Split, excluded | Incomplete |
|---|---:|---:|---:|---:|---:|
| conditions_of_possibility_analyzer | 0 | 2 | 0 | 1 | 0 |
| argument_architecture | 0 | 2 | 0 | 1 | 0 |
| inferential_commitment_mapper | 0 | 0 | 0 | 3 | 0 |
| epistemological_method_detector | 0 | 2 | 0 | 1 | 0 |

| Engine / paper | Old first | Checked first | Result | Recovered parent |
|---|---|---|---|---|
| conditions_of_possibility_analyzer / harris | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__conditions_of_possibility_analyzer__harris__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__conditions_of_possibility_analyzer__harris__old_first/b06fd68958df/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__conditions_of_possibility_analyzer__harris__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__conditions_of_possibility_analyzer__harris__checked_first/e8e9ef069bec/call-0001.md)) | checked | no |
| conditions_of_possibility_analyzer / zambrana | [old](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__conditions_of_possibility_analyzer__zambrana__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__conditions_of_possibility_analyzer__zambrana__old_first/302d35a6f6eb/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__conditions_of_possibility_analyzer__zambrana__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__conditions_of_possibility_analyzer__zambrana__checked_first/207512d9ddc1/call-0001.md)) | split | no |
| conditions_of_possibility_analyzer / chen | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__conditions_of_possibility_analyzer__chen__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__conditions_of_possibility_analyzer__chen__old_first/c933d889e7bc/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__conditions_of_possibility_analyzer__chen__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__conditions_of_possibility_analyzer__chen__checked_first/6d435e7cea33/call-0001.md)) | checked | no |
| argument_architecture / harris | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__argument_architecture__harris__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__argument_architecture__harris__old_first/0e9eee32c4c7/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__argument_architecture__harris__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__argument_architecture__harris__checked_first/65210c7089a2/call-0001.md)) | checked | no |
| argument_architecture / zambrana | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__argument_architecture__zambrana__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__argument_architecture__zambrana__old_first/695ae3d5aa27/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__argument_architecture__zambrana__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__argument_architecture__zambrana__checked_first/b194cc0a688e/call-0001.md)) | checked | no |
| argument_architecture / chen | [old](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__argument_architecture__chen__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__argument_architecture__chen__old_first/3a0b8c85b1c6/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__argument_architecture__chen__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__argument_architecture__chen__checked_first/0f18a150092f/call-0001.md)) | split | yes |
| inferential_commitment_mapper / harris | [old](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__inferential_commitment_mapper__harris__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__inferential_commitment_mapper__harris__old_first/5fe99ef04456/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__inferential_commitment_mapper__harris__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__inferential_commitment_mapper__harris__checked_first/ef4d747cbc99/call-0001.md)) | split | no |
| inferential_commitment_mapper / zambrana | [old](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__inferential_commitment_mapper__zambrana__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__inferential_commitment_mapper__zambrana__old_first/6f76fa974296/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__inferential_commitment_mapper__zambrana__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__inferential_commitment_mapper__zambrana__checked_first/5ee7189aecc0/call-0001.md)) | split | no |
| inferential_commitment_mapper / chen | [old](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__inferential_commitment_mapper__chen__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__inferential_commitment_mapper__chen__old_first/4ac598cfb0d2/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__inferential_commitment_mapper__chen__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__inferential_commitment_mapper__chen__checked_first/265ec636883b/call-0001.md)) | split | no |
| epistemological_method_detector / harris | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__epistemological_method_detector__harris__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__epistemological_method_detector__harris__old_first/2b695ee4cbda/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__epistemological_method_detector__harris__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__epistemological_method_detector__harris__checked_first/5456da881b0f/call-0001.md)) | checked | yes |
| epistemological_method_detector / zambrana | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__epistemological_method_detector__zambrana__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__epistemological_method_detector__zambrana__old_first/4dc898807175/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__epistemological_method_detector__zambrana__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__epistemological_method_detector__zambrana__checked_first/d678f8985456/call-0001.md)) | checked | no |
| epistemological_method_detector / chen | [old](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__epistemological_method_detector__chen__old_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__epistemological_method_detector__chen__old_first/16e932fcbaec/call-0001.md)) | [checked](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/judge__epistemological_method_detector__chen__checked_first.md) ([raw](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/judge__epistemological_method_detector__chen__checked_first/02065ecc6a80/call-0001.md)) | split | no |

## Invocation usage and timing

| Role | Calls | Estimated USD | Input tokens | Output tokens | Invocation seconds | Unknown cost | Retry calls / count | Fallbacks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| generation | 24 | 1.677656 | 379583 | 91849 | 1255.840 | 0 | 0 / 0 | 0 |
| critic | 12 | 0.521615 | 225545 | 137457 | 2084.548 | 0 | 0 / 0 | 0 |
| corpus | 115 | 2.576317 | 2274346 | 522336 | 6283.658 | 0 | 0 / 0 | 0 |
| judge | 24 | 1.959600 | 585850 | 13470 | 439.759 | 0 | 0 / 0 | 0 |
| total | 175 | 6.735188 | 3465324 | 765112 | 10063.805 | 0 | 0 / 0 | 0 |

Summed original attempt duration: 10069.2 s. Recorded activity span, including gaps: 10104.065 s. Unknown attempt durations: 0.

| Requested model | Used model | Calls | Estimated USD | Unknown usage / used model |
|---|---|---:|---:|---:|
| claude-sonnet-4-6 | claude-sonnet-4-6 | 24 | 1.959600 | 0 / 0 |
| openrouter/deepseek/deepseek-v4-pro | openrouter/deepseek/deepseek-v4-pro | 28 | 1.804199 | 0 / 0 |
| openrouter/openai/gpt-5.6-luna | openrouter/openai/gpt-5.6-luna | 95 | 0.446045 | 0 / 0 |
| openrouter/openai/gpt-5.6-sol | openrouter/openai/gpt-5.6-sol | 28 | 2.525344 | 0 / 0 |

## Original failures

Failure classes: `{"postprocess_failure_after_complete_calls": 2}`. Failed invocation receipts: 0; partial responses: 0.

- [argument_architecture__checked__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/argument_architecture__checked__chen/8ac1816319a7/job.json) attempt `8ac1816319a7`: postprocess_failure_after_complete_calls; RuntimeError: critic rulings: duplicate ledger ids: A1.F3, A2.F15, A2.F9, A3.F12, A5.F23

- [epistemological_method_detector__checked__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/epistemological_method_detector__checked__harris/a9c7c8d11194/job.json) attempt `a9c7c8d11194`: postprocess_failure_after_complete_calls; RuntimeError: critic rulings: duplicate ledger ids: F13, F17, F19, F20, F25

## Corpus call accounting

| Job | Status | Nominal | Latest calls | Reanchors | All-attempt calls | Automatic chunk routes |
|---|---|---:|---:|---:|---:|---:|
| [conditions_of_possibility_analyzer__deep__deutschmann](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__deep__deutschmann.md) | complete | 21 | 29 | 8 | 29 | 0 |
| [conditions_of_possibility_analyzer__deep__castoriadis](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__deep__castoriadis.md) | complete | 21 | 28 | 7 | 28 | 0 |
| [inferential_commitment_mapper__deep__deutschmann](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__deep__deutschmann.md) | complete | 21 | 30 | 9 | 30 | 0 |
| [inferential_commitment_mapper__deep__castoriadis](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__deep__castoriadis.md) | complete | 21 | 28 | 7 | 28 | 0 |

Maximum saved user prompt: 363323 characters; frozen automatic-chunk threshold: 999999999. Saved prompt lengths versus the verified frozen run_engine_call_auto threshold. Recorder omits chunked/num_chunks; internal provider request counts are not asserted.

| Corpus job | Missing cited IDs | Missing lineage IDs | Incomplete cross-document rows | Verify carried counts by document |
|---|---|---|---|---|
| [conditions_of_possibility_analyzer__deep__deutschmann](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__deep__deutschmann.md) | — | — | — | deutschmann2001_capitalism_as_religion: 0; deutschmann2001_promise_of_absolute_wealth: 0; deutschmann2022_interpretation_of_capitalism_as_religion: 0; corpus: 0 |
| [conditions_of_possibility_analyzer__deep__castoriadis](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__deep__castoriadis.md) | — | — | F8 | castoriadis1984_technique: 0; castoriadis1990_what_democracy: 0; castoriadis1997_rationality_of_capitalism: 0; corpus: 0 |
| [inferential_commitment_mapper__deep__deutschmann](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__deep__deutschmann.md) | — | — | F14 | deutschmann2001_capitalism_as_religion: 0; deutschmann2001_promise_of_absolute_wealth: 0; deutschmann2022_interpretation_of_capitalism_as_religion: 0; corpus: 0 |
| [inferential_commitment_mapper__deep__castoriadis](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__deep__castoriadis.md) | — | — | F10 | castoriadis1984_technique: 0; castoriadis1990_what_democracy: 0; castoriadis1997_rationality_of_capitalism: 0; corpus: 0 |

## Checked finding dispositions

| Job | In | Confirmed | Carried | Weakened | Rejected | Added | Added dropped | Unverified retained |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [conditions_of_possibility_analyzer__checked__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__checked__harris.md) | 27 | 24 | 0 | 3 | 0 | 3 | 0 | 1 |
| [conditions_of_possibility_analyzer__checked__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__checked__zambrana.md) | 24 | 24 | 0 | 0 | 0 | 2 | 2 | 0 |
| [conditions_of_possibility_analyzer__checked__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__checked__chen.md) | 26 | 26 | 0 | 0 | 0 | 5 | 0 | 0 |
| [argument_architecture__checked__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/argument_architecture__checked__harris.md) | 28 | 27 | 0 | 1 | 0 | 7 | 0 | 1 |
| [argument_architecture__checked__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/argument_architecture__checked__zambrana.md) | 28 | 27 | 0 | 1 | 0 | 7 | 6 | 1 |
| [argument_architecture__checked__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/argument_architecture__checked__chen.md) (recovered) | 25 | 23 | 0 | 0 | 2 | 7 | 4 | 0 |
| [inferential_commitment_mapper__checked__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__checked__harris.md) | 26 | 25 | 0 | 0 | 1 | 2 | 0 | 1 |
| [inferential_commitment_mapper__checked__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__checked__zambrana.md) | 22 | 21 | 0 | 1 | 0 | 2 | 0 | 1 |
| [inferential_commitment_mapper__checked__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__checked__chen.md) | 28 | 25 | 3 | 0 | 0 | 3 | 0 | 1 |
| [epistemological_method_detector__checked__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/epistemological_method_detector__checked__harris.md) (recovered) | 26 | 24 | 0 | 1 | 1 | 3 | 0 | 1 |
| [epistemological_method_detector__checked__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/epistemological_method_detector__checked__zambrana.md) | 22 | 21 | 0 | 1 | 0 | 2 | 1 | 1 |
| [epistemological_method_detector__checked__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/epistemological_method_detector__checked__chen.md) | 25 | 25 | 0 | 0 | 0 | 2 | 0 | 0 |
| Total valid finals | 307 | 292 | 3 | 8 | 4 | 45 | 13 | 8 |

## Final wall metrics

| Job | Valid final | Wall provenance | Rows verified / parsed | Anchors verified / parsed | Cross-document rows | Incomplete pairs |
|---|---|---|---:|---:|---:|---|
| [conditions_of_possibility_analyzer__old__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__old__harris.md) | True | runner post-output wall | 24 / 24 | 24 / 24 | 0 | — |
| [conditions_of_possibility_analyzer__checked__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__checked__harris.md) | True | process final wall | 29 / 30 | 29 / 30 | 0 | — |
| [conditions_of_possibility_analyzer__old__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__old__zambrana.md) | True | runner post-output wall | 26 / 26 | 26 / 26 | 0 | — |
| [conditions_of_possibility_analyzer__checked__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__checked__zambrana.md) | True | process final wall | 26 / 26 | 26 / 26 | 0 | — |
| [conditions_of_possibility_analyzer__old__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__old__chen.md) | True | runner post-output wall | 25 / 25 | 25 / 25 | 0 | — |
| [conditions_of_possibility_analyzer__checked__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__checked__chen.md) | True | process final wall | 31 / 31 | 31 / 31 | 0 | — |
| [argument_architecture__old__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/argument_architecture__old__harris.md) | True | runner post-output wall | 25 / 28 | 25 / 28 | 0 | — |
| [argument_architecture__checked__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/argument_architecture__checked__harris.md) | True | process final wall | 34 / 35 | 34 / 35 | 0 | — |
| [argument_architecture__old__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/argument_architecture__old__zambrana.md) | True | runner post-output wall | 26 / 26 | 26 / 26 | 0 | — |
| [argument_architecture__checked__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/argument_architecture__checked__zambrana.md) | True | process final wall | 34 / 35 | 34 / 35 | 0 | — |
| [argument_architecture__old__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/argument_architecture__old__chen.md) | True | runner post-output wall | 26 / 26 | 26 / 26 | 0 | — |
| [argument_architecture__checked__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/argument_architecture__checked__chen.md) | True | process final wall | 30 / 30 | 30 / 30 | 0 | — |
| [inferential_commitment_mapper__old__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__old__harris.md) | True | runner post-output wall | 35 / 38 | 35 / 38 | 0 | — |
| [inferential_commitment_mapper__checked__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__checked__harris.md) | True | process final wall | 26 / 27 | 30 / 31 | 0 | — |
| [inferential_commitment_mapper__old__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__old__zambrana.md) | True | runner post-output wall | 26 / 26 | 26 / 26 | 0 | — |
| [inferential_commitment_mapper__checked__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__checked__zambrana.md) | True | process final wall | 23 / 24 | 26 / 27 | 0 | — |
| [inferential_commitment_mapper__old__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__old__chen.md) | True | runner post-output wall | 25 / 25 | 25 / 25 | 0 | — |
| [inferential_commitment_mapper__checked__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__checked__chen.md) | True | process final wall | 30 / 31 | 34 / 35 | 0 | — |
| [epistemological_method_detector__old__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/epistemological_method_detector__old__harris.md) | True | runner post-output wall | 23 / 24 | 23 / 24 | 0 | — |
| [epistemological_method_detector__checked__harris](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/epistemological_method_detector__checked__harris.md) | True | process final wall | 27 / 28 | 30 / 31 | 0 | — |
| [epistemological_method_detector__old__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/epistemological_method_detector__old__zambrana.md) | True | runner post-output wall | 23 / 24 | 23 / 24 | 0 | — |
| [epistemological_method_detector__checked__zambrana](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/epistemological_method_detector__checked__zambrana.md) | True | process final wall | 23 / 24 | 23 / 24 | 0 | — |
| [epistemological_method_detector__old__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/epistemological_method_detector__old__chen.md) | True | runner post-output wall | 24 / 24 | 24 / 24 | 0 | — |
| [epistemological_method_detector__checked__chen](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/epistemological_method_detector__checked__chen.md) | True | process final wall | 27 / 27 | 27 / 27 | 0 | — |
| [conditions_of_possibility_analyzer__deep__deutschmann](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__deep__deutschmann.md) | True | process final wall | 28 / 28 | 29 / 29 | 1 | — |
| [conditions_of_possibility_analyzer__deep__castoriadis](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__deep__castoriadis.md) | True | process final wall | 28 / 29 | 33 / 33 | 3 | F8 |
| [inferential_commitment_mapper__deep__deutschmann](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__deep__deutschmann.md) | True | process final wall | 29 / 30 | 44 / 44 | 12 | F14 |
| [inferential_commitment_mapper__deep__castoriadis](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__deep__castoriadis.md) | True | process final wall | 25 / 26 | 42 / 42 | 9 | F10 |

Process final walls retain corpus ancestry information even when a synthesis omits its dimension tag; the table prefers them where available. The JSON aggregate preserves both wall records.

## What the judge reasons establish

The [complete reason audit](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/judge_evidence_2026_09_05.md) separates agreed preferences from splits. Several reasons favor passage-specific inferential work while also using presentation cues. Commitment/Zambrana checked-first explicitly treats the check receipt as a second pass for accuracy; Commitment/Harris and Epistemology/Harris checked-first praise a rejected finding as evidence of calibration. Those statements show that the apparatus was visible, not that the critic's decision was independently validated. In Commitment/Chen old-first, the judge says the checked open-question list is longer, although the submitted old output has ten questions / 215 whitespace words and checked has five / 101. Its reverse-order reason correctly identifies old as more numerous. The mappings are sound; at least one stated differentiator is factually wrong.

## Interpretation limits

- Only agreeing valid Sonnet judgments in both orders count as old/checked wins or ties; splits are excluded, incomplete pairs stay incomplete.
- Output formatting and check receipts may reveal treatment despite A/B labels and counterbalanced order.
- This compares whole production treatments: original questions plus one Sol reading versus redesigned questions, method cards, synthesis brief, a Sol reading, and a DeepSeek check. It does not isolate any question's benefit or the critic's contribution.
- Generation includes old-question and production single-paper Sol readings; critic includes their DeepSeek checks; corpus includes the full DVS runs; judge includes Sonnet comparisons.
- Costs are original invocation-receipt estimates using repository prices, including failed attempts; recovery copies and process receipts are not added again. Missing usage/cost is unknown, not zero.
- Invocation duration includes recorder overhead. Summed original job-attempt seconds exclude idle/review gaps; recorded activity span includes gaps. Offline recovery CPU adds no model latency or billing.
- Requested-versus-used model mismatch is a reported fallback. Provider retries, refusals, internal attempts, or charges may not be fully represented by returned usage.
- Old-prompt auxiliary sections can parse as findings; old/checked row counts are not directly comparable. Anchor occurrence and wall shape are not semantic validity.
- Carried findings were unmentioned by the critic and are separate from confirmed findings, even when frozen rendering assigns a confirmed status. Added/dropped counts are dispositions, not an accuracy score.
- Corpus verify receipts expose carried/rejected/added counts unevenly; absent counters are unknown. Final wall and source coverage do not establish a valid genealogy.
