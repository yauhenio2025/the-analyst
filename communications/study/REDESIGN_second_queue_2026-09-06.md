# Second queue: ideal outputs, questions and method cards (2026-09-06)

Design phase: zero provider calls. Owner scope: eleven methods, generation and independent scoring together capped at USD 12; P1/P2 third round is separate and begins only after the queue release decision. Existing text-facing questions are retained; source defects justify replacements. All methods stay excluded until the source-read report supports release.

The process specification in [designs.json](second_queue_2026_09_06/designs.json) contains the exact answer shapes, cards, indicators, synthesis briefs and routing frozen with this memo. Modes: surface oneshot; standard oneshot_checked; deep/dvs decomposition. Sol strong, DeepSeek V4 Pro mid, Luna cheap. Six or five document dimensions and one corpus dimension per method. All positive cells need complete supporting spans; mechanically valid anchors are not semantic certification.

Validation fixed before scores: two genre-fitting papers per single-paper method, checked and one Sol old control using the original capability questions; one natural pair per corpus method in dvs and checked. Every complete final output receives a source-read memo bound to its hash before either independent Sonnet or Sol rubric score. For A6/C1/E12, anchor rate, row coverage and source accuracy govern usefulness. No superiority threshold and no head-to-head. Incomplete or materially unsupported outputs remain withheld. Sources and exact run matrix will be frozen in the build-phase PLAN before spending.

## G2 — Concept comparison and trajectories (`compare_concept_trajectories`)

### Ideal output

A one-page concept × work matrix comparing meaning, argumentative role, evidence/method, metaphor and force. Lead with the most consequential continuity or difference; distinguish unordered comparison from demonstrated development. Give each work a local inventory before any trajectory. The desks lift the matrix and a paired-change table with chronology and uptake limits.

Scope: Two or more supplied works; dates and identity/uptake evidence only when claiming development; prior analyses must retain their anchors.

Answer contract: Concept × source × dimension, continuity/change relation, paired passages, chronology confidence and explanatory limits.

### Existing questions and demonstrated repairs

Source engines: `concept_evolution`, `concept_cross_text_comparison`, `concept_synthesis`, `epistemic_rupture_tracer`, `genealogy_pass2_prior_scanning`, `genealogy_pass3_cross_work_synthesis`.

Preserved coverage: Unordered and cross-author comparison; vocabulary, method, metaphor and framing; continuity versus rupture; multi-work synthesis; absent-search scope.

Merge the six mapped engines. Preserve vocabulary/method/metaphor/framing comparisons, but move relational questions to corpus scope. Replace career, invisible influence and inevitable rupture questions with supplied dates, uptake and paired passages; a missing term is not abandonment.

### Dimensions, answer shapes and cards

#### local_meanings (document)

- Which terms does this work define or distinguish, and what object does each name?
- Which uses retain the definition and which give the same term a different sense?

Answer: `[D1.F<n>] <one scoped finding> — dim: local_meanings — term: <term> — sense: <local meaning> — boundary: <limit> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory definitions and actual uses; preserve negation and local scope. Split distinct senses before comparing works.

Indicators: by X we mean; defined as; in this sense.

#### argumentative_roles (document)

- What claim does each concept support here, and which premise connects them?
- What supporting claims, dependent concepts, and enabling assumptions constitute the argumentative architecture?

Answer: `[D2.F<n>] <one scoped finding> — dim: argumentative_roles — term: <term> — role: <premise, mechanism, result> — supports: <claim> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Trace the move made with the concept and its warrant. Distinguish sharing a noun from sharing an inferential role.

Indicators: therefore; depends on; constitutes.

#### method_and_evidence (document)

- Which evidence or analytical move establishes this use of the concept?
- Does the text derive, illustrate, apply or assume the concept at this passage?

Answer: `[D3.F<n>] <one scoped finding> — dim: method_and_evidence — term: <term> — move: <derivation, application, assumption> — evidence: <kind> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Record the actual procedure and its passage. A conceptual derivation can supply support without empirical testing.

Indicators: we derive; for example; we assume.

#### metaphor (document)

- What governing metaphors appear in this work, and what relations do they carry?
- Where does the text mark a metaphor as limited or use it as a literal claim?

Answer: `[D4.F<n>] <one scoped finding> — dim: metaphor — term: <term> — mapping: <relation> — use: <metaphorical, literal, unresolved> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Identify the transferred relation and limit; do not infer what the author sees privately.

Indicators: as if; like; metaphor.

#### framing (document)

- What problem is this concept made to answer, with what confidence and scope?
- Where does this work state a continuity, novelty or revision claim and what exact object does it concern?

Answer: `[D5.F<n>] <one scoped finding> — dim: framing — term: <term> — problem: <question> — force: <operator> — claimed-relation: <claim> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Keep hedges attached to their propositions. Do not turn an introductory claim into a demonstrated history.

Indicators: may; must; extending; previously.

#### local_limits (document)

- Which passage qualifies a proposed stable meaning or interpretation?
- Which relevant sections were inspected for an alternative term or use, and what remains outside that inspection?

Answer: `[D6.F<n>] <one scoped finding> — dim: local_limits — term: <term> — qualification: <limit> — inspected: <sections> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Retain counter-uses and avoid forced consistency. Record a negative search in the scope report; its context anchor cannot prove global absence.

Indicators: not in every case; only; scope.

#### concept_trajectories (corpus)

- What terms appear in both the prior work and the current work? **Preserved verbatim.**
- For each key concept, which dimensions changed and which remained stable? **Preserved verbatim.**
- Which paired passages establish a change in meaning rather than only application, scope or rhetorical force? What dates and uptake warrant an ordered trajectory?

Answer: `[X7.F<n>] <one scoped finding> — dim: concept_trajectories — relation: <aligned relation> — alignment: <object, sense, owner, scope> — order-basis: <dates, uptake, or unordered> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — anchor-b: "<verbatim supporting clause B>" — doc-b: <different source key> — confidence: high|medium|low`

Do: Build attributed cells first, each with its own finding and supporting spans. Preserve unordered cross-author comparison; same-year publication and input order establish no sequence. Pair both works and retain counter-passages before claiming rupture, novelty or abandonment.

Indicators: explicit reference; paired formulations; scope qualification.

### Method card and delivery

A one-page concept × work matrix comparing meaning, argumentative role, evidence/method, metaphor and force. Lead with the most consequential continuity or difference; distinguish unordered comparison from demonstrated development. Give each work a local inventory before any trajectory. The desks lift the matrix and a paired-change table with chronology and uptake limits. Merge the six mapped engines. Preserve vocabulary/method/metaphor/framing comparisons, but move relational questions to corpus scope. Replace career, invisible influence and inevitable rupture questions with supplied dates, uptake and paired passages; a missing term is not abandonment.

1. A one-page concept × work matrix comparing meaning, argumentative role, evidence/method, metaphor and force. Lead with the most consequential continuity or difference; distinguish unordered comparison from demonstrated development. Give each work a local inventory before any trajectory. The desks lift the matrix and a paired-change table with chronology and uptake limits.
2. Establish the most consequential local findings and their qualifications; organize the reading by the objects and claims in these texts.
3. Render the named Markdown tables with final finding IDs in every positive cell. Explain the supported relation and the strongest counter-passage; end with what is settled and the exact remaining question.
4. With multiple sources, build each work’s inventory before the paired comparison, and state alignment and chronology limits. With one source, label the result a local inventory where a corpus relation would require another work.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## G3 — Borrowing and changed use (`concept_appropriation_tracker`)

### Ideal output

A source-use → receiving-use table: the concept as used in each context, changed purpose, retained and dropped conditions, acknowledgment and evidence of transmission. Lead with what the receiving argument gains or loses; distinguish adaptation from misrepresentation and resemblance from demonstrated borrowing. Desks lift uses and transmission-status tables.

Scope: Source and receiving texts, plus any supplied intermediary or transmission evidence.

Answer contract: Source use, receiving use, changed purpose or meaning, acknowledgment, paired anchors and status of the transmission claim.

### Existing questions and demonstrated repairs

Source engines: `concept_appropriation_tracker`.

Preserved coverage: Migration paths; semantic mutation; faithful adaptation versus distortion; recombination; acknowledged and unacknowledged use.

Reuse the engine as v2. Preserve semantic mutation, purpose, recombination and citation questions. Replace unconscious absorption, intention and concealment with explicit acknowledgment, supplied intermediaries and unresolved transmission. Fidelity concerns representations of source claims, not permission to create a new use.

### Dimensions, answer shapes and cards

#### use_in_context (document)

- What concept is used here, for what object and purpose?
- What conditions or contrasts define its meaning in the quoted passage?

Answer: `[D1.F<n>] <one scoped finding> — dim: use_in_context — concept: <term> — purpose: <local job> — conditions: <scope> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Reconstruct the local use before judging borrowing. Preserve the owner of the concept and its conditions.

Indicators: means; used to; in contrast.

#### acknowledgment (document)

- Which earlier text or domain does this work explicitly cite for the concept?
- Does the citation endorse a definition, adapt a method, report a rival or merely mention a name?

Answer: `[D2.F<n>] <one scoped finding> — dim: acknowledgment — source-mentioned: <work> — uptake: <specific relation> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the uptake clause; citation alone does not show adoption of a whole system. Mark source descriptions as this work’s reports until inspected independently.

Indicators: following; drawing on; as X argues.

#### changed_purpose (document)

- What new purpose does the appropriated concept serve? **Preserved verbatim.**
- Which changes to the borrowed concept does this work expressly announce?

Answer: `[D3.F<n>] <one scoped finding> — dim: changed_purpose — concept: <term> — change-claimed: <change> — new-job: <purpose> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Separate a new use from a claim to reproduce the origin faithfully. Record announced changes without certifying them from one text.

Indicators: adapt; narrower; apply to.

#### recombination (document)

- Are ideas from the prior work combined with ideas from other sources in the current work? **Preserved verbatim.**
- Are the recombined elements compatible, or does their combination create tensions? **Preserved verbatim.**

Answer: `[D4.F<n>] <one scoped finding> — dim: recombination — components: <attributed inputs> — relation: <combination and conditions> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Anchor each input in this work and show the connecting move. Assess compatibility under the same object and assumptions.

Indicators: combine; together; synthesis.

#### representation_limits (document)

