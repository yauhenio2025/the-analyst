# Audit: Stage 5 / AOI Exemplar Exit Gate Scope

Date: 2026-03-24
Reviewer: Codex
Source memo: [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md)

## Overall Verdict

Approve.

The revised memo is now materially aligned with the live code and the current strategy trail. It closes the substantive first-pass review gaps by:

- requiring one real planner-primary `aoi_selection_blocked` case at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L103)
- handling the locked non-profile readiness gap honestly at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L118)
- defining a concrete artifact-capture method at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L151)
- making Stage 2 closure stricter and explicitly evidence-driven at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L168)
- defining fixture-strength tiers and a minimum stronger-than-fixture condition for Stage 2 closure at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L211)
- requiring the rubric to exist before grading with explicit threshold shape at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L227)

No material pre-implementation scope blockers remain.

## Concrete Findings

### 1. Stage 5 is still the right immediate next step

The memo remains honest that Stage 3/4 Milestone A is already landed and that the next honest move is evaluation, not another structural AOI rewrite, at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L16). That still matches the canonical ledger, which leaves Stage 2 `In progress`, Stage 3 and 4 `Partial`, and Stage 5 `Not started` but explicitly names it as the immediate next gate in [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1167). It also matches the draft roadmap’s sequencing note in [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L218).

The code continues to support that sequencing call. AOI routing now returns the planner handoff contract in [task_router.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_router.py#L387). AOI planning resolves source catalog plus bounded selection and points downstream followup at `POST /v1/presenter/compose-from-selection` in [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L413). The current host consumes that path in [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L540) and [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L414). So there is no remaining Milestone A structural gap that would make a Stage 5 gate premature.

### 2. The fixed eval pack now reflects the real current seam

The revised four-case pack is now shaped correctly for the seam that actually exists.

The negative case is no longer vague. Requiring one real planner-primary `aoi_selection_blocked` case at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L107) is aligned with the code because the blocked selector path now has its own outcome kind, blocked reason codes, and saved selector provenance in [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L973) and [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L1045).

The locked non-profile case also remains a legitimate hard requirement. The analyzer now supports explicit selection-backed compose via [schemas.py](/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py#L669), [composition_source_bridge.py](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L295), and [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L256). Focused tests still cover the non-profile `thematic_synthesis + engagement_mapping + thematic_report` combination in [test_composition_source_bridge.py](/home/evgeny/projects/analyzer-v2/tests/test_composition_source_bridge.py#L185).

The new readiness caveat is also correct. The current readiness surface remains profile-shaped for AOI, not arbitrary-source-family-shaped, in [hostContractV1.ts](/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts#L201) and [source_backed_readiness.py](/home/evgeny/projects/analyzer-v2/src/analysis_products/source_backed_readiness.py#L97). So the memo is right to require direct `plan-task -> compose-from-selection` continuation for the locked non-profile case unless a small compatibility fix is intentionally added.

### 3. The memo is now specific enough about audit artifacts

This was the largest operational gap in the first pass and it is now closed.

The code does expose the required audit surface:

- selected/rejected sources, selection summary, resolved intent seed, and followup contract fields in [task_planning_schemas.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py#L165) and [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L518)
- blocked-path provenance in [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L1045)
- compose trace stages in [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L276)
- actual host compose request formation in [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L429)
- host-proxy forwarding of selection-backed compose in [api/server.py](/home/evgeny/projects/the-critic/api/server.py#L20594)

What the code does not do is persist those artifacts automatically. The memo now says that explicitly and names a concrete default capture method at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L151). That is the right level of specificity for this tranche.

The narrowed definition of “planner rationale” is also correct at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L162). In the current contract there is no richer separate planner-rationale field beyond `selection_summary`, selected-source `rationale`, and rejected-source `rejection_reason`.

### 4. The Stage 2 closure decision is now strong enough

The revised memo is no longer soft on Stage 2.

It still keeps Stage 2 closure explicit rather than automatic at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L168), which matches the canonical roadmap in [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1167). The new non-closure examples at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L179) are concrete enough to prevent a convenience closeout.

The fixture-strength tiering also improves honesty. The shared `fixture_backed | execution_backed | user_initiated` model at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L211) is clear, and requiring at least one ready case to be `execution_backed` or stronger before Stage 2 can close at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L222) is a defensible quality bar.

### 5. The rubric timing, threshold shape, and latency breakdown are now concrete enough

The memo now avoids post-hoc self-certification.

Requiring the rubric to be written before grading at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L227) and giving a minimum threshold shape at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L238) is concrete enough for this scope memo. The latency split into planner selection, composition, and total user-visible latency at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L142) is also auditably better than the earlier generic “responsiveness notes.”

## Scope / Sequence Assessment

The memo is now scoped correctly.

It evaluates the landed AOI exemplar seam rather than reopening Stage 3/4 architecture. It keeps the boundary narrow to the current proof surface in `the-critic` at [MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md#L94). It does not drift into later de-AOI / de-`the-critic` transient generalization, which still belongs to a later tranche because transient compose remains structurally AOI-only and `the-critic`-only in [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L496).

The remaining host residuals are also scoped honestly enough. The host contract still records host-proxy identity translation on the source-backed transient path in [hostContractV1.ts](/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts#L215), and the host still performs snapshot warmup before planner-backed navigation in [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L630). So the memo is drawing the right line between acceptable residuals now and later substrate work.

## Missing Assumptions Or Hidden Prerequisites

No material hidden prerequisite remains unaccounted for in the revised memo.

One optional clarification would make the record slightly sharper:

- if the author wants maximum precision, the refresh/deep-link limitation could explicitly say that the current planner-backed handoff is carried through navigation state in [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L643) and rehydrated from `location.state` in [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L238), which is why refresh/deep-link continuity is still broken

That is an optional clarification, not a blocker.

## Recommended Revisions Before Implementation

None required.

Optional only:

1. Add one sentence tying planner-backed refresh/deep-link discontinuity directly to the current navigation-state handoff mechanism.

## Bottom Line

The revised memo is now implementation-ready as a Stage 5 scope.

It reflects the real Milestone A seam, requires the right negative case, handles the non-profile readiness caveat honestly, makes artifact capture concrete, and sets a materially stronger evidence bar for any Stage 2 closure decision.
