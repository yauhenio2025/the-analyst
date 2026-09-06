# Third queue: demand, ideal outputs and method design

## 1. The twelve and why — selection before design

Selected on 2026-09-06, before designing or purchasing any output: **R1, R3, I1, I2, I3, I15, T2, T10, C2, E2, P3, P4**. Twelve methods, six families; all twelve are validated on one document. A single paper can contain several actors, cases, timelines or attributed sources. That does not turn it into a supplied corpus or independent corroboration.

The demand basis is [Codex's demand memo](TRIAGE_demand_memo_codex_2026-09-05.md), the actual purpose groups in `src/dossier/catalog_purpose.json`, the saved fashion/state-capitalism briefs, and the live desk checks. [The completed numbers-and-sequence check](LIVE_dossier_check_2026-09-06.md) selected `fixed_path_numbers_and_sequence`; the owner reports that the second live check selected a concept-trajectory path. These are observed paths, not a representative demand sample. The live job continues untouched. This tranche supplies the actor, provenance, category and chronology records those paths need most often, without assuming the desk receives a corpus.

| ID | Method | Demand and single-paper validation material | Destination / type |
|---|---|---|---|
| R1 | Metaphorical mappings | Concept-trajectory readers need to see the mappings a term carries before comparing its changes. Deutschmann's Promise of Absolute Wealth. | Follow the words / inventory |
| R3 | Whose voices count | Both paths require speaker attribution before lifting a claim. Zambrana on Rose, Hegel and Marx. | Read it properly / inventory |
| I1 | Stakeholders and means of influence | State-capitalism briefs name actors and agency but need the actual means of influence. Subsea-cable paper. | See the structure / inventory |
| I2 | Distribution of resources, benefits and risks | The briefs ask who supplies, gains and bears costs; a quantity alone cannot establish a transfer. AUKUS paper. | See the structure / inventory |
| I3 | Incentives and constrained choices | The briefs turn source mechanisms into practical implications; distinguish documented incentives from predicted responses. Subsea-cable paper. | Test a position / reading |
| I15 | Rules and behavioral responses | Numbers-and-sequence readers need reported rule changes, dates and implementation status separated. AUKUS paper; a reported-rule inventory, not legal advice or an audit of an unsupplied statute. | Count and date / inventory |
| T2 | Parallel timelines | Extend the live sequence path with source-supported overlap between distinct processes. AUKUS paper. | Count and date / inventory |
| T10 | Testing historical periods | Test the period boundaries through which a source presents change before treating them as a trajectory. Castoriadis, Rationality of Capitalism. | Count and date / reading |
| C2 | Categories and boundaries | Concept readers and state-capitalism briefs need criteria, instances and overlaps before aligning categories. AUKUS paper. | Follow the words / inventory |
| E2 | Claim provenance and corroboration | Both paths need the origin of numbers and attributed claims, with uninspected references left unverified. AUKUS paper. | Read it properly / inventory |
| P3 | Entity and relationship index | Actor/tool/event records are a direct demand-memo gap; identity must be evidenced before constructing relations. Subsea-cable paper. | See the structure / inventory |
| P4 | Cases and examples used by the sources | The briefs promise recurring cases; first establish what each source example actually supports. Chen on Jaeggi. | Read it properly / inventory |

S4 is deferred because no policy package is supplied; E6 because no dataset is supplied; I12 because no market record is supplied. Empirical causal, measurement, sampling, precision and replication audits are also lower priority here: these selected philosophical and political-economy readings do not supply those empirical designs. P5/P6 and other corpus methods wait for bounded collections or explicit information requirements. R2/R4, the remaining institutional and temporal methods, and C4/C5 remain for subsequent tranches, not silently folded into these twelve.

The inventory classification is fixed now, before scores. I3 and T10 must meet the original-question Sonnet comparator; inventory releases depend on useful rows, verified retained anchors and a source check. Every release requires no surviving fabricated finding or attribution reversal and no rejected row carried into a table cell. USD15 is guidance; actual costs, failures and any unknown usage are reported. P1 is a subsequent, separately accounted USD4 repair.


## 2. Design and preservation record

No provider calls in this phase. All mapped legacy JSONs are frozen in [original_definitions](third_queue_2026_09_06/original_definitions/). None of the twelve has a pre-existing capability YAML. The exact base question, extraction instructions and complete schema become a one-Sol-call original control; merges use their declared base engine, not a fabricated merged original. [Frozen designs](third_queue_2026_09_06/designs.json) contain the exact dimensions, cards, answer shapes, routing and final briefs. The source texts are unchanged.

Five document dimensions and one conditional corpus dimension per method. Surface = oneshot, standard = oneshot_checked, deep/dvs = dvs; Luna cheap, DeepSeek V4 Pro mid, Sol strong. All twelve stay excluded pending validation. Method keys are reused at v2 for the five single-engine methods plus T10; new keys name genuine merges. The corpus dimension is not evidence of a corpus validation.

### R1 — Metaphorical mappings (`metaphorical_mappings`)

**Ideal output first.** A mapping inventory: expression, source domain, target, transferred relation, implication used by the argument, and limit or competing frame. A short reading explains which mapping carries the thesis and which is only illustrative; a second table records competing frames.

**Existing questions and demonstrated repairs.** Base: `concept_metaphorical_ground`; mapped sources: `concept_metaphorical_ground`, `metaphor_analogy_network`, `metaphor_network`, `metaphorical_infrastructure_mapper`. Preserve the root-metaphor, source-domain, mapping and rival-frame questions. The legacy request for forgotten origins and universal primary metaphors cannot be established from one text; ask about conventional expressions and supplied origin claims. A phrase does not prove an audience effect or an unstated historical inheritance.

Preserved coverage: Root and conventional metaphors, image schemas, source/target correspondences, coherence, competing frames, explicitly hypothetical extensions.

**Expressions and targets (document).** What metaphors structure understanding of this concept?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: expressions — expression: <value or unknown> — target: <value or unknown> — owner: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory explicit and conventional figurative expressions, including image schemas when the wording supports them. Distinguish the author’s metaphors from those quoted or criticized. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: like, as if, image.

**Transferred relations (document).** For each metaphor, what elements map from source to target? What does the metaphor imply about the concept?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: mappings — source-domain: <value or unknown> — target: <value or unknown> — transferred-relation: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Give the relation, not just two nouns. Quote the wording that carries the transfer; literal technical or theological uses may coexist with a metaphor. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: as, represents, embodies.

**Argumentative implications (document).** Which conclusion does the passage draw using this mapping, and which premise makes the transfer relevant?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: entailments — mapping: <value or unknown> — conclusion: <value or unknown> — warrant: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Separate an implication the source uses from a hypothetical analyst extension. Anchor the inference as well as the expression. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: therefore, promise, because.

**Related expressions (document).** Which expressions elaborate the same mapping, and where do their transferred relations differ?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: coherence — expressions: <value or unknown> — common-relation: <value or unknown> — difference: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Pair occurrences before claiming a systematic metaphor network. State image-schema descriptions as interpretations, without compulsory theory labels. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: journey, container, movement.

**Competing frames and limits (document).** Are there rival metaphors for the same aspect of the concept? What is at stake in the text’s contrast?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: rivals — frame-a: <value or unknown> — frame-b: <value or unknown> — contrast: <value or unknown> — limit: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote both sides and the contrast predicate. Do not turn a technical distinction into a rejected metaphor unless the source makes that move. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: rather than, but, analogy.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. A mapping inventory: expression, source domain, target, transferred relation, implication used by the argument, and limit or competing frame. A short reading explains which mapping carries the thesis and which is only illustrative; a second table records competing frames.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### R3 — Whose voices count (`quote_attribution_voice`)

**Ideal output first.** A speaker-and-statement inventory with direct/reported/narrating level, quoted proposition, the authority or objection it supplies, and the narrator’s stance. A voice-relation table makes nested attribution and disagreement visible without numerical authority rankings.

**Existing questions and demonstrated repairs.** Base: `quote_attribution_voice`; mapped sources: `quote_attribution_voice`. Preserve the original core question and speaker/quote/function coverage. Translate the legacy noun checklist into questions. Replace obligatory dominance metrics with declared counted scope; nested quotations require separate speaker and reporting voice.

Preserved coverage: Speaker inventory, direct and reported speech, rhetorical functions, polyphony, voice balance without unsupported numeric authority scores.

**Speakers and statements (document).** Who is speaking, what are they saying, and why does their voice matter?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: speakers — speaker: <value or unknown> — statement: <value or unknown> — reporting-voice: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Identify each speaker from an explicit attribution span and keep the full attributed predicate. A bibliography entry alone is not a speaking voice. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: writes, argues, according to.

**Attribution levels (document).** Which words are directly quoted, paraphrased or reported through another speaker?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: attribution — utterance: <value or unknown> — direct-or-reported: <value or unknown> — attribution-chain: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Trace nested quotations without collapsing the essayist, commentator and quoted author. Use a second span for an antecedent outside the quoted clause. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: quotes, citing, in her reading.

**Roles in the argument (document).** What claim does this voice support, qualify, exemplify or oppose in this passage?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: functions — voice: <value or unknown> — role: <value or unknown> — claim: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Anchor both the statement and its uptake; a quoted position is not automatically endorsed. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: against, follows, criticizes.

**Agreement and disagreement (document).** Where does the narrator align or contrast the voices on the same question?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: relations — voice-a: <value or unknown> — voice-b: <value or unknown> — question: <value or unknown> — relation: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Keep both attributed positions with their qualifications. Reconcile an apparent reversal by rereading speaker boundaries. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: however, whereas, instead.

**Voice distribution and limits (document).** Which voices recur in the inspected argument, and what does the text establish about their roles or absence?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: coverage — voice: <value or unknown> — inspected-section: <value or unknown> — recurrence: <value or unknown> — limit: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Distinguish a reading inventory from exhaustive quote counting. Put scoped missing-voice searches in scope records; do not infer deliberate silencing. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: introduction, conclusion, quotation.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. A speaker-and-statement inventory with direct/reported/narrating level, quoted proposition, the authority or objection it supplies, and the narrator’s stance. A voice-relation table makes nested attribution and disagreement visible without numerical authority rankings.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### I1 — Stakeholders and means of influence (`stakeholder_power_interest`)

**Ideal output first.** An actor-by-stake-and-means table: actor, stated or inferred interest, legal/resource/technical means, action, affected party and source status. A relationship table records documented alliances, dependencies and conflicts with the mechanism, without invented power scores.

**Existing questions and demonstrated repairs.** Base: `stakeholder_power_interest`; mapped sources: `stakeholder_power_interest`. Preserve Who has power? Who benefits/loses? and the actor/stake/relationship fields. The legacy instructions require calibrated power scores and conflict intensity without measurements; replace them with evidenced means and bounded inference.

Preserved coverage: Stakeholders, power bases, stakes, coalitions, conflicting aims, limits of inference about preferences.

**Actors and stakes (document).** Who has power? Who benefits/loses?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: actors — actor: <value or unknown> — stake: <value or unknown> — declared-or-inferred: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Name actors as the source identifies them and distinguish a declared stake from an analyst inference grounded in a stated constraint. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: government, company, interest.

**Means of influence (document).** What resource, authority or technical position gives each actor influence over this outcome?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: means — actor: <value or unknown> — means: <value or unknown> — affected-decision: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the actor and the operative influence predicate, not a name next to a generic discussion of power. Do not assign numeric rankings. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: licenses, owns, controls.

**Influence exercised (document).** What action did the actor take, through which means, with what reported result?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: actions — actor: <value or unknown> — action: <value or unknown> — means: <value or unknown> — result-status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Separate capability, threat, proposal and completed action. A project announcement establishes no delivered capacity. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: blocked, offered, decided.

**Relationships and coalitions (document).** Which documented relationships align or oppose the actors, and on what issue?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: relations — actor-a: <value or unknown> — actor-b: <value or unknown> — relationship: <value or unknown> — issue: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Require a relationship-bearing clause for every edge; common interests or co-mentions alone establish no alliance. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: partner, dependent, opposes.

**Constraints and contrary evidence (document).** What limits the stated means of influence, or qualifies an inference about an actor’s preferences?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: limits — actor: <value or unknown> — constraint: <value or unknown> — counter-passage: <value or unknown> — limit: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Keep commercial and political constraints distinct. Do not infer private motives or a general ranking from one outcome. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: despite, constrained, uncertainty.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. An actor-by-stake-and-means table: actor, stated or inferred interest, legal/resource/technical means, action, affected party and source status. A relationship table records documented alliances, dependencies and conflicts with the mechanism, without invented power scores.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### I2 — Distribution of resources, benefits and risks (`resource_distribution`)

**Ideal output first.** A resource-flow and burden inventory with supplying actor, receiving actor, resource, mechanism, amount/unit/date/status when given, and beneficiary or risk bearer. Explain documented asymmetries without converting a fund total into a project allocation or a benefit into a motive.

**Existing questions and demonstrated repairs.** Base: `resource_flow_asymmetry`; mapped sources: `resource_flow_asymmetry`, `power_interest_subtext`. Preserve Who pays? Who profits? Who bears the risks? and FROM → TO / magnitude / mechanism. Replace hidden-interest inference and compulsory asymmetry severity with documented transfers and source-reported burdens. Aggregates, pledges and eligibility are not disbursements.

Preserved coverage: Who pays, profits and bears risk, value chains, subsidies, structural advantages, nonfinancial transfers.

**Resource flows (document).** Who pays? Who profits? Who bears the risks?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: flows — supplier: <value or unknown> — recipient: <value or unknown> — resource: <value or unknown> — mechanism: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Anchor the from-to transfer predicate and its status. Record nonfinancial resources, knowledge and access as well as money. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: funds, supplies, transfers.

**Amounts and status (document).** What amount, unit, period and commitment or realization status belongs to each reported flow?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: quantities — flow: <value or unknown> — amount: <value or unknown> — unit: <value or unknown> — period: <value or unknown> — status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Keep aggregates separate from allocations and targets from expenditure. Missing amount is unknown, not zero; a total program fund cannot be assigned to one case. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: million, committed, allocated.

**Benefits and value chains (document).** Who receives the stated benefit, at which stage of the arrangement, through what mechanism?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: benefits — beneficiary: <value or unknown> — benefit: <value or unknown> — stage: <value or unknown> — mechanism: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the benefit predicate and its recipient. Separate promised commercial opportunities from demonstrated revenue or profit. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: access, contracts, returns.

**Costs and risks (document).** Which actor bears a stated cost or risk, and does the text describe a transfer of that burden?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: burdens — risk: <value or unknown> — generator: <value or unknown> — bearer: <value or unknown> — transfer-status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: A warning about a risk is not an observed loss. Preserve financial, social, operational and political kinds. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: cost, liability, risk.

**Supported asymmetries (document).** Which evidenced flows or burdens support a distributional asymmetry, and what limits the comparison?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: asymmetries — relation: <value or unknown> — advantage: <value or unknown> — burden: <value or unknown> — comparison-limit: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Compare like quantities and roles. Name structural advantages without treating them as proof of intention or capture. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: unequal, public, private.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. A resource-flow and burden inventory with supplying actor, receiving actor, resource, mechanism, amount/unit/date/status when given, and beneficiary or risk bearer. Explain documented asymmetries without converting a fund total into a project allocation or a benefit into a motive.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### I3 — Incentives and constrained choices (`incentives_constrained_choices`)

**Ideal output first.** A reading organized around the strongest documented incentive mechanism and its limits, with an actor/action/reward-or-penalty/constraint/observed-response table. A second table tests delegation, information gaps, alternative explanations and explicitly conditional response scenarios.

**Existing questions and demonstrated repairs.** Base: `incentive_structure_mapper`; mapped sources: `incentive_structure_mapper`, `principal_agent_analyzer`, `rational_actor_modeling`. Retain reward, punishment, constraint, delegation and observed-response questions from the three source engines. Their mandatory worldview profiles, numeric gaming probabilities, principal-agent dysfunction and Nash equilibria are not identifiable from an ordinary paper. Ask first whether those relations exist, and distinguish response evidence from a conditional model.

Preserved coverage: Payoffs, misalignment, delegation and information asymmetry, moral hazard, control mechanisms, actor response scenarios.

**Rewards and penalties (document).** What does this system actually reward, and why do people act the way they do?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: incentives — actor: <value or unknown> — action: <value or unknown> — reward-or-penalty: <value or unknown> — mechanism: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Answer the causal part only to the extent the text supports it. Specify who offers the incentive, to whom and conditional on which action. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: incentive, subsidy, sanction.

**Feasible choices (document).** What documented constraints shape the actor’s available choices?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: constraints — actor: <value or unknown> — options: <value or unknown> — constraint: <value or unknown> — scope: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Do not invent a complete option set or private utility function. Differentiate technical, legal, financial and geopolitical constraints. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: license, cost, requirement.

**Observed and conditional responses (document).** Which response is reported, and what evidence links it to the incentive rather than merely preceding it?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: responses — actor: <value or unknown> — response: <value or unknown> — observed-or-conditional: <value or unknown> — link: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the response predicate and the source’s causal attribution separately where necessary. Retain competing commercial and political explanations. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: after, because, switched.

**Delegation and information (document).** Does the text document delegation, conflicting objectives or unequal information; what control mechanism follows?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: delegation — principal: <value or unknown> — agent: <value or unknown> — delegated-task: <value or unknown> — information: <value or unknown> — control: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Do not presume a principal-agent problem from a state-company interaction. Record an absent delegation basis as a scoped limit. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: contract, monitoring, disclosure.

**Rival explanations and changed conditions (document).** What alternative explanation or changed condition would alter the proposed response mechanism?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: alternatives — mechanism: <value or unknown> — rival: <value or unknown> — condition: <value or unknown> — prediction-status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Label analyst scenarios explicitly and ground their constraints in source findings. End with what observed evidence distinguishes the accounts and what remains untested. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: although, alternative, if.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. A reading organized around the strongest documented incentive mechanism and its limits, with an actor/action/reward-or-penalty/constraint/observed-response table. A second table tests delegation, information gaps, alternative explanations and explicitly conditional response scenarios.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Carry one explanatory judgment through the evidence and its strongest counter-passage.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### I15 — Rules and behavioral responses (`rules_and_responses`)

**Ideal output first.** A dated reported-rule inventory: rule identity, jurisdiction, proposal/adoption/effect status, actor and operative requirement, with a response table distinguishing observed implementation from expected effects. Show unresolved identity and interactions; archive-bound reporting only.

**Existing questions and demonstrated repairs.** Base: `regulatory_dynamics_analyzer`; mapped sources: `regulatory_dynamics_analyzer`, `regulatory_pulse`. Preserve regulatory landscape/evolution/effects/compliance/interactions and the dated pulse fields. Arbitrage opportunities require documented responses, not advice. Do not identify a proposed amendment with an effective decree just because their topics match; no current-law claim follows from an old paper.

Preserved coverage: Regulatory evolution, enforcement, compliance deadlines, rule interactions, arbitrage descriptions, reported unintended effects.

**Rule identities and jurisdictions (document).** How do regulations evolve and affect behavior?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: rules — rule: <value or unknown> — jurisdiction: <value or unknown> — actor: <value or unknown> — stated-function: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory the named rules and source-reported function. Separate a program, law, fund and agreement; keep unresolved instruments separate. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: Act, decree, regulation.

**Dates and operative status (document).** What dates and status does the source give for proposal, adoption, entry into force or implementation?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: status — rule: <value or unknown> — date: <value or unknown> — precision: <value or unknown> — status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the exact event predicate with the date. A proposal and an effective instrument need an explicit identity link before merging; no invented deadline. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: proposed, enacted, effective.

**Requirements and enforcement (document).** What requirement, eligibility condition, exception or enforcement mechanism is reported for each actor?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: requirements — rule: <value or unknown> — actor: <value or unknown> — requirement: <value or unknown> — exception: <value or unknown> — enforcement: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Read the operative condition and its scope. A report of a rule supports reported requirements, not an audit of the full unsupplied instrument. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: eligible, exempt, must.

**Behavior and effects (document).** Which behavior is reported after or in response to the rule, and which effects remain expected?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: responses — rule: <value or unknown> — behavior: <value or unknown> — attribution: <value or unknown> — observed-or-expected: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the causal predicate when attributing an effect. Preserve projected benefits, uncertain delivery and observed compliance as different statuses. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: responded, enables, expected.

**Interactions and limits (document).** Which supplied rules reinforce, constrain or overlap one another, and what evidence carries that relation?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: interactions — rule-a: <value or unknown> — rule-b: <value or unknown> — interaction: <value or unknown> — limit: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Use two spans when needed; shared jurisdiction or topic establishes no operative interaction. Report missing implementation evidence without declaring the rule ineffective. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: amendment, alongside, subject to.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. A dated reported-rule inventory: rule identity, jurisdiction, proposal/adoption/effect status, actor and operative requirement, with a response table distinguishing observed implementation from expected effects. Show unresolved identity and interactions; archive-bound reporting only.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### T2 — Parallel timelines (`chronology_simultaneity`)

**Ideal output first.** Parallel process lanes with actor, event or interval, date precision and status; an overlap table identifies which intervals intersect and whether a source establishes synchronization, discrepancy or merely approximate contemporaneity. No causal arrows follow from overlap alone.

**Existing questions and demonstrated repairs.** Base: `chronology_simultaneity`; mapped sources: `chronology_simultaneity`. Preserve the original simultaneity question and lane/intersection/discrepancy fields. The generic relationship-graph instruction supplies no temporal proof. Ask for both intervals, avoid making a year into a specific date, and retain plans separately from events.

Preserved coverage: Concurrent events, parallel processes, intersections, synchronization, temporal discrepancies.

**Processes and dated events (document).** What was happening simultaneously, and how do different timelines overlap or contradict?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: lanes — process: <value or unknown> — actor: <value or unknown> — event: <value or unknown> — date: <value or unknown> — status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Identify distinct source-supported processes before constructing lanes; events in one article need not belong to one causal sequence. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: during, announced, began.

**Intervals and precision (document).** What start, end or bounded interval does the source give, with what date precision?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: intervals — process: <value or unknown> — start: <value or unknown> — end: <value or unknown> — precision: <value or unknown> — open-bound: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Do not fill an unknown endpoint. Keep planned dates apart from completed events and preserve relative dates only where the reference is established. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: since, until, by.

**Evidenced overlap (document).** Which documented intervals overlap, and at what precision can their simultaneity be established?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: overlap — interval-a: <value or unknown> — interval-b: <value or unknown> — overlap: <value or unknown> — precision: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Retain an anchor for each dated predicate, including two in one document. Same-year dates prove at most year-level co-occurrence unless intervals support more. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: meanwhile, in 2024, concurrent.

**Synchronization and intersections (document).** Does the text establish that processes synchronized or interacted, beyond simply overlapping?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: intersections — process-a: <value or unknown> — process-b: <value or unknown> — synchronization: <value or unknown> — evidence-status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Require the linking predicate for coordination or causation. A shared date cannot establish a planned joint response. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: coordinated, linked, coincided.

**Discrepancies and unresolved timing (document).** Do reported dates disagree on the same event, or refer to different stages or levels of precision?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: discrepancies — event: <value or unknown> — date-a: <value or unknown> — date-b: <value or unknown> — stage: <value or unknown> — resolution: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Check identity and stage before alleging contradiction. Report ambiguous chronology openly rather than harmonizing dates. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: approximately, later, proposal.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. Parallel process lanes with actor, event or interval, date precision and status; an overlap table identifies which intervals intersect and whether a source establishes synchronization, discrepancy or merely approximate contemporaneity. No causal arrows follow from overlap alone.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### T10 — Testing historical periods (`periodization_critic`)

**Ideal output first.** A judgment of the source’s strongest historical boundary, with a period/boundary/criterion/evidence/continuity table. A second table compares a source-grounded alternative cut and its costs. Lead with what the periodization explains, and distinguish approximate overlapping thresholds from a factual contradiction.

**Existing questions and demonstrated repairs.** Base: `periodization_critic`; mapped sources: `periodization_critic`. Preserve Are the proposed time periods analytically justified? and boundary/coherence/continuity/alternative probes. The old schema asks for a critique type even when a boundary holds; allow a justified boundary and avoid invented precision or obligatory replacement periods.

Preserved coverage: Period boundaries, coherence, rupture versus continuity, alternative periodizations and stakes.

**Periods and their object (document).** Are the proposed time periods analytically justified?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: periods — scheme: <value or unknown> — period: <value or unknown> — object: <value or unknown> — purpose: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory the actual source scheme, distinguishing a historical phase from a date used only as an example. State what the boundary is intended to explain. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: phase, period, era.

**Boundary criteria (document).** What change or criterion justifies each beginning or end, and how precise is the source’s date?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: boundaries — boundary: <value or unknown> — criterion: <value or unknown> — date: <value or unknown> — precision: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Retain approximately, around and mixed thresholds. Quote the change predicate, not a date alone. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: since, until, around.

**Within-period coherence (document).** Which evidence supports a period’s coherence, and which differences within it matter to the question?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: coherence — period: <value or unknown> — common-feature: <value or unknown> — internal-difference: <value or unknown> — implication: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Assess the source’s evidence and its explanatory purpose; a heterogeneous era is not automatically an invalid analytical period. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: throughout, characteristic, exception.

**Continuities across a cut (document).** What continues across the proposed boundary, and does the source acknowledge it?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: continuities — boundary: <value or unknown> — continuity: <value or unknown> — change: <value or unknown> — acknowledgment: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Pair before-and-after claims and preserve the positive continuity passage. Added factors do not imply that the earlier mechanism disappeared. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: remains true, but new, still.

**Alternative cuts and costs (document).** What source-supported alternative boundary would answer the stated question differently, and with what tradeoff?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: alternatives — alternative: <value or unknown> — source-basis: <value or unknown> — gain: <value or unknown> — cost: <value or unknown> — status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Label analyst alternatives and retain their source basis. Do not invent a historical record or mistake another analytic timescale for the source’s own periodization. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: instead, earlier, long term.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. A judgment of the source’s strongest historical boundary, with a period/boundary/criterion/evidence/continuity table. A second table compares a source-grounded alternative cut and its costs. Lead with what the periodization explains, and distinguish approximate overlapping thresholds from a factual contradiction.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Carry one explanatory judgment through the evidence and its strongest counter-passage.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### C2 — Categories and boundaries (`categories_boundaries`)

**Ideal output first.** A category/criterion/instance inventory plus a boundary-and-overlap table showing nonexclusive membership, disputed cases and criteria that change by context. Preserve the author’s classifications and competing attributed definitions before judging their consequences.

**Existing questions and demonstrated repairs.** Base: `composition_taxonomy`; mapped sources: `composition_taxonomy`, `boundary_probe`, `concept_demarcation_analyzer`. Preserve the taxonomy core question, hierarchy, instances and cross-classification fields. boundary_probe presumes probing would reveal hidden arbitrariness; replace that verdict with an open criterion test. A schema membership is not evidence of exhaustive or exclusive categories.

Preserved coverage: Taxonomic structure, demarcation, borderline cases, threshold sensitivity, cross-classifications, nonexclusive membership.

**Categories and purpose (document).** How are things classified in this domain, and what do the categories reveal?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: categories — category: <value or unknown> — classified-object: <value or unknown> — owner: <value or unknown> — purpose: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory each classification in its attributed context; keep the article’s categories distinct from cited authors’ typologies. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: type, form, classified.

**Inclusion and exclusion (document).** Which stated criterion includes an instance in a category, and what would exclude it?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: criteria — category: <value or unknown> — inclusion: <value or unknown> — exclusion: <value or unknown> — stated-or-reconstructed: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the classification predicate and its limiting condition. Reconstruct a criterion only with explicit status, never from a category name alone. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: defined as, requires, excludes.

**Instances and membership (document).** Which named instances does the text assign to each category, under which criterion?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: instances — instance: <value or unknown> — category: <value or unknown> — criterion: <value or unknown> — qualification: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Use a membership-bearing clause for each assignment. Keep state ownership, financing and procurement distinct even when they occur in one case. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: example, belongs, constitutes.

**Hierarchies and overlaps (document).** How do the classifications nest, intersect or cross-cut one another?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: relations — category-a: <value or unknown> — category-b: <value or unknown> — relation: <value or unknown> — basis: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Preserve nonexclusive membership and alternative schemes. A framework comparison within one paper is a document relation with same-source spans. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: subset, overlapping, hybrid.

**Contested edges (document).** Where does the text contest a criterion or supply a borderline case, and what does changing that threshold change?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: boundaries — case: <value or unknown> — criterion: <value or unknown> — contest: <value or unknown> — consequence: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Retain both definitions in disputes. Do not force arbitrariness, exclusivity or an invented numerical threshold; put missing boundary evidence in the scope report. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: rather than, narrower, contested.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. A category/criterion/instance inventory plus a boundary-and-overlap table showing nonexclusive membership, disputed cases and criteria that change by context. Preserve the author’s classifications and competing attributed definitions before judging their consequences.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### E2 — Claim provenance and corroboration (`claim_provenance`)

**Ideal output first.** A claim-origin-and-chain inventory linking important numbers, dates and mechanisms to the immediate cited or reported source, stated transformation and access status. A dependence table distinguishes repeated reporting, asserted corroboration and genuinely inspected independent support; missing originals stay unverified.

**Existing questions and demonstrated repairs.** Base: `provenance_audit`; mapped sources: `provenance_audit`, `source_triangulation_mapper`. Preserve Where do these claims come from, and how reliable are those sources? as a bounded source-status question. Uninspected citations cannot show actual degradation, reliability or independent corroboration. Replace the presumption of tracing actual origin with the chain the supplied text documents.

Preserved coverage: Claim-as-report versus claim-as-true, circular citations, laundering or repetition hypotheses, independent triangulation, conflicting source chains.

**Claims and immediate origins (document).** Where do these claims come from, and how reliable are those sources?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: claims — claim: <value or unknown> — immediate-source: <value or unknown> — attribution: <value or unknown> — access-status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Treat reliability as what the supplied evidence establishes, not a reputation score. Inventory important numbers and mechanism claims; the citing article is not the original itself. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: according to, reports, cited.

**Documented chains (document).** Which original or intermediary does the text identify, and which links remain uninspected?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: chains — claim: <value or unknown> — origin: <value or unknown> — intermediary: <value or unknown> — inspected-link: <value or unknown> — gap: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the attribution together with the claim predicate, using a second span when separated. Never imply that an unsupplied reference has been read. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: quoting, drawing on, based on.

**Reported transformations (document).** What summarizing, rounding, translation or change of scope is visible in the supplied chain?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: transformations — claim: <value or unknown> — transformation: <value or unknown> — compared-passages: <value or unknown> — status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: An actual transformation needs both formulations. Distinguish the article’s report of a transformation from a transformation verified against an original. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: estimated, summarized, adapted.

**Dependence and corroboration (document).** Do independent sources corroborate these claims?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: dependence — claim: <value or unknown> — sources: <value or unknown> — dependence-evidence: <value or unknown> — corroboration-status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Answer only within supplied access. Different citation labels do not establish independence; name circularity or laundering only with a documented chain, otherwise retain a hypothesis. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same source, confirmed, repeated.

**Conflicts and next evidence (document).** Where do supplied chains disagree on the same claim, and what missing source would resolve the issue?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: conflicts — claim: <value or unknown> — conflict: <value or unknown> — alignment: <value or unknown> — missing-evidence: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Check population, date, target and status before declaring contradiction. Missing originals mean unverified, not false; scope records cannot prove a positive fact. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: however, differs, reference.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. A claim-origin-and-chain inventory linking important numbers, dates and mechanisms to the immediate cited or reported source, stated transformation and access status. A dependence table distinguishes repeated reporting, asserted corroboration and genuinely inspected independent support; missing originals stay unverified.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### P3 — Entity and relationship index (`entity_extraction`)

**Ideal output first.** An entity index with source name, alias or unresolved identity, type, role and location, followed by an evidenced subject–relation–object table. Index people, organizations, places, products/projects and events; keep acronym and case identities unresolved when the source does.

**Existing questions and demonstrated repairs.** Base: `entity_extraction`; mapped sources: `entity_extraction`. Preserve the original question and entity/role/relationship fields. Replace automatic alias consolidation, mention-based significance scores and compulsory graph clusters with evidenced identity and relation spans. Co-occurrence is not an edge.

Preserved coverage: People, organizations, places, products, events, aliases, role and relation indexing with ambiguity retained.

**Entities and mentions (document).** Who and what are the key actors and objects in this discourse?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: mentions — name: <value or unknown> — type: <value or unknown> — mention-context: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory people, organizations, locations, products/projects and events relevant to the argument. A reference author is not automatically a case actor. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: company, government, cable.

**Aliases and identity (document).** Which names or acronyms demonstrably refer to the same entity, and which remain unresolved?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: identity — mention-a: <value or unknown> — mention-b: <value or unknown> — identity-basis: <value or unknown> — status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Require an explicit alias or unambiguous contextual link. Never merge separate projects sharing a geography, sponsor or instrument type. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: known as, formerly, acronym.

**Documented roles (document).** What role does the text assign each entity in the reported arrangement?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: roles — entity: <value or unknown> — role: <value or unknown> — arrangement: <value or unknown> — date-status: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Quote the role predicate with its object. Ownership, operation, financing and partnership are distinct relations. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: owns, operates, financed.

**Evidenced relationships (document).** Which subject–predicate–object relationships are explicitly reported or carefully reconstructed?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: relationships — subject: <value or unknown> — predicate: <value or unknown> — object: <value or unknown> — stated-or-reconstructed: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Retain spans for both entities and the relational verb; use additional spans when necessary. Co-mentions alone establish no causal or institutional edge. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: acquired, connects, partnered.

**Ambiguity and index limits (document).** Which entity or relationship ambiguities matter to the index, and what evidence would resolve them?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: coverage — entity: <value or unknown> — ambiguity: <value or unknown> — inspected-context: <value or unknown> — missing-evidence: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: State relevant coverage and ambiguous identity rather than inventing a canonical expansion. Do not claim completeness from a fixed row count. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: unclear, consortium, project.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. An entity index with source name, alias or unresolved identity, type, role and location, followed by an evidenced subject–relation–object table. Index people, organizations, places, products/projects and events; keep acronym and case identities unresolved when the source does.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

### P4 — Cases and examples used by the sources (`exemplar_catalog`)

**Ideal output first.** A source-example inventory: case or hypothetical example, owner, attributes, claim illustrated or challenged, inferential function, and limits of representativeness. A case-to-claim table preserves distinct examples and the difference between illustrating a possibility and establishing a general history.

**Existing questions and demonstrated repairs.** Base: `exemplar_catalog`; mapped sources: `exemplar_catalog`. Preserve What concrete cases illustrate the arguments? and identification/context/usage/quality. The old representativeness and recurrence fields invite unsupported population claims; distinguish invented thought experiments from historical cases and count only the inspected inventory.

Preserved coverage: Case catalog, recurring exemplars, type/domain/function, example-to-argument map.

**Cases and examples (document).** What concrete cases illustrate the arguments?

Answer shape: `[D1.F<n>] <one source-scoped finding> — dim: examples — example: <value or unknown> — kind: <value or unknown> — owner: <value or unknown> — passage-context: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Inventory historical cases, anecdotes, hypothetical cases and counterexamples separately. Name the source owner before treating the example as the author’s endorsement. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: for example, imagine, case.

**Relevant attributes (document).** Which attributes of each example matter to the claim it is used to support?

Answer shape: `[D2.F<n>] <one source-scoped finding> — dim: attributes — example: <value or unknown> — attribute: <value or unknown> — claim-relevance: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Give each materially different example its own finding. A quote for one case cannot carry attributes of another. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: because, illustrates, insofar.

**Inferential functions (document).** Does the example illustrate, support, test or defeat a claim, and what passage establishes that role?

Answer shape: `[D3.F<n>] <one source-scoped finding> — dim: functions — example: <value or unknown> — claim: <value or unknown> — function: <value or unknown> — warrant: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Anchor both the example and its argumentative uptake. An illustration of possibility is not an empirical estimate of frequency. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: shows, counterexample, suggests.

**Repeated and contrasting uses (document).** Where does the text reuse or contrast examples, and does their argumentative role change?

Answer shape: `[D4.F<n>] <one source-scoped finding> — dim: comparisons — example-a: <value or unknown> — example-b: <value or unknown> — contrast: <value or unknown> — role-change: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Pair the uses with their owners and conditions. Retain separate marriage, childhood, populism or other cases if the source distinguishes them; no forced exhaustive checklist. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: whereas, similarly, by contrast.

**Representativeness and qualifications (document).** What does the source establish about the example’s scope, and which generalization would exceed it?

Answer shape: `[D5.F<n>] <one source-scoped finding> — dim: limits — example: <value or unknown> — scope: <value or unknown> — qualification: <value or unknown> — generalization-limit: <value or unknown> — anchor: "<literal actor and predicate span, <=200 chars>" — doc: <source key> — confidence: high|medium|low`

Do: Preserve conditional and negative clauses. Distinguish an acknowledged unrepresentative illustration from a claimed general case; report absent population evidence as a limit. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: only, if, not necessarily.

**Aligned objects across supplied sources (corpus).** Which supplied sources address the same object on this method’s question, and what aligned agreement or difference do their passages support?

Answer shape: `[X6.F<n>] <scoped relation> — dim: across_sources — object: <aligned object> — relation: <agreement or difference> — anchor: "<literal supporting span>" — doc: <A> — anchor-b: "<literal supporting span>" — doc-b: <different B> — confidence: high|medium|low`

Do: Establish a local inventory in each supplied document first. Match identity, question, time and scope before relating findings. Preserve two distinct source keys and the predicate on each side. One article quoting several authors is still one supplied document. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.

Indicators: same object in two sources, different answers to an aligned question.

**Method delivery card.**

1. A source-example inventory: case or hypothetical example, owner, attributes, claim illustrated or challenged, inferential function, and limits of representativeness. A case-to-claim table preserves distinct examples and the difference between illustrating a possibility and establishing a general history.
2. Lead with the most consequential supported distinction, organized around source objects and questions. Useful inventory coverage is the deliverable; do not force a novel thesis.
3. Render the two named Markdown tables, with explicit limits and citable rows; end with what is established and the evidence still needed.
4. With multiple supplied texts, establish local inventories before an aligned relation; with one text do not pretend there is a supplied corpus.
Every substantive table cell cites final finding IDs with separate [F1] [F2] citations. Before returning, reread the actual final tables against the retained ledger and full source contexts. Rewrite or drop any cell citing a rejected, weakened or unverified claim; never carry a rejected row as valid evidence in a cell. Preserve granular support when merging duplicates. Use comma-separated full IDs in from:. No fabricated completion of missing cells, attribution reversals or silent replacement of missing evidence with context. The models judge meaning; code checks anchors and IDs only. Select literal spans that together carry the finding’s actor, predicate, object and necessary qualification. If one span of at most 200 characters cannot do so, use anchor-b/doc-b for another span, including within one document. Do not join separated text or normalize a quote into invented wording. Retain both poles of a contrast. A verbatim name or prefix without the claimed predicate is insufficient: re-anchor, narrow or reject it. Keep source voice, status, chronology and uncertainty in the final claim. No scope record supplies positive evidence.
