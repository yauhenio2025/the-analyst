# Critique: Phase 1C Bounded Router/Planner Generalization Scope

Date: 2026-03-27
Reviewer: Claude Opus 4.6
Memo under review: `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_scope.md`

## Verdict

**Approve after revision.**

The memo correctly identifies the right next honest step. It is properly sequenced, properly bounded, and the strategic reasoning is sound. However, it contains one material hidden assumption and two boundary ambiguities that would block or mis-scope the implementation if not resolved before coding.

---

## Findings (ordered by severity)

### FINDING 1 (High): The memo assumes genealogy saved-result truth can produce `prose_sections` but does not name the missing bridge infrastructure

The memo's "must land" item #3 says the planner should "derive the direct-sections handoff from analyzer-owned durable genealogy result truth" and lists allowed evidence sources:

- bounded result metadata
- analyzer-owned presentation/view truth
- analyzer-owned artifacts already attached to the saved result

But the current `composition_source_bridge.py` is **entirely AOI-specific**:

- `composition_source_bridge.py:1` — file-level docstring: "AOI source-to-composition bridge for transient compose-from-source."
- `composition_source_bridge.py:9-16` — imports are all AOI constants (`AOI_ENGAGEMENT_MAPPING_ENGINE`, `AOI_THEMATIC_SYNTHESIS_ENGINE`, etc.)
- `composition_source_bridge.py:33-36` — source families are all AOI: `thematic_synthesis`, `engagement_mapping`, `sin_findings`, `thematic_report`
- `composition_source_bridge.py:319` — `resolve_source_catalog()` resolves only AOI candidates and falls back to `AOI_WORKFLOW_KEY` and `AOI_DEFAULT_OBJECTIVE_KEY`

There is **no** existing infrastructure to extract composition-facing `prose_sections` from a completed genealogy job. The memo says the planner should produce `materialized prose_sections ready for the shared direct_sections executor`, but nowhere does it acknowledge that:

1. A genealogy-equivalent of `resolve_source_catalog` or a generic result-to-sections extractor must be built
2. Genealogy phase outputs have a different structure than AOI artifacts — they go through `load_phase_outputs()` (`output_store.py:67`) and `assemble_page()` (`presentation_api.py:888`), not through `load_aoi_normalized_artifact()`
3. The mapping from genealogy engine outputs to `ComposeFromIntentSectionInput` (which needs `engine_key`, `title`, `prose`) is undecided

This is not a fatal flaw — genealogy results DO have per-engine prose stored in the output store, and the presentation layer already assembles these into view payloads. But the memo makes it sound like the planner can just "derive" sections from existing truth, when in fact a new section-extraction layer must be built.

**Required revision**: The memo should acknowledge that Phase 1C requires either:
- A genealogy-specific section extractor (parallel to `composition_source_bridge.py` but for genealogy engine outputs), or
- A generic result-to-sections adapter that works across workflows

And it should name the likely implementation anchor files — probably a new function in or alongside the existing composition bridge, plus helpers from `output_store.py` and the existing presenter machinery.

### FINDING 2 (Medium): The `SavedResultPlanningContext` is too thin for genealogy composition planning

The memo proposes that genealogy should become routable for `saved_result` and that `plan-task` should return a composition-facing handoff. But the existing `SavedResultPlanningContext` (`task_planning_schemas.py:128-133`) carries only:

```python
class SavedResultPlanningContext(StrictBaseModel):
    context_mode: Literal["saved_result"] = "saved_result"
    source_v2_job_id: Optional[str] = None
    consumer_key: Optional[str] = None
```

For the AOI path, this is sufficient because `resolve_source_catalog()` can load everything it needs from the `source_v2_job_id` — the AOI artifacts, plan context, and objective metadata are all resolvable from the job.

But the memo says the handoff payload must include `objective_key`, `consumer_key`, `workflow_key`, and a `resolved_intent_seed`. The `objective_key` is derivable from the job's plan, but the `resolved_intent_seed` (a user-facing composition directive) is not stored anywhere in the genealogy result. This means:

- Either the planner must synthesize the intent seed from result metadata (which requires LLM or heuristic logic)
- Or the `SavedResultPlanningContext` needs additional fields like `user_intent` or `composition_directive`
- Or the handoff payload structure must allow `resolved_intent_seed` to be empty/defaulted for non-AOI paths

The memo's handoff shape at lines 157-165 lists `resolved_intent_seed` as minimum required. This may be too strict for an initial genealogy composition path where the user's intent is implied ("show me the genealogy results as a composed page").

**Required revision**: Decide explicitly whether `resolved_intent_seed` is required or defaultable for the new outcome. If required, specify where it comes from for genealogy. If defaultable, say so.

### FINDING 3 (Medium): The boundary between `direct_sections_composition_handoff_plan` and `AoiCompositionHandoffPlan` is under-specified

