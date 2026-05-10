# Report: Codex Audit Of Phase E Representative Composition Matrix Scope

Date: 2026-03-30
Subject memo: `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_scope.md`
Verdict: `Approve with corrections`

## Bottom Line

The memo is strategically right.

After the Phase D exit, the next honest question is no longer governance accretion. It is whether the already-live analyzer-owned composition substrate can survive a small but real cross-family proof. That is exactly the pivot already recorded in the roadmap stack (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:228-249`, `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:324-348`, `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:342-347`, `484-490`).

The live repo also confirms the core factual premise:

- `POST /v1/presenter/compose-from-source` exists and returns `ComposeFromIntentResponse` through the common transient composer (`src/api/routes/presenter.py:413-443`, `src/presenter/compose_from_intent.py:229-274`, `src/presenter/schemas.py:658-734`)
- `POST /v1/presenter/compose-from-selection` exists and returns the same served shape through the same composer (`src/api/routes/presenter.py:446-470`, `src/presenter/compose_from_intent.py:277-326`, `src/presenter/schemas.py:669-734`)
- genealogy saved-result routing does lower into a persisted `direct_sections` handoff and then into `POST /v1/presenter/compose-from-intent` without host-side semantic reconstruction (`src/orchestrator/task_router.py:397-469`, `src/orchestrator/task_planner.py:430-487`, `src/orchestrator/direct_sections_compose_harness.py:17-79`, `src/api/routes/orchestrator.py:364-394`)

But the memo should be corrected in three places:

1. the genealogy case is not a peer public route in the same sense as the two AOI source routes; it is a planner-backed lowering proof over `compose-from-intent`
2. keeping the consumer fixed to `the-critic` is not only strategically clean, it is currently enforced by the live composer
3. there is a smaller cleaner first Phase E step available, but it is weaker than the memo’s proposed three-case matrix

## Strongest Confirmed Claims

- A representative composition matrix is the roadmap-consistent next move. Multiple same-day roadmap memos already make the Phase D -> Phase E pivot explicit and name `source_profile`, `source_selection`, and `direct_sections` as the first bounded slice (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:240-245`, `308-316`; `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:326-348`; `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:342-347`, `487-490`).

- The three cited surfaces do converge on one served response model. `ComposeFromIntentResponse` contains one transient presentation, one generated-view-definition list, and one trace, and all three public presenter routes are declared to return it (`src/presenter/schemas.py:729-734`, `src/api/routes/presenter.py:383-470`).

- The AOI `source_selection` case is the evolution-ready planner-primary surface, not a narrowed preset. The planner emits an `AoiCompositionHandoffPlan` with explicit `selected_sources`, `expected_source_families`, `available_source_families`, and `legacy_profile_equivalent`, and its downstream followup contract targets `/v1/presenter/compose-from-selection` (`src/orchestrator/task_planning_schemas.py:172-195`, `src/orchestrator/task_planner.py:652-705`). The focused tests also preserve the four-family evolution-ready payload rather than collapsing back to a smaller shortcut (`tests/test_compose_from_intent.py:1537-1685`).

- The genealogy case already has a real analyzer-owned planner-backed lowering seam. The router selects `planner.direct_sections_compose_handoff`, the planner emits a `DirectSectionsCompositionHandoffPlan`, and the lowering adapter rejects any loss of semantic metadata before producing a thin `ComposeFromIntentRequest` (`src/orchestrator/task_router.py:403-467`, `src/orchestrator/task_planning_schemas.py:198-220`, `src/orchestrator/direct_sections_compose_harness.py:17-79`).

- The memo is correct to frame this as representative composition law, not arbitrary engine/pass composition. All three entry surfaces funnel into the same `_compose_handoff_sections(...)` pipeline rather than three unrelated implementations (`src/presenter/compose_from_intent.py:219-300`, `329-375`). So the honest claim is common composition law over multiple live handoff families, not open-ended combinatorics.

## Audit Answers

### 1. Is a representative composition matrix the right first Phase E slice after Phase D exit?

Yes.

