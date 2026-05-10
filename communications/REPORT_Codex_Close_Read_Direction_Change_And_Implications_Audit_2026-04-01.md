# Audit: Close Read Direction Change And Implications

## Verdict

`approve with corrections`

The memo is directionally right on the two most important points:

- the product gap is larger than renderer/output-family law alone
- the next analyzer move should still be the already-scoped Phase E composition metadata extraction, not a premature `Close Read` app build

But it needs correction in three places:

- it overstates how much `analyzer-mgmt` already embodies live downstream patterns
- it understates the existing strict served-renderer law already present in analyzer-v2
- it reaches too quickly from real downstream patterns to `Close Read` as the singular product destination, when the canonical roadmap still frames analyzer-v2 as substrate for dynamic bespoke apps in the plural

## The Memo's Strongest Code-Backed Points

- The missing layer is not just rendering. In `the-critic`, the runtime already supports post-analysis action and routing:
  - `webapp/src/contexts/CaptureContext.tsx:14-45,87-145` defines capture across `genealogy`, `research`, and `analysis`, then routes captures to `to-arsenal` or `to-research-todo`
  - `webapp/src/pages/FindingsPage.tsx:238-275` persists comments and QA history as durable follow-up work
  - `webapp/src/pages/FindingsPage.tsx:424-444` routes comment-derived artifacts into `/outline/talking-points`
  - `webapp/src/pages/FindingsPage.tsx:632-683,1572-1600` loads Arsenal status and promotes findings/revisions into Arsenal
  - this is already `analysis surface -> user action -> routed artifact`, not just `analysis surface -> final render`

- Analyzer-v2 does not yet own that downstream law. A targeted search across `src/presenter`, `src/api`, and `src/orchestrator` found no analyzer-side `Arsenal`, `research_todo`, `to-arsenal`, or `to-research-todo` seams. The memo is therefore right that a product layer is missing upstream rather than merely absent downstream.

- The analyzer-side presenter remains centrally hard-coded in exactly the way the current Phase E memo identifies:
  - `src/presenter/compose_from_intent.py:82-119` hard-codes `_LEAF_PATTERN_BY_ROLE`, `_PRESENTATION_STANCE_BY_ROLE`, and `_ROLE_FROM_ENGINE_KEY`
  - `src/presenter/compose_from_intent.py:778-800` still resolves semantic role through central hint/engine/title heuristics
  - `src/presenter/compose_from_intent.py:704-747` still hard-codes workflow-shaped grouping and parent shell titles like `AOI Comparison` / `AOI Briefing`
  - `src/presenter/manifest_builder.py:117-135` still falls back to `raw_json` when the consumer does not support a renderer

- The recent roadmap context still points to extraction before any sharper product pivot:
  - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:387-425`
  - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:338-378`
  - `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md:27-31,62-78,206-224`
  - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1381-1385`

- There is already an obvious extraction direction in code. `src/presenter/composition_source_bridge.py:45-70` contains bounded AOI source-family definitions with `composition_role_hint`, which shows the analyzer already has one metadata-like seam for role hints. That strengthens the memo's claim that extraction is the right next move.

## The Memo's Weakest Or Overstated Assumptions

- `Close Read` is a good north-star proving ground, but the memo overstates it as the singular destination. The canonical roadmap still frames analyzer-v2 as substrate for dynamic bespoke apps and thin host shells in the plural:
  - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:43-66`
  - The stronger claim is: `Close Read` is the best concrete flagship product target now, not that it supersedes the broader platform thesis.

- The memo is too generous about `analyzer-mgmt` as already-embodied downstream law.
  - `frontend/src/pages/plans/[id].tsx:181-188` only proves that a `research_question` is displayed in the plan UI.
  - `scripts/seed_rhetoric.py:138-146,550-573` and `scripts/populate_rhetoric_schemas.py:216-231` prove there is real thinking around logic-gap follow-up structures, but these are seeding/prompt/schema scripts, not analyzer-owned runtime contracts or integrated UI flows.
  - So `analyzer-mgmt` is evidence of latent product logic, not yet strong evidence of hardened downstream product law.

- The memo implies follow-up operations are broadly engine/path-specific. The code shows a split reality:
  - some operations are generic across source types, for example capture itself in `CaptureContext.tsx:14-45`
  - some operations are output-specific, for example logic-gap revision acceptance in `FindingsPage.tsx:1572-1600`
  - this means the future law is probably not one monolithic “engine-specific follow-up family” layer; it is at least:
    - generic capture/annotation operations
    - output- or surface-specific follow-up operations
    - artifact destination/routing contracts

