# Ideas material study — protocol (2026-09-05)

Status: approved and running. The owner authorized the proposed $20 budget on 2026-09-05 after the independent review and fixes in `c199a93` / `c195138`. A fresh interpreter launched `python -u scripts/study_ideas_material.py --run --budget-usd 20` from `c195138`; study identity `374325c24e6b10a15663e9cbe9fd3520818964bc05f8f46b2d88944e0b7cbfca`, outputs under `data/study/ideas_2026_09_05/374325c24e6b10a1/`. This is step 6 of `NEXT_SESSION_PROMPT_ideas_material_2026-09-05.md`. Engine consolidation follows the findings from this study.

## Comparisons and corpus readings

| Task | Engines | Material | Work |
|---|---|---|---|
| Single-paper comparison | Conditions of Possibility, Argument Architecture, Inferential Commitment Mapper, Epistemological Method Detector | Harris 2026, Zambrana 2025, Chen 2025 | 12 original-question one-call readings on Sol, 12 current production one-call + check readings on Sol / DeepSeek V4 Pro |
| Pairwise judging | Same four engines | Same three papers | Sonnet 4.6 sees each original/current pair in both orders: 24 judgments |
| Corpus reading | Conditions of Possibility, Inferential Commitment Mapper | Deutschmann 2001/2001/2022; Castoriadis 1984/1990/1997 | Four deep chains: Luna extraction, DeepSeek V4 Pro verification, Sol synthesis |

The complete matrix has 28 generation jobs and 24 judging jobs. Each current corpus specification has five document dimensions and one corpus dimension: 15 document extracts, one corpus extract, three document checks, one corpus check, one synthesis. That is 21 base model calls per corpus job, and 144 base calls for the complete study before re-anchoring, chunking, or retries. The original prompt's estimate is $15–20 for generation and judging; actual usage must be recorded. A receipt-based stop threshold is not a provider billing guarantee: retries or requests that fail without usage can incur additional charges.

Both single-paper conditions use the same full source and requested Sol model. The original condition preserves the capability definition's original probing questions and the existing study's anchoring law. The current condition uses the production operationalization and check. This compares the complete production change, including the critic; it does not isolate the causal effect of rewriting the questions.

Only two valid opposite-order judgments naming the same condition count as a win. Two ties count as a tie; an order split or win/tie pair remains inconclusive. Missing or malformed judgments are incomplete, never ties. Judge reasons are retained with the source and output identities. A fallback model must be visible in receipts and must not be described as the requested model.

The judge receives A/B labels rather than condition names, but formatting and the appended Check receipt can reveal the production treatment. This is not a fully blinded comparison. Reversing order checks order sensitivity; it does not remove these other cues or replace source-grounded reader review.

Corpus readings have no baseline and no pairwise verdict. Review them as genealogies of a position: the commitments or givens retained, the changes and refusals supported by passages, and the relation between the papers. Do not infer a sequence between the two 2001 Deutschmann papers merely from their input order. The local corpus's year labels identify the supplied versions; they alone do not establish when an idea first appeared.

The corpus study calls `run_process` with a separate key/text entry for each document. The current workflow adapter, `src/executor/chain_runner.py::_run_engine_process`, instead wraps its incoming text in one dictionary entry, so a concatenated workflow corpus does not activate corpus dimensions. Passing document identities through the workflow adapter is an exposure prerequisite after corpus validation; this direct runner study does not certify the application's corpus dispatch.

## Evidence and review

All 11 supplied source files are present and decode as UTF-8 without replacement characters. This first matrix uses nine; the Hegel concept and Elling papers remain available for subsequent validation. The runner records source hashes and actual sizes. Use the on-disk text, not the handoff's approximate character counts. The source files and their existing `PROVENANCE.md` remain under ignored `data/study/sources_ideas/`; raw papers must not be added to the repository.

The pre-run reading guide is `STUDY_ideas_READING_GUIDE_2026-09-05.md`. It records expectations from reading the sources; it is not evidence that an engine succeeded or failed. After generation, write approximately two-page evaluation memos for the commitment and epistemology engines, then corpus reader memos, grounded in actual output rows and passages.

Particular checks:

- Zambrana: distinguish Rose's method as the paper's object from Zambrana's own way of establishing the interpretation. A missing interview or dataset is not automatically a defect in a philosophical argument.
- Chen: distinguish a theorist being interpreted or criticized from a source credited as authority; inspect the standard Chen applies to Jaeggi and whether Chen's own proposal meets it.
- Harris: state what accepting each argument commits a reader to; distinguish entailment from a plausible alternative the paper does not establish. Inspect productive tensions as well as incompatibilities.
- Corpus P6/X6: preserve both quotations and their document keys through extraction, verification, synthesis, and the desks; check quotations against the document actually named; ensure merged finding IDs are unique. The code checks quotation membership, shape, and references; readers/models judge support and significance.

Keep the current questions fixed for the initial comparison. The productive-tension question already occurs in I3 of the current commitment operationalization; determine whether the live reading uses it before adding a duplicate to I2. E1's possible object/method distinction and the possible corpus synthesis order change remain hypotheses until the readings are evaluated.

## Execution and records

