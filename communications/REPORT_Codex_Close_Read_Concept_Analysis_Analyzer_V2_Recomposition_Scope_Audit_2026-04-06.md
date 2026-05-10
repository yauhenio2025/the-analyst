# Close Read Concept Analysis analyzer-v2 Recomposition Scope Audit

## Context Check
- Read in full: `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md`
- Read in full: `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- Read in full: `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- Read in full: `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- Read in full: `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

## Verdict
**Approve with corrections**

## Executive Summary
The memo gets the strategic move right. The code does support reframing the next tranche as analyzer-v2 recomposition rather than scratch capability-building: analyzer-v2 already has a real inferential engine plus operationalization and a real concept-analysis chain definition, while Critic still owns the active inferential and logical execution paths locally. The memo is also correctly narrow about keeping host surfaces fixed and not widening into standalone host work or general module composition.

The corrections are mostly about the logical path. Inferential rebasing is a schema/adapter problem over an already legible analyzer-v2 engine. Logical rebasing is not that simple. The current Critic logical runtime is a local 12-phase orchestrator with local merge logic, local cache/debug/save behavior, and a local final assembly layer that explicitly reshapes outputs for the existing UI. analyzer-v2 has enough chain/engine inventory to justify rebasing, but not enough evidence of a drop-in final contract to justify treating logical translation as straightforward. The memo should freeze that distinction more sharply.

## Code-Backed Findings

### 1. The memo is right to frame this as recomposition, not invention
analyzer-v2 already contains concrete concept-analysis capability inventory:

- inferential engine definition and canonical schema: `src/engines/definitions/inferential_commitment_mapper.json:2-10`
- inferential staged operationalization: `src/operationalizations/definitions/inferential_commitment_mapper.yaml:3-128`
- dedicated 12-phase concept-analysis chain: `src/chains/definitions/concept_analysis_12_phase.json:2-99`
- broader concept suite inventory: `src/chains/definitions/concept_analysis_suite.json:2-25`

This is enough to justify rebasing as the right strategic frame. The memo is correct to reject “move/build inferential and logical from scratch.”

### 2. The current Critic execution is still too locally owned for “analyzer-v2 as the brain”
The active runtime owner is still Critic:

- API dispatch still calls Critic-local inferential and logical implementations directly: `/home/evgeny/projects/the-critic/api/server.py:3905-3944`
- inferential remains a fully local prompt/build/parse/save loop, even if it says it is “based on” the analyzer engine: `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py:70-383`
- logical remains a local multi-pass orchestrator with local phase ordering, local progress/cancellation, local cache/resume, and local save/final assembly: `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py:102-183`, `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py:249-366`, `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/orchestrator.py:38-278`
- the phase base only fetches analyzer-v2 prompts opportunistically; execution, parsing, debug capture, and intermediate persistence remain local Critic responsibilities: `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py:164-202`, `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py:404-557`

That supports the memo’s claim that the fresh-project tranche did not yet satisfy analyzer-v2-as-brain.

### 3. The memo is right that inferential and logical are two distinct rebasing problems
The code strongly supports keeping them separate.

Inferential:
- one dedicated local script
- one local prompt contract
- one local saved-result schema
- analyzer-v2 already has one corresponding engine plus operationalization

Evidence:
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py:70-383`
- `src/engines/definitions/inferential_commitment_mapper.json:2-10`
- `src/operationalizations/definitions/inferential_commitment_mapper.yaml:3-128`

Logical:
- a local orchestrator drives 12 named phases
- some phases use analyzer-v2 engine keys, but Critic still owns phase sequencing, sub-pass strategy, merge logic, and UI-contract assembly
- the logical path is therefore a chain/runtime/final-contract rebasing problem, not an engine swap

Evidence:
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/orchestrator.py:98-236`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p03_argument_formalization.py:21-197`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p05_chain_taxonomy.py:18-38`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p09_vulnerability_analysis.py:18-32`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p12_synthesis.py:238-542`

So the memo’s “two distinct rebasing problems” claim is well supported.

### 4. The memo correctly keeps the host/product boundary stable
The existing code already expresses the boundary the memo wants to preserve:

- native concept-analysis route remains: `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:159-168`
- Close Read concept routes remain fixed: `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:261-289`
- Close Read concept pages only admit inferential and logical, expose unavailable states, and link back to native concept-analysis rather than widening the host boundary: `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx:53-85`, `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx:560-575`, `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx:760-783`, `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx:880-936`

