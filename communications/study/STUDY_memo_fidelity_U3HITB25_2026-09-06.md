# A memo against its sources, both ways: em:U3HITB25 through the fidelity audit's second input (6 Sep 2026)

The Stacks' `digest_check` checks a synthesis memo statement by statement against the texts it cites; the owner asked (handoff item 4)
for that check as the citation fidelity audit's second input mode, run both ways on one record. The record: the Stacks' memo
"Capitalism is a comparative problem, not a universal sequence" (em:U3HITB25, 2026-09-05, 17,442 chars), a synthesis across four Bruhns texts
on Weber (S1 em:RJRLLVLQ 2019 · S2 em:YASGM27U 2024 · S3 em:WGY2P4N5 2008 · S4 em:NQZYBP6Y 2006; 82.7K · 80.4K · 25.0K · 83.3K chars,
unclipped); 50 numbered statements from `digest_check.statements_of_shape` (1 core finding · 10 themes · 7 paths · 10 divergence positions ·
7 settled · 5 open · 5 next · 5 reading), every statement citing at least one label; 105 statement × source pairs. Inputs filed by the
Stacks session: `communications/inputs/stacks_fidelity_check_inputs_em-U3HITB25_2026-09-06.json`.

## The Stacks' own runs (from the file)

| run | model | unit | n | supported | partly | unsupported | misattributed | cost |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | google/gemini-3.8-flash | statement (markdown parse) | 59 | 57 | 2 | 0 | 0 | $0.10 |
| 2 | anthropic/claude-sonnet-5 | statement (partial) | 22 | 17 | 5 | 0 | 0 | $0.26 |
| 4 | anthropic/claude-sonnet-5 | statement (shape) | 50 | 39 | 10 | 0 | 1 | $0.33 |
| 5 | google/gemini-3.8-flash | statement (shape) | 50 | 48 | 2 | 0 | 0 | $0.10 |

Their unit is the statement (a verdict against all sources it cites at once); their vocabulary supported · partly · unsupported ·
misattributed · unchecked. Runs 4 and 5 match our 50 statements by number; runs 1 and 2 only partly (a different parse).

## Our run

The translator (`src/sources/memo_statements.py`): the memo is the citing author A (its markdown the citing text, each statement an indexed
passage with `ref_id st<no>` and pair ids `st<no>/<label>`), each cited source a held witness with its whole text as one `section` window; the
audit reads it through `prepare_citation_sources` like any citation index, with a plan that says a statement fuses sources and each cited
source is audited separately, that the memo is never a witness for itself, and that an unreachable place is unverifiable, never absent.

Two attempts:

1. **Unbatched, standard (oneshot_checked)**: Sol read 75,151 input tokens and wrote 598 output tokens ($0.16): a refusal on principle. It
   counted the 105 pairs, cited the mode's ledger limit of "12–30 rows", declined to audit a selection "that could misleadingly appear
   complete", and asked for either 105+ rows or batches of ten statements. Kept as `attempt1_unbatched_refusal/`. The right behaviour; the
   lesson is plumbing: a memo of fifty statements is a corpus, not a document.
2. **Batched, standard**: 7 batches of 8 statements (every source in every batch), 4 in parallel, each a Sol read → DeepSeek V4 Pro critic →
   Sol reconciliation; ledgers merged by code with the batch folded into every row id (F3 of batch 2 → F203);
   `scripts/run_memo_fidelity_inprocess.py`. Results below.

RESULTS_PLACEHOLDER

## Reading the two side by side

COMPARISON_PLACEHOLDER

## Decisions

DECISIONS_PLACEHOLDER
