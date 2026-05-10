# Memo: Phase 1B Host Ownership And Contract Unification Decision

Subtitle: Lock Host Contract v2 layering, identity doctrine, and adapter points before Phase 1A

Date: 2026-03-27
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Closeout: `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
Scope Memo: `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_scope.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md`
- `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`
- `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
- `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_scope.md`

## Outcome

Phase 1B is now decision-complete.

This memo locks:

- the authoritative contract structure for the next slice
- the ownership split between analyzer truth and host execution
- the canonical identity doctrine
- the named adapter points where the host is allowed to interpret analyzer-returned contracts
- the durability rules for planner-backed handoff state
- the invariants that Phase 1A must preserve

This is a docs-only decision slice.
It does not change code, routes, or schemas.
Its purpose is to make Phase 1A implementable without new boundary decisions.

## Code-backed basis

These decisions are grounded in the current live code, not only in roadmap prose.

Primary files inspected for this decision:

- `the-critic/webapp/src/lib/hostContractV1.ts`
- `the-critic/webapp/src/lib/hostContractRuntime.ts`
- `the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `the-critic/webapp/src/lib/composeFromIntentClient.ts`
- `the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`
- `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `the-critic/api/server.py`
- `src/orchestrator/task_router.py`
- `src/orchestrator/task_planner.py`
- `src/presenter/compose_from_intent.py`

## Final decisions

### 1. Host Contract v2 is one contract suite with two explicit layers

The next contract story is one authoritative suite, not two sidecar stories.

That suite must have two explicit layers:

1. planner-advisory layer
   - `route-task`
   - `plan-task`
2. delivery/runtime layer
   - run/result/readiness/view families
   - source-backed transient compose families
   - cache warmup

Decision:

- `route-task` and `plan-task` do belong inside the authoritative Host Contract v2 story
- they must not remain an implicit sidecar represented only by `taskLaunchRuntime`
- they also must not be flattened into the ordinary delivery/runtime family table

Reason:

- planner surfaces have different authority and identity semantics from delivery/runtime families
- their outputs are not content delivery payloads or launch results
- they return advisory planning truth, required host preparation, and downstream followup contracts
- they already serve both `saved_result` and `registered_corpus` source modes, which do not share one simple family identity model

Required implementation implication for Phase 1A:

- Host Contract v2 should have one artifact and one runtime story, but with a distinct `planner_advisory` section rather than a single flat family table
- `taskLaunchRuntime` should become the runtime implementation of that planner-advisory layer or be replaced by one shared contract-owned runtime
- it must not remain a separate contract story

### 2. Canonical identity doctrine is asymmetric dual-threading

There is not dual upstream truth.

Decision:

- canonical analyzer boundary identity for saved-result planning and source-backed transient compose is `source_v2_job_id`
- `source_analysis_id` is a host continuity alias only
- the product boundary may thread both ids, but asymmetrically:
  - `source_v2_job_id` is truth
  - `source_analysis_id` is host continuity support

Concrete law:

- if the host has only `source_analysis_id`, the host must resolve canonical `source_v2_job_id` before calling analyzer planning or compose
- if the host already has `source_v2_job_id`, `source_analysis_id` is optional and must not be treated as canonical truth
- the host may still carry `source_analysis_id` to support local snapshot continuity, warm alias reuse, and legacy saved-result rows
- analyzer-facing transient compose and saved-result planning stay canonical-id-first

This settles the current formal/practical gap in Host Contract v1:

- `source_backed_transient_launch.required_inputs` may remain minimal at the family-table level
- but the runtime and ownership law must explicitly acknowledge that the live host path often starts from alias-only context and resolves canonical identity before launch

### 3. Host owns continuity and browser execution

Decision:

- host owns project/thinker/saved-result translation into canonical upstream identity
- host owns warm snapshot materialization and continuity alias creation
- host owns surface selection
- host owns navigation, query construction, return-path handling, and browser handoff timing
- analyzer owns routing/planning truth and followup-contract semantics
- host owns the bounded interpretation and execution of those contracts at named adapter points only

This means:

- analyzer does not own current-consumer page paths
- analyzer does not own browser navigation
- analyzer does not own local DB alias creation
- host does not reinterpret planner truth or synthesize alternate source selections locally

### 4. Registered-corpus task launch is part of the same contract story

Decision:

- the already-live backend genealogy `registered_corpus` path is first-class Phase 1B scope
- it is not an exception outside the contract story

Concrete law:

- host owns corpus identity translation from project docs to `external_project_id` and `external_doc_key` space
- host owns document sync and backend followup execution
- analyzer owns routing/planning truth and execution-plan semantics
- backend execution of `downstream_followup_contract` is allowed only at the named genealogy adapter point

