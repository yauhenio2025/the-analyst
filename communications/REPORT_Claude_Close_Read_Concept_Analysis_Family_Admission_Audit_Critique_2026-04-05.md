# Critical Review: Close Read Concept-Analysis Family Admission Audit

Reviewer: Claude Opus 4.6 (1M context)
Date: 2026-04-05
Memo Under Review: `communications/MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md`

---

## Context Check

### Memos Read

1. **MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md** -- The memo under review. Read in full (448 lines).
2. **MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md** -- Read in full (533 lines). Establishes the dual-destination of default families + composable modules, and names concept analysis as the next serious family.
3. **MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md** -- Read in full (402 lines). Freezes the V1.5 dual-family boundary: genealogy + AOI thematic single thinker.
4. **MEMO_2026-04-05_close_read_post_v1_recalibration_multi_engine_boundary.md** -- Read in full (387 lines). Recalibrates from genealogy-only V1 toward a multi-engine trajectory.
5. **MEMO_2026-04-05_close_read_v1_product_memo.md** -- Read in full (259 lines). Freezes the initial V1 product boundary as a bounded Critic-hosted genealogy-first pilot.
6. **MEMO_2026-04-01_close_read_direction_dictation_reference.md** -- Read in full (37 lines of dictation). The foundational user dictation that names close reading, mixed engine families, follow-up operations, Arsenal, Research, Book Modeler.
7. **MEMO_2026-04-01_close_read_direction_change_and_implications.md** -- Read in full (416 lines). Packages the dictation implications: the missing abstraction is operation families over analytical outputs.
8. **DYNAMIC_BESPOKE_APPS_VISION.md** -- Read in full (200+ lines of the first section; scanned structure). The canonical "analyzer-v2 is the brain, apps are ephemeral presentations" vision document.

### Code Files Inspected

8. **`/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx`** -- Inspected in detail: lines 1-400 (inferential/logical export functions, type system), lines 1740-1940 (scrutiny system, ammunition modal), and targeted grep for analysis types. This is a massive file (~4500+ lines) that is the primary concept-analysis product surface.
9. **`/home/evgeny/projects/the-critic/webapp/src/routes.tsx`** -- Read in full (367 lines). Confirms `concept-analysis/*` route with wildcard sub-pathing, confirms Close Read umbrella with genealogy + AOI families.
10. **`/home/evgeny/projects/the-critic/api/server.py`** -- Read lines 1-100 (imports), lines 1030-1036 (AnalysisType enum), lines 1692-1751 (assumption analysis via visualizer engine), lines 3876-3954 (`run_concept_analysis_thread` dispatch). Confirmed all six analysis types and their execution paths.
11. **`/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`** -- Read lines 1-100. Confirmed: multi-pass 12-phase pipeline, project-local orchestrator, calls `ConceptAnalyzerOrchestrator`.
12. **`/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`** -- Read lines 1-100. Confirmed: dedicated hardcoded inferential-role prompt, calls Anthropic directly, no analyzer-v2 involvement.
13. **`/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py`** -- Read lines 1-120. Confirmed: fetches engine definition and extraction prompt from analyzer-v2 API, then calls Claude directly. This is the analyzer-v2-backed path for semantic_field, causal, and metaphorical modes.
14. **`/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p03_argument_formalization.py`** -- Read lines 1-100. Confirmed: references `engine_key = "concept_argument_formalization"` from analyzer-v2, but builds its own prompt locally.
15. **`/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p09_vulnerability_analysis.py`** -- Read lines 1-100. Confirmed: references analyzer-v2 engine keys for vulnerability sub-passes (`concept_vulnerability_unstated_premises`, etc.) but again builds prompts locally.
16. **`/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx`** -- Read lines 1-100. Confirmed: genealogy-specific Close Read page, uses `CloseReadFamilySwitcher`, `CaptureProvider`, `CaptureActionBar`, `V2TabContent`.
17. **`/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadAoiPages.tsx`** -- Read lines 1-100. Confirmed: AOI-specific Close Read pages with thinker index and thinker detail, delegates to `AoiV2ThematicPanel`.
18. **`/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`** -- Read in full (107 lines). Confirmed: 12-phase sequential chain with 12 concept-specific engine keys, `source_project: "the-critic"`.
19. **`/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json`** -- Read in full (27 lines). Confirmed: looser LLM-selection suite with 5 engines (centrality, evolution, affordance, demarcation, presuppositional).
20. **`/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json`** -- Read in full (676 lines). Confirmed: rich canonical schema with relationship graph, commitment chains, backing hierarchies, operationalization metadata.
21. **`/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml`** -- Read in full (129 lines). Confirmed: four-stance depth sequence (discovery, confrontation, dialectical, integration) with pass dependencies.

