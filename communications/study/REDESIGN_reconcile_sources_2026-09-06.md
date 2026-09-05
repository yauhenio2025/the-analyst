# Redesign: Reconcile sources on shared questions (2026-09-06)

## Purpose and ideal output

Reconcile how supplied sources answer shared questions. Discover recurring themes, then align each source's attributed answer by object, time, definition and warrant before judging agreement, qualification or contradiction. Different scope and inspected silence are distinct from disagreement; insufficient material remains unresolved. The product is an answer reconciliation table and a theme coverage table, preserving source voices and unanswerable cells. Frequency of a theme is never evidence of substantive consensus.

One reconciliation, not a thematic digest: an aligned question has every source's answer, its scope and a justified relation. On Deutschmann the two 2001 papers and 2022 retrospective may repeat, elaborate or qualify a position; shared words and publication dates do not establish change. On Castoriadis an account of technique, democratic self-institution and capitalist rationality can share a question while answering at different levels. Such a difference is often a qualification or different scope rather than contradiction.

The tables desk lifts (1) the shared-question reconciliation with source-attributed answers, object/time/scope, relation and paired evidence; (2) theme coverage with named documents, n/N in this collection and argumentative role. Agreement, qualification, contradiction and silence must appear as table values when supported, never as a quota of findings to invent. Different scope, missing material and insufficient evidence stay visible. A common theme cannot fill an answer cell. Silence is a bounded report of inspected sections and criterion; it cannot be anchored by an invented negative quote.
## Preserved questions from the catalogue

Base: `thematic_synthesis`; the legacy definition is unchanged. `families_codex.json` P1/P2 controls the scope.

| Preserved question | Home |
|---|---|
| Theme discovery and prevalence | source_questions + question_reconciliation |
| Common questions | source_questions + source_answers |
| Consensus versus different scope | answer_limits + question_reconciliation |
| Contradictory positions | source_answers + question_reconciliation |
| Silence and unanswerable cells | answer_limits + scope reports + question_reconciliation |

## Dimensions and answer contracts

Document dimensions inventory answers and coverage separately. The corpus dimension builds relations from those inventories; it receives reports rather than full source text. The corpus critic and synthesis receive every source. Scoped outcomes carry negative/inconclusive inspection reports without forcing invented findings. A missing extraction or failed anchor is evidence trouble, not absence.

### R1. Themes, shared questions and source scope (document)

- What themes organize this source, and what substantive questions does it actually ask or answer under each? Preserve reader-supplied questions and propose additional ones only from passages.
- What object, time, institutional level and kind of inquiry does each question concern? Which concepts require definition before another source can be compared?
- What connections between themes does this source assert, and what role does each theme play: central answer, supporting explanation, incidental mention, or reported rival?

Answer shape: `[R1.F<n>] <source> addresses <question> under <theme>, about <object/time/scope> — dim: source_questions — theme: <label> — question: <substantive question> — role: central|supporting|incidental|reported rival — anchor: "<verbatim>" — doc: <source key> — confidence: high|medium|low`

Method card: Discover themes by the questions and connections the text makes. Distinguish discussing a theme from answering a question, and reporting a view from endorsing it. Preserve definitions and scope before normalizing labels; prevalence later counts named documents in this supplied set only.

Indicators: our question, we ask, concept, relation, in this paper, rather than.

### R2. Attributed answers and their warrants (document)

- For each question, what answer does this source give in its own terms, with the decisive condition, negation and degree of commitment?
- Whose answer is it: this text's position, a cited interlocutor's, or a view reconstructed by the analyst? What passage marks endorsement or distance?
- What reason or evidence supports the answer, and is its force conceptual, empirical, causal, interpretive or normative? What would have to match before another source could contradict it?

