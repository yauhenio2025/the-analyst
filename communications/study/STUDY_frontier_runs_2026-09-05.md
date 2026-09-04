# Frontier study (2026-09-04): quality against cost and time

Runs: 91. Judges: sonnet, sol. Baseline for pairwise: Fable one-shot with the rewritten questions (condition a).

## conditions_of_possibility_analyzer

| condition | model | ran on | paper | rubric mean (sonnet / sol) | halluc (10=none) | wins vs baseline | cost $ | seconds | calls | anchor rate | rows | chars |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a | dsflash | as requested | aukus | 7.2 / 8.2 | 7 / 7 | 0/2 | 0.00 | 131 | 1 | 100% | 19 | 17,099 |
| a | dsflash | as requested | subsea | 7.7 / 7.2 | 8 / 5 | 0/2 | 0.00 | 140 | 1 | 65% | 23 | 17,172 |
| a | luna | as requested | aukus | 7.5 / 9.3 | 8 / 9 | 0/2 | 0.01 | 34 | 1 | 100% | 24 | 15,326 |
| a | luna | as requested | subsea | 7.8 / 9.0 | 8 / 8 | 0/2 | 0.01 | 40 | 1 | 90% | 29 | 19,851 |
| a | dspro | as requested | subsea | 6.8 / 7.8 | 7 / 6 | 0/2 | 0.04 | 164 | 1 | 82% | 22 | 16,340 |
| a | dspro | as requested | aukus | 7.7 / 8.3 | 8 / 7 | 0/2 | 0.04 | 145 | 1 | 100% | 20 | 15,593 |
| a | sol | as requested | aukus | 7.7 / 9.5 | 8 / 9 | 2/2 | 0.09 | 65 | 1 | 100% | 25 | 23,946 |
| a | sol | as requested | subsea | 7.7 / 9.0 | 9 / 8 | 1/2 | 0.10 | 79 | 1 | 83% | 24 | 31,221 |
| a | kimi | as requested | aukus | 7.7 / 9.3 | 8 / 9 | 0/2 | 0.11 | 474 | 1 | 96% | 25 | 19,687 |
| a | kimi3 | as requested | subsea | 8.0 / 8.7 | 9 / 7 | 1/2 | 0.13 | 112 | 1 | 92% | 24 | 17,192 |
| a | kimi3 | as requested | aukus | 7.5 / 8.7 | 8 / 7 | 1/2 | 0.14 | 42 | 1 | 100% | 27 | 19,890 |
| a | sonnet | as requested | subsea | 7.3 / 8.7 | 8 / 7 | 1/2 | 0.16 | 150 | 1 | 90% | 20 | 29,516 |
| a | sonnet | as requested | aukus | 7.5 / 8.5 | 8 / 7 | 1/2 | 0.17 | 147 | 1 | 100% | 20 | 27,929 |
| a | fable | as requested | subsea | 8.0 / 8.8 | 9 / 8 | 29/42 | 1.35 | 253 | 1 | 100% | 34 | 25,028 |
| a | fable | as requested | aukus | 7.2 / 8.7 | 7 / 7 | 35/46 | 1.62 | 295 | 1 | 100% | 31 | 34,500 |
| b | luna | as requested | subsea | 6.7 / 8.3 | 6 / 6 | 0/2 | 0.04 | 148 | 4 | 70% | 10 | 14,997 |
| b | luna | as requested | aukus | 6.3 / 8.2 | 6 / 6 | 0/2 | 0.04 | 136 | 4 | 92% | 12 | 15,784 |
| b | sol | as requested | subsea | 7.0 / 8.5 | 6 / 7 | 1/2 | 0.41 | 304 | 4 | 85% | 13 | 19,031 |
| b | sol | as requested | aukus | 7.0 / 9.2 | 7 / 8 | 1/2 | 0.46 | 338 | 4 | 93% | 15 | 23,960 |
| b | fable | **claude-sonnet-4-6** | aukus | 6.8 / 7.5 | 6 / 4 | 0/2 | 0.72 | 565 | 4 | 85% | 13 | 28,813 |
| b | fable | **claude-sonnet-4-6** | subsea | 7.5 / 7.3 | 7 / 3 | 0/2 | 0.72 | 625 | 4 | 91% | 11 | 29,886 |
| b | sonnet | as requested | subsea | 7.0 / 7.5 | 6 / 4 | 1/2 | 0.72 | 614 | 4 | 73% | 11 | 24,229 |
| b | sonnet | as requested | aukus | 7.2 / 7.5 | 7 / 4 | 0/2 | 0.80 | 652 | 4 | 91% | 11 | 25,128 |
| c | dsflash | as requested | aukus | 7.0 / 8.2 | 7 / 7 | 0/2 | 0.04 | 2263 | 7 | 86% | 42 | 28,053 |
| c | dsflash | as requested | subsea | 7.0 / 7.3 | 7 / 5 | 1/2 | 0.04 | 1629 | 7 | 86% | 51 | 28,173 |
| c | luna | as requested | aukus | 7.0 / 9.3 | 8 / 9 | 0/2 | 0.07 | 152 | 7 | 97% | 39 | 31,173 |
| c | luna | as requested | subsea | 7.2 / 9.2 | 8 / 9 | 0/2 | 0.07 | 154 | 7 | 95% | 38 | 31,063 |
| c | dspro | as requested | aukus | 7.0 / 8.3 | 7 / 7 | 0/2 | 0.34 | 631 | 7 | 100% | 31 | 33,672 |
| c | dspro | as requested | subsea | 8.0 / 8.3 | 8 / 7 | 0/2 | 0.46 | 955 | 7 | 100% | 30 | 30,633 |
| c | sol | as requested | aukus | 7.5 / 9.5 | 8 / 9 | 1/2 | 0.68 | 204 | 7 | 100% | 47 | 35,936 |
| c | sol | as requested | subsea | 7.5 / 9.2 | 8 / 9 | 1/2 | 0.75 | 214 | 7 | 100% | 59 | 36,794 |
| c | sonnet | as requested | aukus | 7.2 / 8.7 | 7 / 7 | 1/2 | 1.13 | 444 | 7 | 100% | 29 | 32,387 |
| c | kimi3 | as requested | subsea | 7.8 / 8.5 | 8 / 7 | 1/2 | 1.22 | 330 | 7 | 100% | 42 | 27,338 |
| c | sonnet | as requested | subsea | 8.2 / 8.7 | 8 / 7 | 1/2 | 1.32 | 513 | 7 | 100% | 30 | 45,514 |
| c | kimi3 | as requested | aukus | 6.8 / 8.7 | 7 / 7 | 0/2 | 1.44 | 924 | 7 | 100% | 33 | 24,309 |
| c | fable | as requested | aukus | 7.2 / 8.8 | 8 / 8 | 2/2 | 7.63 | 724 | 7 | 100% | 30 | 33,143 |
| d | dspro | as requested | subsea | 7.3 / 7.8 | 8 / 7 | 0/2 | 0.17 | 496 | 7 | 90% | 52 | 35,107 |
| d | dspro | as requested | aukus | 7.3 / 8.2 | 8 / 6 | 0/2 | 0.18 | 799 | 7 | 97% | 34 | 22,725 |
| d | sol | as requested | aukus | 7.3 / 9.3 | 8 / 9 | 0/2 | 0.22 | 289 | 7 | 100% | 32 | 30,767 |
| d | sol | as requested | subsea | 7.3 / 9.2 | 8 / 9 | 1/2 | 0.23 | 304 | 7 | 100% | 40 | 32,361 |
| d | kimi3 | as requested | subsea | 8.2 / 8.0 | 8 / 6 | 1/2 | 0.28 | 405 | 7 | 97% | 30 | 24,166 |
| d | kimi3 | as requested | aukus | 7.2 / 8.8 | 8 / 7 | 0/2 | 0.29 | 370 | 7 | 100% | 32 | 25,124 |
| d | sonnet | as requested | subsea | 7.5 / 8.5 | 8 / 7 | 1/2 | 0.32 | 535 | 7 | 97% | 30 | 31,269 |
| d | sonnet | as requested | aukus | 7.5 / 8.7 | 8 / 7 | 1/2 | 0.35 | 478 | 7 | 100% | 45 | 41,164 |
| d | fable | as requested | subsea | 7.8 / 8.8 | 8 / 8 | 1/2 | 1.41 | 378 | 7 | 100% | 30 | 28,617 |
| d | fable | as requested | aukus | 6.3 / 8.7 | 7 / 7 | 1/2 | 1.55 | 744 | 7 | 100% | 30 | 29,652 |