- Which quotation or paraphrase represents the borrowed position, and with what attribution and qualification?
- What would change in this argument if a stated qualification were restored?

Answer: `[D5.F<n>] <one scoped finding> — dim: representation_limits — represented-claim: <owned proposition> — qualification: <retained or omitted locally> — consequence: <route> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Read surrounding attribution and conditions; do not allege distortion without a supplied original. Distinguish local omission from misrepresentation.

Indicators: according to; however; only if.

#### borrowing_and_use (corpus)

- For each migrated concept, what changed in its meaning? **Preserved verbatim.**
- Is each appropriation faithful, adapted, distorted, or inverted relative to the original? **Preserved verbatim.**
- What source–destination link or supplied intermediary establishes transmission, and what remains resemblance only?

Answer: `[X6.F<n>] <one scoped finding> — dim: borrowing_and_use — relation: <aligned relation> — alignment: <object, sense, owner, scope> — order-basis: <dates, uptake, or unordered> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — anchor-b: "<verbatim supporting clause B>" — doc-b: <different source key> — confidence: high|medium|low`

Do: Pair full local uses and acknowledgment evidence. Judge fidelity only to a represented source claim; changed purpose alone is legitimate adaptation. Keep transmission unresolved when no link is supplied, even if meanings resemble each other; do not invent silent or unconscious borrowing.

Indicators: explicit reference; paired formulations; scope qualification.

### Method card and delivery

A source-use → receiving-use table: the concept as used in each context, changed purpose, retained and dropped conditions, acknowledgment and evidence of transmission. Lead with what the receiving argument gains or loses; distinguish adaptation from misrepresentation and resemblance from demonstrated borrowing. Desks lift uses and transmission-status tables. Reuse the engine as v2. Preserve semantic mutation, purpose, recombination and citation questions. Replace unconscious absorption, intention and concealment with explicit acknowledgment, supplied intermediaries and unresolved transmission. Fidelity concerns representations of source claims, not permission to create a new use.

1. A source-use → receiving-use table: the concept as used in each context, changed purpose, retained and dropped conditions, acknowledgment and evidence of transmission. Lead with what the receiving argument gains or loses; distinguish adaptation from misrepresentation and resemblance from demonstrated borrowing. Desks lift uses and transmission-status tables.
2. Establish the most consequential local findings and their qualifications; organize the reading by the objects and claims in these texts.
3. Render the named Markdown tables with final finding IDs in every positive cell. Explain the supported relation and the strongest counter-passage; end with what is settled and the exact remaining question.
4. With multiple sources, build each work’s inventory before the paired comparison, and state alignment and chronology limits. With one source, label the result a local inventory where a corpus relation would require another work.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## G4 — How revisions are presented (`revision_presentation`)

### Ideal output

An earlier-position / later-position / claimed-relation table. Compare the text’s own account of continuity, concession or clarification with changes in force, scope and support. Lead with the consequential match or mismatch, then the exact wording and what it changes for the argument. Desks lift revision and evidence-change tables; honest continuity is a valid result.

Scope: Earlier position, later treatment and any response or declared continuity claim; dated ordering if available.

Answer contract: Earlier position, later position, claimed relation, observed change in scope/force, argumentative consequence and paired anchors.

### Existing questions and demonstrated repairs

Source engines: `evolution_tactics_detector`, `genealogy_pass4_functional_analysis`, `genealogy_pass5_evolution_tactics`, `rhetoric_concession_tracker`, `rhetoric_contradiction_detector`, `rhetoric_retreat_detector`.

Preserved coverage: Revision, concession and clarification; actual versus claimed continuity; function of changed wording; new evidence versus mere escalation.

Merge the mapped evolution and rhetoric engines. Preserve revision, concession, changed wording and evidence escalation. Replace the ten-tactic checklist, career sophistication, public effectiveness and strategic-amnesia presumptions with auditable presentation claims; omit motives and intent.

### Dimensions, answer shapes and cards

#### position (document)

- What position does this text undertake, on what object and under what conditions?
- Which position does it attribute to a prior work or opponent, rather than undertake itself?

Answer: `[D1.F<n>] <one scoped finding> — dim: position — position: <proposition> — owner: <speaker> — scope: <conditions> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Preserve voice and conditions before comparing commitments. Report an earlier view as attributed until the earlier work is inspected.

Indicators: we argue; previously; according to.

#### claimed_relation (document)

- Where does the text call its move a clarification, extension, correction, concession or departure?
- What exactly is said to remain unchanged and what is expressly relinquished?

Answer: `[D2.F<n>] <one scoped finding> — dim: claimed_relation — claimed-relation: <words> — retains: <content> — relinquishes: <content> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the self-description and the object it qualifies. Do not infer a continuity claim from silence.

Indicators: clarify; still; no longer; concede.

#### scope_and_force (document)

- How is the position qualified by quantifier, modality, time or domain?
- Which local formulations change those conditions and what is their argumentative role?

Answer: `[D3.F<n>] <one scoped finding> — dim: scope_and_force — position: <proposition> — force: <operator> — conditions: <scope> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Compare the same proposition; a firm conclusion and a tentative extension can coexist. Preserve adjacent qualifying clauses.

Indicators: sometimes; necessarily; in this domain.

#### support (document)

- What evidence or derivation is offered for this position?
- Does the text identify new evidence or a new argument as its reason for changing the formulation?

Answer: `[D4.F<n>] <one scoped finding> — dim: support — support: <evidence or derivation> — change-reason: <declared or unstated> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory support appropriate to the claim. A stronger expression alone does not establish unsupported escalation until the other work is read.

Indicators: because; new evidence; reconsider.

#### concession_consequence (document)

- What does the text concede and which conclusion does that concession narrow or preserve?
- Does it answer the conceded difficulty, distinguish its scope or leave it open?

Answer: `[D5.F<n>] <one scoped finding> — dim: concession_consequence — concession: <content> — response: <move> — consequence: <affected claim> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Price the concession against the actual commitment. Acknowledged limits and continuing mediation need not be retreat or failure.

Indicators: nevertheless; this is not to say; only partially.

#### revision_record (corpus)

- Which earlier and later formulations concern the same owned position, and what establishes their order?
- Does the observed change in scope, force or support match the later text’s stated relation to the earlier one?
- Where do paired passages show continuity, qualification or revision; which apparently new caution is already present earlier?

Answer: `[X6.F<n>] <one scoped finding> — dim: revision_record — relation: <aligned relation> — alignment: <object, sense, owner, scope> — order-basis: <dates, uptake, or unordered> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — anchor-b: "<verbatim supporting clause B>" — doc-b: <different source key> — confidence: high|medium|low`

Do: Compare the later account with the earlier text itself and its qualifications. Quote both sides of every relation and a separate presentation finding where needed. Distinguish edition dates from composition, no chronology from same-year order, and no concealment from unmentioned change.

Indicators: explicit reference; paired formulations; scope qualification.

### Method card and delivery

An earlier-position / later-position / claimed-relation table. Compare the text’s own account of continuity, concession or clarification with changes in force, scope and support. Lead with the consequential match or mismatch, then the exact wording and what it changes for the argument. Desks lift revision and evidence-change tables; honest continuity is a valid result. Merge the mapped evolution and rhetoric engines. Preserve revision, concession, changed wording and evidence escalation. Replace the ten-tactic checklist, career sophistication, public effectiveness and strategic-amnesia presumptions with auditable presentation claims; omit motives and intent.

1. An earlier-position / later-position / claimed-relation table. Compare the text’s own account of continuity, concession or clarification with changes in force, scope and support. Lead with the consequential match or mismatch, then the exact wording and what it changes for the argument. Desks lift revision and evidence-change tables; honest continuity is a valid result.
2. Establish the most consequential local findings and their qualifications; organize the reading by the objects and claims in these texts.
3. Render the named Markdown tables with final finding IDs in every positive cell. Explain the supported relation and the strongest counter-passage; end with what is settled and the exact remaining question.
4. With multiple sources, build each work’s inventory before the paired comparison, and state alignment and chronology limits. With one source, label the result a local inventory where a corpus relation would require another work.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## A4 — Audit a counterfactual (`counterfactual_analyzer`)

### Ideal output

A one-page audit of the text’s consequential suppositions: antecedent and owner, fixed background and extra changes, bridge and modal force, relevant alternative, and what independently survives. Desks lift scenarios, dependencies and robustness tables. A genuine inferential counterexample qualifies without literal if–then syntax.

Scope: A text advancing a what-if or counterexample, with historical background only where its kind of claim requires it.

Answer contract: Antecedent, retained background, changed assumptions, consequence, inferential type, support and sensitivity to alternatives.

### Existing questions and demonstrated repairs

Source engines: `counterfactual_analyzer`.

Preserved coverage: Possible-world specification; cotenability; minimal changes when relevant; causal versus conceptual inference; backtracking consistency; uncertainty.

Keep the candidate’s five document dimensions and corpus comparison. Correct Harris counterexample eligibility, Ganzinger positive-route ownership, Elling structural necessity versus historical intensity, and Deutschmann continuity and slavery qualifications. Do not substitute denial of a necessity premise for an intervention removing the condition itself.

### Dimensions, answer shapes and cards

#### supposition_and_function (document)

- What antecedent is varied, denied, left open or provisionally granted, and what consequent is claimed? Quote the inferential passage, including a counterexample without literal if–then wording, and preserve its modal force.
- Is this an explicit counterfactual, an open conditional, an even-if concession, a reductio, or an analyst's reconstruction? Explain the classification from the passage rather than from the word if alone.
- Who undertakes the supposition here, and what is its task? Distinguish the paper's commitment from an interpreted thinker's position, an opponent's premise and an assumption adopted only for argument.
- Is the conclusion asserted only under that supposition? Before alleging strength drift elsewhere, check that the comparison concerns the same proposition under the same antecedent.

Answer: `[CF1.F<n>] <supposition and argumentative task> — dim: supposition_and_function — scenario: <stable scenario label> — kind: counterfactual|open_conditional|even_if|reductio|reconstructed_dependency — owner: <speaker and endorsement status> — antecedent: <condition and denied, open or granted status> — consequent: <claim with modal strength> — function: <causal, conceptual, historical, normative or robustness task> — anchor: "<supposition passage>" — doc: <key> — anchor-b: "<separate consequent or attribution passage, if needed>" — doc-b: <key> — confidence: high|medium|low`

