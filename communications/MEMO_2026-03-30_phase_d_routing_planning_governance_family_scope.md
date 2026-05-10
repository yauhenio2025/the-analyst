# Memo: Phase D Routing/Planning Governance Family Scope

Subtitle: The first governance family over upstream analyzer-owned decision surfaces

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase_d_aoi_standalone_governance_family_v1_completion.md`

## Purpose

Define the next bounded governance step after standalone coverage now exists across the two currently supported evaluator substrates.

On the distilled roadmap, we are still:

- late in `Phase D: Governance And Accountability`

But the active question has changed.

The next slice should therefore strengthen Phase D honestly without pretending we have already moved into:

- `Phase E: Generality Proof`

## Strategic Framing

The standalone AOI family completion means the governance stack now has:

- one composite AOI-plus-genealogy family
- one standalone genealogy-only family
- one standalone AOI-only family

So the remaining open Phase D problem is no longer:

- standalone coverage across the two currently supported evaluator substrates

The remaining open Phase D problem is:

- governance still sits mainly over bounded frozen AOI/genealogy result and lifecycle evidence from the current proving line
- governance still does not sit over upstream analyzer-owned routing/planning/composition decision surfaces

That is why the next honest Phase D move is not:

- another frozen-family variation on the same current evaluator substrates

It is:

- one bounded governance family over upstream routing/planning decision surfaces

This is still Phase D work.
It is still governance.
It is still retrospective governance over frozen upstream decision artifacts, not live governance over the current router/planner.
It is still not the broader Phase E “arbitrary engine/pass composition” proof.

## Why This Is The Right Next Phase D Slice

Analyzer-v2 already has real upstream decision substrate in repo:

- task routing
- task planning
- immutable planning-decision persistence
- existing Stage 8 and Stage 9 proof artifacts

And the current Stage 15 gap is already named in the roadmap boundary:

- there is still no broader routing/planning/composition governance family beyond the current frozen proving-campaign surfaces

So the cleanest next bounded step is:

- govern one bounded upstream routing/planning family using the already-landed report/gate/review/resolution/status substrate

That advances the strategic question directly:

- can governance sit on top of upstream analyzer-owned decision objects, not just downstream result/lifecycle proof bundles?

One implementation consequence should be named explicitly:

- this slice is not definition-only
- `src/evaluations/frozen_pack_harness.py` currently hard-dispatches only `aoi_exemplar` and `genealogy_lifecycle`
- the new family therefore requires one new bounded evaluator branch:
  - `routing_planning_decision`

## Scope Decision

### In scope

#### 1. One new upstream frozen governance pack

Add one new pack definition over retrospective upstream routing/planning decision artifacts.

Recommended identity:

- `evaluation_pack_key = phase4_routing_planning_governance_v1`

Recommended evaluator family:

- `evaluator_key = routing_planning_decision`

Default bounded cases:

- `aoi_saved_result_handoff_current_contract`
  - route evidence:
    - one fresh AOI `route-task` artifact captured under the current `planner.aoi_compose_handoff` contract
  - planning evidence:
    - one fresh AOI `plan-task(persist_decision=true)` artifact captured under the current contract
  - snapshot evidence:
    - one fresh persisted planning snapshot artifact for that same AOI decision
- `genealogy_saved_result_direct_sections_snapshot_march28`
  - route and planning evidence:
    - `PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`
  - snapshot evidence:
    - `src/orchestrator/planning_decisions/planning-decision-b1600d054991.json`

The point of those two cases is not exhaustiveness.
It is one bounded cross-objective governance family over upstream route-plus-plan decision surfaces.

Explicit exclusions:

- do not treat `PROOF_stage8_aoi_route_decision_2026-03-23.json` plus `PROOF_stage9_aoi_handoff_plan_decision_2026-03-23.json` as current-contract AOI truth
  - the March 23 AOI route artifact still carries the older `presenter.compose_from_source` contract
- do not treat a Stage 9 plan JSON by itself as persisted-snapshot evidence
  - any case that claims planning-snapshot governance must carry an explicit snapshot artifact

#### 2. One bounded upstream evaluator family

Add one evaluator family under the existing frozen-pack harness for those new cases:

- `routing_planning_decision`

It should stay narrow and deterministic.

It should validate, per case:

- route/objective/workflow fidelity
- source-contract fidelity
- planning outcome and downstream followup fidelity
- upstream decision-trace integrity

Recommended dimension keys:

- `route_fidelity`
- `source_contract_fidelity`
- `planning_followup_fidelity`
- `decision_trace_integrity`

Minimum bounded criteria:

- `route_fidelity`
  - selected objective, workflow, routing outcome, and launch/followup contract kind are internally consistent with the declared case
- `source_contract_fidelity`
  - source sufficiency, required fields, host preparation, and source identity requirements are internally coherent for that route/planning mode
- `planning_followup_fidelity`
  - planning outcome kind and downstream followup contract are internally coherent for the case, whether the case is composition-handoff or execution-followup
- `decision_trace_integrity`
  - required trace stages are present, and when a persisted planning snapshot is part of the case evidence, the snapshot agrees with the route/planning decision without contradiction

The evaluator should reuse the current report substrate:

- per-check evidence refs
- thin persisted reports
- frozen-artifact honesty where evidence is retrospective

The evaluator should judge retrospective artifacts by internal decision consistency against the declared case contract.
It should not fail a historical artifact merely because later code evolved after that artifact was captured.

#### 3. One bounded gate/review/resolution chain

Add one governance family over that pack:

- `gate_key = bounded_routing_planning_readiness_v1`
- `review_key = bounded_routing_planning_review_v1`
- `resolution_key = bounded_routing_planning_resolution_v1`

The gate should require both cases and all four upstream dimensions.

The review and resolution layers should reuse the current bounded laws unchanged:

- review remains bounded `accept / reject / waive`
- resolution remains recording-only in v1
- currentness remains analyzer-owned over:
  - `resolution_key + gate_decision_id`

#### 4. One real upstream governance chain

Materialize one real routing/planning governance chain using the existing builders and routes after the new evaluator family lands:

- one report per upstream case
- one routing/planning gate
- one routing/planning review
- one routing/planning resolution
- one semantic current-governance-status read through the unchanged route

The value of the slice should be stated honestly:

- this is the first governance family over upstream analyzer-owned decision surfaces
- it is stronger than another downstream frozen-family variation
- it is still retrospective and bounded
- it may require one fresh AOI current-contract route/plan/snapshot evidence bundle as part of the slice because the older March 23 AOI proof artifacts are contract-stale
- it is still not the Phase E generality proof

### Out of scope

- broad live rerun governance
- generic evaluator extensibility claims
- UI or operator product surfaces
- downstream enforcement or unlock/deny behavior
- pack-global or gate-global current-governance law
- arbitrary planning-task coverage
- a claim that routing/planning governance is now broadly closed

## Anti-Drift Justification

This slice passes the distilled roadmap’s anti-drift rules because:

1. it strengthens analyzer-owned governance over upstream decision surfaces rather than host behavior
2. it builds on already-landed routing/planning substrate instead of reopening AOI-local proof loops
3. it broadens governance beyond current frozen result/lifecycle families
4. it moves closer to the real “analyzer-v2 is the brain” architecture question without pretending to close it

## Honest Expected Outcome

If this slice lands cleanly, the honest claim afterward should be:

- analyzer-v2 governance now covers:
  - downstream AOI/genealogy result and lifecycle families
  - one upstream routing/planning decision family
- the governance substrate is no longer only a proving-campaign wrapper around current result/lifecycle evidence

But it would still not justify saying:

- Phase D is automatically closed
- Phase E is complete
- analyzer-v2 has already proven arbitrary engine/pass composition generality
- broad live governance policy is solved

## Decision

The next bounded strategic step should be:

- one routing/planning governance family over bounded upstream route/plan/snapshot proof surfaces, using fresh current-contract AOI evidence where needed and existing genealogy snapshot evidence where already sufficient

That is the cleanest next Phase D move after standalone AOI coverage, because it tests governance on upstream analyzer-owned decision objects rather than on yet another variation of the same downstream frozen evidence line.
