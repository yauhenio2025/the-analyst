# Redesign: quantities and their meaning (E8, 2026-09-06)

> First-queue method E8 from Codex's map: "What quantities support the source's claims, and are their meanings and comparisons preserved?" New questions; folds `statistical_evidence` (whose legacy schema scored source credibility 0-1 and methodology transparency 0-1: pseudo-precision the text cannot support). Codex's demand memo: the quantity ledger answers the tables desk's need for numbers with their meaning, not a hypothesis-test reading.

**Ideal output, one text.** Every quantity as written with its five attributes: unit, denominator or population, period, status as the text states it (target, pledge, estimate, observation, forecast), and the source and date the text cites; the claim each is asked to carry and whether it bears the weight (right kind, scope, period; a base to judge scale); the comparisons the text draws, explicit or by juxtaposition, and whether both sides are commensurable, with the attribute that differs; precision as written and where use outruns it; the quantities the argument needs and lacks, ranked by what they would change; the judgment on how far the numbers support the central claim and the one figure to check first. Tables: quantities (id, value, unit, of, period, status, source, anchor), comparisons (pair, commensurable, what differs), missing quantities (claim, missing figure, would change).

**Corpus.** The same quantity across documents, matched by what it measures, with every discrepancy and both anchors.

**Method card.** Measurement discipline (Huff, Tufte, Gelman): no quantity without its five attributes; comparisons need a common base; precision must match provenance. No credibility scores; the text's own verbs give status, the text's own citations give provenance. The critic's duty here: check every digit inside every anchor against the source (the wall already verifies the sentence verbatim).

**Depth.** Every quantity in the text inventoried, including headline figures paired with body figures and quantitative words without numbers ("most", "a surge"); every comparison checked on all five attributes; the withheld comparison named without inventing its figure.

**Definitions.** `src/engines/capability_definitions/statistical_evidence.yaml` (version 2, the engine renamed Quantities and Their Meaning; key kept so the folded legacy engine resolves) and `src/operationalizations/definitions/statistical_evidence.yaml` (`process:`).