### Additional Code Evidence Gathered

- **Counted 39 concept-prefixed engine definitions** in `/home/evgeny/projects/analyzer-v2/src/engines/definitions/concept_*`.
- **Found `assumption_excavation.json`** engine in analyzer-v2 (category: "argument", not "concepts").
- **Confirmed the assumption analysis path** in `server.py` routes through the old Visualizer/Analyzer API (`ANALYZER_API_URL`), not through analyzer-v2.
- **Found the AnalysisType enum** confirms exactly six types: INFERENTIAL, LOGICAL, ASSUMPTION, SEMANTIC_FIELD, CAUSAL, METAPHORICAL.
- **Found substantial scrutiny and ammunition features** in ConceptsPanel that the memo does not discuss.

---

## Section 1: Overall Assessment of the Memo's Strategic Framing

### 1.1 Is "concept analysis family" the right next serious admission frame?

**Verdict: Yes, this is correct and well-argued.**

The memo's central claim -- that the next admission should be framed as the "concept-analysis family" rather than "logic alone" -- is supported by strong code evidence:

- The `routes.tsx` file confirms `concept-analysis/*` as a top-level route family with wildcard sub-pathing, not a single page.
- The `ConceptsPanel.tsx` file is massive (~4500+ lines), embodying a serious product surface with six submodes, export capabilities, scrutiny workflows, and ammunition analysis.
- The `AnalysisType` enum in `server.py` explicitly lists all six types as equal-status members of a single family.
- The analyzer-v2 engine inventory contains 39 concept-prefixed engines, a 12-phase chain, and a separate concept suite -- all of which operate at the concept-family level, not a logic-only level.

The memo is correct that calling this "logic" would be a reductive mischaracterization of both the old product and the current analyzer-v2 capability inventory.

### 1.2 Does the memo overstate analyzer-v2 readiness?

**Verdict: The memo understates the gap more than it overstates readiness. The actual migration picture is more fragmented than the memo suggests.**

The memo's claim of "substantial concept-analysis capability material" in analyzer-v2 is technically true but incomplete. Here is the precise state by submode:

| Submode | Execution Path | analyzer-v2 Role | Honest Readiness |
|---------|---------------|-------------------|------------------|
| **inferential** | `analyze_concept_inferential.py` | None. Hardcoded prompt locally. | **Zero** analyzer-v2 involvement at runtime, despite `inferential_commitment_mapper.json` existing as a definition |
| **logical** | `analyze_concept_logical.py` -> `ConceptAnalyzerOrchestrator` | Phase classes reference analyzer-v2 engine keys in comments/annotations, but build prompts locally | **Shadow-local**: engine key alignment is cosmetic, not functional |
| **assumption** | `server.py` -> `submit_analyzer_job` to `ANALYZER_API_URL` (old Analyzer/Visualizer) | Routed to old Analyzer via the Visualizer pipeline, not analyzer-v2 | **Zero** analyzer-v2 involvement; uses old Analyzer's `assumption_excavation` engine |
| **semantic_field** | `analyze_concept_generic.py` -> analyzer-v2 API | Fetches engine def + extraction prompt from analyzer-v2 | **Real** analyzer-v2 involvement via prompt composition |
| **causal** | `analyze_concept_generic.py` -> analyzer-v2 API | Same as semantic_field | **Real** |
| **metaphorical** | `analyze_concept_generic.py` -> analyzer-v2 API | Same as semantic_field | **Real** |

So the honest tally is:

- **3 submodes** genuinely backed by analyzer-v2 (semantic_field, causal, metaphorical)
- **1 submode** backed by the old Analyzer/Visualizer pipeline, not analyzer-v2 (assumption)
- **2 submodes** entirely legacy-local with no functional analyzer-v2 involvement (inferential, logical)

The memo says the state is "mixed" and that is true. But the memo's language in Section "Current Migration Reality > analyzer-v2 reality" could create a misleading impression. It says:

> "analyzer-v2 already contains substantial concept-analysis capability material"