Answer shape: `[R2.F<n>] <source/speaker> answers <question>: <position with condition and modality> — dim: source_answers — question: <question> — attribution: own|reported other|analyst reconstruction — warrant: conceptual|empirical|causal|interpretive|normative — object-time-scope: <scope> — anchor: "<verbatim>" — doc: <source key> — confidence: high|medium|low`

Method card: Write source-attributed answers, preserving their strongest qualification. Separate the text's own commitments from a quoted opponent and an analyst reconstruction. Compare propositions at the same object and warrant level; a normative demand does not contradict an empirical description merely because their verbs differ.

Indicators: we argue, only if, not, because, according to, must, can.

### R3. Qualifications, inspected silence and unresolved questions (document)

- Where does the source qualify, narrow, contest or explicitly leave open one of its answers? Which passage prevents an apparently categorical reading?
- For a candidate shared question, do the inspected sections provide an answer, only a relevant discussion, or insufficient material? Name the sections inspected and limits; distinguish explicit refusal from inspected silence.
- What object, time, definition, translation or warrant difference could make an apparent conflict a different-scope relation? Which rival interpretation remains possible from the text?

Answer shape: `[R3.F<n>] <source answer> is limited by <qualification/different scope/unresolved issue> — dim: answer_limits — question: <question> — inspected-scope: <sections> — limit: <reason> — anchor: "<verbatim>" — doc: <source key> — confidence: high|medium|low. For silence or insufficient material use a separate scope report; no invented anchor or automatic whole-source absence.`

Method card: Look for conditions and counter-passages before naming disagreement. Make a silence claim only about stated inspected sections with a relevant question and adequate coverage. Keep insufficient material and a change of subject visible. A partial fragment or failed anchor cannot support absence; do not turn an unresolved question into a negative answer.

Indicators: however, not to say, limited, beyond our scope, unresolved, fragment, distinguish.

### RM. Reconcile answers on shared questions (corpus)

- Which questions can actually be aligned across sources after object, time, definition and warrant are compared? Retain source-specific questions and unanswerable cells.
- For each aligned question, what does every source answer and why is the relation agreement, qualification, contradiction, different scope, inspected silence or insufficient evidence? A contradiction requires incompatible answers under the same conditions; silence requires stated inspection, not a count of missing rows.
- Which themes recur in which named sources, and with what role? Report n/N for the supplied collection with the document list and denominator, separately from substantive agreement.
- What defensible synthesis preserves the strongest qualification and unresolved conflict? Which thematic connections are supported across sources, and what evidence would settle the residual question?

Answer shape: `[RM.F<n>] On <shared scoped question>, <source A answer> and <source B answer> stand in <relation and reason> — dim: question_reconciliation — question: <question> — relation: agreement|qualification|contradiction|different scope — scope-test: <object/time/definition/warrant match or mismatch> — anchor: "<A>" — doc: <A key> — anchor-b: "<B>" — doc-b: <distinct B key> — confidence: high|medium|low. Add anchor-c/doc-c for a third source covered. Silence/insufficient cells are separate scoped assessments, never fabricated paired findings.`

Method card: Align questions before reconciling answers; judge each relation rather than counting shared words. Give both attributed sides, their scopes and the exact reason for the relation. Count theme presence only over named inspected sources and never equate frequency with consensus. Preserve an unresolved conflict or scoped silence instead of manufacturing an integrated position; corpus extraction sees earlier reports, so the critic must inspect all relevant source passages.

Indicators: same question, qualification, incompatible answers, different object, theme coverage, inspected silence.

## Synthesis brief in the reader's order

