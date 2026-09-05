# Argument-family mechanical format audit — 2026-09-05

**Initial-stage audit complete: all 16 generation products and 24 raw calls audited. Corpus audit pending.** Campaign identity `530df62823ec1915b1a4a48472d4b59782e6017f92f9d5496a8c645c5836ad16`; runtime `af5861a`, candidate commit `aec1a7f`. The initial 16 single-paper/absence products precede a source-review gate; eight corpus products follow only after that gate. This audit reads saved generation artifacts and replays deterministic processing without provider calls. It does not inspect the independent Sonnet/Sol scores or substitute for the source-reading memos.

The [offline replay script](../../data/study/argument_family_2026_09_05/530df62823ec1915/reader_notes/format_audit/replay.py) denies network access, verifies the frozen harness/runtime/source bindings, and replays every audited complete generation product against its exact saved prompts, raw responses and process receipts. It writes only separate audit evidence. The [latest inventory](../../data/study/argument_family_2026_09_05/530df62823ec1915/reader_notes/format_audit/latest.json) points to a timestamped JSON snapshot and its SHA-256. The separately pinned [initial16 snapshot](../../data/study/argument_family_2026_09_05/530df62823ec1915/reader_notes/format_audit/initial16.json) has SHA-256 `9eaa5b6c306cbff961a9d5e02b52dd5405d4a62e6154ccb6265f0cad4e6232ce`; its [manifest](../../data/study/argument_family_2026_09_05/530df62823ec1915/reader_notes/format_audit/initial16_manifest.json) retains the exact script copy/hash. It was saved while all eight corpus jobs were still unstarted. All 16 exact replays and all raw/final render–reparse checks pass. Running and unstarted jobs are not assigned completed-result metrics.

## What the counts establish

Canonical JSON is a count of explicit supported quote/rewrite fields, separate from row completeness, quotation membership and interpretation. Valid JSON can encode an incorrect quotation. Row counts exclude auxiliary references such as Must keep; stored raw diagnostics remain preserved separately. A matching anchor certifies only the displayed retained substring. Quotes clipped to the length limit and further word-prefix recovery are distinct from malformed-literal refusal; raw lengths and trim flags are retained in the evidence.

Scope identities and the presence of a complete report are structural checks. Reported coverage is the reader/reviewer's assertion, not inspection inferred from file length. An explicit positive-row ruling is distinct from a supported scope assessment. Missing/unknown ruling IDs, carried rows, additions and unresolved references must not be counted as confirmations. A completed job can still contain inconclusive or unchecked scopes.

## Completed-product inventory

| Product | Retained rows matching / rows | Raw supported fields canonical / total | Scope report | Checking |
|---|---:|---:|---|---|
| Dialectical Structure, original Ganzinger | 23 / 24 | Sol 24 / 24 | Original capability condition has no scope contract | One call; F2 does not match |
| Dialectical Structure, candidate Ganzinger | 11 / 11 | Sol 8 / 8; critic 13 / 13 | All five identities; four findings-present, one inconclusive | 8 / 8 exact original-ID rulings; zero carried |
| Dialectical Structure, original Elling | 24 / 24 | Sol 24 / 24 | Original capability condition has no scope contract | One call |
| Dialectical Structure, candidate Elling | 9 / 9; 18 / 18 anchors | Sol 16 / 16; critic 18 / 18 | All five identities, findings-present but unchecked | 8 / 8 exact original-ID rulings; zero carried |
| Dialectical Structure, original Zambrana | 24 / 24 | Sol 24 / 24 | Original capability condition has no scope contract | One call |
| Dialectical Structure, candidate Zambrana | 12 / 12 | Sol 11 / 11; critic 12 / 12 | All five identities, inconclusive/unchecked after inherited reader errors | 11 / 11 exact original-ID rulings; zero carried |
| Dialectical Structure, original inventory control | 16 / 16 | Sol 16 / 16 | Original capability condition has no scope contract | One call; row count does not establish eligible instances |
| Dialectical Structure, candidate inventory control | 0 rows, 0 anchors | Sol 0 / 0; critic 0 / 0 | Five supported scoped negatives | Both calls occur despite empty ledger |
| Counterfactual, original Ganzinger | 22 / 22 | Sol 22 / 22 | Original capability condition has no scope contract | One call |
| Counterfactual, candidate Ganzinger | 8 / 9 | Sol 9 / 9; critic 9 / 9 | Four supported findings-present, one inconclusive | 9 / 9 exact original-ID rulings; F7 remains unverified |
| Counterfactual, original Elling | 22 / 22 | Sol 22 / 22 | Original capability condition has no scope contract | One call |
| Counterfactual, candidate Elling | 14 / 14; 19 / 19 anchors | Sol 17 / 17; critic 19 / 19 | Five supported findings-present scopes | 12 / 12 exact original-ID rulings; zero carried |
| Counterfactual, original Harris | 24 / 25 | Sol 25 / 25 | Original capability condition has no scope contract | F17 does not match |
| Counterfactual, candidate Harris | 12 / 12; 14 / 14 anchors | Sol 15 / 15; critic 20 / 20 | Four supported findings-present, one inconclusive | 13 / 13 exact-ID rulings, including four rejections |
| Counterfactual, original inventory control | 18 / 18 | Sol 18 / 18 | Original capability condition has no scope contract | One call |
| Counterfactual, candidate inventory control | 0 rows, 0 anchors | Sol 0 / 0; critic 0 / 0 | Five supported scoped negatives | Both calls occur despite empty ledger |

