# Stage 10 Cross-Workflow Source-Backed Substrate Scope Audit

Verdict: `Approve`

Post-revision note:

- After reviewing the revised `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md`, the substantive blockers identified in this audit are now addressed at the memo level.
- The revised memo now distinguishes AOI source reconstruction from genealogy result-backed readiness, replaces premature registry language with a shared readiness schema plus workflow-owned implementations, carries the AOI/the-critic coupling explicitly, and raises the proof bar with a genealogy-specific partial-feasibility blocked case.
- The findings below remain the rationale for why the earlier draft was not approvable as written.

## Findings

1. **The repo does not yet support genealogy as a second workflow-owned source-backed slice.**
Evidence: the only explicit source catalog, selector, and section-materialization adapter is the AOI bridge in `src/presenter/composition_source_bridge.py:1-97` and `src/presenter/composition_source_bridge.py:259-437`, and the only public source-backed compose route is AOI-only in `src/presenter/compose_from_intent.py:110-152` and `src/presenter/compose_from_intent.py:330-338`. By contrast, genealogy planning still hydrates only from `registered_corpus` or `inline_documents`, not from durable saved-result identity, in `src/orchestrator/task_planning_schemas.py:40-129`, `src/orchestrator/task_planner.py:274-318`, and `src/orchestrator/task_router.py:172-224`.
Impact: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md:61-79` and `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md:161-195` overstate how close genealogy already is. The honest current state is: AOI has a real source-backed adapter; genealogy has durable result restore plus runtime recomposition, not source-backed composition from durable result truth.

2. **The current result/presenter substrate is real, but it is not yet a Stage-10-ready source-backed readiness substrate.**
Evidence: `src/analysis_products/result_contract.py:273-450` and `src/api/routes/results.py:44-116` expose result state, restoreability, artifact summaries, and optional `composition_mode`, but they do not expose source catalogs, allowed selectors, blocked selectors, or downstream followup contracts. `src/presenter/presentation_api.py:660-787` applies `composition_mode` only after building page payloads from recommended/authored views. `src/presenter/bounded_dynamic_composition.py:1-2` explicitly describes itself as "Proof-only runtime composition for presentations," and `src/presenter/bounded_dynamic_composition.py:267-366` validates and applies runtime composition modes at page-assembly time, not at durable-source adaptation time.
Impact: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md:61-79` and `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md:181-195` should describe the current reusable base as a result-restore/runtime-composition substrate, not as a mostly-ready cross-workflow source-backed substrate.

3. **The memo underplays how much AOI source-backed launch still depends on the-critic-specific host preparation.**
Evidence: Stage 8 and Stage 9 already documented that `source_analysis_id` remains host-side preparation and `profile` selection remains host-side in `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_completion.md:75-87` and `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_completion.md:99-118`. The live code matches that: analyzer-side `compose-from-source` only supports AOI and `consumer_key='the-critic'` in `src/presenter/compose_from_intent.py:330-338`; the-critic request shape still carries `source_analysis_id` in `/home/evgeny/projects/the-critic/api/models_genealogy.py:134-143`; the-critic backend resolves project/thinker-scoped identity and hard-codes `consumer_key: "the-critic"` in `/home/evgeny/projects/the-critic/api/server.py:18621-18686` and `/home/evgeny/projects/the-critic/api/server.py:20311-20340`; the hot path in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:438-497` warms a local snapshot and launches by `source_analysis_id`, not by a generic analyzer-owned contract. A repo search for `route-task` and `plan-task` under `/home/evgeny/projects/the-critic` returned no matches, so the Stage 8/9 analyzer-native routing and planning seams are not yet the live upstream integration path.
Impact: the memo should not describe the current AOI seam as if it were already mostly host-neutral workflow substrate or as if upstream had already cut over to the Stage 8/9 contracts. It is still materially coupled to the-critic's saved-result identity, project/thinker scoping, snapshot warmup behavior, and bespoke AOI launch path.

4. **The memo is right to preserve workflow-specific selectors, but it currently understates that `profile` and `composition_mode` live at different lifecycle layers.**
Evidence: AOI `profile` is a pre-compose selector over source families in `src/presenter/schemas.py:624-635` and `src/presenter/composition_source_bridge.py:67-97` plus `src/presenter/composition_source_bridge.py:362-437`. Genealogy `composition_mode` is a page-assembly/runtime selector in `src/presenter/bounded_dynamic_composition.py:35-82` and `src/presenter/bounded_dynamic_composition.py:267-366`, threaded through result/presenter restore in `src/analysis_products/result_contract.py:273-450` and `src/presenter/presentation_api.py:660-787`. The older runtime-composition memo also framed genealogy `composition_mode` as proof-mode runtime hierarchy generation, not durable-source adaptation, in `communications/MEMO_2026-03-20_round2_bounded_dynamic_composition_completion.md:17-65` and `communications/MEMO_2026-03-20_round2_bounded_dynamic_composition_completion.md:102-122`.
Impact: preserving workflow-specific selector unions is defensible, but the memo should say explicitly that the current selectors are not parallel selectors over one substrate. Without that clarification, Stage 10 risks quietly relabeling Stage-11-adjacent runtime/page composition as source-backed substrate.

5. **Calling Stage 10 the next stage is not aligned with the canonical recommended order unless the memo explicitly declares another intentional pull-forward.**
Evidence: the canonical roadmap defines Stage 10 as the cross-workflow source-backed substrate in `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:882-903`, but the recommended execution order still places AOI transient MVP completion, AOI task-driven composition, AOI source/engine-selection, evaluation, and lifecycle decisions before cross-workflow source-backed generalization in `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1041-1054`. The ledger also still marks Stages 2-6 open while Stage 10 remains not started in `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1087-1099`.
Impact: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md:15` is only defensible if it explicitly says this is another deliberate bridge-infrastructure pull-forward, analogous to Stages 7-9. Without that justification, the memo is misaligned with the larger program order.

