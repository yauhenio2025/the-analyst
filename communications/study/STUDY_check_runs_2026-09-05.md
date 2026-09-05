# One call, then the critic: does the check make the ledger more reliable? (2026-09-05)

29 readings checked by deepseek-v4-pro; judged blind on claude-sonnet-4-6, both orders, ledger against ledger with the source in view.

**Head-to-head, after-check ledger vs before:** after wins 41, before wins 16, ties 1 of 58.

Both orders agree: after better in 16, before better in 4, split or tie in 9 of 29 readings.

Judge's counts per ledger (mean): unsupported rows before 0.4 → after 0.1; misses before 3.2 → after 1.2.

| engine | model | paper | rows before → after | anchors before → after | rejected | weakened | added | after wins (of 2) | critic $ | s |
|---|---|---|---|---|---|---|---|---|---|---|
| argument_arc | dsflash | aukus | 28 → 19 | 46% → 100% | 17 | 0 | 8 | 1 | 0.05 | 169 |
| argument_arc | dsflash | subsea | 25 → 24 | 68% → 100% | 2 | 0 | 4 | 2 | 0.05 | 122 |
| argument_arc | dspro | aukus | 27 → 25 | 63% → 100% | 8 | 0 | 8 | 0 | 0.06 | 197 |
| argument_arc | dspro | subsea | 22 → 19 | 91% → 100% | 4 | 1 | 2 | 1 | 0.05 | 479 |
| argument_arc | fable | aukus | 31 → 38 | 100% → 100% | 1 | 0 | 8 | 2 | 0.06 | 223 |
| argument_arc | fable | subsea | 28 → 41 | 96% → 100% | 2 | 0 | 16 | 2 | 0.06 | 271 |
| argument_arc | kimi3 | aukus | 28 → 30 | 100% → 100% | 0 | 2 | 3 | 2 | 0.06 | 204 |
| argument_arc | kimi3 | subsea | 25 → 29 | 92% → 100% | 0 | 2 | 6 | 2 | 0.06 | 407 |
| argument_arc | luna | aukus | 18 → 24 | 89% → 100% | 0 | 4 | 7 | 2 | 0.03 | 60 |
| argument_arc | luna | subsea | 20 → 23 | 95% → 100% | 2 | 0 | 6 | 1 | 0.05 | 120 |
| argument_arc | sol | aukus | 24 → 26 | 92% → 100% | 0 | 0 | 4 | 0 | 0.05 | 128 |
| argument_arc | sol | subsea | 29 → 37 | 86% → 100% | 0 | 2 | 12 | 1 | 0.07 | 321 |
| argument_arc | sonnet | aukus | 20 → 24 | 95% → 100% | 1 | 1 | 6 | 2 | 0.05 | 313 |
| argument_arc | sonnet | subsea | 22 → 22 | 77% → 100% | 0 | 2 | 4 | 1 | 0.06 | 212 |
| conditions_o | dsflash | aukus | 19 → 15 | 100% → 100% | 7 | 1 | 3 | 0 | 0.04 | 134 |
| conditions_o | dsflash | subsea | 23 → 19 | 65% → 100% | 4 | 3 | 6 | 1 | 0.05 | 250 |
| conditions_o | dspro | aukus | 20 → 24 | 100% → 100% | 1 | 0 | 5 | 1 | 0.04 | 63 |
| conditions_o | dspro | subsea | 22 → 23 | 82% → 100% | 0 | 0 | 4 | 2 | 0.05 | 238 |
| conditions_o | fable | aukus | 31 → 31 | 100% → 100% | 1 | 0 | 1 | 2 | 0.04 | 219 |
| conditions_o | fable | subsea | 34 → 35 | 100% → 100% | 2 | 2 | 4 | 1 | 0.05 | 265 |
| conditions_o | kimi | aukus | 25 → 27 | 96% → 100% | 0 | 0 | 3 | 2 | 0.04 | 174 |
| conditions_o | kimi3 | aukus | 27 → 30 | 100% → 100% | 0 | 1 | 3 | 2 | 0.04 | 221 |
| conditions_o | kimi3 | subsea | 24 → 24 | 92% → 100% | 1 | 3 | 3 | 2 | 0.05 | 146 |
| conditions_o | luna | aukus | 24 → 29 | 100% → 100% | 0 | 4 | 5 | 2 | 0.06 | 261 |
| conditions_o | luna | subsea | 29 → 30 | 90% → 100% | 0 | 0 | 4 | 2 | 0.04 | 152 |
| conditions_o | sol | aukus | 25 → 27 | 100% → 100% | 1 | 0 | 3 | 2 | 0.04 | 166 |
| conditions_o | sol | subsea | 24 → 24 | 83% → 100% | 0 | 1 | 4 | 1 | 0.05 | 267 |
| conditions_o | sonnet | aukus | 20 → 23 | 100% → 100% | 1 | 0 | 4 | 0 | 0.04 | 160 |
| conditions_o | sonnet | subsea | 20 → 22 | 90% → 100% | 1 | 6 | 4 | 2 | 0.06 | 309 |

Per model (mean over engines and papers):

| model | rejected | weakened | added | anchors before → after | after wins of pairs |
|---|---|---|---|---|---|
| dsflash | 7.5 | 1.0 | 5.2 | 70% → 100% | 4/8 |
| dspro | 3.2 | 0.2 | 4.8 | 84% → 100% | 4/8 |
| fable | 1.5 | 0.5 | 7.2 | 99% → 100% | 7/8 |
| kimi | 0.0 | 0.0 | 3.0 | 96% → 100% | 2/2 |
| kimi3 | 0.2 | 2.0 | 3.8 | 96% → 100% | 8/8 |
| luna | 0.5 | 2.0 | 5.5 | 93% → 100% | 7/8 |
| sol | 0.2 | 0.8 | 5.8 | 90% → 100% | 4/8 |
| sonnet | 0.8 | 2.2 | 4.5 | 91% → 100% | 5/8 |

Critic cost $1.48; judging $5.14.
