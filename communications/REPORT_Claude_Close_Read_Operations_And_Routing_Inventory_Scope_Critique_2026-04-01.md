# Critique: Close Read Operations And Routing Inventory Scope

Reviewer: Claude (Opus 4.6, fresh session)
Date: 2026-04-01
Subject Memo: `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_scope.md`
Strategic Context Memos:
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_scope.md`
- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
Prior Reviews:
- `communications/REPORT_Claude_Close_Read_Direction_Change_And_Implications_Critique_2026-04-01.md`
- `communications/REPORT_Codex_Close_Read_Direction_Change_And_Implications_Audit_2026-04-01.md`

---

## 1. Verdict

**Approve with corrections.**

The memo correctly identifies a discovery tranche as the right product-side companion to the extraction tranche. Its sequencing discipline (inventory first, Close Read V1 memo only from evidence) is sound. The four questions it asks are the right questions. But the proposed audit scope is broader than the "smallest honest companion tranche," the source file list is incomplete where it matters most, and one of its three audit areas (analyzer-v2 seam assessment) should be deferred.

---

## 2. Strongest Parts Of The Memo

### A. The sequencing is exactly right

The memo proposes:

1. extraction tranche continues on the analyzer side
2. this inventory tranche documents the real downstream operation/routing surface
3. then a later Close Read V1 memo is written from evidence rather than intuition

Both prior reviews (Claude and Codex) independently converged on this exact sequence. The Codex audit explicitly said: "first produce one bounded operation-and-routing inventory from live the-critic flows... only after that inventory is real should the program write a Close Read product memo." This memo delivers that recommendation faithfully.

### B. The distinction between runtime-real, latent, and aspirational is the key analytical move

The acceptance bar at section 6 correctly demands three-way classification:

- runtime-real downstream operations
- latent product intent
- aspirational future routing

This is the right frame. The prior reviews both flagged that the direction change memo conflated Critic runtime patterns with analyzer-v2 ownership claims. This memo avoids that mistake by making the classification explicit in the inventory schema.

### C. The generic / output-specific / routing-contract distinction is necessary

The memo correctly identifies that downstream operations split into at least three categories:

- generic capture/annotation operations (capture itself, comment creation)
- output- or surface-specific follow-up operations (premise scrutiny, logic-gap revision)
- routing contracts (Arsenal, Research, Outline)

This matches what the code actually shows. CaptureContext.tsx handles generic capture across `genealogy`, `research`, and `analysis` source types. But `logic_gap` revision acceptance in FindingsPage.tsx is output-specific. Arsenal routing is a destination contract. Collapsing these would reproduce the confusion the direction change memo made.

### D. The "discovery/documentation tranche, not a product build" framing is correctly bounded

The memo avoids the temptation to build anything. It avoids the temptation to design affordance schemas. It explicitly excludes changing analyzer routes, adding semantic affordances, or touching hosts. That discipline is correct.

### E. The ownership boundary principle is stated carefully

The memo says: "The deliverable is not 'analyzer-v2 should own every operation.' The deliverable is: a first candidate set of analyzer-owned semantic affordances and routing hints." That distinction matches the reframing both prior reviews recommended: analyzer-v2 should annotate outputs with semantic affordances, hosts should operationalize them.

---

## 3. Weakest Assumptions

### A. This is not quite the smallest honest companion tranche

The memo defines three audit areas:

1. Audit the-critic downstream patterns
2. Audit analyzer-mgmt logic/rhetoric structures
3. Audit analyzer-v2 future attachment points

Area 3 is premature. The Phase E extraction tranche is actively changing the very presenter seams that area 3 proposes to audit. Running both in parallel means the inventory documents seams that extraction will restructure. The inventory would describe `_ROLE_FROM_ENGINE_KEY` and `_LEAF_PATTERN_BY_ROLE` attachment points that the extraction tranche is about to externalize.

**The smallest honest companion tranche is areas 1 and 2 only.** Area 3 should be a short addendum written after extraction lands, when the seams are cleaner and the attachment-point assessment is grounded in the new metadata shape.

### B. The proposed the-critic source list is materially incomplete

The memo lists two files as primary runtime evidence:

- `CaptureContext.tsx`
- `FindingsPage.tsx`

Based on code inspection, the actual downstream operation surface in the-critic is substantially richer than those two files reveal:

| File | What it governs | Why it matters for the inventory |
|------|----------------|--------------------------------|
| `CaptureActionBar.tsx` | The actual UI routing to Arsenal vs Research | Shows the two-destination capture UX surface |
| `ResearchFlagDialog.tsx` | Research question formulation with AI suggestion, scope hints, priority, auto-queueing | The richest routing flow — generates suggested questions via `POST /api/research-todos/suggest-question`, exposes `scope_hints` (books/secondary_lit/empirical), `research_type`, priority, tags, and `Save & Queue` for automatic NotebookLM lookup |
| `useResearchTodos.ts` | Queue polling, NotebookLM lookup, source refresh | The backend research lifecycle: `POST /api/research-todos/{id}/lookup`, `POST /api/research-todos/{id}/refresh-sources`, queue status polling every 3s |
| `ArsenalPage.tsx` | Arsenal display, grouped by stream type, removal | Shows Arsenal is more than a toggle — it's a display surface with stream-typed grouping (rhetoric/vulnerability/genealogy) |
| `OutlinePanel.tsx` / `OutlineEditorPanel.tsx` | Talking point hierarchy, upgrade, navigate-to-source | Shows outline as a real destination with hierarchy, source-type badges, and bidirectional linking to findings |
| `CommentModal.tsx` | Dual-destination flow: comment storage + outline routing | Shows that a single user action (commenting on a finding) can route to two destinations simultaneously |
| `ResearchComments.tsx` | Stub destinations on research answer comments | Has `onSendToArsenal` and `onSendToResearch` callback stubs — evidence of latent routing intent not yet wired |
| `researchConstants.ts` | Research status lifecycle and NotebookLM answer source schema | Defines `draft → queued → in_progress → answered → reviewed → done/archived` and the NotebookLM `notebook_sources`, `notebook_id`, `query_id` shape |

An inventory that only reads `CaptureContext.tsx` and `FindingsPage.tsx` will miss:

- The AI-suggested research question formulation flow (the richest single routing pattern)
- The NotebookLM integration lifecycle
- The dual-destination comment→outline flow
- The research status machine
- The stub routing callbacks in `ResearchComments.tsx` (evidence of latent intent)

### C. The analyzer-mgmt evidence is overframed

The memo says: "Focus on what is useful as evidence of: output richness, logical vulnerability structures, premise / attack / missing-link schema shape, plan-side research intent."

Both prior reviews flagged this. `seed_rhetoric.py` defines **analysis output schemas**, not operation-family patterns. The `logic_gap` schema has `gap_type`, `premise`, `conclusion`, `missing_link`, `benanav_attack`, `suggested_fix`. These are properties of analysis findings — not follow-up operations a user performs on them.

The inventory should classify analyzer-mgmt evidence honestly:

- **Runtime evidence**: None. The rhetoric scripts are seeding/schema tools, not runtime interaction flows.
- **Product intent evidence**: The schemas show structured analysis outputs that are rich enough to support per-item follow-up operations. The `populate_rhetoric_schemas.py` `benanav_attack` field is an analysis output property, not a user action.
- **Schema inconsistency**: The prompt in `seed_rhetoric.py` asks for `gap_type=non_sequitur/missing_premise/inferential_leap/overgeneralization/false_dichotomy`, while `populate_rhetoric_schemas.py` expects `gap_type=non_sequitur/hidden_premise/false_dichotomy/hasty_generalization/circular_reasoning/equivocation`. This inconsistency is itself evidence that these are evolving product-intent artifacts, not settled contracts.

The memo should explicitly classify analyzer-mgmt as "secondary product-intent evidence, not runtime evidence."

### D. The "candidate affordance vocabulary" deliverable needs tighter constraint

The memo says the inventory should produce "a first candidate set of analyzer-owned semantic affordances and routing hints." But without extraction completing first, the inventory cannot know where in the analyzer-v2 response shape those affordances would attach.

The deliverable should be constrained to:

- what operations exist (from code)
- what output properties enable them (from code)
- hypotheses about what analyzer-side annotations would make those operations possible without host-side reconstruction

It should NOT attempt to define the affordance vocabulary itself, the attachment-point shape, or the serialization format. That requires knowing the post-extraction metadata shape.

---

## 4. Code-Backed Findings

### 4.1 The downstream operation surface is richer than the memo expects

Based on direct code inspection of the-critic, here is the actual operation surface the inventory should capture:

**Runtime-real operations (live code, API-backed):**

| Operation | Trigger Surface | Required Output Properties | Destination | Generic vs Specific |
|-----------|----------------|---------------------------|-------------|-------------------|
| Capture | CaptureActionBar button on any rendered section/item | `source_type`, `source_view_key`, `source_renderer_type`, `content_type`, `depth_level` | Intermediate (capture record) | Generic |
| Arsenal routing | "Send to Arsenal" in CaptureActionBar | Capture record ID + optional user annotation | Arsenal database | Generic routing |
| Arsenal toggle | Star button on finding card (FindingsPage) | `finding_id` (integer) | Arsenal database | Generic (applies to all finding types) |
| Research question routing | "Research Question" in CaptureActionBar | Capture selection + formulated question | Research todo database | Generic routing |
| AI-suggested question | "Generate AI Suggestion" in ResearchFlagDialog | `selected_text`, `context_title`, `source_view_key`, `structured_data`, `depth_level`, `parent_context` | Populates form fields | Output-specific (needs semantic context) |
| Research queue | "Save & Queue" in ResearchFlagDialog | Research todo with `status='queued'` | Backend auto-enqueues for NotebookLM | Routing contract |
| NotebookLM lookup | Backend auto-processing of queued items | Research todo `question`, project's primary corpus | NotebookLM API → `answer_text`, `answer_sources` | External routing |
| Comment creation | Text selection on finding fields | `findingId`, `selectedText`, `textField` | Comments array (persisted via annotations API) | Generic |
| Add to outline | "Add to Outline" in CommentModal | `section_id`, `text`, `source_type='comment'` | Outline talking points via `POST /api/outline/talking-points` | Routing contract |
| Talking point upgrade | "Upgrade" in OutlinePanel | `tpId` | Regenerated with full context | Output-specific |
| Q&A (Ask AI) | QA interface in FindingsPage | `question`, finding context | QA history (persisted via annotations API) | Output-specific |
| Export findings | Export button in FindingsPage | All filtered findings | JSON/clipboard | Generic |

**Latent/stub operations (code exists but not wired):**

| Operation | Evidence | Status |
|-----------|----------|--------|
| Research answer → Arsenal routing | `ResearchComments.tsx` has `onSendToArsenal` callback prop (not connected) | Stub |
| Research answer → Research routing | `ResearchComments.tsx` has `onSendToResearch` callback prop (not connected) | Stub |

**Aspirational operations (from dictation only, no code):**

| Operation | Source |
|-----------|--------|
| Route to Book Modeler | Dictation |
| Mobilize further thinkers/reading | Dictation |
| Extract from Arsenal to writing | Dictation |
| Feed back from Arsenal to Book Modeler | Dictation |

### 4.2 The CaptureSelection schema reveals the actual semantic preconditions

`CaptureContext.tsx:17-35` defines `CaptureSelection` with:

```typescript
source_type: 'genealogy' | 'research' | 'analysis'  // discriminator
source_view_key: string
source_section_key?: string
source_renderer_type: string
content_type: 'section' | 'card' | 'item'
depth_level: 'L1_section' | 'L2_element'
parent_context?: { section_key, section_title }
entity_id?: string
```

These fields are the current semantic preconditions for capture. They map directly to the "required output structure or semantic precondition" column the inventory proposes. Notably, the capture system already knows about `source_renderer_type` and `depth_level` — these are proto-affordances that the host currently reconstructs from its own knowledge of the rendered surface.

An honest inventory row for "Capture" would note that analyzer-v2 could potentially supply `capturable: true`, `depth_levels: [L1, L2]`, and `content_types: [section, card, item]` as semantic annotations on views. The host currently derives these from its own renderer knowledge.

### 4.3 The research question formulation flow is the most complex routing pattern

`ResearchFlagDialog.tsx` implements a multi-step flow:

1. User selects text in a rendered analytical surface
2. Dialog shows the capture context (source view, section, text)
3. "Generate AI Suggestion" calls `POST /api/research-todos/suggest-question` with structured data
4. User edits: question, context, scope_hints (books/secondary_lit/empirical), research_type, priority, tags
5. "Save & Queue" creates the capture record, creates the research todo with `status='queued'`
6. Backend auto-enqueues for NotebookLM lookup

This is the strongest evidence that follow-up operations can be output-specific: the AI suggestion endpoint needs `structured_data` and `depth_level` to generate a good question. A generic capture with no semantic context would produce worse suggestions. This is where analyzer-side semantic affordances would add the most value — by annotating which engine outputs support "generate research question from selection."

### 4.4 The compose_from_intent.py hard-coded maps are exactly what extraction targets

The memo proposes auditing "src/presenter/compose_from_intent.py" as a future attachment point. But the extraction tranche is about to restructure exactly these seams:

- `_ROLE_FROM_ENGINE_KEY` (8 entries, lines 110-118) → extraction target
- `_LEAF_PATTERN_BY_ROLE` (5 entries, lines 82-88) → extraction target
- `_PRESENTATION_STANCE_BY_ROLE` (5 entries, lines 89-95) → extraction target

Documenting these as "future attachment points" while the extraction tranche is actively externalizing them creates a stale-on-arrival inventory. The inventory should note their existence in passing but should not treat them as attachment points until extraction has reshaped them.

### 4.5 manifest_builder.py and presentation_bridge.py are structurally mature

`adapt_renderer_for_consumer()` in manifest_builder.py already resolves consumer capabilities from ConsumerRegistry and reports adaptations. The presentation_bridge.py pipeline already distinguishes curated template vs dynamic extraction, with cache-first processing and async/sync variants. These are working seams, not deficiencies. The inventory should not treat them as attachment points that need widening — they are the substrate that a later affordance-annotation layer would extend.

---

## 5. Strategic Implications For The Roadmap

### 5.1 The inventory confirms that downstream operations are real and diverse

The code audit shows at least 12 runtime-real operations, 2 latent stubs, and 3+ aspirational directions from the dictation. This is not a thin surface. A Close Read V1 memo written without this inventory would miss the AI-suggested research question flow, the dual-destination comment→outline flow, and the research status lifecycle — all of which matter for defining what the app actually does.

### 5.2 The ownership boundary question can now be partially answered from code

Based on the code evidence:

- **Generic operations** (capture, comment, export, arsenal toggle) depend only on rendered surface structure (section/card/item) and finding IDs. These need minimal analyzer-side annotation — mainly `capturable` flags and depth-level declarations.
- **Output-specific operations** (AI-suggested question, talking point upgrade, Q&A) depend on semantic context from the analysis output. These are where analyzer-side affordance annotations would add the most value. The research question suggestion endpoint explicitly needs `structured_data` and `depth_level`.
- **Routing contracts** (Arsenal, Research, Outline, NotebookLM) are destination-infrastructure that should remain host-owned. Analyzer-v2 should not own the Arsenal or Outline services.

So the ownership split is:

- analyzer-v2 should own: semantic affordance annotations on views/sections (capturable, scrutinizable, question-generatable, routable-to-research)
- hosts should own: the actual routing infrastructure, destination services, UX for choosing destinations
- nobody yet owns: the vocabulary that connects the two

### 5.3 The inventory should inform but not constrain the extraction tranche

The extraction tranche is behavior-preserving and analyzer-internal. The inventory tranche is product-side discovery. They should not create dependencies on each other. The memo correctly says they are parallel tracks, but it weakens that principle by including analyzer-v2 seam assessment in the inventory scope.

---

## 6. Concrete Corrections And Reframing

### Correction 1: Remove analyzer-v2 seam audit from this tranche

Remove "In Scope §3" entirely. Replace with one sentence: "Analyzer-v2 attachment-point assessment will be produced as a short addendum after the Phase E composition metadata extraction tranche completes."

This makes the inventory purely product-side discovery, as the memo's own framing claims. It eliminates the risk of documenting seams that extraction is about to restructure.

### Correction 2: Expand the the-critic source file list

The "Proposed Sources" section should list:

**Primary runtime evidence:**
- `CaptureContext.tsx` — capture state, destinations, source discriminator
- `CaptureActionBar.tsx` — the capture-to-destination routing UI
- `ResearchFlagDialog.tsx` — AI-suggested question, scope hints, queue routing
- `FindingsPage.tsx` — arsenal toggle, comments, Q&A, outline routing, finding card interactions
- `ArsenalPage.tsx` — arsenal display, removal, stream-typed grouping
- `useResearchTodos.ts` — research lifecycle: queue polling, NotebookLM lookup, source refresh
- `researchConstants.ts` — research status machine, NotebookLM answer source schema
- `OutlinePanel.tsx` / `OutlineEditorPanel.tsx` — talking point generation, hierarchy, source linking
- `CommentModal.tsx` — dual-destination flow: comment + outline routing

**Latent-intent evidence:**
- `ResearchComments.tsx` — stub `onSendToArsenal` / `onSendToResearch` callbacks

### Correction 3: Downgrade analyzer-mgmt to explicitly secondary evidence

Replace "In Scope §2" header with: "Audit the current logic/rhetoric structures in analyzer-mgmt as secondary product-intent evidence."

Add a note: "These are seeding scripts and output schemas, not runtime interaction flows. The inventory should classify them as product-intent evidence, not runtime evidence."

### Correction 4: Constrain the affordance-vocabulary deliverable

Replace "a first candidate set of analyzer-owned semantic affordances and routing hints" with:

"For each operation, hypothesize what analyzer-side annotations would enable thin hosts to operationalize the pattern without reconstructing analysis meaning. Do not attempt to define the affordance schema shape, attachment-point format, or serialization contract — those depend on the post-extraction metadata shape."

### Correction 5: Add "current source of truth" column to the inventory matrix

The proposed matrix columns should include:

- **current source of truth**: Where does the logic that enables this operation currently live? Options: host code (file path), analyzer-v2 response metadata (field name), nowhere yet.

This makes the ownership-boundary question concrete and auditable rather than speculative.

### Correction 6: Clarify that the analyzer-mgmt schema inconsistency is itself a finding

The inventory should note that `seed_rhetoric.py` and `populate_rhetoric_schemas.py` use different enum values for the same `gap_type` field. This is evidence that the rhetoric output schemas are still evolving product-intent, not settled contracts. The inventory should classify this as a datum, not ignore it.

---

## Summary Table

| Aspect | Memo's Claim | Critique Finding |
|--------|-------------|-----------------|
| Is this the right companion tranche? | Yes | Yes, with scope narrowing |
| Smallest honest tranche? | Claims yes | No — remove analyzer-v2 seam audit (area 3) |
| Sequencing | Extraction + inventory parallel, then Close Read V1 | Correct and disciplined |
| the-critic source list | 2 files | At least 10 files needed for honest inventory |
| analyzer-mgmt evidence status | "output richness" | Secondary product-intent, not runtime evidence |
| analyzer-v2 seam audit | In scope | Should be deferred to post-extraction addendum |
| Affordance vocabulary deliverable | "first candidate set" | Should be constrained to hypotheses, not vocabulary definition |
| Generic/specific/routing distinction | Proposed in acceptance bar | Correct and code-confirmed |
| Runtime/latent/aspirational distinction | Proposed in acceptance bar | Correct and code-confirmed |
| Inventory matrix schema | 9 columns | Good, but add "current source of truth" column |

---

## Is There A Smaller Or Stronger Tranche?

**Smaller alternative considered**: Audit only the-critic runtime (skip analyzer-mgmt entirely). This would miss the rhetoric schema evidence, which is genuinely useful as product-intent context for understanding what kinds of structured outputs future engines will produce.

**Recommendation**: The right size is areas 1 (expanded the-critic audit) and 2 (analyzer-mgmt as explicitly secondary/product-intent), with area 3 deferred to a post-extraction addendum. This is slightly smaller than the memo proposes but captures the same evidence base.

That is the smallest tranche that honestly answers all four of the memo's stated questions.

---

## End

The memo is the right tranche at the right time. The corrections above make it tighter, more honest about its source coverage, and better aligned with the parallel extraction tranche by removing the scope overlap on analyzer-v2 seams. The expanded the-critic file list is the most important correction — an inventory that reads only two files from a codebase with 10+ materially relevant files would undercount the actual operation surface by roughly half.
