# Ideas study: anchor audit and implemented repairs

The checked Harris reading exposed a normalization defect, an unverified secondary-quote field, lost trimming history, and a critic-rewrite contract failure. Saved responses reproduce these defects without new model calls. The repair was developed and audited separately, then applied on main only after all 52 baseline jobs and four bounded follow-up syntheses completed. Main validation passes 186 affected-path tests plus 13 study-script guards. Sections below preserve the baseline and candidate-review chronology: “current,” “proposed,” and “live” in those historical observations refer to the frozen baseline or the named candidate, not the final production status.

## Evidence and scope

Study identity: `374325c24e6b10a15663e9cbe9fd3520818964bc05f8f46b2d88944e0b7cbfca`, launched from `c19513884a5453f54073e38cbabf2c6e7d5cfd28`. The audited job is `conditions_of_possibility_analyzer__checked__harris`, attempt `625ee127acdb`.

The evidence is under [`data/study/ideas_2026_09_05/374325c24e6b10a1/`](../../data/study/ideas_2026_09_05/374325c24e6b10a1/):

- `receipts/conditions_of_possibility_analyzer__checked__harris/625ee127acdb/call-0001.md`: Sol's unmodified reading.
- The adjacent `call-0002.md`: DeepSeek V4 Pro's unmodified critic response.
- The corresponding `.json` receipts and `step-read--.json` / `step-check--.json` wall reports.
- `outputs/conditions_of_possibility_analyzer__checked__harris.md`: the production checked output, SHA-256 `a8bb04207756822d1624500c2ea4d3b8e1199dc81eb1b1849505b2a33383d410`.

The Harris source is [`harris2026_eight_arguments_against_honneth.txt`](../../data/study/sources_ideas/harris2026_eight_arguments_against_honneth.txt), SHA-256 `6daf2fecf707a3a81b54bde1cd59e1532d733b76365fb6d2acd832b22994c113`, 71,820 characters. The audited ledger, process-runner and composer files match the hashes stored in `plan.json`. The normalization helper [`src/dossier/walls.py`](../../src/dossier/walls.py) has SHA-256 `0aec91d6195b08c2b5d22b7b2e55d7a0ea83d37735b6a4d3a080df2550e91397`.

The original-question Harris output is useful context, but this audit does not assign a quality winner. The wall tests quotation membership and identifier shape. Whether a quotation supports an inference remains the critic's and reader's judgment.

## 1. A discretionary PDF line break becomes a false word boundary

Harris source lines 492–494 contain the literal sequence `experi\u00ad\nences`. D1.F3 quotes the resulting word as `experiences`. The current `normalize()` first removes U+00AD through `_QUOTE_MAP`, then tries to join hyphenated line wraps. The break marker has already disappeared, so whitespace normalization leaves `experi ences`. The quotation fails even though the words occur in the source.

This is not speculation about the text. The minimal in-memory reproduction is:

```python
normalize("experi\u00ad\nences") == "experi ences"  # current result
```

There are 58 explicit discretionary line wraps in the Harris extraction. Joining only `U+00AD + line break` between word characters, in memory, changes the saved critic's wall result from **29/30 rows verified, three trimmed** to **30/30 verified, none trimmed**. No source file was rewritten and no new model output was generated for this comparison.

The other affected quotes are:

| Row | Source break | Original critic quote length | Surviving production quote |
|---|---|---:|---|
| D3.F5 | `voca\u00ad\ntions`, source line 426 | 122 characters / 17 words | “Equally, some of the most esteemed” — 34 characters / 6 words |
| D4.F2 | `deco\u00ad\nlonial`, source line 659 | 149 characters / 21 words | “Calls for reparations, which are increasingly taking center stage within” — 72 characters / 10 words |
| D5.F5 | `weak\u00ad\nnesses`, source line 223 | 122 characters / 18 words | “the plurality of irresolvable and fatal” — 39 characters / 6 words |

The proposed fix joins explicit soft-hyphen wraps **before** removing U+00AD. It does not join arbitrary newline-separated words or remove ordinary lexical hyphens. Existing ordinary-hyphen normalization and the alternate `SourceIndex` remain unchanged. Regression cases cover LF and CRLF wraps, an inline discretionary hyphen, separate words across a plain newline, and lexical `re-form` versus `reform`.

The check receipt's wording, “rows kept with a paraphrased quote,” is inaccurate for D1.F3. A failed membership check cannot determine whether a quotation is a paraphrase, an extraction mismatch, an incorrect document key, an incomplete pair, or invented. The patch changes this to **“rows kept with an unverified or incomplete anchor.”** It retains `anchor-verified: no` as the code's observable result. The existing desks' user-facing wording already includes unverified or incomplete anchors rather than asserting that all are paraphrases.

## 2. Prefix matching verifies a substring, and serialization loses that history

`verify_quote()` deliberately removes words from the end until a prefix matches the source. `LedgerRow.render()` now carries that shortened quotation forward. In the first Harris result, the final ledger therefore contains the three short quotations above. The process receipt still records three trims, but reparsing the rendered ledger produces a wall report with `trimmed: 0`: those prefixes now match exactly, and their history is absent from the serialized row.

The substring is present in the source; that statement is correct. It does **not** establish that the original quotation was exact, or that the remaining prefix supports the finding. An offline counterexample makes the distinction visible:

```text
Source: The committee found that the proposed reform was ineffective and could not be recommended.
Claimed quote: The committee found that the proposed reform was effective and should immediately be adopted.
Verified prefix: The committee found that the proposed reform was
```