Do: Start with the inferential use, not an alternate-history template. An even-if concession can
establish a requirement that survives granting an antecedent without asserting that antecedent
is actual or possible. A reductio can deliberately assume what the argument rejects. Mark a
reconstructed dependence as the analyst's formulation and cite the textual route it reconstructs;
a causal attribution alone does not establish that removing this cause removes every possible route. A counterexample defeats a universal or primacy claim through its inference; literal conditional syntax is not an eligibility test.

Indicators: if; even if; suppose; without; otherwise; for the sake of argument.

#### fixed_and_changed_conditions (document)

- What does the text explicitly hold fixed while varying or granting the antecedent? Distinguish stated background conditions from assumptions reconstructed by the analyst.
- Which further changes follow from the supposition, and which are additional premises needed to obtain the proposed result? Identify the textual warrant or state that it is not supplied.
- Does the scenario require incompatible fixed conditions, or is the apparent incompatibility the deliberate object of a reductio or conceptual limit test?
- For a historical or causal scenario, what earlier conditions would have to differ and does the text disclose them? For a conceptual or normative scenario, what commitments define the permissible contrast?

Answer: `[CF2.F<n>] <the scenario's fixed and changed conditions and their adequacy> — dim: fixed_and_changed_conditions — scenario: <stable label> — changed: <antecedent and required consequences> — held-fixed: <stated conditions or not specified> — additional-assumption: <extra premise or none established> — basis: stated|reconstructed|unsettled — consistency: compatible|conflict|deliberate_reductio|unsettled — anchor: "<condition-changing passage>" — doc: <key> — anchor-b: "<background or limiting passage, if available>" — doc-b: <key> — confidence: high|medium|low`

Do: Audit the contrast actually used. Separate what must change to make the antecedent hold from
extra changes introduced to secure the conclusion. Apply historical backtracking and similarity
questions where the scenario has that temporal structure; do not require them of a conceptual
dependency test. Compatibility is not enough to show that a background condition should remain
fixed. Conversely, deliberate inconsistency in a reductio is not an unnoticed scenario error.

Indicators: all else; still; regardless; assume; under these conditions.

#### inferential_path (document)

- What connects antecedent to consequent here? Identify a conceptual requirement, definition, causal mechanism, historical regularity, normative premise or cited argument, and the passage doing that work.
- Which steps are stated and which are reconstructed? Does restating the consequent answer the dependency question, or is a connecting premise still required?
- Does the support establish necessity, possibility, tendency or a result conditional on further premises? Preserve necessary vulnerability separately from inevitable realization and risk separately from actual occurrence.
- What scope does the warrant support, and what competing or independent route does the text itself supply? Do not reverse a sufficient argument into a necessary condition of accepting its conclusion.

Answer: `[CF3.F<n>] <the supported link and its limits> — dim: inferential_path — scenario: <stable label> — warrant-kind: conceptual|definitional|causal|historical|normative|cited_argument|mixed — link: <antecedent through bridge to consequent> — bridge-status: stated|reconstructed|unsettled — support-strength: necessary|possible|tendency|conditional|underdetermined — scope: <objects and additional conditions> — anchor: "<claimed link>" — doc: <key> — anchor-b: "<support or qualification, if separate>" — doc-b: <key> — confidence: high|medium|low`

Do: Make the bridge inspectable and apply the standard appropriate to its task. A hypothetical
counterexample need not report observed frequencies; an assertion about actual historical
reception does need evidence of that occurrence. Do not assign numerical probabilities without
a supplied basis. Keep structural claims, illustrations and empirical premises separate. A paper's
argument for a conclusion is one route until it establishes why alternatives cannot support it. Distinguish a positive conceptual derivation from an opponent premise rejected along the way. Quote the actual supporting step. General contingency or historical intensity does not refute a specifically scoped necessity claim.

Indicators: would therefore; requires; only if; might; tends to; because.

#### alternatives_and_scope (document)

- What alternative case or interpretation does the text consider under a comparable supposition, and what makes it relevant to this consequent?
- Do different results arise because a background condition, object, modal force or argumentative task changed? Quote both cases and identify the difference before calling them inconsistent.
- For a historical comparison, what warrants the similarity ordering and treatment of earlier causes? For a conceptual comparison, which disputed commitments must remain in place for the test to bear on the argument?
- If an alternative is the analyst's proposed test, what textual premise makes it discriminating, and what would need further evidence? Do not present an invented scenario as one the paper claims.

Answer: `[CF4.F<n>] <alternative and what the comparison tests> — dim: alternatives_and_scope — scenario: <stable label> — alternative: <case or interpretation> — origin: in_text|analyst_test — relevant-similarity: <shared conditions> — scope-difference: <changed object, background, modality or task> — result: supports|qualifies|challenges|does_not_discriminate|unsettled — anchor: "<original scenario or tested premise>" — doc: <key> — anchor-b: "<textual alternative or limiting passage, if available>" — doc-b: <key> — confidence: high|medium|low`

Do: Compare the same proposition under controlled qualifications. The failure of a negative critique
and the plausibility of a conditional constructive proposal are different targets. Start from
alternatives available in the text. A proposed test can be useful without becoming source evidence;
label it and anchor the premise it tests, not imaginary dialogue. Do not select a closest world
or historical probability by intuition and report it as an established fact.

Indicators: by contrast; another possibility; unless; on a different reading; in that case.

#### survival_and_robustness (document)

- If a disputed premise or additional change is withdrawn, what exactly loses support: this wording, this derivation, a stronger modal conclusion, or every route to the result?
- What independent conceptual, empirical or normative grounds does the text offer for the same conclusion? Test them rather than treating the most prominent route as indispensable.
- Does a criticism remain intact if the paper's constructive alternative fails? Conversely, does failure of one criticism answer other independently developed objections?
- What is the weakest surviving conclusion and its conditions? State when a subtraction is the text's explicit argument, an analyst reconstruction, or a test the available material cannot settle.

Answer: `[CF5.F<n>] <withdrawal and the conclusion it actually leaves> — dim: survival_and_robustness — scenario: <stable label> — withdrawn: <premise or extra change> — affected-route: <specific formulation or derivation> — surviving-route: <separate support or not established> — conclusion-strength: unchanged|narrowed|this_route_defeated|all_routes_defeated_with_basis|unsettled — origin: text|analyst_reconstruction|proposed_test — anchor: "<withdrawn premise or affected route>" — doc: <key> — anchor-b: "<independent support or qualification, if available>" — doc-b: <key> — confidence: high|medium|low`

Do: Remove one premise at a time while holding the remaining argument explicit. Distinguish a
resource that the author uses from a commitment every accepter must undertake. Separate the
identity of a theory from the adequacy of a revised descendant, and conceptual reconstruction
from independently supplied history. Do not invent a casualty: a route can fail while the
conclusion remains supported. No further support found is scoped to the inspected material. Hold the intervention fixed: removing uncertainty differs from rejecting the premise that uncertainty is necessary. Test whether purported independent routes survive the exact intervention, not a weaker substitute.

Indicators: even without; independently; whether or not; sufficient reason; remains valid.

#### suppositions_across_texts (corpus)

- Do two documents vary or grant the same condition under comparable background assumptions? Identify the shared variable and each text's inferential task before comparing outcomes.
- Does one text deny an antecedent that another merely grants for argument, or do they genuinely make competing assertions about the same scenario? Preserve each owner's commitment.
- Which result changes because the mechanism, object, scope or background changes, and which result remains robust? Do not infer revision from a shared conditional phrase alone.
- What supports chronology or transmission between the texts, and what is only a useful comparison? A shared year or input order cannot establish an intellectual development.

Answer: `[CX6.F<n>] <the comparable supposition and its role in each text> — dim: suppositions_across_texts — shared-variable: <condition compared> — background: <comparable and changed assumptions> — antecedent-status: <denied, open or granted in each text> — relation: continuity|changed_role|qualified_result|different_scope|incompatibility|unsettled — uptake-basis: <explicit link, dated order, or comparison only> — anchor: "<verbatim A>" — doc: <A> — anchor-b: "<verbatim B>" — doc-b: <B> — confidence: high|medium|low`

Do: Keep the two local arguments intact. An antecedent granted to test robustness is not an
empirical endorsement that can simply contradict another text's historical denial. Trace changes
in inferential use separately from changes in belief. Retain complete paired anchors and doc
keys in every corpus descendant. Do not manufacture an alternative history, continuity or
retraction to make the texts form a sequence. Report comparison limits and unsupported links. Read earlier caution before positing later sobriety. Preserve slavery versus later industrial-capitalist scope and any Abrahamic or practical qualification with additional anchored rows if needed.

Indicators: same supposition with another function; repeated concession; explicit revision; different background assumptions.

### Method card and delivery

Examine the suppositions that do argumentative work in the text, if any. Distinguish an
explicit counterfactual, an open conditional, an even-if concession, a reductio, and an
analyst's reconstruction of a dependency. Preserve who makes the supposition, what is
varied or granted, what is held fixed, and what conclusion is claimed. Assess the
connecting warrant appropriate to the case: conceptual, causal, historical, or normative.
Identify additional assumptions and independent support that survives their removal.
Report no relevant instance when the inspected material supports that conclusion,
stating the scope and limits of the search.

Eligibility:
A supposition qualifies when varying, granting or assuming a condition performs an
identifiable inferential task. Include explicit counterfactuals, open conditionals,
even-if concessions, reductios and justified reconstructions of dependency, while keeping
those forms distinct. Every causal sentence is not automatically a necessary but-for claim.
No explicit counterfactual wording is narrower than no relevant supposition. Do not create
an analyst's arbitrary scenario merely to avoid a negative finding.

Keep canonical finding IDs consistent in prose and the final ledger. If final IDs change,
use them in every prose citation and preserve original IDs in from fields. Every corpus
comparison and descendant retains complete anchors from both source keys.
1. State the most consequential supported supposition and what it tests. Give a compact
   inventory distinguishing counterfactuals, open conditionals, concessions, reductios and
   analyst reconstructions, with each owner's actual commitment and the consequent's modality.
2. Explain what is varied or granted and what remains fixed. Expose additional assumptions
   without requiring an alternate history when the argument is conceptual or normative.
