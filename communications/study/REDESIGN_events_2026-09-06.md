# Redesign: events and supported causal links (T1, 2026-09-06)

> First-queue method T1 from Codex's map: "What events are reported in what order, and which causal links do the sources support?" Base `event_timeline_causal` (legacy: numeric causal strengths 0-1), folding `temporal_discontinuity_finder` (legacy: "suspicious patterns", deception from gaps). Codex's demand memo: the event inventory answers the dossier's timeline need.

**Ideal output, one text.** The events the text reports, each with the date exactly as written and its precision (day, month, year, approximate, relative, undated), the actors, and the source the text cites; states and trends kept apart from events; the order the text asserts, built from absolute dates first, relative markers second (resolved against the text's own dates where possible), narrative sequence last, and marked as such; the causal links the text claims, each typed by the text's own connective (cause, trigger, enabling condition, contributing factor, correlation), marked asserted or implied by juxtaposition, with its hedge; what the text offers for each link (mechanism, source, sequence only, actor's statement) and the alternative causes the text itself names; the timeline's coverage (span, density, gaps, clusters, undated events, internal date conflicts) stated as coverage, never as concealment; the judgment on which causal claims are supported, asserted, or juxtaposition. Tables: timeline (event, date, precision, actor, source, anchor), causal links (cause → effect, type, claimed, support, anchor), coverage (span, gaps, conflicts).

**Corpus.** The same event across documents with date and attribution conflicts; causal links asserted in one document and absent, hedged or reversed in another, stated as disagreements.

**Method card.** Source criticism and process tracing: date and attribute each event as the source gives it; separate sequence from causation; a causal claim needs a mechanism or a source, not co-occurrence; a motive attributed without a source is a claim about a mind and is marked. A gap is a gap.

**Depth.** Every dated and undated event inventoried; every relative marker resolved or marked unresolvable; every link typed from the text's own words; the text's own alternative causes and internal date conflicts quoted.

**Definitions.** `src/engines/capability_definitions/event_timeline_causal.yaml` (version 2, renamed Events and Supported Causal Links) and `src/operationalizations/definitions/event_timeline_causal.yaml` (`process:`).
