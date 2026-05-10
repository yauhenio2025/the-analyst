# Audit: Stage 3/4/5 AOI Exemplar Completion Scope

Date: 2026-03-24
Reviewer: Codex
Source memo: `communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md`

## Overall Verdict

Approve.

The revised memo is now materially aligned with the live code and the current strategy trail. It now handles canonical Stage 2 honestly, distinguishes the richer analyzer-side AOI handoff from the still-thin effective host-consumed seam, makes the `compose-from-source` public-contract lock explicit, and names the real host continuity residuals that still sit on the proof path. That matches the current roadmap and code in [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1167), [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L171), [task_planning_schemas.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py#L155), [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L427), [taskLaunchRuntime.ts](/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts#L87), [schemas.py](/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py#L624), and [hostContractV1.ts](/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts#L214).

Two minor pre-implementation doc fixes are still worth making:

- tighten the Stage 4 wording about "other AOI product bundles already present in the saved-result substrate," because the current bridge formalizes four AOI source families rather than a broader already-exposed registry at [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L168) and [composition_source_bridge.py](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L28)
- fix the internal count mismatch where the memo lists six residuals and then says "those five residuals" at [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L262)

Neither issue changes the sequencing call or the tranche boundary.

## Concrete Findings

### 1. Stage 2 is now handled honestly instead of being skipped

The memo now explicitly says Stage 2 is subsumed by the current source-backed transient substrate and should be documentary-closed as a side-effect of this tranche's evaluation/ops pack at [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L24) and [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L113). That is a defensible read of the canonical roadmap, which still marks Stage 2 in progress while Stages 3, 4, and 5 remain partial or open at [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1167). It also matches the current draft roadmap, which makes AOI exemplar completion the next main tranche at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L171).

### 2. The planner-contract framing is now correct

The revised memo now says the analyzer-native AOI handoff is already richer than pure allow/block lists, while the effective host-consumed seam is still dominated by `allowed_profiles` / `blocked_profiles` at [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L61) and [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L183). That is accurate.

The code still shows the exact split the memo now describes:

- the backend handoff plan already carries `expected_source_families`, `available_source_families`, `expected_producer_engines`, and `bridge_contract_targets` in [task_planning_schemas.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py#L155), and the planner populates those richer fields in [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L427)
- the current host TypeScript interface still narrows the AOI handoff plan to `allowed_profiles`, `blocked_profiles`, and `handoff_notes` in [taskLaunchRuntime.ts](/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts#L87)
- the compose page still surfaces planner-backed guardrails in terms of allowed and blocked profiles and still renders `dossier` / `comparison` as the primary launch actions in [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L429)

So the memo is now honest about the real issue: the backend is somewhat richer, but the live proof path is still too profile-centric to count as Stage 3/4 closure.

### 3. The memo now makes the public compose-contract lock explicit enough

Decision 5A and the deliverables section now state plainly that a proof case not honestly reducible to `dossier` / `comparison` requires public contract widening or a new planner-resolved downstream compose contract at [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L204), [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L287), and [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L322). That is the correct implementation reality.

The code path remains locked today:

- the public analyzer request still hard-locks `profile` to `Literal["dossier", "comparison"]` in [schemas.py](/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py#L624)
- the analyzer source bridge still resolves through `_PROFILE_SELECTION_PRESETS` for exactly those two profiles in [composition_source_bridge.py](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L67)
- the host contract and client path still validate `profile` as required input for `source_backed_transient_launch` in [hostContractV1.ts](/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts#L214) and [composeFromIntentClient.ts](/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts#L64)

This was a first-pass blocker. It is now correctly surfaced in the memo rather than left implicit.

### 4. The memo now names the real host residuals and likely seams

The revised memo now explicitly names host-proxy identity translation and snapshot warmup as allowed host-owned continuity residuals at [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L67), [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L237), and [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L369). It also now lists the actual likely host seams, not just `taskLaunchRuntime.ts`.

That matches the live host path:

- `source_backed_transient_launch` is explicitly a host-proxy family with `host_local_identity_translation_before_launch: true` in [hostContractV1.ts](/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts#L214)
- the source-backed compose client still validates host-contract inputs before launch in [composeFromIntentClient.ts](/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts#L64)
- snapshot warmup remains a separate host continuity step through `cache_snapshot_warmup` in [boundedV2Client.ts](/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts#L233)

This is now honest enough for scoping. The memo no longer treats those proof-path dependencies as invisible.

### 5. Keeping Stage 5 inside the tranche is still the right call

The revised memo correctly distinguishes the existing readiness gate from the still-missing Stage 5 evaluation pack at [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L217), [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L322), and [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L395). That remains the right sequencing choice.

The roadmap still marks Stage 5 as not started at [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1170), and the current Stage 13 Tier A proof explicitly closed a result-contract seam rather than a stronger quality or polish claim at [PROOF_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout.md](/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout.md#L130). So the memo is correct to keep a bounded AOI rubric/threshold/failure-taxonomy pack inside this tranche instead of treating it as later cleanup.

## Scope / Sequence Assessment

- One planner-primary AOI proof path is still the right bounded deliverable. Another Stage 13 slice or de-AOI transient-substrate generalization first would widen a seam that is still profile-first and not yet evaluated at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L189).
- Treating Stage 4 here as bounded AOI source/product-selection law, rather than broader engine-graph planning, remains the right boundary for this tranche at [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L160).
- Keeping legacy AOI controls outside the proof slice is still the correct bounded transition strategy, as long as the proof path itself becomes analyzer-authoritative and stops re-asking the main analytical choice through profile-first controls at [MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md#L139).

## Missing Assumptions Or Hidden Prerequisites

Most of the previously hidden prerequisites are now surfaced in the memo. The remaining useful clarification is about data-quality scope for the eventual Stage 5 pack:

- if the evaluation pack is meant to support usefulness claims rather than just seam-correctness claims, the closeout should record whether evaluated AOI cases are proof-fixture-backed or based on stronger source material, because the current Stage 13 Tier A proof explicitly limited itself to the former quality boundary at [PROOF_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout.md](/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout.md#L132)

This is not a sequencing blocker. It is a useful closeout-discipline note.

## Recommended Revisions Before Implementation

1. Replace the Stage 4 wording that implies broader already-present AOI product bundles than the current four-family source bridge actually exposes.
2. Fix the "five residuals" sentence after the six-item residual list.
3. Optionally add one closeout requirement that records whether the evaluated AOI cases are proof-fixture-backed or stronger than that.

## Bottom Line

The revised memo is now materially implementation-ready.

The sequencing is sound, the tranche boundary is honest, and the major hidden constraints from the first pass are now surfaced. I would treat this memo as approved with only minor doc cleanup before execution.