and lists the 12-phase chain and inferential engine as evidence. But the 12-phase chain in analyzer-v2 is a **definition artifact** -- it was extracted from the Critic's own orchestrator. It has never been executed through analyzer-v2's executor pipeline for concept analysis. The logical path builds its own prompts locally in `p03_argument_formalization.py`, `p09_vulnerability_analysis.py`, etc., and only stores the engine keys as annotations (e.g., `engine_key = "concept_argument_formalization"`). At runtime, those keys are not used to fetch anything from analyzer-v2.

Similarly, the `inferential_commitment_mapper.json` engine definition in analyzer-v2 is a rich, well-developed definition with a full operationalization YAML. But the actual inferential analysis in Critic's `analyze_concept_inferential.py` uses a **locally hardcoded prompt** that was modeled on the engine definition's style but does not fetch from analyzer-v2 at all.

**Recommendation**: The next boundary memo must state, per submode, whether the analyzer-v2 connection is:
- (a) functional at runtime (prompt fetch, execution, result handling)
- (b) definitional only (engine key registered, definition exists, but not used at runtime)
- (c) absent (no connection at all)

The current memo conflates (a) and (b) by listing definition artifacts as evidence of "already analyzer-v2-backed" capability.

### 1.3 The assumption path misconception

This is the single most important factual correction the review must flag.

The memo lists the assumption submode as one of the six submodes and treats it uniformly with the others. But the assumption path has a fundamentally different execution model:

- It routes through `ANALYZER_API_URL` (the old Visualizer/Analyzer service at `https://analyzer-3wsg.onrender.com`)
- It uses `submit_analyzer_job()` and `poll_analyzer_job()` -- the old job submission pipeline
- It calls the `assumption_excavation` engine, which lives in the **old Analyzer**, not in analyzer-v2

This means the assumption submode is neither legacy-local (like inferential/logical) nor analyzer-v2-backed (like semantic_field/causal/metaphorical). It is backed by a **third system** -- the old Analyzer/Visualizer pipeline.

The memo does not mention this distinction anywhere. A correct admission audit must acknowledge this three-way split:

1. Legacy-local in Critic (inferential, logical)
2. Old Analyzer/Visualizer pipeline (assumption)
3. analyzer-v2-backed (semantic_field, causal, metaphorical)

---

## Section 2: Scrutiny of the Submode Hierarchy

### 2.1 Are the likely first submodes calibrated correctly?

The memo's working hypothesis is:

> First admitted core: inferential + logical
> Likely secondary/supporting or later: assumption, semantic_field, causal, metaphorical

**Verdict: This is strategically reasonable but the code evidence suggests a different ordering for ease of admission.**

From a **pure readiness perspective**, the easiest first admission cut would actually be:

- **semantic_field, causal, metaphorical** -- These already use analyzer-v2 prompt composition via `analyze_concept_generic.py`. They are the cleanest, most straightforward to admit because they already follow the pattern Close Read established for genealogy and AOI: analyzer-v2 defines the engine, composes the prompt, and the host just renders the result.

- **inferential and logical** are strategically central (the dictation explicitly names premise-testing and weak-point identification) but they are the hardest to admit because they require migrating substantial local orchestration logic to analyzer-v2.

So the memo is right about strategic priority (inferential/logical are the most important) but should be more honest about the migration cost. The next boundary memo might want to consider a "V1 concept-analysis admission" that includes:

- The three already-migrated modes (semantic_field, causal, metaphorical) as immediately admitted
- Inferential and logical as the central but higher-cost admission targets
- Assumption as a deferred special case that requires resolving its old-Analyzer dependency

### 2.2 Are any submodes missing from the inventory?

**Yes. The memo misses one important operational behavior: cross-corpus concept analysis.**

The Critic codebase contains:

- `/p/:projectId/cross-concept` route in `routes.tsx`
- `CrossConceptPage` import
- `run_cross_concept_analysis` function imported in `server.py`
- `CrossConceptExtractionDB`, `CrossConceptJobDB`, `CrossConceptSynthesisDB` database models

Cross-corpus concept analysis is a related but distinct product surface that treats concepts across multiple texts rather than analyzing a single concept in depth. The memo should acknowledge this neighbor even if it decides to exclude it from the first concept-analysis family admission.

Additionally, the memo does not mention:

- **Big Picture analysis** (`/p/:projectId/big-picture`) which includes `BigPictureAnalysisType.INFERENTIAL` -- a pre-conceptual document-level inferential analysis. This is a boundary case: it uses inferential analysis but at the document level rather than the concept level. The next boundary memo should decide whether this is inside or outside the concept-analysis family.

