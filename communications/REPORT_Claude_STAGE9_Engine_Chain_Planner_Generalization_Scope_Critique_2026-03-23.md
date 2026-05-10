# Critique: Stage 9 / Engine-Chain Planner Generalization Scope

Reviewer: Claude (skeptical strategic review)
Date: 2026-03-23
Target Memo: `communications/MEMO_2026-03-23_stage9_engine_chain_planner_generalization_scope.md`

## Verdict: Approve after revision

The memo correctly identifies the real missing seam: the gap between Stage 8's routing decision and the actual analytical plan that should follow. The diagnosis is honest, the scope boundaries are disciplined, and the proposed asymmetric outcome set (genealogy_execution_plan vs aoi_composition_handoff_plan vs unsupported) is the right shape. However, the memo has a significant input-contract gap it does not confront, overstates the simplicity of "reusing" the existing planner substrate for this purpose, and under-specifies several architectural joints that will matter during implementation planning.

---

## Finding 1 (Architectural — Critical): The input-contract gap between the task envelope and the planner is unaddressed

**The problem**: The memo says Stage 9 should "accept the Stage 8 task envelope directly" or "accept the Stage 8 task envelope plus an already-produced routing decision." But the Stage 8 `CompositionTaskRequest` (`src/orchestrator/task_routing_schemas.py:104-123`) is a lightweight advisory envelope:

- `task` (free text)
- `objective_hint` (optional string)
- `source_constraints` (metadata-only hints — no actual data, no thinker_name, no target_work, no prior_works)
- `audience`, `desired_depth`, `style_expectations` (optional strings)
- `consumer_key`, `workflow_hint` (optional strings)

The existing planner (`src/orchestrator/planner.py`, `src/orchestrator/adaptive_planner.py`) requires an `OrchestratorPlanRequest` (`src/orchestrator/schemas.py:313-363`) which needs:

- `thinker_name` (required)
- `target_work` (required TargetWork with title, description)
- `prior_works` (list of PriorWork with title, description, relationship hints, source_thinker_id, source_document_id)
- `research_question`, `depth_preference`, `focus_hint`
- `selected_source_thinker_id`, `selected_source_thinker_name`
- `workflow_key`

**The gap is not small.** The task envelope has almost none of the data the planner needs. The memo says "reuse the existing substrate" but does not address how a lightweight composition-facing task envelope gets transformed into the rich planner context required by `generate_plan()` or `generate_adaptive_plan()`.

**What must change**: The memo must explicitly confront this gap. Options include:

1. Stage 9 defines a richer `TaskPlanningRequest` that includes the task envelope plus structured analytical context (this is essentially a superset of both `CompositionTaskRequest` and `OrchestratorPlanRequest`)
2. Stage 9 reuses the routing decision to determine _which_ planner path to invoke, and then requires the host to also provide the planner-level context alongside the task envelope
3. Stage 9 accepts only the task envelope but returns a "planning prerequisites" contract that tells the host what additional context is needed before a plan can be generated

The memo must pick one of these (or a fourth option) and say so explicitly. Without this, the "reuse existing planner" claim is hollow.

---

## Finding 2 (Strategic — Important): The 3-step advisory chain creates friction

The program is building a layered advisory chain:

1. `route-task` -> decides workflow family
2. `plan-task` -> produces analytical plan
3. Host calls downstream endpoint -> execution or composition

That is three round-trips before anything executes. The memo should address:

- Is this the right granularity for real-world host integration?
- Should `plan-task` incorporate routing internally (accepting the same task envelope and producing routing + plan in one call)?
- Or is the separation valuable enough to justify the extra step?

The memo's current framing treats plan-task as a separate advisory step after route-task, but it doesn't argue why that separation is valuable versus combining them. The strongest argument for separation would be that different hosts may want to inspect/approve the routing decision before planning. The memo should make this argument explicitly, or reconsider.

---

## Finding 3 (Architectural — Important): The genealogy "reuse" story is realistic but needs specificity