The memo proposes a new `planning_outcome_kind = direct_sections_composition_handoff_plan` as a generic outcome. Currently `TaskPlanningDecision` (`task_planning_schemas.py:192-211`) has:

```python
planning_outcome_kind: PlanningOutcomeKind  # Literal union
aoi_composition_handoff_plan: Optional[AoiCompositionHandoffPlan] = None
```

The `PlanningOutcomeKind` literal at line 26 is: `genealogy_execution_plan | aoi_composition_handoff_plan | aoi_selection_blocked | insufficient_context | unsupported`.

Adding `direct_sections_composition_handoff_plan` to this union is straightforward. But:

- What model holds the new outcome's payload? The memo says it should be generic, not genealogy-only. But `AoiCompositionHandoffPlan` (lines 166-189) has AOI-specific fields: `selected_sources`, `rejected_sources`, `legacy_profile_equivalent`, `allowed_profiles`, `blocked_profiles`, `bridge_contract_targets` referencing `CompositionSourceCatalog`.
- The memo's required payload (lines 157-165) includes `compose_entrypoint_kind = presenter.compose_from_intent` — note this is `compose_from_intent`, not `compose_from_selection` (which is what AOI uses). This is a deliberate and correct distinction — the new path would use `direct_sections` through `compose_from_intent`, not the selection bridge.
- But the memo doesn't define the actual Pydantic model for the new handoff plan. It should, because the persistence snapshot system needs to serialize it.

**Required revision**: Specify whether the new outcome uses a new model (e.g., `DirectSectionsCompositionHandoffPlan`) or extends the existing schema. The new model should carry the fields listed in the memo (lines 157-165) and be representable inside `PersistedTaskPlanningDecision`.

### FINDING 4 (Low): The memo does not address the `DownstreamReadiness` literal for the new outcome

`DownstreamReadiness` (`task_planning_schemas.py:34-40`) currently has:

```python
DownstreamReadiness = Literal[
    "ready_for_genealogy_execution",
    "ready_for_aoi_compose_handoff",
    "blocked_for_aoi_selection",
    "needs_more_context",
    "unsupported",
]
```

The new outcome needs a new `downstream_readiness` value (e.g., `ready_for_direct_sections_compose_handoff`). The memo's acceptance tests reference "the returned handoff payload can drive the shared compose-from-intent executor" but don't name the `downstream_readiness` value.

This is minor but should be noted for implementation clarity.

### FINDING 5 (Low): The `RoutingOutcome` literal and `LaunchContractKind` literal need expansion

Currently (`task_routing_schemas.py:61-69`):

```python
RoutingOutcome = Literal["aoi_transient_source_backed", "genealogy_job_backed", "unsupported"]
LaunchContractKind = Literal[
    "planner.aoi_compose_handoff",
    "presenter.compose_from_source",
    "orchestrator.analyze",
    "orchestrator.analyze_by_ref",
    "unsupported",
]
```

The new genealogy `saved_result` composition path needs either a new `RoutingOutcome` (e.g., `genealogy_transient_source_backed`) or the existing `genealogy_job_backed` must be reused with a new `LaunchContractKind`. The memo doesn't specify which.

Additionally, `_supported_outcome()` at `task_router.py:387-395` currently maps genealogy to `genealogy_job_backed` with `orchestrator.analyze_by_ref` or `orchestrator.analyze`. The new `saved_result` path needs a different outcome here.

---

## Direct Answers to the Prompt Questions

### Q1: Is the memo correct that the main remaining Phase 1 gap is planner asymmetry?

**Yes.** The code confirms:
- Host Contract v2 is implemented (`hostContractV2.ts` has planner-advisory families)
- Planning snapshots persist and reload (`planning_decision_store.py`)
- The shared handoff executor supports genealogy `direct_sections` (`compose_from_intent.py:152`)
- But `route-task` rejects genealogy `saved_result` (`task_router.py:175`)
- And `plan-task` only produces `genealogy_execution_plan` for genealogy (`task_planner.py:439`)

The asymmetry is real and code-backed.

### Q2: Is the current non-AOI proof only materialization-level?

**Yes.** Genealogy is registered for `direct_sections` in `_SUPPORTED_HANDOFF_KINDS` (`compose_from_intent.py:152`), which means you CAN call `compose-from-intent` with a genealogy workflow key and manually-supplied sections. But no planner path produces those sections from saved results. The proof is: "if someone gives us the sections, we can compose them." It is NOT: "the planner can derive sections from genealogy results and hand them off."

### Q3: Is genealogy + saved_result + generic direct_sections the right bounded target?

**Yes, with the caveat from Finding 1.** This is the right seam to close because:
- It exercises the same `source_v2_job_id` doctrine already proven on AOI
- It uses the same immutable planning snapshot system
- It lands on the same shared `compose-from-intent` executor via `direct_sections`
- It avoids conflating execution planning with composition planning