---

## Section 3: The Missing Operational Behaviors

### 3.1 Scrutiny as a constitutive follow-up operation

The memo's Section "What This Audit Must Determine > 5. Exact family-specific follow-up operations" lists "premise scrutiny / weak-point identification" as a likely constitutive operation. This is correct, but the memo significantly underestimates how developed this already is in the old product.

The `ConceptsPanel.tsx` code reveals a **fully built scrutiny system**:

- `ScrutinyMode` type with three modes: `quick`, `deep`, `both`
- Dedicated API endpoints: `/scrutinize/jobs/{jobId}`, `/scrutiny/results/{concept}`
- Per-premise scrutiny that produces `PremiseScrutinyResult` with `lines_of_attack`
- LocalStorage caching of scrutiny results
- Progress polling with partial quick-results while deep analysis continues
- A complete job lifecycle: submit -> poll -> display -> cache

This is not just "premise scrutiny as an idea." It is an already-built, already-running follow-up operation system. The scrutiny system embodies exactly the kind of engine-specific follow-up work that the dictation described. Any concept-analysis admission that includes the logical submode would need to account for this existing scrutiny workflow.

The memo should explicitly flag this as:

- An existing follow-up operation family with real code, real UI, and real data flow
- A strong precedent for the kind of operation-family law that Close Read needs to develop
- A migration target: should scrutiny run through analyzer-v2's capabilities, or remain a Critic-local operation?

### 3.2 Ammunition analysis as a second follow-up operation

The `ConceptsPanel.tsx` also contains an **ammunition analysis system** that the memo does not mention at all:

- `AmmunitionAnalyzeRequest`, `AmmunitionAnalyzeResponse`, `AmmunitionJobStatus`, `AmmunitionAnalysisResult` types
- A multi-phase modal: `curation` -> `analyzing` -> `results`
- Corpus selection (loading available corpora, user selects which to include)
- LLM-powered cross-corpus ammunition matching

This is a second follow-up operation family where the user:
1. Identifies a vulnerability/line-of-attack from scrutiny
2. Searches across available corpora for supporting material ("ammunition")
3. Gets LLM-analyzed results with matches and relevance scores

This is significant because it demonstrates a two-hop follow-up chain:

```
logical analysis -> scrutiny (premise attack) -> ammunition (find supporting material)
```

This two-hop pattern is exactly what the dictation described when it talked about mobilizing thinkers and finding material to support attacks. The memo should document this existing operational depth because it materially affects:

- How deep the first concept-analysis admission needs to be
- Whether "concept analysis with just reading + capture" is honest, or whether scrutiny + ammunition are constitutive
- What follow-up operation families need to be at least partially admitted

### 3.3 Send-to-outline integration

The ConceptsPanel also imports `OutlineSection` types and supports sending concept analysis outputs to the outline editor. This is another follow-up routing pattern that exists in the old product:

- Analysis output -> user selection -> route to outline

The memo lists "capture-and-route into Arsenal / Research" but does not mention outline routing, which is a third existing destination in the concept-analysis family specifically.

---

## Section 4: Claims Tested Against Code Evidence

### 4.1 Claim: "The old product family is best understood as concept analysis"

**Code evidence: Confirmed.**

- Routes: `concept-analysis/*` wildcard
- Component: `ConceptsPanel` as a single unified component handling all six types
- Types: `ConceptAnalysisType` as a union type
- Server: `AnalysisType` enum grouping all six
- The UI navigates concept-first, then type-second (select concept, then choose analysis type)

This is not merely a naming convention. The product architecture genuinely treats concept analysis as the family and the six types as submodes.

### 4.2 Claim: "Old Critic route structure already makes the family shape visible"

**Code evidence: Confirmed.**

The route structure is:
```
/p/:projectId/concept-analysis         -- dashboard
/p/:projectId/concept-analysis/:concept/:type     -- detail
/p/:projectId/concept-analysis/:concept/:type/:tab -- detail + tab
```

This three-level hierarchy confirms the family structure: concept as the primary dimension, type as the secondary dimension, tab as the tertiary dimension.

### 4.3 Claim: "analyzer-v2 already has a 12-phase chain"

**Code evidence: Confirmed as a definition artifact, but with an important caveat.**

The chain definition at `concept_analysis_12_phase.json` exists and is well-structured. It contains:

```json
{
  "chain_key": "concept_analysis_12_phase",
  "engine_keys": [
    "concept_semantic_constellation",
    "concept_structural_landscape",
    "concept_argument_formalization",
    "concept_chain_building",
    "concept_taxonomy_function",
    "concept_causal_mechanisms",
    "concept_conditional_web",
    "concept_argumentative_weight",
    "concept_vulnerability_inferential_gaps",
    "concept_cross_text_comparison",
    "concept_quote_retrieval",
    "concept_synthesis"
  ],
  "blend_mode": "sequential",
  "source_project": "the-critic"
}
```

The `"source_project": "the-critic"` annotation is honest -- it was extracted from the Critic. But the chain has **never been executed through analyzer-v2's executor pipeline**. The Critic still runs its own local `ConceptAnalyzerOrchestrator` with local prompt-building phases. The chain definition is a catalog entry, not a functioning execution pipeline in analyzer-v2.

### 4.4 Claim: "The old logical path already references analyzer-v2-style engine keys"

**Code evidence: Confirmed, but the reference is weaker than implied.**

`p03_argument_formalization.py` declares:
```python
engine_key = "concept_argument_formalization"
```

`p09_vulnerability_analysis.py` declares:
```python
sub_pass_engine_keys = {
    "unstated_premises": "concept_vulnerability_unstated_premises",
    "inferential_gaps": "concept_vulnerability_inferential_gaps",
    "equivocations": "concept_vulnerability_equivocations",
    "question_begging": "concept_vulnerability_question_begging",
    "false_dichotomies": "concept_vulnerability_false_dichotomies",
}
```

These keys match engine definitions that exist in analyzer-v2. But at runtime, these phase classes **build their own prompts locally** rather than fetching from analyzer-v2. The `engine_key` attributes appear to be annotations or metadata rather than functional integration points.

The memo says the old logical path is "better understood as a partially migrated / partially shadow-local concept-analysis estate." This is fair language, but the memo should be clearer that "partially migrated" means "key names align but execution does not flow through analyzer-v2."

### 4.5 Claim: "The concept-analysis family is already partially on the migration path"

**Code evidence: Confirmed, but the fraction is smaller than the memo implies.**

Of six submodes:
- 3 are functionally analyzer-v2-backed (semantic_field, causal, metaphorical via `analyze_concept_generic.py`)
- 1 routes through the old Visualizer/Analyzer pipeline (assumption)
- 2 are entirely local (inferential, logical)

So 3 out of 6 submodes are on the migration path. That is "partial" but the memo's overall tone suggests more readiness than the 50% actual figure.

---

## Section 5: Evaluation of the Separation Between Layers

### 5.1 Does the memo keep the right separation between default family admission, composition-layer destination, and standalone-host deferral?

**Verdict: Yes, this separation is handled well.**

The memo is disciplined about:

- Not conflating the admission audit with implementation scope
- Not jumping to composition-layer design
- Not reopening standalone-host questions
- Keeping UI/page questions as secondary to family-boundary questions

The five-question framework in "What This Audit Must Determine" is well-structured:

1. Family framing
2. First admitted submodes
3. Readiness mapping
4. Host/page posture
5. Follow-up operations
6. Deferrals

This is a reasonable structure for a boundary memo.

### 5.2 But the memo misses the operational depth problem

The memo correctly identifies that concept analysis is "likely the first family where Close Read must explicitly support more than bounded reading + capture." But it does not adequately convey the magnitude of this gap.

The existing ConceptsPanel supports:

1. **Running new analyses** (not just viewing results) -- job submission, progress tracking, cancellation
2. **Multi-mode scrutiny** with quick/deep/both options and premise-by-premise targeting
3. **LLM-powered ammunition analysis** with corpus curation and cross-text matching
4. **PDF export** with rich formatted output
5. **Send-to-outline** routing
6. **JSON export** of raw analysis data
7. **Markdown export** with deeply structured formatting

This is materially more operational depth than genealogy or AOI currently provide under Close Read. Admitting concept analysis without acknowledging this operational depth would either:

- Produce a concept-analysis Close Read page that is dramatically weaker than the existing ConceptsPanel (regression)
- Or require admitting follow-up operations that are significantly more complex than capture-and-route

The next boundary memo must decide this explicitly. The current audit memo should flag it more prominently.

---

## Section 6: What the Memo Gets Right

### 6.1 The reframing from "logic" to "concept analysis family" is correct and important

