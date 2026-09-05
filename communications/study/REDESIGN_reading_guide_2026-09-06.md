# Redesign: the analytical reading guide (S1, 2026-09-06)

> First-queue method S1 from Codex's map: "What does the text argue and how does its organization, evidence and vocabulary carry that argument?" Base engine `deep_summarization` (kept; its eight dimensions were already text-facing), folding `outline_document_summarizer` and `outline_synthesis_generator`. Codex's demand memo names the reading guide the baseline deliverable ("Read it properly") and the default synthesis engine.

**Ideal output, one text.** For a reader who has not read the text: the thesis in the text's words and its kind; the two or three supporting claims and what depends on what; the route (what each section does and hands on, where the argument turns, which sections carry the load); the evidence kinds and what each carries, where it is thin; the key terms defined, undefined and borrowed; the consequential conceptual moves and where rhetoric carries what argument does not; what the text returns to, minimises, sets aside or never mentions relative to its own framing; and entry points for a deeper reading, each pointing at a finding. Tables: outline (section, job, hands on), key terms (term, status, where), evidence kinds (kind, what it carries, where thin).

**Corpus.** Per-document guides, then shared theses and divergences on shared questions with two anchors; divergences are handed to the reconciliation method (P2), not settled here.

**What changed from `deep_summarization`.** Eight dimensions become five plus a corpus dimension: thesis_architecture → thesis (R1); chapter_argument_map → route (R2); evidence_patterns + conceptual_vocabulary → evidence and vocabulary (R3); conceptual_moves + rhetorical_strategies → moves and rhetoric (R4); foregrounding_suppression → foregrounding and omission (R5, with the rule that an absence is named only relative to what the text's own framing makes relevant); downstream_utility becomes the synthesis's entry-points section rather than a dimension. Every question quotes; none asks about the authors.

**Depth.** The thesis in the text's words; every section given a job and a hand-off; every key term with a definitional status and a location; the declared limit checked against practice.

**Definition.** `src/operationalizations/definitions/deep_summarization.yaml` (`process:`); capability YAML unchanged.