Best mean rubric 8.58. Within 0.5 of it, cheapest first: a/luna/aukus (8.42, $0.01, 34s); a/luna/subsea (8.42, $0.01, 40s); c/luna/aukus (8.17, $0.07, 152s); c/luna/subsea (8.17, $0.07, 154s); a/sol/aukus (8.58, $0.09, 65s); a/sol/subsea (8.33, $0.10, 79s)

## argument_architecture

| condition | model | ran on | paper | rubric mean (sonnet / sol) | halluc (10=none) | wins vs baseline | cost $ | seconds | calls | anchor rate | rows | chars |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a | dsflash | as requested | subsea | 7.8 / 7.7 | 8 / 6 | 0/2 | 0.00 | 119 | 1 | 68% | 25 | 20,871 |
| a | dsflash | as requested | aukus | 8.0 / 8.2 | 8 / 7 | 0/2 | 0.00 | 88 | 1 | 46% | 28 | 15,719 |
| a | luna | as requested | subsea | 7.5 / 9.2 | 8 / 8 | 0/2 | 0.01 | 43 | 1 | 95% | 20 | 20,483 |
| a | luna | as requested | aukus | 7.3 / 9.5 | 8 / 9 | 0/2 | 0.01 | 58 | 1 | 89% | 18 | 26,609 |
| a | dspro | as requested | subsea | 7.5 / 8.3 | 8 / 7 | 0/2 | 0.04 | 156 | 1 | 91% | 22 | 15,560 |
| a | dspro | as requested | aukus | 7.3 / 8.7 | 8 / 7 | 1/2 | 0.05 | 235 | 1 | 63% | 27 | 51,661 |
| a | sol | as requested | subsea | 8.5 / 9.5 | 9 / 9 | 1/2 | 0.09 | 64 | 1 | 86% | 29 | 23,250 |
| a | sol | as requested | aukus | 7.8 / 9.7 | 8 / 10 | 1/2 | 0.10 | 78 | 1 | 92% | 24 | 27,475 |
| a | kimi3 | as requested | subsea | 8.3 / 8.8 | 9 / 8 | 0/2 | 0.12 | 105 | 1 | 92% | 25 | 16,070 |
| a | kimi3 | as requested | aukus | 7.5 / 9.0 | 8 / 8 | 1/2 | 0.16 | 208 | 1 | 100% | 28 | 22,634 |
| a | sonnet | as requested | aukus | 7.8 / 8.5 | 8 / 6 | 1/2 | 0.20 | 180 | 1 | 95% | 20 | 33,505 |
| a | sonnet | as requested | subsea | 8.2 / 8.7 | 9 / 7 | 1/2 | 0.20 | 207 | 1 | 77% | 22 | 38,402 |
| a | fable | as requested | aukus | 8.3 / 9.2 | 9 / 8 | 31/44 | 1.72 | 311 | 1 | 100% | 31 | 32,482 |
| a | fable | as requested | subsea | 8.2 / 9.7 | 8 / 9 | 32/42 | 1.77 | 339 | 1 | 96% | 28 | 34,026 |
| b | luna | as requested | subsea | 7.7 / 9.5 | 9 / 9 | 0/2 | 0.04 | 168 | 4 | 79% | 14 | 18,970 |
| b | luna | as requested | aukus | 7.5 / 9.2 | 8 / 9 | 0/2 | 0.04 | 184 | 4 | 100% | 11 | 15,472 |
| b | sol | as requested | subsea | 8.2 / 9.5 | 9 / 9 | 1/2 | 0.45 | 404 | 4 | 86% | 14 | 26,077 |
| b | sol | as requested | aukus | 7.3 / 9.7 | 8 / 9 | 2/2 | 0.46 | 384 | 4 | 100% | 12 | 23,326 |
| b | sonnet | as requested | subsea | 7.5 / 8.8 | 7 / 7 | 0/2 | 0.72 | 600 | 4 | 92% | 12 | 24,885 |
| b | sonnet | as requested | aukus | 7.2 / 8.0 | 7 / 6 | 0/2 | 0.73 | 561 | 4 | 82% | 11 | 23,417 |
| b | fable | **claude-sonnet-4-6** | subsea | 8.2 / 8.0 | 8 / 5 | 0/2 | 0.73 | 623 | 4 | 73% | 11 | 23,523 |
| b | fable | **claude-sonnet-4-6** | aukus | 7.3 / 7.5 | 6 / 4 | 0/2 | 0.75 | 588 | 4 | 82% | 11 | 25,042 |
| c | dsflash | as requested | aukus | 7.2 / 7.8 | 8 / 6 | 0/2 | 0.03 | 763 | 7 | 100% | 27 | 33,689 |
| c | dsflash | as requested | subsea | 7.5 / 7.8 | 8 / 6 | 0/2 | 0.04 | 1938 | 7 | 98% | 57 | 39,062 |
| c | luna | as requested | aukus | 7.2 / 9.3 | 8 / 9 | 0/2 | 0.06 | 128 | 7 | 100% | 30 | 30,333 |
| c | luna | as requested | subsea | 7.5 / 9.3 | 9 / 9 | 0/2 | 0.08 | 163 | 7 | 95% | 38 | 33,998 |
| c | dspro | as requested | aukus | 7.3 / 8.3 | 7 / 7 | 0/2 | 0.42 | 956 | 7 | 77% | 22 | 27,017 |
| c | dspro | as requested | subsea | 7.3 / 8.7 | 8 / 7 | 0/2 | 0.46 | 904 | 7 | 100% | 30 | 21,481 |
| c | sol | as requested | aukus | 7.5 / 9.7 | 8 / 9 | 2/2 | 0.64 | 205 | 7 | 100% | 22 | 29,219 |
| c | sol | as requested | subsea | 7.8 / 9.5 | 8 / 9 | 1/2 | 0.74 | 205 | 7 | 100% | 29 | 29,970 |
| c | sonnet | as requested | aukus | 7.5 / 8.5 | 8 / 6 | 1/2 | 1.20 | 583 | 7 | 100% | 30 | 47,522 |
| c | sonnet | as requested | subsea | 8.3 / 8.5 | 9 / 7 | 1/2 | 1.41 | 557 | 7 | 100% | 39 | 49,664 |
| c | kimi3 | as requested | aukus | 7.8 / 9.0 | 8 / 8 | 1/2 | 1.42 | 830 | 7 | 100% | 53 | 30,113 |
| c | kimi3 | as requested | subsea | 8.0 / 8.8 | 8 / 8 | 1/2 | 1.43 | 796 | 7 | 100% | 35 | 21,532 |
| c | fable | as requested | aukus | 7.3 / 8.5 | 8 / 7 | 1/2 | 8.66 | 814 | 7 | 100% | 30 | 33,800 |
| d | dspro | as requested | subsea | 7.2 / 8.8 | 7 / 8 | 0/2 | 0.18 | 647 | 7 | 98% | 49 | 37,134 |
| d | dspro | as requested | aukus | 7.3 / 8.8 | 8 / 8 | 0/2 | 0.20 | 859 | 7 | 100% | 53 | 38,312 |
| d | sol | as requested | aukus | 7.7 / 9.5 | 9 / 9 | 0/2 | 0.21 | 336 | 7 | 100% | 26 | 29,043 |
| d | sol | as requested | subsea | 8.0 / 9.5 | 8 / 9 | 1/2 | 0.25 | 536 | 7 | 100% | 26 | 34,054 |
| d | kimi3 | as requested | subsea | 8.2 / 8.5 | 9 / 7 | 1/2 | 0.29 | 627 | 7 | 100% | 28 | 19,740 |
| d | sonnet | as requested | subsea | 8.2 / 8.2 | 8 / 7 | 1/2 | 0.40 | 778 | 7 | 98% | 58 | 47,347 |
| d | sonnet | as requested | aukus | 7.2 / 8.8 | 7 / 8 | 1/2 | 0.40 | 587 | 7 | 100% | 48 | 44,135 |
| d | kimi3 | as requested | aukus | 7.7 / 8.7 | 8 / 7 | 0/2 | 0.42 | 619 | 7 | 100% | 30 | 22,048 |
| d | fable | as requested | subsea | 8.0 / 8.7 | 8 / 7 | 1/2 | 1.54 | 521 | 7 | 97% | 30 | 27,388 |
| d | fable | as requested | aukus | 7.0 / 9.2 | 7 / 8 | 1/2 | 1.60 | 564 | 7 | 100% | 30 | 27,970 |

Best mean rubric 9.00. Within 0.5 of it, cheapest first: b/luna/subsea (8.58, $0.04, 168s); a/sol/subsea (9.00, $0.09, 64s); a/sol/aukus (8.75, $0.10, 78s); a/kimi3/subsea (8.58, $0.12, 105s); d/sol/aukus (8.58, $0.21, 336s); d/sol/subsea (8.75, $0.25, 536s)

Generation $58.56; judging $28.85; total $87.41.

A bold entry in `ran on` means the requested model refused and the runner fell back to the house model for that call; the row measures what ran, not what was asked. Fable refused every four-stance pass on the AUKUS paper (22:41) while accepting the one-call prompt with the rewritten questions.