### 5. Planner-backed handoff must survive reload and deep-link without semantic `location.state`

Decision:

- no planner-backed datum required to reproduce the handoff may remain `location.state`-only after Phase 1A
- `location.state` may remain a display cache only

Minimum durable rule:

- reload and deep-link must preserve enough information to reproduce the planner-backed handoff honestly
- share in this phase means the same route can be reopened or copied and still replay the same handoff law; it does not imply lifecycle/session publishing

Durability classification is fixed in the table below.

## Public surfaces covered by this decision

The Host Contract v2 story this memo authorizes must explicitly cover these live public surfaces:

- analyzer `POST /v1/orchestrator/route-task`
- analyzer `POST /v1/orchestrator/plan-task`
- analyzer run/result/readiness/view families already represented in Host Contract v1
- analyzer `POST /v1/presenter/compose-from-intent`
- analyzer `POST /v1/presenter/compose-from-source`
- analyzer `POST /v1/presenter/compose-from-selection`
- host proxy `POST /api/analysis/anxiety_of_influence_thematic_single_thinker/projects/{project_id}/compose-from-source`
- host proxy `POST /api/analysis/anxiety_of_influence_thematic_single_thinker/projects/{project_id}/compose-from-selection`

This memo's main live-path inventory focuses on the planner-primary selection branch, because that is the branch carrying the unresolved handoff durability and contract-interpretation questions.
But Phase 1A must preserve the fact that the source-backed transient launch layer currently includes both:

- legacy/profile launch through `compose-from-source`
- planner-primary launch through `compose-from-selection`

## Ownership matrix

| Behavior | Owner | Canonical truth | Named adapter points |
| --- | --- | --- | --- |
| Source identity translation from project/thinker/saved-result context | Host | `source_v2_job_id` once resolved | AOI saved-result selection merge, `_resolve_source_backed_compose_identity(...)` |
| Local continuity alias and warm snapshot | Host | `source_analysis_id` is alias only | `cache_snapshot_warmup`, `warmSnapshotForSource(...)` |
| Routing truth | Analyzer | `route-task` response | frontend AOI planner request, backend genealogy task launch |
| Planning truth | Analyzer | `plan-task` response | frontend AOI planner request, backend genealogy task launch |
| Followup-contract semantics | Analyzer | `downstream_followup_contract` meaning | none outside named host adapter points |
| Followup-contract execution | Host | bounded execution only | `AoiV2ThematicPanel`, `AoiComposeFromIntentPage`, `_start_genealogy_v2_run_sync(...)` |
| Result/run/readiness/presentation truth | Analyzer | run/result/readiness payloads | `boundedV2Client.ts`, `useBoundedV2Workspace.ts` |
| Surface selection | Host | host contract/runtime | AOI thematic page, generic workspace path |
| Browser navigation and URL law | Host | host route semantics | `navigate(...)`, query params, `return_to`, `origin` |
| Registered-corpus translation and sync | Host | host-managed project docs mapped to external doc ids | `_build_genealogy_registered_corpus_launch_payload(...)`, `sync_documents_sync(...)` |

## Live path inventory

## Path A: AOI planner-primary saved-result transient handoff

### Public contract surfaces

- analyzer `POST /v1/orchestrator/route-task`
- analyzer `POST /v1/orchestrator/plan-task`
- host proxy `POST /api/analysis/{workflow_key}/cache-v2/{v2_job_id}`
- host proxy `POST /api/analysis/anxiety_of_influence_thematic_single_thinker/projects/{project_id}/compose-from-selection`
- analyzer `POST /v1/presenter/compose-from-selection`

### Internal helper hops

- `AoiV2ThematicPanel` merges analyzer result discovery with local saved-result rows and continuity aliases
- `selectedSource` is chosen at the page layer
- `warmSnapshotForSource(...)` materializes or reuses `source_analysis_id`
- `navigate(...)` carries a mixed URL + `location.state` handoff into `/compose-from-intent`
- `AoiComposeFromIntentPage` reads query params plus planner metadata from `location.state`
- `composeFromIntentClient.composeFromSelection(...)` calls the host proxy route
- `server._resolve_source_backed_compose_identity(...)` resolves or validates `source_v2_job_id`
- analyzer `compose_from_selection(...)` still hard-validates:
  - `workflow_key == anxiety_of_influence_thematic_single_thinker`
  - `consumer_key == the-critic`

### Identity story

Current live inputs:

- project id
- selected thinker id and name
- optional `source_analysis_id`
- canonical `source_v2_job_id`
- planner task text

Current live output chain:

- `route-task` advisory routing truth
- `plan-task` `aoi_composition_handoff_plan`
- host-created or reused `source_analysis_id`
- host-proxied analyzer selection compose response

### Hardcoded constraints