3. Trace the inferential bridge, its supporting passage and the missing step if one remains.
   Distinguish necessity, vulnerability, tendency and possibility; retain limiting conditions.
4. Examine the strongest relevant alternative under comparable conditions. State when the
   comparison changes the object or background, and mark a reader's proposed test as such.
5. Withdraw the disputed premise or extra change and show the surviving argument. Separate
   losing a formulation, losing a route and losing every route; preserve independent grounds
   and distinguish the paper's criticism from the success of its constructive alternative.
6. For a corpus, establish each document's scenario and then compare shared conditions,
   changed roles and qualified outcomes. Keep all source outcomes visible and qualify claims
   of chronology or uptake. End with what the material settles and the one unresolved test
   that matters most, without inventing a probability or a required casualty.
Tables: scenarios lists owner, kind, antecedent status, consequent and function; dependencies
lists changed and fixed conditions, bridge and supported scope; robustness lists withdrawn
premise, affected route, independent support and surviving conclusion. Name finding IDs in
every row; omit a table that has no supported material rather than populating it speculatively.
A scoped negative or inconclusive outcome requires the separate scope report:
what was sought, what was inspected, why no relevant instance was retained, review state
and limits. No fabricated normal ledger or scenario is permitted. Follow the
scoped-outcome contract supplied in this prompt.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## A5 — Development through tensions (`dialectical_structure`)

### Ideal output

A one-page account of the central tension and its handling: both owned and scoped positions, what can or cannot coexist, the warranted transition, what is preserved, and the remainder. Desks lift relations, transitions and remainders. An adequate distinction or continuing mediation is a positive finding; no forced progress.

Scope: One text with developed positions or a sequence of supplied texts; include all sides of any claimed contradiction.

Answer contract: Positions with ownership and scope, relation type, mediation or attempted resolution, retained/lost content and anchors.

### Existing questions and demonstrated repairs

Source engines: `dialectical_structure`.

Preserved coverage: Tension networks; binary exclusions; productive conflict; resolution and displacement; recurrence without forced progress.

Keep the candidate’s five document dimensions and corpus comparison. Correct Ganzinger existence versus adequacy of conceptual proof, Elling normative illness versus resultant parabasis, Zambrana phantom/real appearance, Castoriadis local technical neutrality versus social constitution, and unwarranted compatibility of an unknown fragment.

### Dimensions, answer shapes and cards

#### positions_and_attribution (document)

- Which opposed positions or requirements does the text actually juxtapose? State their shared object and the argumentative work their relation performs; do not infer an opposition from vocabulary alone.
- Who undertakes each position here: this paper, an interpreted thinker, a rival as represented by the paper, or a hypothetical interlocutor? What passage supports that attribution, and does the paper endorse, criticize or provisionally grant it?
- Is a quotation direct evidence of a thinker's position or another interpreter's report or criticism of it? Preserve that mediation and distinguish the author's reconstruction from a distinction expressly made in the interpreted work.
- Do the formulations concern the same time, respect, level and stage of the argument? Identify the limiting clauses before treating them as a pair of commitments.

Answer: `[DS1.F<n>] <the organizing relation and its argumentative role> — dim: positions_and_attribution — relation: <stable relation label> — position-a: <scoped claim> — owner-a: <owner and endorsement status> — position-b: <scoped claim> — owner-b: <owner and endorsement status> — attribution-basis: <direct, mediated, hypothetical, or reconstruction; passage> — anchor: "<verbatim A>" — doc: <key> — anchor-b: "<verbatim B, when separate>" — doc-b: <key> — confidence: high|medium|low`

Do: Reconstruct before classifying. Locate each formulation and its owner in the immediate
discussion. A quoted criticism belongs to the critic unless the text supplies the criticized
party's own statement. Mark grants and objections as such. Align the object, modality and
stage; retain disagreements between interpreters without assigning every view to the paper.

Indicators: whereas; according to; on this reading; the objection is; we distinguish.

#### kind_of_opposition (document)

- Under the owners, object, respect and modality just identified, what would make the two formulations incompatible? State the conflict, or explain how the qualifications allow both to hold.
- Does the claimed conflict concern asserted propositions, the relation between an act and its characterization, practical requirements, or different levels of description? Which passages warrant that classification?
- Does the text distinguish appearance from independence, necessary exposure from inevitable realization, or a presupposed starting point from a derived result? Test the distinction before alleging contradiction.
- Is incompatibility the paper's finding, an opponent's allegation, or the analyst's reconstruction? What evidence could discriminate these readings within the supplied text?

Answer: `[DS2.F<n>] <what the pair can or cannot jointly sustain> — dim: kind_of_opposition — relation: <stable label> — kind: contradiction|performative_conflict|practical_tension|qualified_compatibility|unsettled — same-respect: <object, owner, stage and modality check> — qualification: <operative distinction or none stated> — claim-owner: <paper, attributed position, or analyst> — anchor: "<first formulation>" — doc: <key> — anchor-b: "<second formulation or qualification>" — doc-b: <key> — confidence: high|medium|low`

Do: Specify what excludes what only when exclusion is established. For a performative conflict,
name what the act does and what its characterization denies; do not substitute a sentential
contradiction. For practical tension, explain the difficulty of jointly realizing requirements
without asserting logical impossibility. A scope distinction may resolve an apparent conflict;
examine its adequacy rather than treating either the distinction or the contradiction as automatic. Keep phantom and real appearance in their stated relation: a grounding or contrast does not automatically resolve their tension. Distinguish normative illness from the parabasis it results in.

Indicators: contradiction; at the same time; in this respect; appearance; not necessarily.

#### response_and_transition (document)

- Where does the text reject, distinguish, revise, mediate or preserve the relation? Quote the passage that performs the response rather than merely announcing its name.
- What is retained, changed or relinquished, and at which argumentative stage? Is the result asserted as a local repair, a broader explanation, or complete resolution?
- What premise licenses this particular transition? Does showing that the starting formulation fails establish the proposed successor, or does a further argument supply that step?
- If the transition is challenged, which downstream route is affected and which independently supported claims remain? Do not make the success of one derivation necessary for every conclusion.

Answer: `[DS3.F<n>] <response and what it establishes> — dim: response_and_transition — relation: <stable label> — response: distinction|rejection|revision|mediation|preservation|unsettled — retains: <what> — changes: <what> — warrant: <stated or reconstructed bridge and its support> — affected-route: <route whose support changes> — independent-support: <remaining grounds or not established> — anchor: "<transition passage>" — doc: <key> — anchor-b: "<warrant or limiting passage, if available>" — doc-b: <key> — confidence: high|medium|low`

Do: Trace a transition as an inference, not a compulsory thesis-antithesis-synthesis sequence.
Separate the negative result about the initial position from the positive case for its replacement.
Identify the bridge in the paper's terms; mark a reconstructed bridge as the analyst's work.
Keep conceptual, historical and normative premises distinct. Failure of a conceptual reconstruction
does not erase separately supplied historical evidence. Find the conceptual derivation before saying proof is absent; separately judge whether its bridge is adequate. Do not include an opponent premise rejected in the derivation among its positive grounds.

Indicators: therefore; must be understood; rather; preserves; mediates.

#### dependence_and_self_application (document)

- Which specific resource from an opposed position does the argument use, and what precisely does its criticism reject? Quote both the use and the scope of rejection.
- Does the text acknowledge selective appropriation or distinguish a method from its prior application? What would make that use compatible or incompatible with its criticism?
- Where does the argument state a standard and apply it to its own claims? Is a difference in application warranted by different objects or evidential burdens?
- If the borrowed resource is withdrawn, which formulation or argument route fails? Can another stated resource support the conclusion without adopting the opposed position wholesale?

Answer: `[DS4.F<n>] <a reliance or self-application and its actual consequence> — dim: dependence_and_self_application — relation: <stable label> — resource: <specific premise, method or concept> — criticism-scope: <what is rejected> — application: acknowledged_appropriation|consistent_application|scoped_difference|conflict|unsettled — affected-route: <specific dependence> — surviving-route: <independent grounds or not established> — anchor: "<use or standard>" — doc: <key> — anchor-b: "<rejection or application>" — doc-b: <key> — confidence: high|medium|low`

Do: Test immanent criticism against the standard actually undertaken. Borrowing a distinction does
not entail accepting its originator's system or verdict. Locate the paper's account of appropriation
and assess that account before alleging dependence it cannot acknowledge. Do not infer motives,
embarrassment or concealment. Distinguish grounds the paper uses from commitments incurred by
accepting the conclusion; an independent route can survive withdrawal of those grounds.

Indicators: drawing on; against this interpretation; by its own criterion; nevertheless; on other grounds.

#### remainder_and_consequence (document)

- What does the paper say remains unresolved after its response, and what passage resists the claimed extent of resolution? Distinguish acknowledged limits from a reader's proposed objection.
- Does continuing mediation count as the stated result, or does the argument claim to remove the conflict permanently? Assess it against its actual claim.
- What conceptual or practical consequence follows at the supported modal strength? Does a necessary vulnerability leave its realization contingent?
- Which open question could test the response using the paper's own material? State when an answer would require evidence beyond the supplied text.

Answer: `[DS5.F<n>] <what remains and what follows> — dim: remainder_and_consequence — relation: <stable label> — resolution-scope: local_distinction|revised_position|continuing_mediation|complete_resolution_claim|unsettled — remainder: <acknowledged limit or evidenced challenge> — consequence: <scoped and modal conclusion> — text-or-reader: <paper, attributed view, or proposed test> — anchor: "<claimed result or limit>" — doc: <key> — anchor-b: "<resisting or qualifying passage, if available>" — doc-b: <key> — confidence: high|medium|low`

Do: Preserve a remainder without inventing one. Read the conclusion and its qualifications together;
an account of continuing fragility need not promise final reconciliation. Keep risk, necessity,
possibility and actuality distinct. A missing implementation program does not refute a limited
conceptual result. Explain the concrete unresolved burden and whose burden it is. An unknown fragment supplies no evidence that two requirements are jointly preserved. Use an inconclusive scope outcome when the decisive content is missing.

Indicators: remains; even when; threat; cannot settle; beyond the scope.

#### relations_across_texts (corpus)