The candidate Ganzinger critic returns 12 rows: eight original rulings and four proposed additions. The quote-field denominator includes its explicit `revised-finding` string, so it exceeds the anchor count. Seven originals are confirmed, one weakened, none rejected; three additions survive and one fails its anchor. F8's explicit replacement is applied to the finding head and retained alongside its original wording. The preceding Sol prose is byte-identical after normal section-boundary trimming, and the final check receipt discloses that limitation. F9 and F10 carry explicit trim flags; both were critic additions whose long anchors were clipped. No malformed JSON literal or render–reparse field loss occurs in these audited products.

## Ganzinger: a partly supported scope becomes inconclusive

The [candidate critic](../../data/study/argument_family_2026_09_05/530df62823ec1915/receipts/dialectical_structure__candidate__ganzinger/f2096c717cc7/call-0002.md) declares `kind_of_opposition` supported with references `F3`, `F4` and `V.F1`. The first two remain correctly bound, quoted and retained in the [final ledger](../../data/study/argument_family_2026_09_05/530df62823ec1915/outputs/dialectical_structure__candidate__ganzinger.md). The proposed addition V.F1 fails: its quotation begins “Hegel’s philosophy as dualistic”, whereas the [source](../../data/study/sources_ideas/hegels_concept_of_the_concept_2026.txt) at line 104 names Kant's philosophy. This is incorrect quoted content inside valid JSON, not a parsing failure.

The runtime drops V.F1 and conservatively marks its dimension report inconclusive/unchecked. It detects both a failed anchor in that scope and an unresolved reference in the critic's reported finding list. **This is not an ID-remapping failure or loss of F3/F4.** Other additions map through explicit lineage: V.F2 → F9, V.F3 → F10, V.F4 → F11. The successful original rulings remain 8/8.

The diagnostic “Declared findings have no retained verified evidence” is too broad: this branch fires when **one or more** declared references lack retained evidence. It does not mean every finding in the dimension lacks support. The report also retains the critic's original basis and review explanation while explicitly marking them unchecked and listing the blocking issues. Consequently, a reader sees two valid ledger findings alongside an inconclusive assessment of the critic's broader three-finding scope. Treat this as a conservative scope/reporting limitation with imprecise wording; do not silently repair the frozen product or count the scope as wholly unsupported by source evidence.

## Elling: explicit row checking without completed scope reviews

The Dialectical Structure/Elling critic confirms all eight original rows by exact ID and adds one supported same-document pair. All 18 final anchors match. Its raw scope JSON nevertheless explicitly sets `review_state: unchecked` and an empty `review_basis` on every one of the five scopes. It updates one scope's basis and reference list to include the added practical-tension row, which is correctly remapped from V.F1 to F9.

