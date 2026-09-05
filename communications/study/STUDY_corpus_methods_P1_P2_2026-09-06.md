# P1/P2 corpus methods: build, source validation and release decision

2026-09-06 · Codex · owner's nine-task first queue, tracker §11 · validation cap USD 8

## Decision

**Neither method is ready to be offered.** Both now have loadable capability definitions, operationalizations and useful corpus outputs. The release barrier is the promised source-to-table contract, not lack of an interesting reading. P1 repeats a consequential causal overstatement on the natural pair and loses required source pairs in its conceptual control. P2 produces strong reconciliations but misses relevant control evidence, over-aligns different kinds of state maneuver, invents dimension keys, and leaves rejected citations in its checked tables.

| Method | What works | What prevents release |
|---|---|---|
| **P1 — Compare supplied cases** | Distinguishes sources, case complexes and nested actors; builds an actual case × criterion matrix; preserves exceptions and unavailable outcomes; treats Castoriadis as conceptual approaches. | PEACE inherits EMA's post-exclusion causal status; four Castoriadis findings fail the corpus/lineage wall; some detailed cells cite findings that support only part of their content. |
| **P2 — Reconcile sources on shared questions** | Aligns substantive answers and warrants; distinguishes qualification from contradiction; names source coverage without equating recurrence with consensus; preserves unresolved questions. | Castoriadis's 1990 robotization passage is missed; alliance-linked industrial engagement is over-aligned with France's selective nonalignment; both deep outputs use undeclared dimension names; checked pair tables retain three rejected IDs. |

No new purpose group or positive offer has been registered. The YAMLs remain available to the capability registry for research. Both keys are explicitly excluded from the dossier picker, its “More” fallback, its planning catalog and normal path resolution. This required a small catalog fix: previously `excluded` supplied reasons but did not suppress arbitrary capability keys. Merely omitting these YAMLs from purpose groups would have auto-offered them. Other eligible methods remain available; the four active definitions and Claude's S1/E8/T1 definitions were not changed.

Accounted cost is **$4.706588**, with **$0.952596** still reserved for a failed stream whose usage is unknown: **$5.659184 conservative total**, below $8. There were six completed outputs, twelve valid independent scores and two failed provider attempts. No additional spend is proposed here.

## Built and frozen

Designs: [P1](REDESIGN_compare_supplied_cases_2026-09-06.md), [P2](REDESIGN_reconcile_sources_2026-09-06.md). Each specifies the ideal output, preserved catalogue questions, dimension questions and answer shapes, method cards, corpus scope, reader-order synthesis and desk consumption.

Definitions: [P1 capability](../../src/engines/capability_definitions/compare_supplied_cases.yaml), [P1 process](../../src/operationalizations/definitions/compare_supplied_cases.yaml), [P2 capability](../../src/engines/capability_definitions/reconcile_sources.yaml), [P2 process](../../src/operationalizations/definitions/reconcile_sources.yaml). The legacy `comparative_framework` and `thematic_synthesis` definitions are unchanged. P1 preserves entity alignment, criteria, matrices, similarities/differences, cultural/translation limits and exceptions. P2 preserves substantive themes and their prevalence, common questions, consensus, qualifications, contradictions and unavailable answers.

Each process has three document dimensions and one corpus dimension. P1 inventories identity, answers and limits, then builds `case_matrix`; P2 inventories questions, answers and limits, then builds `question_reconciliation`. Corpus dimensions consume the per-document inventories; corpus checking and synthesis receive the full named sources. Modes are surface `oneshot`, standard `oneshot_checked`, deep `dvs`, with Luna extraction, DeepSeek V4 Pro checking and Sol synthesis. The existing workflow adapter supplies source identity keys. The runner invokes corpus dimensions only for more than one document.

The design, capability/process YAMLs, runtime prompt/runner/wall inputs, complete source bytes, routing, rubric, prices and campaign were hash-frozen at commit `9acf7ec`, **before generation and scores**. Freeze identity:

`b579cfa49898ebac8fcad175fd168335f708ed75cc0af400bd9c7062932aa0a2`

Every paid invocation checked these hashes. No substantive prompt or method changes were made after seeing outputs. A documented transport amendment increased DeepSeek's output allowance from 18,000 to 32,000 tokens after the first verification exhausted its allowance, including 12,952 reasoning tokens. It changed capacity, not questions, models, sources or rubric. Complete saved invocations were replayed only after exact prompt/model/label hash matches; failed partial outputs were never accepted as products.