- Which documents address a comparable relation, and which owners, objects, modalities and argumentative stages make the comparison warranted? Shared terminology alone is insufficient.
- Does the second treatment retain, qualify, revise or refuse a position or response? Can more than one relation hold, such as continuity with a changed argumentative use?
- Does an apparent incompatibility survive each text's qualifications? Distinguish opposing claims from changed questions, local versus social scope, or enabling conditions versus sufficient outcomes.
- What establishes chronology or uptake: composition and edition information, an explicit reference, or only resemblance? State the limit; input order and shared year do not establish development.

Answer: `[DX6.F<n>] <relation and response in each text> — dim: relations_across_texts — relation: <stable label> — comparison: continuity|qualification|revision|refusal|scoped_difference|incompatibility|unsettled — comparable-scope: <owners, objects, modalities and stages> — uptake-basis: <explicit link, dated order, or resemblance only> — anchor: "<verbatim A>" — doc: <A> — anchor-b: "<verbatim B>" — doc-b: <B> — confidence: high|medium|low`

Do: Establish each text's local position before drawing a relation across them. Always retain two
complete anchors with different doc keys, including in descendants and synthesis. Compare the
argument attached to a term, not its spelling alone. Distinguish local technical competence from
global neutrality, opposition from an unintended enabling effect, and selective uptake from
conversion. A claim of omission needs inspected scope and cannot be proved by two snippets. Local technical neutrality can coexist with the social constitution of technical choices; preserve the local qualification in the finding, not only surrounding prose.

Indicators: explicit self-citation; revised application; shared object with changed scope; dated editions.

### Method card and delivery

Examine which opposed positions or requirements, if any, organize the text's argument.
Identify each position's owner, object, scope, modality, and argumentative stage. Determine
whether their relation is a contradiction, a performative conflict, a practical tension,
or compatibility clarified by a distinction. Trace how the text rejects, revises, mediates,
or preserves the relation, and assess the warrant for that response and what remains
unresolved. Selective borrowing and differences between stages may be coherent. Report no
relevant instance when the inspected material supports that conclusion, stating the scope
and limits of the search.

Eligibility:
A relation qualifies when the text juxtaposes or relies on distinguishable positions or
requirements and their relation does argumentative work. Qualified compatibility,
acknowledged appropriation and continuing mediation can be positive findings. A shared
word, any difference between sentences, or the absence of an unrecognized contradiction
does not by itself establish or exclude a relevant dialectical relation.

Keep canonical finding IDs consistent in prose and the final ledger. If final IDs change,
cite those final IDs throughout and preserve the original IDs in from fields. Keep two
source-keyed anchors on every corpus relation and its descendants.
1. Lead with the central supported relation and the paper's response, at its actual scope.
   Explain whether it is a contradiction, performative conflict, practical tension or a
   distinction allowing compatibility. Do not manufacture a hidden contradiction.
2. Present the positions and their owners, with the qualifications that make the relation
   intelligible. For a corpus, give each document's local argument briefly before the comparison.
3. Follow the response: what changes, what is retained, and which premise warrants the move.
   Separate failure of a starting formulation from proof of this particular successor.
4. Test dependence and self-application where they matter. Preserve coherent selective
   appropriation and identify independent routes that survive a challenged premise.
5. State what remains, the consequence supported, and the strongest unresolved question.
   Continuing mediation may be the result; do not replace it with a promised final synthesis.
6. For a corpus, trace the evidenced continuity, qualification or change, retaining both
   sources and explicit limits on chronology and uptake. Do not force a development narrative.
Tables: relations lists positions, owners, scope and relation type; transitions lists response,
retained and changed elements, warrant and affected route; remainders lists resolution scope,
remaining burden, consequence and text-versus-reader status. Each row names its finding IDs.
The separate scope report must state the search,
inspected scope, negative or inconclusive result, review state and uncertainty. Do not create
normal findings or tables merely to fill the positive-output template. Follow the
scoped-outcome contract supplied in this prompt.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## A6 — Possibility, necessity and certainty (`modal_force_inventory`)

### Ideal output

An operator inventory a reader can inspect: exact proposition and owner, must/may/cannot/ought or epistemic hedge, type and scope, supporting warrant, justified force and available alternative. Lead with the most consequential force distinction. Desks lift modal-claim and force-change tables; useful coverage is the product, with no compulsory discovery of equivocation.

Scope: Text containing modal claims or thought experiments; extra evidence only when the claim invokes it.

Answer contract: Claim, exact operator, modality kind, scope, warrant, justified force and alternatives or unknowns.

### Existing questions and demonstrated repairs

Source engines: `modal_reasoning_analyzer`, `epistemic_stance`, `imagination_failure_detector`.

Preserved coverage: Epistemic markers; alethic/deontic distinctions; warranted grades of necessity; thought experiments; threshold claims; inconceivability versus impossibility.

Merge modal reasoning, epistemic stance and imagination failure. Preserve operator, type, thought-experiment and threshold probes. Replace mandatory deductive proof, arbitrary ignored branches and mental incapacity with warrant-appropriate checks and supplied alternatives.

### Dimensions, answer shapes and cards

#### operators (document)

- What does the text claim must be the case, and what kind of necessity is invoked? **Preserved verbatim.**
- What does the text claim could be different, and how is this possibility established? **Preserved verbatim.**

Answer: `[D1.F<n>] <one scoped finding> — dim: operators — claim: <owned proposition> — operator: <exact words> — kind: <epistemic, alethic, deontic, practical> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Keep the operator with its proposition and owner. Inventory uncertainty as well as necessity; a quoted opponent is not the paper’s commitment.

Indicators: must; may; cannot; ought; probably.

#### scope (document)

- What object, quantifier, condition and time fall under each modal operator?
- Does a necessary exposure or capacity leave actual realization contingent?

Answer: `[D2.F<n>] <one scoped finding> — dim: scope — claim: <proposition> — quantifier: <scope> — condition: <if clause> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Bracket the operator’s scope explicitly. Separate necessity of vulnerability, frequency of realization and probability of a particular outcome.

Indicators: always; if; liable to; sometimes.

#### warrant (document)

- Does the text distinguish between different grades of necessity and possibility? **Preserved verbatim.**
- What conceptual, empirical, normative or practical warrant supports this exact force?

Answer: `[D3.F<n>] <one scoped finding> — dim: warrant — claim: <proposition> — warrant: <passage and kind> — justified-force: <assessment> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Assess the argument actually offered; conceptual necessity need not have frequency data. Separate an absent derivation from one present but inadequate.

Indicators: because; by definition; evidence suggests.

#### force_changes (document)

- Are modal operators used consistently, or do they shift meaning across contexts? **Preserved verbatim.**
- Does an alleged change concern the same proposition and conditions, or a distinct claim?

Answer: `[D4.F<n>] <one scoped finding> — dim: force_changes — claim: <aligned proposition> — first-force: <operator> — second-force: <operator> — reason: <scope relation> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Pair both formulations and retain their conditions. Do not infer is-to-ought or epistemic-to-metaphysical drift from adjacent vocabulary alone.

Indicators: could; therefore must; ought.

#### possibility_tests (document)

- What background assumptions does the scenario take for granted? **Preserved verbatim.**
- Does conceivability in the thought experiment genuinely establish possibility? **Preserved verbatim.**
- Which alternative does the text itself consider, and does it vary the condition relevant to this claim?

Answer: `[D5.F<n>] <one scoped finding> — dim: possibility_tests — scenario: <test> — background: <fixed conditions> — supports: <modal conclusion> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Distinguish a coherent conceptual counterexample from a historical forecast. Lack of an imagined alternative proves no impossibility.

Indicators: imagine; suppose; even if.

#### thresholds (document)

- Where does the text assert a sharp boundary between categories? **Preserved verbatim.**
- Does the text acknowledge vagueness and gradual transitions, or does it impose false precision? **Preserved verbatim.**

Answer: `[D6.F<n>] <one scoped finding> — dim: thresholds — boundary: <threshold> — criterion: <rule> — consequence: <modal role> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Record only boundaries that do work; assess their criterion using supplied cases. No arbitrary numerical cutoff or forced sorites criticism.

Indicators: only when; enough; threshold.

#### modal_comparison (corpus)

- Which aligned proposition has a different modal force or warrant in another supplied work?
- Which difference disappears once conditions and owners are preserved?

Answer: `[X7.F<n>] <one scoped finding> — dim: modal_comparison — relation: <aligned relation> — alignment: <object, sense, owner, scope> — order-basis: <dates, uptake, or unordered> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — anchor-b: "<verbatim supporting clause B>" — doc-b: <different source key> — confidence: high|medium|low`

Do: Pair propositions and their qualifiers. A changed confidence level need not be changed meaning or evidence of intellectual development.

Indicators: explicit reference; paired formulations; scope qualification.

### Method card and delivery

An operator inventory a reader can inspect: exact proposition and owner, must/may/cannot/ought or epistemic hedge, type and scope, supporting warrant, justified force and available alternative. Lead with the most consequential force distinction. Desks lift modal-claim and force-change tables; useful coverage is the product, with no compulsory discovery of equivocation. Merge modal reasoning, epistemic stance and imagination failure. Preserve operator, type, thought-experiment and threshold probes. Replace mandatory deductive proof, arbitrary ignored branches and mental incapacity with warrant-appropriate checks and supplied alternatives.

1. An operator inventory a reader can inspect: exact proposition and owner, must/may/cannot/ought or epistemic hedge, type and scope, supporting warrant, justified force and available alternative. Lead with the most consequential force distinction. Desks lift modal-claim and force-change tables; useful coverage is the product, with no compulsory discovery of equivocation.
2. Establish the most consequential local findings and their qualifications; organize the reading by the objects and claims in these texts.
3. Render the named Markdown tables with final finding IDs in every positive cell. Explain the supported relation and the strongest counter-passage; end with what is settled and the exact remaining question.
4. With multiple sources, build each work’s inventory before the paired comparison, and state alignment and chronology limits. With one source, label the result a local inventory where a corpus relation would require another work.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## C1 — Meaning in use (`meaning_in_use`)

### Ideal output

A compact usage lexicon with term, local sense, contrasting or neighboring term, defining boundary, passage and interpretive consequence. A second table pairs apparently inconsistent uses and explains genuine ambiguity versus scope or voice changes. Desks lift both tables. Report stable, precise use when it holds.

