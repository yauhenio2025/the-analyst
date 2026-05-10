# Memo: Close Read Operations And Routing Inventory

Subtitle: Runtime-first inventory of downstream operations, routing seams, and affordance hypotheses

Date: 2026-04-01
Program: Dynamic Bespoke Apps Platformization
Scope Source:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_scope.md`
Direction Context:
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
Companion Analyzer Tranche:
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`
Appendix:
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`

## Summary

This inventory confirms that the current product surface is already larger than rendered analysis alone.

The strongest runtime evidence is in `the-critic`, where current code already supports:

- selection capture
- routed promotion to Arsenal
- routed creation of research todos
- comment and annotation persistence
- routed creation of outline / talking-point artifacts
- research-answer selection routing to Arsenal and research

The inventory also confirms a clean separation that matters for the roadmap:

- **first-hop operations** are real and already implemented
- **destination-internal lifecycle** is real but should be documented separately
- `analyzer-mgmt` is useful secondary evidence of intent and schema richness, not runtime law

The resulting recommendation is still the same:

- keep the active analyzer-side extraction tranche in place
- treat this inventory as the product-side companion
- delay any analyzer-side affordance schema work until after extraction lands

## Method

This tranche stayed runtime-first.

Primary runtime evidence was taken from `the-critic`, especially:

- capture state and action surfaces
- research question formulation
- findings promotion flows
- research-answer comment/routing flows
- outline/talking-point routing

Secondary intent/schema evidence was taken from `analyzer-mgmt`, especially:

- plan-side `research_question`
- rhetoric / logic-gap prompt and schema artifacts

Analyzer-side attachment-point design was deliberately deferred.

## Findings

### 1. The real first-hop routing surface is already concrete

The current runtime-real first-hop routes evidenced by code are:

- selection capture -> Arsenal
- selection capture -> research todo
- finding -> Arsenal
- vulnerability revision acceptance -> Arsenal
- finding comment -> outline talking point
- findings comment / QA state -> annotations persistence
- research-answer comment -> research comment record
- research-answer selection -> Arsenal
- research-answer selection -> research todo

These operations are not hypothetical.
They already exist as concrete callbacks and endpoint seams in Critic.

### 2. Research-answer routing is runtime-real, not latent

One important correction from review:

- research-answer selection -> Arsenal/research is already live

The runtime chain is:

- `ResearchCard.handleSendToArsenal` / `handleSendToResearch`
- passed into `ResearchAnswerBlock`
- passed into `ResearchCommentPopup`
- rendered as destination buttons in `ResearchComments.tsx`
- executed through `CaptureContext.submitCapture(...)`

So these rows belong in `runtime_real`, not `latent_intent`.

### 3. First-hop routing and destination lifecycle are different classes

The runtime audit also confirms that these must stay separate:

**First-hop routing**
- user action on an analysis or research surface
- immediate artifact creation or routing

**Destination-internal lifecycle**
- research queue polling / lookup / refresh
- NotebookLM-backed answer lifecycle
- outline upgrade / extract / saved-summary flows

Both matter, but mixing them in one undifferentiated table would blur the inventory.

### 4. `analyzer-mgmt` is useful, but only as secondary evidence

`analyzer-mgmt` currently contributes:

- plan-side research intent
- richer logic-gap / attack / revision shape
- evidence that some future follow-up operations need premise- and vulnerability-aware structure

It does **not** currently contribute hardened runtime operation/routing law.

The logic-gap prompt/schema mismatch is still real:

- prompt side names `missing_premise`, `benanav_attack`, `suggested_revision`
- schema side names `hidden_premise`, `subject_attack`, `suggested_fix`

So it is best treated as:

- product-intent and schema-richness evidence

not:

- runtime proof

### 5. Candidate affordance hypotheses are now clearer

Without designing analyzer schema yet, the inventory suggests a first hypothesis set:

- `capturable`
- `commentable`
- `supports_text_anchor_context`
- `allowed_destinations`
- `question_generatable_from_selection`
- `promotable_to_arsenal`
- `routable_to_research_todo`
- `routable_to_outline_talking_point`
- `supports_async_research_lifecycle`
- `supports_premise_scrutiny`

These remain hypotheses only.
This tranche does not assign final field names, attachment points, or wire shape.

## Recommendation After Extraction

Once the active composition metadata extraction tranche lands, the smallest follow-on tranche should be:

- one bounded analyzer-side affordance-annotation scope for **first-hop** operations only

The recommended starting family is:

- capture/routing eligibility on rendered analytical surfaces

That follow-on should stay narrow:

- start with `capturable`, `commentable`, and a bounded `allowed_destinations` idea
- do not absorb destination-internal lifecycle
- do not absorb host UX
- do not try to generalize Book Modeler or other aspirational routes yet

## Honest Claim

If this inventory is used honestly, the claim should remain narrow:

- we now have a code-backed map of the downstream first-hop operations and adjacent lifecycle surfaces that a future `Close Read` flagship will need, plus a first set of semantic-affordance and routing-hint hypotheses to revisit after extraction

It does **not** yet mean:

- analyzer-v2 owns operation-family law
- analyzer-v2 has a settled affordance schema
- `Close Read` has been fully product-scoped
- host UX can now be generalized automatically
- aspirational destinations like `Book Modeler` are runtime-real

## Verification Note

This was a docs-and-code audit tranche.
No tests were run.
