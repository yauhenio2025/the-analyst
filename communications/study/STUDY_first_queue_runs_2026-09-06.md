# First-queue methods S1, E8, T1: production default vs original questions (2026-09-06)

One call on Sol + DeepSeek check (`checked`) against the engine's original questions in one call on Sol (`old`, where an original exists). Independent scores by Sonnet and Sol, mean of six criteria; hallucination 10 = none; anchors verified by code.

| engine | paper | condition | rubric sonnet / sol | halluc sonnet / sol | anchors | rows | $ | s |
|---|---|---|---|---|---|---|---|---|
| deep_summarization | aukus | checked | 6.50 / 9.33 | 8 / 9 | 100% | 26 | 0.14 | 277 |
| deep_summarization | aukus | old | 8.00 / 9.33 | 9 / 9 | 100% | 26 | 0.08 | 51 |
| deep_summarization | zambrana | checked | 7.33 / 9.00 | 8 / 9 | 96% | 25 | 0.10 | 181 |
| deep_summarization | zambrana | old | 7.00 / 9.33 | 8 / 9 | 100% | 26 | 0.06 | 48 |
| event_timeline_causal | aukus | checked | 6.00 / 8.33 | 8 / 8 | 100% | 37 | 0.15 | 212 |
| event_timeline_causal | aukus | old | 6.67 / 7.67 | 8 / 7 | 100% | 25 | 0.12 | 71 |
| event_timeline_causal | subsea | checked | 6.50 / 9.00 | 9 / 9 | 94% | 35 | 0.14 | 256 |
| event_timeline_causal | subsea | old | 6.67 / 8.17 | 8 / 7 | 89% | 28 | 0.12 | 69 |
| statistical_evidence | aukus | checked | 6.33 / 9.33 | 8 / 9 | 100% | 34 | 0.16 | 195 |
| statistical_evidence | subsea | checked | 6.00 / 9.00 | 8 / 9 | 87% | 30 | 0.14 | 255 |

Generation $1.21; rating $1.30.

Reading the scores: the six-criterion rubric was written for a reading (coherence = 'one reading, not a list'); the quantity and event methods produce inventories by design, so their coherence and non-obviousness scores are low by construction. The hard measures for them are the code-verified anchor rate, the row counts, and the errors a source check finds. The raters' one-line reasons are in ratings.json.