The risk is that genealogy saved-result truth may be thinner than AOI truth for composition purposes. Genealogy phase outputs are stored as engine-level prose in the output store, which is structurally sufficient, but the extraction/materialization layer doesn't exist yet.

### Q4: Does the code support the claim that genealogy is excluded from saved_result routing?

**Yes, emphatically.** Three explicit code gates:

1. `task_router.py:175` — `_is_source_mode_compatible("genealogical", "saved_result")` returns `False`
2. `task_router.py:224` — `_assess_genealogy_source_sufficiency()` returns `"insufficient"` for `saved_result`
3. `task_planner.py:385` — `_plan_genealogy()` rejects any context mode other than `registered_corpus` or `inline_documents`

And the downstream followup at `task_planner.py:445-448` always points to `/v1/executor/jobs`.

### Q5: Is the proposed generic planner outcome genuinely reusable?

**Mostly yes, if the handoff model is kept workflow-neutral.** The proposed payload shape (lines 157-165) is workflow-neutral: `workflow_key`, `objective_key`, `consumer_key`, `source_v2_job_id`, `compose_entrypoint_kind`, `prose_sections`. None of those are genealogy-only.

The risk is that the section extraction layer will be workflow-specific (because different workflows produce different engine outputs). But that's acceptable — the handoff *contract* is generic even if the *bridge* that produces sections is workflow-specific. This mirrors the AOI design where `composition_source_bridge.py` is AOI-specific but `compose-from-intent` is generic.

### Q6: Does the memo protect the registered_corpus path?

**Yes.** Acceptance test #5 (line 233) explicitly requires that the existing path still returns `genealogy_execution_plan` with `/v1/executor/jobs`. Lines 140-141 say "do not remove or weaken the current registered_corpus and inline_documents routes."

### Q7: Is there a deeper blocker?

**Yes — Finding 1.** The genealogy section extraction gap is a real prerequisite. It is not a blocker to the memo's approval, but it is a blocker to implementation. The memo should name it.

Secondary concern: the `SavedResultPlanningContext` may need enrichment (Finding 2), but this can be discovered during implementation.

No hidden host/runtime dependence found — the host side only needs to call `route-task` and `plan-task` and then navigate to the shared compose page with the planning_decision_id. The existing `taskLaunchRuntime.ts` already dispatches these families.

### Q8: Is it properly sequenced?

**Yes.** The sequence is:
1. Phase 1B locked ownership decisions ✓
2. Phase 1A implemented the bridge substrate ✓
3. Phase 1C generalizes the planner (this memo)
4. End-of-phase browser/harness proof follows Phase 1C (correctly deferred)
5. Phase 2 host-neutral proof follows Phase 1 completion (correctly deferred)

The memo stays on the right side of every sequencing boundary.

### Q9: Is it concrete enough?

**Almost.** The acceptance tests (lines 228-234) are specific and testable. The handoff payload shape (lines 157-165) is well-defined. The "must not widen" constraints (lines 216-223) are appropriate.

What's missing:
- Acknowledgment that a new section-extraction layer must be built (Finding 1)
- Decision on whether `resolved_intent_seed` is required or defaultable (Finding 2)
- The Pydantic model shape for the new outcome (Finding 3)

---

## Concrete Revisions Needed Before Implementation

1. **Add a subsection acknowledging the genealogy section extraction prerequisite.** Something like: "Materializing `prose_sections` from genealogy result truth requires building a section extractor (analogous to but separate from the existing AOI `composition_source_bridge.py`) that can derive `ComposeFromIntentSectionInput` entries from genealogy engine-level phase outputs. This extractor is new code within this slice, not an existing capability."

2. **Decide on `resolved_intent_seed` policy for non-AOI handoffs.** Either make it defaultable (e.g., "Compose the genealogy analysis results") or require it as a planner input.

3. **Name the new handoff model** (e.g., `DirectSectionsCompositionHandoffPlan`) and confirm it will be added as a new optional field on `TaskPlanningDecision` alongside the existing `aoi_composition_handoff_plan`.

4. **Note the schema expansions needed**: `PlanningOutcomeKind`, `DownstreamReadiness`, `RoutingOutcome` / `LaunchContractKind` literals.

---

## Is This The Right Next Honest Step?

**Yes.** The memo correctly identifies the one remaining structural asymmetry that prevents Phase 1 from being honestly complete. The planner layer is the gap, not the host contract, not the compose executor, not AOI local repair.

## Does The Memo Stay Properly Bounded?

**Yes.** It adds one new planner outcome, exercises it on one bounded case (genealogy saved-result), preserves the existing execution-plan path, and defers browser polish and host-neutral proof to later. The "must not widen" constraints are well-chosen and match the anti-drift rules from the fixed-direction roadmap.

The only unboundedness risk is the section extraction work (Finding 1), which is real implementation effort that the memo currently makes sound smaller than it is. Naming it explicitly would prevent scope surprise during implementation.
