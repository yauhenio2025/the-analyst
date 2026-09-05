# Held-out Hegel raw-format audit — 2026-09-05

**Generation audit complete: 32 saved calls, 14 normally completed outputs and two deterministic postprocessing failures.** Trial identity: `43f051bdd4d890762145163d0e1d41c9be46aa19234f61456962ded883530d7e`. Both definition conditions use frozen `d9cfc6e`, including its shared JSON-quote instruction and parser. This note audits raw model responses and their mechanical application; the separate source readings assess interpretation. No model calls, retries, or result changes are part of this audit. Luna is not exercised.

## What the numbers mean

The receipt diagnostic counts explicit supported anchor and rewrite fields in the raw ledger view. **Canonical JSON compliance is a field count**, not proof that all rows supplied the required fields. Rows with no explicit quote field are counted separately; the legacy parser may recover a first inline quotation from them. The raw membership wall separately counts parsed rows, anchors, source matches, and shortened matches. A matching substring does not certify the complete original quotation, attribution, or inference. Source membership for a critic's rewritten finding is distinct from whether the proposed wording is substantively right.

## Final raw-call totals

Every stored generation diagnostic reproduces exactly through the frozen archive. The unchanged harness also [replays all fourteen ordinary finals](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/reader_notes/original_processing_generation_report.json) with exact composed prompts, models and output bytes, returning zero validation errors and retaining both failed jobs. The [reproducible offline audit](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/reader_notes/format_audit_replay.py) denies network access; its [final JSON evidence](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/reader_notes/final_generation_format_audit.json) has SHA-256 `6a2ebdb9069efbd13ba11f393746e1000744530882fa34f0dad43495668331b4`. It preserves stored metrics separately and excludes only explicit auxiliary references when counting actual raw ledger rows. Requested critical-question rows remain included.

| Raw metric | Sol reads | DeepSeek critics |
|---|---:|---:|
| Completed calls | 16 | 16 |
| Canonical / supported quote-and-rewrite fields | 432 / 432 | 525 / 541 |
| Malformed supported fields | 0 | 16 |
| Legacy-but-parseable supported fields | 0 | 0 |
| Actual row-shaped entries | 416 | 492 |
| Rows without a supported quote/rewrite field | 9 | 9 |
| Whole-ledger parsing failures | 0 | 2 |
| Parseable rows | 416 | 435 |
| Matching / parsed anchors | 411 / 441 | 436 / 472 |
| Raw anchors longer than 200 characters | 1 | 18 |
| Reported trimmed rows in raw walls | 4 | 19 |
| Separately misspelled `revized-finding` fields | 0 | 14 |

DeepSeek's parseable-row and matching-anchor totals cover **only the fourteen fully parseable raw critics**; the two failed ledgers are not assigned zero matching anchors or silently repaired in that table. Quoting compliance can be inspected even when duplicate slots prevent whole-ledger parsing. Raw field counts include valid `revised-finding` strings, whereas anchor membership counts do not treat those rewritten findings as evidence.

Both Sol conditions have 216/216 canonical supported fields. DeepSeek's previous condition has 267/283 and revised has 258/258. The revised condition nevertheless contains the repeated-slot parser failure and the 28-ID renaming failure. These eight-call-per-condition counts establish syntax observations, not an overall ranking of checking quality.

| Role | Recorded cost USD | Input / output tokens | Sum of invocation elapsed seconds |
|---|---:|---:|---:|
| Sol | 1.420948 | 354,274 / 71,240 | 963.450 |
| DeepSeek | 0.798283 | 391,817 / 187,055 | 3,431.962 |
| Generation total | **2.219231** | **746,091 / 258,295** | **4,395.412** |

These are the original 32 generation calls, including both calls for each failed postprocessing job. Judgments are excluded. All requested and used models match the pinned routing; reported retries and API failures are zero, and costs/usage are known. All 32 receipts have null partial and stop-reason fields, which remain unknown. The two parser failures are downstream execution failures. Offline recoveries add no billing or substitute raw format diagnostics. The fourteen ordinary finals contain 29 carried original rows: one typo case and the 28-ID renaming case below; none counts as an explicit confirmation.

## First raw Sol example: previous Conditions / Ganzinger