1. State the shared inquiry and a compact position map naming every source key, its object/time/scope, central answer, distinctive role and important qualification. Do not infer an intellectual chronology from input order or edition dates. If only one source is supplied, return a source-position inventory and say reconciliation awaits additional sources.
2. Render an actual Markdown reconciliation table: shared question | source-attributed answers (one named entry for every supplied source, each positive answer with final finding id) | object/time/definition/warrant alignment | agreement/qualification/contradiction/different scope/inspected silence/insufficient evidence | reason and paired finding ids or inspected-scope basis. Split the table into compact question tables if needed; do not collapse source voices into a single consensus column. Missing and incommensurable cells stay visible.
3. Develop the strongest substantive agreement and the strongest qualification or unresolved disagreement. Quote both sides; explain why different objects, conditions or kinds of warrant make some apparent conflicts a different-scope relation. A shared theme is not a shared answer; do not force a contradiction when none survives alignment.
4. Render a theme coverage table: theme and substantive question | named source keys | n/N within the supplied collection | central/supporting/incidental roles | supported connection to another theme | limits and finding ids. Count discussion separately from endorsed answers; no prevalence claim beyond this set. Mark uncertain presence instead of treating missing extraction as absence.
5. End with what the collection jointly licenses, the exact remaining disagreement or unanswered question, and what further passage or evidence would decide it. Preserve every inspected-silence or insufficient-material assessment with its stated scope; no invented quotation for a negative cell.
Retain final finding ids in every positive answer cell. Cross-source rows keep dim: question_reconciliation and one anchor/doc pair for every source covered (at least two distinct keys). Final findings and all prose/table citations use F1..Fn; from: carries earlier ids. The desks lift the reconciliation and coverage tables directly, including all unresolved and unanswerable cells.

## Execution and desk consumption

`surface = oneshot`, `standard = oneshot_checked`, `deep = dvs`. Deep runs three dimension inventories per source, one corpus inventory, one check per source plus a corpus check, and one synthesis. Extraction is Luna, verification DeepSeek V4 Pro, synthesis Sol. Zero to six findings per extraction keeps the inventory selective; the critic hunts substantive misses. No positive minimum is imposed. The process runner invokes corpus dimensions only for two or more documents, keyed by real source identity through the workflow adapter.

The spine cites final finding ids to develop one comparison/reconciliation. The tables desk receives actual Markdown tables plus the findings, preserving empty cells, qualifications and doc keys; no separate renderer is needed. The figures desk may visualize supported contrasts/relations but must retain the scope limits and must not infer causal arrows from a table. Cross-document positive rows need at least two verbatim anchors with distinct source keys and a pair for every further source covered. Document-level cells use their own anchored rows. Scope reports are reported assessments, not citable positive evidence. Walls verify quotes and ids; the model judges equivalence, support, relevance and relation. The checked mode applies critic rulings to the ledger and leaves the first reading's prose/tables untouched, so the validation must inspect contradictions between revised findings and original prose.

## Frozen validation and readiness decision

Freeze these designs, definitions, study script, corpus identities and rubric before generation and scoring; record hashes. USD 8 is the cumulative campaign cap, including generation, re-anchoring, failures and both judges. P1: deep AUKUS/subsea and three-text Castoriadis. P2: deep three-text Deutschmann and Castoriadis. Also one standard checked AUKUS/subsea corpus per method. Every output receives a source-read memo bound to its content hash before any scores for that output. Independent Sonnet and Sol score one output at a time against the sources; no head-to-head, model identity or other judge scores. Read the reasons and use Sol as a second opinion given known family effects.

Readiness requires a usable matrix/reconciliation on both deep cases, every supplied source represented or explicitly unassessable, no decisive source-attribution or invented-consensus error, and explicit missing/incommensurable cells where needed. All offered positive table cells must trace to existing findings with valid source anchors; cross-source findings must retain all required pairs. Report residual wall failures, ruling omissions, unsupported scope and checked-prose inconsistencies separately. Scores are evidence, not an automatic threshold: both judges' usefulness and anchoring below 7 are a reason to withhold; a decisive source error withholds regardless of score. Register only after a documented ready judgment, with scope/mode limits if appropriate. Reuse `archive_inventory`, `archive_policy`, `archive_fragment` in offline mixed-scope runner/desk tests without paid generation; this checks preservation and walls, not model behavior on unseen controls.
