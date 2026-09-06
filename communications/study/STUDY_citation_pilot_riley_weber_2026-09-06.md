# The Riley → Weber pilot both ways: the Mastermind's dossier and the Stacks' memo on one pair (6 Sep 2026)

The decision this pilot serves (handoff item 2): whether the Stacks' one-pair memo lane is retired, kept as the fast path, or becomes the
planner and editor around the Mastermind's ledgers. One pair, two memos, the owner's read first, then Sonnet in both orders with only
agreements counted.

## The two conditions

| | The Mastermind's dossier | The Stacks' memo 2 |
|---|---|---|
| job / record | dossier-bdc5eb48c407 (`scripts/pilot_dossier_inprocess.py`, in-process on the new machine) | em:PPZHGAXP, filed 2026-09-06 02:31 (`data/cites_memos/memo_2/`) |
| citing texts | 27 Riley texts (the pilot corpus, `pilot_corpus/PROVENANCE.md`), full texts keyed by uid | 18 Riley texts from the ledger (30 passages) |
| Weber | 28 held page windows of the cited loci (pdftotext, calibrated; the evidence index) | the ledger's context sentences; no Weber pages (written before the accuracy lens existed) |
| readers | 8 held secondary texts | none (the reception lens came later) |
| engines | engagement map (deep, dvs) → fidelity audit (standard, checked) → reception map (deep, dvs); then the desks (spine, tables, draft, crosscheck) | the memo lane: per-passage readings on Sonnet, one essay call, quotes verified by code (30 of 30 verbatim) |
| models | Luna / DeepSeek V4 Pro / Sol in the engines; Sonnet in the desks | Sonnet 5 |
| cost | see results | $0.70 |

Three of the Stacks' eighteen texts are not in the pilot corpus (the fascism book, the censuses chapter, a second record of the Bourdieu
piece); their texts were pulled from the local Zotero for the judge's packet so both memos' anchors can be checked; Perdita (2024) has no
extractable text. Neither memo is judged on coverage of texts it was not given.

## Provenance and the run

The first launch (dossier-9cdb518f9304) keyed the documents by a slug of a broken title, so the evidence index's texts never met the supplied
full texts and every citing text was double-witnessed; cancelled at 34 of 36 profiles ($2.64) and relaunched with uid keys and the paid
profiles carried over re-keyed (`--reuse-profiles-from`). The unpacker now matches by uid or key (commit 301fb8f).

RUN_PLACEHOLDER

## The owner's read

OWNER_PLACEHOLDER

## Sonnet, both orders

The judge sees a bounded packet (`scripts/pilot_compare_riley_weber.py`): every held Weber window, the index's passage windows, and every
quotation of 40+ characters either memo makes with ±1,200 normalized characters of context, from the pilot corpus and the three extra texts;
it is told not to certify coverage or absence from the packet and not to infer quality from the format. Six criteria per memo, then the pair
in both orders; the pairwise verdict counts only when both orders agree.

SCORES_PLACEHOLDER

## Decision

DECISION_PLACEHOLDER