The current wall accepts the prefix and marks it trimmed. Code should not decide the substantive claim from that prefix. In Harris, “the plurality of irresolvable and fatal” omits the object and the conclusion that repair is futile. The normalization repair happens to restore the full quotation in this case; it does not eliminate the general limitation of prefix matching.

The patch preserves `trimmed-anchor: yes` and secondary equivalents such as `trimmed-anchor-b: yes` through render/reparse/reverification. Tests require both primary and secondary trim history to survive. This repairs the false disappearance of trimming from later reports while retaining the existing prefix-matching policy. The raw model receipts remain the original-quotation evidence.

A separate policy decision remains: whether to require a full normalized match for citability and treat a prefix match only as a re-anchoring hint. That would be a clear shape rule, but it changes the existing extraction/drop behavior. The proposed patch does not silently make that policy change. Nor does it equate a minimum quote length or retained fraction with semantic support.

## 3. `counter-anchor:` is requested by the definition but ignored by the wall

The Conditions of Possibility visibility dimension explicitly requests `counter-anchor:` in its answer shape, at [`conditions_of_possibility_analyzer.yaml`](../../src/operationalizations/definitions/conditions_of_possibility_analyzer.yaml), dimension `visibility`. The current parser recognizes `anchor:` and `anchor-<suffix>:`, but neither pattern recognizes `counter-anchor:`.

The final Harris ledger has five such fields: D4.F4, D4.F5, D4.F6, D4.F7, and F3, the last added by the critic as V.F3. Each row is currently represented as having one anchor. Thus the report counts 30 anchors while these five additional declared quotations are not checked. The problem is the supported field contract, not a claim that the five Harris quotations are fabricated.

An offline fixture containing a valid primary quote and a completely fabricated `counter-anchor:` still produces a verified row, and rendering preserves the unverified secondary quotation. That is a real gap in the claim that all supported anchor fields are checked.

The reviewed patch recognizes the existing spelling as the secondary `counter` anchor, including optional `counter-doc:`; it also accepts `anchor-counter:` / `doc-counter:`. Recognition is limited to actual fields outside quoted prose and metadata. It retains the raw row and does not rewrite `counter-anchor:` when those words occur inside a finding or quotation. The secondary-anchor machinery verifies the quote, inherits the primary document key for a same-document quotation, and preserves it for the desks. A declared key naming an existing source remains binding. Ordinary rows retain the baseline fallback for a foreign executor key absent from the source index; corpus rows still reject foreign declared keys. Tests cover fabricated second quotes, same-document inheritance, wrong-existing-document failure, serialization, and the desk handoff.

With this change and the soft-hyphen fix, the saved Harris critic response verifies **35/35 declared anchors across 30 rows**, with no trimming. This is an offline replay result, not a replacement for the live study's recorded 29/30 result.

## 4. An explicit critic replacement can remain outside the applied finding

All three weakened Harris rows retain the original finding at the start of the critic's row, followed by a separate quoted field `finding rewritten to:`. The intended prompt asks for the rewritten finding in the head of the row. `parse_rows()` uses that head as `.finding`; `apply_rulings()` copies `.finding` for a weakened row. It does not read the appended replacement field.

Consequently the production receipt says “weakened 3,” while the original head remains the finding consumed by `analysis_ledger()`. D5.F5 is a concrete example: the head still says that the claim collapses without the frame, while the explicit proposed replacement merely says that the text claims the plurality of weaknesses makes repair futile. Those are different findings. The latter does not establish the former's counterfactual claim.

This can become a substantive handoff bug. A bounded fixture using an original “Recognition explains every injustice” and a quoted replacement “Recognition explains some injustices” retains the universal original in the current desk handoff despite a `weakened` receipt.

The patch establishes a small explicit contract:

- New critic prompts request the rewritten head plus `revised-finding: "<replacement>"`, a JSON quoted string.
- The parser accepts that canonical field and the already observed `finding rewritten to:` alias. It does not infer a replacement from free-form `reason:` text.
- A weakened row with an explicit replacement uses the complete replacement as `.finding`. Application and rendering quote its replacement head as a JSON string so field-like prose remains prose; reparsing obtains the full finding from the explicit replacement field. A critic that already rewrote the head continues to work.
- Checked application retains the previous finding as `original-finding:` provenance. The existing raw critic/reading receipts remain unchanged.
- Empty, malformed or competing explicit replacement fields raise a shape error instead of silently reporting that the intended rewrite was applied.

Tests follow the replacement through apply → render → parse → `analysis_ledger()`, check preservation of the original, and cover quoted field-like prose inside the replacement. The patched in-memory replay applies all three Harris replacements while leaving the reading's prose unchanged, as the production check design specifies. This repair does not certify the semantic adequacy of the critic's weaker formulations.

That design leaves a separate limitation: the checked reading's prose can retain a stronger claim even after its ledger finding is weakened or rejected. The corrected ledger and the unchanged prose must therefore be assessed together; applying a critic ruling does not establish that the reading itself has been rewritten consistently.

The proposed receipt now makes this scope visible whenever findings were weakened, rejected or added: “The ledger incorporates the critic's changes; the preceding prose is unchanged from the original reading.” Offline checked-flow tests cover all three change types and confirm that the original prose and raw critic response remain untouched. This disclosure does not resolve the substantive disagreement between prose and ledger.

