# Audit: Draft Next Platformization Stages Roadmap

Date: 2026-03-24
Reviewer: Codex
Source memo: `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Overall Verdict

Approve.

The revised draft is now strategically honest relative to the live code and the recent strategy trail. The main issues from the first pass are closed:

- `aoi-canary` is now acknowledged explicitly as an existing thin second consumer
- Stage 13 exit is now split into an honest Tier A / Tier B bar
- Host Contract v1/runtime is no longer overstated as the whole host-neutral story
- the missing structural step is now named correctly as de-AOI / de-`the-critic` transient-substrate work
- the memo now separates the narrow UI-composition vision from the broader analyzer-as-brain platform claim

I would treat this as a good candidate draft roadmap rather than a document that still needs another revision round before it can guide sequencing.

## Concrete Findings

### 1. The Stage 13 Tier A / Tier B split is now honest relative to `aoi-canary` and the transient lock

The memo now frames Tier A as a result-backed second-consumer proof using `aoi-canary` at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L120) and reserves transient-inclusive proof for Tier B at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L244).

That matches the code:

- `aoi-canary` is a real registered consumer with a thin AOI read-only scope at [aoi-canary.json](/home/evgeny/projects/analyzer-v2/src/consumers/definitions/aoi-canary.json#L2)
- the live canary fetches result-backed presenter surfaces directly with `consumer_key=aoi-canary` at [App.tsx](/home/evgeny/projects/aoi-canary/src/App.tsx#L72)
- transient compose is still structurally locked to AOI and `the-critic` at [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L445) and [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L482)
- AOI readiness still encodes the same `the-critic` followup lock at [source_backed_readiness.py](/home/evgeny/projects/analyzer-v2/src/analysis_products/source_backed_readiness.py#L147)

So the new framing is materially better than the earlier “generic host proof first” shape. Tier A is now cheap and honest. Tier B is now correctly gated on structural work that has not happened yet.

### 2. The memo now describes Host Contract v1 and task-launch adoption accurately

The revised draft explicitly says Host Contract v1/runtime is not the whole host-neutral story because task-launch currently sits beside it at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L41).

That matches the implementation:

- Host Contract v1 covers the bounded 11-family run/result/readiness/transient set at [hostContractV1.ts](/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts#L6)
- the shared runtime is authoritative for that family set at [hostContractRuntime.ts](/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts#L185)
- the Stage 8/9 adoption layer is separate and dispatches `route-task` / `plan-task` through `dispatchAnalyzerApiRequest(...)` at [taskLaunchRuntime.ts](/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts#L130)
- the Stage 8/9 completion memo also describes that work as a bounded first adoption slice rather than Host Contract v1 closure at [MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md#L7)

This is the right level of precision.

### 3. The new de-AOI / de-`the-critic` transient-substrate tranche is the right missing structural step

The revised memo now names the main missing bridge concretely at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L76) and gives it its own tranche at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L205).

That is well-supported by the code:

- transient routes still hard-lock both workflow and consumer at [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L445) and [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L482)
- AOI planning still stops at a handoff plan that requires host-side profile choice and downstream `compose-from-source` launch at [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L417) and [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L454)
- the current AOI planner-backed seam in the-critic is real but still bounded to AOI-specific source-backed composition flow at [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L515) and [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L157)

So “planner-to-presentation bridge” remains the right category, but the memo now correctly spells out which bridge components are actually missing.

### 4. AOI exemplar completion before transient-substrate generalization is now defensible

The revised sequence keeps AOI exemplar completion ahead of the de-AOI transient tranche at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L159) and [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L205).

I think that is acceptable for two reasons:

- the current code really does give AOI the strongest composition-facing starting point, because planner-backed AOI handoff is already live in the host at [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L515)
- the canonical roadmap still puts AOI task-driven composition, source/engine-selection law, and AOI guardrails ahead of later bridge/generalization work at [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1120)

The important caveat is already in the memo: AOI completion must stay bounded and must not turn into another long AOI-only branch. The revised draft now says that explicitly at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L193).

### 5. Lifecycle and governance remain deferred at the right point

The draft still defers lifecycle and governance until after stronger bridge and host-neutrality evidence at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L283) and [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L318).

That is still the right call. The underlying reason has not changed:

- transient proof routes and dynamic durable surfaces are not the same thing yet
- broad governance makes more sense once routing/planning/composition contracts are more reusable than they are today

### 6. The memo now distinguishes the narrow vision from the broader platform claim correctly

The revised draft now makes the distinction explicitly at [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L397).

That matches the underlying documents:

- the narrow vision doc is explicitly scoped to UI composition after prose already exists at [DYNAMIC_BESPOKE_APPS_VISION.md](/home/evgeny/projects/analyzer-v2/communications/DYNAMIC_BESPOKE_APPS_VISION.md#L7)
- the broader master roadmap still tracks a much wider platform program including lifecycle and governance at [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1163)

This fix matters because it prevents the roadmap from sounding either falsely “almost done” or falsely “still mostly aspirational.”

## Sequencing Assessment

### Is the revised Stage 13 Tier A / Tier B framing now honest?

Yes.

Tier A matches the real second-consumer state.
Tier B is correctly held behind the transient/source-backed structural blockers.

### Should AOI exemplar completion come before the de-AOI / de-`the-critic` transient-substrate tranche?

Yes, but only as a bounded exemplar-completion move.

The current AOI seam is the best available reference surface, and finishing one honest task-driven exemplar loop before broader generalization is consistent with both the live code and the canonical strategy trail. The memo now keeps that move bounded enough that I would not reverse the order.

### Is the planner-to-presentation bridge still the main structural gap?

Yes.

More specifically, the main gap is now:

- task/planning truth turning into reusable composition truth
- without AOI-only assumptions
- without `the-critic`-only consumer law
- and without requiring host-local analytical reconstruction

The revised draft now states that correctly.

### Are Stage 14 lifecycle and Stage 15 governance deferred at the right point?

Yes.

The draft keeps them behind stronger substrate, bridge, and proof work. That remains the correct boundary.

### Does this preserve the real objective?

Yes.

The sequence still points at the right end state:

- more than one consumer or one truly generic host
- analyzer-owned routing/planning/composition truth
- hosts acting as shells rather than re-embedding workflow intelligence

## Missing Assumptions Or Missing Stages

No blocking missing stage remains after the revision.

The main structural gap that was previously underspecified is now explicit in Tranche 3, and the Host Contract v1 versus task-launch distinction is now explicit in the “Current Strategic Position” section.

## Recommended Revisions Before Canonical Use

No blocking revisions remain.

One optional clarity improvement would still help if this draft is later promoted into the master roadmap:

1. Add one sentence stating that this tranche ordering is a proposed near-term sequencing update relative to the current master-roadmap order, not a claim that the canonical stage ledger has already been changed.

That is a clarity improvement, not a reason to hold approval.

## Bottom Line

The revised draft now says the important things plainly:

- the program is much further along than a thin-host proof
- `aoi-canary` makes a cheap honest Tier A second-consumer proof available
- transient/source-backed composition is still structurally AOI- and `the-critic`-bound
- finishing one bounded AOI exemplar loop still makes sense before broader bridge generalization
- lifecycle and governance should stay behind stronger platform evidence

That is a sound roadmap draft.