The [raw reading](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/receipts/conditions_of_possibility_analyzer__previous__ganzinger/9a1cd9b4cd2d/call-0001.md) has 27 parsed rows and 28 matching anchors. All 25 tokenized quote fields are canonical JSON strings; there are no legacy-quoted or malformed explicit fields. Three rows have no explicit quote field. The reported cost is USD 0.090340.

- **Unlabeled second quotations are outside the secondary-anchor check.** D5.F1–F3 follow the previous rival answer shape: a rival is “available at” one quoted passage and the text forbids it by another. The parser recovers the first quote as the primary anchor; it does not register the second as `counter-anchor` or `anchor-b`. Consequently, 25/25 canonical fields does not mean whole-ledger schema compliance or verification of every quotation displayed in those rows.
- **A true quotation can become a shorter verified anchor.** D3.F2 quotes the passage connecting the essence of the Concept with “the original synthetic unity of apperception.” In the [source](../../data/study/sources_ideas/hegels_concept_of_the_concept_2026.txt), lines 34–40 span a PDF page number, publication footer and running header. The wall recovers a matching prefix ending at “the original,” dropping the phrase identifying apperception. This is the one shortened row. Its JSON was valid and its full quotation was present across the page boundary; neither the formatting metric nor the final substring match fully describes that fact.

## First raw DeepSeek example and source-matching distinction

The previous Conditions/Ganzinger critic returned 30 rows and 31 matching anchors: 28/28 explicit quote fields are canonical JSON, with the same three unlabeled rival rows. It confirmed all 27 input rows and added three, with zero carried rows, rejections or weakenings. The two calls cost USD 0.135496 in total. Requested and used models match, reported retries are zero, and both calls have null partial/stop-reason metadata; those nulls are unknown termination metadata rather than positive completion signals.

D2.F6 illustrates the structured application boundary. The critic’s reason says the performative-contradiction provenance is declared rather than hypothetical, but its actual row still supplies `provenance: hypothesis` and `status: confirmed`. The final ledger consequently retains hypothesis. The model has mentioned a correction in explanatory prose without submitting it as an applied field change.

The revised Conditions/Ganzinger Sol reading has 24 parsed rows, 27/27 canonical quote fields, no unlabeled rows, and 25/27 matching anchors. Its F5 uses `self-contradiction` where source line 641 reads `selfcontradiction`; F15 begins `The further step` where lines 556–557 use `[t]he further step`. These are source-representation differences, not malformed JSON. The critic incorrectly calls F5 verbatim and confirms it; the final wall keeps it tagged unverified. It rejects F15 for the bracket/typography mismatch rather than re-anchoring it. The unchanged prose still calls this passage the strongest bridging fact. The source supports the underlying passage, so that persistence is a mismatch between the prose and the ledger ruling, not proof of a false substantive claim.

## A successful call can fail the checking contract

Previous Conditions/Elling has one carried row: the raw and final reading use D3.F2, but the critic responds to D3.2 and misspells its anchor’s “although” as “althought.” Its unmatched confirmation is ignored. The receipt correctly reports 26 confirmed plus one unmentioned, kept; carried does not mean confirmed.

The [revised Conditions/Elling critic](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/receipts/conditions_of_possibility_analyzer__revised__elling/33e2a237dc33/call-0002.md) changes **all 28 original F-number IDs** into dimension-prefixed D-number IDs, despite receiving the original IDs and the explicit preservation instruction. It also misspells 14 proposed rewrite fields as `revized-finding`; the one correctly named `revised-finding` contains a whole serialized row rather than just its finding. The application carries all 28 originals, confirms/weakens/rejects none, and adds three of four new findings. The final is a complete saved checked invocation, but its original findings did not receive applied critic rulings. Canonical JSON quote syntax does not imply adherence to this larger contract.

The stored format diagnostic for that critic counts 38 row-shaped lines because it also sees five bracketed Must-keep references and one Counter-evidence reference. The frozen row parser correctly excludes them and returns **32 actual rulings**. Audit totals therefore recompute formatting on the raw lines returned by that parser; they do not silently amend the stored diagnostic. All 36 explicit supported quote/rewrite fields remain canonical. The 14 misspelled fields are outside that supported-field denominator and are separately disclosed here.

## Length clipping is not the reported trim count