A subsequent deep-chain review found a further handoff gap in the candidate repair: deep verification keeps parsed critic rows directly, bypassing `apply_rulings()`. Although `.finding` contained the explicit weaker replacement, `render_rows()` still sent the original head to synthesis. Fake one-document and two-document deep runs both reproduced this failure before the correction. Rendering now uses the protected explicit replacement head without mutating the row's stored text or the raw critic receipt. The two regressions inspect the actual synthesis prompt head, including quoted `reason:` and `anchor:` prose, and follow it through final parsing, document/corpus anchor verification, lineage and the desk handoff. These are deterministic offline fixtures, not results from the forthcoming live corpus study.

## 5. Independent review: finding text must remain opaque to the field parser

The first candidate patch passed its direct replacement-property test but failed a complete apply → render → parse → desk round trip. The review reproduced four concrete problems:

| Input content | First candidate's behavior | Reviewed repair |
|---|---|---|
| Replacement `The text says "recognition" — reason: its scope is limited.` | `.finding` was correct immediately after application, but reparsing and the desk retained only `The text says "recognition"`. | The protected replacement head and explicit field preserve the complete finding at every handoff. |
| Replacement containing `anchor: "a rhetorical label"` | Rendering overwrote that prose quotation with the row's source anchor. | Rendering edits only actual anchor-field value spans. |
| Replacement containing `counter-anchor: "a rhetorical label"` | The alias substitution changed the finding's prose and introduced a false secondary anchor. | Aliases are recognized as field names only; quoted finding/provenance values remain untouched. |
| Quoted prose or provenance containing ` — revised-finding:` | The unscoped regular expression could interpret literal prose as a second replacement field and raise an error. | Field recognition skips quoted text, including escaped JSON strings and curly quotations. |

The repair retains the existing separator-delimited row format. It preserves ordinary colon-bearing heads such as `Omission:`, `Strongest form:`, `Attack on Marx:`, and `Warrant:`. These are exercised by the saved Argument Architecture / Zambrana output; an initial tokenizer draft incorrectly treated five such heads as fields, and that regression was corrected before regenerating the patch. It also preserves the legacy quoted-field fallback used by `promised-at` and `nearest-delivery`, including the observed nonbreaking-hyphen spelling. Status, confidence and dimension values retain the previous prefix-recognition behavior; supplementary parenthetical text does not become part of those scalar values. The final document-field correction validates the complete key or bracketed-key segment, preserving separately delimited unlabeled annotations as described in section 10.

Explicit `revised-finding` and `original-finding` strings cannot create evidence, status, document, dimension or lineage fields. Even when a quoted replacement happens to match the source, serializing the replacement head cannot manufacture a fallback anchor. Repeated actual anchor fields, including duplicate `counter-anchor` / `anchor-counter` aliases, now raise a clear ambiguous-shape error rather than choosing one quote and overwriting both fields with it. Real duplicate finding IDs still fail the runner's uniqueness check.

## 6. A live critic's auxiliary references are not competing rulings

The subsequently completed raw Argument Architecture / Chen critic response, attempt `8ac1816319a7`, contains 36 unique ruling rows, followed by `### Must keep` references repeating five earlier IDs. The baseline parser treated those five references as additional ledger rows. `apply_rulings()` consequently raised a duplicate-ID error and the live checked job failed despite the absence of competing rulings in the requested ledger section.

The reviewed parser excludes the requested auxiliary sections—Must keep, Counter-evidence, Open questions, rejected rows and the check receipt—from finding/ruling rows. A later explicit Findings ledger heading resumes row collection. Raw model receipt strings and their full auxiliary tails are preserved; this is not deduplication of actual rulings. A regression runs the complete checked-reading path with repeated auxiliary references, verifies that the raw critic tail and the reading's open-question tail remain present, and still requires two conflicting ruling rows to raise an error.

Offline replay of that failed baseline attempt yields 25 reading rows, 36 critic rulings and 30 kept rows: 23 confirmed, two rejected, seven additions kept and four additions dropped by the anchor wall. This is a repaired replay of saved calls, **not** a completed live baseline job or an additional model result.

## 7. Saved-output compatibility review and fingerprint coverage

At the first review snapshot, six checked outputs had completed: Conditions of Possibility on Harris, Zambrana and Chen; Argument Architecture on Harris and Zambrana; and Inferential Commitment Mapper on Harris. Their six final outputs and twelve raw read/critic files covered 18 files and 536 retained row instances. After the deep-render correction, the replay expanded to all **nine completed checked outputs, 27 files and 767 retained row instances**, adding Commitment Mapper on Zambrana and Chen and Epistemological Method Detector on Zambrana. All nine recorded output hashes were checked. The earlier six-output evidence remains preserved in the scratch worktree with the `-before-deep-render` filename suffix.

The latest checked-output review covers **ten original completed outputs plus two separately recovered artifacts, 36 files and 1,020 retained row instances**. The tenth ordinary completion is Epistemological Method / Chen. The two additional files are the narrow auxiliary-section recoveries of Argument / Chen and Epistemological Method / Harris in [`auxiliary_recovery/20260905T045321.120955Z`](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/auxiliary_recovery/20260905T045321.120955Z/manifest.json). Their accepted manifest, transformation and output hashes were checked; they remain explicitly identified as separate recovery artifacts from failed live jobs. This broader repair replay reparses their text and original raw calls; it does not claim that the broad patch generated them or that changed prompt handoffs would receive the same model answers. The preceding nine-output evidence remains preserved with the `-before-recovered-artifacts` suffix.

