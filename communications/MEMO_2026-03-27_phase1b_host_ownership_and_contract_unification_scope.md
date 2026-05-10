# Memo: Phase 1B Host Ownership And Contract Unification Scope

Subtitle: Lock the analyzer-to-host boundary before Phase 1A bridge implementation

Date: 2026-03-27
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Closeout: `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md`
- `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`
- `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
- `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_scope.md`

## Purpose

Define the next bounded slice after honest Phase 0 closure.

This is not a Phase 1A implementation memo.
It is a Phase 1B decision memo scope: lock the host/analyzer ownership boundary and unify the current contract story before any de-AOI bridge implementation starts.

## Why this is now the next step

Phase 0 is closed.

What the March 27 closeout proved:

- one fresh `execution_backed` AOI case now completes honestly on the real `the-critic` path
- the counted planner-primary browser proof now passes on that fresh run
- the current AOI / `the-critic` surface is strong enough as a bounded exemplar
- it is still not the generalized architecture

That means the next real problem is no longer “can the current AOI exemplar work once honestly?”

It is:

- who owns source identity translation
- who owns local continuity alias / warm snapshot behavior
- who owns surface selection
- who owns navigation and launch handoff semantics
- whether `taskLaunchRuntime` is part of the contract story or a floating sidecar

If those are not decided first, Phase 1A will drift into accidental product behavior, hidden host intelligence, or fake genericity.

## Code-backed current state

The live codebase is explicit enough now that the Phase 1B questions are concrete.

### 1. Host Contract v1 is typed, but not yet the full runtime story

`the-critic/webapp/src/lib/hostContractV1.ts` is a real typed artifact.

It already encodes:

- 11 Host Contract v1 families
- ownership labels for analyzer-direct vs host-proxy families
- canonical identity semantics
- readiness capabilities
- host-surface selection rules

`the-critic/webapp/src/lib/hostContractRuntime.ts` uses that artifact for:

- dispatch mode checks
- required-input validation
- consumer-key threading rules
- readiness capability lookup
- surface-family lookup

But it still does not govern the full planner-to-launch path.

### 2. `taskLaunchRuntime` is live, but adjacent rather than unified

`the-critic/webapp/src/lib/taskLaunchRuntime.ts` is the actual client for:

- `POST /v1/orchestrator/route-task`
- `POST /v1/orchestrator/plan-task`

It dispatches through `dispatchAnalyzerApiRequest(...)`, not through a host-contract family definition.

So today:

- Host Contract v1 is the typed/runtime story for result, readiness, warmup, and source-backed compose families
- `taskLaunchRuntime` is the live runtime story for routing/planning families
- the two stories sit beside each other

That adjacency is exactly what Phase 1B must resolve.

There is also already one backend task-launch consumer, not just the frontend AOI handoff path:

- `the-critic/api/server.py` already implements task-planned genealogy launch by calling:
  - `route-task`
  - registered-corpus sync
  - `plan-task`
  - `/v1/executor/jobs`

So the current task-launch contract story is split across:

- typed host contract/runtime
- frontend `taskLaunchRuntime`
- backend task-planned genealogy launch interpretation
- page-local host navigation/launch code

### 3. The current AOI planner-primary path still mixes host-owned and analyzer-owned law

`the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx` currently owns:

- selected-source row pinning
- readiness check timing
- warm snapshot timing
- planner task submission
- navigation into `/compose-from-intent`
- transport of planner metadata in navigation state

`the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx` currently owns:

- reading URL/search-param source context
- deciding whether the path is profile-backed or planner-backed
- calling `composeFromSource(...)` or `composeFromSelection(...)`

`the-critic/webapp/src/lib/composeFromIntentClient.ts` already uses host-contract runtime helpers for the compose families, but the route shapes remain AOI-specific:

- analyzer-direct `compose-from-intent`
- host-proxy `compose-from-source`
- host-proxy `compose-from-selection`

So the current host path is real, but still AOI-shaped and page-local in important ways.

### 4. Source identity and continuity alias behavior are still materially host-owned

`the-critic/api/server.py` currently does real host-side work in `_resolve_source_backed_compose_identity(...)`.

That helper resolves:

- `source_analysis_id`
- `source_v2_job_id`
- project + thinker scope
- backfill between saved AOI rows and durable upstream job identity
- local continuity alias reuse

That is not incidental glue.
It is active contract behavior.

The Phase 1B memo must decide whether that remains host-owned law, moves upstream, or stays host-owned but becomes more explicitly delimited.

### 5. The analyzer transient boundary is still AOI-bound and `the-critic`-bound

`src/presenter/compose_from_intent.py` still hard-validates:

- `workflow_key == anxiety_of_influence_thematic_single_thinker`
- `consumer_key == the-critic`

Those checks are not only one generic gate.
They are currently enforced in three concrete validators:

- `_validate_request()`
- `_validate_source_request()`
- `_validate_selection_request()`

So Phase 1A cannot honestly start by “just opening the validators.”

Phase 1B must first define the reusable handoff boundary that Phase 1A is allowed to generalize toward.

## The key Phase 1B tension that now has to be resolved explicitly

There is a real unresolved identity doctrine split across recent work:

1. Stage 7 correctly preserved the product-facing host identity seam:
   - project id
   - thinker id
   - saved-result identity / `source_analysis_id`
2. Stage 13 Host Contract v1 correctly records canonical upstream truth for source-backed launch as `upstream_v2_job_id`, with `source_analysis_id` acting as host-local continuity alias
3. The March 27 Phase 0 closeout proved the fresh path using both ids together:
   - `source_v2_job_id` as canonical upstream source truth
   - `source_analysis_id` as stable host continuity alias

Phase 1B must reconcile that explicitly.

It should not leave future implementors guessing whether the product contract is:

- alias-first
- canonical-id-first
- or permanently dual-identity

There is also one formal-versus-practical gap in the current contract artifact that Phase 1B must settle explicitly:

- `hostContractV1.ts` models `source_backed_transient_launch.required_inputs` as:
  - `project_id`
  - `selected_source_thinker_id`
  - `variant`
- but the live host runtime practically requires at least one of:
  - `source_analysis_id`
  - `source_v2_job_id`
  - or a resolvable latest saved-result context

So the open question is not whether analyzer-v2 should accept dual canonical truth.
It is whether the product-facing contract should continue to thread both ids for host continuity support, and how explicitly that requirement should be represented in the contract layer.

## Source-mode scoping note

`taskLaunchRuntime` already carries two live source modes:

- `saved_result`
- `registered_corpus`

Phase 1B should cover both at the contract-boundary level, because both already pass through the same routing/planning story.

But the depth of decision is different:

- for `saved_result`, Phase 1B must settle the canonical-id versus continuity-alias doctrine directly
- for `registered_corpus`, Phase 1B must at minimum decide ownership of:
  - corpus identity translation
  - planner-contract interpretation
  - backend followup execution semantics

Phase 1B does not need to redesign registered-corpus planning.
It does need to stop pretending the live task-launch contract only exists for AOI saved-result identity.

## Scope of this slice

This slice is decision-only.

It should produce one code-backed ownership and contract memo that answers the Phase 1B questions cleanly enough that Phase 1A implementation can start without re-litigating boundary law.

### Must land

1. One explicit ownership decision for source identity translation.
2. One explicit ownership decision for warm-snapshot / continuity-alias behavior.
3. One explicit ownership decision for surface selection.
4. One explicit ownership decision for navigation / launch-handoff semantics.
5. One explicit decision on the relation between `taskLaunchRuntime` and the host contract story.
6. One explicit separation between:
   - host-neutral run/result/readiness law
   - planner-advisory / task-launch law
   - composition-facing transient/source-backed law
7. One current-state inventory of the actual call path for:
   - AOI planner-primary source-backed transient launch
   - one result-backed workspace path
   - the already-live backend genealogy registered-corpus task-planned launch path
8. One explicit decision on reload / deep-link / share durability for planner-backed handoff state:
   - what must survive in the URL or recoverable state
   - what is allowed to remain ephemeral browser navigation state
9. One explicit list of invariants that Phase 1A must preserve.

### Must not widen

- do not implement Phase 1A in this slice
- do not add new transient endpoints
- do not add non-AOI materialization yet
- do not reopen lifecycle/session/share/save law
- do not turn this into a second-consumer proof slice
- do not do app-local UX cleanup that is not required to settle ownership
- do not hide unresolved decisions behind “Host Contract v2” branding alone

## Working hypotheses this memo should test

These are starting hypotheses, not locked conclusions.

### Hypothesis 1: source identity translation stays host-owned

Default hypothesis:

- the host owns translation from project/thinker/saved-result context into canonical upstream `source_v2_job_id`
- analyzer-facing transient composition should still receive canonical upstream identity, not opaque host aliases
- host-local `source_analysis_id` remains continuity support, not upstream truth

Why this is plausible:

- the-critic already owns project-scoped saved-result rows and alias reuse
- the current proxy layer already enforces project + thinker context honestly
- moving this upstream too early risks re-embedding host persistence concerns inside analyzer-v2

### Hypothesis 2: warm snapshot / continuity alias stays host-owned

Default hypothesis:

- local snapshot materialization and continuity alias behavior remain host responsibilities
- upstream run/result/presentation truth remains analyzer-owned

Why this is plausible:

- Host Contract v1 already models `cache_snapshot_warmup` as host-proxy behavior
- the host owns local DB state and restore continuity for current product surfaces

### Hypothesis 3: surface selection stays host-owned, but becomes executable contract law

Default hypothesis:

- the host still decides which host surface to render or navigate to
- but it should do so through typed contract/runtime law, not page-local branching
- analyzer routing/planning should declare launch contract kind and required preparation, not page routes

Why this is plausible:

- current host surfaces are still product/UI-specific
- `hostContractV1.ts` already records surface selection rules as host-owned

### Hypothesis 4: navigation / launch handoff semantics stay host-owned

Default hypothesis:

- analyzer returns:
  - routing outcome
  - planning outcome
  - downstream followup contract
  - required host preparation
- host owns:
  - URL construction
  - navigation
  - search params / state threading
  - autostart timing

Why this is plausible:

- page routing and browser state are still host concerns
- analyzer should not need to synthesize current-consumer paths to be “the brain”

### Hypothesis 5: `taskLaunchRuntime` should not remain a floating sidecar, but it may need to stay a distinct planner-advisory layer

Default hypothesis:

- `route-task` and `plan-task` belong inside one authoritative analyzer-to-host contract suite
- but they may need to remain a distinct planner-advisory subcluster rather than being flattened into ordinary delivery families

So the concrete Phase 1B question should be:

- should `route-task` and `plan-task` become named contract families with explicit ownership, identity, and input requirements in the same family table
- or should they remain outside that family table as a bounded planner-advisory layer with its own explicit contract artifact and mapping onto delivery/runtime families?

What should not happen:

- `taskLaunchRuntime` remaining a separate implicit contract with no bounded relation to Host Contract v1

## The real questions Phase 1B must answer

1. What is the canonical source identity at the analyzer boundary?
2. What is the canonical source identity at the product boundary?
3. Is dual-id threading temporary or stable law?
4. Which exact behaviors are continuity-alias responsibilities rather than analyzer truth?
5. Should surface selection remain host-owned in v2, or should analyzer launch contracts begin naming executable host surfaces?
6. Are `route-task` and `plan-task` part of the host contract proper, or a bounded pre-contract advisory layer?
7. Who is allowed to interpret `downstream_followup_contract` today, and where should that interpretation live after Phase 1B?
8. What planner-backed launch state must survive reload, deep-link, or share, and what may remain ephemeral browser state?
9. Which launch semantics are allowed to remain page-owned after Phase 1B, and which must move into shared runtime?
10. What exact invariants must Phase 1A preserve while generalizing away from AOI-specific compose entry?

## Recommended deliverable shape

The Phase 1B output should be one memo, not code.

That memo should contain at minimum:

1. A one-page ownership matrix.
2. A current-path call graph for the live AOI planner-primary handoff.
3. A current-path call graph for one result-backed workspace path.
4. A current-path call graph for the already-live backend genealogy registered-corpus task-planned launch path.
5. One explicit decision on `taskLaunchRuntime` versus Host Contract v2.
6. One explicit decision on canonical identity versus host continuity alias.
7. One explicit decision on reload / deep-link durability for planner-backed handoff state.
8. One list of Phase 1A implementation permissions.
9. One list of things Phase 1A is forbidden to do without reopening Phase 1B.

Each call-path inventory must be deep enough to name:

- every hop
- every identity translation point
- every hardcoded workflow or consumer constraint
- every place where host code interprets analyzer-returned contracts
- every place where navigation state or URL state becomes semantically significant

## Acceptance criteria

Phase 1B is decision-complete only if a future implementor can answer all of the following without guessing:

- When a host has only `source_analysis_id`, who is allowed to resolve canonical `source_v2_job_id`?
- When a host already has `source_v2_job_id`, is `source_analysis_id` still required, optional, or deprecated?
- Who owns snapshot warmup and local alias creation?
- Who owns host-surface selection?
- Who owns navigation and browser-state handoff?
- Are `route-task` and `plan-task` contract families now, or a distinct planner-advisory layer with an explicit relation to the delivery contract?
- Who owns interpretation of `downstream_followup_contract` on both the frontend AOI path and the backend genealogy path?
- What planner-backed handoff information must survive reload or deep-link?
- What parts of the current AOI path are reusable host/runtime law versus bounded AOI residue?
- What parts of the current registered-corpus task-launch path are reusable host/runtime law versus bounded genealogy residue?
- What exactly is Phase 1A allowed to generalize next?

If those answers are still fuzzy, Phase 1B is not done.

## Why this is the honest next slice

This memo keeps the program aligned with the fixed direction:

- Phase 0 proved the exemplar honestly
- Phase 1B decides the boundary
- Phase 1A can then generalize the bridge against a locked boundary

Skipping Phase 1B would push unresolved host/analyzer ownership questions into implementation, which is exactly how the program keeps producing sidecar law instead of reusable platform law.
