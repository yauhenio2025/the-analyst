# Frontier study — synthesis (2026-09-05, 02:30)

> Question: for the two redesigned engines, which execution shape and which model give the best reading per dollar and per minute? Four shapes × seven models × two papers × two engines, 91 runs, two blind judges, $87.41 all in ($58.56 generation, $28.85 judging). Runner `scripts/study_engine_harness_v3.py`; aggregates `scripts/study_frontier_analysis.py`; per-run table `STUDY_frontier_runs_2026-09-05.md`; outputs, receipts and judgments under `data/study/v3/` on the desk machine. Designs: `REDESIGN_*_2026-09-04.md`.

## 1. What was run

- **Shapes.** (a) one call carrying the redesigned question sets and method cards; (b) the production four-stance harness at deep depth, unchanged, as the control; (c) extract → verify → synthesize with every step on the same model; (d) the same chain with extraction on GPT-5.6 Luna, the critic on DeepSeek V4 Pro, and only the synthesis on the model under test.
- **Models.** Fable 5.1 ($10/$50 per M), GPT-5.6 Sol ($2/$10), Kimi K3 ($3/$15; K2.6 ran once and was replaced at the owner's ask), Sonnet 4.6 ($3/$15, the production model), DeepSeek V4 Pro ($1.04/$2.09), GPT-5.6 Luna ($0.2/$1.2), DeepSeek V4 Flash ($0.09/$0.18). Shape (b) ran on Fable, Sonnet, Sol and Luna only; (d) synthesised on the five stronger models; the Fable-everywhere chain ran on the AUKUS paper only ($7.63 and $8.66 a run).
- **Papers.** Wijaya & Hayes 2025 on AUKUS (86K chars) and Abels 2026 on subsea cables (77K chars).
- **Judges.** Sonnet 4.6 and GPT-5.6 Sol, blind: a six-criterion rubric (specificity, anchoring, non-obviousness, coherence, usefulness, hallucination risk) on every output, and a head-to-head of every output against the Fable one-call on the same paper, each judge seeing one order. Code, not a judge, measured the share of each output's ledger quotes that appear verbatim in the source.

## 2. The tables


## conditions_of_possibility_analyzer

| condition | rubric mean sonnet / sol | hallucination sonnet / sol (10 = none) | pairwise wins vs Fable one-call, sonnet / sol | mean cost $ | mean seconds | anchors verified | n |
|---|---|---|---|---|---|---|---|
| a (excluding the Fable baseline itself) | 7.54 / 8.63 | 8.0 / 7.4 | 6/13 / 1/13 | 0.08 | 133 | 92% | 13 |
| b | 6.94 / 8.00 | 6.4 / 5.2 | 2/8 / 1/8 | 0.49 | 423 | 85% | 8 |
| c | 7.33 / 8.67 | 7.6 / 7.5 | 6/13 / 2/13 | 1.17 | 703 | 97% | 13 |
| d | 7.38 / 8.60 | 7.9 / 7.3 | 6/10 / 0/10 | 0.50 | 480 | 98% | 10 |

Paired deltas on the same model and paper (condition minus the one call), mean and count up / down / same:

| condition | by sonnet | by sol | n |
|---|---|---|---|
| b − a | -0.65 (0 up / 8 down / 0 same) | -0.94 (0 up / 8 down / 0 same) | 8 |
| c − a | -0.17 (2 up / 10 down / 1 same) | +0.09 (6 up / 1 down / 6 same) | 13 |
| d − a | -0.15 (3 up / 6 down / 1 same) | -0.07 (3 up / 4 down / 3 same) | 10 |

The one call per model (mean of the two papers):

| model | rubric sonnet / sol | hallucination sonnet / sol | wins vs Fable one-call sonnet / sol | cost $ | seconds | anchors | n |
|---|---|---|---|---|---|---|---|
| fable | 7.58 / 8.75 | 8.0 / 7.5 | baseline | 1.49 | 274 | 100% | 2 |
| sol | 7.67 / 9.25 | 8.5 / 8.5 | 2/2 / 1/2 | 0.10 | 72 | 92% | 2 |
| kimi3 | 7.75 / 8.67 | 8.5 / 7.0 | 2/2 / 0/2 | 0.13 | 77 | 96% | 2 |
| sonnet | 7.42 / 8.58 | 8.0 / 7.0 | 2/2 / 0/2 | 0.17 | 148 | 95% | 2 |
| dspro | 7.25 / 8.08 | 7.5 / 6.5 | 0/2 / 0/2 | 0.04 | 155 | 91% | 2 |
| luna | 7.67 / 9.17 | 8.0 / 8.5 | 0/2 / 0/2 | 0.01 | 37 | 95% | 2 |
| dsflash | 7.42 / 7.67 | 7.5 / 6.0 | 0/2 / 0/2 | 0.00 | 135 | 83% | 2 |
| kimi | 7.67 / 9.33 | 8.0 / 9.0 | 0/1 / 0/1 | 0.11 | 474 | 96% | 1 |

## argument_architecture

| condition | rubric mean sonnet / sol | hallucination sonnet / sol (10 = none) | pairwise wins vs Fable one-call, sonnet / sol | mean cost $ | mean seconds | anchors verified | n |
|---|---|---|---|---|---|---|---|
| a (excluding the Fable baseline itself) | 7.81 / 8.81 | 8.2 / 7.7 | 6/12 / 0/12 | 0.08 | 128 | 83% | 12 |
| b | 7.60 / 8.77 | 7.8 / 7.2 | 2/8 / 1/8 | 0.49 | 439 | 87% | 8 |
| c | 7.56 / 8.76 | 8.1 / 7.5 | 6/13 / 2/13 | 1.28 | 680 | 98% | 13 |
| d | 7.63 / 8.87 | 7.9 / 7.8 | 6/10 / 0/10 | 0.55 | 607 | 99% | 10 |

Paired deltas on the same model and paper (condition minus the one call), mean and count up / down / same:

| condition | by sonnet | by sol | n |
|---|---|---|---|
| b − a | -0.35 (2 up / 5 down / 1 same) | -0.46 (2 up / 4 down / 2 same) | 8 |
| c − a | -0.28 (2 up / 9 down / 2 same) | -0.08 (3 up / 5 down / 5 same) | 13 |
| d − a | -0.32 (1 up / 7 down / 2 same) | -0.13 (3 up / 5 down / 2 same) | 10 |

The one call per model (mean of the two papers):

| model | rubric sonnet / sol | hallucination sonnet / sol | wins vs Fable one-call sonnet / sol | cost $ | seconds | anchors | n |
|---|---|---|---|---|---|---|---|
| fable | 8.25 / 9.42 | 8.5 / 8.5 | baseline | 1.75 | 325 | 98% | 2 |
| sol | 8.17 / 9.58 | 8.5 / 9.5 | 2/2 / 0/2 | 0.10 | 71 | 89% | 2 |
| kimi3 | 7.92 / 8.92 | 8.5 / 8.0 | 1/2 / 0/2 | 0.14 | 157 | 96% | 2 |
| sonnet | 8.00 / 8.58 | 8.5 / 6.5 | 2/2 / 0/2 | 0.20 | 194 | 86% | 2 |
| dspro | 7.42 / 8.50 | 8.0 / 7.0 | 1/2 / 0/2 | 0.04 | 195 | 77% | 2 |
| luna | 7.42 / 9.33 | 8.0 / 8.5 | 0/2 / 0/2 | 0.01 | 50 | 92% | 2 |
| dsflash | 7.92 / 7.92 | 8.0 / 6.5 | 0/2 / 0/2 | 0.00 | 103 | 57% | 2 |

Judge agreement on the winner of the same pair (seen in opposite orders): 48/87.
sonnet as judge: 40 A-wins, 47 B-wins, 0 ties of 87; the Fable one-call won 47.
sol as judge: 80 A-wins, 7 B-wins, 0 ties of 87; the Fable one-call won 80.

Generation $58.56 over 91 runs; judging $28.85.

Critic's work inside the chains (mean per run; "rests on an added row" counts final-ledger rows whose lineage cites a row the critic added):

| engine | shape | critic | rows judged | rejected | added | final rows resting on an added row |
|---|---|---|---|---|---|---|
| argument_architecture | c | same model | 78 | 4.0 | 9.2 | 5.7 |
| argument_architecture | d | DeepSeek V4 Pro | 73 | 7.8 | 10.5 | 4.3 |
| conditions_of_possibility | c | same model | 70 | 4.6 | 5.4 | 2.5 |
| conditions_of_possibility | d | DeepSeek V4 Pro | 63 | 6.2 | 4.5 | 2.7 |

## 3. Reading the judges before reading the results

- **GPT-5.6 Sol's head-to-head verdicts are a position effect and are set aside.** It chose whichever reading it saw first in 80 of 87 pairs, and the split-order design showed it the Fable reading first every time. Sonnet as judge showed no lean (40 first, 47 second). Agreement between the judges on the same pair was 48 of 87, chance.
- **Sol's rubric scores favour its own family.** Sol and Luna outputs score 9.2–9.6 with Sol and 7.4–8.2 with Sonnet; Claude outputs score 8.6–8.8 with Sol. Sonnet's rubric is flat across families (7.4–8.3) and is the scale used below. Where Sol's rubric agrees in direction it is quoted as a second opinion.
- **The judges' reasons are the most useful output.** Sonnet's explanations for preferring the Fable one-call repeat one thing on the AUKUS paper: it "identifies the load-bearing definitional premise", shows the text's own definition of regulatory control ("motivated by geopolitics") inverting the abstract's causal order ("obscure the nature of the capitalist economy"), and "quotes both sides of it". Cheaper readings describe the same territory; the difference at the top is precision on the lynchpin.

## 4. What the frontier says

1. **The four-stance harness loses on every measure, on both engines, on both papers, on both judges.** On the same model and paper it scored below the one call in 8 of 8 cases on Conditions of Possibility (−0.65 Sonnet, −0.94 Sol) and in 5–6 of 8 on Argument Architecture (−0.35, −0.46); its hallucination scores are the lowest in the study (Conditions: 6.4 Sonnet, 5.2 Sol, the judges flagging claims about the authors); it won 2 of 8 head-to-heads against the Fable one-call on Sonnet's judgment; it costs $0.49 and seven minutes; and **Fable refused every one of its passes on both papers and both engines** (16 of 16 calls fell back to Sonnet) while accepting the redesigned prompts on the same papers. The old stance framing is what Fable declines, not the material. Retire it as a default.
2. **The one call with the redesigned questions is the best or tied-best execution mode.** Against it, the same-model chain (c) scores −0.17 / +0.09 (Conditions) and −0.28 / −0.08 (Argument) by Sonnet / Sol; the cheap-read chain (d) −0.15 / −0.07 and −0.32 / −0.13. Those are within a judge's noise and slightly negative, at three to sixteen times the cost and four to five times the time. Four extra calls do not buy a better reading. This confirms the 2026-09-04 result with two papers, seven models and the rewritten definitions.
3. **What the chain buys is not reading quality but the contract.** Its ledgers verify at 97–99% against 83–92% for one call and 85–87% for the four-stance harness, and the critic does real work: 4–8 rows rejected and 5–10 added per run, of which 2.5–5.7 rows reach the final ledger. Those are the anchored rows the spine, tables and figures desks can cite without re-finding quotes. Run the chain when the output feeds the desks; run the one call when a person reads it.
4. **If the chain runs, route it.** Cheap read + strong write (d) matches the same-model chain (c) at 40–45% of its cost (Conditions $0.50 vs $1.17; Argument $0.55 vs $1.28) with the best anchoring in the study (98–99%). Extraction is reading with a checklist and Luna does it at a cent a call; the critic on DeepSeek Pro rejects more than any same-model critic; the strong model should only write. The Fable-everywhere chain ($7.63–$8.66 a run; its critic writes 56K characters and timed out once at 480 s) buys nothing over (d) with Fable writing ($1.41–$1.60).
5. **Models, on the one call (Sonnet's rubric, mean of two papers).** Conditions of Possibility: Kimi K3 7.75, Sol 7.67, Luna 7.67, Fable 7.58, Sonnet 7.42, DeepSeek Pro 7.25, Flash 7.42; head-to-head against the Fable one-call, Sol, Kimi K3 and Sonnet each won 2 of 2, Luna 0 of 2. Argument Architecture: Fable 8.25, Sol 8.17, Sonnet 8.00, Kimi K3 7.92, Flash 7.92, Luna 7.42, DeepSeek Pro 7.42; Sol and Sonnet won 2 of 2, Kimi K3 1 of 2, Luna 0 of 2. **Sol at $0.10 and about 70 seconds is the value pick on both engines**; Kimi K3 ($0.13–0.14) is the second; Sonnet, the production model, is level with them at $0.17–0.20. Luna at one cent and 40 seconds scores within 0.1 of Sol on the rubric but loses every head-to-head: Sonnet's reasons say it "gives a cleaner top-level summary" and misses the lynchpin. DeepSeek Flash is the cheapest and paraphrases (57–83% of quotes verbatim). Fable is the ceiling on argument mapping at seventeen times Sol's price and mid-pack on genealogy; the Fable one-call won 47 of 87 head-to-heads, so the field is close behind it.
6. **Time.** One call: 37–325 s (Luna fastest, Fable slowest). Chains: 128–956 s on the priced models; DeepSeek Flash chains took 13–38 minutes and are not usable interactively.

## 5. Decisions read off the frontier

| question | answer | evidence |
|---|---|---|
| default execution mode | the one call with the redesigned question sets and method cards (`compose_oneshot_prompt`) | §4.2 |
| default model for a reading a person reads | GPT-5.6 Sol; Kimi K3 second; Sonnet 4.6 stays acceptable; Luna for previews and bulk; Fable when the reading is the deliverable and argument mapping is the method | §4.5 |
| when the output feeds the desks | the chain at depth `dvs` with routing cheap = Luna, mid = DeepSeek V4 Pro, strong = Sol (or Sonnet): ≈ $0.25–0.35, 5–9 min, 98–99% verified rows | §4.3, §4.4 |
| the four-stance sequence | retired as a default; kept only for reference (Fable refuses it; worst scores) | §4.1 |
| judging | never split orders with an unchecked judge; Sonnet judges both orders, or two judges both orders; Sol's rubric only as a second opinion | §3 |

## 6. Caveats

Two papers in one field (international political economy); rubric judges are models and the reliable one is the production model itself; each cell is one run (variance unmeasured; the earlier study saw position effects of a full margin); the Fable-everywhere chain on the argument engine was measured on one paper; three truncated streams (two DeepSeek, one Sol) and one timeout were redone; Fable's cost includes its hidden reasoning tokens (25K output tokens for a 34K-character reading); prices are OpenRouter's on 2026-09-04.

## 7. What was fixed during the run (walls, not method)

Four shape bugs in the ledger wall surfaced on live model output and were fixed and tested, with the finished runs rescanned: bolded row ids (Sonnet), page references after the closing quote (DeepSeek), rows without a bullet (DeepSeek), the quote in the finding with no `anchor:` field (DeepSeek), and PDF spaced hyphens in the source ("cross- referenced"). Each would have penalised a verbatim quote for its formatting. `--rescan` recomputes every run with the current parser and reruns any run whose critic output failed to parse or whose stream was truncated.
