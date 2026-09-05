# Redesign: Compare supplied cases (2026-09-06)

## Purpose and ideal output

Compare supplied cases on justified common questions. The unit may be a country, policy, institution, option or conceptual approach, but a source is not automatically one case. The product is a case by criterion matrix with attributed evidence, explicit missing and incommensurable cells, supported contrasts and exceptions. Comparison criteria must answer the shared inquiry; evaluative rankings require reader criteria. Cultural context and translation may limit equivalence; universal patterns cannot exceed the supplied coverage.

One comparison, not consecutive document reviews: a case × criterion matrix followed by a reasoned contrast that survives the difficult case. On the AUKUS/subsea pair the question concerns state strategies toward private networks and markets; the source-to-case map must distinguish the AUKUS policy complex from the subsea article's US/China and French cases. Neither paper is a single homogeneous state. The matrix can use two supplied case complexes with named subcases rather than silently pooling US exclusion and French ownership. On Castoriadis the cases are the supplied conceptual approaches, not three observed societies or an assumed developmental sequence.

The tables desk lifts (1) cases as rows and justified questions as columns, with an answer, source identity, scope and finding id per filled cell; (2) criterion × comparability limit/exception. A compact matrix may group dimensions into sections, but every case must have an explicit cell. Missing means the needed material is not supplied; insufficient evidence means the supplied passage cannot settle the criterion; incommensurable means that units, objects or meanings cannot support that contrast. None means zero or a failed case.
## Preserved questions from the catalogue

Base: `comparative_framework`; the legacy definition is unchanged. `families_codex.json` P1/P2 controls the scope.

| Preserved question | Home |
|---|---|
| Entity alignment | case_identity |
| Comparison criteria | case_identity + case_answers |
| Matrices | case_matrix |
| Similarities and differences | case_matrix |
| Cultural context and translation limits | comparison_limits |
| Exceptions to proposed patterns | comparison_limits + case_matrix |

## Dimensions and answer contracts

Document dimensions inventory answers and coverage separately. The corpus dimension builds relations from those inventories; it receives reports rather than full source text. The corpus critic and synthesis receive every source. Scoped outcomes carry negative/inconclusive inspection reports without forcing invented findings. A missing extraction or failed anchor is evidence trouble, not absence.

### C1. Cases, boundaries and comparable objects (document)

- What case or approach does this source actually document, which actors belong to it, and what object, place and time does it cover? Distinguish a source from the cases within it.
- What shared reader question could this case answer, and which comparison criteria does the source justify? Preserve supplied reader criteria; label analyst-proposed criteria and explain their relevance.
- Which names denote the same entity and which similar names denote different entities, institutional levels or objects? What evidence warrants alignment?

Answer shape: `[C1.F<n>] <case and source-supported boundary or criterion> — dim: case_identity — case: <stable descriptive key> — object-time-scope: <scope> — criterion: <shared question or proposed criterion with rationale> — anchor: "<verbatim>" — doc: <source key> — confidence: high|medium|low`

Method card: Identify the unit before comparing it. Separate a paper, a case and an actor inside a case; keep nested cases explicit. Choose criteria because they answer a shared question and the sources can speak to them. Treat approaches as cases when the material is conceptual, without pretending they are empirical countries or successive stages.

Indicators: case selection, empirically, in contrast, jurisdiction, period, we examine.

### C2. Answers on candidate common criteria (document)

- On each justified candidate criterion, what answer does this case supply, with its mechanism, evidence and qualification? Use the criterion as a question, not a topic label.
- What are the relevant actors, instruments, constraints and reported consequences, or the conceptual equivalents if the case is an approach? Distinguish a stated aim, a mechanism and a demonstrated result.
- Where is the value quantitative, qualitative, binary or ordinal, and what definition, denominator, date or evaluative standard makes that value meaningful? Do not create a ranking without supplied criteria.

Answer shape: `[C2.F<n>] <case> answers <criterion/question>: <value and qualification> — dim: case_answers — case: <key> — criterion: <question> — value-kind: quantitative|qualitative|binary|ordinal — evidence-role: aim|mechanism|reported result|conceptual claim — scope: <object/time/unit> — anchor: "<verbatim>" — doc: <source key> — confidence: high|medium|low`

Method card: Inventory answers that can become matrix cells. Preserve the case actor, instrument, mechanism and evidential status; do not convert the source's interpretation into an independently observed outcome. Copy units and denominators with values. Supply the exact answer, not a generic synopsis; leave unanswerable criteria in the coverage report.

Indicators: instrument, depends on, result, capacity, market, institution, definition.

### C3. Exceptions, context and unavailable cells (document)

- What in this source qualifies or defeats a proposed common pattern, and which case detail would a uniform template erase?
- Which cultural or institutional assumptions and translation choices limit equivalence? Does a common word have a different local meaning or referent?
- Which candidate criteria cannot be answered from the inspected passages, and why: not supplied, insufficient evidence, or incommensurable object, time, unit or meaning? State inspected sections and coverage; a missing extraction is not silence.

Answer shape: `[C3.F<n>] <case-specific exception or comparability limit> — dim: comparison_limits — case: <key> — criterion: <question> — limit: <context/translation/coverage/comparability> — pattern-tested: <proposed pattern, if any> — anchor: "<verbatim>" — doc: <source key> — confidence: high|medium|low. Unanswerable cells belong in separate scope reports with inspected sections and reasons, not invented negative findings.`

Method card: Try to break the proposed pattern with the source's exceptions. Name what a translation or cultural assumption changes in the comparison, or state that no such issue is established in the inspected scope. Keep missing, insufficient and incommensurable distinct. Record actual inspection and its limits separately; never fabricate a quote for an empty cell.