- AOI workflow key is fixed in the panel and compose page
- consumer key is fixed to `the-critic`
- analyzer transient compose validators remain AOI-only and `the-critic`-only
- the current compose page treats planner-backed state as mixed URL + `location.state` truth

### Decision implications

- this path is real but not yet reusable host/runtime law
- the host is allowed to interpret planner outcomes only at named adapter points:
  - `AoiV2ThematicPanel.handlePlannerBackedPlan(...)`
  - `AoiV2ThematicPanel.launchPlannerBackedCompose(...)`
  - `AoiComposeFromIntentPage.runPlannerBackedCompose(...)`
- those adapter points may not reinterpret selection truth or invent alternate source families
- Phase 1A must remove semantic dependence on `location.state` for planner-backed handoff data

## Path B: Genealogy result-backed workspace path

### Public contract surfaces

- analyzer `GET /v1/runs/discovery`
- analyzer `GET /v1/results/discovery`
- analyzer `GET /v1/results/by-job/{job_id}`
- analyzer `GET /v1/results/by-job/{job_id}/presentation`
- analyzer `POST /v1/results/by-job/{job_id}/refresh-presentation`
- analyzer `GET /v1/presenter/view/{job_id}/{view_key}`
- analyzer `GET /v1/results/by-job/{job_id}/source-backed-readiness`

### Internal helper hops

- `AnalysisWorkspacePage` reads `workflowKey`, `projectId`, and optional `composition_mode` from URL
- `useBoundedV2Workspace(...)` decides whether to show current run, default presentation, or requested composition-mode presentation
- `displayCompositionMode` is derived locally from analyzer readiness rather than copied directly from the requested URL mode
- local saved-result rows may contribute `analysis_id` fallback for continuity or snapshot fallback, but not result truth
- `loadLocalSnapshot(...)` is host-local snapshot recovery, not upstream presentation authority

### Identity story

- canonical result identity is `v2_job_id`
- local `analysis_id` is continuity support only
- `composition_mode` is a host-owned selector carried in the URL

### Hardcoded constraints

- this path already uses host contract runtime and bounded client helpers
- genealogy workspace surface selection is host-owned
- requested blocked composition modes remain URL-visible while `displayCompositionMode` can fall back to default content

### Decision implications

- this path is the current proof that result-backed consumption already lives mostly in delivery/runtime law
- Phase 1A should preserve:
  - analyzer-owned readiness truth
  - host-owned `requestedMode` versus `displayMode` selection law
  - canonical `v2_job_id` truth over local alias continuity

## Path C: Backend genealogy `registered_corpus` task-planned launch

### Public contract surfaces

- analyzer `POST /v1/orchestrator/route-task`
- analyzer `POST /v1/orchestrator/plan-task`
- analyzer `POST /v1/executor/jobs` as the semantic downstream contract target

### Internal helper hops

- `_build_genealogy_registered_corpus_launch_payload(...)` translates host project docs into external document identifiers and sync payloads
- `sync_documents_sync(...)` hydrates analyzer registered-corpus state
- `_build_genealogy_task_route_request(...)` builds routing inputs
- `_build_genealogy_task_plan_request(...)` builds planning context
- `_start_genealogy_v2_run_sync(...)` verifies planning outcome, verifies `downstream_followup_contract.endpoint == /v1/executor/jobs`, extracts `plan_id`, and then starts execution via `start_job_from_plan_sync(...)`

### Identity story

- host-side document ids and project docs are translated into:
  - `external_project_id`
  - `target_external_doc_key`
  - prior-work external doc keys
  - context external doc keys
- planner output returns `workflow_execution_plan`, `hydrated_document_ids`, and semantic executor followup contract
- canonical run identity becomes upstream `plan_id` then upstream `job_id`

### Hardcoded constraints

- task-planned mode is currently limited to `intellectual_genealogy`
- it requires the registered-corpus by-ref path
- it does not support targeted ideas or model overrides

### Decision implications

- this path proves planner surfaces already have a second consumer and second source mode
- the host currently executes analyzer followup contracts at a backend adapter point rather than a generic dispatcher
- Phase 1A must preserve that bounded adapter model while making the contract law explicit

## Followup-contract interpretation law

The phrase "analyzer owns followup-contract semantics" is easy to over-read.

The actual law is:

- analyzer defines routing truth, planning truth, and the semantic meaning of the returned followup contract
- host owns the bounded interpretation and execution of that contract only at named adapter points

Named adapter points after this memo:

- frontend AOI planning adapter:
  - receives `route-task` and `plan-task`
  - may decide whether the planner result is blocked, insufficient, or launchable
  - may not alter selected source families or replace analyzer planning truth
- frontend AOI compose adapter:
  - may warm local snapshot state
  - may construct the compose-page route
  - may execute the host proxy compose route