The comparison checked each row's finding, primary anchor, document key, dimension, status, confidence, lineage and secondary anchors against the frozen baseline parser, then checked render/reparse/reverification. There were **zero unexplained field differences**. Intentional differences were the explicit Harris critic replacements, recognition of the previously ignored counter-anchor fields, and exclusion of one rejected F20 row from the Commitment Mapper's final auxiliary receipt section. The expanded snapshot also exposed three previously ignored `anchor‑b:` fields with nonbreaking hyphens in the Commitment/Zambrana critic, attempt `f6691e5f5042`, rows F10, F12 and F13; the existing scratch field-name normalization recognizes and checks those second quotations. Subsequent offline application also preserved each kept finding and anchor through serialization.

The recovery artifacts add expected exclusions of rejected-row receipts and repeated references in auxiliary sections. Two Chen / Argument critic additions, V.F9 and V.F11, explicitly declare `anchor: none`. The baseline instead extracted quoted critical questions from their finding heads as fallback anchors. The scratch parser retains an absent anchor; both additions were already dropped by the baseline membership wall. A regression confirms that even a source containing that quoted question cannot turn an explicitly absent anchor into declared evidence. Across the expanded checked set, there are still zero unexplained field differences or render/reparse failures. The subsequently accepted quoted-value grammar introduces 36 additional explained field changes across these saved views: ambiguous displayed quotation fields remain unverified, as detailed in section 10. The following table includes that final grammar.

| Completed checked output | Patched final rows verified | Declared anchors verified |
|---|---:|---:|
| Conditions / Harris | 30/30 | 35/35 |
| Conditions / Zambrana | 24/26 | 26/28 |
| Conditions / Chen | 31/31 | 31/31 |
| Argument / Harris | 35/35 | 35/35 |
| Argument / Zambrana | 26/35 | 26/35 |
| Commitment / Harris | 27/27 | 31/31 |
| Commitment / Zambrana | 23/24 | 26/27 |
| Commitment / Chen | 28/31 | 32/35 |
| Epistemological method / Zambrana | 23/24 | 23/24 |
| Epistemological method / Chen | 27/27 | 27/27 |
| Argument / Chen, narrow recovered artifact | 30/30 | 30/30 |
| Epistemological method / Harris, narrow recovered artifact | 27/28 | 30/31 |

These are membership checks on saved final text, not quality judgments. Argument / Zambrana F16 remains unverified. The raw Conditions / Zambrana critic still has five unmatched rows; the patch does not claim to resolve all quotation mismatches. The replay script and complete per-file field-change evidence are in the scratch worktree as `review_all_completed.py` and `review-replay-2026-09-05.json`. Recheck the expanded set, including real corpus outputs, before application after the baseline finishes.

The saved old-condition outputs were also checked: twelve final outputs and twelve raw responses, covering 608 retained row instances. All retained findings and metadata match the frozen parser, with no parser errors or render/reparse differences. The only row exclusions are the explicit Counter-evidence and Open questions sections of Commitment / Harris: CE1–CE6 and OQ1–OQ6, repeated in the final and raw response. Nine of those twelve auxiliary rows previously verified, so the finding-ledger count changes from 35 verified rows to 26. The soft-hyphen repair separately restores two old Argument / Harris quotations (25 to 27 verified) and one old Epistemological / Harris quotation (23 to 24). The new quoted-value grammar produces no additional changes in these old outputs. Evidence is retained as `review-old-output-quote-compat-2026-09-05.json`.

The study runner's `CODE_FILES` originally omitted `src/dossier/walls.py`, although its `normalize()` function changes anchor results and therefore the study. The reviewed patch adds that file to future study fingerprints. This hash expansion remains unapplied during the live run; do not rewrite the existing `plan.json` or its identity. The original normalizer hash is recorded above to retain the missing baseline evidence.

Several related limitations remain explicit. Ordinary rows with foreign executor keys absent from the source index retain the baseline's cross-source fallback; keys present in the index remain binding. Corpus rows remain stricter: every declared document key must exist, and foreign keys fail verification. Argument Architecture's `promised-at` / `nearest-delivery` answer shape contains two quotations, while the legacy fallback verifies only its first candidate. Ambiguous nested same-delimiter quotations are now visibly unverified under the accepted grammar in section 10; this is separate from intentional word-prefix trimming. Finally, serialized legacy outputs cannot retrospectively recover omitted trim history without replaying their raw calls. These are separate constraints on what the current wall result means; the patch neither infers quote support nor silently broadens those policies.

## 8. First real corpus result: intact input, incomplete source selection in synthesis

The completed Conditions / Deutschmann chain, attempt `aad753f7db72`, distinguishes pair preservation from adequate corpus coverage and complete quotation verification. Its [P6 extraction receipt](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/conditions_of_possibility_analyzer__deep__deutschmann/aad753f7db72/step-extract-path_dependence-.json) records twelve cross-document rows and 24 matched parsed anchor spans, with no wall-reported trimming or incomplete pairs. These counts do not establish that every complete displayed quotation was checked: the internal-quote limitation below occurs in these actual rows. The two distinct 2001 papers retain separate stable keys. The [corpus critic receipt](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/conditions_of_possibility_analyzer__deep__deutschmann/aad753f7db72/step-verify--.json) records fifteen rulings with thirty parsed anchors: fourteen rows and 29 spans verify, while one addition fails its primary quotation. One original finding is rejected, one weakened, and two additions survive, leaving thirteen paired rows for synthesis. Three verified rows require quotation trimming.