Frozen `verify_quote` first clips a quote to 200 characters, then initializes its `trimmed` flag to false. Only later word-by-word substring recovery sets that flag. Consequently the final wall does not count every shortened quotation:

| Revised Conditions / Ganzinger | Original raw quote | Final anchor | Reported trimmed |
|---|---:|---:|---|
| Sol F8 | 214 characters | 200, ending “Kant’s” | No |
| Critic V.F1 → F25 | 204 characters | 200, ending midword “internally oppo” | No |
| Critic V.F2 → F26 | 116 characters | 84, ending “the original” | Yes |

F8 is already clipped in the critic’s actual input and response; F25 is clipped when applying the addition. F26 is the distinct PDF-page-boundary example. These are all canonical JSON strings. The length ceiling limits both what is displayed and what the membership wall tests; material beyond the first 200 characters is not certified by a successful prefix match. Counts of raw over-length anchors will therefore be reported separately from the receipt’s `trimmed` count.

## Application boundary

The frozen checked runner applies critic rulings to the findings ledger. Explicit `revised-finding` strings replace weakened finding heads, with original-finding provenance retained; the introductory prose, original counter-evidence and open questions remain unchanged. When the critic weakens, rejects, or adds rows, the final receipt now says that the preceding prose is unchanged. This disclosure is accurate, but it does not itself reconcile a sentence in the prose with a revised or rejected finding. Previous Argument/Ganzinger F3 and F12 demonstrate successful explicit rewrites with retained `original-finding` provenance, although both primarily correct anchoring or remove labels. Previous Argument/Elling F18 is a clearer substantive example: the critic changes the finding’s inference scheme from sign/example to cause in an explicit JSON `revised-finding`, and the final head adopts that classification. The reading’s preceding inference discussion remains unchanged. A well-formed applied rewrite can therefore improve the ledger while leaving the displayed essay out of step with it.


## Malformed fields and whole-ledger failures are different measures

The previous Argument/Elling critic has two malformed supported fields: F19 supplies an empty `counter-anchor`, and proposed addition V.F9 supplies `anchor: (unaddressed)`. Its whole ledger still parses. The invalid confirmation does not replace F19’s verified original anchoring, and the unsupported addition is dropped. Final matching-anchor totals consequently conceal these raw failures unless raw-call diagnostics are preserved.

Previous Epistemology/Elling adds thirteen malformed `anchor-b: not provided` placeholders, on F14–F19 and F21–F27. They remain parseable invalid secondary slots. The confirmed rulings cannot replace the originals with those bad anchor sets, so the final returns 33/33 matching anchors while the raw critic had only 34/47. This is another reason to inspect raw calls separately from sanitized finals.

The revised Argument/Ganzinger critic instead uses three repeated primary `anchor:` fields in its requested I4 critical-question row. Each quoted field is individually canonical JSON, but the duplicate slot causes strict whole-ledger parsing to fail. Previous Commitment/Ganzinger supplies the malformed bare F16 `revised-finding: same finding, anchor‑b corrected`, which causes a different whole-ledger failure. Both were successful recorded backend calls; neither was an API failure. Their original raw diagnostics remain unchanged by the [two narrowly scoped recovery proposals](STUDY_ideas_HEGEL_HELDOUT_RECOVERY_2026-09-05.md). The recovery does not turn the directive into finding prose or map unknown I IDs onto original F IDs.

The later main implementation fixes the missing initial-length-clipping provenance flag and adds explicit ruling-coverage disclosure. Those changes are excluded from the frozen trial. This audit reports `d9cfc6e` behavior and its original receipt metrics; it does not retroactively credit the study with those implementation fixes.


## Canonical JSON can encode the wrong quotation bytes

Previous Epistemology/Ganzinger makes this visible without a parser failure. Sol’s F13, F17 and F22 encode extra literal quotation marks *inside* valid JSON strings. F13’s decoded anchor therefore includes outer ASCII quotes around the note about capitalizing ‘Concept’; the source note at lines 850–851 has that wording without those outer quotes. DeepSeek confirms F13 while introducing `convenction` and `Conceppt` into its proposed anchor. Frozen application keeps the original rather than adopting that invalid replacement, and the final anchor remains explicitly unverified. The final has nine unverified rows despite 26 critic confirmations. These are source-representation and checking failures, not malformed JSON or evidence that the underlying source-supported proposition is false.