- backend genealogy task-launch adapter:
  - may sync registered-corpus documents
  - may verify the returned executor followup contract
  - may execute the plan through the backend analyzer client

No other page-local code should interpret `downstream_followup_contract` semantically after Phase 1A.

## Durability classification for planner-backed handoff

This table is now the Phase 1A requirement.

| Datum | Classification | Rule |
| --- | --- | --- |
| `selected_source_thinker_id` | URL-carried | Required in the route or query for source-backed AOI handoff |
| `source_v2_job_id` | URL-carried | Required canonical source identity for planner-backed replay |
| planner task text | URL-carried | Required to recompute planner-backed handoff after reload or deep-link |
| `origin` | URL-carried | Host navigation semantics |
| `return_to` | URL-carried | Host navigation semantics |
| `selected_source_thinker_name` | recoverable | Convenience only; recover from saved-result/run context if absent |
| `source_analysis_id` | recoverable | Host continuity alias only; may be URL-carried as an optimization, but must not be required truth |
| planner selected sources | recoverable | Recompute from `plan-task` using URL-carried canonical source identity plus task |
| planner rejected sources | recoverable | Recompute from `plan-task` |
| planner selection summary | recoverable | Recompute from `plan-task` |
| planner resolved intent seed | recoverable | Recompute from `plan-task`; do not rely on `location.state` only |
| planner allowed/blocked profiles | recoverable | Recompute from `plan-task` |
| planner legacy profile equivalent | recoverable | Recompute from `plan-task` |
| transient banners, open panels, temporary notices | ephemeral-by-design | UI-only state may remain local |

Implication:

- the current `location.state` planner payload is acceptable only as a temporary display cache
- it is not acceptable as the semantic source of truth after Phase 1A

## Phase 1A permissions

Phase 1A may now:

- replace AOI-only transient entry constraints with reusable contract checks
- move planner-backed handoff state out of semantic `location.state`
- bring planner-advisory runtime under one authoritative Host Contract v2 story
- introduce a shared host/runtime resolver for source-backed transient compose launch
- make host-owned surface selection executable through shared runtime law instead of page-local branching
- preserve host proxy execution where host identity translation or continuity alias behavior is still required

## Phase 1A forbidden moves

Phase 1A must not:

- treat `source_analysis_id` as canonical analyzer truth
- allow page-local code to reinterpret analyzer source selection truth
- weaken AOI validators without replacing them with reusable handoff contract checks
- omit the `registered_corpus` genealogy path from the contract story
- widen into lifecycle/session/share publication semantics
- widen into second-consumer proof or non-AOI materialization beyond the bounded Phase 1 objective
- flatten planner-advisory surfaces into ordinary result/readiness families if that erases their distinct ownership and identity semantics

## Explicit answers to the acceptance questions

When the host has only `source_analysis_id`, the host resolves canonical `source_v2_job_id`.

When the host already has `source_v2_job_id`, `source_analysis_id` is optional continuity support only.

Snapshot warmup and local alias creation stay host-owned.

Host-surface selection stays host-owned.

Navigation and browser-state handoff stay host-owned.

`route-task` and `plan-task` become part of the Host Contract v2 suite as a distinct planner-advisory layer, not an unrelated sidecar and not an ordinary delivery family.

Interpretation of `downstream_followup_contract` is owned by named host adapter points only:

- frontend AOI planner/compose adapters
- backend genealogy task-launch adapter

Planner-backed handoff must survive reload and deep-link through URL-carried canonical identity plus task, with planner outputs recoverable and not `location.state`-only.

Reusable host/runtime law today already includes:

- result/run/readiness consumption through the bounded client/runtime path
- host-owned identity translation and snapshot warmup
- bounded adapter execution of analyzer followup contracts

Bounded AOI residue today still includes:

- AOI workflow and consumer hard constraints in analyzer transient compose validators
- AOI-specific compose page and proxy route shapes
- current planner metadata threaded through `location.state`

Reusable host/runtime law in the registered-corpus path includes:

- host-side corpus translation
- route-task / plan-task interpretation at a named backend adapter point
- execution-plan launch through analyzer plan/job primitives

Bounded genealogy residue still includes:

- current task-planned launch restrictions
- genealogy-specific payload builders and launch validation

## Final judgment

The contract boundary is now locked strongly enough for Phase 1A to start.

The key result of Phase 1B is not a new name for the same split.
It is this:

- there is one contract suite
- planner advisory is a real layer inside it
- canonical identity is `source_v2_job_id`
- `source_analysis_id` is continuity alias only
- host owns translation, continuity, surfaces, and browser execution
- analyzer owns planning truth and followup semantics
- planner-backed handoff may no longer depend semantically on `location.state`

That is the boundary law Phase 1A must now implement against.