This matches the memo’s “keep routes and surfaces fixed while shifting runtime ownership” stance.

### 5. The memo slightly overstates translation ease, especially for inferential
Inferential rebasing is justified, but the current Critic rendering contract is not close to analyzer-v2’s canonical schema.

Current Critic inferential UI expects a sectioned narrative contract:
- `the_deceptively_simple`
- `commitment_cascade`
- `incompatibility_map`
- `tensions`
- `practical_stakes`
- `commitment_packages`
- `synthesis`

Evidence:
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py:103-257`
- `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:3096-3427`

The analyzer-v2 inferential engine instead declares a graph- and entity-oriented canonical schema:
- `key_ideas`
- `what_youre_signing_up_for`
- `what_backs_this_up`
- `either_or_choices`
- `real_world_implications`
- `unresolved_tensions`
- `relationship_graph`
- `commitment_chains`

Evidence:
- `src/engines/definitions/inferential_commitment_mapper.json:10-120`

That does not make rebasing wrong. It does mean the memo should not imply “adapter/translation” is likely light. The adapter is plausible, but non-trivial.

### 6. The logical compatibility question is the main under-scoped issue
The logical path is where the memo needs correction.

The analyzer-v2 12-phase chain is real, but its declared engines are materially coarser than the current Critic logical runtime:

- chain phase 5 uses one engine key, `concept_taxonomy_function`: `src/chains/definitions/concept_analysis_12_phase.json:52-55`
- current Critic phase 5 expects five separate taxonomy sub-passes: `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p05_chain_taxonomy.py:21-38`

- chain phase 9 uses one engine key, `concept_vulnerability_inferential_gaps`: `src/chains/definitions/concept_analysis_12_phase.json:76-79`
- current Critic phase 9 expects five separate vulnerability sub-passes: `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p09_vulnerability_analysis.py:21-32`

The current analyzer-v2 engine definitions are also thinner than the current Critic logical UI/scrutiny contract:

- `concept_taxonomy_function` exposes only an object-shaped canonical schema and a general argumentative-function question: `src/engines/definitions/concept_taxonomy_function.json:2-18`
- `concept_vulnerability_inferential_gaps` only guarantees `vulnerability_id`, `vulnerability_type`, `gap_description`, and `severity`: `src/engines/definitions/concept_vulnerability_inferential_gaps.json:2-33`

But the current logical UI and scrutiny flows depend on much richer assembled fields:

- `LogicalDetail` expects `argument_inventory`, `argument_chains`, `causal_architecture`, `conditional_web`, `logical_vulnerabilities`, and `synthesis`: `/home/evgeny/projects/the-critic/webapp/src/ConceptsPanel.tsx:4483-4755`
- Close Read scrutiny requests depend on `arg.id`, `logical_form.premises`, `logical_form.conclusion`, `unstated_premises`, `quote`, and `concept_role`: `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx:380-438`
- Critic’s local phase-12 assembly explicitly exists to reshape phase outputs into this legacy UI contract: `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p12_synthesis.py:238-542`

Most importantly, analyzer-v2’s `concept_synthesis` definition is not a drop-in version of the current logical UI schema. It is evolution/genealogy-oriented and centers `semantic_core`, `argumentative_architecture`, `evolution_timelines`, `convergence_divergence`, and `critical_verdict`: `src/engines/definitions/concept_synthesis.json:4-18`, `src/engines/definitions/concept_synthesis.json:24-105`.

That means the memo is right to call for a parity audit, but not yet concrete enough on the logical target contract. The ambiguity is more prior than “adapter or translation?” It is: **what exact analyzer-v2-owned logical output contract are we rebasing onto?**

### 7. Scrutiny should stay host-local in this tranche, but only under a stricter requirement
The memo’s safe default is directionally right. Current scrutiny is a host/API follow-up operation:

- UI starts scrutiny from logical arguments and premise data: `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx:380-438`
- API keeps a separate scrutiny job/result flow: `/home/evgeny/projects/the-critic/api/server.py:6717-6865`

So keeping scrutiny host-local while changing logical execution ownership is a sensible bounded answer.

But the memo should say explicitly that this is only valid if the rebased logical output preserves the scrutiny input contract or provides an equivalent normalized contract before the host invokes scrutiny.

### 8. The scope remains properly narrower than migration-everything, module-composition work, or standalone Close Read host work
The memo stays narrower than:

- analyzer-v2-native migration of every concept submode
- general composition-layer work
- standalone Close Read host work

The current code boundary supports that reading:

- native concept-analysis remains live: `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:159-168`
- Close Read remains one family under the Critic umbrella, not a separate host: `/home/evgeny/projects/the-critic/webapp/src/routes.tsx:261-289`
- server dispatch still treats other concept submodes separately and does not collapse the whole concept estate into one move: `/home/evgeny/projects/the-critic/api/server.py:3924-3944`

### 9. No material contradiction with the default-families-plus-composable-modules roadmap
I do not see a roadmap contradiction. The memo is consistent with the larger direction captured in the earlier roadmap memos:

- analyzer-v2 remains the capability brain
- Close Read remains a family surface under Critic
- this tranche is one bounded family rebasing step, not a substitute for later composition-layer work

The only caution is wording: if “adapter/translation” were allowed to become indefinitely host-local and unowned, that would drift away from analyzer-v2-as-brain. But the memo frames this as a bounded tranche, so that risk is correctable rather than structural.

## Explicit Answers

- **Is the memo right that analyzer-v2 already has enough inferential/logical capability definition to justify rebasing rather than reinvention?**
  - **Yes, with correction.** Inferential clearly does. Logical does at the level of chain/phase inventory, but not yet at the level of a drop-in final contract.

- **Does the code support the memo’s claim that inferential and logical should be treated as two distinct rebasing problems?**
  - **Yes.** Inferential is a single-script local runtime over an analyzer-v2-aligned idea. Logical is a local chain/orchestrator/assembly runtime with only partial analyzer-v2 prompt alignment.

- **Does the memo correctly keep Close Read/native concept routes fixed in this tranche?**
  - **Yes.** That is aligned with the current route tree and with the current Close Read concept family implementation.

- **Is the parity-audit requirement concrete enough, or does it still leave a more prior design ambiguity unresolved?**
  - **Not fully concrete enough.** It is concrete for inferential. For logical, it still leaves unresolved what the analyzer-v2-owned target contract actually is.

- **Does the memo overstate the ease of translating analyzer-v2 outputs into current Critic rendering contracts?**
  - **Yes, somewhat.** Inferential translation is non-trivial, and logical translation is materially more complex than the memo suggests.

- **Is the logical scrutiny compatibility question scoped correctly, or does the memo leave too much unresolved there?**
  - **The question is scoped correctly, but too much remains unresolved.** The memo needs an explicit requirement that scrutiny-critical fields survive the rebasing.

- **Does this scope stay properly narrower than analyzer-v2-native migration of every concept submode, general module-composition work, and standalone Close Read host work?**
  - **Yes.** The memo remains properly bounded.

- **Is there any place where the memo contradicts the larger default-families-plus-composable-modules roadmap?**
  - **No material contradiction.** It is consistent with the roadmap’s “default family first, broader composition later” logic.

## Required Corrections Before Freezing Scope

1. **Name the logical target contract explicitly.**
   - The memo should say whether the tranche targets:
   - analyzer-v2 owning raw phase execution plus a temporary Critic-side adapter/finalizer
   - or analyzer-v2 owning both execution and the final normalized logical contract consumed by Critic
   - Without that decision, “parity audit + adapter” is underspecified.

2. **Require a contract matrix, not only a narrative parity audit.**
   - At minimum, produce:
   - inferential field matrix: analyzer-v2 canonical fields -> current native/Close Read inferential fields
   - logical field matrix: analyzer-v2 chain/engine outputs -> current `argument_inventory` / `argument_chains` / `causal_architecture` / `conditional_web` / `logical_vulnerabilities` / `synthesis`
   - scrutiny input matrix: rebased logical output -> `ScrutinizePremiseRequest` requirements

3. **Tone down any implication that translation is likely simple.**
   - For inferential, say “bounded but non-trivial contract adapter.”
   - For logical, say “explicit compatibility-layer design required before execution-owner swap.”

4. **Make scrutiny acceptance criteria stricter.**
   - The tranche should not count as complete unless one rebased logical result supports the current scrutiny flow without synthetic/manual patching of the request payload at the UI layer.

## Bottom Line
The memo is strategically right and roadmapped correctly. The next phase should indeed be analyzer-v2 recomposition, not another round of Critic-local hardening and not a scratch rebuild. But the memo should be corrected before freeze so that it does not blur a real difference:

- inferential rebasing is mostly an engine/schema adapter problem
- logical rebasing is a chain/runtime/final-contract problem with a scrutiny dependency

That is why the correct outcome is **approve with corrections**, not full approval and not rejection.
