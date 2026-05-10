# Report: Codex Audit Of Phase D Cross-Campaign Planner-To-Presentation Governance Scope

Date: 2026-03-30
Subject memo: `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_scope.md`
Verdict: `Approve with corrections`

## Bottom Line

The memo is directionally right.

The next bounded honest Phase D move is still a second planner-to-presentation governance proof campaign, not product UI, downstream enforcement, or a premature Phase E generality claim. The live repo does show that the current planner-to-presentation family is still tied to one AOI March 30 bundle plus one genealogy March 28 trace/snapshot line rather than a second fresh upstream campaign (`src/evaluations/frozen_pack_definitions.py:276-319`, `communications/PROOF_phase_d_aoi_transient_compose_current_contract_2026-03-30.json`, `communications/PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`, `communications/PROOF_phase_d_genealogy_direct_sections_planning_snapshot_2026-03-30.json`).

But the memo slightly understates two implementation realities:

1. reusing `planner_presentation_decision` is the right default, but it will not be definition-only work
2. a fresh genealogy bundle needs an explicit bundle-level planning-decision binding story, because the current `compose-from-intent` request contract does not carry `planning_decision_id` natively (`src/presenter/schemas.py:613-620`, `src/evaluations/frozen_pack_harness.py:1609-1620`)

## Strongest Confirmed Claims

- The current remaining Phase D gap is anti-coupling, not basic capability existence. The repo already has:
  - one upstream routing/planning governance family
  - one upstream planner-to-presentation governance family
  - generic gate/review/resolution/status seams that already serve multiple families without route redesign
  - evidence: `src/evaluations/frozen_pack_definitions.py:218-319`, `src/evaluations/gate_definitions.py:101-164`, `src/evaluations/review_definitions.py:54-69`, `src/evaluations/resolution_definitions.py:53-72`, `src/evaluations/governance_status.py:25-94`

- The current planner-to-presentation family is genuinely mixed-vintage. AOI uses one fresh current-contract transient compose bundle, while genealogy still depends on the March 28 multi-surface trace plus a March 30 exported snapshot artifact:
  - AOI: `src/evaluations/frozen_pack_definitions.py:279-295`
  - genealogy: `src/evaluations/frozen_pack_definitions.py:297-318`

- The memo is strategically honest that this is still retrospective frozen-artifact governance, not live governance and not Phase E. That matches the code. The evaluator reads pinned artifacts, not live planner/presenter state (`src/evaluations/frozen_pack_harness.py:180-253`, `1555-1651`).

- Reusing the existing governance-status seam is realistic. The semantic status derivation is keyed by `resolution_key + gate_decision_id` and validates linked resolution/review/gate records without caring which family produced them (`src/evaluations/governance_status.py:25-94`). Existing tests already prove this unchanged seam across multiple newer families (`tests/test_evaluation_governance_status.py:485-606`, `tests/test_evaluation_governance_status_routes.py:412-545`).

## Audit Answers

### 1. Is a second fresh planner-to-presentation proof campaign the right next bounded Phase D step?

Yes.

That conclusion is supported by:

- the distilled roadmap’s explicit Phase D exit condition requiring one second materially distinct proof campaign (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:195-224`)
- the master roadmap’s current Stage 15 note that governance remains partial because it is still tied to one proving-campaign lineage and lacks a second fresher planner-to-presentation campaign (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1213`, `1238`, `1341-1345`)
- the live pack definitions showing the first planner-to-presentation family still reuses one stale genealogy artifact lineage (`src/evaluations/frozen_pack_definitions.py:276-319`)

### 2. Does the memo accurately describe the current substrate and the real remaining gap?

Mostly yes.

Accurate:

- the repo already has the planner-to-presentation evaluator family and one real planner-to-presentation gate/review/resolution/status chain
- the remaining strategic doubt is anti-coupling, not whether governance can reach planner-to-presentation at all

The one correction is emphasis:

- the actual stale dependency is more concentrated on genealogy than on AOI
- AOI already has a fresh March 30 current-contract bundle
- genealogy is the side still anchored to the March 28 trace plus March 30 support snapshot

That does not invalidate the memo’s paired-campaign proposal, but it matters when discussing smaller alternatives.

### 3. Is reusing `planner_presentation_decision` the right default?

Yes, with a stronger caution than the memo currently gives.

The four dimension checks remain the right law for the next slice (`src/evaluations/frozen_pack_harness.py:1141-1385`). So a fresh cross-campaign family should start by reusing `planner_presentation_decision`.

However, the evaluator family is not generic over arbitrary case names or arbitrary artifact shapes. It is still explicitly case-key and extraction-shape aware:

- case specs are hard-coded in `_PLANNER_PRESENTATION_CASE_SPECS` (`src/evaluations/frozen_pack_harness.py:137-177`)
- evidence extraction is hard-coded by case key in `_extract_planner_presentation_evidence(...)` (`src/evaluations/frozen_pack_harness.py:1555-1651`)

So the honest implementation assumption should be:

- reuse the evaluator family and dimensions
- expect bounded harness/extraction work for any fresh genealogy bundle and any new case keys

### 4. Does the memo stay honest about proving anti-coupling rather than generic evaluator extensibility or Phase E generality?

Yes, mostly.

The memo repeatedly frames the slice as a proof that the same governance law survives a second bounded campaign, not as proof of arbitrary evaluator extensibility or arbitrary engine/pass composition. That matches the codebase reality, because the harness is still explicitly bounded and not plugin-like (`src/evaluations/frozen_pack_harness.py:217-253`).