Scope: One text or comparable usage passages; disciplinary reference material if making a standard-usage comparison.

Answer contract: Term, sense, context, semantic neighbor or contrast, boundary, paired uses and consequence for interpretation.

### Existing questions and demonstrated repairs

Source engines: `concept_semantic_constellation`, `concept_semantic_field`, `conceptual_anomaly_detector`, `reification_detector`.

Preserved coverage: Synonyms and opposites; collocations; semantic fields; ambiguity; connotations; baseline-relative anomalies; reification and literalization checks.

Merge the mapped semantic and reification engines. Preserve synonyms, opposites, collocations, boundary, usage and connotation probes. Replace disciplinary anomalies without a baseline, strategic ambiguity and predicted emotional responses with textual comparisons; causation assigned to an abstraction requires checking its specified agents.

### Dimensions, answer shapes and cards

#### senses (document)

- Is the concept's actual usage consistent with its stated definition? **Preserved verbatim.**
- Which distinct senses are supported by the surrounding predicates and examples?

Answer: `[D1.F<n>] <one scoped finding> — dim: senses — term: <term> — sense: <meaning> — context: <owned use> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory actual use beside definitions. Keep quoted rivals and the paper’s own senses separate.

Indicators: means; defined as; in this sense.

#### neighbors (document)

- What terms does the author use as near-synonyms -- and what subtle distinctions does the author draw between them? **Preserved verbatim.**
- What antonyms or contrasts define the concept negatively -- what it is NOT? **Preserved verbatim.**
- What terms habitually co-occur with the concept (collocations), and what do these associations reveal? **Preserved verbatim.**

Answer: `[D2.F<n>] <one scoped finding> — dim: neighbors — term: <term> — neighbor: <term> — relation: <stated or inferred> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Anchor both terms and the relation in context. Co-occurrence alone establishes no synonymy or causal link.

Indicators: rather than; also called; paired terms.

#### boundaries (document)

- Where are the boundaries between related concepts sharp and explicit? **Preserved verbatim.**
- Where are boundaries fuzzy or contested -- and does the author acknowledge the fuzziness? **Preserved verbatim.**

Answer: `[D3.F<n>] <one scoped finding> — dim: boundaries — terms: <pair> — boundary: <criterion> — edge-case: <source example> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Use membership and contrast criteria the text supplies. Preserve acknowledged uncertainty without assigning strategic intent.

Indicators: distinguish; borderline; not merely.

#### paired_usage (document)

- Does the concept's meaning shift across different parts of the work? **Preserved verbatim.**
- Does the concept function differently in positive arguments vs. critiques of others? **Preserved verbatim.**

Answer: `[D4.F<n>] <one scoped finding> — dim: paired_usage — term: <term> — use-a: <meaning and owner> — use-b: <meaning and owner> — effect: <interpretive consequence> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Pair passages before diagnosing equivocation. A changed object, quotation or application can explain different predicates without changing sense.

Indicators: earlier definition; later application; quoted criticism.

#### connotations (document)

- What evaluative connotations attach to key terms -- positive, negative, neutral? **Preserved verbatim.**
- Which wording makes an evaluation part of a description, and does it affect the inference?

Answer: `[D5.F<n>] <one scoped finding> — dim: connotations — term: <term> — evaluation: <wording> — function: <local work> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Locate evaluation in modifiers and contrasts. Do not predict a reader’s feelings or assert disciplinary deviation without a supplied baseline.

Indicators: mere; rational; distorted; liberation.

#### literalization (document)

- Where does the text attribute action or causal power to an abstraction, and what agents or mechanism does it specify?
- Which metaphor is used literally, and which passage establishes that rather than ordinary shorthand?

Answer: `[D6.F<n>] <one scoped finding> — dim: literalization — term: <abstraction> — predicate: <action> — mechanism: <specified or unresolved> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Check the surrounding account before alleging reification. A social relation or collective mechanism may legitimately be the causal object.

Indicators: capital demands; society acts; as if.

#### usage_comparison (corpus)

- Which paired usage passages show the same or different sense under comparable objects?
- Is a claimed anomaly relative to an explicitly supplied baseline, or merely a difference?

Answer: `[X7.F<n>] <one scoped finding> — dim: usage_comparison — relation: <aligned relation> — alignment: <object, sense, owner, scope> — order-basis: <dates, uptake, or unordered> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — anchor-b: "<verbatim supporting clause B>" — doc-b: <different source key> — confidence: high|medium|low`

Do: Compare uses without imposing a standard from memory. Retain source ownership and scope on both sides.

Indicators: explicit reference; paired formulations; scope qualification.

### Method card and delivery

A compact usage lexicon with term, local sense, contrasting or neighboring term, defining boundary, passage and interpretive consequence. A second table pairs apparently inconsistent uses and explains genuine ambiguity versus scope or voice changes. Desks lift both tables. Report stable, precise use when it holds. Merge the mapped semantic and reification engines. Preserve synonyms, opposites, collocations, boundary, usage and connotation probes. Replace disciplinary anomalies without a baseline, strategic ambiguity and predicted emotional responses with textual comparisons; causation assigned to an abstraction requires checking its specified agents.

1. A compact usage lexicon with term, local sense, contrasting or neighboring term, defining boundary, passage and interpretive consequence. A second table pairs apparently inconsistent uses and explains genuine ambiguity versus scope or voice changes. Desks lift both tables. Report stable, precise use when it holds.
2. Establish the most consequential local findings and their qualifications; organize the reading by the objects and claims in these texts.
3. Render the named Markdown tables with final finding IDs in every positive cell. Explain the supported relation and the strongest counter-passage; end with what is settled and the exact remaining question.
4. With multiple sources, build each work’s inventory before the paired comparison, and state alignment and chronology limits. With one source, label the result a local inventory where a corpus relation would require another work.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## C6 — Frameworks and their components (`framework_components`)

### Ideal output

A framework map showing the inquiry, attributed lens, components, relations and one worked application. Lead with what the composition makes visible and a source-evidenced limit; distinguish a named tradition from an inferred profile. Desks lift component–relation and application–limit tables; an optional source-search profile is made of passages, never a biography.

Scope: One text or a supplied collection; a genealogy profile is a declared output mode with hypotheses tagged.

Answer contract: Framework, evidence for attribution, components and relations, applications, limits, alternatives and source passages.

### Existing questions and demonstrated repairs

Source engines: `conceptual_framework_extraction`, `concept_taxonomy_theoretical_register`, `genealogy_pass1_idea_extraction`, `interdisciplinary_connection`, `paradigm_boundary_mapper`, `paradigm_departure_analyzer`.

Preserved coverage: Vocabulary and method profile; theoretical registers; conceptual architecture; cross-disciplinary translations; paradigm boundaries and departures; source-search profile.

Merge the mapped framework engines. Preserve vocabulary/method profile, architecture, translations and boundaries. Replace fixed school registers, training inference, forgotten metaphors and unsupplied precursors with attributed lenses and explicit hypotheses; inventory components rather than narrating theory construction.

### Dimensions, answer shapes and cards

#### attribution (document)

- Which framework does the text name as organizing its inquiry, and what passage enacts it?
- What theoretical register is inferred from vocabulary or method, and what makes that only a hypothesis?

Answer: `[D1.F<n>] <one scoped finding> — dim: attribution — framework: <name or descriptive lens> — attribution: <declared or hypothesis> — inquiry: <object> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Attribute named frameworks from passages; an inferred profile needs vocabulary and method evidence. Do not force the text into a school checklist.

Indicators: following; framework; we approach.

#### components (document)

- What terms does the author coin or use distinctively? **Preserved verbatim.**
- What key oppositions structure the argument, and what local definition does each component have?

Answer: `[D2.F<n>] <one scoped finding> — dim: components — framework: <lens> — component: <concept> — definition: <scope> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory components as the text defines them. Standard usage needs supplied reference material before a deviation can be claimed.

Indicators: defined as; opposed to; component.

#### relations (document)

- Which frameworks are foundational -- everything else depends on them? **Preserved verbatim.**
- Do any frameworks compete with each other -- offering alternative explanations for the same phenomena? **Preserved verbatim.**
- What passage links component A to B, and what conclusion relies on that link?

Answer: `[D3.F<n>] <one scoped finding> — dim: relations — components: <nodes> — relation: <premise, mechanism, constraint> — support: <passage> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Prove a dependency by the argument route, not frequency. Test competing lenses on the same object and preserve independent routes.

Indicators: requires; constitutes; alternative explanation.

#### method_profile (document)

- What types of evidence does the author rely on (historical narrative, data, theoretical derivation, analogy, case study, thought experiment)? **Preserved verbatim.**
- What analytical move applies these components to the object, and what does it establish?

Answer: `[D4.F<n>] <one scoped finding> — dim: method_profile — framework: <lens> — procedure: <move> — evidence: <kind> — result: <claim> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Give an enacted example; keep studied, advocated and used methods apart. Avoid judging a conceptual derivation by an empirical checklist.

Indicators: we examine; derive; apply.

#### translations (document)

- What concepts, methods, or analogies are imported from other fields? **Preserved verbatim.**
- How have imports been adapted for the current domain -- what was changed and what was preserved? **Preserved verbatim.**

Answer: `[D5.F<n>] <one scoped finding> — dim: translations — import: <component> — source-domain: <stated or hypothesis> — adaptation: <change> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Anchor the origin as stated and the local use. Mark unverified provenance; no inference to training or unconscious influence.

Indicators: borrow; adapt; analogy with.

#### limits (document)

- How is the central problem or question framed -- what does this framing make visible and invisible? **Preserved verbatim.**
- Which supplied application or rival interpretation tests a boundary the framework states?

Answer: `[D6.F<n>] <one scoped finding> — dim: limits — framework: <lens> — application: <case> — limit: <qualification> — alternative: <source view> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Ground visibility in an actual finding and limits in a bracket or counter-passage. An unasked question is not automatically impossible within the framework.

Indicators: beyond our scope; cannot explain; alternative.

#### framework_comparison (corpus)

- Which supplied works use comparable components and what relation or application differs?
- Which paired passage supports continuity, translation or an unresolved framework conflict?

Answer: `[X7.F<n>] <one scoped finding> — dim: framework_comparison — relation: <aligned relation> — alignment: <object, sense, owner, scope> — order-basis: <dates, uptake, or unordered> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — anchor-b: "<verbatim supporting clause B>" — doc-b: <different source key> — confidence: high|medium|low`