All six source-read memos were committed at `d6c798b` before the first score. Each score binds the exact final-output and prior-memo hashes. The [baseline source reading](corpus_methods_P1_P2_2026_09_06/source_read_baseline.md) and six memos describe targeted manual passage checks, not exhaustive human rereading. Each judge independently received the complete sources and one output, without another output, another score or generation-model identity. The original rubric was unchanged; there were no head-to-head comparisons or order-based wins.

## Outputs and costs

“Standard” here means the final checked output. Its original strong-call reading is also archived, but was not separately scored. Run time includes failed attempts and recovery where relevant; independent jobs overlapped, so these times are not additive elapsed session time.

| Output and pre-score memo | Paid generation calls | Generation, known USD | Both judges, USD | Run minutes |
|---|---:|---:|---:|---:|
| [P1 deep, AUKUS/subsea](corpus_methods_P1_P2_2026_09_06/outputs/P1__deep__pair.md) · [memo](corpus_methods_P1_P2_2026_09_06/P1__deep__pair.md) | 14 | 0.546551 | 0.309428 | 16.64 |
| [P1 deep, Castoriadis](corpus_methods_P1_P2_2026_09_06/outputs/P1__deep__castoriadis.md) · [memo](corpus_methods_P1_P2_2026_09_06/P1__deep__castoriadis.md) | 19 | 0.595620* | 0.353926 | 18.33 |
| [P1 standard, AUKUS/subsea](corpus_methods_P1_P2_2026_09_06/outputs/P1__standard__pair.md) · [memo](corpus_methods_P1_P2_2026_09_06/P1__standard__pair.md) | 2 | 0.254448 | 0.286196 | 3.14 |
| [P2 deep, Deutschmann](corpus_methods_P1_P2_2026_09_06/outputs/P2__deep__deutschmann.md) · [memo](corpus_methods_P1_P2_2026_09_06/P2__deep__deutschmann.md) | 16 | 0.509521 | 0.305534 | 19.80 |
| [P2 deep, Castoriadis](corpus_methods_P1_P2_2026_09_06/outputs/P2__deep__castoriadis.md) · [memo](corpus_methods_P1_P2_2026_09_06/P2__deep__castoriadis.md) | 19 | 0.587365 | 0.367448 | 17.18 |
| [P2 standard, AUKUS/subsea](corpus_methods_P1_P2_2026_09_06/outputs/P2__standard__pair.md) · [memo](corpus_methods_P1_P2_2026_09_06/P2__standard__pair.md) | 2 | 0.292757 | 0.297794 | 4.11 |
| **Total** | **72** | **2.786262** | **1.920326** | — |

*P1 Castoriadis also retains the full **$0.952596 unknown-cost reservation**. Its first Sol synthesis stream ended without usage/completion metadata. The partial text was preserved, then only the failed synthesis was repeated ($0.198586, 80.5 seconds). P1 pair's failed DeepSeek verification is included in its known cost ($0.065429). The 72 generation invocations include ten ordinary runner re-anchoring calls and both failures; twelve judging calls bring the total to 84, of which 82 completed. Exact receipts are in [calls.json](corpus_methods_P1_P2_2026_09_06/calls.json).

Accounting uses the larger of provider-reported cost and repository list-price token accounting, with a conservative input/output reservation admitted under one shared lock. Unknown costs remain fully reserved. This is a budget ledger, not a reconciled invoice. OpenRouter's reported-cost subtotal excludes Anthropic and the unknown call, so it is not the campaign total. Paid activity ran from **01:03:45 to 01:52:59 Singapore time on September 6**, approximately 49.2 minutes including intervening review and recovery. Source bytes were not truncated to save cost.

## What the comparison got right and wrong

### P1: natural two-paper pair

The deep matrix distinguishes AUKUS, Chinese and US SeaMeWe-6 strategies, France–ASN, and associated Australian/Japanese/Korean activity. It preserves the difference between announced financing, procurement decisions and realized capability. France's 80% acquisition for EUR350 million is treated as an intervention, not proof of long-run profitability or resilience. Japan and South Korea are not promoted into formal AUKUS members. Missing outcomes and non-equivalent effectiveness measures remain visible; there is no unsupported overall ranking. The checked matrix is more compact, using three case complexes instead of seven subrows.

**The consequential error appears in both modes:** the analyses group PEACE and EMA as responses to exclusion from SeaMeWe-6. The source presents PEACE as another route, but expressly attributes the post-exclusion/direct-reaction status to **EMA**. Parallel infrastructure supports the broader duplication claim; that does not transfer EMA's causal chronology to PEACE. This was identified in both pre-score memos and independently by Sol. Sonnet did not catch it.