The saved [synthesis prompt](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/conditions_of_possibility_analyzer__deep__deutschmann/aad753f7db72/call-0029.prompt.json) contains all three complete source texts verbatim and exactly the 177 expected retained rows: 62 from the first document critic, 55 from the second, 47 from the third and thirteen from the corpus critic. Comparing those retained rows with the actual saved synthesis input finds no missing or extra IDs, finding/status/dimension/lineage changes, or anchor-pair changes. Ten of the thirteen corpus pairs involve the second 2001 paper. The user message is 312,065 characters; the [invocation receipt](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/conditions_of_possibility_analyzer__deep__deutschmann/aad753f7db72/call-0029.json) reports 68,093 input tokens and a complete output. The application wrapper's chunk threshold is 999,999,999 characters, and this backend passes system and user messages through unchanged. There is no observed application-side truncation or missing-document handoff.

Nevertheless, the [final reading](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__deep__deutschmann.md) has 28 primary anchors all assigned to the first 2001 paper. Only F15 retains a second anchor, from the 2022 paper, with valid lineage to P6.F9. The second 2001 paper disappears from final anchor coverage. Thus the final verifies 28 rows and 29 quotations but covers only two of three sources and retains only one corpus pair. This is a synthesis-selection failure on the recorded evidence, not a validated three-document genealogy merely because its membership score is 28/28. The parser cannot establish semantic coverage from valid quotations or lineage alone.

The scratch replay of this first completed chain covers 29 raw calls, four actual critic input ledgers, the actual synthesis input and rejected material, and the final output. The initial replay found 99 parsed-field differences, all from counter-anchor recognition. After the accepted quoted-value repair, the complete snapshot contains 152 field differences: counter-anchor recognition, complete decoding of JSON strings, and refusal of ambiguous displayed literals. There are no parser errors or render/reparse differences; its final membership counts remain 28/28 rows and 29/29 anchors. One retained document-level row, D4.DOC2.F5, has an unmatched counter-anchor in its extraction, critic input, critic output and synthesis input; the baseline counted only its primary quote. That gap does not explain the missing second document, since the synthesis received the other retained material from that document. Raw-to-handoff comparison also confirms lost trim history, including four shortened quotes in the first document critic's input. An unverified quote's existing `trimmed` flag can record an unsuccessful shortening attempt; only a verified shortened quotation demonstrates that the retained quote was actually reduced.

The read-only corpus evidence and comparison logic are retained in the scratch worktree as `review-corpus-replay-2026-09-05.json` and `review_corpus_completed.py`. They inspect actual saved prompts and outputs; no model response is treated as an answer to a hypothetical repaired handoff.

## 9. Second corpus: coverage retained, one incomplete descendant and contradictory auxiliary references

Conditions / Castoriadis, attempt `39cc121e535e`, sends all three complete sources and all 195 expected retained rows to [synthesis](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/conditions_of_possibility_analyzer__deep__castoriadis/39cc121e535e/call-0028.prompt.json): 63, 63 and 59 document rows plus ten P6 rows. No IDs, findings, scalar metadata or parsed anchor pairs disappear at this handoff. The corpus critic's five additions each supply only one anchor; the live wall correctly drops all five as incomplete pairs even though their individual anchor spans match.

The [final reading](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/conditions_of_possibility_analyzer__deep__castoriadis.md) covers all three documents, with primary-anchor counts 12, 10 and seven. F2 and F13 preserve distinct-document pairs. F8, however, descends from P6.F3 and retains only one document anchor. The lineage-aware process wall correctly flags F8 as incomplete: 28/29 rows pass despite 33/33 parsed anchor spans matching. This is a concrete reason to retain the process wall alongside standalone final-quote counts.

A separate live input defect occurs in the first document critic. Its [raw output](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/conditions_of_possibility_analyzer__deep__castoriadis/39cc121e535e/call-0024.md) contains 67 actual rulings followed by five positive “Must keep” references. The frozen deep runner parses the references as rows with failed anchors and assigns them to rejected material, while retaining their corresponding real rulings. Consequently D1.DOC1.F1, D4.DOC1.F6, D4.DOC1.F10, D5.DOC1.F1 and D5.DOC1.F10 appear in both the verified ledger and the synthesis prompt's rejected section. The existing scratch auxiliary-section fix prevents this contradiction. The deep-chain regression now checks that positive auxiliary references cannot leak into synthesis as rejected findings while raw critic receipts remain intact.

## 10. The accepted quoted-value grammar checks the complete displayed literal

The frozen anchor regular expression stops at an internal quotation mark, including a JSON-escaped ASCII quote. It can verify that prefix while leaving the remainder of the displayed quotation outside the checked span. Field tokenization alone does not fix this separate value-grammar problem.

Concrete corpus examples include Deutschmann P6.F2 and P6.F8 secondary anchors in call-0024, and Castoriadis P6.F4, P6.F5 and P6.F10 anchor slots in call-0023. Deutschmann P6.F2 checks the prefix `Simmel's paradoxical characterization of money as an` while leaving the quoted `absolute means` phrase and following text unchecked. The first two complete corpus inventories contain thirty and 52 distinct row/field/raw-value cases with quoted remainders; nine and 21 respectively are valid JSON strings. Repeated occurrences across raw responses and saved handoffs are recorded separately in the scratch evidence.

Implementation review accepted this bounded repair after examining the compatibility costs:

- Valid JSON anchor strings are decoded completely, including escaped internal double quotation marks and backslashes. Rendering replaces the complete original literal, preserving a trailing page annotation.
- A same-delimiter literal with unescaped inner quotation marks is ambiguous. Its displayed text and raw receipt are retained, but its parsed quotation is empty, the row remains unverified, and `quote-error:` (or its secondary equivalent) explains that JSON escaping is required. This is a nonfatal shape result eligible for the existing re-anchoring path.
- A successful replacement removes the obsolete diagnostic and becomes citable only after the normal document and quotation checks. Full fake deep-chain regressions cover both primary and secondary corpus anchor repair, including a model response that copies the stale diagnostic.
- The existing SourceIndex word-prefix shortening policy is unchanged. A refusal to parse an ambiguous literal is reported separately from deliberate shortening of a valid parsed quotation. No code infers what the author or critic meant by ambiguous punctuation.

A further concrete fixture exposed why literal decoding also needs a bounded trailer rule. In `anchor: "The source makes a claim "quoted — doc: invented" after the quotation" — doc: actual`, field tokenization cuts the anchor value at the exposed inner field, hiding the last quotation mark from the literal parser. The remaining bare word `quoted` is noncanonical. The final grammar allows punctuation and balanced parenthesized/bracketed citation trailers, plus explicit numeric `p.`/`pp.` page references; other bare text after a quoted literal produces a nonfatal parse diagnostic and stays eligible for re-anchoring. This retains the saved `(Rose, 1981: 214).` citation. It deliberately treats `“Essence must appear,” Hegel says (Hegel, 2010: 418).` as a noncanonical anchor value: put the attribution in another field or re-anchor it. No speaker name is special-cased. The actual Commitment / Deutschmann I4.DOC3.F2 value, beginning `"capitalism" is meant to make clear...`, is also now unverified instead of checking only the quoted word.

The adjacent fixture without `quoted` exposes either two primary `doc:` declarations or a single declaration containing unexplained quotation marks and prose. The final parser handles both nonfatally: normalize `counter-doc` / `doc-counter` aliases, require one declaration per anchor slot, and validate the complete key or `[key]` segment. The next existing row separator ends that segment; separately requested unlabeled slots such as `— drawn`, `— stopped` and `— presupposed in ...` remain intact. A pre-final inventory found 125 such separate annotation slots and preserved all of them. An attached parenthetical such as `doc: [paper] (supplied)` is noncanonical; `doc: [paper] — supplied` remains supported. Syntactically valid foreign executor keys retain the ordinary-row fallback, while corpus keys remain strict. Duplicate document declarations, malformed key segments and unexpected literal trailers do not become job exceptions. Their diagnostics use the existing per-anchor `quote-error` field and clear after a successful replacement of the quotation/document fields.

These rules specify supported literal and document-field shapes. They do not claim to interpret every ambiguous free-form row. Regression checks preserve raw text, reject the reported prefix bypasses, and exercise full re-anchor/render/reparse/desk recovery for primary and secondary corpus anchors.

The future anchoring instruction now says: “Write each anchor value as one JSON string, escaping internal double quotation marks and backslashes without changing the quoted text.” This prompt change remains in scratch; it has not changed any live baseline call.

The stricter handling lowers several saved-final membership counts. Conditions / Zambrana changes from 26 to 24 verified rows (F25 and F26). Argument / Zambrana changes from 34 to 26 (F10, F11, F17, F21, F23, F29 and F31 have ambiguous literals; F34 has a noncanonical bare attribution trailer; F16 already failed). Commitment / Chen changes from 30 to 28 (I2.F3 and a secondary anchor in I3.F18 become unverified; I3.F17 already failed). The other nine checked artifacts retain their preceding scratch membership counts. These reductions expose previously unchecked portions of displayed quotations, not new evidence that the associated findings are false.

Conditions / Deutschmann's final remains 28/28 rows and 29/29 anchors. Conditions / Castoriadis changes from the frozen lineage-aware result of 28/29 rows and 33/33 parsed spans to **25/29 rows and 29/33 anchors**: F4, F8, F18 and F23 have ambiguous displayed literals. F8 also retains its independent incomplete-corpus-pair failure. Across every saved response and handoff view, the first corpus has 45 ambiguous ASCII-literal instances and nine fully decoded JSON instances; the second has 85 and 38 respectively. Those are repeated view instances, not distinct findings.

All four corpus inventories are now complete. The final unapplied patch includes the accepted literal-trailer and document-field corrections, and the stable files have been supplied for the independent integration rehearsal.


## 11. Third corpus: three-document coverage, another incomplete descendant and malformed third anchors

Commitment / Deutschmann, attempt `ec8abd1d1bce`, supplies [synthesis](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/inferential_commitment_mapper__deep__deutschmann/ec8abd1d1bce/call-0030.prompt.json) with all three full sources and exactly 204 expected retained rows: 64, seventy and 58 document rows plus twelve X6 rows. The saved input has no missing or extra IDs, finding/scalar metadata changes, or parsed-anchor drift. Its user message is 312,442 characters, and the complete invocation receipt records 68,961 input tokens. All thirty final rows have lineage into the recorded input; none cites an unknown predecessor. There is no verified/rejected input overlap.

The [X6 extraction](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/inferential_commitment_mapper__deep__deutschmann/ec8abd1d1bce/step-extract-shared_score-.json) contains twelve rows with three doc-keyed anchors each. The frozen wall initially verifies nine rows and 33 of 36 parsed spans, with two trimmed rows. A re-anchor call replaces X6.F6, X6.F10 and X6.F12, after which all twelve rows pass the frozen wall. The accepted grammar exposes that the latter two replacements still contain ambiguous internal double quotation marks in their third-document anchors. The same literals survive in the [corpus critic](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/inferential_commitment_mapper__deep__deutschmann/ec8abd1d1bce/call-0029.md), which the repaired parser verifies as ten of twelve rows and 34 of 36 anchors. This is a limitation of the original re-anchoring outcome, not a missing document key or a claim about semantic support.