Indicators: however, exception, only, not comparable, translation, beyond the scope, not available.

### CM. The justified case by criterion matrix (corpus)

- Which common questions are justified by the supplied case inventories? Explain alignment, keeping a source-to-case map when a source contains several cases or several sources describe one case.
- For each common criterion, what does each case answer, with its source identity and scope? Retain every case and every missing, insufficient or incommensurable cell in the table.
- Which similarities, differences, clusters or outliers survive equivalent definitions and explicit exceptions? Test the strongest proposed common pattern against the most inconvenient case.
- What comparison is supportable within this collection, and which evaluative ranking or universal claim remains unlicensed by the supplied criteria and coverage?

Answer shape: `[CM.F<n>] On <shared criterion>, <case A answer> compared with <case B answer>, qualified by <scope/exception> — dim: case_matrix — cases: <keys> — criterion: <question> — relation: similarity|difference|pattern|exception|incommensurable — anchor: "<A>" — doc: <A source key> — anchor-b: "<B>" — doc-b: <distinct B source key> — confidence: high|medium|low. Include anchor-c/doc-c for a claim covering a third source. Empty cells remain scope reports and table statuses.`

Method card: Build the comparison from attributed cells, then argue the contrast. Use a shared label only after checking object, time, unit and local meaning. Keep exceptions and unfilled cells visible rather than imputing values. Every positive cross-source relation needs an anchor from every source it covers; two distinct keys are the minimum. Per-document inventories permit only provisional coverage claims until the corpus critic inspects the sources.

Indicators: matched criterion, same object, different scope, exception, unavailable cell.

## Synthesis brief in the reader's order

1. State the comparison question and a compact source-to-case map: every source key, the case or approach it supports, object/time boundary, distinctive claim and qualification. Justify the common criteria. If only one source is supplied, provide a provisional case inventory and state that the corpus comparison has not run.
2. Render an actual Markdown case × criterion matrix, not a promise of a table. Rows are cases; columns are 3–6 justified shared questions. Each populated cell gives its answer, source key and final finding id; keep relevant time/unit and qualification. If a source contains nested cases, distinguish them in the cell or explicit subrows. Every unfilled cell says missing, insufficient evidence or incommensurable, with the scope and reason. Do not invent an anchor for an empty cell.
3. Explain the most consequential similarities and differences through paired evidence, then test the strongest common pattern against the exception. Distinguish intended policy from reported results and conceptual cases from empirical ones. Do not infer progression from document dates or input order.
4. Render a comparability and exceptions table: criterion | cases affected | object/time/unit/translation limit | consequence for the contrast | finding ids or inspected-scope basis. No unasked ranking; conditional evaluation only against stated reader criteria.
5. End with the comparison the supplied evidence supports and the most useful missing evidence. State cultural and translation limits where established, and do not generalize beyond coverage.
Retain final finding ids in every populated table cell. Cross-source rows keep dim: case_matrix and one anchor/doc pair per source covered (at least two distinct doc keys). Final findings and all prose/table citations use F1..Fn; from: carries earlier ids. Keep absence and inconclusive scope reports distinct from anchored findings. The desks must be able to lift the actual tables with their empty cells intact.

## Execution and desk consumption

`surface = oneshot`, `standard = oneshot_checked`, `deep = dvs`. Deep runs three dimension inventories per source, one corpus inventory, one check per source plus a corpus check, and one synthesis. Extraction is Luna, verification DeepSeek V4 Pro, synthesis Sol. Zero to six findings per extraction keeps the inventory selective; the critic hunts substantive misses. No positive minimum is imposed. The process runner invokes corpus dimensions only for two or more documents, keyed by real source identity through the workflow adapter.

The spine cites final finding ids to develop one comparison/reconciliation. The tables desk receives actual Markdown tables plus the findings, preserving empty cells, qualifications and doc keys; no separate renderer is needed. The figures desk may visualize supported contrasts/relations but must retain the scope limits and must not infer causal arrows from a table. Cross-document positive rows need at least two verbatim anchors with distinct source keys and a pair for every further source covered. Document-level cells use their own anchored rows. Scope reports are reported assessments, not citable positive evidence. Walls verify quotes and ids; the model judges equivalence, support, relevance and relation. The checked mode applies critic rulings to the ledger and leaves the first reading's prose/tables untouched, so the validation must inspect contradictions between revised findings and original prose.

## Frozen validation and readiness decision

Freeze these designs, definitions, study script, corpus identities and rubric before generation and scoring; record hashes. USD 8 is the cumulative campaign cap, including generation, re-anchoring, failures and both judges. P1: deep AUKUS/subsea and three-text Castoriadis. P2: deep three-text Deutschmann and Castoriadis. Also one standard checked AUKUS/subsea corpus per method. Every output receives a source-read memo bound to its content hash before any scores for that output. Independent Sonnet and Sol score one output at a time against the sources; no head-to-head, model identity or other judge scores. Read the reasons and use Sol as a second opinion given known family effects.

Readiness requires a usable matrix/reconciliation on both deep cases, every supplied source represented or explicitly unassessable, no decisive source-attribution or invented-consensus error, and explicit missing/incommensurable cells where needed. All offered positive table cells must trace to existing findings with valid source anchors; cross-source findings must retain all required pairs. Report residual wall failures, ruling omissions, unsupported scope and checked-prose inconsistencies separately. Scores are evidence, not an automatic threshold: both judges' usefulness and anchoring below 7 are a reason to withhold; a decisive source error withholds regardless of score. Register only after a documented ready judgment, with scope/mode limits if appropriate. Reuse `archive_inventory`, `archive_policy`, `archive_fragment` in offline mixed-scope runner/desk tests without paid generation; this checks preservation and walls, not model behavior on unseen controls.
