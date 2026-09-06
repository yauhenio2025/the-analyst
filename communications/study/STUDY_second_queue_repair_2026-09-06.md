# Second queue repair and release under the first-queue standard

2026-09-06 · Codex · tracker §11 · USD10 guidance, not an admission gate.

**Released all eleven second-queue methods and P2 (`reconcile_sources`). P1 stays withheld.** The measured record is in [the repair archive](second_queue_repair_2026_09_06/). No score is used in place of a source read. The owner’s standard supersedes the earlier requirement that every consequential cell carry a complete local evidence package.

## Standard and scope

Release requires verified retained anchors, no unverified or rejected evidence treated as valid in table cells, no fabricated finding or surviving attribution reversal in the source read, and a Sonnet mean at least equal to the original-question mean on the same paper where available. A6, C1, E12 and S3 are inventories, judged by rows, anchors and source fidelity rather than the reading/novelty rubric alone. The desks continue to decide citability row by row. An incomplete local quotation is not itself a fabricated claim when the full source supplies the claimed content.

All eleven methods use the same paper or natural pair as the first-round comparison, production checked mode for the eight single-paper methods and dvs for G2–G4. A3 and S3 receive one bounded final repair on those same papers after the first repaired-output checks identify the specific remaining defects below. The [protocol](PROTOCOL_second_queue_repair_2026-09-06.md) and [frozen plan](second_queue_repair_2026_09_06/plan.json) record the selected material and unchanged model routes. These are defect-focused checks, not held-out generalization tests. No original reading was regenerated, and no protected questions or P1/P2 definitions were edited.

## Shared repair and propagation

Commit `1bda5ff` strengthens `ANCHORING_LAW` and `check_anchors_in_context`: the quote must carry the finding’s actor and predicate, including its object and necessary qualification; separate spans are required when one cannot do so. The critic must re-anchor or reject a verbatim prefix that omits the asserted predicate. The ledger heading and row grammar are unchanged. The 68-prompt hash fixture was deliberately refreshed in the same commit, not treated as accidental snapshot drift.

The runner now preserves a critic’s fuller confirmed anchor even if the original fragment already matched. Checked methods with declared synthesis tables send their actual reading to the critic and run the existing `reconcile_checked` synthesis against the applied ledger. The model rewrites or drops affected cells, and the existing bounded wall checks anchors and IDs. No semantic heuristic was added. All eleven methods declare tables; none needs a table-free exemption. Table-free single-document methods retain the existing two-call prose/receipt behavior. Corpus deep mode already synthesizes after verification.

[Claude’s review](second_queue_repair_2026_09_06/CLAUDE_runner_review.md) approved with one confirmed action item: remove corpus-specific two-key repair wording from one-document repairs. That was fixed using the actual source count, with a regression. Two other tentative items were withdrawn in the review itself. [Disposition and review accounting](second_queue_repair_2026_09_06/CLAUDE_review_disposition.md). The focused suite after the correction passed 226 tests.

## Method repairs

Commit `24623d9` adds the [recorded cards and briefs](second_queue_repair_2026_09_06/repairs.json). Analytical questions are unchanged: the memos implicated execution and evidence selection, not the questions themselves.

- A6 gives each example its own finding and preserves literal conditional spans.
- C1 separates senses and contrasts, retaining attribution and complete dependence predicates.
- E12 retains granular construction evidence when deduplicating.
- S3 preserves temporal conditions and attributed voices.
- A3 requires separate literal spans, complete alternatives, and warranted necessary/sufficient criteria.
- A4/A5 preserve attribution, strongest alternatives, modality and final-table consequences.
- C6 assigns a within-article framework comparison to document-level relations.
- G2/G3/G4 inspect the earlier positive claim, align comparable concepts and retain earlier qualifications before naming change.

The law is guidance to the models, not a semantic guarantee. Source memos disclose remaining short packets even where the claims are supported and eligible for release under the owner’s standard.

## Validation record

The ten initially completed outputs and their source reads were committed in `3df89d0`; G4’s source read was already committed in `d6b128f`. G3’s final source read and the complete generation record were committed in `3f3b0be`, before either rater scored any repaired output. A3 had no first-round Sonnet original rating: the unchanged original and its already committed source memo were bound by a separate manifest, then rated once at **7.67**. This supplemental comparator is explicitly distinguished from the frozen first-round scores; no original reading was regenerated.

