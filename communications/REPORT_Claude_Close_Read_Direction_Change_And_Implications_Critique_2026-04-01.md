# Critique: Close Read Direction Change And Implications

Reviewer: Claude (Opus 4.6, fresh session)
Date: 2026-04-01
Subject Memo: `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
Reference Dictation: `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`

---

## 1. Verdict

**Approve with corrections.**

The memo correctly identifies a real missing layer (operation families and artifact routing), correctly keeps the next implementation move as composition metadata extraction, and correctly avoids jumping to a new product build. But it overstates the code evidence, mischaracterizes the nature of some references, and risks premature product-target framing that could distort prioritization.

---

## 2. Strongest Parts Of The Memo

### A. The three-layer decomposition is genuinely sound

The distinction between:

- renderer families (bounded interface surfaces)
- output families (canonical semantic artifacts)
- operation families (follow-up actions valid on specific outputs)
- artifact routing (downstream destinations)

is real and not artificial. These are different concerns with different ownership boundaries. The current roadmap talks mainly about the first two; the dictation makes the third and fourth impossible to ignore. That observation is correct.

### B. Keeping Phase E composition metadata extraction as the next code move is disciplined

The memo resists the temptation to jump from a strategic dictation into a product build. It correctly reasons:

- the dictation changes the frame more than it changes the next move
- the current presenter coupling still needs extraction before operation families can be defined honestly
- skipping extraction would mean Close Read inherits the same AOI/genealogy-shaped presenter code

This is the correct judgment. The code confirms it: `compose_from_intent.py` still has 8 hard-coded entries in `_ROLE_FROM_ENGINE_KEY`, workflow-specific handoff-kind admission in `_SUPPORTED_HANDOFF_KINDS`, and consumer-specific adapter registrations. Until those are externalized, adding a new product target on top of them would create the same per-app coupling the program is trying to eliminate.

### C. The "do not overbuild the final super-app" discipline is correct

The memo says: "The dictation defines a north star, not necessarily the first implementation form." That is the right reading of the dictation, which itself uses language like "maybe," "I guess my broader point is," and "we can do it in such a way that through practice and use, we will keep adding them."

---

## 3. Weakest Assumptions

### A. CaptureContext.tsx is Critic-local, not platform evidence

The memo claims:

> "webapp/src/contexts/CaptureContext.tsx already models capture state and downstream destination intents like `arsenal` and `research_todo`"

This is true as a code fact. But CaptureContext is a **Critic-local React context**. It hits Critic's own API endpoints (`/api/captures`, `/api/captures/{id}/to-arsenal`, `/api/captures/{id}/to-research-todo`). It knows nothing about analyzer-v2. The capture/route flow is entirely host-side logic.

This is evidence that the **product** has downstream operation patterns. It is not evidence that **analyzer-v2 should own operation-family law**. The memo conflates "the product already does this" with "analyzer-v2 should define which follow-up operations are valid." Those are different claims with different implications.

### B. Rhetoric seed scripts are analysis-output schemas, not operation-family evidence

The memo claims:

> "scripts/seed_rhetoric.py already models follow-up logic like `logic_gap`, `premise`, `missing_link`, `severity`"

This misdescribes what those scripts contain. `seed_rhetoric.py` defines **rhetoric analyzer types** (deflection, contradiction, logic_gap, etc.) with their document requirements. `populate_rhetoric_schemas.py` defines **output schemas** for those analyzers — the shape of findings, not follow-up actions.

The `benanav_attack` field in the logic_gap schema and the `severity` field in multiple schemas describe **attributes of analysis findings**, not user follow-up operations. "What severity is this finding?" is analysis output metadata. "Promote this finding to Arsenal" is a follow-up operation. The memo treats them as the same thing.

### C. The NEXT_SESSION_ANNOTATIONS_PANEL.md reference is off-target

The memo cites this file as documenting "inline comment and research-answer interaction patterns." In reality, the file is a **UI bug-fix ticket** for making an annotations panel sticky-scrollable and fixing click-to-align. It documents CSS overflow debugging, not operation-family patterns. This weakens the code-evidence section.

### D. FindingsPage.tsx Arsenal flow is basic CRUD, not sophisticated operation-family evidence

The Arsenal toggle in FindingsPage.tsx is a simple add/remove toggle: `toggleArsenal` calls `POST /arsenal` or `DELETE /arsenal/{id}`. It stores a `Set<number>` of finding IDs. This is standard CRUD UI interaction, not evidence of complex operation-family routing that analyzer-v2 should own the law for.

### E. The dictation itself is more exploratory than the memo treats it

The dictation uses language like:

- "Maybe we have not actually done that as much in Anxiety of Influence"
- "I guess my broader point is"
- "we basically try to understand"
- "We can do it in such a way that through practice and use, we will keep adding them"
- "We need to start lean"

The memo converts this exploratory ideation into "the dictation makes impossible to ignore." That overstates the directive force of the dictation. The dictation is directionally real but explicitly tentative.

---

## 4. Code-Backed Findings

### 4.1 compose_from_intent.py coupling is real but more declarative than spaghetti

The hard-coded maps are:

| Map | Entries | Nature |
|-----|---------|--------|
| `_ROLE_FROM_ENGINE_KEY` | 8 | engine → semantic role |
| `_LEAF_PATTERN_BY_ROLE` | 5 | role → view pattern |
| `_PRESENTATION_STANCE_BY_ROLE` | 5 | role → stance |
| `_SUPPORTED_HANDOFF_KINDS` | 2 workflows | workflow → allowed handoff kinds |
| `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` | 4 consumers | consumer → allowed handoff kinds |
| `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER` | 2 consumers | consumer → allowed profiles |

The role/pattern/stance maps are the extraction target the Phase E scope memo identifies. They are straightforward to externalize because they are already declarative dictionaries, not procedural branching.

The harder coupling lives in the admission/handoff maps (`_SUPPORTED_HANDOFF_KINDS`, `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS`, `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`). These encode operational policy, not composition metadata. The Phase E scope memo correctly defers them, but the Close Read direction change memo does not acknowledge that the operational/admission layer is the harder problem.

There is only **1 actual workflow-specific branch** in the composition logic (AOI vs generic parent tab titles around line 717). The system is more declarative than "too composition-shaped" suggests.

### 4.2 manifest_builder.py is more mature than the memo implies

`adapt_renderer_for_consumer()` already correctly resolves consumer capabilities from `ConsumerRegistry`, falls back to `raw_json` only when available, and reports adaptations. This is already a proper consumer-contract seam, not a stub. The memo's claim that it "still contains fallback behavior including `raw_json`" frames working architecture as a deficiency.

### 4.3 presentation_bridge.py WARN mode is honest and bounded

The bridge validates in `ValidationMode.WARN`, wraps validation in try/except, and logs without blocking. The memo correctly notes this. But the pipeline architecture is already well-modularized: curated template vs dynamic extraction, cache-first processing, async/sync variants. The "still validates in observational WARN mode" framing undersells the structural maturity.

### 4.4 analyzer-mgmt research_question is a single display field

The plan detail page in `analyzer-mgmt/frontend/src/pages/plans/[id].tsx` displays `plan.research_question` as a read-only italic text block (lines 181-188). It is not "planning/research structure" in any generative sense — it is a display field on a plan summary. The memo overstates this as evidence of "follow-up logic."

---

## 5. Strategic Implications For The Roadmap

### 5.1 Operation families are real but their ownership boundary is the hard question

The dictation correctly identifies that analysis surfaces → follow-up operations → artifact routing is a real product flow. The question is: **where in the stack should operation-family law live?**

Option A (what the memo implies): analyzer-v2 owns operation-family law and tells hosts which operations are valid.

Option B (more aligned with thin-host architecture): analyzer-v2 annotates engine outputs with **semantic affordances** (e.g., "this output supports per-item capture," "this output supports premise scrutiny," "items in this output are individually routable to Arsenal"). Hosts operationalize those affordances according to their own UX patterns.

Option B is more consistent with the existing architecture. CaptureContext.tsx is already host-local. Arsenal routing is already host-local. If analyzer-v2 starts defining `operation_families` and `artifact_routing_destinations`, it becomes coupled to host UX in ways the thin-host principle explicitly avoids.

**Recommendation**: The memo should reframe from "analyzer-v2 must own operation-family law" to "analyzer-v2 should define engine-output semantic affordances; hosts operationalize them." This keeps the brain-of-the-system frame without violating thin-host architecture.

### 5.2 Close Read as north star is premature

The memo is correct that a product target is more useful than abstract architecture generalization. But the current substrate is not yet at a stage where a product target can usefully constrain implementation choices:

1. Output-family taxonomy does not yet exist
2. Composition-law extraction is not yet done
3. The admission/handoff policy layer is still workflow-specific
4. Lifecycle generality is still bounded to one form

Naming "Close Read" as the product target before these substrate layers exist creates one of two risks:

- **Risk A**: The product target drives premature product-specific engineering (shortcuts to make Close Read work without general contracts), reproducing the per-app coupling the program is trying to eliminate.
- **Risk B**: The product target is acknowledged as aspirational and ignored in practice, in which case it adds no implementation value and risks becoming another planning-horizon document that accretes without effect.

**Recommendation**: Defer naming a product target until the composition metadata extraction tranche is complete. At that point, the program will have externalized metadata and can judge whether the substrate supports a product target definition. If you must name it now, call it an "indicative product direction" rather than "the north star."

### 5.3 The Critic/Benanav audit has value but needs a different frame

The memo proposes auditing Critic/Benanav patterns to extract "actual follow-up operation families." That audit has value, but the frame should be:

- **Not**: "what operation families should analyzer-v2 own"
- **Instead**: "what semantic affordance annotations would make engine outputs actionable in downstream apps without coupling analyzer-v2 to host UX"

The audit should produce:

1. A catalog of downstream actions currently implemented in Critic (capture, arsenal routing, research-todo routing, annotation, comment, Q&A)
2. For each action: what properties of the engine output make it valid (e.g., per-item structure, severity field, quotation reference)
3. A proposed annotation vocabulary that analyzer-v2 could attach to engine output metadata

This is more useful than a top-down "operation family" taxonomy because it stays grounded in existing code patterns.

---

## 6. Concrete Corrections And Reframing

### Correction 1: Reduce code-evidence claims to what they actually show

- **CaptureContext.tsx**: Shows the product has capture→route patterns. Does not show analyzer-v2 should own them. Reframe as "product evidence" not "codebase evidence for analyzer-v2 direction."
- **seed_rhetoric.py / populate_rhetoric_schemas.py**: Shows analysis outputs have structured schemas with semantic fields. Does not show follow-up operation families. Reframe as "output schema richness that future affordance annotations could build on."
- **NEXT_SESSION_ANNOTATIONS_PANEL.md**: Remove entirely — it's a CSS bug-fix memo.
- **FindingsPage.tsx Arsenal toggle**: Acknowledge as basic CRUD, not as evidence of complex routing.

### Correction 2: Reframe operation-family ownership

Replace:

> "analyzer-v2 must become the brain not only for analysis generation and composition, but also for determining which follow-up operations are valid on which analytical outputs"

With:

> "analyzer-v2 should annotate engine outputs with semantic affordances that indicate which downstream actions are structurally supportable; hosts decide how and whether to operationalize those affordances"

This preserves the "analyzer-v2 is the brain" frame without making analyzer-v2 responsible for host UX.

### Correction 3: Downgrade Close Read from "north star" to "indicative direction"

The dictation is real input. But it is exploratory. Treat it as an indicative direction that validates the current substrate work, not as a product target that should constrain the next tranche.

### Correction 4: Acknowledge the dictation's own tentativeness

The memo should include a brief acknowledgment that the dictation explicitly hedges ("maybe," "I guess," "we can keep adding them"). The memo currently treats the dictation as more settled than its own language suggests.

### Correction 5: Reframe the Critic/Benanav audit

Propose the audit as "semantic affordance extraction" not "operation family extraction." The deliverable should be a vocabulary of output annotations, not a taxonomy of operations analyzer-v2 must own.

---

## Summary Table

| Aspect | Memo's Claim | Critique Finding |
|--------|-------------|-----------------|
| Missing layer identified | Operation families + artifact routing | Correct, genuinely distinct from renderers/output families |
| Next code move | Phase E composition metadata extraction | Correct, well-justified |
| Close Read as north star | Product target now | Premature — defer until extraction complete |
| CaptureContext as evidence | Shows analyzer-v2 direction | Shows product patterns only, not analyzer-v2 ownership |
| Rhetoric scripts as evidence | Show follow-up operation schemas | Show analysis output schemas, not operation families |
| compose_from_intent coupling | "Still too composition-shaped" | Real but more declarative than implied; extraction is bounded |
| manifest_builder | "Still contains fallback behavior" | Working consumer-contract architecture, not a deficiency |
| Operation-family ownership | analyzer-v2 should own the law | analyzer-v2 should own affordance annotations; hosts operationalize |

---

## End

The memo is directionally right and operationally disciplined. The corrections above strengthen it by grounding the claims more honestly and avoiding premature product-target commitment. The recommended forward move — extraction first, audit second, product framing only when the substrate supports it — is sound with the ownership reframe.