The final therefore preserves five structurally valid `findings_present` reports while saying that they are not supported by completed scope reviews. This is the critic's submitted state, not discarded review metadata or missing IDs. Positive-row coverage is 8/8; scope-review support is 0/5. The runtime correctly keeps those distinct instead of inferring scope support from the confirmed rows. The unchanged initial prose and the disclosed added row remain separate surfaces.

## Zambrana: a repaired ledger retains earlier scope failures

Sol wraps every document key in Markdown backticks, for example ``doc: `zambrana2025_philosophy_in_the_severe_style_rose` ``. The frozen declared-document grammar accepts a plain key or `[key]`, not this wrapper. All 11 rows therefore receive `invalid document declaration` diagnostics before source matching, even though their 11 quotation literals are canonical JSON strings. Each of the five reader scope reports becomes inconclusive because its references lack verified evidence at that stage.

The critic removes those backticks, explicitly confirms all 11 original IDs, and adds one finding. The final ledger has 12 matching anchors and correct source keys. All five raw critic scope records expressly claim support within their stated scope with separate review reasons. Nevertheless, the final scope reports remain inconclusive/unchecked: the frozen implementation carries earlier `blocking_issues` forward even when the critic repairs the document declaration and supplies verified positive references.

This is persistent conservative scope state after successful ledger repair, not an ID-remapping failure or continued failure of the displayed final quotes. It cannot be read as evidence that the paper contains no relevant opposition, or that all final findings lack source support. The combination exposes a reporting limitation to assess after the frozen campaign; no parser or scope-policy change has been applied during the run.

## Empty control and an unsuccessful prefix search

The Dialectical Structure inventory candidate returns an empty ledger, and its critic still runs. Both calls supply all five expected scope records; the final retains five explicit supported negative reviews with criteria, inspected scope, basis and limits. The check receipt correctly says there were no original finding rows and points to the scope review. The generic row-coverage metric remains false for zero originals; it is not displayed as an incomplete 0/0 check. The original-capability condition instead emits 16 matching ledger rows. Source readers assess their eligibility and analytical value; membership alone does not establish that the control contains 16 relevant instances.

Counterfactual/Ganzinger F7 is a different failure from malformed JSON or a mistaken document key. The source quotation begins `[…] [w]e begin` and crosses a page footer between “some” and “sort” (source lines 451–457); Sol instead quotes a continuous sentence beginning “We begin”. DeepSeek confirms that same anchor as verbatim. The wall cannot verify it, and the final retains it explicitly unverified while marking its scope inconclusive. The original nine findings all receive exact-ID confirmations, so 9/9 ruling coverage does not imply 9/9 supported anchors.

F7 also bears `trimmed-anchor: yes` although its displayed quotation is unchanged. The flag records the attempted word-prefix search; no candidate prefix verified, so the original quotation remains. Count successful shortened matches separately from failed searches carrying a trim flag. Neither the flag nor the complete raw JSON string proves that the complete displayed quote matched.

## Harris: rejected prefixes return as additions, while prose keeps old IDs

The Counterfactual/Harris critic rejects F5, F7 and F11 because their supplied anchors are shortened rather than complete sentences. Those shortenings were already present in its actual input after the reader wall. It then proposes fuller quotations for additions V.F2 and V.F3 that substantially restate F7 and F11. Code applies the additions as F15 and F16 and repeats the existing quote-length/membership policy:

| Rejected row | New addition and final ID | Actual final anchor comparison |
|---|---|---|
| F7 | V.F2 → F15 | Identical 200-character prefix, ending “linked t” |
| F11 | V.F3 → F16 | Identical 118-character prefix, ending “insights from” |
| F5 | No replacement | Its 200-character prefix ending “which c” remains only in the rejected receipt |

F15/F16 retain lineage to V.F2/V.F3, not to F7/F11; code has not inferred that the rejected originals are revisions of those additions. The critic's requirement for whole sentences conflicts with the actual anchored-substring handoff, and its additions recreate the same prefixes. F4 is separately rejected for lacking an explicit conditional/if–then form. Whether its inferential counterexample qualifies is a semantic application of the candidate's eligibility criterion, assessed in the source memo.