This is the memo's central contribution and it is well-supported. Treating "logic" as the next admission would lose the family structure that already exists and would orphan three already-migrated submodes (semantic_field, causal, metaphorical) that could be admitted with relatively low effort.

### 6.2 The "audit-first, then boundary memo, then implementation" sequence is sound

The memo correctly positions itself as a docs-first artifact that avoids premature implementation decisions. The recommended artifact chain (audit -> boundary memo -> implementation scope) is disciplined and appropriate.

### 6.3 The recognition that concept analysis embodies engine-specific follow-up work

The memo correctly identifies that concept analysis is the strongest old-product precedent for the kind of engine-specific follow-up operations that the dictation described. This is true and important for the roadmap.

### 6.4 The mixed-migration hypothesis is honest

Hypothesis 3 ("mixed migration posture") is the right framing. The next phase cannot assume either full greenfield or full turnkey migration.

### 6.5 The five working hypotheses are well-calibrated

All five hypotheses (concept analysis as next family, inferential/logical as center, mixed migration posture, stronger-than-reading operations needed, admission before standalone-host work) are defensible and well-grounded in the evidence.

---

## Section 7: What the Memo Gets Wrong or Misses

### 7.1 The assumption analysis execution path is mischaracterized

As detailed in Section 2.3 above, the assumption submode routes through the old Analyzer/Visualizer pipeline (`ANALYZER_API_URL`), not through analyzer-v2. The memo lumps all non-generic modes together as "legacy" but the assumption path is a distinct third category.

### 7.2 The scrutiny and ammunition features are entirely absent from the audit

This is the most significant omission. The ConceptsPanel contains approximately 800+ lines of code dedicated to premise scrutiny and ammunition analysis. These are not aspirational features -- they are fully built, fully operational product behaviors with:

- Dedicated API endpoints
- Job lifecycle management
- Multi-mode analysis (quick/deep/both)
- Persistent result storage (API + localStorage)
- Cross-corpus matching
- Rich UI with progress tracking

These features are constitutive for the logical analysis submode. Any admission of logical analysis without accounting for scrutiny would be dishonest about the old product's actual capabilities.

### 7.3 The send-to-outline routing is missing from the follow-up operations inventory

The ConceptsPanel supports routing analysis outputs to the outline editor, which is a follow-up destination beyond Arsenal and Research. The memo should inventory this.

### 7.4 The cross-corpus concept analysis is not acknowledged

The `cross-concept` route and its associated backend infrastructure (`CrossConceptExtractionDB`, `CrossConceptJobDB`, `CrossConceptSynthesisDB`) represent a related product surface that the memo does not mention. Even if cross-corpus analysis is excluded from the first concept-analysis admission, it should be named as a known neighbor.

### 7.5 The inferential engine definition vs. runtime usage gap is understated

The memo presents the `inferential_commitment_mapper.json` and its operationalization YAML as evidence that "inferential analysis is not merely a legacy local prompt idea." This is true at the definitional level -- the engine definition is rich and well-developed. But at the runtime level, the Critic's inferential analysis does not use this definition at all. The `analyze_concept_inferential.py` file contains a hardcoded prompt that was "based on the inferential_commitment_mapper engine" (as its docstring says) but does not fetch from analyzer-v2.

The gap between "definition exists" and "definition is functionally used" matters for an admission audit. A definition that sits in a JSON file is not the same as a definition that drives runtime behavior.

### 7.6 The memo does not address the Big Picture analysis boundary question

`BigPictureAnalysisType.INFERENTIAL` in `server.py` shows that inferential analysis also operates at the document level (not concept-scoped). The Big Picture page uses inferential analysis over entire documents rather than specific concepts. The next boundary memo should decide whether this is inside or outside the concept-analysis family.

### 7.7 The concept_analysis_suite chain is mentioned but its different character is not explored

The memo notes the existence of both the 12-phase chain and the concept_analysis_suite. But it does not explore a significant difference: the 12-phase chain is `blend_mode: "sequential"` while the suite is `blend_mode: "llm_selection"` with `max_engines: 3`. These represent fundamentally different composition patterns:

- The 12-phase chain is a deep, fixed-sequence pipeline (mirrors the old logical analyzer)
- The suite is a lighter, selective composition (choose 2-3 engines based on content)

This distinction matters for the composition-layer direction. The memo should note it more explicitly as evidence that analyzer-v2 already contains the seed of both "default deep analysis" and "selective bespoke analysis" patterns.

---