G3 encountered two provider-limit failures at the same religion2022 verifier: the first response was empty after 32,000 reasoning tokens; the first continuation produced a partial review and stopped at 32,000 total output tokens. Both were refused and preserved, with costs. Commit `655dca8` records a second continuation raising only that verifier’s study allowance to 48,000 tokens. The source, prompt hash, model, low reasoning effort and production dvs mode are unchanged; the twelve completed earlier calls replay locally, and all following calls retain the original allowances. The verifier completed with 37,935 output tokens; the following corpus verifier and synthesis completed with the original allowances. This is a disclosed token-limit amendment, not a different method condition.

The first pass completed all eleven outputs and 22 ratings for USD6.382102, plus the USD0.130737 direct Claude review. The [post-score source adjudication](second_queue_repair_2026_09_06/post_score_source_adjudication.md) preserves two necessary corrections: S3’s ending sequence is factually reversed in its table, and A3’s 7.50 Sonnet mean falls below its unchanged original’s 7.67 while omitting a consequential venture-capital comparison. The pre-score memos and ratings remain unchanged; the S3 miss is explicitly acknowledged.

Commit `ff0d1e7` strengthens only these two cards/briefs and freezes one additional checked run each on the same papers. S3 must distinguish source paragraph order from the analyst’s own concluding question. A3 must inventory application-level financial and institutional comparisons as well as headline classifications. No questions, source papers, routes, originals, runner or walls change. The [bounded final-repair manifest](second_queue_repair_2026_09_06/final_repairs/manifest.json) declares one new generation each and one independent rating per rater, with source memos first. The [first-pass audit](second_queue_repair_2026_09_06/first_pass_audit.json) and all first-pass scores remain preserved.

The final A3/S3 source memos were committed in `778790a` before their four independent ratings. A3's final Sonnet mean is **8.00**, above the unchanged original's 7.67; S3's false ending sequence is cured in both prose and the actual table. Both final source reads find no fabricated finding or surviving attribution reversal. Their first outputs and scores remain in the archive and are not the selected release artifacts.

| Method | Paper / pair | Rows / anchors | Trimmed rows | Sonnet | Sol | Original Sonnet | Decision |
|---|---|---:|---:|---:|---:|---:|---|
| [G2](second_queue_repair_2026_09_06/source_memos/G2__dvs__technique_rationality.md) | Technique / Rationality | 23 / 32 | 0 | 7.67 | 7.00 | — | Release |
| [G3](second_queue_repair_2026_09_06/source_memos/G3__dvs__religion2001_religion2022.md) | Religion 2001 / 2022 | 22 / 36 | 1 | 7.83 | 8.33 | — | Release |
| [G4](second_queue_repair_2026_09_06/source_memos/G4__dvs__promise_religion2022.md) | Promise / Religion 2022 | 16 / 26 | 0 | 6.83 | 7.83 | — | Release |
| [A4](second_queue_repair_2026_09_06/source_memos/A4__checked__harris.md) | Harris | 13 / 18 | 2 | 7.83 | 9.00 | 7.67 | Release |
| [A5](second_queue_repair_2026_09_06/source_memos/A5__checked__elling.md) | Elling | 11 / 16 | 0 | 8.67 | 8.83 | 8.50 | Release |
| [A6](second_queue_repair_2026_09_06/source_memos/A6__checked__chen.md) | Chen | 20 / 26 | 0 | 7.83 | 8.17 | 7.50 | Release (inventory) |
| [C1](second_queue_repair_2026_09_06/source_memos/C1__checked__zambrana.md) | Zambrana | 17 / 22 | 3 | 7.50 | 8.17 | 8.00 | Release (inventory) |
| [C6](second_queue_repair_2026_09_06/source_memos/C6__checked__aukus.md) | AUKUS | 18 / 19 | 2 | 7.83 | 8.83 | 7.67 | Release |
| [S3](second_queue_repair_2026_09_06/final_repairs/source_memos/S3__checked__subsea.md) | Subsea | 19 / 28 | 4 | 7.83 | 8.50 | 6.67 | Release (inventory) |
| [E12](second_queue_repair_2026_09_06/source_memos/E12__checked__promise.md) | Promise | 19 / 27 | 0 | 8.50 | 8.50 | — | Release (inventory) |
| [A3](second_queue_repair_2026_09_06/final_repairs/source_memos/A3__checked__aukus.md) | AUKUS | 20 / 20 | 0 | 8.00 | 8.17 | 7.67† | Release |