Do: Compare local architectures under aligned objects. Preserve uncertainty in inferred attribution and do not turn resemblance into influence.

Indicators: explicit reference; paired formulations; scope qualification.

### Method card and delivery

A framework map showing the inquiry, attributed lens, components, relations and one worked application. Lead with what the composition makes visible and a source-evidenced limit; distinguish a named tradition from an inferred profile. Desks lift component–relation and application–limit tables; an optional source-search profile is made of passages, never a biography. Merge the mapped framework engines. Preserve vocabulary/method profile, architecture, translations and boundaries. Replace fixed school registers, training inference, forgotten metaphors and unsupplied precursors with attributed lenses and explicit hypotheses; inventory components rather than narrating theory construction.

1. A framework map showing the inquiry, attributed lens, components, relations and one worked application. Lead with what the composition makes visible and a source-evidenced limit; distinguish a named tradition from an inferred profile. Desks lift component–relation and application–limit tables; an optional source-search profile is made of passages, never a biography.
2. Establish the most consequential local findings and their qualifications; organize the reading by the objects and claims in these texts.
3. Render the named Markdown tables with final finding IDs in every positive cell. Explain the supported relation and the strongest counter-passage; end with what is settled and the exact remaining question.
4. With multiple sources, build each work’s inventory before the paired comparison, and state alignment and chronology limits. With one source, label the result a local inventory where a corpus relation would require another work.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## S3 — Narrative form and perspective (`narrative_form_perspective`)

### Ideal output

A one-page account of how sequence and viewpoint shape this text: local arc or limited narration, presentation order versus narrated time, voices and access, the turn that changes the reader’s understanding, and what the ending settles. Desks lift sequence–effect and perspective–evidence tables. Academic exposition may contain only local narratives.

Scope: A text or comparable narrative passages, allowing an absent or limited narrative structure.

Answer contract: Arc or local sequence, voice/register, focalizer, narrated versus presented time, device and anchored interpretive effect.

### Existing questions and demonstrated repairs

Source engines: `narrative_structure_analyzer`, `narrative_transformation`.

Preserved coverage: Emplotment without a closed label set; register; perspectives; tension; actants and narrative programs where applicable; temporal construction.

Merge narrative structure and transformation. Preserve turns, closure, register, focalization, devices and temporal questions. Replace closed emplotment labels and deliberate/unconscious shifts with source-specific effects; actants and narrative programs are optional descriptions when supported, not mandatory categories.

### Dimensions, answer shapes and cards

#### sequence (document)

- Where are the narrative turning points — crises, reversals, revelations? **Preserved verbatim.**
- What situation opens the account, what changes it, and is there a sustained arc or only a local sequence?

Answer: `[D1.F<n>] <one scoped finding> — dim: sequence — sequence: <opening, turn, result> — extent: <local or sustained> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Read the actual order of presentation; distinguish events from the order of an exposition. Do not impose romance, tragedy or a closed plot.

Indicators: initially; then; turning point.

#### perspective (document)

- Whose perspective does the narrator primarily adopt? **Preserved verbatim.**
- Where does focalization shift, and what wording or access to experience marks the shift?

Answer: `[D2.F<n>] <one scoped finding> — dim: perspective — voice: <speaker> — focalizer: <whose access> — shift: <passage> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Separate narrator, quoted voice and represented experience. Omitted testimony limits access; it does not establish a deliberately excluded viewpoint.

Indicators: we; they experienced; according to.

#### time (document)

- What is the text's dominant temporality? **Preserved verbatim.**
- What time scales are deployed and for what purposes? **Preserved verbatim.**
- How does it construct the relationship between past, present, and future? **Preserved verbatim.**

Answer: `[D3.F<n>] <one scoped finding> — dim: time — presented-order: <sequence> — narrated-time: <dates or scale> — effect: <local implication> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Anchor dates, retrospection and anticipation. A sequence can suggest causation without evidencing it; keep those claims distinct.

Indicators: before; by now; would later.

#### register (document)

- What registers does the author deploy and where? **Preserved verbatim.**
- Do different registers serve different argumentative functions? **Preserved verbatim.**

Answer: `[D4.F<n>] <one scoped finding> — dim: register — register: <passage-specific description> — transition: <where> — function: <work> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Show a wording change and its local function. Do not infer whether the change was deliberate or unconscious.

Indicators: irony; direct address; technical definition.

#### devices (document)

- What narrative devices does the text deploy? **Preserved verbatim.**
- Which actor seeks what, with which helper or obstacle, where a narrative program is actually developed?

Answer: `[D5.F<n>] <one scoped finding> — dim: devices — device: <device or role> — passage-function: <effect> — evidential-limit: <what it cannot prove> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Use concrete devices such as anticipation, repetition or withheld information only when shown. Narrative agency does not establish causal agency.

Indicators: repeated image; anticipated ending; obstacle.

#### closure (document)

- How does it achieve or refuse closure? **Preserved verbatim.**
- Where do the demands of narrative conflict with the demands of argument? **Preserved verbatim.**

Answer: `[D6.F<n>] <one scoped finding> — dim: closure — ending: <settlement or openness> — tension: <source-supported issue> — consequence: <interpretive effect> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Compare the closure with the evidence and stated question. Open-endedness can be the intended textual result; do not manufacture hidden resolution or author intention.

Indicators: remains; finally; uncertain future.

#### narrative_comparison (corpus)

- How do comparable accounts order the same object or adopt different perspectives?
- Which paired devices explain a difference in presentation without establishing changed historical facts?

Answer: `[X7.F<n>] <one scoped finding> — dim: narrative_comparison — relation: <aligned relation> — alignment: <object, sense, owner, scope> — order-basis: <dates, uptake, or unordered> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — anchor-b: "<verbatim supporting clause B>" — doc-b: <different source key> — confidence: high|medium|low`

Do: Pair the passages and their narrated objects. Report limited comparability; publication order alone is no narrative development.

Indicators: explicit reference; paired formulations; scope qualification.

### Method card and delivery

A one-page account of how sequence and viewpoint shape this text: local arc or limited narration, presentation order versus narrated time, voices and access, the turn that changes the reader’s understanding, and what the ending settles. Desks lift sequence–effect and perspective–evidence tables. Academic exposition may contain only local narratives. Merge narrative structure and transformation. Preserve turns, closure, register, focalization, devices and temporal questions. Replace closed emplotment labels and deliberate/unconscious shifts with source-specific effects; actants and narrative programs are optional descriptions when supported, not mandatory categories.

1. A one-page account of how sequence and viewpoint shape this text: local arc or limited narration, presentation order versus narrated time, voices and access, the turn that changes the reader’s understanding, and what the ending settles. Desks lift sequence–effect and perspective–evidence tables. Academic exposition may contain only local narratives.
2. Establish the most consequential local findings and their qualifications; organize the reading by the objects and claims in these texts.
3. Render the named Markdown tables with final finding IDs in every positive cell. Explain the supported relation and the strongest counter-passage; end with what is settled and the exact remaining question.
4. With multiple sources, build each work’s inventory before the paired comparison, and state alignment and chronology limits. With one source, label the result a local inventory where a corpus relation would require another work.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## E12 — How a theory is built (`theory_construction_analyzer`)

### Ideal output

A construction ledger: problem and scope → inputs → move → resulting concept or mechanism → warrant → limit. Lead with how the text earns its proposed contribution, distinguishing claimed novelty from demonstrated work. Desks lift construction moves and theory–evidence articulation tables; a well-supported inventory is sufficient.

Scope: Text proposing, revising or combining theory; empirical measures only where empirical claims are undertaken.

Answer contract: Construction move, inputs, resulting concept/mechanism, scope, justification, theory–evidence direction and passage.

### Existing questions and demonstrated repairs

Source engines: `theory_construction_analyzer`.

Preserved coverage: Middle-range scope; conceptual transfer; synthesis compatibility; innovation; parsimony/fecundity; empirical articulation where applicable.

Reuse v2. Preserve middle-range scope, conceptual transfer, compatible synthesis, innovation and evidence direction. Replace impossible questions, ungrounded alternative paradigms and nature-at-its-joints tests with supplied problems, distinctions and warrants; empirical operationalization is conditional on empirical claims.

### Dimensions, answer shapes and cards

#### problem_and_scope (document)

- What specific phenomenon does the theory claim to explain? **Preserved verbatim.**
- What scope conditions delimit where the theory applies? **Preserved verbatim.**

Answer: `[D1.F<n>] <one scoped finding> — dim: problem_and_scope — problem: <question> — explanandum: <object> — scope: <conditions> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Record the problem the theory undertakes, including a conceptual problem. Do not demand a general theory from a bounded construction.

Indicators: explain; our concern; applies when.

#### inputs (document)

- What concepts does the text borrow from other domains? **Preserved verbatim.**
- What premises or earlier results does the construction adopt, revise or provisionally grant?

Answer: `[D2.F<n>] <one scoped finding> — dim: inputs — input: <concept or premise> — ownership: <source and status> — use: <job> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Keep inputs attributed and distinguish grants for argument from endorsed foundations. A reference does not import the entire source system.

Indicators: following; assume; borrow.

#### moves (document)

- What mechanisms are proposed to account for the phenomenon? **Preserved verbatim.**
- Which passage derives, abstracts, redefines or combines inputs into that mechanism or concept?

Answer: `[D3.F<n>] <one scoped finding> — dim: moves — move: <operation> — inputs: <premises> — result: <concept or mechanism> — warrant: <bridge> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Trace construction as a sequence of justified moves. A failed old formulation does not by itself prove the proposed replacement.

Indicators: derive; therefore; redefine; combine.

#### synthesis (document)

- What distinct theoretical frameworks does the text combine? **Preserved verbatim.**
- Are the combined frameworks logically compatible? **Preserved verbatim.**
- Where do tensions between frameworks remain unresolved? **Preserved verbatim.**

Answer: `[D4.F<n>] <one scoped finding> — dim: synthesis — inputs: <frameworks> — compatibility: <conditions> — result: <new relation> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Judge compatibility at the level of selected components and their actual assumptions. Selective borrowing can be coherent despite disagreement with the originator.