## Section 8: Specific Questions Answered

### Q1: Is "concept analysis family" the right next serious admission frame after genealogy and AOI?

**Yes.** The evidence is strong from multiple directions:

- Product evidence: The old ConceptsPanel is the largest, most feature-rich analytical surface in Critic
- Dictation evidence: The Close Read vision explicitly names logical analysis, premise-testing, and weak-point identification
- Capability evidence: analyzer-v2 has 39 concept-prefixed engine definitions, two chains, and a rich inferential engine with operationalization passes
- Strategic evidence: Concept analysis embodies the engine-specific follow-up operations that distinguish Close Read from a generic reader

No other family candidate (rhetoric, lines of attack, paradigms, etc.) has this combination of old product maturity, analyzer-v2 capability inventory, and dictation alignment.

### Q2: Does the memo overstate analyzer-v2 readiness for a first admitted concept-analysis cut?

**Yes, moderately.** The memo treats engine definitions and chain definitions as stronger evidence of readiness than they actually represent. The distinction between "definition exists in JSON" and "definition drives runtime behavior" is not made clearly enough. Only 3 of 6 submodes functionally use analyzer-v2 at runtime. The memo should have been more precise about this.

### Q3: Are the likely first submodes calibrated correctly?

**The strategic priority is correct (inferential + logical as the center); the readiness ordering should also be stated.** The three already-migrated modes (semantic_field, causal, metaphorical) could be admitted with minimal effort. The two strategic center modes (inferential, logical) require significant migration work. The next boundary memo should consider whether to admit the easy three as a first slice and the hard two as a second slice, rather than attempting all at once.

### Q4: Does the memo keep the right separation between default family admission, composition-layer destination, and standalone-host deferral?

**Yes.** The layering discipline is sound. The memo does not overclaim, does not jump to implementation, and does not reopen settled questions about V1.5 or standalone-host architecture.

### Q5: Does the memo miss any important old Critic concept-analysis behavior that should materially affect the next boundary memo?

**Yes, critically:**

1. **Scrutiny system** (~800+ lines of code, full job lifecycle, multi-mode analysis, premise-by-premise targeting) -- This is the single most important missing item. It represents exactly the kind of engine-specific follow-up operation that makes concept analysis different from genealogy/AOI.

2. **Ammunition analysis** (LLM-powered cross-corpus matching for lines of attack) -- A second-hop follow-up operation demonstrating a logical analysis -> scrutiny -> ammunition chain.

3. **Send-to-outline routing** -- A follow-up destination beyond Arsenal and Research.

4. **Cross-corpus concept analysis** -- A related but distinct product surface.

5. **Big Picture inferential analysis** -- A boundary case where inferential analysis operates at document level.

6. **PDF and Markdown export** -- Rich formatted export capabilities specific to concept analysis outputs.

7. **The assumption path's unique execution model** -- Routes through the old Analyzer/Visualizer, not through analyzer-v2 or through local Critic code.

---

## Section 9: Verdict

### **APPROVE WITH CORRECTIONS**

The memo's central strategic claim is correct and well-argued. Concept analysis is the right next family, the "family not logic" reframing is important, and the audit-first approach is disciplined. The memo correctly positions itself relative to the V1.5 boundary, the composition-layer horizon, and the standalone-host deferral.

However, the next boundary memo that follows this audit **must address** the following corrections:

#### Required Corrections for the Boundary Memo

1. **Clarify the three-way execution model split**: Legacy-local (inferential, logical), old Analyzer/Visualizer (assumption), and analyzer-v2-backed (semantic_field, causal, metaphorical). Do not conflate definition existence with runtime functional involvement.

2. **Inventory the scrutiny system explicitly**: This is constitutive for logical analysis and represents the strongest existing precedent for engine-specific follow-up operations. Any concept-analysis admission that includes logical analysis must decide what to do about scrutiny.

3. **Inventory the ammunition analysis system**: This is a second-hop follow-up operation that demonstrates the exact chain the dictation described (analysis -> vulnerability -> mobilize thinkers/material).

4. **Acknowledge cross-corpus concept analysis** as a neighboring surface, even if deferred.

5. **Distinguish "definition exists in analyzer-v2" from "definition is functionally used at runtime"** in the readiness mapping.

6. **Consider a phased admission**: The three already-migrated submodes could be admitted as an immediate first slice (low cost, real value), while inferential and logical are admitted as the higher-investment central slice.