### 5. Are the proposed pack/family boundaries and regression expectations viable?

Mostly yes.

Viable:

- one second pack
- one second gate
- one second review
- one second resolution
- one real persisted chain
- unchanged governance-status route

Those expectations are already consistent with how the routing/planning and planner-to-presentation families were added (`src/evaluations/gate_definitions.py:101-164`, `src/evaluations/review_definitions.py:54-69`, `src/evaluations/resolution_definitions.py:53-72`).

Correction:

- the anti-coupling regression expectation saying the second campaign should not need to “drift back toward the old campaign” is too vague to be a good test target
- better concrete regressions are:
  - the new pack has its own pinned artifact paths and hashes
  - the new family passes on those new artifacts
  - the original planner-to-presentation family still passes unchanged
  - older standalone and routing/planning families still pass unchanged

### 6. Is there a smaller cleaner next step that would still materially reduce proving-campaign coupling?

There is a smaller step, but it is weaker.

The smaller cleaner alternative is:

- one fresh dedicated genealogy current-contract planner-to-presentation bundle
- one genealogy-only planner-to-presentation family proving the evaluator is not tied to the March 28 trace shape

Why it is smaller:

- the current stale dependency is concentrated on genealogy
- AOI already has a fresh March 30 current-contract compose bundle

Why it is weaker:

- it would not prove a second fresh paired campaign across the full current planner-to-presentation family
- it would reduce coupling, but less cleanly than the memo’s proposed paired AOI+genealogy campaign

So the memo’s proposed paired campaign remains the better main-line choice.

## Scope Corrections

### 1. Genealogy `planning_decision_id` binding needs a more explicit statement

The memo currently implies the fresh genealogy bundle can straightforwardly prove stable `planning_decision_id` agreement “between persisted planning truth and compose execution.”

That is not route-native today.

`ComposeFromIntentRequest` contains:

- `workflow_key`
- `consumer_key`
- `user_intent`
- `prose_sections`
- optional style/audience

It does not contain `planning_decision_id` (`src/presenter/schemas.py:613-620`).

By contrast, the current genealogy evaluator derives its `compose_binding_planning_decision_id` from the planning snapshot artifact, not from compose request/response fields (`src/evaluations/frozen_pack_harness.py:1616-1620`).

So the scope memo should say explicitly:

- the fresh genealogy bundle must include explicit bundle-level binding metadata if it wants to claim compose-execution linkage to one planning decision
- do not imply that `/v1/presenter/compose-from-intent` already carries that linkage on its public request contract

### 2. Reusing the evaluator is not the same as definition-only reuse

The memo should strengthen this sentence. A fresh planner-to-presentation family reusing `planner_presentation_decision` will still likely require:

- new case spec entries
- new artifact refs
- new extraction handling for the fresh genealogy bundle

This is still bounded work, but it is real harness work, not just new pack definitions.

### 3. The regression language should become more concrete

Replace the vague anti-coupling regression phrasing with explicit assertions around:

- distinct artifact paths
- distinct hashes
- distinct case keys / family keys
- unchanged passing status of prior families

## Implementation Cautions

### 1. Keep the fresh genealogy bundle normalized to the existing evaluator inputs

The safest way to keep evaluator changes bounded is for the fresh genealogy bundle to expose the same logical evidence surfaces the current evaluator already consumes:

- `planning_decision`
- `planning_snapshot`
- compose request payload
- compose response payload
- explicit planning-decision binding metadata at bundle level

If the new genealogy artifact can be normalized to those surfaces, the evaluator-law can stay stable even if extraction changes.

### 2. Do not over-claim parity between AOI and genealogy request shapes

AOI `compose-from-selection` carries `source_v2_job_id` in the request contract (`src/presenter/schemas.py:669-680`).
Genealogy `compose-from-intent` does not (`src/presenter/schemas.py:613-620`).

The current evaluator already respects that asymmetry (`src/evaluations/frozen_pack_harness.py:1170-1240`).
The next memo should keep that asymmetry explicit rather than implying identical lowering surfaces.

### 3. Preserve the existing governance-status claim boundary

The status seam is generic across family keys, but it still validates exact family-key alignment across resolution, review, and gate (`src/evaluations/governance_status.py:115-259`).

So the new family should be added as a new exact declared chain, not by trying to reuse old family keys against new artifacts.

## Strategic Disagreement

No material strategic disagreement.

The memo stays inside the correct Phase D boundary and does not drift into UI/product or Phase E theater. The main required changes are scope-accuracy corrections, not a different strategic direction.

## Verification Performed

Code and artifact inspection:

- `src/evaluations/frozen_pack_harness.py`
- `src/evaluations/frozen_pack_definitions.py`
- `src/evaluations/gate_definitions.py`
- `src/evaluations/review_definitions.py`
- `src/evaluations/resolution_definitions.py`
- `src/evaluations/governance_status.py`
- `src/orchestrator/task_planner.py`
- `src/api/routes/presenter.py`
- `src/presenter/compose_from_intent.py`
- `src/presenter/schemas.py`
- the requested proof artifacts under `communications/`

Focused verification:

- `PYTHONPATH=. pytest -q tests/test_frozen_governance_pack.py tests/test_bounded_release_gate.py tests/test_bounded_review_disposition.py tests/test_bounded_disposition_resolution.py tests/test_evaluation_governance_status.py tests/test_evaluation_governance_status_routes.py`
  - result: `83 passed, 2 warnings`
