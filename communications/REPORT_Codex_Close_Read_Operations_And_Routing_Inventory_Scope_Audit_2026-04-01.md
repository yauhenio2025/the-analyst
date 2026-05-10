# Audit: Close Read Operations And Routing Inventory Scope

## 1. Verdict

`approve with corrections`

This revised memo is materially stronger than the earlier draft and is now close to the right immediate companion to the extraction tranche.

The major earlier problems are now substantially corrected:

- the tranche is explicitly runtime-first
- active analyzer-side attachment-point auditing is deferred to a post-extraction addendum
- `the-critic` source coverage now matches the real runtime operation surface much better
- `analyzer-mgmt` is correctly downgraded to secondary intent/schema evidence
- the deliverable is now framed as semantic-affordance and routing-hint hypotheses rather than final analyzer contract design
- the inventory matrix is more concrete

The remaining corrections are smaller:

- keep first-hop routing inventory distinct from destination-internal lifecycle workflows
- avoid letting aspirational destinations sit at the same level as runtime-real ones
- tighten one remaining inconsistency where the memo still names current analyzer-v2 seams in the recommended inspection surface despite deferring primary attachment-point analysis

## 2. The Memo's Strongest Code-Backed Points

- The memo is now correctly anchored in the real Critic runtime surface rather than a too-narrow file pair.
  - `webapp/src/contexts/CaptureContext.tsx` creates captures and routes them to Arsenal or research todos.
  - `webapp/src/components/CaptureActionBar.tsx` exposes those destination actions directly from active capture state.
  - `webapp/src/components/ResearchFlagDialog.tsx` turns a capture into a research todo and records the capture-to-research audit trail.
  - `webapp/src/pages/FindingsPage.tsx` routes findings to Arsenal and routes comment-derived material to `/outline/talking-points`.
  - `webapp/src/pages/research/ResearchCard.tsx` extends this further by letting selected answer/contextualizer text be sent to Arsenal or to research through `onSendToArsenal` and `onSendToResearch`.
  - `webapp/src/hooks/useResearchTodos.ts` captures the research queue, lookup, refresh, and NotebookLM-style lookup lifecycle that follows after research-todo creation.
  - `webapp/src/OutlinePanel.tsx` and `webapp/src/OutlineEditorPanel.tsx` show that outline/talking-point destinations are not hypothetical; they are active downstream surfaces with add, delete, upgrade, extract, and saved-summary operations.

- The memo now does a much better job of separating host-local runtime behavior from analyzer-owned law.
  - The runtime flows above are all Critic-owned behavior.
  - `the-critic` still injects capture semantics through host-local config and callbacks.
  - The memo no longer tries to turn those flows into already-existing analyzer contract law.

- The memo is now correct to treat `analyzer-mgmt` as secondary evidence.
  - `frontend/src/pages/plans/[id].tsx` shows a real `research_question` field, but as display/product intent rather than operational routing law.
  - `scripts/seed_rhetoric.py` and `scripts/populate_rhetoric_schemas.py` still provide useful shape evidence for logic-gap, attack, missing-link, revision/fix, and severity semantics.
  - That is the right role for them: vocabulary input, not runtime proof.

- Deferring analyzer attachment-point analysis until after extraction is the right move.
  - The active extraction tranche is restructuring the current metadata seam.
  - The revised memo no longer makes primary-scope claims that depend on settling analyzer schema shape before that tranche lands.

- The revised matrix fields are now concrete enough to be useful later.
  - `current source of truth`
  - `source granularity`
  - `current artifact seam`
  - These additions directly answer the earlier ownership-boundary problem and make the inventory more reusable.

## 3. The Memo's Weakest Or Overstated Assumptions

- The memo is still slightly too broad about what counts as one inventory class.
  - First-hop routes such as:
    - capture -> Arsenal
    - capture -> research todo
    - finding -> Arsenal
    - comment -> talking point
  - are not the same class of thing as destination-internal lifecycle workflows such as:
    - research queue polling and lookup
    - answer refresh
    - outline talking-point upgrade
    - notes extraction into outline
    - saved outline summaries
  - Both are worth documenting, but they should not sit in one undifferentiated matrix without a stronger subtype column or separate subtable.