Indicators: synthesis; complement; tension.

#### contribution (document)

- What new concepts does the text introduce? **Preserved verbatim.**
- What existing concepts, if any, does the innovation replace or supplement? **Preserved verbatim.**
- What analytical work does the new concept enable? **Preserved verbatim.**

Answer: `[D5.F<n>] <one scoped finding> — dim: contribution — contribution: <claimed change> — demonstrated-work: <application> — economy: <what must be retained> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Separate novelty claims from demonstrated use; test parsimony against the text’s own distinctions and fecundity against actual applications. Do not certify field-wide originality.

Indicators: we propose; unlike; allows us.

#### evidence_direction (document)

- What is the direction of inference: evidence to theory, theory to evidence, or iterative? **Preserved verbatim.**
- Where empirical claims are undertaken, how are abstract concepts operationalized into observable indicators?
- Where does a conceptual derivation supply the justification, and which step remains disputed?

Answer: `[D6.F<n>] <one scoped finding> — dim: evidence_direction — direction: <inductive, deductive, iterative> — link: <theory to evidence or derivation> — limit: <scope> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Match the warrant to the construction. A conceptual theory need not have measured indicators; existence of a derivation differs from its adequacy.

Indicators: indicates; derive; illustrate; test.

#### construction_comparison (corpus)

- Which supplied works construct an aligned concept by different inputs or moves?
- Which paired warrants support continuity, revision or a difference of scope?

Answer: `[X7.F<n>] <one scoped finding> — dim: construction_comparison — relation: <aligned relation> — alignment: <object, sense, owner, scope> — order-basis: <dates, uptake, or unordered> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — anchor-b: "<verbatim supporting clause B>" — doc-b: <different source key> — confidence: high|medium|low`

Do: Compare moves with both local arguments intact. Do not infer development, originality or uptake merely from dates or shared vocabulary.

Indicators: explicit reference; paired formulations; scope qualification.

### Method card and delivery

A construction ledger: problem and scope → inputs → move → resulting concept or mechanism → warrant → limit. Lead with how the text earns its proposed contribution, distinguishing claimed novelty from demonstrated work. Desks lift construction moves and theory–evidence articulation tables; a well-supported inventory is sufficient. Reuse v2. Preserve middle-range scope, conceptual transfer, compatible synthesis, innovation and evidence direction. Replace impossible questions, ungrounded alternative paradigms and nature-at-its-joints tests with supplied problems, distinctions and warrants; empirical operationalization is conditional on empirical claims.

1. A construction ledger: problem and scope → inputs → move → resulting concept or mechanism → warrant → limit. Lead with how the text earns its proposed contribution, distinguishing claimed novelty from demonstrated work. Desks lift construction moves and theory–evidence articulation tables; a well-supported inventory is sufficient.
2. Establish the most consequential local findings and their qualifications; organize the reading by the objects and claims in these texts.
3. Render the named Markdown tables with final finding IDs in every positive cell. Explain the supported relation and the strongest counter-passage; end with what is settled and the exact remaining question.
4. With multiple sources, build each work’s inventory before the paired comparison, and state alignment and chronology limits. With one source, label the result a local inventory where a corpus relation would require another work.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.

## A3 — Audit comparisons and analogies (`comparative_reasoning_analyzer`)

### Ideal output

A compact audit ordered by the conclusions that depend on comparison: what is transferred, which correspondence warrants it, where disanalogies matter, and what weaker conclusion survives. The desks lift comparison → conclusion → correspondence → defeating difference → scoped verdict, plus criteria and alternatives. The reading’s categories are the consequential comparisons in this text.

Scope: A text making comparisons; source and target material when the comparison relies on facts outside it.

Answer contract: Comparison, mapped dimension, source/target correspondence, disanalogy, criterion, transfer claim and scoped assessment.

### Existing questions and demonstrated repairs

Source engines: `comparative_reasoning_analyzer`, `concept_vulnerability_false_dichotomies`.

Preserved coverage: Analogical transfer; dichotomy exhaustiveness; scalar endpoints; typologies; evaluative criteria; case representativeness.

Replace the lifted block. Keep text-facing critical questions but regroup them by audit work, not six kinds of device. Replace unsupported case-selection motives, suppressed options and free-floating alternative rankings with source-supported alternatives and explicit analyst tests. Typology, scalar endpoints and dichotomy checks are conditional probes inside the audit.

### Dimensions, answer shapes and cards

#### transfer_claim (document)

- What inferential work does the analogy perform—does it generate predictions, explanations, or evaluations? **Preserved verbatim.**
- Which conclusion depends on which comparison, and is the move illustrative, classificatory or an evidential transfer?

Answer: `[D1.F<n>] <one scoped finding> — dim: transfer_claim — comparison: <items> — conclusion: <claim> — job: <function> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Start with the dependent conclusion and its force. An illustration need not prove a general law; an explanatory transfer needs a warrant.

Indicators: like; similarly; therefore.

#### correspondence (document)

- What specific relations are mapped from source to target domain? **Preserved verbatim.**
- Which attributes of the source domain are transferred versus left behind? **Preserved verbatim.**

Answer: `[D2.F<n>] <one scoped finding> — dim: correspondence — comparison: <items> — correspondence: <mapped relation> — warrant: <why relevant> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Map the relevant relation, not shared adjectives. Give supporting spans for both compared sides; unsupported external facts stay unverified.

Indicators: corresponds; same relation; unlike.

#### defeating_difference (document)

- Where does the analogy break down—which source domain features have no target domain counterpart? **Preserved verbatim.**
- Which stated disanalogy changes the transferred conclusion, and does the text answer it or merely acknowledge it?

Answer: `[D3.F<n>] <one scoped finding> — dim: defeating_difference — comparison: <items> — difference: <scoped disanalogy> — consequence: <effect> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Test a difference for relevance to this transfer. Preserve disanalogies the text actually discusses; inadequate treatment differs from absence.

Indicators: however; unlike; only partially.

#### criterion (document)

- On what criteria are the compared items being evaluated? **Preserved verbatim.**
- How are the endpoints of the scale defined and anchored? **Preserved verbatim.**
- How does the typology handle borderline, mixed, or anomalous cases? **Preserved verbatim.**

Answer: `[D4.F<n>] <one scoped finding> — dim: criterion — comparison: <items> — criterion: <stated or reconstructed> — boundary: <endpoints or types> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Run scale and typology probes only when used. Ask whether the same rule governs both items and whether overlap is allowed, without imposing exclusive categories.

Indicators: more than; best; type; between.

#### alternatives (document)

- Are the two options presented as genuinely exhaustive of the possibility space? **Preserved verbatim.**
- What part, example, or case is made to stand for a larger whole or class? **Preserved verbatim.**
- Which supplied alternative or counter-case tests exhaustiveness or representativeness, and which proposed test needs more evidence?

Answer: `[D5.F<n>] <one scoped finding> — dim: alternatives — comparison: <items> — coverage-claim: <scope> — alternative: <source case or analyst test> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Use the text’s own third cases first. Do not infer case-selection motives or force an illustrative example to be a representative sample.

Indicators: either; all cases; for example; exception.

#### surviving_conclusion (document)

- Once the relevant difference or criterion limit is retained, what conclusion still follows and at what force?
- Which independent route supports the conclusion if this comparison fails?

Answer: `[D6.F<n>] <one scoped finding> — dim: surviving_conclusion — comparison: <items> — supported-result: <qualified claim> — repair: <needed premise or comparison> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Keep a failed analogy distinct from a defeated conclusion. State a concrete repair in the text’s terms, or explain why the comparison holds.

Indicators: even without; on other grounds; at most.

#### comparisons_across_works (corpus)

- Do supplied texts make the same comparison under aligned criteria and conditions?
- Which paired claims agree or diverge once source, target and transfer are matched?

Answer: `[X7.F<n>] <one scoped finding> — dim: comparisons_across_works — relation: <aligned relation> — alignment: <object, sense, owner, scope> — order-basis: <dates, uptake, or unordered> — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <source key> — anchor-b: "<verbatim supporting clause B>" — doc-b: <different source key> — confidence: high|medium|low`

Do: Compare audits after each local inference is reconstructed. Paired anchors establish each side; dates alone do not show uptake.

Indicators: explicit reference; paired formulations; scope qualification.

### Method card and delivery

A compact audit ordered by the conclusions that depend on comparison: what is transferred, which correspondence warrants it, where disanalogies matter, and what weaker conclusion survives. The desks lift comparison → conclusion → correspondence → defeating difference → scoped verdict, plus criteria and alternatives. The reading’s categories are the consequential comparisons in this text. Replace the lifted block. Keep text-facing critical questions but regroup them by audit work, not six kinds of device. Replace unsupported case-selection motives, suppressed options and free-floating alternative rankings with source-supported alternatives and explicit analyst tests. Typology, scalar endpoints and dichotomy checks are conditional probes inside the audit.

1. A compact audit ordered by the conclusions that depend on comparison: what is transferred, which correspondence warrants it, where disanalogies matter, and what weaker conclusion survives. The desks lift comparison → conclusion → correspondence → defeating difference → scoped verdict, plus criteria and alternatives. The reading’s categories are the consequential comparisons in this text.
2. Establish the most consequential local findings and their qualifications; organize the reading by the objects and claims in these texts.
3. Render the named Markdown tables with final finding IDs in every positive cell. Explain the supported relation and the strongest counter-passage; end with what is settled and the exact remaining question.
4. With multiple sources, build each work’s inventory before the paired comparison, and state alignment and chronology limits. With one source, label the result a local inventory where a corpus relation would require another work.
Every consequential table cell must cite a final finding whose complete supporting spans contain the attributed fact and qualification. Split compound claims into several rows when <=200 characters cannot carry them. Use a separate [F1] [F2] citation per finding. Include an anchor-b with its doc-b for a second supporting span when needed, even in the same document; corpus relations always retain at least two distinct source keys. Never use a scope record as a positive finding. Use comma-separated full IDs in from:, never space-concatenated IDs. Judge meaning and completeness by reading the sources; code checks only anchors and IDs. Before returning, read the actual final tables against their cited final rows and the source contexts, including each source counted in coverage; repair or narrow unsupported cells. Keep execution/scope diagnostics separate from source interpretations; an unchecked record means the check was incomplete, not that the source is meaningless or silent.
