# One shape for the estate's analytical methods (2026-09-04)

> The generalisation of `REDESIGN_conditions_of_possibility_2026-09-04.md` and `REDESIGN_argument_architecture_2026-09-04.md`: a single process the registry can hold, with per-step model routing, and the list of engines that are parameters of it.

## 1. The shape

Every analytical method in the estate does three different kinds of work, and the study showed that conflating them (four re-readings of the whole text, each doing all three under a different mood) is what made the passes expensive without making them better.

```
extract     read the text with one question set; return anchored findings only     cheap model, parallel per dimension (and per document)
verify      check every finding against the source; reject, weaken, merge; hunt for misses   mid model, one call per document (+ one across a corpus)
synthesize  write the reading for a reader from the verified ledger; cite by id    strong model, one call
```

The **findings ledger** is the only hand-off. Its row shape is the one the plumbing already parses (`split_ledger`, the `## Findings ledger` heading) with three additions: a dimension tag, an optional `from:` lineage, and optional typed fields the dimension's answer shape declares (`depends:`, `supports:`, `counter-anchor:`, `provenance:`).

```
- [<step>.F<n>] <finding, one sentence> — dim: <D2> — anchor: "<verbatim, ≤200 chars>" — <typed fields> — confidence: high|medium|low
```

**Walls** (code, never meaning): anchors verbatim against the source (`walls.verify_anchor`, with trimming); ids unique and every cited id existent; one re-anchor round for failed rows, then drop; heading and shape. **Judgment** (model): what is a finding, whether an anchor supports it, what is missing, what the reading says.

A **method card** per dimension replaces the lineage name-drop: two to four imperatives (what to do), the indicators to hunt for, and for scheme-based methods the questions to run. It is rendered into the extraction prompt for that dimension and into the verify and synthesize prompts in full.

## 2. What the registry holds

An operationalization gains an optional `process` block; a depth sequence may point at a process instead of listing stance passes. Nothing existing changes: engines without a process keep their stance passes; the four-stance `deep` sequence stays as it is for the frontier study's control condition.

```yaml
engine_key: conditions_of_possibility_analyzer
process:
  key: dvs                              # decompose-verify-synthesize
  dimensions:                           # the redesigned, text-facing dimension set
    - key: givens
      name: The givens
      questions: [...]
      answer_shape: "[F] The text presupposes <premise> — anchor — depends: <what falls> — confidence"
      method_card: |
        Do: list what the text treats as sayable without argument ...
      indicators: [...]
      scope: document                   # document | corpus (corpus dimensions run only with 2+ texts)
  steps:
    - key: extract
      kind: extract                     # extract | verify | synthesize
      parallel_over: dimension          # dimension | document | dimension_x_document | none
      model_tier: cheap                 # cheap | mid | strong
      output: ledger                    # ledger | prose_ledger
    - key: verify
      kind: verify
      consumes: [extract]
      model_tier: mid
      output: ledger
      duties: [check_anchors_in_context, reject_biography, merge_duplicates, hunt_misses, name_must_keep]
    - key: synthesize
      kind: synthesize
      consumes: [verify]
      model_tier: strong
      output: prose_ledger
      is_final: true
      brief: |
        The reading a reader needs, in this order: ...
      tables: [givens, inheritance, visibility]
  routing:                              # per-tier defaults; the plan's model_hint and env override
    cheap: openrouter/openai/gpt-5.6-luna
    mid: openrouter/deepseek/deepseek-v4-pro
    strong: claude-sonnet-4-6
depth_sequences:
  - depth_key: dvs
    process: dvs
```

Per-pass routing in the runner: each step resolves its model from `routing[model_tier]`, overridable by an explicit per-step `model`, by the executor plan's `model_hint` (which then applies to the strong tier only, so a plan that asks for Fable does not send Fable to read with a checklist), and by environment (`PROCESS_ROUTING_CHEAP` etc.). `run_engine_call_auto(model_hint=...)` is called once per step invocation; extractions run in parallel threads; refusals fall back as they do today.

Depth keys under this shape: `surface` = extract on the three load-bearing dimensions + synthesize (no verify); `standard` = the full `dvs` on one document; `deep` = the corpus variant (per-document extraction, corpus dimensions, cross-document verify, one synthesis with the sources in context). Depth is a change of *work*, not of pass count.

## 3. Engines that are parameters of the same method

Of the 28 capability engines, the following are "read the text for X with an anchored ledger, verify, synthesize" with X as the parameter. Verified against the registry keys; the definitions themselves have not all been studied, so each needs its own text-facing question set before it runs under the shape.

| family | engines (capability keys) | what the dimensions are about |
|---|---|---|
| genealogy and conditions | conditions_of_possibility_analyzer, concept_evolution, concept_appropriation_tracker, evolution_tactics_detector, genealogy_relationship_classification, genealogy_final_synthesis | givens, inheritance, drift, borrowing, relationships between texts |
| argument and logic | argument_architecture, inferential_commitment_mapper, dialectical_structure, counterfactual_analyzer, modal_reasoning_analyzer, comparative_reasoning_analyzer, specialized_reasoning_classifier, theory_construction_analyzer, epistemological_method_detector, structural_pattern_detector | claims, grounds, warrants, commitments, schemes, modal and conditional structure, method claims |
| concept mapping | conceptual_framework_extraction, concept_centrality_mapper, concept_semantic_constellation, concept_taxonomy_argumentative_function, concept_synthesis | terms, definitions, relations, centrality, argumentative function |
| structure and narrative | narrative_structure_analyzer, chapter_role_analyzer, deep_summarization | sections, roles, arcs, what each part does |
| corpus reports | aoi_engagement_mapping, aoi_sin_findings, aoi_thematic_report, aoi_thematic_synthesis | already corpus-scoped; their dimensions are the corpus dimensions of the shape |

What differs between families is only: the dimension set (questions, answer shapes, method cards), which dimensions are corpus-scoped, which tables the synthesis names, and whether the verify step has method-specific duties (reconcile ids for argument methods; reject biography for genealogical ones). The `kind` field (`synthesis`, `relational`, `extraction`, `primitive`, `comparison`) stops deciding pass count and instead sets the default depth: `extraction` and `primitive` engines default to `surface` (extract + synthesize, no critic); `synthesis` and `relational` to `standard`; `comparison` to `deep`.

## 4. The frontier study, restated in the shape's terms

Conditions: (a) one call with the rewritten questions and method cards (the whole shape in one prompt on one model); (b) the fixed four-stance harness as it stands (production control); (c) `dvs` with every step on the same model; (d) `dvs` with cheap extract, mid verify, strong synthesize. Models as listed in the next-session prompt. Two papers. Two blind judges, both orders, rubric and pairwise against the Fable one-shot. Recorded per run: tokens, cost, seconds, and the code-computed anchor verification rate. The default execution mode and routing are read off the frontier: the cheapest condition within a judge's "slight" margin of the best.

## 5. What this is not

Not a new engine catalogue. The 275 registered definitions are not touched; the 28 capability engines get a `process` block one at a time, each after its question set is rewritten to ask about the text. Not a change to the desks: they keep reading the final pass's prose and ledger; they gain the option to read ledger rows by id, which is a small change to the spine's prompt and the tables desk's row source.