- The destination examples still allow future inference to bleed into the runtime-first tranche.
  - `Arsenal`, `research todo`, and outline/talking points are runtime-real.
  - “external research support flows” and “future Book Modeler-adjacent destinations” are still mostly strategic or aspirational.
  - They should remain clearly appendix-level or explicitly flagged as non-runtime rows.

- The memo now defers primary analyzer-side attachment-point analysis correctly, but one line still muddies that boundary.
  - The “Recommended inspection surface” still includes current analyzer-v2 presenter/schema seams.
  - That is defensible as context gathering, but it cuts slightly against the memo's otherwise clean “post-extraction addendum only” rule.
  - The cleaner version would say those seams are optional contextual awareness now, primary audit material later.

## 4. Factual Discrepancies I Found

- The revised memo is now much closer to the runtime evidence, but one distinction should remain explicit:
  - NotebookLM-backed lookup is evidenced through the research-todo lifecycle in `useResearchTodos.ts` and the research card flows.
  - It is not a distinct first-hop destination on the same level as Arsenal or research todo creation.

- The runtime-real first-hop destinations evidenced by code are:
  - Arsenal
  - research todos
  - outline/talking points
  - annotation/comment/QA persistence

- `OutlinePanel.tsx` and `OutlineEditorPanel.tsx` mainly govern downstream destination-internal management after routing has already occurred.
  - They are useful evidence for the downstream surface area.
  - They are weaker evidence for initial output-to-destination routing than the capture/findings/research-card seams.

- `analyzer-mgmt` still should not be read as stable contract evidence.
  - The `logic_gap` prompt/schema mismatch remains:
    - `seed_rhetoric.py` asks for `missing_premise`, `benanav_attack`, and `suggested_revision`
    - `populate_rhetoric_schemas.py` expects `hidden_premise`, `subject_attack`, and `suggested_fix`
  - So the memo is right to demote it, and it should stay demoted.

## 5. What This Changes For The Larger Roadmap

- This revised memo now genuinely supports the intended order:
  - extraction tranche continues
  - runtime-first operations/routing inventory runs alongside it
  - later `Close Read V1` memo is written from that evidence

- The roadmap can now name a future contract layer more cleanly:
  - semantic affordances over outputs
  - routing hints for downstream destinations
  - without prematurely binding that layer to a final analyzer schema

- The revised memo is now more aligned with the thin-host thesis.
  - The strongest architecture reading remains:
    - analyzer-v2 should eventually expose enough semantic meaning that thin hosts do not reconstruct analysis semantics locally before offering valid actions
    - hosts still operationalize those actions in product-specific UX

- `Close Read` is better positioned by this revision.
  - The memo now feels more like preparatory evidence gathering for a later flagship memo than an early attempt to smuggle in a full product design exercise.

## 6. The Most Defensible Next Move After This Memo

Execute this revised tranche, but structure the output in two levels.

1. Make the primary matrix strictly about first-hop runtime operations.
   - Examples:
     - capture -> Arsenal
     - capture -> research todo
     - finding -> Arsenal
     - vulnerability revision acceptance -> Arsenal
     - comment/highlight -> talking point
     - research-answer selection -> Arsenal
     - research-answer selection -> research todo

2. Put destination-internal lifecycle flows in a secondary section or appendix.
   - Examples:
     - research queue/lookup/refresh
     - NotebookLM-backed answer handling
     - outline upgrade/extract/save-summary flows

3. Keep `analyzer-mgmt` as an appendix-level evidence source for vocabulary only.
   - Use it to suggest hypothesis labels and semantic preconditions.
   - Do not mix it into the runtime-real inventory rows as equivalent evidence.

4. Keep analyzer-side discussion narrow until extraction lands.
   - A short post-extraction addendum can inspect likely metadata seams.
   - The main inventory should remain product/runtime evidence-backed.

Bottom line:

- the revised memo is now the right immediate product-side companion to the extraction tranche
- it now mostly avoids conflating host-local behavior with analyzer-owned law
- it now defers analyzer attachment-point analysis in the right order
- the main remaining improvement is to separate first-hop routing inventory from downstream destination lifecycle so the tranche stays as small and strong as intended