The [final reading](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__deep__deutschmann.md) retains all three sources, with primary-anchor counts fourteen, eleven and five, and eleven actual distinct-document pairs. F14 cites X6.F11 but keeps only its later-text anchor. The frozen lineage-aware wall correctly marks that descendant incomplete: **29/30 rows pass despite 44/44 parsed spans matching**. The accepted grammar additionally marks F11, F13 and F21 unverified, producing **26/30 rows and 41/44 anchors**. F11 is a particularly clear parser counterexample: the frozen wall accepted only the two-word prefix `The term` from a displayed sentence beginning `The term "capitalism"`.

A separate downstream check calls `analysis_ledger()` on that exact final text with the three actual sources. The frozen standalone verification does not receive upstream corpus IDs or the process wall, so it presents F14 as citable despite the recorded incomplete-pair failure. An initial quote-repair draft also made malformed-primary F11 disappear from the desk block because its parsed primary quote was empty; malformed-secondary F13 and F21 appeared with empty `near` slots. These concrete findings motivated an explicitly approved, bounded correction in `src/dossier/common.py`.

The corrected desk derives only the composer's encoded corpus namespaces from the operationalization: each corpus dimension uses `id_prefix` or its uppercase key, and corpus critic additions use `V.CORPUS`. It matches the exact namespace followed by a dot in row IDs and lineage, then passes those IDs into the existing pair wall. It does not infer corpus meaning from a finding or match a prefix inside an unrelated identifier. Thus F14 remains unverified even when its final dimension is `consequences`; valid paired descendants remain citable. Malformed primary and secondary quotations are visible in the unverified section with their document keys and the specific JSON-escaping diagnostic, including when the primary parsed span is empty. Raw final text is unchanged.

Regression cases cover real F14/F8-style descendants, a `V.CORPUS` descendant, direct corpus IDs, valid paired descendants, the uppercase-key fallback, unrelated similar prefixes, and ordinary foreign executor key compatibility. An additional read-only desk replay covers all 28 saved final texts: twelve old, ten original checked, two separate recovered artifacts and four completed corpora. It confirms that no previously visible retained finding becomes hidden; the only excluded rows are the twelve explicit old Harris auxiliary entries. The repaired handoff moves F14 and malformed F11/F13/F21 into the unverified section. This is a format-and-provenance correction; workflow document selection and receipt transport are outside this patch.

The complete third-chain review covers thirty raw calls and 37 saved views, with 55 explained field-change entries: 37 primary-quotation changes, seventeen secondary-quotation changes and one auxiliary-section exclusion. There are zero parser errors or render/reparse differences. The excluded reference repeats the critic's added V.DOC3.F1 in a Must keep section; it is not a competing ruling and does not create a verified/rejected overlap in this saved synthesis prompt. The evidence retains that distinction from the second corpus's actual contradictory input.


## 12. Fourth corpus and final compatibility inventory

Commitment / Castoriadis, attempt `233dc221ebd7`, sends all three complete source texts and exactly 224 expected retained rows to [synthesis](../../data/study/ideas_2026_09_05/374325c24e6b10a1/receipts/inferential_commitment_mapper__deep__castoriadis/233dc221ebd7/call-0028.prompt.json): 68, 74 and 75 document rows plus seven X6 rows. No IDs, findings, scalar metadata or parsed anchor pairs disappear from that handoff. The complete invocation records 76,622 input tokens; the user message contains 353,809 characters. There is no verified/rejected input overlap, and every final row has known lineage.

The X6 extraction supplies ten paired rows and twenty parsed spans. The frozen wall accepts all ten, while the repaired literal grammar flags X6.F7 and X6.F10, giving eight rows and eighteen complete anchors. The corpus critic supplies sixteen rows: ten rulings plus six additions. All six additions have only one anchor and are correctly dropped. X6.F4 is weakened but its ellipsis-containing replacement quote fails membership; X6.F6 is rejected despite matching anchors. X6.F8 writes a second primary `doc:` field where `doc-b:` is needed. It already fails the frozen pair/membership wall; the final repair explicitly reports duplicate-document ambiguity and does not silently choose a key. The seven retained X6 rows are present in the actual synthesis input.

The [final reading](../../data/study/ideas_2026_09_05/374325c24e6b10a1/outputs/inferential_commitment_mapper__deep__castoriadis.md) covers all three sources, with primary-anchor counts ten, nine and seven and eight actual distinct-document pairs. F10 cites X6.F10 but loses its second anchor. The frozen process wall correctly reports **25/26 rows despite 42/42 parsed spans**. F24 contains two ambiguous displayed quotations from the democracy text. The repaired grammar reports **24/26 rows and 40/42 anchors**, with F10 still incomplete and F24 unverified. The repaired standalone desk also retains the encoded corpus requirement for F10 and keeps F24 visible with diagnostics.

The complete corpus review covers **115 completed raw calls, 143 saved response/input/final views and 3,729 retained row instances**. It reports zero parser errors and zero render/reparse differences. Per-chain field-change entries are 152, 237, 55 and 73, respectively. They consist of supported counter-anchor recognition, complete JSON decoding, detected malformed quotation shapes, six auxiliary-reference exclusions across two critic views, and the one actual duplicated-document declaration in X6.F8. All final lineage checks pass; this does not establish that the final findings preserve enough corpus comparison or that their quotations support them.