The preceding prose and tables remain unchanged and still cite **F4, F5, F7 and F11**. Those IDs are absent from the retained ledger, although the rejected rows are available in the check-receipt section. The independent prose-versus-retained-ledger check finds all four references. The stored oneshot `missing_cited: []` field does not establish that these citations resolve: this runner path does not perform a prose-citation check. The final discloses that the prose was not revised; that disclosure does not reconcile the old citations or the analytical claims they support.

The fourth proposed addition V.F4 fails one of its two anchors, and the associated survival/robustness report becomes inconclusive despite its other retained findings. This is another instance of the conservative any-loss policy. No unknown-ID guessing, silent reanchoring or runtime alteration was used in this audit.

## Initial gate totals

| Mechanical measure | Original Sol reads | Candidate Sol reads | Candidate DeepSeek critics |
|---|---:|---:|---:|
| Completed raw calls | 8 | 8 | 8 |
| Parsed rows | 175 | 61 | 73 |
| Canonical / supported quotation-and-rewrite fields | 175 / 175 | 76 / 76 | 91 / 91 |
| Matching / parsed raw anchors | 173 / 175 | 64 / 76 | 87 / 90 |
| Raw anchors longer than 200 characters | 0 | 6 | 7 |
| Raw rows with a trim flag | 2 | 7 | 8 |
| Raw receipt cost USD | 0.439454 | 0.624220 | 0.316908 |

All **342/342** explicit supported fields are canonical JSON; there are no malformed or legacy quote literals, missing explicit quote fields, whole-ledger parse failures or render–reparse field losses. None of these initial decoded anchor values contains an embedded ASCII double quote, so this batch does not specifically exercise the escaped-inner-quote branch. The 11 rejected backtick document declarations are separate from quotation-literal compliance.

The 24 raw receipts total **USD1.380582**. Requested and used models match; reported retries are zero and there are no reported transport failures. All 24 `partial` and `stop_reason` fields are null: termination metadata remains unknown, not positively verified as untruncated. Stored raw quote diagnostics reproduce exactly.

Final original products have 173/175 matching rows and anchors. Final candidates have **66/67 matching rows and 82/83 matching anchors**, with 12 trim flags; the one retained unverified row is Counterfactual/Ganzinger F7. The critic rules on all **61 original candidate IDs**: 56 confirmed, one weakened, four rejected, **zero carried or unmatched original rulings**. Ten additions survive and two are dropped. This is complete ID/status coverage, not evidence that every ruling is substantively appropriate.

Every candidate preserves all five expected scope identities: **40/40** overall, comprising 22 findings-present, ten negative and eight inconclusive outcomes. Review states are **27 supported and 13 unchecked**. Five findings-present scopes are explicitly unchecked in DS/Elling; the other eight unchecked scopes are inconclusive. Both absence controls return no ledger rows and five explicit supported negative reviews each. Their comparison baselines return 16 and 18 anchored rows respectively; source memos assess whether those observations meet the method's eligibility criterion.

Mechanical replay supplies no reason to mutate or restart the frozen initial stage. The source gate must retain the reported limitations: partial scope support despite retained findings, persistent prior errors after repaired anchoring, an explicitly incomplete scope review, and inconsistent critic/prose behavior. Positive-row coverage and matching anchors do not certify checker reliability.

## Remaining corpus audit

Preserve raw and final views independently when a critic changes a quote, finding, ID or dimension.

For each later candidate corpus, inspect the actual 15 document extractions, one corpus extraction, three document critics, one corpus critic and final synthesis, plus every bounded re-anchor. Verify all 16 expected scopes and both document-keyed anchors on corpus rows/descendants. Compare source availability in synthesis inputs with final source representation; matching every displayed quote alone is not complete corpus coverage. Root retains the first source-content reading; this audit independently traces mechanical handoffs without changing receipts, products, runtime or candidate definitions.
