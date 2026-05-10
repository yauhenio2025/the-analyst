# Report: Codex Fixed-Direction Phased Roadmap Audit

Date: 2026-03-26
Verdict: Approve with revisions

## Bottom Line

This is the right fixed direction from the current state. The program should finish the AOI exemplar honestly, then shift the main line to planner-to-presentation generalization, then prove host-neutral transient consumption, then define lifecycle, and only after that add governance. That order is stronger than the still-canonical master order that brings lifecycle earlier.

The approval should be conditional on tightening the roadmap where it currently understates the remaining distance from the real goal. The codebase now has real upstream routing and planning seams, but transient composition is still structurally AOI- and `the-critic`-bound, and the host still owns meaningful launch, identity, and surface behavior.

## Findings

### High: Phase 1 exit criteria are too weak for the actual code distance

The memo's Phase 1 exit only requires the transient/planner-to-presentation substrate to stop being structurally single-workflow-only and single-consumer-only (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:133-150`). That is necessary, but it is not sufficient for the stated "analyzer-v2 is the brain" goal.

- `src/presenter/compose_from_intent.py` is not just entry-gated to AOI and `the-critic`; it is internally AOI-shaped. The module declares itself "Bounded transient compose-from-intent orchestration for AOI," hard-codes `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"`, embeds AOI default intents, and maps AOI engine keys to semantic roles and patterns (`src/presenter/compose_from_intent.py:1`, `src/presenter/compose_from_intent.py:54-114`).
- All three transient entry points hard-fail unless `workflow_key == AOI_WORKFLOW_KEY` and `consumer_key == "the-critic"` (`src/presenter/compose_from_intent.py:496-560`).
- The planner substrate is real but still bounded. `src/orchestrator/task_router.py` only supports two objective families and a narrow source-mode matrix (`src/orchestrator/task_router.py:21-43`, `src/orchestrator/task_router.py:172-224`, `src/orchestrator/task_router.py:387-395`). `src/orchestrator/task_planner.py` branches only between genealogy execution planning and AOI handoff planning (`src/orchestrator/task_planner.py:88-147`, `src/orchestrator/task_planner.py:333-596`).
- Host Contract v1 still records transient compose as structurally tied to `the-critic`, while source-backed transient launch and cache warmup remain `host_proxy`, and surface selection remains `host_owned_v1` (`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:187-245`, `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:272-313`).

Revision required:

- Do not let Phase 1 close on removal of the hard `workflow_key` and `consumer_key` locks alone.
- Require one reusable planner-to-presentation handoff contract that is not AOI semantic law in disguise.
- Require one non-AOI materialization path through that contract.
- Require an explicit decision on which remaining host responsibilities are truly stable host obligations.

### High: The transient seam is still materially host-owned, and task launch still sits beside Host Contract v1, so Phase 2 cannot be treated as only a proof exercise

The memo correctly says task launch and Host Contract v1 still sit beside each other (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:123-140`), but it underweights how much analytical behavior still lives in the host.

- `AoiV2ThematicPanel.tsx` directly calls `routeTask(...)` and `planTask(...)`, interprets `unsupported` and `insufficient_context`, holds the selected saved-result identity, warms the snapshot locally, performs readiness checks, and navigates to `/compose-from-intent` with planner-selected state in navigation memory (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:573-741`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:744-810`).
- `taskLaunchRuntime.ts` is a typed transport shim over `/v1/orchestrator/route-task` and `/v1/orchestrator/plan-task`, while `hostContractV1.ts` separately encodes families, readiness capability, and host-surface rules. That is real progress, but it is still adjacency, not one coherent lifecycle/host law (`/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:154-189`, `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:75-85`, `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:344-365`).
- Host Contract v1 explicitly says the AOI source-backed transient launch experience is host-owned for source identity resolution, readiness gating, and proxy launch sequencing, and that the genealogy result-backed workspace still owns mode selection and blocked-mode fallback display (`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:288-313`).

Revision required:

- Add an explicit Phase 1 work item for ownership resolution of source identity translation.
- Add an explicit Phase 1 work item for ownership resolution of warm-snapshot and continuity-alias behavior.
- Add an explicit Phase 1 work item for ownership resolution of surface selection.
- Add an explicit Phase 1 work item for ownership resolution of navigation and launch-handoff semantics.
- Add an explicit Phase 1 work item to either unify task-launch runtime semantics into the host contract or deliberately define why they remain separate layers.

Without that, Phase 2 risks proving only that a second consumer can reproduce the same host-owned analytical glue.

### Medium: The anti-drift rules are directionally right, but not enforceable enough

The anti-drift rules correctly target app-local polish and downstream compensation (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:40-76`). The weakness is that they are not yet strong enough to stop the two current drift modes:

- analyzer-side AOI accretion that masquerades as reusable platform law
- host-side analytical branching that gets justified as "stable host contract"

Current code already shows both risks.

- AOI planning is still AOI-family-specific and depends on an AOI source-selection LLM prompt (`src/orchestrator/task_planner.py:33-53`, `src/orchestrator/task_planner.py:428-596`, `src/orchestrator/task_planner.py:727-760`).
- AOI transient composition still contains AOI-specific semantic-role and pattern law (`src/presenter/compose_from_intent.py:61-114`).
- Host surface rules are still host-owned (`/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:272-313`).

Revision required:

- Require every post-Phase-0 host change to name the exact Host Contract family it belongs to or the analyzer-side contract it shrinks.
- Require every new AOI-specific analyzer change to carry either a planned generalization target or an explicit deletion condition.
- Reject any change that increases host-owned analytical branching unless it removes a larger downstream branch at the same time.

### Medium: The roadmap is better than the canonical order, but it must be merged back into the canonical roadmap quickly

This fixed-direction memo moves lifecycle and governance behind bridge generalization and host-neutral proof (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:183-235`, `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:248-256`). That is an improvement over the current canonical roadmap, which still recommends making the lifecycle decision before the broader planner/host generalization sequence (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1128-1143`).

If this memo is accepted but the canonical roadmap is not updated, the program will keep two incompatible strategic orders alive at once.

Revision required:

- Add an immediate follow-on action to update the canonical master roadmap and stage ledger after roadmap approval.

## Direct Answers

1. Is the memo’s phase ordering the best available sequencing from the current state?

Yes, with the revisions above. The March 26 Stage 5 closeouts still show Stage 2 open and Tranche 3 blocked pending one fresh post-fix AOI rerun (`communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md:31-38`, `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_completion.md:25-29`, `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_completion.md:163-174`). From that state, Phase 0 before generalization is correct. Lifecycle and governance should stay later.

2. Does it correctly separate immediate exemplar honesty work, architectural generalization work, and later lifecycle/governance work?

Yes. This is one of the memo’s main strengths. It is materially clearer than the older canonical order and the March 24 draft roadmap about what is proof maintenance versus architecture.

3. Are the anti-drift rules strong enough?

Not yet. They need explicit acceptance tests for host-side changes and analyzer-side AOI accretion, or the program can still drift while technically claiming compliance.

4. Does the memo overstate how close the current codebase is to host-neutral planner-to-presentation behavior?

Somewhat. It is accurate that real routing, planning, readiness, and host-contract progress exists (`src/api/routes/orchestrator.py:301-326`, `src/orchestrator/task_router.py:58-140`, `src/orchestrator/task_planner.py:88-147`). But the current code is still well short of host-neutral planner-to-presentation behavior because transient composition remains AOI-shaped upstream, launch and surface semantics still live significantly in the host, and the host still carries a separate task-launch runtime beside Host Contract v1 rather than consuming one unified analyzer-to-host law (`src/presenter/compose_from_intent.py:1-114`, `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts:154-189`, `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:187-313`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:573-810`).

5. What is missing from the roadmap?

- a stronger Phase 1 exit bar that requires reusable planner-to-presentation law, not just removal of two hard locks
- an explicit ownership decision for source identity translation, continuity warmup, surface selection, and navigation/handoff semantics
- an explicit decision on whether task-launch runtime becomes part of the host contract or remains a separate bounded layer with named responsibilities
- enforceable anti-drift gates for host changes and AOI-specific analyzer changes
- immediate reconciliation with the canonical master roadmap

## Final Judgment

Approve with revisions.

The fixed direction is right: finish the AOI exemplar honestly, then make the planner-to-presentation bridge host-neutral, then prove broader transient consumption, then decide lifecycle, then add governance. That is the best current sequence for reaching the actual platform goal. The needed revisions are about honesty of distance and exit criteria: the codebase has real upstream movement, but it is still substantially more AOI-shaped and host-owned than a simple de-locking exercise would suggest.