| Corpus final | Frozen lineage-aware rows | Repaired rows | Repaired anchors | Sources with final anchors | Actual distinct-document pairs |
|---|---:|---:|---:|---:|---:|
| Conditions / Deutschmann | 28/28 | 28/28 | 29/29 | 2/3 | 1 |
| Conditions / Castoriadis | 28/29 | 25/29 | 29/33 | 3/3 | 2 |
| Commitment / Deutschmann | 29/30 | 26/30 | 41/44 | 3/3 | 11 |
| Commitment / Castoriadis | 25/26 | 24/26 | 40/42 | 3/3 | 8 |

Source and pair counts describe the saved final structure, not a semantic quality score. They must not be replaced by a single claim that the corpus path was fully validated.

The durable, ignored audit bundle is [`reader_notes/anchor_audit/20260905T064048.084131Z`](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/anchor_audit/20260905T064048.084131Z/README.md). It contains the final patch, reproducible scripts with configurable baseline/repaired worktree paths, current and historical JSON/stdout evidence, and a file-hash manifest. It removes dependence on `/tmp` surviving. The original saved study/source inputs remain separately preserved and are checked by their hashes. The scratch worktree remains intact for the combined-candidate review.

## Final patch, validation and application

The preserved standalone repair patch is [`reader_notes/anchor_repairs.patch`](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/anchor_repairs.patch), inside the ignored study directory. The final patch SHA-256 is `917de1d345a0db215434c59516c82b30d1f9c2b609d6f05a2bf74f42c49dc721` (73,634 bytes). The audited repair files include a bounded desk handoff correction and are in `/tmp/the-analyst-anchor-repairs-2026-09-05`, a detached worktree at `c195138`, and change only:

- `scripts/study_ideas_material.py` (future fingerprint coverage only)
- `src/dossier/walls.py`
- `src/dossier/common.py`
- `src/executor/ledger_walls.py`
- `src/executor/process_runner.py`
- `src/stages/process_composer.py`
- New `tests/test_anchor_repairs_2026_09_05.py`

Validation in that separate worktree after independent review, the deep-render correction, receipt disclosure, quoted-value repair, trailer/document-field validation and desk handoff correction: **161 tests passed** across the new repairs, corpus ledger, process shape, desks' handoff and ideas runner. Existing deprecation warnings remain. `git diff --check` and `git apply --check` against the main checkout passed. Those scratch audit steps made no paid calls and did not modify the live checkout. The subsequent integrated application is recorded below.

An offline replay from the original saved read and critic responses gives:

| Artifact | Rows verified | Anchors verified | Trimmed rows |
|---|---:|---:|---:|
| Original production checked ledger | 29/30 | 29/30 counted | Process receipt 3; serialized recheck 0 |
| Patched replay of original reading | 27/27 | 31/31 | 0 |
| Patched replay of original critic | 30/30 | 35/35 | 0 |
| Patched apply/render/reparse | 30/30 | 35/35 | 0 |

For the original Harris / Conditions case, the model's substantive ruling counts remain 24 confirmed, three weakened, zero rejected, three added; the formerly missing explicit rewrites now reach the findings. The side-by-side counts must remain labeled as baseline versus repaired offline replay.

After both the baseline and the bounded follow-up completed, root applied the integrated **combined v3** patch, which merges this repair with the four question revisions and corpus instruction. Its SHA-256 is `22ee7f9a833667443013244d34f26bb5d30a3aca4ccf91bd1e2b38d28caa9a43`; its [manifest](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/combined_integration_2026_09_05/v3/manifest.json) pins all eleven resulting files. Input pins matched immediately before application; `git apply --check` and all resulting file hashes passed. Do not apply the standalone repair on top of the integrated change.

A fresh main-checkout test run passed **186 tests** across the five focused files above and the existing prior-plumbing, dossier-table-wall and spine-wall suites. The recovery, aggregation and follow-up tools separately passed **13 guard tests**. Four definitions load with six dimensions. Existing deprecation warnings remain. Raw baseline/follow-up responses, their frozen walls and their identities have not been rewritten.

The four actual follow-up outputs were also reparsed under combined v3 as a separate, post-study observation. The [post-study wall audit](../../data/study/ideas_corpus_synthesis_followup_2026_09_05/d04d447a6d944d02/reader_notes/combined_v3_poststudy_walls.json) retains original frozen corpus ancestry and pins the candidate code. Conditions/Deutschmann remains 32/32 rows and 43/43 anchors; Commitment/Deutschmann remains 27/28 and 59/60. Conditions/Castoriadis changes from 29/30 to 23/30 rows and 38/38 to 31/38 anchors; Commitment/Castoriadis changes from 30/30 to 24/30 rows and 61/61 to 53/61 anchors. The new failures are malformed displayed quotation literals; matching-source coverage remains three of three in each case. These stricter counts are not substituted for the frozen experiment's metrics. They show why the original parser's high membership score overstated what it actually checked.


Two follow-up audit details limit interpretation further. Conditions/Castoriadis F26 has an unclosed quotation that hides its later document, confidence and lineage fields from the stricter tokenizer; the raw text remains intact and the row is explicitly unverified. An empty parsed missing-lineage list does not validate metadata that could not be parsed. Commitment/Deutschmann’s verified-trim count falls from one to zero because complete JSON decoding restores F4’s third quotation; F23’s third quotation also becomes fully matched, while its second remains unmatched after a shortening attempt. The report retains those field-level explanations rather than treating stable totals as byte-identical behavior.