Cell evidence is also uneven. In the checked output, France's concrete acquisition terms cite F6's generic strategy typology, while the AUKUS delay cell cites F9's scope exclusion about regional conflict. The sources contain the underlying facts, but those findings cannot carry those cells unaided. Deep P1 also underuses the AUKUS source's specific Title III domestic-source eligibility, export licensing, export finance and venture-capital mechanisms in its instruments comparison. Its seven-row expansion duplicates some Japanese material and makes the commissioned pair less compact.

**Desk value:** the source-to-case map, actor separation, criterion headings and comparability/exception table are useful drafts. Correct EMA's causal attribution and give concrete cells their own supporting findings before lifting them as evidence.

### P1: Castoriadis three-case control

The output correctly compares approaches—technique, democracy and capitalist rationality. It retains narrow technical efficiency, real liberties under liberal oligarchy, capitalism's productive capacity, genuine consumer markets in the democratic alternative and unresolved institutional scale. Cultural meanings and non-comparable quantities limit the comparison without becoming a fictional ranking of three societies.

The final synthesizer breaks the evidence contract after successful checking. F2/F3/F4 are single-source definitions labeled as corpus `case_matrix` findings. F17 retains corpus lineage `CM.F2` but only a Democracy anchor. All their quotations occur, yet four rows correctly fail the requirement for two distinct source keys. The matrix's first column and its scale-limit row cite these incomplete findings. Several other cells combine more propositions than the quoted finding supports: F10 anchors consumer sovereignty but also carries self-management and allocation; F14 anchors unemployment but its matrix cell also reports theoretical incoherence, precarious work and rising profits.

**Desk value:** a useful three-by-five conceptual matrix and qualified exception tests, requiring correctly scoped findings and granular evidence before release. Corpus passage occurrence alone would have concealed the four broken rows.

## What the reconciliation got right and wrong

### P2: Deutschmann

The six-question table preserves each source's answer about religious character, money, growth, innovation, the myth cycle and response. It distinguishes capitalism's religious functions from theological equivalence; the two 2001 texts already qualify the analogy, while 2022 makes particular limits explicit. There is no invented same-year order or wholesale later reversal. The theme table correctly includes 2022's money-as-absolute-means passage and distinguishes **3/3 discussion** of myths/imaginations from the **2/3 detailed shared mechanism** in 2001. Different levels of growth explanation are not forced into contradiction.

Two qualifications need tightening. The 2001 Promise article already rejects new utopias and calls for disillusionment; 2022's more explicit containment proposal should not imply that rejection of a replacement promise is new. The synthesis also connects different growth explanations into a more integrated causal account than the aligned cells establish; that reconstruction needs an explicit inference label. The final ledger introduces undeclared `source_position` and `theme_coverage` dimensions. Their anchors happen to cover the sources here, but these names are outside the frozen contract. Composite source summaries are not always fully supported by the displayed quote.

**Desk value:** the question-reconciliation and theme-coverage tables are strong editorial drafts. Preserve the 2001/2022 continuity and separate documented agreement from an analyst's reconstruction.

### P2: Castoriadis

The six relations preserve proposition-level agreement on capitalist technology's direction and pseudomarkets; distinguish workplace transformation from economy-wide allocation; and retain implementation limits. Anti-formalism is explicitly qualified because political equality, technical non-neutrality and quantitative rationality evaluate different objects. Consumer sovereignty and genuine markets remain visible; the output does not equate capitalist-market criticism with rejection of every market.

**A missed passage matters.** Sol identified the 1990 text's statement that increasing robotization is capitalism's response to contradictions inside the enterprise. A post-score source check confirms the passage and its qualification: robotization defers or displaces the problem into nonrobotized parts. The table's “insufficient retained evidence” cell is honest about the extraction, but the supplied source contains a relevant answer that should be reconciled as a qualification/different scope. It is not proof of whole-source silence, and our pre-score review missed this opportunity too. The repeated undeclared dimensions and compressed anchors remain additional contract defects.

**Desk value:** the agreement/qualification structure and coverage table are useful, with the robotization answer restored and its scope distinguished from the broader historical thesis of the other two texts.

### P2: checked pair

The one strong call already supplies a substantive reconciliation. It distinguishes AUKUS's beneficiary formation from subsea's intervention effectiveness, and correctly observes that delivery failure would not itself disprove a thesis about state transformation. It leaves the relationship between the two frameworks unresolved instead of claiming a demonstrated integrated theory.

