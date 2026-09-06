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

The run, as it happened: launched 17:36 (cancelled at 34/36 profiles for the key defect, $2.64); relaunched 18:00 with uid keys and the
profiles carried over; paused at `awaiting_brief` (a runner bug for chosen-path jobs, fixed) and resumed 18:08; the engagement map's verify
pass ran one text at a time (the process runner ignored the YAML's `parallel_over` on verify) and the analysis hit its 90-minute clock at
19:39 with its outputs unsaved (a missing executor row); relaunched 19:41 and again 19:51 on a pooled verify with a four-hour clock; engines
done 21:01 (engagement map 4.1 deep: 23 rows, 34/34 anchors; fidelity audit 4.2 standard over the whole 2.8M-char corpus in one call: 28
pairs, accurate 6 · fair 4 · selective 5 · stretched 1 · unverifiable 12, five unverifiable rows tagged by the wall; reception map 4.3 deep:
26 rows, 33/33 anchors); desks 21:02–21:17 (five spine sections with finding ids; three tables, 12 · 20 · 17 rows, none dropped; the draft
"Riley's Weber: Modular Borrowing, Selective Fidelity, Gramscian Frame", every claim anchored; the crosscheck refused a clean verdict on
three framing faults: a conclusion that restates the decision table, "twelve citing acts" said of a 27-text corpus, a foil of Riley's used as
evidence about Weber). Recorded cost $31.11 on the job plus about $8 of unreceipted calls lost with the first analysis process. Archive:
`data/study/citation_family_2026_09_06/pilot/dossier-bdc5eb48c407/`; the reading pair and the ledgers under
`citation_pilot_riley_weber_2026_09_06/`; Claude's source read `source_memos/mastermind_dossier_read_2026-09-06.md` (committed 63d57ae
before any score was opened): anchors verified by code, no fabrication or attribution reversal found in the rows and claims read (the one
stretched verdict, the 2018/2025 estate tension, the rationalization foil, the reception contrasts), the four framing defects above.

## The owner's read

Pending. The owner reads `mastermind_dossier_riley_on_weber.md` and `stacks_memo_2_riley_on_weber.md` in the reading-pair folder before opening `compare/`.

## Sonnet, both orders

The judge sees a bounded packet (`scripts/pilot_compare_riley_weber.py`): every held Weber window, the index's passage windows, and every
quotation of 40+ characters either memo makes with ±1,200 normalized characters of context, from the pilot corpus and the three extra texts;
it is told not to certify coverage or absence from the packet and not to infer quality from the format. Six criteria per memo, then the pair
in both orders; the pairwise verdict counts only when both orders agree.

Run 21:26–21:28 on claude-sonnet-4-6 over a 240K-char packet (35 documents: 8 whole, 27 windowed; both memos' quotations located; $1.35 for four calls). The scores and the two pairwise verdicts are sealed in `citation_pilot_riley_weber_2026_09_06/compare/` (`summary.json`, `rubric_ours.json`, `rubric_theirs.json`, `pair_ours_first.json`, `pair_theirs_first.json`) and are not quoted here until the owner has read both memos.

## Decision

Pending the owner's read and the opened scores. The question: retire the Stacks' lane, keep it as the fast path, or make it the planner and editor around the Mastermind's ledgers.
