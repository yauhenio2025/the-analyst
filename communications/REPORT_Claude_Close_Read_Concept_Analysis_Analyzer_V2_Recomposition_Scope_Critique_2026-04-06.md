# Review: Close Read Concept-Analysis analyzer-v2 Recomposition Scope

Date: 2026-04-06
Reviewer: Claude Opus 4.6
Memo Under Review: `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md`

## Context Check

Confirmed read of every required memo:

- `MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md` - the memo under review
- `MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md` - the immediate predecessor tranche
- `MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md` - the first concept family implementation cut
- `MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md` - the concept family boundary freeze
- `MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md` - the concept family admission audit
- `MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` - the broader Close Read roadmap
- `MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md` - V1.5 multi-engine boundary
- `MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md` - V1.5 coexistence implementation
- `MEMO_2026-04-01_close_read_direction_dictation_reference.md` - original user dictation
- `MEMO_2026-04-01_close_read_direction_change_and_implications.md` - direction change implications
- `DYNAMIC_BESPOKE_APPS_VISION.md` - the analyzer-v2-as-brain vision document

Confirmed code inspection of every required file:

- `/home/evgeny/projects/the-critic/api/server.py` (first 100 lines + import map)
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py` (full, 408 lines)
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py` (full, 555 lines)
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py` (full, 833 lines)
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/` (directory listing, 12 phase files)
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx` (first 100 lines)
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx` (first 100 lines)
- `/home/evgeny/projects/analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json` (full, 676 lines)
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml` (full, 129 lines)
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json` (full, 108 lines)
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_suite.json` (full, 27 lines)

---

## Verdict

**Approve with corrections.**

The memo is strategically sound, architecturally honest, and correctly framed as the next phase after fresh-project runtime enablement. Its central claim - that this should be recomposition/rebinding, not capability invention - is factually supported by the codebase. Its discipline in keeping the host contract frozen, separating the inferential and logical problems, and deferring composition-layer work is appropriate.

Three corrections are needed, all relating to where the memo understates the actual distance between analyzer-v2 outputs and current Critic host expectations:

1. The inferential schema distance is larger than the memo's language implies
2. The inferential execution model difference (single-pass vs. multi-stance operationalization) is not called out
3. The existing partial V2 prompt integration in `phase_base.py` should be acknowledged

None of these corrections change the strategic direction. They change the parity audit's expected findings and the likely size of the adapter work.

---

## Detailed Answers To Each Question

### 1. Is the memo right that the next move should be framed as recomposition/rebinding rather than capability invention?

**Yes. Strongly supported by code.**

The evidence is unambiguous:

- `inferential_commitment_mapper.json` is a 676-line engine definition with a full canonical schema containing 20+ structured sections, rich extraction steps, concretization guidance, visual grammar, and relationship graph specifications. This is not a stub or a placeholder - it is a complete, production-grade capability definition.

- `inferential_commitment_mapper.yaml` defines a 4-stance operationalization (discovery, confrontation, dialectical, integration) with 3 depth sequences (surface, standard, deep). This is materially richer than the Critic-local inferential prompt, which is effectively a single-pass call.

- `concept_analysis_12_phase.json` maps 12 phases to 12 named engine keys (`concept_semantic_constellation` through `concept_synthesis`), matching the Critic's `phases/p01_*.py` through `phases/p12_*.py` one-to-one.

- `concept_analysis_suite.json` provides a separate lighter chain (5 engines, LLM selection). This gives the system compositional flexibility the Critic-local code does not have.

The Critic-local code, meanwhile, is essentially a runtime wrapper around prompt logic that either duplicates or could be replaced by these definitions. The `phase_base.py` class even has built-in V2 prompt fetching infrastructure (`get_v2_prompt_template`, `build_prompt_from_v2`), proving that the migration direction was already anticipated in the code architecture.

Framing this as capability invention would misread the codebase.

### 2. Does the code actually support the claim that analyzer-v2 already has the decisive building blocks?

**Yes, with an important nuance the memo does not fully surface.**

The building blocks exist. But there is a significant structural difference between the analyzer-v2 inferential engine output schema and what the Critic inferential UI currently renders.

**What the Critic inferential UI renders** (from `analyze_concept_inferential.py` prompt and `InferentialDetail` in `ConceptsPanel.tsx`):

- `the_deceptively_simple`
- `commitment_cascade` (with `commitment_relations` and `hidden_commitments`)
- `incompatibility_map` (with `incompatibility_relations`)
- `tensions` (with `unresolved_tensions`)
- `practical_stakes`
- `commitment_packages`
- `synthesis`

**What the analyzer-v2 `inferential_commitment_mapper.json` canonical schema produces:**

- `key_ideas`
- `what_youre_signing_up_for`
- `what_backs_this_up`
- `either_or_choices`
- `real_world_implications`
- `how_the_conversation_shifts`
- `package_deals`
- `unresolved_tensions`
- `entitlement_landscape`
- `perspectival_gaps`
- `expressive_moves`
- `citation_baggage`
- `performative_contradictions`
- `authority_map`
- `same_word_different_concept`
- `modal_strength_analysis`
- `open_horizons`
- `cross_document_dynamics`
- `relationship_graph`
- `commitment_chains`
- `backing_hierarchies`
- `meta`

These are **not the same sections**. The V2 schema is structurally different and much richer. The section names are different. The nesting is different. Many V2 sections have no Critic UI counterpart. Some Critic sections (e.g., `the_deceptively_simple`) have no direct V2 equivalent.

For the **logical** path, the alignment is much closer. The 12-phase chain phases correspond one-to-one with the Critic orchestrator phases. The output fields may still differ at the detail level, but the structural correspondence is strong.

**Correction needed**: The memo should acknowledge that the inferential schema distance is substantial, not just "fields needing translation." The parity audit (Section A) is even more critical than the memo implies, specifically for inferential. The adapter layer for inferential will likely need to be a real structural transformation, not just field renaming.

### 3. Does the memo correctly distinguish the two rebasing problems?

**Yes. The distinction is both correct and important.**

**Inferential** is an engine/operationalization rebinding problem, but the memo understates the nature of this rebinding. The Critic-local path is a single LLM call with a single prompt. The analyzer-v2 path is a 4-stance operationalization with multi-pass depth sequences. So "rebinding" means switching from a one-shot prompt to a staged multi-pass analysis with accumulating passes. That is a rebinding problem, not an invention problem, because the operationalization already exists. But it is a more complex rebinding than the memo's language suggests.

**Logical** is correctly identified as a chain-level recomposition problem. The Critic's `ConceptAnalyzerOrchestrator` already runs 12 phases with per-phase prompt building, sub-passes (e.g., per-document argument formalization), and phase-to-phase context passing. The analyzer-v2 chain definition specifies the same 12 phases with the same engine keys. The recomposition question is whether execution should still be orchestrated by Critic's local `ConceptAnalyzerOrchestrator` using V2-sourced prompts, or whether it should be fully delegated to analyzer-v2's executor.

The fact that `phase_base.py` already has V2 prompt integration (lines 164-201, 227-345) means the logical path is **partially recomposed already** at the prompt level. The orchestrator still runs locally, but prompts can already come from V2. The memo should acknowledge this existing integration seam rather than treating the logical path as entirely un-migrated.

### 4. Is it right to keep the current Close Read and native Critic host contracts fixed during this tranche?

**Yes. This is the correct decision.**

The Close Read concept pages (`CloseReadConceptPages.tsx`) already import `InferentialDetail` and `LogicalDetail` from `ConceptsPanel`, have working submode/tab dispatch, scrutiny integration, and capture mode. Changing these surfaces while simultaneously swapping the execution backend would create compounding risk.

The native concept-analysis routes must also remain live because:

- Concept detection and launch UI live there
- Deferred submodes (assumption, semantic_field, causal, metaphorical) still run through native paths
- The admission audit correctly identified that Close Read is result-backed only

Freezing both host contracts is the right move. It lets the recomposition tranche focus on the execution ownership shift without coupling it to UI changes.

### 5. Does the memo correctly preserve the roadmap distinction between the four horizons?

**Yes. The distinctions are clear and consistently maintained.**

- **Fresh-project runtime truth**: Making existing analyzers work on new projects (genericize prompts, normalize persistence). Transitional but necessary. The fresh-project memo is explicit that analyzer-v2-native migration remains later.

- **analyzer-v2 recomposition**: Shifting execution ownership to analyzer-v2 definitions/chains while keeping host surfaces stable. This is the memo under review.

- **Composition-layer work**: General module-composition contracts across families, bespoke sequential modules, engine-to-engine compositions. The memo explicitly defers this (Section 6, "Deliberately Defers").

- **Standalone-host work**: Close Read as its own app. Also explicitly deferred.

The memo does not conflate these horizons. Its scope stays bounded to one family (concept analysis) and two surfaces (inferential, logical).

### 6. Does the memo overstate how close analyzer-v2 outputs already are to the current Critic host/result contracts?

**Yes, moderately, for inferential. No, for logical.**

For **inferential**: As detailed in answer #2 above, the schema distance is substantial. The memo's language - "fields already aligned / fields needing translation" - suggests a manageable field-mapping exercise. The reality is that the V2 inferential engine produces a structurally different output with different section names, different nesting, and many additional sections. The adapter layer will need to perform real structural transformation, not just field renaming.

The memo should acknowledge this more honestly. The parity audit (Section A) will likely find:

- Very few "fields already aligned"
- Many "fields needing translation" (which is really structural mapping)
- A large set of V2 fields with no Critic UI counterpart (which is fine - they can be ignored in the adapter)
- Some Critic UI fields with no direct V2 equivalent (which may need custom assembly from V2 output)

For **logical**: The 12-phase chain alignment is strong. The output fields may differ at the detail level, but the structural correspondence between V2 chain phases and Critic orchestrator phases means the adapter work is likely manageable.

**Correction needed**: The memo should add an explicit note that the inferential parity audit is likely to reveal a deeper structural gap than the logical one, and the adapter layer for inferential may be correspondingly more substantial.

### 7. Is the proposed parity-audit-plus-adapter approach the right bounded answer, or does the code suggest a more prior blocker still exists?

**The parity-audit-plus-adapter approach is the right bounded answer.**

No more prior blocker exists. The fresh-project runtime tranche (the immediate predecessor) addresses the last pre-existing blocker: making the analyzers project-aware and persistence-neutral. Once that lands, the recomposition work can proceed.

The only risk is that the parity audit reveals a larger adapter surface than expected (especially for inferential). But that does not change the approach - it changes the estimated effort. The alternative approaches are worse:

- Rewriting the UI around V2 schemas would violate the "keep host contract fixed" decision
- Rewriting the V2 engine to match Critic output shapes would treat Critic as canonical instead of transitional
- Waiting for a general composition layer would delay the first real proof of analyzer-v2-owned execution

The audit-then-adapt approach is correct. The memo should just be more explicit about the likely findings.

### 8. Does the memo correctly keep scrutiny narrower than the broader ammunition/send-to-outline estate?

**Yes. This is well-handled.**

The boundary memo already established:

- Scrutiny: admitted, logical-surface only
- Ammunition: explicitly deferred
- Send-to-outline: explicitly deferred
- Big-picture: explicitly deferred
- Cross-concept: explicitly deferred

The recomposition memo (Section E) correctly asks only whether scrutiny can consume rebased logical outputs, not whether the broader downstream estate should be migrated. Its "safe default" - keep scrutiny host-local but make its input derive from V2-owned logical results - is the right bounded answer.

### 9. Is the memo honest about the likely remaining dependence on host-local translation or normalization for the logical path?

**Partially honest. Could be more explicit.**

The memo says (Section D): "some adaptation is likely necessary because the old logical host surfaces reflect a legacy result shape and a legacy phase model."

That is correct but vague. The concrete situation is:

- The Critic `analyze_concept_logical.py` produces output validated against `LogicalAnalysisResult` (a Pydantic model in `api/models_concepts.py`)
- The logical UI (`LogicalDetail` in `ConceptsPanel.tsx`) renders specific fields from that model: `argument_inventory`, `argument_chains`, `logical_vulnerabilities`, `synthesis`, etc.
- The V2 chain phases produce individual phase outputs. The final result is assembled by the orchestrator
- The V2 chain's output shape is determined by the 12 engine schemas, not by `LogicalAnalysisResult`

So the host-local translation for logical is:

- V2 chain output (12 phase outputs) --> Critic `LogicalAnalysisResult` shape --> existing UI rendering

The memo should be more explicit that this translation layer exists and that its design is one of the key decisions the logical workstream must make.

### 10. Is there any place where the memo quietly slips back into treating Critic-local analyzers as canonical instead of transitional?

**No. The memo is consistently honest about the transitional nature of Critic-local code.**

- Section 3: "Critic-local prompt text and phase logic should be treated as transitional runtime residue to be reduced or wrapped, not as the authoritative future state."
- Section C (inferential rebinding): "analyzer-v2's inferential engine definition and operationalization as the canonical path"
- Section D (logical recomposition): "analyzer-v2's chain composition rather than the old Critic-local phase runtime as the primary owner"
- Section E (scrutiny): "keep scrutiny as a host-local follow-up operation" - this is acceptable because scrutiny is a host operation, not a core analytical capability

The only place that could be read as borderline is the acceptance path (Section F), which says "confirm the resulting concept appears correctly in native Critic concept views." But this is about rendering verification, not about treating native views as the canonical surface. It is asking whether the adapter produces results that current views can still display. That is correct.

---

## Corrections Required

### Correction 1: Acknowledge the inferential schema structural gap

The memo's Section A (Capability parity audit) should add an explicit note that the inferential parity audit is likely to find a **structural** gap, not just a field-naming gap. The analyzer-v2 `inferential_commitment_mapper.json` canonical schema uses fundamentally different section names and a different organizational structure compared to the Critic-local inferential prompt output. The adapter for inferential will need to perform structural transformation (assembling sections from V2 output into the shape the Critic UI expects), not just field renaming.

This does not change the approach. It changes the expected complexity of the adapter layer.

### Correction 2: Acknowledge the inferential execution model difference

The memo should note that the analyzer-v2 inferential engine has a **multi-pass operationalization** (4 stances across 3 depth sequences), while the Critic-local inferential path is a single LLM call. This means "rebinding" inferential does not just mean swapping one prompt for another - it means connecting to a fundamentally different execution model. The recomposition scope should decide:

- Whether to use the full multi-pass operationalization (which produces richer output)
- Or whether to use a bounded single-pass V2 execution path (which more closely matches the current Critic experience)
- Or whether to stage this (single-pass first, multi-pass later)

This decision belongs in the implementation scope, not the product boundary, but the recomposition memo should acknowledge that it exists.

### Correction 3: Acknowledge the existing V2 prompt integration in phase_base.py

The memo should note that `phase_base.py` already contains a complete V2 prompt integration layer:

- `get_v2_prompt_template()` (line 164): fetches prompts from analyzer-v2
- `build_prompt_from_v2()` (line 227): fills prompt templates with concept, documents, and previous phase outputs
- `_run_single_pass()` (line 477): tries V2 prompt first, falls back to hardcoded

This means the logical path is **partially recomposed already at the prompt level**. The orchestrator runs locally but can already source prompts from V2. The recomposition scope should explicitly build on this existing integration rather than designing from scratch.

This strengthens the memo's claim that the work is recomposition, not invention. But it also means the scope should characterize the remaining logical work more precisely: the missing piece is not "connect to V2 prompts" (that's already done) but "shift execution ownership from the local orchestrator to V2's executor or chain runner."

---

## Assessment Against The Broader Roadmap

### Alignment with the Close Read dictation

The original dictation explicitly names logical analysis, premise testing, and weak-point identification as core Close Read operations. Rebasing these onto analyzer-v2 execution is directly aligned with the dictation's intent: the app should be a composition over the analytical brain, not a standalone engine.

### Alignment with the analyzer-v2-as-brain objective

This memo is the first concrete scope that proposes making analyzer-v2 the **execution owner** for a shipped product family, not just a definition/prompt source. That makes it strategically significant. If this tranche succeeds, it proves that the "analyzer-v2 is the brain" thesis works for real product surfaces, not just for proof harnesses.

### Alignment with the default-families-then-composition-layer roadmap

The roadmap document (`MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`) explicitly says the path is:

1. Default families (genealogy, AOI, concept analysis)
2. Then composition layer
3. Then standalone host

This memo fits cleanly into step 1 by deepening concept analysis from "host-local execution with V2 prompt sourcing" to "V2-owned execution with host adapter." That is the right progression before attempting the general composition layer.

### Sequencing after fresh-project runtime

The fresh-project runtime memo addresses the immediate blocker (making existing analyzers work on new projects). The recomposition memo addresses the next architectural layer (making analyzer-v2 the execution owner). This sequencing is correct: you need the runtime to work before you can shift its ownership.

---

## Summary

The memo is well-crafted, strategically sound, and honest about the major direction. Its central claims about recomposition vs. invention, the two rebasing problems, and the correct scope boundaries are all supported by code evidence.

The three corrections above address gaps in the memo's treatment of schema distance (inferential), execution model difference (inferential), and existing integration state (logical). None change the strategic direction. They sharpen the implementation expectations.

**Verdict: Approve with corrections.**