The autonomy relation overreaches. Japan/Korea leveraging defence industries to engage with AUKUS does not establish the same kind of autonomous positioning as France's selective participation across US and Chinese projects. Sol flagged this; rereading the cited source supports **different scope**, not the table's stronger common answer about maneuver beyond bloc discipline.

Checking creates a separate, code-verifiable failure. F11/F13/F14 are rejected and related replacements become F19/F20/F21, but the original tables and prose retain the rejected IDs. Replacement lineage does not resolve the old citations. Both tables therefore need revision after the applied ledger. The receipt reports this correctly; Sonnet nevertheless calls the output coherent and liftable, while Sol notices the problem but still gives high usefulness.

**Desk value:** the interpretive organization is useful; the final checked tables are not a consistent evidence handoff.

## Mechanical verification and actual desk consumption

All 173 individual anchor strings across the six outputs match after the existing normalization/trimming rules. **That does not mean every row is valid or every quote entails the whole claim.** The offline audit also expands final F-number lists/ranges, checks declared dimension IDs, and sends each actual output through `analysis_ledger` with the real `Document.key` values. [audit.json](corpus_methods_P1_P2_2026_09_06/audit.json) records both production checks and the actual citable desk IDs; the six desk inputs are archived under [desk_ledgers](corpus_methods_P1_P2_2026_09_06/desk_ledgers/).

| Output | Matching anchors | Production valid rows | Citable desk rows | Trimmed rows | Principal mechanical problem |
|---|---:|---:|---:|---:|---|
| P1 deep pair | 30/30 | 27/27 | 27/27 | 3 | No missing IDs; semantic/cell-support errors remain. |
| P1 deep Castoriadis | 27/27 | 14/18 | 14/18 | 1 | F2/F3/F4/F17 incomplete corpus evidence, cited in tables. |
| P1 checked pair | 20/20 | 17/17 | 16/17 | 5 | Added single-source F17 inherits `V.CORPUS` lineage. |
| P2 deep Deutschmann | 35/35 | 15/15 | 15/15 | 0 | Undeclared `source_position`, `theme_coverage`. |
| P2 deep Castoriadis | 36/36 | 20/20 | 20/20 | 0 | Same undeclared dimensions; relevant answer missed. |
| P2 checked pair | 25/25 | 18/18 | 15/18 | 3 | Tables cite rejected F11/F13/F14; single-source additions F16/F17/F18 inherit corpus lineage. |

The checked-mode desk discrepancy is partly conservative plumbing, not fabricated quotations. The corpus-wide critic can add a legitimate single-source finding under `V.CORPUS`; the desk then treats that lineage as requiring two source anchors. Call scope and finding scope need distinct identity handling. Conversely, P1's deep control really does label single-source rows as corpus findings or retain corpus lineage without the paired evidence.

Every original critic input received an explicit ruling: 38, 54, 16, 55, 52 and 15 rows respectively in the table's order. Deutschmann's receipt additionally flags one unexpected non-added ID; its complete disposition count should not be confused with an entirely clean receipt. Scope outcomes across the six runs are **8 findings-present and 43 inconclusive**, with no certified negative/silence outcome. Missing or malformed scope references remain inconclusive; a finished final ledger does not retroactively repair an earlier scope record. The model sometimes supplies an overly substantive explanation for a technical record failure, so those explanations also require review.

The existing mixed-scope control (`archive_inventory`, `archive_policy`, `archive_fragment`) was reused **without paid calls**. Both methods and both deep/checked runners preserve a positive policy answer, a bounded negative inventory assessment and an inconclusive fragment through the real runner and desk interfaces. Separate two-/three-document tests reject missing pairs, same-key pairs, wrong keys and invented third anchors. These fixtures validate plumbing; they do not establish new model performance on archive material. No paid spine/table/figure desk generation was commissioned; “desk value” above is based on source review, actual ledger handoff and offline controls.

## Independent rubric scores and their limits

Six scores, 1–10, higher always better: **S** specificity, **A** anchoring, **N** non-obviousness, **C** coherence, **U** usefulness, **H** safety from hallucination. Means are descriptive, not a release threshold. Complete source-specific reasons, decisive-error claims and memo bindings are preserved in [scores.json](corpus_methods_P1_P2_2026_09_06/scores.json).

