# Critique: Phase D Routing/Planning Governance Family Scope

Date: 2026-03-30
Reviewer: Claude (Opus 4.6)
Subject: `communications/MEMO_2026-03-30_phase_d_routing_planning_governance_family_scope.md`

## Verdict: Approve With Revisions

The proposed slice is strategically coherent and directionally correct within the Phase D governance line. It is the right *kind* of next step. But the memo overstates what is being proven, and one structural implementation gap needs addressing before the slice is executed.

---

## What The Memo Gets Right

### 1. Strategic placement is sound

The memo correctly identifies the remaining Phase D gap. After three governance families (composite, genealogy-standalone, AOI-standalone), the governance stack has only been exercised over downstream frozen result/lifecycle evidence. Extending it to upstream routing/planning decision surfaces is a genuine qualitative broadening, not another variation on the same substrate. This follows the distilled roadmap's anti-drift rules honestly.

### 2. Honest Phase D / Phase E boundary

The memo is explicit and disciplined about not claiming this enters Phase E. It states clearly: "it is still retrospective and bounded" and "it is still not the Phase E generality proof." This is the right posture. The repeated disclaimers may feel excessive, but given the program's history of scope-drift through ambiguous completion claims, the explicitness is warranted.

### 3. Scope is genuinely bounded

One pack, two cases, four dimensions, one gate/review/resolution chain. The out-of-scope list is clear and appropriate. The proposed evaluator family does not attempt to cover arbitrary planning tasks or live rerun policy. This is a well-scoped slice.

### 4. Evidence artifacts exist

The four specific proof artifacts referenced in the memo all exist on disk:

- `communications/PROOF_stage8_aoi_route_decision_2026-03-23.json`
- `communications/PROOF_stage9_aoi_handoff_plan_decision_2026-03-23.json`
- `communications/PROOF_stage8_genealogy_by_ref_route_decision_2026-03-23.json`
- `communications/PROOF_stage9_genealogy_by_ref_plan_decision_2026-03-23.json`

These are real Stage 8/9 decision snapshots, not placeholders.

### 5. Reuse of existing governance substrate

The proposal correctly plans to reuse the existing report/gate/review/resolution/status infrastructure without new route shapes, new persisted governance object types, or new builder/store semantics. This is the right approach -- it tests whether the governance substrate is genuinely generic by feeding it a qualitatively different evidence class.

---

## Concrete Findings And Revisions Required

### Finding 1: The harness currently hard-dispatches on evaluator_key (implementation gap)

**Severity: Must address in implementation plan**

The frozen pack harness (`src/evaluations/frozen_pack_harness.py:77-93`) currently dispatches on exactly two evaluator keys:

```python
if case_definition.evaluator_key == "aoi_exemplar":
    return _evaluate_aoi_case(...)
if case_definition.evaluator_key == "genealogy_lifecycle":
    return _evaluate_genealogy_case(...)
raise ValueError(f"Unknown evaluator_key: {case_definition.evaluator_key}")
```

The proposed `routing_planning_decision` evaluator key will require a *new evaluation branch* with its own logic. The memo says the evaluator should "reuse the current report substrate" with "per-check evidence refs" and "thin persisted reports," which is true at the report/gate/review/resolution layer. But the *evaluation logic itself* -- the part that reads the frozen artifacts and produces dimension-level check results -- must be entirely new.

This is not a problem with the proposal. It is a predictable implementation detail. But the memo should acknowledge that the harness needs a new `_evaluate_routing_planning_case(...)` function, and that this is the actual new code in this slice -- not just new definitions.

### Finding 2: The framing slightly overstates what is being governed

**Severity: Revision recommended**

The memo frames this as "governance over upstream routing/planning decision surfaces." That language implies governance sits *on top of* the routing/planning code paths themselves -- evaluating whether the router and planner behave correctly.

What is actually being proposed is governance over *frozen snapshots of recorded routing/planning decision outputs* from the March 23 Stage 8/9 proof campaign. The evidence artifacts are JSON files in `communications/` that captured routing decisions and planning decisions at a point in time.

This is an important distinction. The frozen artifacts were captured against an older version of the router code. For example:

- The Stage 8 AOI proof artifact uses `launch_contract_kind: "presenter.compose_from_source"` (March 23 code)
- The current `task_router.py` code emits `launch_contract_kind: "planner.aoi_compose_handoff"` for the same routing outcome

The evaluator must assess the *internal consistency and completeness of the frozen decision*, not whether it matches the current code. The memo's dimension keys (`route_fidelity`, `source_contract_fidelity`, `planning_handoff_fidelity`, `decision_trace_integrity`) are appropriate for that narrower assessment. But the memo should state explicitly that:

- This is retrospective frozen governance over recorded decision artifacts, not live governance over routing/planning behavior
- The evaluation dimensions assess internal decision consistency, not correspondence to current code state
- The artifacts predate code evolution since March 23

This does not invalidate the slice. It sharpens the honest claim.

### Finding 3: The four dimension keys need clearer definitions

**Severity: Should be addressed in scope or implementation**

The memo proposes four dimensions:

- `route_fidelity`
- `source_contract_fidelity`
- `planning_handoff_fidelity`
- `decision_trace_integrity`

These are named but not defined. The existing evaluators have implicit definitions baked into their check logic. The new evaluator will need explicit criteria for what constitutes "pass" vs "fail" on each dimension, because the evidence shape (routing/planning decision JSON) is structurally different from executor job state or compose session state.

The memo should either:

(a) Include brief dimension definitions (2-3 sentences each), or
(b) Explicitly defer dimension definitions to the implementation while acknowledging this is a design decision still to be made.

### Finding 4: No strategic disagreement with the distilled roadmap

**Severity: Confirming alignment**

Checked against the distilled roadmap's anti-drift rules:

1. *Prefer upstream intelligence over downstream convenience* -- This slice governs upstream decision artifacts. Passes.
2. *Do not confuse bounded proof with generalized architecture* -- The memo is explicit about boundedness. Passes.
3. *Do not confuse governance with architecture* -- This is the most relevant rule. The memo does not claim that governance over routing/planning decisions creates or substitutes for planner generality. It explicitly defers Phase E. Passes, with the caveat in Finding 2.
4. *Prefer representative matrices over exhaustive workflow theater* -- Two cases (AOI + genealogy) across the routing/planning surface is a minimal matrix broadening. Passes.

---

## Questions Answered

### 1. Is this the right next Phase D slice, or is it drifting?

It is the right next Phase D slice. The three existing families all govern downstream result/lifecycle evidence. Moving governance to upstream decision surfaces is the natural next broadening before Phase D can be considered materially complete. This is not drift -- it is the gap the distilled roadmap already identified.

### 2. Is the memo honest about Phase D governance progress vs Phase E generality proof?

Yes. The memo is explicit and repeatedly careful about this distinction. The honest expected outcome section correctly states what the slice does and does not justify claiming afterward. The only overstatement risk is the "upstream decision surfaces" framing discussed in Finding 2.

### 3. Are the codebase claims accurate?

Mostly accurate with one important nuance:

- **Accurate**: The evidence artifacts exist. The governance substrate (packs, gates, reviews, resolutions, governance status) exists and works as described. The task router and task planner code exist.
- **Nuance**: The memo implies the governance infrastructure will absorb the new family without new code, but the harness requires a new evaluator branch (Finding 1). The definition layers (pack, gate, review, resolution) will indeed be pure declaration, but the evaluation logic itself is new.

### 4. Is the proposed evaluator-family expansion appropriately bounded?

Yes. One new evaluator key, one new pack with two cases, four narrow dimensions. The expansion is minimal. The risk is not scope creep -- it is under-specification of what the dimension checks actually verify (Finding 3).

### 5. Is there a smaller or cleaner next step that would better serve the program?

No. The current three families are all variations on the same evidence class (downstream frozen results/lifecycle). The smallest meaningful broadening is exactly what this memo proposes: one family over a different evidence class. A smaller step would be another variation on the same substrate, which the memo correctly identifies as less valuable.

The one alternative worth noting: the program could instead pivot directly to Phase E and defer this slice. The distilled roadmap says governance should become "mature enough" before Phase E, and three families might already meet that bar. But the qualitative improvement of demonstrating governance over upstream decision surfaces is genuine and strengthens the Phase D exit claim. On balance, executing this slice before Phase E is justified.

---

## Summary Of Revisions

1. **Must**: Acknowledge in the scope or implementation plan that the frozen pack harness requires a new `_evaluate_routing_planning_case(...)` branch -- this is the actual new code, not just new declarations.
2. **Should**: Sharpen the "upstream decision surfaces" framing to explicitly state this is retrospective governance over frozen decision artifacts from the March 23 proof campaign, not live governance over current routing/planning behavior.
3. **Should**: Provide brief dimension definitions for the four proposed evaluation dimensions, or explicitly defer them to implementation.
4. **May**: Note that the frozen artifacts predate code evolution (e.g., `launch_contract_kind` has changed since March 23) and that the evaluator should assess internal decision consistency rather than correspondence to current code.

---

## Bottom Line

The slice is directionally correct, well-bounded, and strategically justified. It broadens the governance substrate in a qualitatively meaningful way without pretending to enter Phase E. The revisions above are implementation and honesty refinements, not strategic disagreements. Execute with the clarifications noted.
