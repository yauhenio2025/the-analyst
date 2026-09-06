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

### Attempt 3 (the one that counts): 7 batches, 878 s, $5.59

| | |
|---|---|
| ledger rows | 139 (paired_fidelity 105, the rest attribution kind, source position, context, edition, sample practice) |
| anchors | 259, of which 257 re-found verbatim by the wall; 2 failed (F114, F415: the same S4 sentence, quoted as "Weber defends Bücher's system, conceiving his stages as ideal types, hence not in the sense of a determinate chronological sequence", which the held text does not contain in those words); those two rows are tagged and dropped by the desks, so two accurate verdicts rest on an unverified witness |
| pairs with a verdict | 105 of 105 (every held pair); by pair: accurate 69 (67 with both anchors verified), fair 30, selective 6, stretched 0, misattributed 0, unverifiable 0 |
| by statement (the worst of its pairs) | accurate 23, fair 22, selective 5 |
| every verdict row | pair-ref, attribution kind (direct · reported · contrast · none), what A attributes, what P says, `how` (page · section · search), a reason, an anchor from the statement list and an anchor from the source with distinct keys |

Attempt 2 (batched, the memo prose as the citing text, $5.50) reached 88 verdicts in its ledgers; its batch 4 declared its 17 pairs unverifiable
because "statement 25 is not marked in the memo": the translator had shown the model the memo's prose and only the metadata of the statements.
Kept under `attempt2_batched_memo_body/` as the record of the defect. Attempt 1 ($0.16) is the refusal above. Total spent on the record: $11.25.


## Reading the two side by side

Two units, two vocabularies. The Stacks judge a statement against all the sources it cites at once (supported · partly · unsupported ·
misattributed); we judge each statement × source pair (accurate · fair · selective · stretched · misattributed · unverifiable) and roll up to the
statement by the worst pair. Cross-tab of our roll-up against the Stacks' Sonnet 5 run (run 4, 50 statements):

| ours \ Stacks Sonnet 5 | supported (39) | partly (10) | misattributed (1) |
|---|---:|---:|---:|
| accurate (23) | 19 | 3 | 1 |
| fair (22) | 19 | 3 | 0 |
| selective (5) | 1 | 4 | 0 |

Read as a direction, the two agree: the memo is grounded in its four sources, nothing is invented, and the softer verdicts cluster on the same
statements (four of our five "selective" statements are their "partly"). The differences are granularity and vocabulary: our "fair" (the
attribution holds, a qualifier or a compression noted) is their "supported"; our "selective" (the source supports part of a compound
statement) is mostly their "partly". Gemini's run (48 supported, 2 partly) agrees with the direction and with none of the nuance.

**The one flag they raise and we do not.** Statement 17 ("From religious causation to a bundle of conditions: S4 rejects the interpretation of
Weber as making capitalism an expression of Protestant mentality. S1 and S2 incorporate religious ethics into the rationalization of conduct
while subordinating monocausal claims …"): Sonnet 5 called it misattributed because Weber's "two foolish and doctrinaire theses" disclaimer
appears in S1's footnote 4 and S2's identical footnote, "not clearly stated in S4's text". Our audit read the three pairs separately:
S4 — "That was of course an entirely mistaken interpretation, both in respect of Weber and for Marx" (Bruhns 2006, on the Protestant-mentality
reading); S1 — "a whole bundle of factors, among which the religious is essential but only one of many"; S2 — Weber "had only pursued 'one side
of the causal relationship'". All three re-found by code. My read (Claude, under the first-queue standard): the statement attributes to S4 a
rejection of the Protestant-mentality reading, and S4 rejects it in its own words; the Stacks' verdict rests on the location of one quotation,
not on the claim. Their flag is a false positive here; ours ("accurate" ×3) stands.

**Our six selective pairs**, read against the sources: st1/S3 (the French article supports the ideal-typical comparison, not the memo's full list
of law, religion, associations, coercion); st10/S4 (the rejection is there, the "bundle" is not S4's developed claim); st22/S4 (the
anti-genetic conclusion holds; Rodbertus is not named in S4); st40/S2 and st40/S4 (an "open question" line: the sources supply the instruments,
not the beyond-sample question); st50/S3 (Sombart's economic-system concept appears; the four-topic comparison is not developed). All six are
right as readings of the sources; two of them (st40, st50) are questions and reading suggestions, not attributions, which the memo shape files as
statements. Design note below.

**Cost.** Ours $5.59 for 105 pair verdicts with two verbatim anchors each and a critic pass per batch; theirs $0.33 (Sonnet 5) and $0.10 (Gemini)
for 50 statement verdicts with a quoted passage each: 17× and 56×. That is the price of the pair unit and the wall, and it is what makes the
result citable row by row.


## Decisions

1. **The second input mode works and stays**: `role: statements` (the Stacks' digest_check inputs, or any code-numbered statement list with
   its sources by uid) into `citation_fidelity_audit` through the evidence index, no new engine and no catalogue entry; released as plumbing
   (commits 8ed7a98, f1da827, 4d061af). Its anchors are the statement's own words (A) and the source's (W), both verified by code.
2. **Batching is the audit's shape for a memo**: a memo of fifty statements over four sources is a corpus of a hundred pairs, and the one-call
   modes cap a ledger at a few dozen rows; Sol's refusal to fake a partial audit was right. Batching by statements lives in
   `scripts/run_memo_fidelity_inprocess.py` tonight; to move into the process runner as "corpus-scope pair audits batch by the citing unit when
   the index carries more than ~25 pairs" (tracker item), so a dossier job with a `statements` source gets it without a script.
3. **Non-attributive statements**: the memo shape's "still open", "next steps" and "reading" lines are questions and suggestions; the translator
   should mark their section kind and the plan should ask for grounding (do the sources supply what the question presupposes) rather than an
   attribution verdict. Small change to `src/sources/memo_statements.py` and the plan text; not yet done.
4. **For the Stacks**: their digest_check remains the cheap tier at filing time; our audit is the audit tier for a memo that is disputed, cited
   onward, or read by the owner. On this record theirs found no fabrication because there is none, and its one "misattributed" is a false
   positive on my read; a memo with a real stretched attribution is the test neither run has had yet.
5. **As a statement-level wall on our own dossiers**: the draft's prose can be cut into numbered statements with the sources they cite (the
   spine's claims already carry anchors and finding ids) and audited the same way; a statements extractor from our draft is the missing piece
   (next session).