The memo says genealogy planning should "use the existing objective/planner substrate" and "return explicit phase/chain/engine planning truth." Verified against code:

- `src/orchestrator/adaptive_planner.py` already generates a full `WorkflowExecutionPlan` with phases, chains, engines, decision traces
- `src/orchestrator/catalog.py` already assembles a planner-readable capability catalog
- `src/objectives/definitions/genealogical.json` already has rich planner_strategy, primary_goals, quality_criteria
- The pipeline (`src/orchestrator/pipeline.py`) already chains plan generation into execution

So the claim that genealogy planning substrate exists is **true and well-grounded in code**.

However, the current planner takes `OrchestratorPlanRequest` — not a `CompositionTaskRequest`. The memo's genealogy slice needs to specify exactly how the task envelope maps into the planner call. The existing `generate_adaptive_plan()` requires book samples (from actual document text), which the task envelope does not contain.

**What this means**: For genealogy, Stage 9 would either need to:
- Call the planner with whatever context is available and accept a lower-quality plan, or
- Require the host to provide planner-level context alongside the task, or
- Produce a "plan skeleton" that names phases/chains but can't produce the full adaptive plan without document text

The memo should be explicit about which of these Stage 9 targets.

---

## Finding 4 (Architectural — Important): The AOI "composition-handoff plan" is genuinely novel and needs more specification

The memo proposes that AOI planning should return a "bounded composition-handoff plan that names expected producer engines, required source families, and downstream compose prerequisites." This is a new object type that does not exist in the codebase today.

Currently, AOI composition uses:
- `composition_source_bridge.py` — resolves a source catalog from a job_id, applies a preset profile selector (dossier/comparison), materializes sections
- No planning step at all — the bridge goes straight from `source_v2_job_id + profile` to compose-ready sections

The memo's proposal would insert a planning layer before the bridge:

```
task envelope -> routing -> AOI composition-handoff plan -> (later: source bridge -> composition)
```

This is architecturally sound, but the memo does not specify:

1. What the composition-handoff plan actually contains beyond prose description ("expected producer engines, required source families, downstream compose prerequisites")
2. How it relates to the existing `CompositionSourceCatalog` and `CompositionSourceSelection` dataclasses in `composition_source_bridge.py`
3. Whether the plan is generated deterministically or via LLM
4. Whether it replaces the `profile` selector or sits above it

**Recommendation**: The memo should include a concrete schema sketch (even pseudocode-level) for the AOI composition-handoff plan to make the boundary testable.

---

## Finding 5 (Strategic — Important): The roadmap ordering skip should be acknowledged

The canonical roadmap (`MASTER_BIG_ROADMAP_MEMO`) defines Stages 3-6 as:
- Stage 3: AOI task-driven composition
- Stage 4: AOI engine/source-selection law
- Stage 5: AOI evaluation/ops guardrails
- Stage 6: Lifecycle decision

The actual execution order has been Stage 7 -> Stage 8 -> Stage 9, skipping 3-6 entirely.

The Stage 9 memo acknowledges this implicitly (it says "Stage 9 should not claim: planner-driven AOI profile selection" — which is Stage 3/4 territory). But it does not explicitly address why Stages 3-6 are being deferred in favor of 7-8-9.

The strongest argument would be: "Stages 7-9 build the bridge infrastructure that Stages 3-4 will later depend on, so building the bridge first is the right sequencing." The memo hints at this but should state it directly to prevent future reviewers from flagging the apparent skip as an oversight.

---

## Finding 6 (Proof/Evidence — Moderate): The proof standard is appropriately bounded but the genealogy proof case needs a feasibility check

The memo requires:

1. One genealogy task producing a real nontrivial execution-planning outcome
2. One AOI task producing a bounded composition-handoff planning outcome
3. One unsupported/ambiguous planning outcome

For case 1: generating a "real nontrivial execution-planning outcome" for genealogy requires calling the existing planner, which requires `OrchestratorPlanRequest` with thinker context. This loops back to Finding 1 — where does that context come from if the input is a task envelope?