| Output | Judge | S | A | N | C | U | H | Mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| P1 deep pair | Sonnet | 7 | 7 | 7 | 7 | 7 | 7 | 7.00 |
| P1 deep pair | Sol | 9 | 8 | 8 | 7 | 9 | 6 | 7.83 |
| P1 deep Castoriadis | Sonnet | 8 | 7 | 8 | 7 | 7 | 7 | 7.33 |
| P1 deep Castoriadis | Sol | 9 | 9 | 8 | 7 | 8 | 7 | 8.00 |
| P1 checked pair | Sonnet | 8 | 7 | 8 | 7 | 8 | 7 | 7.50 |
| P1 checked pair | Sol | 9 | 8 | 9 | 7 | 9 | 8 | 8.33 |
| P2 deep Deutschmann | Sonnet | 8 | 7 | 7 | 8 | 8 | 8 | 7.67 |
| P2 deep Deutschmann | Sol | 9 | 8 | 9 | 6 | 8 | 4 | 7.33 |
| P2 deep Castoriadis | Sonnet | 8 | 7 | 7 | 8 | 8 | 7 | 7.50 |
| P2 deep Castoriadis | Sol | 9 | 8 | 8 | 6 | 8 | 6 | 7.50 |
| P2 checked pair | Sonnet | 8 | 7 | 7 | 7 | 8 | 7 | 7.33 |
| P2 checked pair | Sol | 9 | 9 | 9 | 8 | 9 | 8 | 8.67 |

Three lessons constrain interpretation of these scores:

1. Sol independently caught PEACE/EMA, the missed robotization passage and the autonomy over-alignment; source rechecks substantiate those concerns. Sonnet's positive reading is useful evidence of quality but did not detect those defects.
2. Sol repeatedly calls the review records and provenance IDs invented because they are absent from the scholarly sources. **That diagnosis is wrong as stated:** those records exist in the saved execution receipts. The scoring prompt hid the check receipt/model identity but left scope material visible without supplying the complete process record. This confounds source judgment with evaluation of provenance. Raw scores stand; no favorable rescoring was purchased. Reader-facing audit verbosity and occasional reinterpretation of a technical failure are real weaknesses, but the existence of the audit record is not fabricated.
3. Neither scores nor quote occurrence establish the full desk contract. High usefulness scores coexist with incomplete corpus rows and dangling citations. Independent calls remove head-to-head position effects; they do not make Sol independent of the generating model family or make either judge infallible.

Both [unchecked P1](corpus_methods_P1_P2_2026_09_06/unchecked_oneshots/P1__standard__pair.md) and [unchecked P2](corpus_methods_P1_P2_2026_09_06/unchecked_oneshots/P2__standard__pair.md) already answer their main task in about 74 seconds ($0.162516 and $0.167564 respectively). Checking adds roughly 114 and 172 seconds. On this pair, the chain is not demonstrated to be necessary for substantive understanding; P1's causal error persists in both modes, and P2 checking breaks references despite useful additions. Pure oneshots were not independently scored and P2 has no deep run on this pair, so these observations are not a controlled estimate of a quality gain or loss from chaining.

## What is missing before offering

A subsequent revision should retain these question sets while repairing the evidence handoff:

- Give each populated cell findings that carry the whole answer; let the model narrow claims, add warranted passages and distinguish genuinely aligned answers. Correct PEACE/EMA and the autonomy relation, and retain the 1990 robotization qualification.
- Preserve declared dimension and source IDs through synthesis. Keep single-document findings in document scope; require distinct-source pairs on corpus claims and preserve all claimed-source anchors. Distinguish a corpus critic call from an individual added finding's scope. Code should check IDs and anchors, while the model decides meaning and equivalence.
- Reconcile prose/tables to the applied checked ledger so rejected IDs disappear or are explicitly replaced after model judgment. A replacement is not automatically semantically interchangeable with a rejected claim.
- Repair scope-record references and expose compact, bounded statuses without turning a failed extraction into source silence. Revalidate the revised frozen methods on the failed natural/control cases and check the actual desk handoff before adding a purpose offer.

These are documented missing conditions, not unvalidated fixes silently applied to the scored design. The release choice follows the pre-frozen requirement that every offered positive cell retain valid evidence and that decisive source errors withhold release.

Validation: **88 tests passed** across the P1/P2 suite, corpus ledger walls, workflow corpus dispatch and brief/catalog checks. The catalog tests cover positive purpose entries, the “More” fallback, recipes and direct normal path rejection for excluded methods. Only existing deprecation warnings remain. Designs, definitions, recovery/scoring/audit scripts, source memos, outputs, scores and receipts are committed by phase; the [validation manifest](corpus_methods_P1_P2_2026_09_06/validation.json) records hashes, routing, budget and run lineage. Full source texts and paid prompt/raw-call artifacts remain in the ignored local campaign directory.
