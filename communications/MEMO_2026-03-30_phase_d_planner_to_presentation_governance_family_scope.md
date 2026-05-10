# Memo: Phase D Planner-To-Presentation Governance Family Scope

Subtitle: The first governance family over upstream planner-to-presentation composition decision surfaces

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
- `communications/MEMO_2026-03-30_phase_d_routing_planning_governance_family_v1_completion.md`
Relevant Prior Proof Line:
- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`

## Purpose

Define the next bounded governance step after the routing/planning governance family.

On the distilled roadmap, we are still:

- in `Phase D: Governance And Accountability`

The next slice should keep strengthening analyzer-owned governance honestly without pretending we have already moved into:

- `Phase E: Generality Proof`

## Strategic Framing

The routing/planning governance completion means the governance stack now has:

- one composite AOI-plus-genealogy family
- one declared genealogy-only family
- one declared AOI-only family
- one broader upstream routing/planning governance family over frozen analyzer-owned decision artifacts

So the remaining open Phase D question is no longer:

- whether governance can sit over upstream route/plan artifacts at all

The remaining open Phase D question is:

- whether governance can also sit over the planner-to-presentation composition layer rather than stopping at route/plan decisions

That is why the next honest Phase D move is not:

- another downstream frozen-family variation
- another route/plan-only family
- a premature jump to generic evaluator extensibility or Phase E generality claims

It is:

- one bounded governance family over upstream planner-to-presentation composition decision surfaces

This is still Phase D work.
It is still retrospective governance over frozen proof artifacts, not live governance over the current planner/presenter.
It is still not the broader “arbitrary engine/pass composition” proof.

## Why This Is The Right Next Phase D Slice

Analyzer-v2 already has the relevant substrate in repo:

- immutable planning-decision persistence
- analyzer-owned planner handoff models
- analyzer-owned presenter composition routes
- one AOI `compose-from-selection` proof line
- one genealogy `compose-from-intent` proof line

And the current Phase D gap is now narrower:

- governance reaches downstream result/lifecycle families
- governance reaches standalone AOI and genealogy families
- governance reaches one upstream routing/planning family
- but governance still does not reach the composition handoff and composed-presentation surfaces that sit between planner truth and served presentation truth

So the cleanest next bounded step is:

- govern one bounded planner-to-presentation family using the already-landed report/gate/review/resolution/status substrate

That advances the strategic question directly:

- can governance stand over the handoff and composition layer that actually turns persisted planning truth into served presentation truth?

One implementation consequence should be named explicitly:

- this slice is not definition-only
- `src/evaluations/frozen_pack_harness.py` currently hard-dispatches only:
  - `aoi_exemplar`
  - `genealogy_lifecycle`
  - `routing_planning_decision`
- the new family therefore requires one new bounded evaluator branch:
  - `planner_presentation_decision`

## Scope Decision

### In scope

#### 1. One new upstream frozen governance pack

Add one new pack definition over retrospective planner-to-presentation composition artifacts.

Recommended identity:

- `evaluation_pack_key = phase4_planner_to_presentation_governance_v1`

Recommended evaluator family:

- `evaluator_key = planner_presentation_decision`

Default bounded cases:

- `aoi_compose_selection_current_contract`
  - `subject_kind = planning_decision`
  - `subject_identity = <fresh AOI planning_decision_id from the exported transient compose proof bundle>`
  - `workflow_key = anxiety_of_influence_thematic_single_thinker`
  - `consumer_key = the-critic`
  - frozen artifacts in `communications/`:
    - one fresh current-contract AOI transient compose proof bundle captured from a live transient compose execution and containing:
      - route evidence
      - planning evidence
      - persisted planning snapshot evidence
      - `compose-from-selection` request/response evidence
    - that AOI bundle must tie the persisted `planning_decision_id` to the `compose-from-selection` request/response on the same frozen proof surface
- `genealogy_direct_sections_compose_snapshot_march28`
  - `subject_kind = planning_decision`
  - `subject_identity = planning-decision-b1600d054991`
  - `workflow_key = intellectual_genealogy`
  - `consumer_key = the-critic`
  - frozen artifacts in `communications/`:
    - existing multi-surface transient proof:
      - `PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`
    - optional explicit exported snapshot support artifact if needed for simpler evidence refs:
      - `PROOF_phase_d_genealogy_direct_sections_planning_snapshot_2026-03-30.json`

Important implementation rules:

- do not point frozen pack artifacts at `src/orchestrator/planning_decisions/*.json`
- keep frozen evidence `communications/`-scoped and hash-pinned
- do not build a generic proof-capture framework for this slice
- capture the fresh AOI transient compose bundle once, commit it, and pin hashes
- the AOI bundle must come from a real live transient compose execution, not from re-exporting only the already-captured March 30 planning artifacts

Important AOI honesty boundary:

- the existing March 27 AOI request proof remains useful context
- but it is not a sufficient frozen subject by itself for this slice because it does not carry a stable persisted `planning_decision_id` on the same proof surface as the compose execution
- the required AOI evidence path is therefore one fresh current-contract transient compose bundle with a persisted planning identity

Important genealogy honesty boundary:

- the genealogy trace artifact is a multi-surface artifact
- it supplies planning, snapshot, lowered request, and compose-response evidence through nested JSON paths
- the optional exported snapshot artifact exists only to keep evidence refs simpler and more explicit if needed
- AOI and genealogy therefore have real proof-shape asymmetry at the handoff seam:
  - AOI should be governed from one fresh dedicated transient compose bundle anchored to a persisted planning identity
  - genealogy can be governed from the existing multi-surface transient trace plus optional exported snapshot support

#### 2. One bounded planner-to-presentation evaluator family

Add one evaluator family under the existing frozen-pack harness:

- `planner_presentation_decision`

It should stay narrow and deterministic.

It should validate, per case:

- handoff-contract fidelity
- planner-to-presentation agreement
- presentation-contract fidelity
- composition-trace integrity

Recommended dimension keys:

- `handoff_contract_fidelity`
- `planner_presentation_agreement`
- `presentation_contract_fidelity`
- `composition_trace_integrity`

Minimum bounded criteria:

- `handoff_contract_fidelity`
  - AOI case must show:
    - `planning_outcome_kind = aoi_composition_handoff_plan`
    - `downstream_readiness = ready_for_aoi_compose_handoff`
    - `downstream_followup_contract.endpoint = /v1/presenter/compose-from-selection`
    - `aoi_composition_handoff_plan.compose_entrypoint_kind = presenter.compose_from_selection`
  - genealogy case must show:
    - `planning_outcome_kind = direct_sections_composition_handoff_plan`
    - `downstream_readiness = ready_for_direct_sections_compose_handoff`
    - `downstream_followup_contract.endpoint = /v1/presenter/compose-from-intent`
    - `downstream_followup_contract.handoff_kind = direct_sections`

Implementation guidance for handoff asymmetry:

- the AOI compose-entrypoint signal is checked at:
  - `aoi_composition_handoff_plan.compose_entrypoint_kind`
- the genealogy handoff-mode signal is checked at:
  - `planning_decision.downstream_followup_contract.handoff_kind`
- do not force those two structural locations into one artificial shared path in this slice

- `planner_presentation_agreement`
  - AOI case must show the planning handoff, compose request, and composed presentation agree on:
    - `source_v2_job_id`
    - selected thinker identity
    - AOI workflow identity at the served presentation
    - consumer identity at the served presentation
  - genealogy case must show the planning snapshot, lowered compose request, and composed presentation agree on:
    - `planning_decision_id`
    - `workflow_key`
    - `consumer_key`
    - direct-sections composition path

Artifact-to-field authority for the agreement dimension should be explicit:

- AOI case:
  - planning identity and handoff truth come from the fresh AOI transient compose proof bundle's persisted planning snapshot/decision surface
  - compose-request truth comes from that same bundle's `compose-from-selection` request payload
  - served-presentation truth comes from that same bundle's `compose-from-selection` response payload
- genealogy case:
  - planning identity and snapshot truth come from `PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`
    - and optionally the exported March 30 snapshot artifact for simpler direct refs
  - lowered-request truth comes from the same Phase 2 transient trace
  - served-presentation truth comes from the same Phase 2 transient trace

- `presentation_contract_fidelity`
  - AOI case must show:
    - composed presentation `workflow_key = anxiety_of_influence_thematic_single_thinker`
    - composed presentation `consumer_key = the-critic`
    - `resolver_version = compose-from-selection-v1`
    - `compose response presentation.view_count == len(compose response generated_view_definitions)`
  - genealogy case must show:
    - composed presentation `workflow_key = intellectual_genealogy`
    - composed presentation `consumer_key = the-critic`
    - `resolver_version = compose-from-intent-v2`
    - `compose response presentation.view_count == len(compose response generated_view_definitions)`

- `composition_trace_integrity`
  - AOI compose trace must include at least:
    - `source_catalog_resolution`
    - `source_selection`
    - `section_materialization`
    - `semantic_surface_matching`
    - `hierarchy_planning`
    - `page_plan`
    - `view_generation`
    - `transformation_execution`
    - `consumer_adaptation`
    - `contract_validation`
  - genealogy compose trace must include at least:
    - `semantic_surface_matching`
    - `hierarchy_planning`
    - `page_plan`
    - `view_generation`
    - `transformation_execution`
    - `consumer_adaptation`
    - `contract_validation`

Trace checks in this slice are inclusion-only:

- require the expected stages to be present
- do not require an exact stage list match
- do not fail a historical proof merely because later implementations emitted additional trace entries

The evaluator should reuse the current report substrate:

- per-check evidence refs
- thin persisted reports
- frozen-artifact honesty where evidence is retrospective

The evaluator should judge retrospective artifacts by internal agreement against the declared case contract.
It should not fail a historical artifact merely because later code evolved after the artifact was captured.

#### 3. One bounded gate/review/resolution chain

Add one governance family over that pack:

- `gate_key = bounded_planner_to_presentation_readiness_v1`
- `review_key = bounded_planner_to_presentation_review_v1`
- `resolution_key = bounded_planner_to_presentation_resolution_v1`

The gate should require both cases and all four planner-to-presentation dimensions.

The review and resolution layers should reuse the current bounded laws unchanged:

- review remains bounded `accept / reject / waive`
- resolution remains recording-only in v1
- currentness remains analyzer-owned over:
  - `resolution_key + gate_decision_id`

The existing semantic seam should serve the new family unchanged:

- `GET /v1/evaluations/governance-status/current`

#### 4. One real planner-to-presentation governance chain

Materialize one real planner-to-presentation governance chain using the existing builders and routes after the new evaluator family lands:

- one report per upstream case
- one planner-to-presentation gate
- one planner-to-presentation review
- one planner-to-presentation resolution
- one semantic current-governance-status read through the unchanged route

The value of the slice should be stated honestly:

- this is the first governance family over upstream planner-to-presentation composition decision surfaces
- it is stronger than another downstream or route/plan-only family
- it is still retrospective and bounded
- it still does not justify a Phase E claim

### Out of scope

- broad live rerun governance
- generic evaluator extensibility claims
- a generic proof-capture framework
- UI or operator product surfaces
- downstream enforcement or unlock/deny behavior
- pack-global or gate-global current-governance law
- arbitrary presenter/composition coverage
- a claim that planner-to-presentation governance is now broadly closed

## Anti-Drift Justification

This slice passes the distilled roadmap’s anti-drift rules because:

1. it strengthens analyzer-owned governance over an upstream decision layer rather than host behavior
2. it builds directly on already-landed planner and presenter substrate
3. it closes the next named Phase D gap after routing/planning governance
4. it moves closer to the real “analyzer-v2 is the brain” question without pretending to prove generic engine/pass composition

## Honest Expected Outcome

If this slice lands cleanly, the honest claim afterward should be:

- analyzer-v2 governance now covers:
  - downstream AOI/genealogy result and lifecycle families
  - standalone governance on the two currently supported evaluator substrates
  - one upstream routing/planning decision family
  - one upstream planner-to-presentation composition family

But it would still not justify saying:

- Phase D is automatically closed
- Phase E is complete
- analyzer-v2 has already proven arbitrary engine/pass composition generality

## Suggested Review Questions

When this memo is reviewed, the critical questions should be:

1. Is planner-to-presentation governance the right next Phase D slice, or is this still too proving-campaign-specific to matter?
2. Is one fresh AOI transient compose bundle the smallest honest way to anchor a planning-decision-scoped AOI case?
3. Are the proposed dimensions concrete enough to avoid a vague “compose looked good” grading regime?
4. Is there a smaller alternative that would still advance Phase D more than another downstream or route/plan-only family?
