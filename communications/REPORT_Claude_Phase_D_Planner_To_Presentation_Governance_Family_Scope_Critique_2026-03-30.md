# Report: Claude Review Of Phase D Planner-To-Presentation Governance Family Scope

Date: 2026-03-30
Reviewer: Claude (Opus 4.6)
Reviewed Memo: `communications/MEMO_2026-03-30_phase_d_planner_to_presentation_governance_family_scope.md`
Grounding Documents:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-30_phase_d_routing_planning_governance_family_v1_completion.md`
- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- Proof artifacts: `PROOF_phase_d_aoi_planning_decision_current_contract_2026-03-30.json`, `PROOF_phase_d_genealogy_direct_sections_planning_snapshot_2026-03-30.json`, `PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`, `PROOF_phase0_aoi_execution_backed_after_guard_recalibration_requests_2026-03-27.json`
- Code: `src/evaluations/frozen_pack_harness.py`, `src/evaluations/frozen_pack_definitions.py`, `src/evaluations/gate_definitions.py`, `src/evaluations/governance_status.py`

---

## Verdict: Approve With Revisions

The memo is strategically correct, honestly framed, and appropriately bounded. The revisions are implementation-level corrections, not strategic disagreements.

---

## What The Memo Gets Right

### 1. Strategic sequencing is correct

The memo correctly identifies the planner-to-presentation composition layer as the remaining open Phase D gap. The argument is sound:

- downstream result/lifecycle families are already governed
- standalone AOI and genealogy families exist
- one upstream routing/planning family exists
- governance does not yet reach the composition handoff that turns persisted planning truth into served presentation truth

This is the right next slice. The alternative candidates the memo explicitly rejects (another downstream family, another route/plan-only family, a premature Phase E jump) are all genuinely worse choices.

### 2. The Phase D / Phase E honesty boundary is well drawn

The memo is consistently honest about what this slice is and is not:

- it is retrospective governance over frozen proof artifacts
- it is not live governance over the current planner/presenter
- it does not justify a Phase E generality claim
- it does not pretend planner-to-presentation governance is broadly closed

This matches the distilled strategic roadmap's anti-drift rules, particularly Rule 3 ("do not confuse governance with architecture") and Rule 2 ("do not confuse bounded proof with generalized architecture").

### 3. The AOI honesty boundary is correctly stated

The memo correctly identifies that the existing March 27 AOI request proof (`PROOF_phase0_aoi_execution_backed_after_guard_recalibration_requests_2026-03-27.json`) is not a sufficient frozen subject by itself for this slice. That artifact carries `compose_from_selection` evidence but does not carry a persisted `planning_decision_id` on the same proof surface as the compose execution. Requiring one fresh current-contract transient compose bundle is honest.

### 4. The genealogy evidence reuse is defensible

The memo correctly identifies the Phase 2 transient proof trace (`PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`) as a multi-surface artifact that already carries planning, snapshot, lowered request, and compose-response evidence through nested JSON paths. The optional exported snapshot artifact for simpler evidence refs is a reasonable implementor affordance, not evidence inflation.

### 5. The evaluator family expansion is appropriately bounded

Adding `planner_presentation_decision` as a new evaluator branch is the honest implementation consequence of this scope. The harness currently hard-dispatches on `evaluator_key` at `frozen_pack_harness.py:152-176`, so this is structurally required. The four proposed dimensions are concrete and testable.

### 6. The out-of-scope list is right

The memo explicitly excludes live rerun governance, generic evaluator extensibility, UI/operator surfaces, downstream enforcement, and a claim that planner-to-presentation governance is broadly closed. These are the correct boundaries.

---

## Findings Requiring Revision

### Finding 1: The AOI compose-from-selection compose-response evidence does not exist yet — scope the capture explicitly

The memo says the fresh AOI bundle should contain "compose-from-selection request/response evidence." This is correct as an aspiration, but the scope should be explicit about what "fresh current-contract transient compose bundle" means operationally:

- It requires running a live AOI transient compose against the current contract (route → plan → snapshot → compose-from-selection)
- It requires capturing the planning_decision_id on the same proof surface
- It requires the compose response to carry a `resolver_version`, `view_count`, and compose trace

The memo should state this as an implementation prerequisite, not an assumption. If the live compose capture fails or the contract has drifted since the routing/planning proof was captured, the implementation must document that honestly rather than silently substituting the older March 27 request evidence.

**Recommendation**: Add one explicit implementation note stating that the AOI fresh bundle requires a live transient compose execution against the current code, not just a re-export of the planning artifacts already captured for the routing/planning slice.

### Finding 2: The proposed dimensions are concrete but the compose trace stage lists need verification

The memo proposes `composition_trace_integrity` checks against specific compose trace stages:

AOI:
- `source_catalog_resolution`, `source_selection`, `section_materialization`, `semantic_surface_matching`, `hierarchy_planning`, `page_plan`, `view_generation`, `transformation_execution`, `consumer_adaptation`, `contract_validation`

Genealogy:
- `semantic_surface_matching`, `hierarchy_planning`, `page_plan`, `view_generation`, `transformation_execution`, `consumer_adaptation`, `contract_validation`

I verified these against the existing compose-from-intent implementation (`src/presenter/compose_from_intent.py`) and the compose-from-selection route (`src/api/routes/presenter.py`). The stage names are plausible but they are the *expected* stage names based on the trace structure of prior proof artifacts. The actual compose trace structure in current code may differ — compose traces are assembled dynamically by the presenter pipeline, and trace stage names are not guaranteed stable across code changes.

**Recommendation**: The evaluator should validate trace stage *presence* (are expected stages present?), not trace stage *exhaustiveness* (are only these stages present?). The memo should state explicitly that the compose trace check is an inclusion check, not an exact-match check. This aligns with the memo's own principle: "The evaluator should judge retrospective artifacts by internal agreement against the declared case contract. It should not fail a historical artifact merely because later code evolved after the artifact was captured."

### Finding 3: The `planner_presentation_agreement` dimension for AOI needs one clarification

The memo says the AOI case must show agreement on:
- `source_v2_job_id`
- selected thinker identity
- AOI workflow identity at the served presentation
- consumer identity at the served presentation

This is correct, but the memo should specify *which artifact carries each field*. In the routing/planning evaluator, the implementation maps fields to specific artifact slots (e.g., `route_artifact.get("selected_objective_key")` vs `planning_artifact.get("routing_decision", {}).get("selected_objective_key")`). The planner-to-presentation evaluator will need similar explicit mappings:

- planning handoff: carries `source_v2_job_id`, `selected_source_thinker_id`, `workflow_key`, `consumer_key`
- compose request: carries `source_v2_job_id`, `workflow_key`, `consumer_key`, and (for AOI) `selection` with thinker identity
- compose response: carries `workflow_key`, `consumer_key`, `resolver_version`, trace

Without this mapping, the implementor has latitude to check the wrong fields or skip fields that are in different artifact locations.

**Recommendation**: Add a brief note (can be a table or bullet list) mapping which artifact is authoritative for which agreement field. This is not scope creep — it prevents the evaluator from drifting into a vague "things generally agree" check.

### Finding 4: The `handoff_contract_fidelity` dimension should specify which compose entrypoint field carries the handoff kind

For the AOI case, the memo says:
- `aoi_composition_handoff_plan.compose_entrypoint_kind = presenter.compose_from_selection`

For the genealogy case, the memo says:
- `downstream_followup_contract.handoff_kind = direct_sections`

These are checking two different structural locations. That asymmetry is honest (the two workflows have genuinely different handoff shapes), but the evaluator code should validate both pathways explicitly rather than having a generic "check compose_entrypoint_kind" that accidentally only works for one case.

**Recommendation**: The memo should note this asymmetry explicitly as an implementation guide, similar to how the routing/planning completion memo documented the AOI/genealogy evidence extraction asymmetry.

### Finding 5: Minor — the `presentation_contract_fidelity` dimension's `view_count` check needs a source for the expected count

The memo says:
- `presentation.view_count == len(generated_view_definitions)`

But `generated_view_definitions` is an internal compose artifact, not a field that appears in the public compose response by that name. The implementor needs to know where the expected view count comes from. In practice, the compose response carries a `presentation` object with `views` or `view_definitions` whose length can be counted. The evaluator should check that the compose response's view array length matches the compose trace's view_generation stage output.

**Recommendation**: Clarify the source of the expected count — is it `len(response.presentation.views)` vs `len(response.presentation.generated_view_definitions)` vs a trace-reported count?

---

## Strategic Assessment Questions

### 1. Is this the right next Phase D slice, or is it drifting?

**It is the right next Phase D slice.** The governance gap over planner-to-presentation composition is real and specifically named in the distilled roadmap's Phase D "still missing" section and in the routing/planning completion memo's "not yet true" section. This is not lateral drift — it directly addresses the next named open question.

The anti-drift filter passes clearly:
- Does this move intelligence upstream into analyzer-v2? Yes — it governs the composition layer that turns planning truth into presentation truth.
- Does this reduce host-specific analytical behavior? Not directly, but it makes the composition handoff reviewable and inspectable.
- Does this strengthen generic law rather than one more special case? Moderately — it extends governance to a new layer (composition) rather than repeating governance over the same layer.
- Does this help eventual contract-based generality? Yes — it creates accountability over the handoff that will matter most when the system generalizes.

### 2. Is the memo honest about the distinction between retrospective planner-to-presentation governance and Phase E generality proof?

**Yes, entirely honest.** The memo draws the line clearly in multiple places:
- "This is still Phase D work."
- "It is still retrospective governance over frozen proof artifacts, not live governance over the current planner/presenter."
- "It still does not justify saying Phase D is closed" or "Phase E is complete."
- The honest expected outcome explicitly says it would still not justify arbitrary engine/pass composition generality.

### 3. Are the codebase claims and proof-surface claims accurate?

**Mostly accurate, with minor corrections noted above.** The codebase currently has:
- Three evaluator branches in `frozen_pack_harness.py` (lines 152-176): `aoi_exemplar`, `genealogy_lifecycle`, `routing_planning_decision` — confirmed
- Four frozen pack definitions in `frozen_pack_definitions.py` — confirmed
- Four gate definitions in `gate_definitions.py` — confirmed
- Unchanged governance-status derivation in `governance_status.py` — confirmed
- The routing/planning evaluator uses `_RoutingPlanningCaseSpec` and `_RoutingPlanningCaseEvidence` patterns that the new evaluator can follow — confirmed

The proof artifact claims are accurate:
- `PROOF_phase_d_aoi_planning_decision_current_contract_2026-03-30.json` exists and carries a fresh `planning_decision_id = planning-decision-1b0dbef41b28` with `planning_outcome_kind = aoi_composition_handoff_plan` and `downstream_followup_contract.endpoint = /v1/presenter/compose-from-selection` — confirmed
- `PROOF_phase_d_genealogy_direct_sections_planning_snapshot_2026-03-30.json` exists and carries `planning-decision-b1600d054991` with `direct_sections_composition_handoff_plan` — confirmed
- `PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json` exists as a multi-surface artifact — confirmed

### 4. Is the proposed `planner_presentation_decision` evaluator-family expansion appropriately bounded?

**Yes.** Four dimensions is appropriately narrow. The routing/planning evaluator used the same four-dimension pattern (`route_fidelity`, `source_contract_fidelity`, `planning_followup_fidelity`, `decision_trace_integrity`). The new family uses a structurally parallel set (`handoff_contract_fidelity`, `planner_presentation_agreement`, `presentation_contract_fidelity`, `composition_trace_integrity`). This is consistent and bounded.

The one concern is that the composition-layer checks are inherently more complex than route/plan checks because the compose response is larger and more nested. The scope should resist the temptation to make the composition_trace_integrity check exhaustive — an inclusion check on expected stages is sufficient for retrospective governance.

### 5. Is one fresh AOI current-contract transient compose bundle the smallest honest AOI evidence path?

**Yes, and the memo is right that the March 27 request proof is not sufficient by itself.** The March 27 artifact (`PROOF_phase0_aoi_execution_backed_after_guard_recalibration_requests_2026-03-27.json`) records `compose_from_selection` request/response data, but it does not carry a `planning_decision_id` because it was captured on the AOI hot-path flow before the immutable planning-decision persistence was part of the contract. Since this evaluator is specifically about planner-to-presentation governance, requiring a `planning_decision_id`-scoped AOI proof is the honest minimum.

### 6. Is there a smaller or cleaner next step that would better serve the program?

**No.** The alternatives are:
- Another downstream family variation → already well-covered, no new strategic question answered
- Another route/plan-only family → already covered by the routing/planning slice
- Jump to Phase E → premature; composition governance is the last meaningful Phase D gap
- Skip governance entirely and pivot to generality proof → would leave the composition layer unaccountable

This slice is the right size and the right question.

---

## Summary Of Required Revisions

| # | Finding | Severity | Action |
|---|---------|----------|--------|
| 1 | AOI fresh bundle requires live compose execution, not re-export | Medium | Add explicit implementation note |
| 2 | Compose trace stage checks should be inclusion-only, not exact-match | Medium | State explicitly in evaluator criteria |
| 3 | `planner_presentation_agreement` needs artifact-to-field mapping | Low | Add brief field mapping table |
| 4 | Handoff contract field asymmetry between AOI/genealogy needs explicit note | Low | Document the asymmetry |
| 5 | `view_count` check source needs clarification | Low | Specify which field carries expected count |

None of these revisions change the strategic direction or the Phase D framing. They are implementor-guidance corrections that prevent the evaluator from being accidentally vague or from silently substituting weaker evidence.

---

## Verdict Rationale

**Approve with revisions** because:

1. The strategic framing is correct — this is the right next Phase D slice
2. The Phase D / Phase E boundary is honestly drawn
3. The out-of-scope boundaries are right
4. The evaluator family expansion is appropriately bounded
5. The codebase claims are accurate
6. The required revisions are implementation-level, not strategic

The memo should incorporate the five corrections above before the implementor begins. None require a re-scope or a different strategic direction.