`scripts/study_ideas_material.py` is the dedicated runner. Its default invocation previews the matrix without model calls; execution requires `--run`. Source, definition, prompt/code, and output identities guard resume, so changed inputs do not reuse stale results. Direct call receipts retain prompts, output, requested/used models, tokens, timing, and available cost estimates, including partial output. Interrupted or failed jobs remain explicit and cannot become successful comparison results.

The handoff's standing rule is **“Ask before spend”** and its checks section says **“≈ $15–20; ask before launching.”** Request approval for the prepared matrix before using `--run`. Preparation, offline tests, and review can proceed. Its **“Commit and push per phase (master deploys to Render)”** instruction authorizes publishing each completed, tested phase to this repository's `origin/master`.

Offline validation: 51 tests passed in a fresh interpreter after the independent review's fixes, across the ideas runner, corpus ledger, process shape, desks' ledger handoff, and prior plumbing tests. The fixes preserve ordinary findings when executor and dossier document keys differ while requiring valid declared keys for corpus rows. The model run launched only after this check and the owner's approval.

## Operational exception identified during generation

Before Sonnet judging, two checked jobs (Argument Architecture/Chen and Epistemology/Harris) failed after both model calls completed. The critic's actual rulings have unique IDs; the parser also consumes its requested `### Must keep` section, whose references repeat those IDs. The resulting duplicate-ID exception is a section-boundary defect. Raw responses, usage and original failure receipts remain available.

A narrowly scoped, offline recovery is being prepared. It must use the frozen runtime and original responses, exclude only explicit auxiliary sections from critic-row parsing, require exact matches to the original composed prompts and requested models, and refuse incomplete responses or missing calls. It must retain the original failed record and write a separate recovered artifact with response, transformation and output hashes. Replaying already completed checked jobs must establish whether this transformation leaves their outputs byte-identical; any differences require explicit review before inclusion. This is separate from the broader proposed quotation/rewrite repairs, which remain unapplied during the initial matrix.

The recovery requirements passed and the recovered artifacts were accepted for judging before any Sonnet judgment was available. Frozen `c195138` first reproduced both exact failures; the narrow boundary correction recovered both outputs and left all ten other completed checked outputs byte-identical. No checked jobs were skipped, no model calls were made, and the original failures remain intact. The accepted bundle is `reader_notes/auxiliary_recovery/20260905T045321.120955Z/` beneath the study directory; its manifest records original calls, prompt and response hashes, transformation hash, output hashes, and timing provenance.

The recovered outputs will be adopted only after the original process finishes, with a preserved results snapshot and an explicit recovery field on each affected record. The unchanged judge phase can then fill the four missing judgments. This changes output assembly, not the sources, question sets, model responses or judging rule. It avoids selecting a fresh stochastic reading merely to escape a known parser defect. The broader quotation/rewrite patch is excluded from the judged baseline.

## Bounded corpus synthesis follow-up

The first completed corpus reading, Conditions/Deutschmann, failed substantive coverage: its 28 findings all use the first paper as their primary source, with one additional quotation from 2022 and none from the other 2001 paper. The saved synthesis request contains all three full texts and all 177 expected retained findings, including 13 cross-document rows. This is an observed synthesis-selection failure, despite complete anchor and lineage checks. The [reader memo](STUDY_ideas_CORPUS_CONDITIONS_DEUTSCHMANN_2026-09-05.md) assesses the delivered result.

After the fixed 52-job matrix is complete, test one revised corpus instruction on each of the four saved synthesis requests. This adds four Sol synthesis calls, with no repeat extraction, critic calls, or Sonnet judgments. Insert only the reviewed corpus instruction into each system prompt. Its SHA-256 is `a598d16071667a9ae772a04b889ed56f66ece8e3450b7ccccc71bb2fedf46481`; the exact text is preserved in the follow-up plan. The instruction asks for a compact position map for every document followed by supported relations across the collection, with passage roles, qualifications and chronology distinguished.

Before any follow-up launch, the plan was amended for a second observed manifestation of the auxiliary-section defect. The first Castoriadis document critic returns 67 actual rulings and five positive `Must keep` references. The frozen deep path treats the references as failed rows and can put their IDs under rejected findings while keeping their actual positive rulings. An instruction-only follow-up would retain this known contradictory handoff. Reassemble each synthesis input offline with auxiliary sections excluded only when parsing the exact recorded critic responses. First reproduce the original complete run, including all prompt hashes and its final output; then require every extraction, re-anchor and critic request to remain byte-identical during the corrected replay. Only the final synthesis ledger assembly may change. Source text remains byte-identical, and affected IDs and original/reassembled user-prompt hashes must be recorded. Unaffected user prompts must remain byte-identical.

This follow-up implements the handoff's expected corpus-brief tweak and stays within the owner's existing $20 cap, measured cumulatively across the original study and follow-up receipts. Both the follow-up and amendment were disclosed before launch. It has a separate identity, original prompt/output hashes and receipts; it does not replace the baseline or alter its judging rule. Reader assessment must compare genealogy and source fidelity as well as coverage. These calls test the added corpus instruction plus the narrowly scoped auxiliary-section correction where needed; they do not isolate the instruction's effect in affected cases. The broader quotation, explicit-rewrite and question changes are excluded from their prompts and mechanical wall evaluation.
