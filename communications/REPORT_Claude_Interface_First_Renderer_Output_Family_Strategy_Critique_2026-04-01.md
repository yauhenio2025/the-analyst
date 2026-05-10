# Critique: Interface-First Renderer / Output-Family Strategy

Date: 2026-04-01
Reviewer: Claude (Opus 4.6, fresh session)
Memo Under Review: `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
Program: Dynamic Bespoke Apps Platformization
Roadmap Context:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

---

## 1. Verdict

**Approve with corrections.**

The memo's strategic direction is right. But the memo significantly understates the actual level of workflow-specific coupling in the current composition pipeline, which means its implied "we're closer than it seems" framing is too optimistic about the distance between where we are and where this strategy needs us to be.

---

## 2. Strongest Parts of the Memo

### A. The renderer catalog really is bounded and that really does matter

The live catalog is 9 renderers. 8 of 9 have real `input_data_schema` definitions (only `raw_json` has an empty schema, which is intentional). The memo's claim that the UI problem is better framed as "how many renderer families?" rather than "how many bespoke engine UIs?" is genuinely supported by the code.

Code-backed evidence:
- `src/renderers/definitions/` contains exactly 9 JSON files
- `accordion`, `card_grid`, `evidence_trail`, `prose`, `stat_summary`, `tab`, `table`, `timeline` all have non-empty `input_data_schema`
- `RendererDefinition` in `src/renderers/schemas.py` already carries `ideal_data_shapes`, `primitive_affinities`, `config_schema` — the right metadata for contract-based matching

### B. The consumer-capability inversion is real architecture, not just scaffolding

`src/consumers/schemas.py` models consumer support via `supported_renderers` and `supported_sub_renderers`. `src/presenter/manifest_builder.py:105-135` implements `adapt_renderer_for_consumer()` as a genuine consumer-neutral fallback seam. This is not a stub — it drives real behavior in the manifest builder loop.

### C. The "bounded LLM projection, not freeform" discipline is the right rule

The memo's distinction between "LLM fills one strict target schema" vs "LLM improvises UI structure" is exactly the right line to draw. The current codebase already has one example of each:

- Good version: `src/views/generator.py` uses LLM to fill a `ViewDefinition` (strict Pydantic schema) from a pattern + engine context, then validates via `ViewDefinition.model_validate()`
- Dangerous version: `src/presenter/compose_from_intent.py` uses LLM to generate dynamic extraction prompts and transformation payloads that are then trusted as composition inputs — this is closer to freeform structure invention

### D. The composition-law-as-differentiator framing is correct

The memo correctly identifies that if renderer families and output families are bounded, the hard platform problem shifts to composition law. That is the right reframe.

---

## 3. Weakest Assumptions

### A. The memo dramatically understates current workflow-specific coupling

The memo says:

> "The current substrate is still bounded and partly hand-tuned, but the architectural direction is already compatible with an interface-first strategy."

This is too generous. A thorough audit of `src/presenter/compose_from_intent.py` (1,632 lines — the actual composition orchestrator) reveals:

- **24+ workflow-specific conditional branches** across the presenter pipeline
- **30+ hardcoded keys** (workflow keys, consumer keys, engine-to-role mappings, composition modes)
- **Explicit AOI/genealogy dichotomy baked into the data model**:
  - `_SUPPORTED_HANDOFF_KINDS`: AOI gets 3 handoff kinds, genealogy gets 1 (`compose_from_intent.py:149-157`)
  - `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS`: per-consumer handoff kind whitelist (`compose_from_intent.py:158-185`)
  - `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`: per-consumer source profile whitelist (`compose_from_intent.py:186-189`)
  - `_ROLE_FROM_ENGINE_KEY`: hardcoded mapping of 8 specific engine keys to 5 semantic roles (`compose_from_intent.py:110-119`)

- **Three separate composition entry points** with workflow-specific dispatch:
  - `compose_from_intent()` — the original AOI path
  - `compose_from_source()` — AOI source-profile path
  - `compose_from_selection()` — AOI source-selection path

- **Renderer contract enforcement is mode-branched** (`src/presenter/renderer_contract_enforcement.py`):
  - `_STRICT_AOI_COMPOSITION_MODES` (2 modes)
  - `_STRICT_GENEALOGY_COMPOSITION_MODES` (1 mode)
  - `_SHADOW_GENEALOGY_COMPOSITION_MODES` (3 modes)
  - Different enforcement policies per workflow family

This is not "partly hand-tuned." This is an AOI-and-genealogy-specific orchestration system that happens to pass some parameters generically. Onboarding a new workflow today would require touching 5+ files and adding entries to multiple hardcoded dictionaries.

### B. The memo conflates "renderer families" with "output families" without accounting for the projection gap

The memo proposes two layers:

1. Renderer families (the 9 renderers)
2. Output families (semantic artifacts like "findings bank", "sectioned analysis", etc.)

But the memo does not account for the actual projection gap between them. Today that projection is done by:

- `_ROLE_FROM_ENGINE_KEY` — a hardcoded dict mapping 8 engines to 5 roles
- `_LEAF_PATTERN_BY_ROLE` — a hardcoded dict mapping 5 roles to view patterns
- `_PRESENTATION_STANCE_BY_ROLE` — a hardcoded dict mapping 5 roles to stances

The memo proposes that future engines "declare how they project into those families." But the current code does the opposite: the composition orchestrator hardcodes the projection per engine. There is no engine-side declaration metadata today — engines do not carry output-family, composability-role, or preferred-renderer fields.

The gap between the current state (centralized hardcoded projection) and the proposed state (engine-declared projection) is larger than the memo acknowledges.

### C. The memo understates how much composition law is workflow-shaped, not family-shaped

Even after you factor out renderer families, the composition decisions remain workflow-shaped:

- **Handoff kind dispatch**: AOI supports `direct_sections`, `source_profile`, `source_selection`. Genealogy supports only `direct_sections`. These are not output-family distinctions — they are workflow-level architectural decisions about how analytical results get composed.
- **Source bridge logic**: `compose_from_source()` and `compose_from_selection()` use fundamentally different data flows than `compose_from_intent()`. The memo treats these as minor variants; in code they are 3 distinct orchestration paths.
- **Profile-specific intent defaults**: `_SOURCE_PROFILE_DEFAULT_INTENTS` hardcodes AOI-specific prose for "dossier" vs "comparison" profiles.
- **Consumer admission gates**: `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` gates which consumers can use which handoff kinds — this is not renderer-family law, it is operational consumer-workflow admission control.

These are composition-law decisions, and they are currently workflow-specific, not family-generic.

---

## 4. Code-Backed Findings

### Finding 1: Only `dynamic_prompt.py` is genuinely generic

Of 8 files audited in the presenter pipeline (totaling ~8,500 lines), exactly one — `src/presenter/dynamic_prompt.py` (338 lines) — operates generically over its inputs with zero hardcoded workflow, consumer, or engine references. This file composes LLM extraction prompts from engine metadata + renderer shape + stance, and is the closest existing code to what the memo envisions.

### Finding 2: Renderer schemas are real but shallow

8 of 9 renderers have `input_data_schema`. But the schemas are small (199-1005 chars of JSON Schema). For example, `evidence_trail` has 199 chars — that's barely a type declaration. For the "strict contracts" claim to hold, these schemas would need to be substantially richer.

### Finding 3: The `preparation_coordinator.py` is also genuinely generic

`src/presenter/preparation_coordinator.py` (295 lines) orchestrates preparation steps without workflow-specific branching. This is the second file (of 8) that achieves real generality.

### Finding 4: The view refiner's system prompt is genealogy-biased

`src/presenter/view_refiner.py:57` contains:

```
SYSTEM_PROMPT = """You are a presentation curator for intellectual genealogy analyses.
```

This is used for ALL workflows, not just genealogy. That is a concrete example of the kind of coupling the memo's strategy would need to eliminate.

### Finding 5: Consumer adaptation is real but minimal

`adapt_renderer_for_consumer()` in `manifest_builder.py:105-135` does exist and works. But its logic is: if unsupported, fall back to `raw_json`. That is one if-else, not a rich adaptation layer. The memo describes this as "the right seam" — that is correct directionally, but the seam is still a single-fallback stub.

---

## 5. Strategic Implications for the Larger Roadmap

### The memo is directionally aligned with Phase E

The distilled strategic roadmap's Phase E asks: can analyzer-v2 compose across arbitrary engine/pass combinations by contract, not by custom host behavior? The interface-first strategy is one valid approach to answering that question.

### But the memo skips the extraction cost

The memo proposes defining output families and making engines declare projections into them. That is the right destination. But the current codebase has ~30 hardcoded keys and ~24 workflow-specific branches that would need to be refactored before that destination is reachable.

The strategic implication is: this is not primarily a "define new contracts" problem. It is first a "extract and generalize the workflow-specific law that already exists" problem. The memo frames it as if the next step is taxonomy design. The actual next step is extraction surgery on `compose_from_intent.py` and `renderer_contract_enforcement.py`.

### The LLM-projection risk is real and present

The memo correctly identifies the risk that "bounded LLM projection quietly turns into freeform structure invention." That risk is **already partially realized** in the current code. `compose_from_intent.py` uses LLM calls for view generation and dynamic transformation within the composition pipeline. Whether those calls are "bounded schema-filling" or "soft structure invention" depends on how strictly the downstream validators enforce. Today, the validator mode is `WARN` (log, don't block) — see `src/renderers/validator.py:50-53`. So the pipeline already tolerates invalid LLM-projected payloads.

### The lifecycle question is orthogonal

The memo barely mentions lifecycle, which is appropriate for its scope. But the roadmap context shows that lifecycle generality (save/reopen across request families) is the current active Phase E frontier. Output-family taxonomy work and lifecycle generality work are not sequentially dependent — they could proceed in parallel. The memo should be explicit that it is not proposing to defer or replace the lifecycle question.

---

## 6. Concrete Corrections and Reframing

### Correction 1: Replace "partly hand-tuned" with honest coupling assessment

The memo should state plainly:

- The current composition pipeline is an AOI-and-genealogy-specific system with ~30 hardcoded keys and ~24 workflow-conditional branches
- Onboarding a new workflow today requires touching multiple files and multiple dictionaries
- The path to generic output-family composition requires substantial extraction work, not just taxonomy definition

### Correction 2: Separate the three distinct problems

The memo conflates three things that should be tracked separately:

1. **Renderer-family boundedness** — already proven, already stable, genuinely small (9 renderers). This is the strongest claim in the memo and needs no further proof.

2. **Output-family taxonomy** — does not yet exist. No engine today declares its output family, composability role, or preferred renderer. The memo proposes this as if it's the next step; the actual next step is defining the taxonomy AND adding the declaration metadata to engine definitions AND refactoring `compose_from_intent.py` to consume those declarations instead of hardcoded dicts.

3. **Composition-law generalization** — the hardest problem. The memo acknowledges this in its "Risk 3" section but does not give it enough weight. The current composition law is not family-generic. The three entry points (`compose_from_intent`, `compose_from_source`, `compose_from_selection`) encode different data-flow architectures, not just different parameter values.

### Correction 3: Reframe the near-term work

Instead of the memo's proposed near-term decision (inventory renderer families → define output taxonomy → map engines), a more honest framing is:

1. **Inventory the current hardcoded coupling** — what workflow-specific decisions actually exist in the composition pipeline today? (This critique provides that inventory.)

2. **Classify each coupling as either**:
   - family-generic (can be expressed as output-family metadata on the engine definition)
   - composition-law (requires composition-level intelligence that cannot be reduced to engine-side metadata)
   - operational-admission (consumer/workflow gating that is fundamentally a policy decision)

3. **Extract the family-generic couplings first** — move `_ROLE_FROM_ENGINE_KEY`, `_LEAF_PATTERN_BY_ROLE`, `_PRESENTATION_STANCE_BY_ROLE` into engine definition metadata. This is the lowest-risk, highest-signal first step.

4. **Then attack composition-law generalization** — unify or parameterize the three composition entry points so that adding a workflow does not require new orchestration code.

5. **Leave operational-admission gating last** — consumer/workflow admission control is policy, not architecture. It can stay hardcoded longer without blocking the strategy.

### Correction 4: Acknowledge the validator discipline gap

The memo proposes "fail closed if invalid." The current validator default is `WARN` (never blocks). That gap should be named, because it means the "strict contracts" story is aspirational, not operational. The memo should either propose changing the default to `STRICT` (which would break current pipelines) or propose a phased tightening plan.

### Correction 5: Name the honest work quantum

The memo's "proposed near-term decision" (Section: Proposed Near-Term Decision) lists 5 steps that sound like a weekend of taxonomy design. The honest work quantum is larger:

- Define 6-10 output families with schemas
- Add output-family metadata to 160+ engine definitions (or at least the ~30 that are composition-relevant)
- Refactor `compose_from_intent.py` to consume engine-declared metadata instead of `_ROLE_FROM_ENGINE_KEY`
- Refactor `renderer_contract_enforcement.py` to work on family-level policy instead of mode-level branching
- Update the view refiner system prompt to be workflow-neutral
- Tighten the validator from WARN to at least WARN-with-metrics toward eventual STRICT

That is a real generalization tranche, not a taxonomy design exercise.

---

## Summary

The memo gets the direction right: renderer families are bounded, the UI problem should be framed as a bounded-contract problem, and analyzer-v2 should own the projection and composition law. These are correct strategic claims.

The memo understates three things:

1. **The current coupling is deep** — ~30 hardcoded keys, ~24 workflow branches, 3 distinct composition entry paths
2. **The projection gap is large** — no engine today declares its output family; all projection is centrally hardcoded
3. **The composition-law problem is harder than the renderer-family problem** — composition is workflow-shaped today, not family-shaped

The recommended reframing: treat this as an extraction-and-generalization program, not a taxonomy-and-declaration program. The taxonomy is the easy part. Extracting the workflow-specific law into family-generic contracts is the hard part, and that work needs to be named honestly.
