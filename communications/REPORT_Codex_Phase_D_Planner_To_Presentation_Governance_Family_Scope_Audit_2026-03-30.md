# Report: Codex Audit Of Phase D Planner-To-Presentation Governance Family Scope

Date: 2026-03-30
Audited memo: `communications/MEMO_2026-03-30_phase_d_planner_to_presentation_governance_family_scope.md`

## Verdict

`Approve with corrections`

## Bottom line

Planner-to-presentation governance is the right next bounded Phase D step after the routing/planning governance family. The roadmap documents and the latest Phase D completion memo consistently identify this as the next honest Stage 15 gap, and the repo already contains the substrate needed to support one more frozen governance family over this seam.

The memo is mostly strategically honest and codebase-accurate. The main corrections are about asymmetry and proof shape:

- genealogy already has a persisted-planning-to-`compose-from-intent` lowering seam
- AOI does not have an equivalent analyzer-owned lowering seam; its planner surface still hands the host an explicit `compose-from-selection` contract
- the current repo does not yet contain one frozen AOI artifact that ties a persisted `planning_decision_id` to a composed presentation response on the same proof surface

So the slice is valid, but the memo should state more explicitly that this evaluator family will govern two different bounded handoff shapes under one family, not one fully symmetric lowering law.

## Strongest confirmed claims

- The strategy is aligned with the roadmap. `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`, `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`, `communications/MEMO_2026-03-30_phase_d_routing_planning_governance_family_v1_completion.md`, and the master roadmap all point to one broader planner-to-presentation governance family as the next honest Phase D gap after routing/planning governance.
- The governance substrate is reusable as claimed. `src/evaluations/frozen_pack_definitions.py`, `src/evaluations/gate_definitions.py`, `src/evaluations/review_definitions.py`, `src/evaluations/resolution_definitions.py`, and `src/evaluations/governance_status.py` are already multi-family and do not need new object types or new current-status law for one more family.
- A new evaluator branch is definitely required. `src/evaluations/frozen_pack_harness.py:141-170` still hard-dispatches only `aoi_exemplar`, `genealogy_lifecycle`, and `routing_planning_decision`.
- The planner/presenter seam is real in code. `src/orchestrator/task_planner.py:448-470` emits a genealogy `direct_sections_composition_handoff_plan` that targets `/v1/presenter/compose-from-intent`, while `src/orchestrator/task_planner.py:661-705` emits an AOI `aoi_composition_handoff_plan` that targets `/v1/presenter/compose-from-selection`.
- Persisted planning truth is real. `src/orchestrator/planning_decision_store.py` persists immutable planning snapshots, and the March 30 AOI and genealogy planning snapshot artifacts already prove that persisted shape exists.
- The presenter composition seam is real and tested. `src/api/routes/presenter.py:383-462` exposes `compose-from-intent`, `compose-from-source`, and `compose-from-selection`. `tests/test_compose_from_intent.py:560-600` confirms genealogy composition through `compose_from_intent`, and AOI selection composition is exercised extensively in the same test file.

## Audit answers

### 1. Is planner-to-presentation governance the right next bounded Phase D step?

Yes.

This is the cleanest remaining Stage 15 gap after the routing/planning family landed. It broadens governance upward from route/plan decisions into the seam that turns persisted planner truth into served presentation truth, without pretending to prove Phase E generality.

### 2. Does the memo accurately describe the current substrate and its limits?

Mostly yes.

Confirmed:

- persisted planning decisions exist
- analyzer-owned planner handoff models exist
- analyzer-owned presenter composition routes exist
- one AOI `compose-from-selection` proof line exists
- one genealogy `compose-from-intent` proof line exists
- the current governance substrate can absorb another family without new store or semantic status primitives

Needed correction:

- the memo should say explicitly that the AOI and genealogy seams are not symmetric in implementation
- genealogy has analyzer-owned lowering from persisted planning snapshot to `ComposeFromIntentRequest` via `src/api/routes/orchestrator.py:364-392` and `src/orchestrator/direct_sections_compose_harness.py:17-79`
- AOI does not have an equivalent persisted-planning lowerer; its planner currently instructs the host to carry planner-selected source families and the resolved intent seed into `compose-from-selection` (`src/orchestrator/task_planner.py:688-705`)

That asymmetry is acceptable for this slice, but it is a real substrate limit and should be stated plainly.

### 3. Is the proposed AOI evidence path honest?

Yes, with one important correction.

The memo is correct that the March 27 AOI request proof is not sufficient by itself. `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_requests_2026-03-27.json` contains:

- route evidence
- plan-task evidence
- `compose-from-selection` request/response evidence
- compose trace stages through `contract_validation`

But it does not contain a persisted `planning_decision_id`.

Separately, the March 30 AOI current-contract planning artifacts do contain persisted planning identity:

- `communications/PROOF_phase_d_aoi_planning_decision_current_contract_2026-03-30.json`
- `communications/PROOF_phase_d_aoi_planning_snapshot_current_contract_2026-03-30.json`

But those artifacts do not contain the downstream compose response.

So the repo does not currently have one frozen AOI proof surface that ties:

- persisted planning identity
- planner handoff contract
- `compose-from-selection` request
- composed presentation response

Therefore the honest options are:

1. preferred: capture one fresh AOI frozen bundle that spans planning snapshot plus `compose-from-selection` request/response and pins the shared `planning_decision_id`
2. fallback: change the AOI case shape so it is not pretending to be a persisted-planning-identity-governed compose proof

The memo should explicitly choose option 1 and say why.

### 4. Are the proposed composition-surface cases and dimension laws viable for one bounded evaluator family?

Yes, if the family is written contract-first and case-aware.

The four proposed dimensions are viable:

- `handoff_contract_fidelity`
- `planner_presentation_agreement`
- `presentation_contract_fidelity`
- `composition_trace_integrity`

Why they work:

- AOI and genealogy both have planner-declared followup contracts
- both produce composed presentation payloads with stable `workflow_key`, `consumer_key`, `resolver_version`, `generated_view_definitions`, and `presentation.view_count`
- both expose composition traces that can be checked deterministically

What must not happen:

- the evaluator must not quietly require the same lowering path for both cases
- the AOI case should be judged against selection-carry contract fidelity
- the genealogy case should be judged against direct-sections lowering fidelity

If the evaluator enforces agreement against the declared case contract rather than a single hidden internal path, one family is appropriate.

### 5. Does the memo stay honest about not being Phase E?

Yes.

The memo consistently frames this as:

- retrospective governance
- frozen proof artifacts
- one bounded evaluator family
- not a generic evaluator extensibility claim
- not arbitrary engine/pass composition proof

That is aligned with the distilled roadmap and master roadmap.

### 6. Are there missing scope constraints, cleaner alternatives, or hidden implementation risks?

Yes. The main ones are below.

## Strategic disagreement

None.

I do not see a stronger bounded Phase D alternative than planner-to-presentation governance at this point. Another downstream frozen family would be weaker, and a Phase E-style generic evaluator story would be premature.

## Scope corrections

### 1. State the AOI/genealogy asymmetry explicitly

The memo should add a plain statement that:

- genealogy is persisted-planning-snapshot -> analyzer lowering -> `compose-from-intent`
- AOI is persisted-planning-snapshot -> planner-selected handoff -> host-carried `compose-from-selection`

Without that sentence, the family reads more symmetric than the repo actually is.

### 2. Require one fresh AOI bundle that joins planning identity to compose output

This is the most important correction.

Current repo state:

- March 27 AOI proof has compose request/response but no persisted `planning_decision_id`
- March 30 AOI planning artifacts have persisted `planning_decision_id` but no compose response

So the memo should say that the AOI case is blocked on one fresh frozen bundle, not merely “preferably supported” by one.

### 3. Make the evaluator law explicitly case-contract-based

The memo should say that the family tolerates asymmetric proof shapes as long as:

- each case declares its contract up front
- evidence refs pin the declared surfaces
- the evaluator only checks internal agreement against that case contract

This is the same honesty rule the routing/planning family already used.

### 4. Do not imply analyzer-owned AOI lowering

The memo should avoid wording that sounds like AOI already has the same analyzer lowering seam genealogy has. The repo does not currently support `planning_decision_id -> compose-from-selection request` as an analyzer route.

## Implementation cautions

### 1. The new branch is real work, not definition-only

`src/evaluations/frozen_pack_harness.py:141-170` confirms that another evaluator family means new branch logic, new evidence extraction helpers, and new tests.

### 2. The evidence loader will likely need deliberate AOI/genealogy split helpers

The routing/planning evaluator already handles asymmetric evidence extraction. The new family should expect the same:

- AOI: planning snapshot plus `compose-from-selection` request/response bundle
- genealogy: existing multi-surface trace plus optional explicit planning snapshot

Trying to force one artifact parser will likely create brittle logic.

### 3. Documentation strings are behind the actual substrate

`src/presenter/compose_from_intent.py:1`, `src/presenter/compose_from_intent.py:219-230`, and `src/api/routes/presenter.py:383-448` still describe these routes as AOI-specific even though the code and tests already support genealogy on `compose-from-intent`. That is documentation drift, not a blocker, but future scope/review memos should not rely on those docstrings as architectural truth.

### 4. The evaluator should remain retrospective, not live-revalidating against present code behavior

The memo already points in the right direction here. It should keep that rule. Otherwise this family will accidentally become a moving-target compatibility test instead of frozen governance.

## Recommended memo edits

- Add one paragraph naming the AOI/genealogy asymmetry directly.
- Change the AOI evidence text from a preference to a requirement: one fresh current-contract AOI frozen bundle that ties persisted `planning_decision_id` to `compose-from-selection` request/response evidence.
- Add one sentence that the evaluator judges case-specific contract agreement and does not require identical proof shapes.
- Keep the current “not Phase E” boundary unchanged.

## Verification run

Focused verification passed:

- `PYTHONPATH=. pytest -q tests/test_task_planner.py tests/test_compose_from_intent.py tests/test_frozen_governance_pack.py tests/test_evaluation_governance_status.py tests/test_evaluation_governance_status_routes.py`
- Result: `80 passed`

## Final judgment

Approve the scope memo after the corrections above.

The next step is not to rethink the slice. It is to tighten the memo around the real asymmetry, capture the missing AOI frozen bundle, and then implement one bounded `planner_presentation_decision` family without widening into generic evaluator architecture or Phase E claims.