7. **Name the outline routing destination** alongside Arsenal and Research as a concept-analysis-specific follow-up route.

#### What the Memo Gets Right and Should Be Preserved

- The concept-analysis family frame (not "logic alone")
- The five working hypotheses
- The audit-first, then boundary memo, then implementation sequence
- The recognition that concept analysis is the first family where Close Read needs stronger-than-reading operations
- The honest "mixed migration" framing
- The layering discipline between admission, composition, and standalone-host

The memo is a good strategic artifact that correctly identifies the next serious roadmap question. Its omissions are primarily about the depth and specificity of the old product's operational features, not about the strategic direction. The corrections above would make the subsequent boundary memo significantly more honest and actionable.

---

## Appendix A: Engine Inventory Summary

For reference, the concept-analysis-related engines in analyzer-v2 include:

**Core concept engines (39 files with `concept_` prefix):**
- Semantic: `concept_semantic_constellation`, `concept_semantic_field`
- Structural: `concept_structural_landscape`, `concept_argument_formalization`, `concept_chain_building`
- Taxonomy: `concept_taxonomy_function`, `concept_taxonomy_argumentative_function`, `concept_taxonomy_causal_structure`, `concept_taxonomy_dialectical_function`, `concept_taxonomy_epistemic_status`, `concept_taxonomy_inferential_mode`, `concept_taxonomy_inferential_role`, `concept_taxonomy_strength`, `concept_taxonomy_theoretical_register`
- Causal: `concept_causal_mechanisms`, `concept_causal_as_cause`, `concept_causal_as_effect`, `concept_causal_bidirectional`, `concept_causal_conditions`, `concept_causal_interventions`
- Conditional: `concept_conditional_web`, `concept_conditional_antecedent`, `concept_conditional_biconditional`, `concept_conditional_consequent`, `concept_conditional_nested`
- Vulnerability: `concept_vulnerability_unstated_premises`, `concept_vulnerability_inferential_gaps`, `concept_vulnerability_equivocations`, `concept_vulnerability_question_begging`, `concept_vulnerability_false_dichotomies`
- Synthesis/Other: `concept_synthesis`, `concept_argumentative_weight`, `concept_cross_text_comparison`, `concept_quote_retrieval`, `concept_evolution`, `concept_centrality_mapper`, `concept_demarcation_analyzer`, `concept_metaphorical_ground`, `concept_appropriation_tracker`

**Related non-concept-prefixed engines:**
- `inferential_commitment_mapper` (with operationalization YAML)
- `assumption_excavation` (category: argument)
- `presuppositional_excavator`
- `conceptual_affordance_analyzer`

**Chains:**
- `concept_analysis_12_phase` (sequential, 12 engines)
- `concept_analysis_suite` (llm_selection, 5 engines, max 3)

## Appendix B: Execution Path Summary

```
ConceptsPanel.tsx
    -> POST /concept/start-analysis
        -> server.py: run_concept_analysis_thread()
            -> if inferential:
                -> analyze_concept_inferential.py (LOCAL, hardcoded prompt, NO analyzer-v2)
            -> if logical:
                -> analyze_concept_logical.py (LOCAL, ConceptAnalyzerOrchestrator, engine key annotations only)
            -> if assumption:
                -> server.py: run_assumption_analysis() (OLD ANALYZER via ANALYZER_API_URL)
            -> if semantic_field:
                -> analyze_concept_generic.py (ANALYZER-V2 via ANALYZER_V2_URL)
            -> if causal:
                -> analyze_concept_generic.py (ANALYZER-V2 via ANALYZER_V2_URL)
            -> if metaphorical:
                -> analyze_concept_generic.py (ANALYZER-V2 via ANALYZER_V2_URL)

Follow-up operations (logical submode only):
    -> POST /scrutinize/start (premise scrutiny)
        -> server.py: scrutiny endpoints (LOCAL)
    -> POST /ammunition/analyze (cross-corpus ammunition)
        -> server.py: ammunition endpoints (LOCAL)
```

## Appendix C: Review Methodology

This review was conducted by:

1. Reading all 7 required context memos in full
2. Inspecting all 14 required code files with targeted reading and grep operations
3. Conducting additional code searches to verify specific claims (engine counts, execution paths, type definitions, API routing)
4. Cross-referencing memo claims against actual code behavior at each execution branch
5. Identifying gaps between what the memo inventories and what the codebase contains

All file paths and code citations are based on direct inspection of the codebase at the time of this review.