This is the right first Phase E move because it directly tests the open question the roadmap stack now names: whether analyzer-owned planning/composition/rendering law generalizes across representative workflow-output families without host-specific intelligence (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:232-248`, `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:326-348`).

It is also the right size:

- narrower than arbitrary engine/pass composition
- broader than one more governance family
- grounded in already-live routes and proof artifacts rather than speculative substrate

### 2. Does the memo accurately describe the currently live compose surfaces and their differences?

Mostly yes.

Confirmed:

- `source_profile` is a distinct public request contract via `ComposeFromSourceRequest` (`src/presenter/schemas.py:658-666`)
- `source_selection` is a distinct public request contract via `ComposeFromSelectionRequest` (`src/presenter/schemas.py:669-679`)
- both AOI source routes lower through different bridge builders and trace prefixes before entering the common transient composer (`src/presenter/compose_from_intent.py:229-326`)
- genealogy saved-result composition is planner-backed through `direct_sections` and reaches the public presenter only after analyzer-owned lowering (`src/orchestrator/task_planner.py:430-487`, `src/orchestrator/direct_sections_compose_harness.py:17-79`, `src/api/routes/orchestrator.py:364-394`)

Correction:

- the genealogy case should not be described as if it were a third peer public route like the AOI source routes
- the truth is more specific: it is a persisted planning decision plus analyzer-owned lowering into the thin public `compose-from-intent` request
- that asymmetry matters because `ComposeFromIntentRequest` itself does not carry `planning_decision_id` (`src/presenter/schemas.py:613-621`)

There is also a minor documentation-drift issue in the codebase: several docstrings still say “AOI” even though the implementation and tests now support genealogy direct-sections too (`src/presenter/compose_from_intent.py:1`, `219-220`; `src/api/routes/presenter.py:385`, `415`, `448`; `tests/test_compose_from_intent.py:557-600`). That drift does not invalidate the memo, but it is worth naming.

### 3. Is the proposed three-case matrix the smallest honest proof of generality available right now?

Not quite. It is the best bounded proof, but not the smallest.

The smallest cleaner proof that still materially advances the program would be a two-case planner-backed matrix:

- AOI `source_selection`
- genealogy `direct_sections`

Why that smaller alternative is cleaner:

- both cases are planner-backed
- both are tied to persisted planning decisions
- both isolate the analyzer-owned handoff question more directly than the preset `source_profile` route

Why the memo’s three-case matrix is still stronger:

- it proves common law across all three currently live handoff families already named in the roadmap
- it shows the analyzer-owned composer handles both preset-profile entry and explicit planner-selected entry on the AOI side
- it avoids quietly treating `source_profile` as dead or merely legacy when it is still a live served surface

So the three-case matrix is not the absolute smallest slice, but it is the smallest strong honest proof of generality across the currently live families.

### 4. Does the memo stay honest about proving representative composition law rather than arbitrary engine/pass composition?

Yes, mostly.

The live code actually supports that framing. The three surfaces do not prove three separate composition engines. They prove that one analyzer-owned transient composition pipeline can accept multiple handoff kinds and still produce the same served response shape (`src/presenter/compose_from_intent.py:145-158`, `219-300`, `329-375`).

That is the right claim boundary. The memo should keep saying:

- common composition law over representative handoff families

and should keep not saying:

- arbitrary engine/pass graph composition is already proven

### 5. Is keeping the consumer fixed to `the-critic` the right default for isolating the Phase E question?

Yes.

Strategically, that isolates the variable that matters first: composition/handoff generality rather than consumer-adapter generality.

Implementation-wise, it is also the only honest default today. The transient composer currently hard-registers only one consumer adapter and rejects other consumer keys fail-closed (`src/presenter/compose_from_intent.py:158`, `524-536`). So widening the consumer set would no longer be “just isolation scope”; it would become new substrate work.

This means the memo’s fixed-consumer choice is not merely convenient. It is the current contract boundary.

### 6. Is there a smaller cleaner first Phase E step that would still materially advance the analyzer-v2-as-brain proof?

Yes, but it is weaker.

The smaller cleaner option is:

- one planner-backed two-case matrix over AOI `source_selection` and genealogy `direct_sections`

That alternative would still materially advance the proof because it would demonstrate:

- one AOI planner-selected handoff family
- one non-AOI planner-backed handoff family
- one shared served response model
- no host-side semantic reconstruction across either path

But it would leave one live compose family untested:

- AOI `source_profile`

So it is better treated as a fallback if implementation pressure or proof-capture complexity forces a tighter first cut. It is not the better main recommendation.

## Scope Corrections

### 1. Name the genealogy asymmetry more explicitly

The memo already hints at this, but it should say it more plainly:

- AOI `source_profile` and AOI `source_selection` are public presenter routes with dedicated public request contracts
- genealogy `direct_sections` is a planner-backed internal handoff that must be lowered into the thin public `compose-from-intent` contract

Relevant seams:

- `src/presenter/schemas.py:613-679`
- `src/orchestrator/task_planner.py:448-470`
- `src/orchestrator/direct_sections_compose_harness.py:17-79`
- `src/api/routes/orchestrator.py:364-394`

### 2. Say explicitly that `planning_decision_id` linkage for genealogy is bundle-level truth, not request-contract truth

This is the most important factual correction.

`ComposeFromIntentRequest` contains:

- `workflow_key`
- `consumer_key`
- `user_intent`
- `prose_sections`

It does not contain `planning_decision_id` (`src/presenter/schemas.py:613-621`).

So for the genealogy case, any proof record tying compose execution back to one persisted planning decision must be wrapper-level or bundle-level metadata, exactly as the memo partly acknowledges. That point should be made unambiguously.

### 3. Keep the “three families” claim attached to handoff families, not independent composition engines

The current codebase has one common transient composer. `compose-from-source` and `compose-from-selection` both rewrite into `ComposeFromIntentRequest` and then call `_compose_handoff_sections(...)` (`src/presenter/compose_from_intent.py:229-326`).

That is good news for the memo’s main thesis, but the wording should stay precise:

- three live analyzer-owned handoff families
- one common analyzer-owned composition law

Not:

- three separate composition subsystems

## Implementation Cautions

### 1. Keep the proof seam bounded to route-faithful execution plus frozen proof capture

The repo already has enough live substrate to prove the matrix without inventing a generic proof-capture framework. The best implementation shape is still:

- one focused matrix test or tiny harness
- one frozen proof record per case under `communications/`
- exact route-faithful requests and responses

Anything larger would drift back toward Phase D-style infrastructure accretion.

### 2. Do not widen consumer support inside this slice

The code does not currently admit any transient consumer besides `the-critic` (`src/presenter/compose_from_intent.py:158`, `524-536`). So trying to make the matrix “more general” by adding a second consumer would turn this into a consumer-expansion slice, not a composition-law slice.

### 3. Preserve the AOI four-family evolution-ready path in the planner-backed case

The planner-backed AOI case should be anchored on `source_selection`, not reduced to `source_profile`, because that is where the broader planner-selected contract truth lives (`src/orchestrator/task_planning_schemas.py:172-195`, `src/orchestrator/task_planner.py:661-705`). The focused contract test already validates the four-family path (`tests/test_compose_from_intent.py:1537-1685`).

## Strategic Disagreement

No material strategic disagreement.

The memo is aligned with the live roadmap and the live codebase. My objections are scope-accuracy refinements, not a different strategic direction.

## Verification Performed

Code and artifact inspection:

- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_scope.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_v1_completion.md`
- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_scope.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/PROOF_phase_d_cross_campaign_aoi_transient_compose_2026-03-30.json`
- `communications/PROOF_phase_d_cross_campaign_genealogy_transient_compose_2026-03-30.json`
- `src/api/routes/presenter.py`
- `src/presenter/compose_from_intent.py`
- `src/presenter/schemas.py`
- `src/presenter/composition_source_bridge.py`
- `src/orchestrator/task_router.py`
- `src/orchestrator/task_planner.py`
- `src/orchestrator/task_planning_schemas.py`
- `src/orchestrator/direct_sections_compose_harness.py`
- `src/api/routes/orchestrator.py`
- `tests/test_compose_from_intent.py`
- `tests/test_task_router.py`
- `tests/test_task_planner.py`
- `tests/test_run_contract.py`

Focused verification:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_task_router.py tests/test_task_planner.py tests/test_run_contract.py`
  - result: `69 passed, 29 warnings`