† A3's 7.67 comparator is the disclosed supplemental Sonnet rating of its unchanged first-round original. All other available original means are frozen first-round scores. The required non-inventory comparisons pass. C1's 7.50 is below its original 8.00, and it releases under the owner's explicit inventory exception. G2–G4 have no original-question control. Sol's independent scores are reported without averaging them into Sonnet's comparison.

The selected eleven outputs contain **198 findings and 270 retained anchors**, all verified, including **15 corpus findings** with distinct source keys. Every actual table citation resolves to a citable row at the real desk handoff. **263/270 supplied spans match in full through the existing source index; 12 rows use its existing recorded trimming**. The remaining spans also pass as retained anchors after that existing operation. No matching rule was loosened in this round. See the [combined custody, anchor, desk and score audit](second_queue_repair_2026_09_06/release_audit.json), [initial audit](second_queue_repair_2026_09_06/first_pass_audit.json) and [final-repair audit](second_queue_repair_2026_09_06/final_repairs/audit.json).

All thirteen completed artifacts (eleven initial, two final repairs) have source memos and two independent ratings. There are **26 repaired-output ratings plus one supplemental original rating**. The study still uses only one paper or pair per method, one production condition per method, and no new original generation. Three bounded structural synthesis repairs succeeded: C6 and S3 initially, and S3 in its final repair.

## Catalogue release

`catalog_purpose.json` explicitly lists the released keys and removes their exclusions:

- **Follow the words:** G2 `compare_concept_trajectories`, G3 `concept_appropriation_tracker`, G4 `revision_presentation`, C1 `meaning_in_use`.
- **Test a position:** A4 `counterfactual_analyzer`, A5 `dialectical_structure`, A6 `modal_force_inventory`.
- **See the structure:** A3 `comparative_reasoning_analyzer`, C6 `framework_components`, E12 `theory_construction_analyzer`, P2 `reconcile_sources`.
- **Read it properly:** S3 `narrative_form_perspective`.

No second-queue method remains withheld. P1 remains withheld as instructed: its final PEACE anchor repair failed, and the proposed/effective Eximbank decree identity remains unsupported. No P1/P2 definitions or protected engine questions were edited. [Definition-preservation record](second_queue_repair_2026_09_06/definition_preservation.json).

## Remaining citation and scope limits

These limits remain visible to the desks and do not reinstate the superseded complete-package veto:

| Method | Remaining limitation in the reviewed output |
|---|---|
| G2 | The first matrix is organized by conceptual features; a later table aligns issues across works. Some causal cells rely on surrounding source text. A corpus scope clause wrongly says dates were unavailable, although the substantive comparison gives the dates and does not invent uptake. |
| G3 | The generic Marx–Schumpeter quote remains too short for some detailed cells, although the source supplies the content. Scope references leave the coverage review inconclusive. The Weber change error is cured in the actual aligned table. |
| G4 | The later emphasis can be described too strongly as a more determinate function, although the earlier article already contains the epistemic/property material. The output retains the earlier conditional and anti-redemptive qualifications. |
| A4 | Thompson and the decolonial example remain selective coverage gaps. The no-concession counterfactual and pluralist alternative are retained with appropriately limited conclusions. |
| A5 | F5 still quotes a prefix before the second-nature object; the source supplies it. The critical/reflective attribution reversal is cured in prose and tables. |
| A6 | F15 names Nazism and populism while its quote covers populism; both occur in the source, and the actual table cell is narrowed to populism. Other examples have separate findings. |
| C1 | Layout-affected spans use existing wall trimming; the source supports the paired senses, voices and dependence predicate. |
| C6 | Two rows use existing trimming. The classification is consistently a within-article comparison, and application cells distinguish rules/eligibility from achieved outcomes. |
| S3 | The first ending-order error is cured in the selected final artifact. Four rows still use existing trimming for layout-affected spans, and scope metadata remains limited. |
| E12 | A malformed coverage key makes the appended scope review inconclusive. Local pronouns sometimes require surrounding context; the distinct synthesis components now survive in separate findings. |
| A3 | The selected final artifact adds distinct financial and critical-minerals comparisons. Some anchors rely on nearby actors, and the article does not quantify aggregate predominance; the reading marks that limit. |
| P2 | Some causal cells have incomplete local packets; F3 mislocates a delivery qualification on support, while the source and the rest of the output distinguish strong support from uncertain implementation. |