**Options**:
- The proof uses a pre-populated task request with enough context for planning (but then it's not really testing the task-envelope-to-plan bridge)
- The proof demonstrates the plan contract shape without full LLM planning (a deterministic plan sketch from the task envelope)
- The proof requires the full host-provided analytical context alongside the task

The memo should clarify which of these the proof targets.

---

## Finding 7 (Codebase — Minor): Objective coverage is narrow and the memo should acknowledge this

Only 3 objectives exist in `src/objectives/definitions/`: `genealogical.json`, `influence_thematic.json`, `logical.json`. The Stage 8 task router only supports 2 (`influence_thematic`, `genealogical` — see `task_router.py:21`). The `logical` objective has no routing path.

Stage 9's "planner generalization" will therefore only cover 2 objective families. The memo should note this explicitly so the "generalization" claim is bounded honestly. The word "generalization" in the stage name could create false expectations about broader objective coverage.

---

## Finding 8 (Codebase — Minor): The `WorkflowExecutionPlan` docstring still says "genealogy workflow"

`src/orchestrator/schemas.py:428-433`:
```python
class WorkflowExecutionPlan(BaseModel):
    """A concrete, contextualized plan for executing a workflow.

    This is the orchestrator's primary output. It configures the existing
    5-phase genealogy pipeline with context-appropriate settings.
    """
```

If Stage 9 is about "planner generalization," this docstring is already misleading. The plan model itself is technically workflow-agnostic (it has `workflow_key`), but the documentation, field descriptions, and validation logic (`_validate_aoi_single_thinker_context`) still assume a narrow genealogy-or-AOI binary. This isn't a blocker for the memo, but the implementation planning should flag it.

---

## What the memo gets right

1. **The core diagnosis is correct**: There is a real gap between "which workflow family?" (Stage 8) and "what analytical plan?" (needed for composition). The code confirms this.

2. **The asymmetric outcome set is honest**: `genealogy_execution_plan` vs `aoi_composition_handoff_plan` vs `unsupported` reflects the actual codebase reality. Genealogy has a real planner; AOI has a source bridge with preset selectors.

3. **"Planner generalization, not invention" is the right framing**: The existing `adaptive_planner.py`, `catalog.py`, and objective definitions are real and substantial. Stage 9 should build on them.

4. **The composition handoff requirement is the real value-add**: Making the plan output say "what analytical products are expected" and "what source families later composition would depend on" is genuinely new and strategically important. Without this, the plan and the composition side remain disconnected.

5. **The exclusion list is well-calibrated**: No consumer adoption, no automatic dispatch, no fake unification, no AOI profile replacement, no Stage 10-12 claims.

6. **The "route-plus-plan, not execute" boundary is correct**: The memo is right to keep execution out of Stage 9.

---

## What must change before execution planning

1. **Confront the input-contract gap** (Finding 1): Specify how a lightweight task envelope becomes a planner-compatible request. This is the single most important revision.

2. **Address the 3-step advisory question** (Finding 2): Either justify the route-task -> plan-task separation or propose combining them.

3. **Specify the genealogy proof feasibility** (Finding 6): Clarify what "real nontrivial execution-planning outcome" means given the input-contract gap.

4. **Add a concrete AOI composition-handoff plan sketch** (Finding 4): Even pseudocode-level, to make the boundary testable.

5. **Acknowledge the roadmap ordering skip** (Finding 5): One sentence explaining why 7-8-9 before 3-6 is intentional.

---

## Perspective Docs

No relevant Perspective docs folder was found in analyzer-v2 or the-critic. This is consistent with the memo's own statement.

---

## Summary

The memo is strategically sound and identifies the right next seam. The diagnosis of what exists, what doesn't, and what the asymmetry looks like is grounded in code reality. The scope boundaries are disciplined. The main gap is the input-contract question: how does the lightweight advisory task envelope from Stage 8 get enriched enough to drive the existing planner substrate? Until the memo addresses that, the "reuse existing planner" story is aspirational rather than architecturally grounded. With the revisions above, this is ready for execution planning.