6. **Genealogy's current artifact law is narrower than the memo implies.**
Evidence: `src/analysis_products/store.py:24-37` defines three AOI artifact families but only one genealogy artifact family, `genealogy.relationship_classification`. That family is persisted via `store_relationship_classification_artifact(...)` in `src/analysis_products/store.py:688-722`, and the write is triggered opportunistically during presentation payload construction in `src/presenter/presentation_api.py:2033-2067`.
Impact: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md:167-170` should not treat current genealogy artifact-slot law as if it already amounts to a durable source-material adapter registry. Right now it is one presenter-derived artifact seam, not a general genealogy source catalog.

## Direct Answers

- **Is the proposed Stage 10 seam really "workflow-owned source-backed substrate"?**
As a target, yes. In the live repo today, no. Today it would mostly be a renaming of one real AOI source-backed bridge plus existing result-restore and runtime-composition paths unless a real second workflow adapter is added.

- **Does the repo actually support genealogy as a second workflow source-backed slice, or only genealogy result restore with runtime view recomposition?**
Only genealogy result restore with runtime view recomposition. It does not yet support genealogy source-backed composition or genealogy source-backed inspection from durable saved-result identity.

- **Is the suggestion to preserve workflow-specific selector unions defensible, or should the stage force a single selector contract?**
Preserving workflow-specific selector unions is defensible now. The stage should not force a single selector contract yet. But the memo should clarify that AOI `profile` and genealogy `composition_mode` are selectors at different lifecycle phases, not just different enum vocabularies.

- **Does the memo correctly avoid importing Stage 11 page-planning and Stage 13 host-contract work too early?**
Mostly yes in prose: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md:117-123` and `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md:226-238` draw the right boundary. The risk is practical, not rhetorical: if genealogy's existing `composition_mode` path is treated as the Stage 10 substrate, that quietly imports Stage-11-adjacent runtime/page composition; if the proposed inspection boundary is over-specified as host behavior rather than analyzer-owned readiness inspection, that starts drifting into Stage 13.

## Checked Absence

No relevant `Perspective` docs folder exists in this repo. I checked for directories matching `*Perspective*` under the repo root, `docs`, and `communications`, and found none.

## Required Revisions And Proof Requirements

1. Revise the memo's "already real" section so it distinguishes three different things:
AOI source-backed adapter law; result/presentation restore law; runtime `composition_mode` law. Do not call the latter two already-source-backed substrate.

2. Recast genealogy from "already credible second source-backed slice" to "best second candidate, but still missing a durable-result adapter."
The current repo does not meet the roadmap's Stage 10 exit evidence of "a second workflow can compose from durable source truth without AOI-specific hacks" in `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:900-903`.

3. Carry the AOI host-preparation seam explicitly into the stage scope.
Today the-critic still owns `source_analysis_id` resolution, project/thinker validation, snapshot warmup, and the current analyzer compose path only supports `consumer_key='the-critic'`.

4. Keep selector asymmetry explicit with a discriminated union, but label each selector by lifecycle phase.
AOI `profile` is source-selection-time; genealogy `composition_mode` is restore/page-runtime-time. Stage 10 should normalize readiness output shape, not pretend these selectors already live at one abstraction level.

5. Either justify Stage 10 as an intentional pull-forward despite open Stages 2-6, or stop calling it the next stage.
The roadmap already provides the standard for that justification in `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1041-1054`.

6. Raise the Stage 10 proof bar so it requires code and artifacts for:
one AOI case proving the new adapter layer wraps the current Stage 7 bridge; one genealogy case proving durable saved-result identity can produce source-backed readiness/followup without relying only on page restore plus `composition_mode`; one blocked-source case returning explicit blocker reasons; one analyzer-owned inspection/readiness contract returning normalized source families, allowed selectors, blocked selectors, and downstream followup.

## Secondary Summary

The memo's core instinct is good: do not force a fake universal selector enum, do not claim Stage 11 page planning or Stage 13 host-contract formalization too early, and do not pretend AOI's current bridge already generalizes. The revision it needs is narrower but important: genealogy is not yet a real second source-backed workflow slice, and the current reusable substrate is still mostly result restore plus proof/runtime recomposition rather than cross-workflow source-backed adapter law.