- The memo moves too quickly from “real downstream patterns exist” to “write a full `Close Read V1` target-state memo now.” The stronger and smaller step is to inventory concrete operations and destinations first, then write the larger product memo from audited evidence.

## Factual Discrepancies

- The memo understates current validator discipline.
  - It is true that `presentation_bridge.py` validates in WARN mode: `src/presenter/presentation_bridge.py:468-499`
  - It is also true that assembly-time validation in `presentation_api.py` is WARN-only: `src/presenter/presentation_api.py:1507-1538`
  - And `src/renderers/validator.py:1-6,49-53` confirms WARN is the default pipeline mode
  - But the memo omits that `src/presenter/renderer_contract_enforcement.py:120-170,217-242` already applies strict/shadow/warn served-intent policy, with transient compose outputs always strict and selected AOI/genealogy served surfaces already fail-closed
  - So the true problem is not “validation is only WARN”; it is that validator discipline is split across multiple boundaries and only partially generalized

- The memo understates how much hard-coded presenter logic remains outside the first role/pattern/stance maps.
  - `src/presenter/compose_from_intent.py:148-189` still hard-codes supported handoff kinds, transient consumer adapters, and source-profile admission
  - `src/presenter/compose_from_intent.py:704-747` still hard-codes grouping and parent-shell naming logic
  - The current Phase E scope correctly leaves some of this out as later work, but the memo should name that the remaining policy surface is broader than the first three maps

- The analyzer-mgmt rhetoric evidence is internally inconsistent, which weakens the memo's claim that it already embodies stable follow-up law.
  - `scripts/seed_rhetoric.py:568-571` asks for `gap_type=non_sequitur/missing_premise/inferential_leap/overgeneralization/false_dichotomy`, `benanav_attack`, and `suggested_revision`
  - `scripts/populate_rhetoric_schemas.py:224-228` expects `gap_type=non_sequitur/hidden_premise/false_dichotomy/hasty_generalization/circular_reasoning/equivocation`, `subject_attack`, and `suggested_fix`
  - That is evidence of product intent, not settled contract law

- The cited downstream files support Arsenal, research todo capture, comments/QA, and outline/talking-point routing. They do not directly support current Book Modeler routing, and the cited files do not directly show NotebookLM routing either. Those parts of the memo are still mostly strategic inference from dictation rather than code-backed fact.

## What This Changes For The Larger Roadmap

- Do not move the next analyzer tranche away from Phase E composition metadata extraction. The code and roadmap context still support that as the immediate prerequisite.

- Add a new explicit future layer to the roadmap after the extraction work: operation-family law plus artifact-routing law. The memo is correct that renderer-family and output-family framing alone is no longer enough.

- Treat `Close Read` as a flagship proving ground for the broader platform, not as a replacement for the broader “dynamic bespoke apps” destination. That keeps the roadmap consistent with the canonical platform thesis while still honoring the new product insight from the dictation.

- Separate three future contract problems rather than collapsing them:
  - renderer/output projection law
  - follow-up operation law
  - artifact destination/routing law

- Raise the risk level on presenter policy sprawl. If operation and routing logic are introduced before the remaining hard-coded admission/grouping/policy seams are extracted, the program will reproduce the same coupling in a new shell under a new name.

## The Most Defensible Next Move After This Memo

1. Keep the next analyzer implementation move exactly where the roadmap already put it:
   - execute `Phase E Composition Metadata Extraction V1`
   - keep it analyzer-side and behavior-preserving
   - use the existing bounded metadata direction in `src/presenter/composition_source_bridge.py` as the natural pattern to extend

2. Make the product-side move smaller than the memo recommends:
   - do not start with a full `Close Read V1` target-state memo
   - first produce one bounded operation-and-routing inventory from live `the-critic` flows and the `analyzer-mgmt` rhetoric artifacts
   - classify each operation as:
     - generic capture/annotation
     - output-specific follow-up
     - destination/routing contract

3. Only after that inventory is real should the program write a `Close Read` product memo.
   - At that point the memo can be honest about what is actually implemented
   - It can avoid inventing premature mega-app scope
   - It will have a concrete basis for deciding what analyzer-v2 should own versus what should stay in the host

In short:

- the memo is right that the product gap is bigger than renderer law
- it is right that `Close Read` is the best new north-star framing
- it is right that the next analyzer code move should still be composition metadata extraction

But the stronger correction is:

- treat `Close Read` as the next flagship proving ground, not the singular destination
- treat `analyzer-mgmt` as partial evidence, not hardened proof
- and make the immediate product follow-up a bounded operations/routing inventory, not a larger target-state design exercise