A mechanical scope record is not proof of source coverage. Conversely, an inconclusive scope record is not proof that an individually verified and source-supported finding is fabricated. The source memos make that distinction explicitly.

## P2 and P1

P2’s unchanged third-round artifact is reviewed in [the release source memo](second_queue_repair_2026_09_06/P2_release_source_memo.md), with [a fresh anchor/ID audit](second_queue_repair_2026_09_06/P2_release_audit.json). The French hub/industry mechanism and Japanese/Korean engagement are in the supplied sources, although absent from some local packets. The remaining F3 imprecision attaches delivery risks to the support claim; the same output retains strong support and correctly describes implementation risks elsewhere. It is recorded as a mislocated qualification, not an invented delay or a source-voice reversal. No rejected row is retained as valid in a table.

P2 passes the existing retained-row wall: 15 rows, 19 anchors, three two-key corpus rows. One supplied span uses the pre-existing wall’s recorded prefix trimming (18/19 match in full before that operation). No new matcher or relaxation was introduced. Its unchanged third-round means are Sonnet 7.67 and Sol 7.33; there is no original-question control for this merged method. Release `reconcile_sources` under See the structure. Its incomplete packets remain subject to the desks’ walls.

P1 stays withheld: the final PEACE anchor repair failed, and its proposed/effective Eximbank decree identity remains unsupported. No P1 repair or new P2 output was purchased in this round.

## Tests and accounting

The exact requested suite after the final card and catalogue changes reports **1,303 passed, 2 skipped, 11 failed, 8 collection errors**. The failures comprise the ten listed baseline failures plus the events-store ordering failure already recorded in the first-round protocol. The events-store file passes in isolation. Seven legacy mock cases that explicitly exercise unchanged prose/receipts now declare table-free test specs; no production questions were changed to satisfy those tests. [Phase-one test record](second_queue_repair_2026_09_06/phase1_tests.json).

The final catalogue/propagation focus passes **44 tests**. Excluding the documented old failures and collection errors gives **1,303 passed, 2 skipped, 11 deselected**. The exact full suite has identical failure/error IDs to phase one. [Release test record](second_queue_repair_2026_09_06/release_tests.json). The final card changes were followed by the exact full suite again: the same **1,303 passed, 2 skipped, 11 failed and 8 collection errors**, with no new failure/error IDs. [Final test record](second_queue_repair_2026_09_06/final_tests.json). The 68-prompt fixture and propagation tests pass. The baseline-filtered green run preceded the two final card edits; the exact full run after them confirms no new failures.

Known total: **USD7.555422** = first-pass generation/failures/ratings and original comparator **6.382102** + two final checked repairs and four ratings **1.042583** + direct Claude runner review **0.130737**. This includes both refused G3 attempts and all bounded synthesis repairs. Provider usage has **no unknown reserve**. The terminated Claude CLI attempt has no receipt, so its cost remains **unknown**, not zero; the known subtotal is below USD10 guidance, but a complete monetary total cannot be asserted. The owner authorized completion rather than a hard cap. Raw paid responses, prompts' hashes and receipts are preserved; cached G3 calls are not charged twice.

Commits were pulled/rebased before each phase and pushed: `1bda5ff` shared laws/runner/fixture; `24623d9` eleven cards and freeze; `d6b128f`, `3df89d0`, `655dca8`, `3f3b0be` source custody and G3 continuations; `78d058e` first-pass ratings/adjudication; `ff0d1e7` two bounded final cards; `778790a` final source memos. The final release commit updates the catalogue, FEATURES, CHANGELOG, tracker §11 and this report.
